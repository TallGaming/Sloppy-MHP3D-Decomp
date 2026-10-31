#!/usr/bin/env python3
"""Compare two reviewed C-source alternatives with a frozen full-bench baseline.

The same pinned builds/settings compile every cohort. Only the declared body
may differ, and every unchanged function must retain its compiled bytes. This
is a controlled source experiment, not original-source or matching credit.
"""

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

try:
    from .bench_compiler import run_bench
    from .prepare_reference import file_identity, check_identity, reject_link, write_report
except ImportError:
    from bench_compiler import run_bench
    from prepare_reference import file_identity, check_identity, reject_link, write_report


ROOT = Path(__file__).resolve().parents[1]


def sha256(data):
    """Hash exact bytes, preserving the source's original line endings."""
    return hashlib.sha256(data).hexdigest()


def body_span(source, function_name):
    """Locate one ordinary C definition, including its braces, without rewriting.

    This bounded research helper recognizes comments and quoted literals so
    their braces cannot alter the result. It is not a general C parser; these
    header-free sources contain no preprocessor directives or complex declarators.
    """
    if not isinstance(source, bytes) or not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", function_name):
        raise ValueError("Invalid source or function name")
    mask = bytearray(source)
    pos = 0
    while pos < len(source):
        start = pos
        if source[pos:pos + 2] == b"/*":
            end = source.find(b"*/", pos + 2)
            if end < 0:
                raise ValueError("Unterminated source comment")
            pos = end + 2
        elif source[pos:pos + 2] == b"//":
            end = source.find(b"\n", pos + 2)
            pos = len(source) if end < 0 else end
        elif source[pos] in (34, 39):
            quote = source[pos]
            pos += 1
            while pos < len(source) and source[pos] != quote:
                if source[pos] == 92:
                    pos += 2
                else:
                    pos += 1
            if pos >= len(source):
                raise ValueError("Unterminated source literal")
            pos += 1
        else:
            pos += 1
            continue
        mask[start:pos] = b" " * (pos - start)
    if b"#" in mask:
        raise ValueError("Preprocessor directives are outside this source experiment")
    pattern = rb"\b" + function_name.encode("ascii") + rb"\s*\([^;{}]*\)\s*\{"
    matches = list(re.finditer(pattern, mask))
    if len(matches) != 1:
        raise ValueError("Function definition is missing or ambiguous")
    start = matches[0].end() - 1
    depth = 0
    for pos in range(start, len(mask)):
        if mask[pos] == 123:
            depth += 1
        elif mask[pos] == 125:
            depth -= 1
            if depth == 0:
                return start, pos + 1
    raise ValueError("Unterminated function body")


def validate_source_change(baseline, alternative, function_name):
    """Prove that exactly one named body changed and everything outside did not."""
    left, right = body_span(baseline, function_name), body_span(alternative, function_name)
    if baseline[:left[0]] != alternative[:right[0]] or baseline[left[1]:] != alternative[right[1]:]:
        raise ValueError("Source differs outside the declared function body")
    original, changed = baseline[left[0]:left[1]], alternative[right[0]:right[1]]
    if original == changed:
        raise ValueError("Alternative has no declared body change")
    return {"baseline_span": list(left), "alternative_span": list(right),
            "baseline_body_sha256": sha256(original), "alternative_body_sha256": sha256(changed),
            "unchanged_prefix_sha256": sha256(baseline[:left[0]]),
            "unchanged_suffix_sha256": sha256(baseline[left[1]:])}


def indexed_rows(report):
    """Validate a complete matrix's keys and exact-count accounting."""
    if (report.get("status") != "COMPILER_BENCH_COMPLETE" or report.get("matched_progress") != 0
            or not report.get("results") or report.get("probe_count", 0) <= 0):
        raise ValueError("Expected a complete non-credit compiler bench")
    rows = {}
    for row in report["results"]:
        key = row["candidate"], row["setting"]
        if key in rows:
            raise ValueError("Duplicate matrix row")
        comparisons = row["comparisons"]
        names = [c["name"] for c in comparisons]
        if len(names) != report["probe_count"] or len(names) != len(set(names)):
            raise ValueError("Missing or duplicate probe comparison")
        for item in comparisons:
            exact = (item["compiled_size"] == item["target_size"]
                     and item["compiled_sha256"] == item["target_sha256"])
            if type(item["exact_probe_bytes"]) is not bool or item["exact_probe_bytes"] != exact:
                raise ValueError("Inconsistent exact-probe flag")
        if row["exact_probes"] != sum(c["exact_probe_bytes"] for c in comparisons):
            raise ValueError("Inconsistent exact-probe count")
        rows[key] = row
    return rows


