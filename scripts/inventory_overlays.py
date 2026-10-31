"""Inventory bounded PSP archive prefixes against the original overlay map.

Only entry prefixes are deobfuscated. Header coverage, reservation compatibility
and complete payload recovery are separate claims; no game code is executed.
The established single-overlay extractor and all earlier locks stay unchanged.
"""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

try:
    from . import extract_overlay as pilot
except ImportError:
    import extract_overlay as pilot

ROOT = Path(__file__).resolve().parents[1]
PREFIX_LIMIT = 64


def parse_header(prefix, stored_length):
    """Validate just the header using the independently declared stored length.

    The two final address words are preserved without entry/constructor labels.
    No fabricated payload padding or code-content validation is performed.
    """
    if len(prefix) != PREFIX_LIMIT or prefix[:4] != b"MWo3":
        raise ValueError("Claimed MWo3 entry lacks a complete 64-byte header")
    fields = dict(zip(("id", "load_address", "code_size", "data_size", "bss_size",
                       "raw_0x18", "raw_0x1c"), struct.unpack_from("<7I", prefix, 4)))
    if not isinstance(stored_length, int) or stored_length < PREFIX_LIMIT:
        raise ValueError("Invalid declared stored length")
    if PREFIX_LIMIT + fields["code_size"] + fields["data_size"] != stored_length:
        raise ValueError("Overlay header and archive stored length disagree")
    if fields["load_address"] % 4 or fields["code_size"] % 4:
        raise ValueError("Overlay load address or code length is not word aligned")
    if fields["load_address"] + stored_length + fields["bss_size"] > 0x100000000:
        raise ValueError("Overlay memory range overflows 32 bits")
    raw_name = prefix[32:64]
    if b"\0" not in raw_name:
        raise ValueError("Overlay name is not terminated")
    try:
        name = raw_name.split(b"\0", 1)[0].decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError("Overlay name is not ASCII") from error
    if not re.fullmatch(r"[A-Za-z0-9_]+\.ovl", name):
        raise ValueError("Overlay name is not a bounded filename")
    fields["name"] = name
    return fields


def overlay_descriptors(elf):
    return [item for item in elf.sections if item["name"].endswith(".ovl")
            and item["type"] == 1 and item["flags"] & 2 and item["size"] == 0]


def associations(header, stored_length, elf):
    """Keep every value-compatible candidate; never infer a slot capacity."""
    descriptors = [item["index"] for item in overlay_descriptors(elf)
                   if item["name"] == header["name"] and item["address"] == header["load_address"]]
    memory_size = stored_length + header["bss_size"]
    reservations = [index for index, ph in enumerate(elf.program_headers)
                    if ph[0] == 0 and ph[4] == 0 and ph[2] == header["load_address"]
                    and ph[5] == memory_size]
    return {"descriptor_candidates": descriptors, "reservation_candidates": reservations,
            "header_id_agrees_with_reservation_index": header["id"] in reservations,
            "reservation_value_ambiguity": len(reservations) > 1,
            "declared_memory_size": memory_size}


def magic_label(data):
    return data[:4].hex() if len(data) >= 4 else "short:" + str(len(data))


