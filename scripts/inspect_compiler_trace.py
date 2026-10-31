#!/usr/bin/env python3
"""Map PE diagnostic labels to bounded static, decoded reference candidates.

This reads an existing compiler and GNU objdump text; it never executes the
compiler. Relocations, instruction bytes and supported immediate operands must
agree. Static candidates are not live hooks, reachable stages or decoded IR.
"""

import argparse
import bisect
import hashlib
import json
from pathlib import Path
import re
import struct


class Pe32:
    """Read only the PE32/i386 file-backed mappings and HIGHLOW relocations used here."""

    def __init__(self, data):
        self.data = data
        if len(data) < 64 or data[:2] != b"MZ":
            raise ValueError("Missing bounded DOS header")
        pe = struct.unpack_from("<I", data, 60)[0]
        if pe < 64 or pe + 24 > len(data) or data[pe:pe + 4] != b"PE\0\0":
            raise ValueError("Invalid PE header")
        machine, count = struct.unpack_from("<HH", data, pe + 4)
        optional_size = struct.unpack_from("<H", data, pe + 20)[0]
        opt = pe + 24
        if (machine != 0x14C or not 1 <= count <= 96 or optional_size < 96
                or opt + optional_size + count * 40 > len(data)
                or struct.unpack_from("<H", data, opt)[0] != 0x10B):
            raise ValueError("Unsupported or truncated PE32/i386 layout")
        self.base = struct.unpack_from("<I", data, opt + 28)[0]
        self.image_size, header_size = struct.unpack_from("<II", data, opt + 56)
        self.entry_rva = struct.unpack_from("<I", data, opt + 16)[0]
        directories = struct.unpack_from("<I", data, opt + 92)[0]
        if (not self.image_size or self.base + self.image_size > 0x100000000
                or header_size > len(data) or header_size < opt + optional_size + count * 40
                or directories > 16 or 96 + directories * 8 > optional_size):
            raise ValueError("Invalid PE image/header/directory bounds")
        self.sections = []
        for i in range(count):
            off = opt + optional_size + i * 40
            name = data[off:off + 8].split(b"\0", 1)[0].decode("ascii", errors="strict")
            virtual_size, rva, size, raw = struct.unpack_from("<IIII", data, off + 8)
            flags = struct.unpack_from("<I", data, off + 36)[0]
            extent = max(virtual_size, size)
            if (rva < header_size or rva + extent > self.image_size or raw + size > len(data)
                    or (size and raw < header_size)):
                raise ValueError("Invalid PE section bounds")
            self.sections.append({"name": name, "rva": rva, "virtual_size": virtual_size,
                "raw": raw, "size": size, "extent": extent, "flags": flags})
        for index, section in enumerate(self.sections):
            for other in self.sections[index + 1:]:
                if (section["rva"] < other["rva"] + other["extent"]
                        and other["rva"] < section["rva"] + section["extent"]):
                    raise ValueError("Ambiguous overlapping PE virtual sections")
                if (section["size"] and other["size"] and section["raw"] < other["raw"] + other["size"]
                        and other["raw"] < section["raw"] + section["size"]):
                    raise ValueError("Ambiguous overlapping PE raw sections")
        self.reloc_rva, self.reloc_size = struct.unpack_from("<II", data, opt + 96 + 5 * 8) if directories > 5 else (0, 0)
        if bool(self.reloc_rva) != bool(self.reloc_size):
            raise ValueError("Incomplete relocation directory")

    def file_mapping(self, offset, size):
        if size <= 0 or offset < 0 or offset + size > len(self.data):
            raise ValueError("Invalid file span")
        matches = [s for s in self.sections if s["raw"] <= offset and offset + size <= s["raw"] + s["size"]]
        if len(matches) != 1:
            raise ValueError("File span needs one file-backed section")
        section = matches[0]
        return section["rva"] + offset - section["raw"], section

    def rva_mapping(self, rva, size):
        if size <= 0 or rva < 0 or rva + size > self.image_size:
            raise ValueError("Invalid RVA span")
        matches = [s for s in self.sections if s["rva"] <= rva and rva + size <= s["rva"] + s["size"]]
        if len(matches) != 1:
            raise ValueError("RVA span needs one file-backed section, not a virtual tail")
        section = matches[0]
        return section["raw"] + rva - section["rva"], section

    def highlow_relocations(self):
        if not self.reloc_size:
            return set()
        raw, unused = self.rva_mapping(self.reloc_rva, self.reloc_size)
        records, cursor = set(), 0
        while cursor < self.reloc_size:
            if cursor + 8 > self.reloc_size:
                raise ValueError("Truncated relocation block")
            page, size = struct.unpack_from("<II", self.data, raw + cursor)
            if page % 4096 or size < 8 or size % 2 or cursor + size > self.reloc_size:
                raise ValueError("Invalid relocation block")
            for off in range(cursor + 8, cursor + size, 2):
                entry = struct.unpack_from("<H", self.data, raw + off)[0]
                kind, displacement = entry >> 12, entry & 0xFFF
                if kind == 0:
                    continue
                if kind != 3:
                    raise ValueError("Unsupported PE relocation type")
                place = page + displacement
                self.rva_mapping(place, 4)
                if place in records:
                    raise ValueError("Duplicate HIGHLOW relocation")
                records.add(place)
            cursor += size
        return records