def compare_cohorts(baseline_report, variant_reports, variants):
    """Isolate the changed function and reject changes in any control function."""
    baseline = indexed_rows(baseline_report)
    if set(variant_reports) != {v["id"] for v in variants} or len(variants) != len(variant_reports):
        raise ValueError("Missing or duplicate variant report")
    effects = []
    for variant in variants:
        alternative_report = variant_reports[variant["id"]]
        alternative = indexed_rows(alternative_report)
        if set(alternative) != set(baseline) or alternative_report["probe_count"] != baseline_report["probe_count"]:
            raise ValueError("Cohort row/probe scope differs")
        changed = variant["changed_function"]
        results, control_checks = [], 0
        for key, left in baseline.items():
            right = alternative[key]
            if left["flags"] != right["flags"] or left["version"] != right["version"]:
                raise ValueError("Cohort compiler settings differ")
            original = {c["name"]: c for c in left["comparisons"]}
            actual = {c["name"]: c for c in right["comparisons"]}
            if set(original) != set(actual) or changed not in original:
                raise ValueError("Cohort probe selection differs")
            for name, before in original.items():
                after = actual[name]
                if any(before[k] != after[k] for k in ("address", "target_size", "target_sha256")):
                    raise ValueError("Cohort target metadata differs")
                if name != changed:
                    if any(before[k] != after[k] for k in ("compiled_size", "compiled_sha256")):
                        raise ValueError("Unchanged source control emitted different bytes: " + name)
                    control_checks += 1
            old, new = original[changed], actual[changed]
            results.append({"candidate": key[0], "setting": key[1],
                            "baseline_exact_probes": left["exact_probes"],
                            "alternative_exact_probes": right["exact_probes"],
                            "baseline_function": old, "alternative_function": new,
                            "function_bytes_changed": any(old[k] != new[k] for k in ("compiled_size", "compiled_sha256"))})
        effects.append({"id": variant["id"], "changed_function": changed,
                        "control_comparisons": control_checks, "results": results})
    return {"variants": effects}


