"""Test two readable archive-key source copies against the complete target.

The original draft is an immutable historical control. No byte trimming, register
normalization or flag selection is performed; successful object comparison is
reported independently of full-game matching credit, which remains zero.
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
    from . import bench_archive_key as archive
    from .bench_address_reuse import inspect_address_fixture
    from .bench_mw_archive_versions import diff_words
except ImportError:
    import bench_archive_key as archive
    from bench_address_reuse import inspect_address_fixture
    from bench_mw_archive_versions import diff_words

ROOT = Path(__file__).resolve().parents[1]


def local_items(config):
    return [config["archive_profile"], config["historical_object"],
            *[item["source"] for item in config["forms"]]]


def verify_inputs(root, config):
    for item in local_items(config):
        path = root / item["relative_path"]
        archive.reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Archive pointer input escapes project")
        archive.check_identity(archive.file_identity(path), item, "Archive pointer input")
    original = json.loads((root / config["archive_profile"]["relative_path"]).read_bytes())
    families, profile, manifest, reference, reference_pin, language = archive.verify_archive_inputs(root, original)
    if (config["status"] != "frozen_before_source_compilation"
            or config["common_flags"] != original["common_flags"]
            or config["optimization"] != original["optimization"]
            or config["object_symbol"] != original["object_symbol"]
            or config["field_offsets"] != {"lower": 0x2F53C, "upper": 0x2F540}
            or config["defaults"] != {"lower": 0x7F8D, "upper": 0x2345}
            or config["declared_trials"] != 2 or config["plain_source_budget"] != 3
            or [(item["id"], item["attempt"]) for item in config["forms"]]
               != [("flat", 1), ("grouped", 2), ("pointer", 3)]
            or config["forms"][0]["source"] != original["source"]):
        raise ValueError("Archive pointer experiment differs from the three reviewed source forms")
    inherited = (archive.local_items(original) + archive.language_items(language)
                 + archive.profile_items(families) + [reference_pin])
    return families, profile, manifest, reference, reference_pin, inherited


def run_archive_pointer(*, root=ROOT, config_path=None, report_path=None):
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/archive-pointer.json"
    archive.reject_link(config_path)
    raw = config_path.read_bytes()
    config = json.loads(raw)
    families, profile, manifest, reference, reference_pin, inherited = verify_inputs(root, config)
    protected = {config_path.resolve()} | {
        (root / item["relative_path"]).resolve() for item in local_items(config) + inherited}
    if report_path is not None:
        report_path = Path(report_path)
        archive.reject_link(report_path)
        if report_path.resolve() in protected:
            raise ValueError("Archive pointer report aliases an input")
        if report_path.exists():
            raise ValueError("Preserve existing archive pointer report")
    build = root / "build"
    archive.reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("Archive pointer build escapes project")
    build.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="archive-pointer-", dir=build))
    target = reference.virtual_bytes(manifest["probes"][0]["address"], manifest["probes"][0]["size"])
    report = {"schema_version": 1, "status": "ARCHIVE_POINTER_INVESTIGATION_INCOMPLETE",
              "profile_sha256": archive.sha256(raw), "reference_sha256": reference_pin["sha256"],
              "matched_progress": 0, "flags": config["common_flags"] + config["optimization"],
              "declared_source_attempts": 3, "attempted_source_count": 1,
              "plain_source_budget_exhausted": False,
              "forms": []}
    emitted = {}
    for form in config["forms"]:
        output = directory / (form["id"] + ".o")
        row = {"id": form["id"], "attempt": form["attempt"],
               "source_sha256": form["source"]["sha256"], "outcome": "REJECTED_NO_SCORE"}
        try:
            report["attempted_source_count"] = max(report["attempted_source_count"], form["attempt"])
            result = archive.compile_profile(
                dict(profile, common_flags=config["common_flags"],
                     timeout_tool=families["linux_utilities"][0]["linux_path"]),
                root / form["source"]["relative_path"], output, config["optimization"], root=root)
            diagnostic = result["stdout"] + result["stderr"]
            output.with_suffix(".log").write_text(diagnostic, encoding="utf-8")
            row["returncode"] = result["returncode"]
            if output.is_file():
                archive.reject_link(output)
                emitted[output] = output.read_bytes()
                row["object_sha256"] = archive.sha256(emitted[output])
            if (result["returncode"] or output not in emitted
                    or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
                row["reason"] = "Compiler failure, warning or missing object"
            elif (form["id"] == "flat" and emitted[output] !=
                  (root / config["historical_object"]["relative_path"]).read_bytes()):
                row["outcome"] = "CONTROL_MISMATCH"
                row["reason"] = "Direct whole object differs from historical control"
            else:
                comparison = archive.compare_archive_object(
                    emitted[output], reference, manifest, config["object_symbol"])
                observation = inspect_address_fixture(
                    emitted[output], config["object_symbol"], config["field_offsets"])
                body = bytes.fromhex(observation["function"]["bytes_hex"])
                difference = diff_words(body, target)
                row.update(comparison, outcome="COMPLETE", observation=observation,
                           full_word_difference=difference)
        except (OSError, subprocess.SubprocessError, ValueError) as error:
            row["reason"] = type(error).__name__ + ": " + str(error)
        # Preserve partial failure objects without accepting or scoring them.
        if output.exists() or output.is_symlink():
            archive.reject_link(output)
            if not output.is_file():
                raise ValueError("Archive pointer output is not a regular file")
            data = output.read_bytes()
            if output in emitted and emitted[output] != data:
                raise ValueError("Archive pointer object changed while inspected")
            emitted[output] = data
            row["object_sha256"] = archive.sha256(data)
        report["forms"].append(row)
        if form["id"] == "flat" and row["outcome"] != "COMPLETE":
            break
    verify_inputs(root, config)
    if config_path.read_bytes() != raw:
        raise ValueError("Archive pointer profile changed during trial")
    for output, data in emitted.items():
        archive.reject_link(output)
        if output.read_bytes() != data:
            raise ValueError("Retained archive pointer output changed during trial")
    if len(report["forms"]) == 3 and all(item["outcome"] == "COMPLETE" for item in report["forms"]):
        report["status"] = "ARCHIVE_POINTER_INVESTIGATION_COMPLETE"
    report["plain_source_budget_exhausted"] = report["attempted_source_count"] >= config["plain_source_budget"]
    if report_path is not None:
        archive.write_report(report_path, report)
    return report, directory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    if os.name == "nt":
        return subprocess.run(["wsl", "-d", "Ubuntu", "--", "python3",
                               "scripts/bench_archive_pointer.py", "--report", args.report], cwd=ROOT).returncode
    report, directory = run_archive_pointer(report_path=ROOT / args.report)
    print(json.dumps({"status": report["status"], "build_directory": str(directory), "report": args.report}))
    return 0 if report["status"] == "ARCHIVE_POINTER_INVESTIGATION_COMPLETE" else 1


if __name__ == "__main__":
    sys.exit(main())