def decode_listing(image, text):
    """Check objdump's linear instruction boundaries/bytes against executable PE bytes."""
    instructions = []
    pattern = re.compile(r"^\s*([0-9a-fA-F]+):\s+((?:[0-9a-fA-F]{2}[ \t]+)+)(\S.*)?$")
    for line in text.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        va, raw = int(match[1], 16), bytes.fromhex(match[2])
        if not 1 <= len(raw) <= 15 or not match[3]:
            raise ValueError("Invalid or incomplete decoded instruction")
        offset, section = image.rva_mapping(va - image.base, len(raw))
        if section["flags"] & 0x20000000 == 0 or image.data[offset:offset + len(raw)] != raw:
            raise ValueError("Decoded instruction differs from executable PE bytes")
        if instructions and va < instructions[-1]["va"] + len(instructions[-1]["raw"]):
            raise ValueError("Overlapping or unordered decoded instructions")
        instructions.append({"va": va, "raw": raw, "assembly": match[3].strip()})
    return instructions


def label_operand(instruction, operand_va, target_va):
    """Accept only characterized whole immediate-address forms without prefixes."""
    raw = instruction["raw"]
    relative = operand_va - instruction["va"]
    immediate = struct.pack("<I", target_va)
    if len(raw) == 5 and relative == 1 and raw[1:] == immediate:
        if raw[0] == 0x68:
            return "PUSH_IMM32"
        if 0xB8 <= raw[0] <= 0xBF:
            return "MOV_REG_IMM32"
    if 6 <= len(raw) <= 11 and raw[0] == 0xC7 and raw[1] & 0x38 == 0:
        mod, rm = raw[1] >> 6, raw[1] & 7
        prefix = 2
        displacement = 0
        if mod != 3 and rm == 4:
            prefix += 1  # SIB addressing adds one byte before displacement.
            if mod == 0 and raw[2] & 7 == 5:
                displacement = 4
        if mod == 0 and rm == 5:
            displacement = 4
        elif mod == 1:
            displacement = 1
        elif mod == 2:
            displacement = 4
        expected = prefix + displacement + 4
        if len(raw) == expected and relative == expected - 4 and raw[-4:] == immediate:
            return "MOV_RM_IMM32"
    if len(raw) == 6 and raw[0] == 0x8D and raw[1] & 0xC7 == 5 and relative == 2 and raw[2:] == immediate:
        return "LEA_ABSOLUTE_DISP32"
    return None


