#!/usr/bin/env python3
"""Compare fixed C++/O2 archive output across eleven existing PSP MW builds.

Reuse the unchanged strict single-member comparator. Every declared case stays
visible; historical build 219 must reproduce exactly. This grants no game-match
credit and makes no original compiler/source-language attribution.
"""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

try:
    from .bench_archive_key import compare_archive_object, verify_archive_inputs, local_items as archive_items
    from .bench_compiler_families import compile_profile, profile_items, sha256
    from .bench_language_modes import local_items as language_items
    from .elf32 import Elf32
    from .prepare_reference import check_identity, file_identity, reject_link, write_report
except ImportError:
    from bench_archive_key import compare_archive_object, verify_archive_inputs, local_items as archive_items
    from bench_compiler_families import compile_profile, profile_items, sha256
    from bench_language_modes import local_items as language_items
    from elf32 import Elf32
    from prepare_reference import check_identity, file_identity, reject_link, write_report

ROOT = Path(__file__).resolve().parents[1]
BUILD_NUMBERS = (121, 134, 139, 147, 151, 180, 192, 201, 205, 210, 219)
IDS = [f"mwccpsp_3.0.1_{number}" for number in BUILD_NUMBERS]


def local_items(config):
    """List new metadata/evidence without changing earlier profile definitions."""
    return [config[k] for k in ("archive_profile", "compiler_candidates", "historical_control")] + [
        v[k] for v in config["versions"] for k in ("archive", "help")] + config["preserved_inputs"]


def candidate_items(catalogue):
    """Bind each unmodified compiler, its support files and the shared runner."""
    return [catalogue["runner"]] + [i for c in catalogue["candidates"]
        for i in [c["compiler"], *c["support_files"]]]


def verify_inputs(root, config):
    """Verify all source, tool, naming, target and historical-control bindings."""
    def checked(item):
        path = root / item["relative_path"]
        reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("MW archive-version input escapes project")
        check_identity(file_identity(path), item, "MW archive-version input")
        return path
    for item in local_items(config):
        checked(item)
    archive = json.loads(checked(config["archive_profile"]).read_bytes())
    families, control, manifest, reference, reference_pin, language = verify_archive_inputs(root, archive)
    catalogue = json.loads(checked(config["compiler_candidates"]).read_bytes())
    if (config["common_flags"] != archive["common_flags"] or config["optimization"] != ["-O2"]
            or config["declared_trials"] != 2 or config["source_attempts"] != 1
            or [v["id"] for v in config["versions"]] != IDS
            or [v["id"] for v in catalogue["candidates"]] != IDS
            or catalogue["runner"] != control["runner"]
            or config["compiler_candidates"]["sha256"] != families["existing_candidate_config"]["sha256"]):
        raise ValueError("MW archive-version matrix differs from reviewed eleven-case scope")
    for item in candidate_items(catalogue):
        checked(item)
    for declared, candidate in zip(config["versions"], catalogue["candidates"]):
        if (declared["archive"]["sha256"] != candidate["archive_sha256"]
                or declared["help"]["relative_path"] != candidate["help_evidence"]
                or declared["help"]["sha256"] != candidate["help_sha256"]):
            raise ValueError("MW archive-version tools differ from existing catalogue")
    last = catalogue["candidates"][-1]
    if last["compiler"] != control["compiler"] or last["support_files"] != control["support_files"]:
        raise ValueError("Build 219 differs from inherited control tools")
    historic = json.loads(checked(config["historical_control"]).read_bytes())
    if (historic["status"] != "ARCHIVE_KEY_INVESTIGATION_COMPLETE" or historic["outcome"] != "COMPLETE"
            or historic["profile_sha256"] != config["archive_profile"]["sha256"]
            or historic["source_sha256"] != archive["source"]["sha256"]
            or historic["reference_sha256"] != reference_pin["sha256"]
            or historic["flags"] != config["common_flags"] + config["optimization"]
            or len(historic["comparisons"]) != 1):
        raise ValueError("Historical MW archive control does not bind these frozen inputs")
    return families, control, manifest, reference, reference_pin, language, archive, catalogue, historic


def validate_control(current, historic):
    """Do not silently replace the 219 baseline when any full result changes."""
    fields = ("returncode", "outcome", "flags", "object_sha256", "exact_probes",
              "elf_flags", "compiler_comments", "comparisons")
    if any(current.get(k) != historic.get(k) for k in fields):
        raise ValueError("Historical Metrowerks build 219 control did not reproduce")


def diff_words(candidate, control):
    """Retain actual word/length differences against 219, not a size-only claim."""
    if candidate is None:
        return {"status": "UNSCORED", "identical": None, "word_differences": None}
    differences = []
    for offset in range(0, max(len(candidate), len(control)), 4):
        left, right = candidate[offset:offset + 4], control[offset:offset + 4]
        if left != right:
            differences.append({"offset": offset, "candidate_bytes_hex": left.hex() if left else None,
                                "control_bytes_hex": right.hex() if right else None})
    return {"status": "VALIDATED", "identical": candidate == control,
            "candidate_size": len(candidate), "control_size": len(control), "word_differences": differences}


