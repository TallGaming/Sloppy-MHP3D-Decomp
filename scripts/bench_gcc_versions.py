#!/usr/bin/env python3
"""Compare two frozen PSP GCC packages without changing prior experiments.

Only complete validated fourteen-function settings receive diagnostic scores.
Both versions use the same inherited C backend flags and pinned GNU assembler;
this is not a reproduction of either complete SDK driver pipeline.
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
LEVELS = [{"id": f"O{i}", "flags": [f"-O{i}"]} for i in range(4)]
COMMON = ["-quiet", "-nostdinc", "-G", "0", "-march=allegrex", "-mtune=allegrex", "-mel", "-mabi=eabi"]
ASSEMBLER = ["-EL", "-march=allegrex", "-mabi=eabi", "-G0", "-O0"]


def local_items(config):
    """Protect new evidence/tools and the complete inherited comparison inputs."""
    return [config[k] for k in ("family_profiles", "source", "probe_manifest", "reference_lock",
            "control_report", "tool_inventory", "selection", "preflight_source", "preflight_evidence")] + [
            config["candidate"][k] for k in ("compiler", "archive")] + config["candidate"]["support_files"] + config["pre_score_evidence"] + config["preserved_inputs"]


def verify_inputs(root, config):
    """Bind the exact two packages, prior control, flags, source and reference."""
    def checked(item):
        path = root / item["relative_path"]
        reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("GCC version input escapes project")
        check_identity(file_identity(path), item, "GCC version input")
        return path
    for item in local_items(config):
        checked(item)
    families = json.loads(checked(config["family_profiles"]).read_bytes())
    verify_profile_files(root, families)
    candidate = config["candidate"]
    controls = [p for p in families["profiles"] if p["id"] == config["control_profile_id"]]
    if len(controls) != 1:
        raise ValueError("GCC version control must be unique")
    control = controls[0]
    if (config["control_profile_id"] != "psp_gcc_1_7_1"
            or candidate["id"] != "psp_gcc_1_3_1"
            or candidate["version"] != "gcc 3.3.3+allegrex-2.2.1-psp-1.3.1"
            or control["version"] != "gcc 3.3.3+allegrex-2.2.2-psp-1.7.1"
            or config["declared_trials"] != 2 or config["probe_count"] != 14
            or config["source"] != families["baseline_source"]
            or config["probe_manifest"] != families["probe_manifest"]
            or config["reference_lock"] != families["reference_lock"]):
        raise ValueError("GCC versions differ from the reviewed pair/original scope")
    for profile in (candidate, control):
        if (profile["mode"] != "gcc_backend_native" or profile["status"] != "runnable"
                or profile["family"] != "GCC" or profile["levels"] != LEVELS
                or profile["common_flags"] != COMMON or profile["assembler_flags"] != ASSEMBLER
                or profile["assembler"] != control["assembler"]):
            raise ValueError("GCC version commands differ from fixed equivalent settings")
    inventory = json.loads(checked(config["tool_inventory"]).read_bytes())
    selected = json.loads(checked(config["selection"]).read_bytes())
    records = [{k: item[k] for k in ("relative_path", "size", "sha256")} for item in inventory["files"]]
    backends = [i for i in records if i["relative_path"].endswith("/cc1")]
    if (selected["candidate"] != "psp-gcc-1.3.1" or selected["declared_trials"] != 2
            or inventory["selection_sha256"] != config["selection"]["sha256"]
            or candidate["support_files"] != records or len(backends) != 1
            or candidate["compiler"] != backends[0] or candidate["archive"] != inventory["archive"]):
        raise ValueError("GCC version tool identity differs from reviewed inventory")
    lock = json.loads(checked(config["reference_lock"]).read_bytes())
    if lock["status"] != "active" or lock["baseline_selected_by_user"] is not True:
        raise ValueError("GCC version comparison lacks selected reference")
    reference_pin = lock["decrypted_executable"]
    reference = Elf32(checked(reference_pin).read_bytes())
    manifest = json.loads(checked(config["probe_manifest"]).read_bytes())
    if manifest["source"] != config["source"]["relative_path"] or len(validate_probes(reference, manifest)) != 14:
        raise ValueError("GCC version comparison needs all fourteen original probes")
    historic = json.loads(checked(config["control_report"]).read_bytes())
    matching = [f for f in historic["families"] if f["id"] == control["id"]]
    if (len(matching) != 1 or historic["profiles_sha256"] != config["family_profiles"]["sha256"]
            or historic["source_sha256"] != config["source"]["sha256"]
            or historic["manifest_sha256"] != config["probe_manifest"]["sha256"]
            or historic["reference_sha256"] != reference_pin["sha256"]
            or historic["probe_count"] != 14):
        raise ValueError("Historical GCC control does not bind these complete inputs")
    expected = matching[0]
    if ([a["setting"] for a in expected["attempts"]] != [l["id"] for l in LEVELS]
            or len(expected["rows"]) != expected["completed_settings"]
            or expected["declared_settings"] != 4):
        raise ValueError("Historical GCC control lacks all declared outcomes")
    return families, candidate, control, manifest, reference, reference_pin, expected


def validate_control(current, expected):
    """Require exact prior object hashes, outcomes and complete scored rows."""
    if current["attempts"] != expected["attempts"] or current["rows"] != expected["rows"]:
        raise ValueError("Existing GCC 1.7.1 control did not reproduce historical output")


def compare_versions(candidate_functions, control_functions):
    """Compare complete validated bodies; never score a rejected setting."""
    if candidate_functions is None or control_functions is None:
        return {"status": "UNSCORED", "identical_functions": None, "comparisons": None}
    if set(candidate_functions) != set(control_functions) or len(candidate_functions) != 14:
        raise ValueError("GCC version function sets differ from complete bench")
    comparisons = []
    for name, candidate in candidate_functions.items():
        control = control_functions[name]
        first = next((i for i, pair in enumerate(zip(candidate, control)) if pair[0] != pair[1]), None)
        if first is None and len(candidate) != len(control):
            first = min(len(candidate), len(control))
        comparisons.append({"name": name, "candidate_size": len(candidate), "control_size": len(control),
            "identical": candidate == control, "first_difference": first,
            "candidate_sha256": sha256(candidate), "control_sha256": sha256(control)})
    return {"status": "BOTH_VALIDATED", "identical_functions": sum(c["identical"] for c in comparisons),
            "comparisons": comparisons}


def run_gcc_versions(*, root=ROOT, config_path=None, report_path=None):
    """Attempt eight fresh objects and reject changed inputs or retained outputs."""
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/gcc-versions.json"
    raw = config_path.read_bytes()
    config = json.loads(raw)
    if config["status"] != "frozen_before_candidate_target_scoring" or config["no_candidate_target_scores_observed"] is not True:
        raise ValueError("GCC version profile was not frozen before target scoring")
    protected = {config_path.resolve()} | {(root / i["relative_path"]).resolve() for i in local_items(config)}
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        if report_path.resolve() in protected:
            raise ValueError("GCC version report aliases input")
    families, candidate, control, manifest, reference, reference_pin, historic = verify_inputs(root, config)
    if report_path is not None and report_path.resolve() in {
            (root / i["relative_path"]).resolve() for i in profile_items(families) + [reference_pin]}:
        raise ValueError("GCC version report aliases inherited input")
    build = root / "build"
    reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("GCC version build escapes project")
    build.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="gcc-versions-", dir=build))
    report = {"schema_version": 1, "status": "GCC_VERSION_INVESTIGATION_COMPLETE",
        "profile_sha256": sha256(raw), "source_sha256": config["source"]["sha256"],
        "manifest_sha256": config["probe_manifest"]["sha256"], "reference_sha256": reference_pin["sha256"],
        "probe_count": 14, "declared_configurations": 8, "matched_progress": 0, "versions": []}
    emitted, bodies = {}, {}
    source = root / config["source"]["relative_path"]
    for profile in (candidate, control):
        case = {"id": profile["id"], "version": profile["version"], "rows": [], "attempts": []}
        for level in LEVELS:
            obj = directory / (profile["id"] + "-" + level["id"] + ".o")
            attempt = {"setting": level["id"], "status": "REJECTED_NO_SCORE"}
            bodies[(profile["id"], level["id"])] = None
            try:
                result = compile_profile(dict(profile, timeout_tool=families["linux_utilities"][0]["linux_path"]),
                    source, obj, level["flags"], root=root)
                diagnostic = result["stdout"] + result["stderr"]
                obj.with_suffix(".log").write_text(diagnostic, encoding="utf-8")
                if obj.is_file():
                    reject_link(obj)
                    emitted[obj] = obj.read_bytes()
                    attempt["object_sha256"] = sha256(emitted[obj])
                if (result["returncode"] or obj not in emitted
                        or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
                    attempt.update(reason="compiler/assembler failure, warning or missing object",
                        returncode=result["returncode"], failed_stage=result.get("failed_stage", "compiler"))
                else:
                    comparison = compare_object(emitted[obj], reference, manifest)
                    case["rows"].append({"setting": level["id"], "flags": profile["common_flags"] + level["flags"],
                        "assembler_flags": profile["assembler_flags"],
                        "exact_probes": sum(c["exact_probe_bytes"] for c in comparison["comparisons"]),
                        "artifacts": result.get("artifacts", {}), **comparison})
                    attempt = {"setting": level["id"], "status": "OBJECT_VALIDATED",
                               "object_sha256": comparison["object_sha256"]}
                    bodies[(profile["id"], level["id"])] = {f["name"]: f["bytes"] for f in Elf32(emitted[obj]).functions()}
            except (OSError, subprocess.SubprocessError) as error:
                attempt["reason"] = "profile execution unavailable: " + type(error).__name__
            except ValueError as error:
                attempt["reason"] = "profile output rejected: " + str(error)
            # A timed-out stage may leave an object before raising. Retain its
            # identity too, so subsequent invocations cannot silently replace it.
            if obj.exists() or obj.is_symlink():
                reject_link(obj)
                retained = obj.read_bytes()
                if obj in emitted and emitted[obj] != retained:
                    raise ValueError("GCC version object changed during inspection")
                emitted[obj] = retained
                attempt.setdefault("object_sha256", sha256(retained))
            case["attempts"].append(attempt)
        case["completed_settings"] = len(case["rows"])
        case["status"] = "COMPLETE" if len(case["rows"]) == 4 else "INCOMPLETE_SETTINGS"
        report["versions"].append(case)
    verify_inputs(root, config)
    if config_path.read_bytes() != raw:
        raise ValueError("GCC version profile changed during trial")
    for path, data in emitted.items():
        reject_link(path)
        if path.read_bytes() != data:
            raise ValueError("Emitted GCC version object changed during trial")
    validate_control(report["versions"][1], historic)
    report["historical_control_reproduced"] = True
    report["cross_version"] = [{"setting": l["id"], **compare_versions(
        bodies[(candidate["id"], l["id"])], bodies[(control["id"], l["id"])])} for l in LEVELS]
    report["completed_configurations"] = sum(len(v["rows"]) for v in report["versions"])
    write_report(directory / "report.json", report)
    if report_path is not None:
        write_report(report_path, report)
    return report, directory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="evidence/bucket-03k/gcc-versions-trial.json")
    args = parser.parse_args()
    if os.name == "nt":
        return subprocess.run(["wsl", "-d", "Ubuntu", "--", "python3", "scripts/bench_gcc_versions.py",
                               "--report", args.report], cwd=ROOT).returncode
    try:
        report, directory = run_gcc_versions(report_path=ROOT / args.report)
        print(json.dumps({"status": report["status"], "build_directory": str(directory), "report": args.report}))
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("GCC VERSION INVESTIGATION FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