def analyze(data, markers, listing):
    """Keep decoded/relocated label operands, data pointers and unknowns distinct."""
    image = Pe32(data)
    instructions = decode_listing(image, listing)
    starts = [i["va"] for i in instructions]
    relocations = image.highlow_relocations()
    labels = []
    seen = set()
    for marker in markers:
        offset, text = marker["file_offset"], marker["text"]
        expected = text.encode("ascii") + b"\0"
        if offset in seen or data[offset:offset + len(expected)] != expected:
            raise ValueError("Duplicate, changed or nonterminated diagnostic marker")
        seen.add(offset)
        rva, section = image.file_mapping(offset, len(expected))
        if section["flags"] & 0x20000000:
            raise ValueError("Diagnostic marker unexpectedly occupies executable bytes")
        labels.append({"text": text, "file_offset": offset, "rva": rva,
                       "preferred_va": image.base + rva, "section": section["name"], "references": []})
    by_va = {label["preferred_va"]: label for label in labels}
    for place in sorted(relocations):
        offset, section = image.rva_mapping(place, 4)
        target = struct.unpack_from("<I", data, offset)[0]
        if target not in by_va:
            continue
        row = {"operand_rva": place, "operand_preferred_va": image.base + place, "section": section["name"]}
        if not section["flags"] & 0x20000000:
            row["status"] = "RELOCATED_DATA_POINTER"
        else:
            index = bisect.bisect_right(starts, image.base + place) - 1
            instruction = instructions[index] if index >= 0 else None
            if instruction is None or not instruction["va"] <= image.base + place < instruction["va"] + len(instruction["raw"]):
                row.update(status="UNCLASSIFIED", reason="No decoded instruction covers relocation operand")
            else:
                form = label_operand(instruction, image.base + place, target)
                row.update(status="DECODED_RELOCATED_LABEL_OPERAND" if form else "UNCLASSIFIED",
                    instruction_va=instruction["va"], instruction_bytes_hex=instruction["raw"].hex(),
                    assembly=instruction["assembly"], form=form)
                if not form:
                    row["reason"] = "Instruction/operand form outside characterized whitelist"
                row["context"] = [{"va": i["va"], "bytes_hex": i["raw"].hex(), "assembly": i["assembly"]}
                    for i in instructions[max(0, index - 2):index + 5]]
        by_va[target]["references"].append(row)
    return {"schema_version": 1, "status": "STATIC_TRACE_FEASIBILITY_ONLY",
        "compiler_sha256": hashlib.sha256(data).hexdigest(), "image_base": image.base,
        "entry_rva": image.entry_rva, "entry_preferred_va": image.base + image.entry_rva,
        "sections": image.sections, "highlow_relocation_count": len(relocations),
        "decoded_instruction_count": len(instructions), "markers": labels,
        "candidate_operand_count": sum(r["status"] == "DECODED_RELOCATED_LABEL_OPERAND" for l in labels for r in l["references"]),
        "live_hooks_validated": False, "pass_order_observed": False, "compiler_executed": False,
        "limitations": ["Linear decoding and relocations do not prove code reachability or stage activation.",
            "Preferred VAs are not observed runtime addresses; the loader may relocate the image.",
            "Unclassified operands are not hooks. No PSP IR/register layout or debugger transport is validated."]}


def validate_listing_provenance(provenance, listing, data, compiler_path):
    """Bind a retained decoder artifact to its exact command, tool and PE input.

    This checks the declared provenance; independent re-decoding still audits
    that the artifact came from the real decoder, rather than trusting row text.
    """
    command = provenance["command"]
    tool = Path(provenance["tool"]["linux_path"])
    if (provenance["returncode"] != 0 or provenance["stderr"] != ""
            or provenance["stdout_sha256"] != hashlib.sha256(listing).hexdigest()
            or provenance["compiler_sha256"] != hashlib.sha256(data).hexdigest()
            or len(command) != 5 or command[0] != str(tool) or command[1:4] != ["-d", "-w", "-Mintel"]
            or Path(command[4]).resolve() != compiler_path.resolve() or not tool.is_absolute()):
        raise ValueError("Decoder provenance differs from reviewed command/input/listing")
    raw = tool.read_bytes()
    if len(raw) != provenance["tool"]["size"] or hashlib.sha256(raw).hexdigest() != provenance["tool"]["sha256"]:
        raise ValueError("Decoder differs from pinned tool")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--compiler", required=True, type=Path)
    parser.add_argument("--markers", required=True, type=Path)
    parser.add_argument("--listing", required=True, type=Path)
    parser.add_argument("--decoder-provenance", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    data = args.compiler.read_bytes()
    declared = json.loads(args.markers.read_bytes())
    if len(data) != declared["compiler"]["size"] or hashlib.sha256(data).hexdigest() != declared["compiler"]["sha256"]:
        raise ValueError("Compiler differs from pinned static marker input")
    if args.report.resolve() in {p.resolve() for p in (args.compiler, args.markers, args.listing, args.decoder_provenance)}:
        raise ValueError("Static report aliases input")
    listing = args.listing.read_bytes()
    validate_listing_provenance(json.loads(args.decoder_provenance.read_bytes()), listing, data, args.compiler)
    report = analyze(data, declared["markers"], listing.decode("utf-8"))
    raw = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    if args.report.exists() and args.report.read_bytes() != raw:
        raise ValueError("Refusing conflicting static report")
    args.report.parent.mkdir(exist_ok=True, parents=True)
    args.report.write_bytes(raw)
    print(json.dumps({"markers": len(report["markers"]), "candidate_operands": report["candidate_operand_count"],
                      "live_hooks_validated": False}))


if __name__ == "__main__":
    main()
