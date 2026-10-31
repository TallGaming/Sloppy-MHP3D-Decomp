#!/usr/bin/env python3
"""Create a fresh pinned Ghidra project and export Bucket 3B analysis.

Run through WSL Ubuntu on Windows. Original game bytes are opened read-only;
the local project and pseudocode exports remain ignored research artifacts.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

try:
    from .elf32 import Elf32
    from .bench_compiler import runtime_root
    from .prepare_reference import file_identity, check_identity, write_report
except ImportError:
    from elf32 import Elf32
    from bench_compiler import runtime_root
    from prepare_reference import file_identity, check_identity, write_report


ROOT = Path(__file__).resolve().parents[1]
TARGETS = (0x08830550, 0x08830654)


def validate_export(data, reference, probes):
    """Verify processor, code mapping, target bytes, bodies and direct callers.

    Types and pseudocode are never promoted to verified original source.
    Ghidra's workspace does not map every runtime memory/overlay reservation.
    """
    if data["language_id"] != "Allegrex:LE:32:default" or data["compiler_spec_id"] != "default":
        raise ValueError("Ghidra did not use the pinned PSP processor specification")
    if data["executable_sha256"].lower() != hashlib.sha256(reference.data).hexdigest():
        raise ValueError("Ghidra executable identity mismatch")
    text = [s for s in reference.sections if s["name"] == ".text"]
    if len(text) != 1:
        raise ValueError("Reference has no unique main text section")
    text = text[0]
    if int(data["image_base"], 16) != text["address"]:
        raise ValueError("Ghidra image base changed")
    mapped = [b for b in data["memory_blocks"] if b["name"] == ".text"]
    if (len(mapped) != 1 or int(mapped[0]["start"], 16) != text["address"]
            or int(mapped[0]["end"], 16) != text["address"] + text["size"] - 1
            or mapped[0]["size"] != text["size"] or not mapped[0]["initialized"]):
        raise ValueError("Ghidra main text mapping disagrees with the ELF")
    targets = {int(t["address"], 16): t for t in data["targets"]}
    if len(targets) != len(data["targets"]) or set(targets) != {p["address"] for p in probes}:
        raise ValueError("Ghidra target selection is missing or duplicated")
    functions = {int(f["entry"], 16): f for f in data["functions"]}
    if len(functions) != len(data["functions"]):
        raise ValueError("Ghidra function entries are duplicated")
    code = reference.section_data(text)
    verified = []
    for probe in probes:
        address, size = probe["address"], probe["size"]
        target = targets[address]
        expected = hashlib.sha256(reference.virtual_bytes(address, size)).hexdigest()
        if (expected != probe["target_sha256"] or target["memory_sha256"] != expected
                or target["size"] != size or target["function_at_start"] is None
                or int(target["function_at_start"], 16) != address):
            raise ValueError("Ghidra target memory or function start disagrees with the ELF")
        function = functions.get(address)
        if (not function or not function["decompile_completed"]
                or int(function["body_min"], 16) != address
                or int(function["body_max"], 16) != address + size - 1
                or function["body_address_count"] != size):
            raise ValueError("Ghidra target function body/decompilation is incomplete")
        expected_calls = set()
        for offset in range(0, len(code) - 3, 4):
            word = struct.unpack_from("<I", code, offset)[0]
            place = text["address"] + offset
            if word >> 26 == 3 and ((place + 4) & 0xF0000000 | (word & 0x03FFFFFF) << 2) == address:
                expected_calls.add(place)
        actual_calls = [int(c["site"], 16) for c in target["call_references"]]
        if len(actual_calls) != len(set(actual_calls)) or set(actual_calls) != expected_calls:
            raise ValueError("Ghidra direct call references disagree with the instruction scan")
        if any(c["caller"] is None or int(c["caller"], 16) not in functions
               for c in target["call_references"]):
            raise ValueError("A direct caller was not included in the analysis export")
        for call in target["call_references"]:
            caller = functions[int(call["caller"], 16)]
            if (not caller["decompile_completed"]
                    or not int(caller["body_min"], 16) <= int(call["site"], 16) <= int(caller["body_max"], 16)):
                raise ValueError("Reported caller body/decompilation does not cover its call site")
        verified.append({"address": address, "size": size, "sha256": expected,
                         "direct_call_sites": sorted(expected_calls),
                         "caller_entries": sorted({int(c["caller"], 16) for c in target["call_references"]})})
    return {"verified_targets": verified, "exported_function_count": len(functions),
            "completed_decompilations": sum(bool(f["decompile_completed"]) for f in functions.values()),
            "image_base": text["address"], "main_text_size": text["size"]}


def verify_tools(config):
    """Check downloaded archives and every pinned installed file/link."""
    item = config["installed_manifest"]
    path = ROOT / item["relative_path"]
    check_identity(file_identity(path), item, "Installed analysis manifest")
    manifest = json.loads(path.read_bytes())
    for entry in [*config["archives"], config["export_script"], *manifest["files"]]:
        path = ROOT / entry["relative_path"]
        if not path.resolve().is_relative_to(ROOT):
            raise ValueError("Analysis tool path escapes the project")
        if "symlink" in entry:
            if not path.is_symlink() or os.readlink(path) != entry["symlink"]:
                raise ValueError("Installed analysis symlink differs: " + str(path))
        else:
            if path.is_symlink():
                raise ValueError("Installed analysis file became a symlink")
            check_identity(file_identity(path), entry, "Installed analysis tool")


def main(argv=None):
    """Analyze the verified main ELF in a fresh, project-local Ghidra workspace."""
    args_list = sys.argv[1:] if argv is None else argv
    if os.name == "nt":
        # Run the same script under Linux so installed JDK symlinks are verified
        # with native filesystem semantics. CLI artifact paths are project-relative.
        result = subprocess.run(["wsl", "-d", "Ubuntu", "--", "python3",
                                 runtime_root(ROOT, "Ubuntu") + "/scripts/analyze_reference.py", *args_list],
                                stdin=subprocess.DEVNULL, cwd=ROOT)
        return result.returncode
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", default="reference/ghidra/bucket03b-review")
    parser.add_argument("--export", default="evidence/bucket-03b/ghidra-review.json")
    parser.add_argument("--report", default="evidence/bucket-03b/ghidra-review-summary.json")
    args = parser.parse_args(args_list)
    try:
        tool_path, lock_path = ROOT / "config/analysis-tools.json", ROOT / "config/reference.json"
        tool_raw, lock_raw = tool_path.read_bytes(), lock_path.read_bytes()
        tools, lock = json.loads(tool_raw), json.loads(lock_raw)
        if lock.get("status") != "active" or lock.get("baseline_selected_by_user") is not True:
            raise ValueError("No active user-selected reference")
        reference_path = ROOT / lock["decrypted_executable"]["relative_path"]
        check_identity(file_identity(reference_path), lock["decrypted_executable"], "Analysis reference")
        reference = Elf32(reference_path.read_bytes())
        manifest_path = ROOT / "config/compiler-probes.json"
        manifest_raw = manifest_path.read_bytes()
        probes = [p for p in json.loads(manifest_raw)["probes"] if p["address"] in TARGETS]
        if len(probes) != 2:
            raise ValueError("The two declared target probes are missing")
        project, export, report_path = ((ROOT / p).resolve() for p in (args.project_dir, args.export, args.report))
        console, log = report_path.with_suffix(".console.log"), report_path.with_suffix(".ghidra.log")
        if not project.is_relative_to(ROOT / "reference/ghidra"):
            raise ValueError("Ghidra project must stay under reference/ghidra")
        if len({export, report_path, console, log}) != 4 or any(not p.is_relative_to(ROOT / "evidence")
                or p.exists() for p in (export, report_path, console, log)) or project.exists():
            raise ValueError("Use fresh project and distinct evidence paths; existing artifacts are preserved")
        verify_tools(tools)
        project.mkdir(parents=True)
        export.parent.mkdir(parents=True, exist_ok=True)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        user_home = ROOT / "toolchains/ghidra-user"
        user_home.mkdir(exist_ok=True)
        environment = os.environ.copy()
        environment.update(JAVA_HOME=str(ROOT / tools["jdk"]["relative_path"]),
                           JAVA_TOOL_OPTIONS="-Duser.home=" + str(user_home))
        command = ["timeout", "600s", "bash", str(ROOT / tools["ghidra"]["relative_path"] / "support/analyzeHeadless"),
                   str(project), "mhp3rd", "-import", str(reference_path), "-scriptPath", str(ROOT / "scripts/ghidra"),
                   "-postScript", "ExportProbeAnalysis.java", str(export), "-analysisTimeoutPerFile", "300",
                   "-max-cpu", "2", "-log", str(log)]
        with console.open("xb") as stream:
            result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=stream, stderr=subprocess.STDOUT,
                                    env=environment, timeout=620)
        if result.returncode or not export.is_file():
            raise ValueError("Ghidra failed or produced no export; inspect the local console log")
        data = json.loads(export.read_bytes())
        summary = validate_export(data, reference, probes)
        console_text = console.read_text(errors="replace")
        if ("BUCKET_03B_EXPORT_COMPLETE" not in console_text or "Import succeeded" not in console_text
                or "Analysis timed out" in console_text):
            raise ValueError("Ghidra did not confirm completed import, analysis and export")
        check_identity(file_identity(reference_path), lock["decrypted_executable"], "Analysis reference changed")
        verify_tools(tools)
        if (tool_path.read_bytes() != tool_raw or lock_path.read_bytes() != lock_raw
                or manifest_path.read_bytes() != manifest_raw):
            raise ValueError("Analysis metadata changed during execution")
        report = {"schema_version": 1, "status": "PINNED_STATIC_ANALYSIS_COMPLETE",
                  "scope": "verified import and bounded static hypotheses; no game runtime or matching proof",
                  "tool_config_sha256": hashlib.sha256(tool_raw).hexdigest(),
                  "reference_sha256": lock["decrypted_executable"]["sha256"],
                  "probe_manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
                  "export_sha256": hashlib.sha256(export.read_bytes()).hexdigest(), **summary}
        write_report(report_path, report)
        print(report["status"] + ": " + str(summary["exported_function_count"]) + " functions/callers")
        return 0
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print("STATIC ANALYSIS FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