def run_mw_archive_versions(*, root=ROOT, config_path=None, report_path=None):
    """Compile all eleven cases freshly, then validate every retained input/output."""
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/mw-archive-versions.json"
    raw = config_path.read_bytes()
    config = json.loads(raw)
    if config["status"] != "frozen_before_matrix_target_scoring" or config["no_matrix_target_scores_observed"] is not True:
        raise ValueError("MW archive-version profile was not frozen before scoring")
    protected = {config_path.resolve()} | {(root / i["relative_path"]).resolve() for i in local_items(config)}
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        if report_path.resolve() in protected:
            raise ValueError("MW archive-version report aliases input")
    families, control, manifest, reference, reference_pin, language, archive, catalogue, historic = verify_inputs(root, config)
    inherited = profile_items(families) + language_items(language) + archive_items(archive) + candidate_items(catalogue) + [reference_pin]
    if report_path is not None and report_path.resolve() in {(root / i["relative_path"]).resolve() for i in inherited}:
        raise ValueError("MW archive-version report aliases inherited input")
    build = root / "build"
    reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("MW archive-version build escapes project")
    build.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="mw-archive-versions-", dir=build))
    report = {"schema_version": 1, "status": "MW_ARCHIVE_VERSION_INVESTIGATION_COMPLETE",
        "profile_sha256": sha256(raw), "source_sha256": archive["source"]["sha256"],
        "reference_sha256": reference_pin["sha256"], "flags": config["common_flags"] + config["optimization"],
        "declared_cases": 11, "matched_progress": 0, "versions": []}
    emitted, bodies = {}, {}
    for candidate in catalogue["candidates"]:
        obj = directory / (candidate["id"] + ".o")
        row = {"id": candidate["id"], "version": candidate["version"], "outcome": "REJECTED_NO_SCORE",
               "flags": report["flags"]}
        bodies[candidate["id"]] = None
        profile = dict(control, id=candidate["id"], compiler=candidate["compiler"],
            support_files=candidate["support_files"], runner=catalogue["runner"], common_flags=config["common_flags"],
            timeout_tool=families["linux_utilities"][0]["linux_path"])
        try:
            result = compile_profile(profile, root / archive["source"]["relative_path"], obj,
                                     config["optimization"], root=root)
            diagnostic = result["stdout"] + result["stderr"]
            obj.with_suffix(".log").write_text(diagnostic, encoding="utf-8")
            row["returncode"] = result["returncode"]
            if obj.is_file():
                reject_link(obj)
                emitted[obj] = obj.read_bytes()
                row["object_sha256"] = sha256(emitted[obj])
            if (result["returncode"] or obj not in emitted
                    or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
                row["reason"] = "Compiler failure, warning or missing object"
            else:
                comparison = compare_archive_object(emitted[obj], reference, manifest, archive["object_symbol"])
                row.update(comparison, outcome="COMPLETE",
                    exact_probes=sum(c["exact_probe_bytes"] for c in comparison["comparisons"]))
                bodies[candidate["id"]] = next(Elf32(emitted[obj]).functions())["bytes"]
        except (OSError, subprocess.SubprocessError) as error:
            row["reason"] = "Compilation unavailable: " + type(error).__name__
        except ValueError as error:
            row["reason"] = "Object rejected: " + str(error)
        # Failed stages can leave partial objects even when the subprocess raises.
        if obj.exists() or obj.is_symlink():
            reject_link(obj)
            retained = obj.read_bytes()
            if obj in emitted and retained != emitted[obj]:
                raise ValueError("MW archive-version object changed during inspection")
            emitted[obj] = retained
            row.setdefault("object_sha256", sha256(retained))
        report["versions"].append(row)
    verify_inputs(root, config)
    if config_path.read_bytes() != raw:
        raise ValueError("MW archive-version profile changed during trial")
    for path, data in emitted.items():
        reject_link(path)
        if path.read_bytes() != data:
            raise ValueError("Emitted MW archive-version object changed during trial")
    validate_control(report["versions"][-1], historic)
    report["historical_control_reproduced"] = True
    report["completed_cases"] = sum(v["outcome"] == "COMPLETE" for v in report["versions"])
    report["differences_from_219"] = [{"id": name, **diff_words(code, bodies[IDS[-1]])} for name, code in bodies.items()]
    write_report(directory / "report.json", report)
    if report_path is not None:
        write_report(report_path, report)
    return report, directory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="evidence/bucket-03l/mw-archive-versions-trial.json")
    args = parser.parse_args()
    if os.name == "nt":
        return subprocess.run(["wsl", "-d", "Ubuntu", "--", "python3", "scripts/bench_mw_archive_versions.py",
                               "--report", args.report], cwd=ROOT).returncode
    try:
        report, directory = run_mw_archive_versions(report_path=ROOT / args.report)
        print(json.dumps({"status": report["status"], "build_directory": str(directory), "report": args.report}))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("MW ARCHIVE VERSION INVESTIGATION FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