def run_experiment(*, root=ROOT, experiment_path=None, report_path=None):
    """Run baseline plus two reviewed alternatives without changing old inputs."""
    root = Path(root).resolve(strict=True)
    experiment_path = Path(experiment_path) if experiment_path else root / "config/source-hypotheses.json"
    experiment_raw = experiment_path.read_bytes()
    experiment = json.loads(experiment_raw)
    if (experiment.get("status") != "reviewed_frozen_source_experiment_not_toolchain_lock"
            or experiment.get("reviewed_before_compilation") is not True):
        raise ValueError("Source experiment must be reviewed and frozen before compilation")
    pinned = []
    def checked(item):
        path = root / item["relative_path"]
        reject_link(path)
        path = path.resolve(strict=True)
        if not path.is_relative_to(root):
            raise ValueError("Experiment input escapes the project")
        check_identity(file_identity(path), item, "Experiment input")
        pinned.append((path, item))
        return path
    baseline_path = checked(experiment["baseline"])
    candidates_path = checked(experiment["candidate_config"])
    manifest_path = checked(experiment["probe_manifest"])
    lock_path = checked(experiment["reference_lock"])
    baseline_bytes = baseline_path.read_bytes()
    candidates, manifest = json.loads(candidates_path.read_bytes()), json.loads(manifest_path.read_bytes())
    if (candidates["source_sha256"] != experiment["baseline"]["sha256"]
            or candidates["manifest_sha256"] != experiment["probe_manifest"]["sha256"]
            or manifest["source"] != experiment["baseline"]["relative_path"]):
        raise ValueError("Baseline source/configuration provenance disagrees")
    variants = experiment["variants"]
    if (len(variants) != 2 or len({v["id"] for v in variants}) != 2
            or len({v["changed_function"] for v in variants}) != 2
            or any(v["id"] == "baseline" or not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", v["id"])
                   for v in variants)):
        raise ValueError("Expected exactly two unique source alternatives/functions")
    probe_names = {p["name"] for p in manifest["probes"]}
    for variant in variants:
        path = checked(variant["source"])
        if variant["changed_function"] not in probe_names:
            raise ValueError("Changed function is not in the frozen probe manifest")
        change = validate_source_change(baseline_bytes, path.read_bytes(), variant["changed_function"])
        if change != variant["change"]:
            raise ValueError("Changed-body identity differs from its reviewed freeze")
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        if report_path.resolve() in {p.resolve() for p in (experiment_path, *[p for p, _ in pinned])}:
            raise ValueError("Report aliases an experiment input")
    build = root / "build"
    reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("Experiment build path escapes the project")
    build.mkdir(exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix="source-hypotheses-", dir=build)).resolve()
    baseline_report = run_bench(root=root, candidates_path=candidates_path, manifest_path=manifest_path,
                                lock_path=lock_path, report_path=output / "baseline-report.json", build_parent=output)
    alternative_reports = {}
    for variant in variants:
        # Only the source identity/path changes. Candidate builds, tool pins,
        # targets, settings and ordering stay exactly the same as the baseline.
        config, targets = copy.deepcopy(candidates), copy.deepcopy(manifest)
        targets["source"] = variant["source"]["relative_path"]
        target_path = output / (variant["id"] + "-targets.json")
        write_report(target_path, targets)
        config["source_sha256"] = variant["source"]["sha256"]
        config["manifest_sha256"] = sha256(target_path.read_bytes())
        config_path = output / (variant["id"] + "-candidates.json")
        write_report(config_path, config)
        alternative_reports[variant["id"]] = run_bench(
            root=root, candidates_path=config_path, manifest_path=target_path, lock_path=lock_path,
            report_path=output / (variant["id"] + "-report.json"), build_parent=output)
    effects = compare_cohorts(baseline_report, alternative_reports, variants)
    expected_rows = {(c["id"], s["id"]) for c in candidates["candidates"] for s in candidates["settings"]}
    expected_probes = {p["name"] for p in manifest["probes"]}
    for report in [baseline_report, *alternative_reports.values()]:
        if set(indexed_rows(report)) != expected_rows or any(
                {p["name"] for p in row["comparisons"]} != expected_probes for row in report["results"]):
            raise ValueError("Experiment report omits declared candidates/settings/probes")
    for path, item in pinned:
        check_identity(file_identity(path), item, "Experiment input changed during compilation")
    if experiment_path.read_bytes() != experiment_raw:
        raise ValueError("Experiment freeze changed during compilation")
    report = {"schema_version": 1, "status": "SOURCE_HYPOTHESES_COMPLETE",
              "scope": "two frozen source alternatives; no toolchain lock, historical source or game-match credit",
              "matched_progress": 0, "experiment_sha256": sha256(experiment_raw),
              "baseline_sha256": experiment["baseline"]["sha256"],
              "candidate_config_sha256": experiment["candidate_config"]["sha256"],
              "probe_manifest_sha256": experiment["probe_manifest"]["sha256"],
              "cohorts": {"baseline": baseline_report, **alternative_reports}, "source_effects": effects}
    write_report(output / "experiment-report.json", report)
    if report_path is not None:
        write_report(report_path, report)
    return report


def main(argv=None):
    """Expose the reviewed experiment without arbitrary source/flag overrides."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=ROOT / "evidence/bucket-03c/source-hypotheses.json")
    args = parser.parse_args(argv)
    try:
        report = run_experiment(report_path=args.report)
        for effect in report["source_effects"]["variants"]:
            exact = sum(row["alternative_function"]["exact_probe_bytes"] for row in effect["results"])
            print(effect["id"] + ": " + str(exact) + "/" + str(len(effect["results"]))
                  + " configurations emit the exact changed probe; all controls unchanged")
        print("SOURCE EXPERIMENT ONLY: no toolchain lock or matching credit")
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("SOURCE EXPERIMENT FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
