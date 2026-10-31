"""Compare grouped member access with one named pointer, under fixed MW219/O2.

This is an invented source-expression diagnostic. Full ELF/function equality,
historical control reproduction and bounded address inspection are separate
observations. It never compares a new source hypothesis with game bytes.
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
    from . import bench_address_reuse as address
except ImportError:
    import bench_address_reuse as address

ROOT = Path(__file__).resolve().parents[1]


def local_items(config):
    return [config["grouping_profile"], config["historical_control"],
            *[item["source"] for item in config["fixtures"]]]


def verify_pointer_inputs(root, config):
    """Keep all prior game/settings inputs and the two declared cases frozen."""
    for item in local_items(config):
        path = root / item["relative_path"]
        address.reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Pointer fixture input escapes project")
        address.check_identity(address.file_identity(path), item, "Pointer fixture input")
    grouping = json.loads((root / config["grouping_profile"]["relative_path"]).read_bytes())
    families, profile, archive, language, reference_pin = address.verify_inputs(root, grouping)
    if (config["status"] != "frozen_before_fixture_compilation"
            or config["common_flags"] != grouping["common_flags"]
            or config["optimization"] != grouping["optimization"]
            or config["object_symbol"] != grouping["object_symbol"]
            or config["field_offsets"] != grouping["field_offsets"]
            or config["defaults"] != grouping["defaults"]
            or config["declared_trials"] != 2
            or config["named_pointer_only"] is not True
            or [item["id"] for item in config["fixtures"]] != ["grouped", "pointer"]
            or config["fixtures"][0]["source"] != grouping["fixtures"][1]["source"]):
        raise ValueError("Pointer fixtures differ from the reviewed fixed two-case scope")
    inherited = (address.local_items(grouping) + address.archive_items(archive)
                 + address.language_items(language) + address.profile_items(families)
                 + [reference_pin])
    return families, profile, inherited


def run_pointer_reuse(*, root=ROOT, config_path=None, report_path=None):
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/pointer-reuse.json"
    address.reject_link(config_path)
    raw = config_path.read_bytes()
    config = json.loads(raw)
    families, profile, inherited = verify_pointer_inputs(root, config)
    protected = {config_path.resolve()} | {
        (root / item["relative_path"]).resolve() for item in local_items(config) + inherited}
    if report_path is not None:
        report_path = Path(report_path)
        address.reject_link(report_path)
        if report_path.resolve() in protected:
            raise ValueError("Pointer fixture report aliases an input")
        # Refuse a conflicting report before creating outputs or invoking tools.
        if report_path.exists():
            raise ValueError("Preserve existing pointer fixture report")
    build = root / "build"
    address.reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("Pointer fixture build escapes project")
    build.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="pointer-reuse-", dir=build))
    report = {"schema_version": 1, "status": "POINTER_REUSE_INVESTIGATION_INCOMPLETE",
              "profile_sha256": address.sha256(raw), "matched_progress": 0,
              "flags": config["common_flags"] + config["optimization"],
              "fixtures": [], "function_comparison": None,
              "address_comparison": {"status": "UNINTERPRETED", "static_site_reduction": None}}
    emitted = {}
    for fixture in config["fixtures"]:
        output = directory / (fixture["id"] + ".o")
        row = {"id": fixture["id"], "source_sha256": fixture["source"]["sha256"],
               "outcome": "OUTPUT_REJECTED"}
        try:
            execution = address.compile_profile(
                dict(profile, common_flags=config["common_flags"],
                     timeout_tool=families["linux_utilities"][0]["linux_path"]),
                root / fixture["source"]["relative_path"], output,
                config["optimization"], root=root)
            diagnostic = execution["stdout"] + execution["stderr"]
            output.with_suffix(".log").write_text(diagnostic, encoding="utf-8")
            row["returncode"] = execution["returncode"]
            if output.is_file():
                address.reject_link(output)
                emitted[output] = output.read_bytes()
                row["object_sha256"] = address.sha256(emitted[output])
            if (execution["returncode"] or output not in emitted
                    or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
                row["reason"] = "Compiler failure, warning or missing object"
            elif (fixture["id"] == "grouped" and
                  emitted[output] != (root / config["historical_control"]["relative_path"]).read_bytes()):
                row["outcome"] = "CONTROL_MISMATCH"
                row["reason"] = "Grouped complete object differs from the pinned historical control"
            else:
                row["observation"] = address.inspect_address_fixture(
                    emitted[output], config["object_symbol"], config["field_offsets"])
                row["outcome"] = "OBJECT_VALIDATED"
        except (OSError, subprocess.SubprocessError, ValueError) as error:
            row["reason"] = type(error).__name__ + ": " + str(error)
        # A failed or interrupted compiler can still leave an output. Preserve
        # its identity as failure evidence and include it in the final drift
        # check; its existence never changes the rejected outcome.
        if output.exists() or output.is_symlink():
            address.reject_link(output)
            if not output.is_file():
                raise ValueError("Pointer fixture output is not a regular file")
            retained = output.read_bytes()
            if output in emitted and emitted[output] != retained:
                raise ValueError("Pointer fixture object changed while inspected")
            emitted[output] = retained
            row["object_sha256"] = address.sha256(retained)
        report["fixtures"].append(row)
        if row["outcome"] != "OBJECT_VALIDATED":
            break
    verify_pointer_inputs(root, config)
    if config_path.read_bytes() != raw:
        raise ValueError("Pointer fixture profile changed during trial")
    for output, original in emitted.items():
        address.reject_link(output)
        if output.read_bytes() != original:
            raise ValueError("Emitted pointer fixture object changed during trial")
    if len(report["fixtures"]) == 2 and all(row["outcome"] == "OBJECT_VALIDATED" for row in report["fixtures"]):
        first, second = [row["observation"] for row in report["fixtures"]]
        a, b = first["function"], second["function"]
        report["status"] = "POINTER_REUSE_INVESTIGATION_COMPLETE"
        report["function_comparison"] = {
            "identical": a["bytes_hex"] == b["bytes_hex"],
            "grouped_size": a["size"], "pointer_size": b["size"],
            "grouped_sha256": a["sha256"], "pointer_sha256": b["sha256"],
            "whole_objects_identical": report["fixtures"][0]["object_sha256"] == report["fixtures"][1]["object_sha256"]}
        analysis = [item["address_analysis"] for item in (first, second)]
        if all(item["status"] == "INTERPRETED" for item in analysis):
            report["address_comparison"] = {"status": "INTERPRETED", "static_site_reduction":
                analysis[0]["large_base_site_count"] - analysis[1]["large_base_site_count"]}
    if report_path is not None:
        address.write_report(report_path, report)
    return report, directory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    if os.name == "nt":
        return subprocess.run(["wsl", "-d", "Ubuntu", "--", "python3",
                               "scripts/bench_pointer_reuse.py", "--report", args.report], cwd=ROOT).returncode
    report, directory = run_pointer_reuse(report_path=ROOT / args.report)
    print(json.dumps({"status": report["status"], "build_directory": str(directory), "report": args.report}))
    return 0 if report["status"] == "POINTER_REUSE_INVESTIGATION_COMPLETE" else 1


if __name__ == "__main__":
    sys.exit(main())
