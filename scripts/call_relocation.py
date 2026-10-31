"""Resolve one declared external MIPS26 call form in selected function bytes.

This is a narrow diagnostic for the invented fixture, not an object linker.
Only ELF32 little-endian MIPS REL/JAL calls to undefined global symbols are
supported. Non-executable R_MIPS_32 metadata is reported without applying it.
All other relocation forms fail. No original game reference is modified.
"""

import struct

try:
    from .elf32 import Elf32
except ImportError:
    from elf32 import Elf32


def require_address(value, label):
    """Require a concrete aligned address in the supported 32-bit model."""
    if type(value) is not int or not 0 <= value <= 0xFFFFFFFF or value % 4:
        raise ValueError(label + " must be an aligned 32-bit address")


def implicit_addend(word):
    """Decode the signed 28-bit addend for this external R_MIPS_26 form."""
    value = (word & 0x03FFFFFF) << 2
    return value - 0x10000000 if value & 0x08000000 else value


def apply_mips26(word, place, symbol_address):
    """Resolve one JAL word, preserving opcode and checking its P+4 region.

    The supported external-symbol form uses S + sign_extend(imm26 << 2).
    Local/section-symbol relocation has different ABI rules and is unsupported.
    Address-space wrap at P+4 is excluded by this diagnostic's memory model.
    """
    if type(word) is not int or not 0 <= word <= 0xFFFFFFFF or word >> 26 != 3:
        raise ValueError("MIPS26 call must point at a JAL instruction")
    require_address(place, "Relocation place")
    require_address(symbol_address, "Symbol")
    if place > 0xFFFFFFF8:
        raise ValueError("JAL delay slot wraps the supported address space")
    target = symbol_address + implicit_addend(word)
    if not 0 <= target <= 0xFFFFFFFF:
        raise ValueError("Resolved call target overflows the address space")
    if target & 0xF0000000 != (place + 4) & 0xF0000000:
        raise ValueError("Resolved call target is outside the JAL P+4 region")
    return (word & 0xFC000000) | ((target >> 2) & 0x03FFFFFF)


def read_symbol_tables(elf):
    """Read indexed symbol records without losing duplicate names."""
    tables = {}
    for section in elf.sections:
        if section["type"] != 2:
            continue
        if (section["entry_size"] != 16 or section["size"] % 16
                or not 0 < section["link"] < len(elf.sections)):
            raise ValueError("Invalid symbol-table bounds")
        strings = elf.sections[section["link"]]
        if strings["type"] != 3:
            raise ValueError("Symbol table does not link to a string table")
        names = elf.section_data(strings)
        records = []
        for index, values in enumerate(struct.iter_unpack("<IIIBBH", elf.section_data(section))):
            name, value, size, info, other, shndx = values
            records.append({"index": index, "name": elf.string(names, name),
                            "value": value, "size": size, "binding": info >> 4,
                            "type": info & 15, "other": other, "section_index": shndx})
        tables[section["index"]] = records
    return tables


