#!/usr/bin/env python3
"""Trace one invented function through frozen compiler and linker stages.

This diagnostic grants no game matching credit and never changes ELF inputs.
Linux compilers run under WSL; the existing linker runs through native Windows
interop because wibo does not complete its version-resource path reliably.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import struct
import subprocess
import sys
import tempfile

try:
    from .bench_compiler_families import compile_profile, verify_profile_files
    from .elf32 import Elf32
    from .prepare_reference import check_identity, file_identity, reject_link, write_report
except ImportError:
    from bench_compiler_families import compile_profile, verify_profile_files
    from elf32 import Elf32
    from prepare_reference import check_identity, file_identity, reject_link, write_report

ROOT = Path(__file__).resolve().parents[1]


def digest(data):
    """Hash complete bytes, including metadata and compiler padding."""
    return hashlib.sha256(data).hexdigest()


def inspect_fixture(data, expected_type, symbol="family_smoke"):
    """Require one complete executable function and retain exact metadata bytes."""
    elf = Elf32(data)
    if expected_type not in (1, 2) or elf.file_type != expected_type:
        raise ValueError("Unexpected fixture ELF type")
    functions = list(elf.functions())
    if len(functions) != 1 or functions[0]["name"] != symbol:
        raise ValueError("Expected exactly one fixture function symbol")
    function = functions[0]
    section = elf.sections[function["section_index"]]
    if (function["size"] <= 0 or function["size"] % 4 or function["section_offset"] % 4
            or section["flags"] & 6 != 6 or section["type"] != 1):
        raise ValueError("Fixture function is not complete allocated executable code")
    # No calls exist in this fixture. Do not pretend to compare unapplied code
    # relocations; noncode compiler metadata remains visible to the linker.
    for relocation in elf.sections:
        if relocation["type"] not in (4, 9):
            continue
        if (not 0 < relocation["info"] < len(elf.sections)
                or not 0 < relocation["link"] < len(elf.sections)
                or elf.sections[relocation["link"]]["type"] != 2
                or relocation["entry_size"] != (12 if relocation["type"] == 4 else 8)
                or relocation["size"] % relocation["entry_size"]):
            raise ValueError("Invalid fixture relocation section")
        if relocation["size"] and elf.sections[relocation["info"]]["flags"] & 4:
            raise ValueError("Unsupported fixture code relocation")
        symbols = elf.sections[relocation["link"]]
        if symbols["entry_size"] != 16 or symbols["size"] % 16:
            raise ValueError("Invalid fixture relocation symbol table")
        target = elf.sections[relocation["info"]]
        fmt = "<IIi" if relocation["type"] == 4 else "<II"
        for record in struct.iter_unpack(fmt, elf.section_data(relocation)):
            place, info = record[:2]
            relative = place if expected_type == 1 else place - target["address"]
            width = 0 if info & 255 == 0 else 4
            if info >> 8 >= symbols["size"] // 16 or relative < 0 or relative + width > target["size"]:
                raise ValueError("Fixture relocation place or symbol exceeds bounds")
    address = section["address"] + function["section_offset"]
    if expected_type == 2:
        if address % 4 or address + function["size"] > 2**32 or elf.entry != address:
            raise ValueError("Linked entry differs from fixture function address")
        if elf.virtual_bytes(address, function["size"]) != function["bytes"]:
            raise ValueError("Linked section mapping differs from fixture bytes")
        for other in elf.sections:
            if (other["index"] != section["index"] and other["flags"] & 2 and other["size"]
                    and other["address"] < address + function["size"]
                    and address < other["address"] + other["size"]):
                raise ValueError("Linked fixture overlaps another allocated section")
        mappings = []
        for kind, offset, virtual, physical, filesz, memsz, flags, align in elf.program_headers:
            if kind != 1:
                continue
            if virtual + memsz > 2**32:
                raise ValueError("Linked load segment overflows address space")
            overlaps = virtual < address + function["size"] and address < virtual + memsz
            contains = virtual <= address and address + function["size"] <= virtual + filesz
            if overlaps and not contains:
                raise ValueError("Linked fixture has a partial overlapping load mapping")
            if contains:
                mapped = offset + address - virtual
                if (flags & 1 == 0 or mapped != section["offset"] + function["section_offset"]
                        or elf.region(mapped, function["size"]) != function["bytes"]):
                    raise ValueError("Linked load mapping differs from fixture section")
                mappings.append(mapped)
        if len(mappings) != 1:
            raise ValueError("Fixture needs one unambiguous executable PT_LOAD mapping")
    comments = [elf.section_data(s).hex() for s in elf.sections if s["name"] == ".comment"]
    return {"sha256": digest(data), "file_type": elf.file_type, "flags": elf.flags,
            "entry": elf.entry, "comments": comments,
            "function": {"name": symbol, "size": function["size"], "address": address,
                         "section_index": function["section_index"],
                         "section_offset": function["section_offset"],
                         "sha256": digest(function["bytes"]), "bytes_hex": function["bytes"].hex()},
            "sections": elf.sections,
            "program_headers": [list(p) for p in elf.program_headers]}


def compare_linked_fixture(input_bytes, output_bytes, entry_address):
    """Compare complete function bytes while keeping metadata observations separate."""
    if not isinstance(entry_address, int) or not 0 <= entry_address < 2**32 or entry_address % 4:
        raise ValueError("Invalid declared fixture entry address")
    before, after = inspect_fixture(input_bytes, 1), inspect_fixture(output_bytes, 2)
    if after["entry"] != entry_address:
        raise ValueError("Linked fixture differs from frozen text address")
    equal = before["function"]["bytes_hex"] == after["function"]["bytes_hex"]
    return {"status": "PRESERVED" if equal else "CODE_CHANGED",
            "complete_function_bytes_equal": equal,
            "flags_equal": before["flags"] == after["flags"],
            "comments_equal": before["comments"] == after["comments"],
            "input": before, "output": after}


def local_items(config):
    """List every pinned project input for alias and immutability checks."""
    return [config[k] for k in ("family_profiles", "source", "layout", "linker")] + config["support_files"] + config["prelink_evidence"]


def verify_inputs(root, config):
    """Check project pins and the explicitly declared native Windows dependencies."""
    for item in local_items(config):
        path = root / item["relative_path"]
        reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Synthetic-link input escapes project")
        check_identity(file_identity(path), item, "Synthetic-link input")
    for item in config["native_windows_dependencies"]:
        path = Path(item["linux_path"])
        if not path.is_absolute():
            raise ValueError("Native dependency requires absolute path")
        check_identity(file_identity(path), item, "Native Windows dependency")
    families = json.loads((root / config["family_profiles"]["relative_path"]).read_bytes())
    verify_profile_files(root, families)
    if ([p["id"] for p in families["profiles"]] != config["profile_ids"]
            or config["optimization"] != ["-O0"] or config["entry_symbol"] != "family_smoke"
            or config["text_address"] != 0x08804000 or config["no_libraries"] is not True
            or config["runner"] != "wsl_native_windows_interop"):
        raise ValueError("Synthetic experiment differs from declared scope")
    return families


def windows_path(root, config, path):
    """Convert only project-contained paths to the frozen Windows project root."""
    relative = path.resolve().relative_to(root)
    return str(PureWindowsPath(config["windows_project_root"]).joinpath(*relative.parts))


def link_fixture(config, obj, output, map_path, *, root):
    """Run the same bare-link command for each family without hidden libraries."""
    if output.exists() or map_path.exists():
        raise ValueError("Refusing stale synthetic link output")
    linker = root / config["linker"]["relative_path"]
    substitutions = {"linker": str(linker),
                     "layout": windows_path(root, config, root / config["layout"]["relative_path"]),
                     "map": windows_path(root, config, map_path),
                     "output": windows_path(root, config, output),
                     "object": windows_path(root, config, obj)}
    command = [arg.format(**substitutions) for arg in config["command_template"]]
    result = subprocess.run(command, cwd=output.parent, stdin=subprocess.DEVNULL,
                            capture_output=True, text=True, timeout=config["timeout_seconds"])
    return {"returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


def run_experiment(*, root=ROOT, config_path=None, report_path=None):
    """Compile/link all three fresh inputs; retain failures and reject changing pins."""
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/synthetic-link.json"
    raw = config_path.read_bytes()
    config = json.loads(raw)
    if config["status"] != "frozen_before_link_outputs" or config["no_link_outputs_observed"] is not True:
        raise ValueError("Synthetic profile was not frozen before link outputs")
    protected = {config_path.resolve()} | {(root / i["relative_path"]).resolve() for i in local_items(config)}
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        if report_path.resolve() in protected:
            raise ValueError("Synthetic report aliases input")
    families = verify_inputs(root, config)
    # Ancillary compiler pins are protected too, even when not used by linking.
    try:
        from .bench_compiler_families import profile_items
    except ImportError:
        from bench_compiler_families import profile_items
    if report_path is not None and report_path.resolve() in {(root / i["relative_path"]).resolve() for i in profile_items(families)}:
        raise ValueError("Synthetic report aliases compiler input")
    build = root / "build"
    reject_link(build)
    if not build.resolve().is_relative_to(root):
        raise ValueError("Synthetic build escapes project")
    build.mkdir(exist_ok=True)
    directory = Path(tempfile.mkdtemp(prefix="synthetic-link-", dir=build))
    report = {"schema_version": 1, "status": "SYNTHETIC_LINK_INVESTIGATION_COMPLETE",
              "profile_sha256": digest(raw), "source_sha256": config["source"]["sha256"],
              "layout_sha256": config["layout"]["sha256"], "matched_progress": 0, "families": []}
    for profile in families["profiles"]:
        obj = directory / (profile["id"] + ".o")
        output, map_path = obj.with_suffix(".elf"), obj.with_suffix(".map")
        row = {"id": profile["id"], "status": "COMPILE_FAILED", "optimization": ["-O0"]}
        try:
            execution = compile_profile(dict(profile, timeout_tool=families["linux_utilities"][0]["linux_path"]),
                                        root / config["source"]["relative_path"], obj, ["-O0"], root=root)
            diagnostic = execution["stdout"] + execution["stderr"]
            obj.with_suffix(".compile.log").write_text(diagnostic, encoding="utf-8")
            row["compile_returncode"] = execution["returncode"]
            if (execution["returncode"] or not obj.is_file()
                    or re.search(r"\b(warning|error|fatal|illegal|unknown)\b", diagnostic, re.I)):
                row["reason"] = "Compiler failure, warning or missing object"
                report["families"].append(row)
                continue
            reject_link(obj)
            input_bytes = obj.read_bytes()
            row["input"] = inspect_fixture(input_bytes, 1)
            row["status"] = "LINK_FAILED"
            execution = link_fixture(config, obj, output, map_path, root=root)
            diagnostic = execution["stdout"] + execution["stderr"]
            obj.with_suffix(".link.log").write_text(diagnostic, encoding="utf-8")
            row["link_returncode"] = execution["returncode"]
            if obj.read_bytes() != input_bytes:
                raise ValueError("Linker changed input object")
            if output.is_file():
                reject_link(output)
                row["output_sha256"] = digest(output.read_bytes())
            if (execution["returncode"] or not output.is_file() or not map_path.is_file()
                    or re.search(r"\b(warning|error|fatal)\b", diagnostic, re.I)):
                row["reason"] = "Linker failure, warning or missing output/map"
            else:
                reject_link(map_path)
                row.update(compare_linked_fixture(input_bytes, output.read_bytes(), config["text_address"]))
                # Maps/logs contain fresh absolute paths. Retain them as evidence,
                # but exclude their hashes/paths from the repeatable scientific row.
        except (OSError, subprocess.SubprocessError) as error:
            row["reason"] = "Execution unavailable: " + type(error).__name__
        except ValueError as error:
            row.update(status="VALIDATION_FINDING", reason=str(error))
        report["families"].append(row)
    verify_inputs(root, config)
    if config_path.read_bytes() != raw:
        raise ValueError("Synthetic profile changed during experiment")
    report["preserved_functions"] = sum(r["status"] == "PRESERVED" for r in report["families"])
    report["declared_families"] = len(config["profile_ids"])
    if report_path is not None:
        write_report(report_path, report)
    return report, directory


def main():
    """Provide one command on Windows while keeping compiler execution native WSL."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", default="evidence/bucket-03e/synthetic-link.json")
    args = parser.parse_args()
    if os.name == "nt":
        command = ["wsl", "-d", "Ubuntu", "--", "python3", "scripts/bench_synthetic_link.py", "--report", args.report]
        return subprocess.run(command, cwd=ROOT).returncode
    try:
        report, directory = run_experiment(report_path=ROOT / args.report)
        print(json.dumps({"status": report["status"], "preserved_functions": report["preserved_functions"],
                          "build_directory": str(directory), "report": args.report}))
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
