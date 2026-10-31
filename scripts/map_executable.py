#!/usr/bin/env python3
"""Inventory the pinned PSP ELF and its overlay descriptors without executing it.

The map describes stored metadata. It does not extract overlay payloads, prove
function boundaries, classify library code, or select a compiler configuration.
Numeric addresses and offsets remain integers in JSON; section/program indices
are preserved even when names or addresses repeat.
"""

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

try:
    from .elf32 import Elf32
except ImportError:
    from elf32 import Elf32


ROOT = Path(__file__).resolve().parents[1]
ELF32_LIMIT = 1 << 32
PT_NULL = 0
PT_LOAD = 1
SHT_NOBITS = 8
SHF_ALLOC = 2
MAX_CANDIDATE_RELATIONSHIPS = 1_000_000


def checked_end(start, size, description):
    """Reject a range that cannot fit in the ELF32 virtual-address space."""
    end = start + size
    if end > ELF32_LIMIT:
        raise ValueError(description + " exceeds the ELF32 address space")
    return end


def describe_program(index, values):
    """Retain every original program-header field, including unusual values."""
    result = dict(zip(
        ("type", "offset", "virtual_address", "physical_address", "file_size",
         "memory_size", "flags", "alignment"), values
    ))
    result["index"] = index
    result["type_name"] = {PT_NULL: "PT_NULL", PT_LOAD: "PT_LOAD"}.get(
        result["type"], "other"
    )
    result["virtual_end"] = checked_end(
        result["virtual_address"], result["memory_size"], "Program-header range"
    )
    return result


def build_map(elf_bytes):
    """Build a deterministic metadata map from one bounded ELF32 MIPS image."""
    elf = Elf32(elf_bytes)
    if elf.file_type != 2:
        raise ValueError("Expected an executable ELF (ET_EXEC)")

    sections = []
    for original in elf.sections:
        section = dict(original)
        section["file_backed"] = section["type"] != SHT_NOBITS
        if section["flags"] & SHF_ALLOC:
            section["virtual_end"] = checked_end(
                section["address"], section["size"], "Allocated section range"
            )
        sections.append(section)

    programs = [describe_program(index, values)
                for index, values in enumerate(elf.program_headers)]
    loads = []
    for program in programs:
        if program["type"] != PT_LOAD:
            continue
        start = program["virtual_address"]
        file_end = start + program["file_size"]
        memory_end = program["virtual_end"]
        loads.append({
            "program_index": program["index"],
            "file_range": {"offset": program["offset"],
                           "end": program["offset"] + program["file_size"],
                           "size": program["file_size"]},
            "virtual_file_range": {"start": start, "end": file_end},
            "virtual_memory_range": {"start": start, "end": memory_end},
            "zero_fill_range": {"start": file_end, "end": memory_end,
                                "size": memory_end - file_end},
            "note": "Program metadata only; non-file memory is not all proven BSS.",
        })

    # Index structural candidates once. A malformed file with many identical
    # descriptors must not trigger an unbounded Cartesian-product report.
    candidate_index = {}
    for program in programs:
        if program["type"] != PT_LOAD:
            key = (program["virtual_address"], program["offset"], program["file_size"])
            candidate_index.setdefault(key, []).append(program["index"])

    descriptors = []
    relationships = 0
    for section in sections:
        # Relocation sections also end in .ovl, but are not overlay descriptors.
        if (section["type"] != 1 or not section["flags"] & SHF_ALLOC
                or not section["name"].endswith(".ovl")
                or section["name"].startswith(".rel")):
            continue
        key = (section["address"], section["offset"], section["size"])
        candidates = candidate_index.get(key, [])
        count = len(candidates)
        relationships += count
        if relationships > MAX_CANDIDATE_RELATIONSHIPS:
            raise ValueError("Overlay candidate relationships exceed the map size limit")
        status = ("unique_candidate" if count == 1 else
                  "ambiguous_candidates" if count > 1 else "no_candidate")
        descriptors.append({
            "section_index": section["index"], "name": section["name"],
            "address": section["address"], "size": section["size"],
            "file_offset": section["offset"],
            "matching_program_indices": candidates,
            "pairing_status": status,
            "payload_extracted": False,
        })

    slots = []
    for address in sorted({descriptor["address"] for descriptor in descriptors}):
        group = [descriptor for descriptor in descriptors
                 if descriptor["address"] == address]
        indices = sorted({index for descriptor in group
                          for index in descriptor["matching_program_indices"]})
        reservations = [programs[index]["memory_size"] for index in indices]
        slots.append({
            "address": address, "descriptor_count": len(group),
            "descriptor_section_indices": [d["section_index"] for d in group],
            "names": [d["name"] for d in group],
            "matching_program_indices": indices,
            "max_reserved_size": max(reservations, default=0),
            "note": "Shared-start group, not proof of simultaneous loading or lifetime.",
        })

    compiler_strings = []
    for section in elf.sections:
        if section["name"] == ".comment" and section["type"] != SHT_NOBITS:
            compiler_strings.extend(
                value.decode("utf-8", errors="backslashreplace")
                for value in elf.section_data(section).split(b"\0") if value
            )

    roles = {
        "main_code": ".text", "import_stubs": ".sceStub.text",
        "initialized_data": ".data", "declared_bss": ".bss",
        "module_information": ".rodata.sceModuleInfo",
    }
    named_regions = {
        role: [s["index"] for s in sections if s["name"] == name]
        for role, name in roles.items()
    }

    return {
        "schema_version": 1,
        "scope": "Executable metadata inventory only; not a rebuild or runtime test.",
        "source": {"size": len(elf_bytes),
                   "sha256": hashlib.sha256(elf_bytes).hexdigest()},
        "header": {"file_type": elf.file_type, "machine": 8, "class": "ELF32",
                   "byte_order": "little", "entry": elf.entry, "flags": elf.flags},
        "counts": {"sections": len(sections), "program_headers": len(programs),
                   "load_segments": len(loads), "overlay_descriptors": len(descriptors),
                   "overlay_start_groups": len(slots),
                   "zero_sized_overlay_descriptors": sum(d["size"] == 0 for d in descriptors),
                   "descriptors_with_embedded_bytes": sum(d["size"] > 0 for d in descriptors),
                   "extracted_overlay_payloads": 0},
        "named_region_section_indices": named_regions,
        "sections": sections, "program_headers": programs, "load_segments": loads,
        "overlay_descriptors": descriptors, "overlay_start_groups": slots,
        "observations": {"compiler_comment_strings": compiler_strings},
        "unknowns": [
            "Overlay archive extents, compression and payload bytes are not recovered by this map.",
            "Program candidates are structural metadata matches; ordering alone does not pair a name to a reservation size.",
            "PT_NULL entries are preserved as metadata, not treated as PT_LOAD segments.",
            "Non-file memory in a load segment does not prove BSS boundaries or overlay state lifetime.",
            "The compiler comment does not prove an exact compiler build, flags or source language.",
            "Function boundaries and game/SDK/third-party classifications remain unestablished.",
        ],
    }