def relocate_function(object_bytes, *, function_name, load_address, symbols, expected_calls):
    """Return selected function bytes with exactly the declared calls resolved.

    Relocation offsets are section-relative, whereas the plan is relative to
    the function. The returned bytes exclude all headers, padding and metadata.
    This operation makes no claim about a linked object or original game code.
    """
    require_address(load_address, "Function load address")
    elf = Elf32(object_bytes)
    if elf.file_type != 1:
        raise ValueError("Expected a relocatable MIPS ELF object")
    tables = read_symbol_tables(elf)
    all_symbols = [symbol for table in tables.values() for symbol in table]
    named = [symbol for symbol in all_symbols if symbol["name"] == function_name]
    if len(named) != 1:
        raise ValueError("Selected function symbol is missing or ambiguous")
    fn = named[0]
    if (fn["type"] != 2 or fn["binding"] != 1 or fn["other"] != 0
            or not 0 < fn["section_index"] < len(elf.sections)):
        raise ValueError("Selected symbol is not a defined global function")
    code = elf.sections[fn["section_index"]]
    start, size = fn["value"], fn["size"]
    if (code["type"] != 1 or code["flags"] & 6 != 6 or size < 8 or size % 4
            or start % 4 or start + size > code["size"]
            or load_address + size > 0x100000000):
        raise ValueError("Selected function exceeds its executable/address bounds")
    plans = {}
    for call in expected_calls:
        offset, name, addend = call["offset"], call["symbol"], call["addend"]
        if (type(offset) is not int or offset % 4 or not 0 <= offset <= size - 8
                or offset in plans or not isinstance(name, str) or not name
                or type(addend) is not int or addend % 4
                or not -0x08000000 <= addend < 0x08000000):
            raise ValueError("Invalid or duplicate expected call")
        plans[offset] = call
    if not plans or set(symbols) != {call["symbol"] for call in plans.values()}:
        raise ValueError("Expected calls and explicit symbol addresses disagree")
    for name, address in symbols.items():
        require_address(address, "External symbol " + name)
        matches = [symbol for symbol in all_symbols if symbol["name"] == name]
        if len(matches) != 1:
            raise ValueError("External symbol is missing or ambiguous")
        symbol = matches[0]
        if (symbol["binding"] != 1 or symbol["type"] not in (0, 2)
                or symbol["section_index"] != 0 or symbol["value"] != 0
                or symbol["size"] != 0 or symbol["other"] != 0):
            raise ValueError("Unsupported external symbol form")
    output = bytearray(elf.section_data(code)[start:start + size])
    applied, non_code, seen_calls, seen_relocations = [], [], set(), set()
    for relocation in elf.sections:
        if relocation["type"] not in (4, 9):
            continue
        if relocation["type"] != 9:
            raise ValueError("RELA relocations are outside this diagnostic")
        if (relocation["entry_size"] != 8 or relocation["size"] % 8
                or relocation["link"] not in tables
                or not 0 < relocation["info"] < len(elf.sections)):
            raise ValueError("Invalid REL section metadata")
        target = elf.sections[relocation["info"]]
        table = tables[relocation["link"]]
        seen_places = set()
        for offset, info in struct.iter_unpack("<II", elf.section_data(relocation)):
            symbol_index, kind = info >> 8, info & 255
            key = (target["index"], offset)
            if (offset % 4 or offset + 4 > target["size"] or key in seen_relocations
                    or offset in seen_places
                    or symbol_index >= len(table)):
                raise ValueError("Invalid or duplicate relocation place/symbol")
            seen_places.add(offset)
            seen_relocations.add(key)
            symbol = table[symbol_index]
            if not target["flags"] & 4:
                opaque_mwcats = target["type"] == 0xCA2A82C2 and target["name"] == ".mwcats"
                if (target["type"] != 1 and not opaque_mwcats) or kind != 2:
                    raise ValueError("Unsupported non-code metadata relocation")
                non_code.append({"section_index": target["index"], "offset": offset,
                                 "type": kind, "symbol": symbol["name"],
                                 "status": "not applied; outside function-byte scope"})
                continue
            local_offset = offset - start
            if (target["index"] != code["index"] or kind != 4
                    or local_offset not in plans or local_offset in seen_calls):
                raise ValueError("Unsupported, undeclared or duplicate code relocation")
            call = plans[local_offset]
            if symbol["name"] != call["symbol"]:
                raise ValueError("Code relocation symbol disagrees with declared call")
            word = struct.unpack_from("<I", output, local_offset)[0]
            if implicit_addend(word) != call["addend"]:
                raise ValueError("Code relocation addend disagrees with declared call")
            place = load_address + local_offset
            resolved = apply_mips26(word, place, symbols[symbol["name"]])
            struct.pack_into("<I", output, local_offset, resolved)
            applied.append({"offset": local_offset, "section_offset": offset,
                            "symbol": symbol["name"], "symbol_address": symbols[symbol["name"]],
                            "addend": call["addend"], "place": place,
                            "type": kind, "original_word": word, "resolved_word": resolved})
            seen_calls.add(local_offset)
    if seen_calls != set(plans):
        raise ValueError("Declared call has no matching relocation")
    return {"bytes": bytes(output), "relocations": applied, "non_code_relocations": non_code}
