#!/usr/bin/env python3
"""Compare three pre-reviewed compiler-family profiles on frozen C probes.

Native Linux execution is required for the old GCC backend and explicit system
assembler pins; Windows CLI calls relaunch under WSL Ubuntu. Each scored
configuration must validate every probe; rejected configurations receive no
score. This diagnostic never selects a game toolchain.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

try:
    from .bench_compiler import compare_object, runtime_root, validate_probes
    from .elf32 import Elf32
    from .prepare_reference import check_identity, file_identity, reject_link, write_report
except ImportError:
    from bench_compiler import compare_object, runtime_root, validate_probes
    from elf32 import Elf32
    from prepare_reference import check_identity, file_identity, reject_link, write_report


ROOT = Path(__file__).resolve().parents[1]


def sha256(data):
    """Hash exact source, metadata and object bytes."""
    return hashlib.sha256(data).hexdigest()


def profile_items(config):
    """List pinned project-local files, including all available subtools."""
    items = [config[k] for k in ("baseline_source", "probe_manifest", "reference_lock", "existing_candidate_config")]
    items += config.get("pre_score_evidence", [])
    for profile in config["profiles"]:
        items += profile.get("support_files", [])
        for key in ("compiler", "runner", "archive"):
            if key in profile:
                items.append(profile[key])
    return items


def verify_profile_files(root, config):
    """Verify every declared local tool/input and native host dependency."""
    for item in profile_items(config):
        path = root / item["relative_path"]
        reject_link(path)
        path = path.resolve(strict=True)
        if not path.is_relative_to(root):
            raise ValueError("Compiler-family input escapes the project")
        check_identity(file_identity(path), item, "Compiler-family input")
    native = [*config.get("linux_dependencies", []), *config.get("linux_utilities", [])]
    native += [p["assembler"] for p in config["profiles"] if "assembler" in p]
    for item in native:
        path = Path(item["linux_path"])
        if not path.is_absolute():
            raise ValueError("Native tool/dependency needs an explicit absolute path")
        check_identity(file_identity(path), item, "Native compiler dependency")


def compile_profile(profile, source, output, optimization_flags, *, root, timeout=20):
    """Compile one frozen profile without PATH assembler or SDK fallbacks."""
    if output.exists():
        raise ValueError("Refusing stale family object")
    timeout_tool = profile["timeout_tool"]
    artifacts = {}
    def stage(tool, flags, label, cwd):
        result = subprocess.run([timeout_tool, str(timeout) + "s", str(tool), *flags],
                                cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True,
                                text=True, timeout=timeout + 5)
        return {"returncode": result.returncode, "stdout": result.stdout,
                "stderr": result.stderr, "failed_stage": label, "artifacts": artifacts}
    if profile["mode"] == "wibo_driver":
        runner, compiler = root / profile["runner"]["relative_path"], root / profile["compiler"]["relative_path"]
        return stage(runner, [str(compiler), *profile["common_flags"], *optimization_flags,
                              "-o", str(output), str(source)], "compiler", compiler.parent)
    if profile["mode"] != "gcc_backend_native":
        raise ValueError("Unsupported compiler-family pipeline")
    if os.name == "nt":
        raise ValueError("The old GCC backend needs native Linux staging")
    # This unmodified 32-bit backend cannot stat the Windows mount's large inode
    # numbers. A byte-identical copy on native /tmp avoids that filesystem error.
    with tempfile.TemporaryDirectory(prefix="mhp3rd-family-", dir="/tmp") as name:
        scratch = Path(name).resolve()
        if not scratch.is_relative_to(Path("/tmp").resolve()):
            raise ValueError("Native compiler staging escaped /tmp")
        staged_source, assembly = scratch / source.name, scratch / "probe.s"
        source_bytes = source.read_bytes()
        staged_source.write_bytes(source_bytes)
        if staged_source.read_bytes() != source_bytes:
            raise ValueError("Native staged source differs")
        first = stage(root / profile["compiler"]["relative_path"],
                      [*profile["common_flags"], *optimization_flags, "-o", assembly.name, staged_source.name],
                      "compiler", scratch)
        diagnostic = first["stdout"] + first["stderr"]
        if first["returncode"] or not assembly.is_file() or re.search(r"\b(warning|error|fatal)\b", diagnostic, re.I):
            return first
        if staged_source.read_bytes() != source_bytes:
            raise ValueError("Compiler changed staged source")
        assembly_bytes = assembly.read_bytes()
        artifacts["assembly_sha256"] = sha256(assembly_bytes)
        second = stage(profile["assembler"]["linux_path"],
                       [*profile["assembler_flags"], "-o", str(output), str(assembly)], "assembler", scratch)
        second["stdout"] = first["stdout"] + second["stdout"]
        second["stderr"] = first["stderr"] + second["stderr"]
        if staged_source.read_bytes() != source_bytes or assembly.read_bytes() != assembly_bytes:
            raise ValueError("Assembler changed staged source or emitted assembly")
        return second


def run_families(*, root=ROOT, profiles_path=None, report_path=None):
    """Attempt all four levels and score only complete, validated configurations."""
    root = Path(root).resolve(strict=True)
    profiles_path = Path(profiles_path) if profiles_path else root / "config/compiler-families.json"
    config_raw = profiles_path.read_bytes()
    config = json.loads(config_raw)
    if config.get("status") != "profiles_frozen_before_target_scoring" or config.get("no_target_scores_observed") is not True:
        raise ValueError("Family profiles must have been frozen before scoring")
    profiles = config["profiles"]
    if not profiles or len({p["id"] for p in profiles}) != len(profiles):
        raise ValueError("Compiler family profiles are empty or duplicated")
    for profile in profiles:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", profile["id"]):
            raise ValueError("Invalid compiler-family identifier")
        if profile["status"] == "runnable":
            if (profile["mode"] not in ("wibo_driver", "gcc_backend_native")
                    or profile["levels"] != [{"id": f"O{i}", "flags": [f"-O{i}"]} for i in range(4)]
                    or not isinstance(profile["common_flags"], list)
                    or any(not isinstance(f, str) for f in profile["common_flags"])):
                raise ValueError("Family profile does not declare the fixed four-level matrix")
        elif profile["status"] != "unavailable" or not profile.get("reason"):
            raise ValueError("Unavailable profile needs an explicit reason")
    verify_profile_files(root, config)
    lock_path = root / config["reference_lock"]["relative_path"]
    lock_raw = lock_path.read_bytes()
    lock = json.loads(lock_raw)
    if lock.get("status") != "active" or lock.get("baseline_selected_by_user") is not True:
        raise ValueError("No active selected reference")
    reference_path = root / lock["decrypted_executable"]["relative_path"]
    reject_link(reference_path)
    if not reference_path.resolve().is_relative_to(root):
        raise ValueError("Reference escapes the project")
    check_identity(file_identity(reference_path), lock["decrypted_executable"], "Family reference")
    reference = Elf32(reference_path.read_bytes())
    manifest_path = root / config["probe_manifest"]["relative_path"]
    manifest_raw = manifest_path.read_bytes()
    manifest = json.loads(manifest_raw)
    if manifest["source"] != config["baseline_source"]["relative_path"]:
        raise ValueError("Family bench does not use the original source")
    probes = validate_probes(reference, manifest)
    source = root / config["baseline_source"]["relative_path"]
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        protected = {profiles_path.resolve(), reference_path.resolve()}
        protected |= {(root / item["relative_path"]).resolve() for item in profile_items(config)}
        if report_path.resolve() in protected:
            raise ValueError("Family report aliases an input")
    build = root / "build"
    reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("Family build path escapes the project")
    build.mkdir(exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix="compiler-families-", dir=build)).resolve()
    report = {"schema_version": 1, "status": "COMPILER_FAMILY_INVESTIGATION_COMPLETE",
              "scope": "fixed source and pre-reviewed family profiles; no toolchain lock or game-match credit",
              "profiles_sha256": sha256(config_raw), "source_sha256": config["baseline_source"]["sha256"],
              "manifest_sha256": config["probe_manifest"]["sha256"],
              "reference_sha256": lock["decrypted_executable"]["sha256"],
              "probe_count": len(probes), "matched_progress": 0, "families": []}
    utilities = config.get("linux_utilities", [])
    timeout_tool = next((i["linux_path"] for i in utilities if Path(i["linux_path"]).name == "timeout"), None)
    if not timeout_tool:
        raise ValueError("No explicitly pinned timeout utility")
    for number, profile in enumerate(profiles):
        family = {"id": profile["id"], "family": profile["family"], "version": profile["version"],
                  "status": "UNAVAILABLE_NO_SCORE", "rows": [],
                  "completed_settings": 0, "declared_settings": 4}
        if profile["status"] == "unavailable":
            family["reason"] = profile["reason"]
            report["families"].append(family)
            continue
        rows, attempts = [], []
        cohort_failed = False
        def reject_attempt(level, reason, **details):
            nonlocal cohort_failed
            cohort_failed = True
            attempt = {"setting": level["id"], "status": "REJECTED_NO_SCORE", "reason": reason, **details}
            obj = output / (str(number) + "-" + level["id"] + ".o")
            if obj.is_file() and not obj.is_symlink():
                attempt["object_sha256"] = sha256(obj.read_bytes())
            attempts.append(attempt)
            if "reason" not in family:
                family.update(reason=reason, failed_setting=level["id"])
        for level in profile["levels"]:
            obj = output / (str(number) + "-" + level["id"] + ".o")
            if obj.exists():
                raise ValueError("Refusing stale family object")
            execution_profile = dict(profile, timeout_tool=timeout_tool)
            try:
                result = compile_profile(execution_profile, source, obj, level["flags"], root=root, timeout=20)
                diagnostic = result["stdout"] + result["stderr"]
                (output / (obj.stem + ".log")).write_text(diagnostic, encoding="utf-8")
                if (result["returncode"] or not obj.is_file()
                        or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
                    reject_attempt(level, "compiler/assembler failure, warning or missing object",
                                   returncode=result["returncode"], failed_stage=result.get("failed_stage", "compiler"))
                    continue
                reject_link(obj)
                comparison = compare_object(obj.read_bytes(), reference, manifest)
                rows.append({"setting": level["id"], "flags": profile["common_flags"] + level["flags"],
                             "assembler_flags": profile.get("assembler_flags", []),
                             "exact_probes": sum(c["exact_probe_bytes"] for c in comparison["comparisons"]),
                             "artifacts": result.get("artifacts", {}), **comparison})
                attempts.append({"setting": level["id"], "status": "OBJECT_VALIDATED",
                                 "object_sha256": comparison["object_sha256"]})
            except (OSError, subprocess.SubprocessError) as error:
                reject_attempt(level, "profile execution unavailable: " + type(error).__name__)
            except ValueError as error:
                reject_attempt(level, "profile output rejected: " + str(error))
        if not cohort_failed:
            family.update(status="COMPLETE", rows=rows)
        elif rows:
            family.update(status="INCOMPLETE_SETTINGS", rows=rows)
        family["attempts"] = attempts
        family["completed_settings"] = len(rows)
        # A rejected setting never exposes a partial function score. Other
        # complete settings stay visible, alongside every declared failure.
        report["families"].append(family)
    verify_profile_files(root, config)
    check_identity(file_identity(reference_path), lock["decrypted_executable"], "Family reference changed")
    if profiles_path.read_bytes() != config_raw or lock_path.read_bytes() != lock_raw or manifest_path.read_bytes() != manifest_raw:
        raise ValueError("Family freeze/metadata changed during execution")
    report["completed_profiles"] = sum(f["status"] == "COMPLETE" for f in report["families"])
    report["partial_profiles"] = sum(f["status"] == "INCOMPLETE_SETTINGS" for f in report["families"])
    report["declared_profiles"] = len(profiles)
    report["completed_configurations"] = sum(len(f["rows"]) for f in report["families"])
    report["declared_configurations"] = 4 * len(profiles)
    write_report(output / "report.json", report)
    if report_path is not None:
        write_report(report_path, report)
    return report


def main(argv=None):
    """Run the native pinned investigation, relaunching from Windows via WSL."""
    args_list = sys.argv[1:] if argv is None else argv
    if os.name == "nt":
        result = subprocess.run(["wsl", "-d", "Ubuntu", "--", "python3",
                                 runtime_root(ROOT, "Ubuntu") + "/scripts/bench_compiler_families.py", *args_list],
                                stdin=subprocess.DEVNULL, cwd=ROOT)
        return result.returncode
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="evidence/bucket-03d/compiler-families.json")
    args = parser.parse_args(args_list)
    try:
        report = run_families(report_path=ROOT / args.report)
        for family in report["families"]:
            if family["status"] != "COMPLETE":
                print(family["family"] + ": " + family["status"] + "; rejected setting(s) unscored: " + family["reason"])
            for row in family["rows"]:
                print(family["family"] + " / " + row["setting"] + ": " + str(row["exact_probes"])
                      + "/" + str(report["probe_count"]) + " exact probe sequences")
        print("FAMILY INVESTIGATION ONLY: no toolchain lock or matching credit")
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("FAMILY INVESTIGATION FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