def write_report(path, encoded):
    """Create evidence once, or accept an identical rerun without rewriting it."""
    if path.is_symlink():
        raise ValueError("Refusing a symbolic-link report path")
    if path.exists():
        if path.read_bytes() != encoded:
            raise ValueError("Existing report differs; use a fresh output path: " + str(path))
        return "unchanged"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        output.write(encoded)
    return "written"


def main(argv=None):
    """Verify the selected reference before publishing a local JSON map."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--elf", type=Path)
    parser.add_argument("--lock", type=Path, default=ROOT / "config/reference.json")
    parser.add_argument("--out", type=Path, default=ROOT / "evidence/bucket-01/executable-map-v1.json")
    args = parser.parse_args(argv)
    try:
        lock = json.loads(args.lock.read_text(encoding="utf-8"))
        if lock.get("status") != "active" or lock.get("baseline_selected_by_user") is not True:
            raise ValueError("No active user-selected reference")
        expected = lock["decrypted_executable"]
        path = args.elf or ROOT / expected["relative_path"]
        if path.stat().st_size != expected["size"]:
            raise ValueError("Decrypted ELF size differs from the reference lock")
        data = path.read_bytes()
        if len(data) != expected["size"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError("Decrypted ELF hash differs from the reference lock")
        report = build_map(data)
        encoded = (json.dumps(report, indent=2, ensure_ascii=True) + "\n").encode("utf-8")
        result = write_report(args.out, encoded)
        print("EXECUTABLE MAP " + result.upper() + ": " + str(args.out.resolve()))
        print(str(report["counts"]["overlay_descriptors"]) + " overlay descriptors; "
              + str(report["counts"]["extracted_overlay_payloads"]) + " payloads extracted")
        return 0
    except (OSError, ValueError, KeyError, TypeError, struct.error) as error:
        print("MAP FAILED: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
