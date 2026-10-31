#!/usr/bin/env python3
"""Compile and resolve an invented direct-call fixture across pinned candidates.

This diagnostic never reads or rewrites a game function. One fixed -O2 setting
is used for every candidate; it is not a proposed game toolchain configuration.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile

try:
    from .bench_compiler import compile_probe
    from .call_relocation import relocate_function
    from .prepare_reference import file_identity, check_identity, reject_link, write_report
except ImportError:
    from bench_compiler import compile_probe
    from call_relocation import relocate_function
    from prepare_reference import file_identity, check_identity, reject_link, write_report


ROOT = Path(__file__).resolve().parents[1]


def run_fixture(*, root=ROOT, fixture_lock_path=None, candidates_path=None, report_path=None):
    """Publish one complete, deterministic fixture report, failing on any row."""
    root = Path(root).resolve(strict=True)
    fixture_lock_path = Path(fixture_lock_path) if fixture_lock_path else root / "config/direct-call-fixture.json"
    candidates_path = Path(candidates_path) if candidates_path else root / "config/compiler-candidates.json"
    fixture_raw, candidate_raw = fixture_lock_path.read_bytes(), candidates_path.read_bytes()
    fixture, candidates = json.loads(fixture_raw), json.loads(candidate_raw)
    if fixture.get("status") != "invented_fixture_only_not_game_toolchain_lock":
        raise ValueError("Expected an invented-fixture lock")
    if hashlib.sha256(candidate_raw).hexdigest() != fixture["candidate_config_sha256"]:
        raise ValueError("Compiler candidate configuration hash mismatch")
    if candidates.get("status") != "investigation_only_not_locked":
        raise ValueError("Expected investigation-only compiler candidates")
    pinned = []
    def checked(item):
        path = root / item["relative_path"]
        reject_link(path)
        path = path.resolve(strict=True)
        if not path.is_relative_to(root):
            raise ValueError("Fixture input escapes the project")
        check_identity(file_identity(path), item, "Fixture input")
        pinned.append((path, item))
        return path
    source, runner = checked(fixture["source"]), checked(candidates["runner"])
    rows = candidates["candidates"]
    if not rows or len({row["id"] for row in rows}) != len(rows):
        raise ValueError("Fixture candidate list is empty or duplicated")
    compilers = []
    for candidate in rows:
        compilers.append(checked(candidate["compiler"]))
        for support in candidate["support_files"]:
            checked(support)
    flags = fixture["flags"]
    if not isinstance(flags, list) or any(not isinstance(flag, str) for flag in flags):
        raise ValueError("Invalid fixture compiler flags")
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        if report_path.resolve() in {p.resolve() for p in (fixture_lock_path, candidates_path, *[p for p, _ in pinned])}:
            raise ValueError("Report aliases a fixture input")
    parent = root / "build"
    reject_link(parent)
    parent.mkdir(exist_ok=True)
    output = Path(tempfile.mkdtemp(prefix="direct-call-", dir=parent)).resolve()
    report = {"schema_version": 1, "status": "DIRECT_CALL_DIAGNOSTIC_COMPLETE",
              "scope": "invented function bytes only; not game linking or matching",
              "fixture_lock_sha256": hashlib.sha256(fixture_raw).hexdigest(),
              "candidate_config_sha256": fixture["candidate_config_sha256"],
              "source_sha256": fixture["source"]["sha256"], "flags": flags,
              "load_address": fixture["load_address"], "symbols": fixture["symbols"],
              "matched_progress": 0, "results": []}
    for index, (candidate, compiler) in enumerate(zip(rows, compilers)):
        obj = output / (str(index) + ".o")
        if obj.exists():
            raise ValueError("Refusing stale fixture object")
        result = compile_probe(compiler, runner, source, obj, flags, timeout=20, root=root, distro="Ubuntu")
        diagnostic = result["stdout"] + result["stderr"]
        (output / (str(index) + ".log")).write_text(diagnostic, encoding="utf-8")
        if (result["returncode"] or not obj.is_file()
                or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
            raise ValueError("Fixture compiler failed: " + candidate["id"] + "; " + str(output))
        reject_link(obj)
        object_bytes = obj.read_bytes()
        resolved = relocate_function(object_bytes, function_name=fixture["function_name"],
                                     load_address=fixture["load_address"], symbols=fixture["symbols"],
                                     expected_calls=fixture["expected_calls"])
        for call in resolved["relocations"]:
            if call["resolved_word"] != fixture["expected_resolved_word"]:
                raise ValueError("Fixture call differs from independently declared word")
        (output / (str(index) + ".resolved.bin")).write_bytes(resolved["bytes"])
        report["results"].append({"candidate": candidate["id"],
                                  "object_sha256": hashlib.sha256(object_bytes).hexdigest(),
                                  "function_size": len(resolved["bytes"]),
                                  "resolved_function_sha256": hashlib.sha256(resolved["bytes"]).hexdigest(),
                                  "relocations": resolved["relocations"],
                                  "non_code_relocations": resolved["non_code_relocations"]})
    for path, item in pinned:
        check_identity(file_identity(path), item, "Fixture input changed")
    if fixture_lock_path.read_bytes() != fixture_raw or candidates_path.read_bytes() != candidate_raw:
        raise ValueError("Fixture metadata changed during compilation")
    write_report(output / "report.json", report)
    if report_path is not None:
        write_report(report_path, report)
    return report


def main(argv=None):
    """Run this controlled diagnostic independently from the frozen game bench."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=ROOT / "evidence/bucket-03b/direct-call.json")
    args = parser.parse_args(argv)
    try:
        report = run_fixture(report_path=args.report)
        print(report["status"] + ": " + str(len(report["results"])) + " compiler candidates; no matching credit")
        return 0
    except (OSError, ValueError, KeyError, TypeError, struct.error, subprocess.SubprocessError) as error:
        print("DIRECT CALL DIAGNOSTIC FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
