#!/usr/bin/env python3
"""Inspect one complete object function; optionally compare a private reference.

No compiler, game or emulator is launched. Original target bytes are neither
included nor printed. An exact isolated comparison never earns game-match credit.
"""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.elf32 import Elf32

REFERENCE_IDENTITY = {
    "size": 2247320,
    "sha256": "755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950",
}
CASES = {
    "initializer": {"address": 0x0886233C, "size": 68,
                    "sha256": "7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57"},
    "key-advance": {"address": 0x08862700, "size": 140,
                    "sha256": "0ff874a4e619b6a6202257c13125a9ed1ed5dab4c45cbc0242eb9ad5f0a3261f"},
}
MAX_INPUT_SIZE = 16 * 1024 * 1024


def identity(raw):
    return {"size": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def _complete_function(raw):
    """Choose by declarations alone; never search bytes for a favorable range."""
    elf = Elf32(raw)
    if elf.file_type != 1:
        raise ValueError("Expected an ELF32 little-endian MIPS relocatable object")
    symbols, tables = [], {}
    for table in elf.sections:
        if table["type"] == 11:
            raise ValueError("Dynamic symbol tables are outside this object's supported model")
        if table["type"] != 2:
            continue
        if (table["entry_size"] != 16 or table["size"] % 16
                or not 0 < table["link"] < len(elf.sections)
                or elf.sections[table["link"]]["type"] != 3):
            raise ValueError("Malformed symbol table or string-table link")
        strings = elf.section_data(elf.sections[table["link"]])
        rows = []
        for name, value, size, info, other, section in struct.iter_unpack("<IIIBBH", elf.section_data(table)):
            row = dict(name=elf.string(strings, name), value=value, size=size,
                       binding=info >> 4, kind=info & 15, other=other, section=section)
            rows.append(row)
            symbols.append(row)
        tables[table["index"]] = rows
    defined = [s for s in symbols if s["kind"] == 2 and s["section"] != 0]
    if len(defined) != 1:
        raise ValueError("Exactly one defined STT_FUNC is required, including zero-sized declarations")
    function = defined[0]
    if (not function["name"] or sum(s["name"] == function["name"] for s in symbols) != 1
            or function["binding"] != 1 or function["other"] & 3
            or function["size"] <= 0 or function["size"] % 4 or function["value"] % 4
            or not 0 < function["section"] < len(elf.sections)):
        raise ValueError("Function must be unique, strong global, default visibility and positive word-aligned size")
    section = elf.sections[function["section"]]
    start, size = function["value"], function["size"]
    if section["type"] != 1 or section["flags"] & 6 != 6 or start + size > section["size"]:
        raise ValueError("Function must fit wholly in allocated executable PROGBITS")
    non_code_relocations = 0
    for reloc in elf.sections:
        if reloc["type"] not in (4, 9):
            continue
        rela = reloc["type"] == 4
        width = 12 if rela else 8
        if (reloc["entry_size"] != width or reloc["size"] % width or reloc["link"] not in tables
                or not 0 < reloc["info"] < len(elf.sections)):
            raise ValueError("Malformed REL/RELA declaration")
        target = elf.sections[reloc["info"]]
        for values in struct.iter_unpack("<IIi" if rela else "<II", elf.section_data(reloc)):
            offset, info = values[:2]
            kind, symbol = info & 255, info >> 8
            if symbol >= len(tables[reloc["link"]]):
                raise ValueError("Relocation symbol index exceeds its table")
            if (offset > target["size"] or kind and offset == target["size"]
                    or kind == 1 and offset + 2 > target["size"]
                    or 2 <= kind <= 12 and offset + 4 > target["size"]):
                raise ValueError("Relocation place exceeds its target section")
            if kind and target["flags"] & 4:
                raise ValueError("Nonzero code relocations are unsupported; no masking or relocation application")
            if not target["flags"] & 4:
                non_code_relocations += 1
    code = elf.section_data(section)[start:start + size]
    return code, dict(object=identity(raw), elf_flags=elf.flags,
        function=dict(symbol=function["name"], section_index=section["index"], section_offset=start,
                      raw_symbol_other=function["other"], **identity(code)),
        non_code_relocations_retained_unapplied=non_code_relocations)


def compare_complete(compiled, target):
    """Compare every byte and length, retaining differences without normalization."""
    first = next((i for i, (a, b) in enumerate(zip(compiled, target)) if a != b), None)
    if first is None and len(compiled) != len(target):
        first = min(len(compiled), len(target))
    return dict(compiled=identity(compiled), target=identity(target), first_difference=first,
                exact_diagnostic_body=compiled == target)


def compare_function(object_bytes, case, reference_bytes=None):
    if case not in CASES:
        raise ValueError("Unknown reviewed case")
    code, inspected = _complete_function(object_bytes)
    report = dict(case=case, status="OBJECT_INSPECTED_REFERENCE_NOT_SUPPLIED", inspection=inspected,
                  comparison=None, source_participation_proved=False, game_match_credit=False,
                  relocations_applied_or_masked=False, compiler_or_game_executed=False)
    if reference_bytes is not None:
        if identity(reference_bytes) != REFERENCE_IDENTITY:
            raise ValueError("Reference must be the exact pinned decrypted PSP v1.02 EBOOT.ELF")
        reference = Elf32(reference_bytes)
        if reference.file_type != 2:
            raise ValueError("Pinned reference must be an executable ELF")
        target = CASES[case]
        original = reference.virtual_bytes(target["address"], target["size"])
        if identity(original) != {key: target[key] for key in ("size", "sha256")}:
            raise ValueError("Complete target interval identity differs from the reviewed case")
        report.update(status="COMPLETE_DIAGNOSTIC_COMPARISON", comparison=compare_complete(code, original))
    return report


def read_input(path):
    path = Path(path)
    if path.is_symlink():
        raise ValueError("Input must be a regular file rather than a symbolic link")
    before = path.stat()
    if not stat.S_ISREG(before.st_mode) or not 0 < before.st_size <= MAX_INPUT_SIZE:
        raise ValueError("Input must be a nonempty regular file no larger than 16 MiB")
    raw = path.read_bytes()
    after = path.stat()
    fields = ("st_dev", "st_ino", "st_size", "st_mtime_ns", "st_ctime_ns")
    if any(getattr(before, key) != getattr(after, key) for key in fields) or len(raw) != after.st_size:
        raise ValueError("Input changed while being read")
    return raw


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--object", type=Path, required=True, help="Your standalone compiled object")
    parser.add_argument("--case", choices=tuple(CASES), required=True)
    parser.add_argument("--reference", type=Path, help="Your own exact decrypted PSP v1.02 EBOOT.ELF")
    args = parser.parse_args(argv)
    try:
        raw = read_input(args.object)
        reference = read_input(args.reference) if args.reference else None
        report = compare_function(raw, args.case, reference)
    except (OSError, ValueError, UnicodeError) as error:
        print("Inspection rejected: " + str(error), file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
