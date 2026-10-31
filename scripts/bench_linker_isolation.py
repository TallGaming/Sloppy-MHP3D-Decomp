#!/usr/bin/env python3
"""Compare two prefrozen layouts using one fresh invented SNC object per trial.

No game code is compiled or linked. The default layout's placement is observed;
the explicit layout has a declared base. Both require the same strict entry,
complete-function and load-mapping checks before claiming byte preservation.
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
    from .bench_compiler_families import compile_profile, profile_items
    from .bench_synthetic_link import digest, inspect_fixture, compare_linked_fixture, link_fixture, local_items, verify_inputs
    from .prepare_reference import check_identity, file_identity, reject_link, write_report
except ImportError:
    from bench_compiler_families import compile_profile, profile_items
    from bench_synthetic_link import digest, inspect_fixture, compare_linked_fixture, link_fixture, local_items, verify_inputs
    from prepare_reference import check_identity, file_identity, reject_link, write_report

ROOT = Path(__file__).resolve().parents[1]


def assess_case(input_bytes, output_bytes, case):
    """Observe default placement without relaxing entry or complete-byte checks."""
    expected = case["expected_entry_address"]
    if expected is None:
        expected = inspect_fixture(output_bytes, 2)["function"]["address"]
    return compare_linked_fixture(input_bytes, output_bytes, expected)


def verify_isolation_inputs(root, config):
    """Verify the new layout plus all unchanged previous compiler/linker pins."""
    for key in ("baseline_experiment", "minimal_layout"):
        item = config[key]
        path = root / item["relative_path"]
        reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Isolation input escapes project")
        check_identity(file_identity(path), item, "Isolation input")
    base = json.loads((root / config["baseline_experiment"]["relative_path"]).read_bytes())
    families = verify_inputs(root, base)
    prefix = ["{linker}", *base["common_link_flags"]]
    tail = ["-Map", "{map}", "-o", "{output}", "{object}"]
    expected_cases = [
        {"id": "default_layout", "expected_entry_address": None, "command_template": prefix + tail},
        {"id": "minimal_explicit_layout", "expected_entry_address": 0x08804000,
         "command_template": prefix + ["-T", "{layout}"] + tail},
    ]
    if (config["cases"] != expected_cases or config["compiler_profile_id"] != "psp_snc_1_2_7503"
            or config["optimization"] != ["-O0"] or config["entry_symbol"] != "family_smoke"
            or config["common_link_flags"] != base["common_link_flags"]
            or config["runner"] != base["runner"] or config["timeout_seconds"] != base["timeout_seconds"]
            or config["trial_count"] != 2 or config["no_libraries"] is not True
            or config["same_object_for_both_cases"] is not True or config["compile_once_per_trial"] is not True):
        raise ValueError("Isolation profile differs from the two declared cases")
    profiles = [p for p in families["profiles"] if p["id"] == config["compiler_profile_id"]]
    if len(profiles) != 1 or profiles[0]["status"] != "runnable":
        raise ValueError("Isolation requires the existing runnable SNC profile")
    return base, families, profiles[0]


def run_isolation(*, root=ROOT, config_path=None, report_path=None):
    """Run both cases on one immutable object and preserve every failed outcome."""
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/linker-isolation.json"
    raw = config_path.read_bytes()
    config = json.loads(raw)
    if (config["status"] != "frozen_before_isolation_outputs"
            or config["no_isolation_link_outputs_observed"] is not True):
        raise ValueError("Isolation cases were not frozen before outputs")
    protected = {config_path.resolve()} | {(root / config[k]["relative_path"]).resolve()
                                          for k in ("baseline_experiment", "minimal_layout")}
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        if report_path.resolve() in protected:
            raise ValueError("Isolation report aliases input")
    base, families, profile = verify_isolation_inputs(root, config)
    protected |= {(root / i["relative_path"]).resolve() for i in local_items(base) + profile_items(families)}
    protected |= {Path(i["linux_path"]).resolve() for i in base["native_windows_dependencies"]}
    if report_path is not None and report_path.resolve() in protected:
        raise ValueError("Isolation report aliases inherited input")
    build = root / "build"
    reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("Isolation build escapes project")
    build.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="linker-isolation-", dir=build))
    obj = directory / "snc-smoke.o"
    report = {"schema_version": 1, "status": "LINKER_ISOLATION_INVESTIGATION_COMPLETE",
              "profile_sha256": digest(raw), "baseline_profile_sha256": config["baseline_experiment"]["sha256"],
              "source_sha256": base["source"]["sha256"], "matched_progress": 0,
              "compiler_profile_id": profile["id"], "optimization": ["-O0"], "cases": []}
    input_bytes = None
    try:
        execution = compile_profile(dict(profile, timeout_tool=families["linux_utilities"][0]["linux_path"]),
                                    root / base["source"]["relative_path"], obj, ["-O0"], root=root)
        diagnostic = execution["stdout"] + execution["stderr"]
        (directory / "compile.log").write_text(diagnostic, encoding="utf-8")
        report["compile_returncode"] = execution["returncode"]
        if (execution["returncode"] or not obj.is_file()
                or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
            report["compile_reason"] = "Compiler failure, warning or missing object"
        else:
            reject_link(obj)
            candidate = obj.read_bytes()
            report["input"] = inspect_fixture(candidate, 1)
            input_bytes = candidate
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        report["compile_reason"] = "Compilation unavailable or rejected: " + type(error).__name__ + ": " + str(error)
    for case in config["cases"]:
        row = {"id": case["id"], "expected_entry_address": case["expected_entry_address"],
               "status": "NOT_RUN_COMPILE_FAILED"}
        if input_bytes is None:
            report["cases"].append(row)
            continue
        reject_link(obj)
        if obj.read_bytes() != input_bytes:
            raise ValueError("Shared fixture object changed before link case")
        case_directory = directory / case["id"]
        case_directory.mkdir()
        output, map_path = case_directory / "fixture.elf", case_directory / "fixture.map"
        row.update(status="LINK_FAILED", input_sha256=digest(input_bytes))
        execution_config = dict(base, layout=config["minimal_layout"], command_template=case["command_template"])
        try:
            execution = link_fixture(execution_config, obj, output, map_path, root=root)
            diagnostic = execution["stdout"] + execution["stderr"]
            (case_directory / "link.log").write_text(diagnostic, encoding="utf-8")
            row["link_returncode"] = execution["returncode"]
            if output.is_file():
                reject_link(output)
                row["output_sha256"] = digest(output.read_bytes())
            if (execution["returncode"] or not output.is_file() or not map_path.is_file()
                    or re.search(r"\b(warning|error|fatal)\b", diagnostic, re.I)):
                row["reason"] = "Linker failure, warning or missing output/map"
            else:
                reject_link(map_path)
                row.update(assess_case(input_bytes, output.read_bytes(), case))
        except (OSError, subprocess.SubprocessError) as error:
            row["reason"] = "Link execution unavailable: " + type(error).__name__
        except ValueError as error:
            row.update(status="VALIDATION_FINDING", reason=str(error))
        # A mutated shared object invalidates the trial, rather than letting a
        # later case use different bytes and calling that a layout comparison.
        reject_link(obj)
        if obj.read_bytes() != input_bytes:
            raise ValueError("Linker changed shared fixture object")
        report["cases"].append(row)
    verify_isolation_inputs(root, config)
    if config_path.read_bytes() != raw:
        raise ValueError("Isolation profile changed during trial")
    report["preserved_cases"] = sum(c["status"] == "PRESERVED" for c in report["cases"])
    if report_path is not None:
        write_report(report_path, report)
    return report, directory


def main():
    """Run one trial; repeat with another report path for the planned second trial."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="evidence/bucket-03f/isolation-trial.json")
    args = parser.parse_args()
    if os.name == "nt":
        return subprocess.run(["wsl", "-d", "Ubuntu", "--", "python3", "scripts/bench_linker_isolation.py",
                               "--report", args.report], cwd=ROOT).returncode
    try:
        report, directory = run_isolation(report_path=ROOT / args.report)
        print(json.dumps({"status": report["status"], "preserved_cases": report["preserved_cases"],
                          "build_directory": str(directory), "report": args.report}))
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