def scan_prefixes(stream, archive_offset, archive_size, index, table, elf):
    """Read at most 64 exact entry bytes and decode only complete prefix words.

    Short unaligned tails stay raw; nothing is read beyond an entry's declared
    exact length just to complete a cipher word. Empty extents require no read.
    Both raw and deobfuscated MWo3 claims remain visible if present.
    """
    entries, overlays, invalid = [], [], []
    raw_magics, decoded_magics = Counter(), Counter()
    reads = []
    for number, (block, end) in enumerate(zip(index["blocks"], index["blocks"][1:])):
        extent = (end - block) * pilot.BLOCK
        length = index["exact_sizes"].get(number, extent)
        if not 0 <= length <= extent:
            raise ValueError("Invalid entry length or extent")
        count = min(PREFIX_LIMIT, length)
        raw = pilot.read_extent(stream, archive_offset, archive_size, block * pilot.BLOCK, count) if count else b""
        decoded = pilot.decode(raw[:len(raw) // 4 * 4], block, table)
        raw_magics[magic_label(raw)] += 1
        decoded_magics[magic_label(decoded)] += 1
        reads.append(len(raw))
        row = {"archive_index": number, "block": block, "extent_size": extent,
               "stored_length": length, "prefix_size": len(raw), "decoded_prefix_size": len(decoded),
               "raw_prefix_sha256": pilot.identity(raw)["sha256"],
               "decoded_prefix_sha256": pilot.identity(decoded)["sha256"],
               "raw_magic": magic_label(raw), "decoded_magic": magic_label(decoded),
               "overlay_candidates": []}
        for encoding, prefix in (("raw", raw), ("deobfuscated", decoded)):
            if prefix[:4] != b"MWo3":
                continue
            candidate = {"archive_index": number, "encoding": encoding}
            try:
                header = parse_header(prefix, length)
                candidate.update(header=header, stored_length=length,
                                 header_sha256=pilot.identity(prefix)["sha256"],
                                 header_bytes_hex=prefix.hex(), **associations(header, length, elf))
                row["overlay_candidates"].append(len(overlays))
                overlays.append(candidate)
            except ValueError as error:
                invalid.append(dict(candidate, reason=str(error)))
        entries.append(row)
    descriptors = overlay_descriptors(elf)
    links = {item["index"]: [] for item in descriptors}
    for number, item in enumerate(overlays):
        if len(item["descriptor_candidates"]) == 1:
            links[item["descriptor_candidates"][0]].append(number)
    missing = [key for key, values in links.items() if not values]
    duplicated = [key for key, values in links.items() if len(values) > 1]
    unresolved = [number for number, item in enumerate(overlays)
                  if len(item["descriptor_candidates"]) != 1 or not item["reservation_candidates"]]
    starts = sorted({item["address"] for item in descriptors})
    for item in overlays:
        base = item["header"]["load_address"]
        following = next((start for start in starts if start > base), None)
        item["next_distinct_named_start"] = following
        item["extends_past_next_named_start"] = (
            following is not None and base + item["declared_memory_size"] > following)
    complete = not invalid and not missing and not duplicated and not unresolved and len(overlays) == len(descriptors)
    return {"status": "OVERLAY_PREFIX_INVENTORY_COMPLETE" if complete else "OVERLAY_PREFIX_INVENTORY_INCOMPLETE",
            "entries": entries, "overlays": overlays, "invalid_overlay_candidates": invalid,
            "raw_magic_counts": dict(sorted(raw_magics.items())),
            "decoded_magic_counts": dict(sorted(decoded_magics.items())),
            "prefix_bytes_read": sum(reads), "maximum_entry_prefix_bytes_read": max(reads, default=0),
            "coverage": {"entry_count": len(entries), "named_descriptor_count": len(descriptors),
                "valid_overlay_headers": len(overlays), "known_descriptor_header_coverage_complete": complete,
                "unmatched_descriptor_indexes": missing, "multiply_matched_descriptor_indexes": duplicated,
                "unresolved_overlay_indexes": unresolved,
                "reservation_value_ambiguities": sum(item["reservation_value_ambiguity"] for item in overlays),
                "header_id_reservation_index_agreements": sum(item["header_id_agrees_with_reservation_index"] for item in overlays),
                "distinct_named_starts": len(starts), "complete_game_code_inventory_established": False},
            "full_overlay_payloads_recovered": 0}


def local_items(config):
    return [config["reference_lock"], config["pilot_lock"]]


def inventory_overlays(iso_path, *, root=ROOT, config_path=None, elf_path=None, report_path=None):
    root = Path(root).resolve(strict=True)
    config_path = Path(config_path) if config_path else root / "config/overlay-inventory.json"
    pilot.reject_link(config_path)
    raw_config = config_path.read_bytes()
    config = json.loads(raw_config)
    if (config["status"] != "frozen_before_inventory" or config["maximum_prefix_bytes"] != PREFIX_LIMIT
            or config["full_payload_recovery"] is not False or config["interpret_final_address_words"] is not False):
        raise ValueError("Inventory differs from the reviewed header-only scope")
    inputs = {}
    for item in local_items(config):
        path = root / item["relative_path"]
        pilot.reject_link(path)
        if not path.resolve(strict=True).is_relative_to(root):
            raise ValueError("Inventory lock escapes project")
        inputs[path] = path.read_bytes()
        pilot.check_identity(pilot.identity(inputs[path]), item, "Inventory lock")
    lock = json.loads(inputs[root / config["reference_lock"]["relative_path"]])
    earlier = json.loads(inputs[root / config["pilot_lock"]["relative_path"]])
    if lock.get("status") != "active" or lock.get("baseline_selected_by_user") is not True or earlier["reference_sha256"] != lock["sha256"]:
        raise ValueError("No matching active PSP reference lock")
    iso_path = Path(iso_path)
    elf_path = Path(elf_path) if elf_path else root / lock["decrypted_executable"]["relative_path"]
    for path in (iso_path, elf_path):
        pilot.reject_link(path)
    iso_path, elf_path = iso_path.resolve(strict=True), elf_path.resolve(strict=True)
    protected = {config_path.resolve(), iso_path, elf_path, *[p.resolve() for p in inputs]}
    if report_path is not None:
        report_path = Path(report_path)
        pilot.reject_link(report_path)
        if report_path.resolve() in protected or report_path.exists():
            raise ValueError("Inventory report aliases input or existing evidence")
    before = iso_path.stat()
    pilot.check_identity(pilot.file_identity(iso_path), lock, "ISO")
    fresh_iso = pilot.inspect_iso(iso_path)
    # The ISO directory inspector reports size/SHA-256. The complete catalogue
    # checksum set is checked by file_identity before and after this scan.
    pilot.check_identity(fresh_iso, {key: lock[key] for key in ("size", "sha256")}, "Fresh ISO inventory")
    archive_pin = earlier["archive"]
    matches = [item for item in fresh_iso["files"] if item["path"] == archive_pin["iso_path"]]
    if len(matches) != 1:
        raise ValueError("Expected exactly one original archive")
    archive = matches[0]
    pilot.check_identity(archive, archive_pin, "Archive")
    if archive["lba"] != archive_pin["lba"]:
        raise ValueError("Archive extent moved")
    elf_data = elf_path.read_bytes()
    pilot.check_identity(pilot.identity(elf_data), lock["decrypted_executable"], "Reference ELF")
    elf = pilot.Elf32(elf_data)
    if elf.file_type != 2 or len(overlay_descriptors(elf)) != config["expected_named_descriptors"]:
        raise ValueError("Original named-overlay descriptor set changed")
    table_pin = earlier["decode_table"]
    table = elf.region(table_pin["elf_offset"], table_pin["size"])
    pilot.check_identity(pilot.identity(table), table_pin, "Decode table")
    if elf.virtual_bytes(table_pin["elf_address"], table_pin["size"]) != table:
        raise ValueError("Decode table address/file mapping disagrees")
    directory_pin = earlier["directory"]
    if not 0 < directory_pin["size"] <= pilot.MAX_DIRECTORY or directory_pin["size"] % pilot.BLOCK:
        raise ValueError("Invalid directory size")
    with iso_path.open("rb") as stream:
        encoded = pilot.read_extent(stream, archive["lba"] * pilot.BLOCK, archive["size"], 0, directory_pin["size"])
        pilot.check_identity(pilot.identity(encoded), directory_pin, "Encoded directory")
        directory = pilot.decode(encoded, 0, table)
        if pilot.identity(directory)["sha256"] != directory_pin["decoded_sha256"]:
            raise ValueError("Decoded directory drift")
        index = pilot.parse_index(directory, archive["size"], entry_count=directory_pin["entry_count"],
                                 exact_size_count=directory_pin["exact_size_count"])
        report = scan_prefixes(stream, archive["lba"] * pilot.BLOCK, archive["size"], index, table, elf)
    after = iso_path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError("ISO changed during inventory")
    # Timestamps alone do not bind the scanned bytes: a writer can restore them.
    pilot.reject_link(iso_path)
    pilot.check_identity(pilot.file_identity(iso_path), lock, "ISO after inventory")
    for path, raw in inputs.items():
        pilot.reject_link(path)
        if path.read_bytes() != raw:
            raise ValueError("Inventory lock changed during scan")
    pilot.reject_link(config_path)
    pilot.reject_link(elf_path)
    if config_path.read_bytes() != raw_config or elf_path.read_bytes() != elf_data:
        raise ValueError("Inventory profile or reference ELF changed during scan")
    report.update(schema_version=1, scope="bounded prefix inventory only; no full payload recovery or runtime",
                  profile_sha256=hashlib.sha256(raw_config).hexdigest(), iso={"size":lock["size"],"sha256":lock["sha256"]},
                  elf=pilot.identity(elf_data), archive={key:archive[key] for key in ("path","lba","size","sha256")},
                  directory={"encoded":pilot.identity(encoded),"decoded":pilot.identity(directory),
                    "uninterpreted_tail_size":len(directory)-4*(directory_pin["entry_count"]+1+2*directory_pin["exact_size_count"])},
                  matched_progress=0, runtime_tested=False)
    if report_path is not None:
        pilot.write_report(report_path, report)
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iso", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = inventory_overlays(args.iso, report_path=args.report)
        print(json.dumps({"status":report["status"], "coverage":report["coverage"], "report":str(args.report)}))
        return 0 if report["status"] == "OVERLAY_PREFIX_INVENTORY_COMPLETE" else 1
    except (OSError, ValueError, KeyError, TypeError, struct.error) as error:
        print("OVERLAY INVENTORY FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
