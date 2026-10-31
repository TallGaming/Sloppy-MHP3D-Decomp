#!/usr/bin/env python3
"""Compare one frozen natural archive-key hypothesis with its complete interval.

This uses the unchanged MW219/C++/O2 diagnostic pipeline. An exact interval
would not establish original class/language, a linked build or game-match credit.
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
    from .bench_compiler import validate_probes
    from .bench_compiler_families import compile_profile, profile_items, sha256
    from .bench_language_modes import compare_language_object, local_items as language_items, verify_inputs as verify_language_inputs
    from .elf32 import Elf32
    from .prepare_reference import check_identity, file_identity, reject_link, write_report
except ImportError:
    from bench_compiler import validate_probes
    from bench_compiler_families import compile_profile, profile_items, sha256
    from bench_language_modes import compare_language_object, local_items as language_items, verify_inputs as verify_language_inputs
    from elf32 import Elf32
    from prepare_reference import check_identity, file_identity, reject_link, write_report

ROOT = Path(__file__).resolve().parents[1]


def compare_archive_object(data, reference, manifest, symbol):
    """Use one exact raw member name, preserving the original ELF bytes."""
    if len(manifest["probes"]) != 1:
        raise ValueError("Archive experiment requires exactly one function")
    return compare_language_object(data, reference, manifest, {manifest["probes"][0]["name"]: symbol})


def local_items(config):
    """List the frozen candidate, interpretation, naming and inherited profile."""
    return [config[k] for k in ("language_profile", "source", "target_manifest", "source_hypothesis",
                                "naming_source", "naming_evidence", "naming_object")]


def verify_archive_inputs(root, config):
    """Check exact source/target/naming bindings before and after compilation."""
    for item in local_items(config):
        path = root / item["relative_path"]
        reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Archive input escapes project")
        check_identity(file_identity(path), item, "Archive input")
    language = json.loads((root / config["language_profile"]["relative_path"]).read_bytes())
    families, profile, unused, reference, reference_pin = verify_language_inputs(root, language)
    manifest = json.loads((root / config["target_manifest"]["relative_path"]).read_bytes())
    naming = json.loads((root / config["naming_evidence"]["relative_path"]).read_bytes())
    hypothesis = json.loads((root / config["source_hypothesis"]["relative_path"]).read_bytes())
    if (config["common_flags"] != ["-nostdinc", "-lang", "c++", "-c"]
            or config["optimization"] != ["-O2"] or config["declared_trials"] != 2
            or config["source_attempts"] != 1 or len(manifest["probes"]) != 1
            or config["canonical_name"] != "archive_key_initialize"
            or config["target_address"] != 0x0886233C or config["target_size"] != 68
            or config["object_symbol"] != "initialize_key__17ArchiveKeyContextFUi"):
        raise ValueError("Archive profile differs from the single reviewed hypothesis")
    target = manifest["probes"][0]
    if (target["name"] != config["canonical_name"] or target["address"] != config["target_address"]
            or target["size"] != config["target_size"] or manifest["source"] != config["source"]["relative_path"]
            or hypothesis["source"] != config["source"] or hypothesis["target_manifest"] != config["target_manifest"]
            or hypothesis["naming_fixture"] != config["naming_source"]
            or hypothesis["attempt_count"] != 1 or hypothesis["matching_tricks"] != 0):
        raise ValueError("Archive source/target binding differs from review")
    if (naming["source"] != config["naming_source"] or naming["object"] != config["naming_object"]
            or naming["flags"] != config["common_flags"] + config["optimization"]
            or naming["object_symbol"] != config["object_symbol"]
            or naming["canonical_name"] != config["canonical_name"] or naming["diagnostic"] != ""):
        raise ValueError("Archive member name differs from invented naming evidence")
    obj = Elf32((root / config["naming_object"]["relative_path"]).read_bytes())
    functions = list(obj.functions())
    if (obj.file_type != 1 or len(functions) != 1 or functions[0]["name"] != config["object_symbol"]
            or functions[0]["size"] <= 0 or functions[0]["size"] % 4
            or obj.sections[functions[0]["section_index"]]["flags"] & 6 != 6):
        raise ValueError("Invalid invented member-naming object")
    validate_probes(reference, manifest)
    return families, profile, manifest, reference, reference_pin, language


def run_archive_key(*, root=ROOT, config_path=None, report_path=None):
    """Compile once freshly; reject incomplete output or changing input/evidence."""
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/archive-key-experiment.json"
    raw = config_path.read_bytes()
    config = json.loads(raw)
    if (config["status"] != "frozen_before_archive_candidate_compilation"
            or config["no_archive_candidate_compilation_observed"] is not True):
        raise ValueError("Archive candidate was not frozen before compilation")
    protected = {config_path.resolve()} | {(root / i["relative_path"]).resolve() for i in local_items(config)}
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        if report_path.resolve() in protected:
            raise ValueError("Archive report aliases an input")
    families, profile, manifest, reference, reference_pin, language = verify_archive_inputs(root, config)
    inherited = profile_items(families) + language_items(language) + [reference_pin]
    if report_path is not None and report_path.resolve() in {(root / i["relative_path"]).resolve() for i in inherited}:
        raise ValueError("Archive report aliases inherited input")
    build = root / "build"
    reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("Archive build escapes project")
    build.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="archive-key-probe-", dir=build))
    obj = directory / "candidate.o"
    report = {"schema_version": 1, "status": "ARCHIVE_KEY_INVESTIGATION_COMPLETE",
              "profile_sha256": sha256(raw), "source_sha256": config["source"]["sha256"],
              "reference_sha256": reference_pin["sha256"], "matched_progress": 0,
              "flags": config["common_flags"] + config["optimization"],
              "outcome": "REJECTED_NO_SCORE", "comparisons": []}
    emitted = None
    try:
        execution = compile_profile(dict(profile, common_flags=config["common_flags"],
                                          timeout_tool=families["linux_utilities"][0]["linux_path"]),
                                    root / config["source"]["relative_path"], obj, config["optimization"], root=root)
        diagnostic = execution["stdout"] + execution["stderr"]
        (directory / "compile.log").write_text(diagnostic, encoding="utf-8")
        report["returncode"] = execution["returncode"]
        if obj.is_file():
            reject_link(obj)
            emitted = obj.read_bytes()
            report["object_sha256"] = sha256(emitted)
        if (execution["returncode"] or emitted is None
                or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
            report["reason"] = "Compiler failure, warning or missing object"
        else:
            comparison = compare_archive_object(emitted, reference, manifest, config["object_symbol"])
            report.update(comparison, outcome="COMPLETE", exact_probes=sum(c["exact_probe_bytes"] for c in comparison["comparisons"]))
    except (OSError, subprocess.SubprocessError) as error:
        report["reason"] = "Compilation unavailable: " + type(error).__name__
    except ValueError as error:
        report["reason"] = "Object rejected: " + str(error)
    if emitted is not None:
        reject_link(obj)
        if obj.read_bytes() != emitted:
            raise ValueError("Archive object changed during trial")
    verify_archive_inputs(root, config)
    if config_path.read_bytes() != raw:
        raise ValueError("Archive profile changed during trial")
    if report_path is not None:
        write_report(report_path, report)
    return report, directory


def main():
    """Run a fresh trial through the established WSL toolchain environment."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="evidence/bucket-03i/archive-key-trial.json")
    args = parser.parse_args()
    if os.name == "nt":
        return subprocess.run(["wsl", "-d", "Ubuntu", "--", "python3", "scripts/bench_archive_key.py",
                               "--report", args.report], cwd=ROOT).returncode
    try:
        report, directory = run_archive_key(report_path=ROOT / args.report)
        print(json.dumps({"status": report["status"], "outcome": report["outcome"],
                          "build_directory": str(directory), "report": args.report}))
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
