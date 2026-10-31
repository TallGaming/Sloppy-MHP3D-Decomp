#!/usr/bin/env python3
"""Compare fixed C/C++ modes without changing source or object symbol records.

Exact aliases come from a separately reviewed invented naming fixture. Only
complete fourteen-function configurations receive diagnostic scores; these are
not game matches and do not select an original compiler or language.
"""

import argparse
import copy
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

try:
    from .bench_compiler import compare_object, validate_probes
    from .bench_compiler_families import compile_profile, profile_items, verify_profile_files, sha256
    from .elf32 import Elf32
    from .prepare_reference import check_identity, file_identity, reject_link, write_report
except ImportError:
    from bench_compiler import compare_object, validate_probes
    from bench_compiler_families import compile_profile, profile_items, verify_profile_files, sha256
    from elf32 import Elf32
    from prepare_reference import check_identity, file_identity, reject_link, write_report

ROOT = Path(__file__).resolve().parents[1]


def compare_language_object(object_bytes, reference, manifest, symbol_map):
    """Apply an exact manifest alias bijection without editing object bytes."""
    canonical = [p["name"] for p in manifest["probes"]]
    if (len(set(canonical)) != len(canonical) or set(symbol_map) != set(canonical)
            or len(set(symbol_map.values())) != len(canonical)
            or any(not isinstance(n, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", n)
                   for n in symbol_map.values())):
        raise ValueError("Language symbols must be an exact unique probe mapping")
    derived = copy.deepcopy(manifest)
    for probe in derived["probes"]:
        probe["name"] = symbol_map[probe["name"]]
    comparison = compare_object(object_bytes, reference, derived)
    inverse = {v: k for k, v in symbol_map.items()}
    for row in comparison["comparisons"]:
        symbol = row["name"]
        row.update(name=inverse[symbol], object_symbol=symbol)
    return comparison


def validate_modes(config, families, manifest, naming_spec, naming_evidence):
    """Bind both commands and every canonical association to pre-score evidence."""
    profiles = [p for p in families["profiles"] if p["id"] == config["compiler_profile_id"]]
    if (len(profiles) != 1 or profiles[0]["id"] != "mwccpsp_3_0_1_219"
            or profiles[0]["status"] != "runnable" or profiles[0]["mode"] != "wibo_driver"
            or profiles[0]["common_flags"] != ["-nostdinc", "-lang", "c", "-c"]
            or config["optimization"] != ["-O2"] or config["declared_trials"] != 2
            or config["probe_count"] != 14 or len(manifest["probes"]) != 14
            or [m["id"] for m in config["modes"]] != ["c", "cpp"]
            or [m["id"] for m in naming_evidence["modes"]] != ["c", "cpp"]
            or naming_evidence["spec_sha256"] != config["naming_spec"]["sha256"]):
        raise ValueError("Language profile differs from the fixed reviewed pair")
    pairs = naming_spec["pairs"]
    if ([p["canonical_name"] for p in pairs] != [p["name"] for p in manifest["probes"]]
            or [p["fixture_name"] for p in pairs] != [f"naming_fixture_{i:02d}" for i in range(14)]):
        raise ValueError("Naming fixture pairs do not bind the complete probe order")
    for mode, observed, language in zip(config["modes"], naming_evidence["modes"], ("c", "c++")):
        flags = ["-nostdinc", "-lang", language, "-c"]
        if (mode["common_flags"] != flags or observed["flags"] != flags + ["-O2"]
                or len(observed["mappings"]) != 14):
            raise ValueError("Only the language operand may change")
        expected = {}
        for pair, row in zip(pairs, observed["mappings"]):
            if any(row[k] != pair[k] for k in ("canonical_name", "fixture_name", "signature_category")):
                raise ValueError("Language association differs from invented signature binding")
            suffix = row["suffix"]
            if ((language == "c" and suffix != "")
                    or (language == "c++" and (not suffix.startswith("__") or len(suffix) <= 2))
                    or row["fixture_symbol"] != pair["fixture_name"] + suffix
                    or row["object_symbol"] != pair["canonical_name"] + suffix):
                raise ValueError("Language map does not follow observed naming rule")
            expected[pair["canonical_name"]] = row["object_symbol"]
        if mode["symbol_map"] != expected or len(set(expected.values())) != 14:
            raise ValueError("Language mapping differs from frozen naming observations")
    return profiles[0]


def local_items(config):
    """Protect every new profile/naming input and the inherited frozen source."""
    return [config[k] for k in ("family_profiles", "source", "probe_manifest", "reference_lock",
                                "naming_spec", "naming_source", "naming_evidence")] + config["naming_objects"]


def verify_inputs(root, config):
    """Check hashes, inherited scope, naming objects and selected reference bytes."""
    def checked(item):
        path = root / item["relative_path"]
        reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Language input escapes project")
        check_identity(file_identity(path), item, "Language input")
        return path
    for item in local_items(config):
        checked(item)
    families = json.loads((root / config["family_profiles"]["relative_path"]).read_bytes())
    verify_profile_files(root, families)
    if (config["source"] != families["baseline_source"]
            or config["probe_manifest"] != families["probe_manifest"]
            or config["reference_lock"] != families["reference_lock"]):
        raise ValueError("Language bench does not use original frozen inputs")
    manifest = json.loads((root / config["probe_manifest"]["relative_path"]).read_bytes())
    spec = json.loads((root / config["naming_spec"]["relative_path"]).read_bytes())
    evidence = json.loads((root / config["naming_evidence"]["relative_path"]).read_bytes())
    if (spec["fixture"] != config["naming_source"] or spec["probe_manifest"] != config["probe_manifest"]
            or spec["compiler_families"] != config["family_profiles"]
            or manifest["source"] != config["source"]["relative_path"]):
        raise ValueError("Naming/source identity differs from reviewed inputs")
    profile = validate_modes(config, families, manifest, spec, evidence)
    if len(config["naming_objects"]) != 2:
        raise ValueError("Both naming objects must remain pinned")
    for item, observed in zip(config["naming_objects"], evidence["modes"]):
        if item["relative_path"] != observed["object_relative_path"] or item["sha256"] != observed["object_sha256"]:
            raise ValueError("Naming object pin differs from observation")
        obj = Elf32(checked(item).read_bytes())
        functions = list(obj.functions())
        names = [fn["name"] for fn in functions]
        if (obj.file_type != 1 or len(names) != 14 or len(set(names)) != 14
                or set(names) != {r["fixture_symbol"] for r in observed["mappings"]}):
            raise ValueError("Observed naming symbols differ from fixture object")
        for fn in functions:
            section = obj.sections[fn["section_index"]]
            if fn["size"] <= 0 or fn["size"] % 4 or section["flags"] & 6 != 6:
                raise ValueError("Invalid complete naming function")
    lock = json.loads((root / config["reference_lock"]["relative_path"]).read_bytes())
    if lock["status"] != "active" or lock["baseline_selected_by_user"] is not True:
        raise ValueError("Language experiment lacks selected reference")
    reference = Elf32(checked(lock["decrypted_executable"]).read_bytes())
    validate_probes(reference, manifest)
    return families, profile, manifest, reference, lock["decrypted_executable"]


def run_language_modes(*, root=ROOT, config_path=None, report_path=None):
    """Run both complete configurations freshly and reject changing inputs."""
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/language-modes.json"
    raw = config_path.read_bytes()
    config = json.loads(raw)
    if config["status"] != "frozen_before_cpp_target_scoring" or config["no_cpp_target_scores_observed"] is not True:
        raise ValueError("Language profile was not frozen before C++ target scoring")
    protected = {config_path.resolve()} | {(root / i["relative_path"]).resolve() for i in local_items(config)}
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        if report_path.resolve() in protected:
            raise ValueError("Language report aliases an input")
    families, profile, manifest, reference, reference_pin = verify_inputs(root, config)
    protected |= {(root / i["relative_path"]).resolve() for i in profile_items(families) + [reference_pin]}
    if report_path is not None and report_path.resolve() in protected:
        raise ValueError("Language report aliases inherited input")
    build = root / "build"
    reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("Language build escapes project")
    build.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="language-modes-", dir=build))
    report = {"schema_version": 1, "status": "LANGUAGE_MODE_INVESTIGATION_COMPLETE",
              "profile_sha256": sha256(raw), "source_sha256": config["source"]["sha256"],
              "naming_evidence_sha256": config["naming_evidence"]["sha256"],
              "reference_sha256": reference_pin["sha256"], "matched_progress": 0, "modes": []}
    completed_bytes = {}
    emitted_objects = {}
    for mode in config["modes"]:
        obj = directory / (mode["id"] + ".o")
        row = {"id": mode["id"], "status": "REJECTED_NO_SCORE", "comparisons": [],
               "flags": mode["common_flags"] + config["optimization"]}
        try:
            execution = compile_profile(dict(profile, common_flags=mode["common_flags"],
                                              timeout_tool=families["linux_utilities"][0]["linux_path"]),
                                        root / config["source"]["relative_path"], obj,
                                        config["optimization"], root=root)
            diagnostic = execution["stdout"] + execution["stderr"]
            obj.with_suffix(".log").write_text(diagnostic, encoding="utf-8")
            row["returncode"] = execution["returncode"]
            if obj.is_file():
                reject_link(obj)
                emitted_objects[obj] = obj.read_bytes()
                row["object_sha256"] = sha256(emitted_objects[obj])
            if (execution["returncode"] or not obj.is_file()
                    or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
                row["reason"] = "Compiler failure, warning or missing object"
            else:
                raw_object = obj.read_bytes()
                comparison = compare_language_object(raw_object, reference, manifest, mode["symbol_map"])
                row.update(comparison, status="COMPLETE",
                           exact_probes=sum(c["exact_probe_bytes"] for c in comparison["comparisons"]))
                inverse = {v: k for k, v in mode["symbol_map"].items()}
                completed_bytes[mode["id"]] = {inverse[f["name"]]: f["bytes"] for f in Elf32(raw_object).functions()}
        except (OSError, subprocess.SubprocessError) as error:
            row["reason"] = "Compilation unavailable: " + type(error).__name__
        except ValueError as error:
            row["reason"] = "Object rejected: " + str(error)
        report["modes"].append(row)
    # Later compiler invocations must not silently replace an earlier mode's
    # scored object, including a partial object retained from a failed mode.
    for obj, original in emitted_objects.items():
        reject_link(obj)
        if obj.read_bytes() != original:
            raise ValueError("Emitted language object changed during trial")
    verify_inputs(root, config)
    if config_path.read_bytes() != raw:
        raise ValueError("Language profile changed during execution")
    report["mode_byte_comparisons"] = []
    if set(completed_bytes) == {"c", "cpp"}:
        for probe in manifest["probes"]:
            name = probe["name"]
            c, cpp = completed_bytes["c"][name], completed_bytes["cpp"][name]
            report["mode_byte_comparisons"].append({"name": name, "identical": c == cpp,
                "c_size": len(c), "cpp_size": len(cpp), "c_sha256": sha256(c), "cpp_sha256": sha256(cpp)})
    report["completed_configurations"] = sum(m["status"] == "COMPLETE" for m in report["modes"])
    if report_path is not None:
        write_report(report_path, report)
    return report, directory


def main():
    """Use the established WSL environment for both language modes."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="evidence/bucket-03h/language-mode-trial.json")
    args = parser.parse_args()
    if os.name == "nt":
        return subprocess.run(["wsl", "-d", "Ubuntu", "--", "python3", "scripts/bench_language_modes.py",
                               "--report", args.report], cwd=ROOT).returncode
    try:
        report, directory = run_language_modes(report_path=ROOT / args.report)
        print(json.dumps({"status": report["status"], "completed_configurations": report["completed_configurations"],
                          "build_directory": str(directory), "report": args.report}))
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
