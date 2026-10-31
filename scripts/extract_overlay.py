#!/usr/bin/env python3
"""Recover the single Bucket 2 overlay from the pinned original PSP image.

The archive and executable are opened read-only. Decode only the directory and
one selected payload; no bulk-extraction interface or game execution is provided.
All pins, lengths and descriptor relationships pass before output publication.
This is reference recovery, not a matching build or runtime validation.

Format research: codestation/mhtools (d71d174) Decrypter/DecryptUtils and
TeamGDB/Yakumo docs/DATA_BIN.md. See docs/ARCHIVE_FORMAT.md for attribution and
PSP-specific evidence. The substitution table is read from the local pinned ELF;
no game table or payload is embedded in this script.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import tempfile

try:
    from .elf32 import Elf32
    from .inspect_input import inspect_iso
    from .prepare_reference import check_identity, file_identity, reject_link, write_report
except ImportError:
    from elf32 import Elf32
    from inspect_input import inspect_iso
    from prepare_reference import check_identity, file_identity, reject_link, write_report


ROOT = Path(__file__).resolve().parents[1]
BLOCK = 2048
MAX_DIRECTORY = 1024 * 1024
MAX_PAYLOAD = 16 * 1024 * 1024


def identity(data):
    """Describe exactly the bytes in a validated in-memory range."""
    return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def decode(data, block, table):
    """Undo byte substitution and the two modular halfword sequences.

    Seed from the archive-relative block, independently for each entry. The
    generators advance before each word, including the first. This pilot reads
    only whole words; arbitrary-length or compressed assets are outside scope.
    """
    if not isinstance(block, int) or not 0 <= block <= 0xFFFFFFFF:
        raise ValueError("Invalid archive block seed")
    if len(data) % 4:
        raise ValueError("Decode input must contain complete words")
    if len(table) != 256 or len(set(table)) != 256:
        raise ValueError("Decode table must be a 256-byte permutation")
    high = (block >> 16) or 0x2345
    low = (block & 0xFFFF) or 0x7F8D
    output = bytearray(data.translate(bytes(table)))
    for offset in range(0, len(output), 4):
        high = high * 0x2345 % 0xFFD9
        low = low * 0x7F8D % 0xFFF1
        word = struct.unpack_from("<I", output, offset)[0]
        struct.pack_into("<I", output, offset, word ^ (high << 16 | low))
    return bytes(output)


def parse_index(decoded, archive_size, *, entry_count, exact_size_count):
    """Validate the pinned table boundaries instead of guessing a terminator.

    The trailing directory bytes have no established meaning and are preserved
    by the directory hash. Do not reinterpret that tail as additional entries.
    """
    if (not 0 < len(decoded) <= MAX_DIRECTORY or len(decoded) % BLOCK
            or archive_size <= len(decoded) or archive_size % BLOCK):
        raise ValueError("Invalid directory/archive size")
    if (not isinstance(entry_count, int) or not isinstance(exact_size_count, int)
            or entry_count <= 0 or not 0 <= exact_size_count <= entry_count
            or (entry_count + 1 + 2 * exact_size_count) * 4 > len(decoded)):
        raise ValueError("Invalid index table counts")
    words = struct.unpack("<%dI" % (len(decoded) // 4), decoded)
    blocks = list(words[:entry_count + 1])
    if blocks[0] * BLOCK != len(decoded) or blocks[-1] * BLOCK != archive_size:
        raise ValueError("Directory or archive boundary disagrees with block table")
    if any(right < left for left, right in zip(blocks, blocks[1:])):
        raise ValueError("Archive blocks are not monotone")
    sizes = {}
    start = entry_count + 1
    previous = -1
    for pos in range(start, start + exact_size_count * 2, 2):
        index, length = words[pos:pos + 2]
        if not previous < index < entry_count:
            raise ValueError("Exact-size indices are invalid or not strictly sorted")
        if not 0 < length <= (blocks[index + 1] - blocks[index]) * BLOCK:
            raise ValueError("Exact length exceeds its archive extent")
        sizes[index] = length
        previous = index
    return {"blocks": blocks, "exact_sizes": sizes}


def parse_overlay(data):
    """Read the MWo3 header and validate its stored and memory ranges.

    The two final address words keep provisional names. Their exact loader
    semantics are not established by parsing or by disassembly plausibility.
    """
    if len(data) < 64 or data[:4] != b"MWo3":
        raise ValueError("Not a complete MWo3 overlay")
    fields = dict(zip(("id", "load_address", "code_size", "data_size", "bss_size",
                       "end_address", "entry_address"),
                      struct.unpack_from("<7I", data, 4)))
    if 64 + fields["code_size"] + fields["data_size"] != len(data):
        raise ValueError("Overlay header length disagrees with decoded payload")
    if fields["load_address"] + len(data) + fields["bss_size"] > 0x100000000:
        raise ValueError("Overlay memory range overflows 32 bits")
    raw_name = data[32:64]
    if b"\0" not in raw_name:
        raise ValueError("Overlay name is not terminated")
    try:
        name = raw_name.split(b"\0", 1)[0].decode("ascii")
    except UnicodeDecodeError as error:
        raise ValueError("Overlay name is not ASCII") from error
    if not re.fullmatch(r"[A-Za-z0-9_]+\.ovl", name):
        raise ValueError("Invalid overlay name")
    fields["name"] = name
    return fields


def read_extent(stream, archive_offset, archive_size, offset, length):
    """Read one bounded region relative to the freshly located archive."""
    if offset < 0 or length < 0 or offset + length > archive_size:
        raise ValueError("Requested region exceeds archive bounds")
    stream.seek(archive_offset + offset)
    data = stream.read(length)
    if len(data) != length:
        raise ValueError("Archive region is truncated")
    return data


def extract_overlay(iso_path, output_dir, *, elf_path=None,
                    lock_path=ROOT / "config/reference.json",
                    overlay_lock_path=ROOT / "config/overlay-pilot.json",
                    report_path=None):
    """Recover one pinned overlay; publish only after all verification succeeds."""
    iso_path, output_dir = Path(iso_path), Path(output_dir)
    lock_path, overlay_lock_path = Path(lock_path), Path(overlay_lock_path)
    lock_bytes, pilot_bytes = lock_path.read_bytes(), overlay_lock_path.read_bytes()
    lock, pilot = json.loads(lock_bytes), json.loads(pilot_bytes)
    if lock.get("status") != "active" or lock.get("baseline_selected_by_user") is not True:
        raise ValueError("No active user-selected reference lock")
    if pilot["reference_sha256"] != lock["sha256"]:
        raise ValueError("Overlay pilot belongs to another reference")
    elf_path = Path(elf_path) if elf_path is not None else ROOT / lock["decrypted_executable"]["relative_path"]
    for path in (iso_path, elf_path, output_dir):
        reject_link(path)
    iso_path, elf_path = iso_path.resolve(strict=True), elf_path.resolve(strict=True)
    before = iso_path.stat()
    iso_identity = file_identity(iso_path)
    check_identity(iso_identity, lock, "ISO")
    inventory = inspect_iso(iso_path)
    check_identity(inventory, {k: lock[k] for k in ("size", "sha256")},
                   "Fresh ISO inventory")
    archive_pin = pilot["archive"]
    matches = [f for f in inventory["files"] if f["path"] == archive_pin["iso_path"]]
    if len(matches) != 1:
        raise ValueError("Expected exactly one game archive")
    archive = matches[0]
    check_identity(archive, archive_pin, "Game archive")
    if archive["lba"] != archive_pin["lba"]:
        raise ValueError("Game archive LBA changed")
    elf_data = elf_path.read_bytes()
    check_identity(identity(elf_data), lock["decrypted_executable"], "Decrypted executable")
    elf = Elf32(elf_data)
    if elf.file_type != 2:
        raise ValueError("Decrypted executable is not an ELF executable")
    table_pin = pilot["decode_table"]
    table = elf.region(table_pin["elf_offset"], table_pin["size"])
    check_identity(identity(table), table_pin, "Decode table")
    if elf.virtual_bytes(table_pin["elf_address"], table_pin["size"]) != table:
        raise ValueError("Decode table file offset and allocated address disagree")
    directory_pin, selected = pilot["directory"], pilot["overlay"]
    directory_size = directory_pin["size"]
    if not 0 < directory_size <= MAX_DIRECTORY or directory_size % BLOCK:
        raise ValueError("Invalid pinned directory size")
    with iso_path.open("rb") as stream:
        raw_directory = read_extent(stream, archive["lba"] * BLOCK, archive["size"], 0, directory_size)
        check_identity(identity(raw_directory), directory_pin, "Encrypted directory")
        directory = decode(raw_directory, 0, table)
        if identity(directory)["sha256"] != directory_pin["decoded_sha256"]:
            raise ValueError("Decoded directory hash mismatch")
        index = parse_index(directory, archive["size"],
                            entry_count=directory_pin["entry_count"],
                            exact_size_count=directory_pin["exact_size_count"])
        number = selected["archive_index"]
        if not isinstance(number, int) or not 0 <= number < len(index["blocks"]) - 1:
            raise ValueError("Selected overlay index is outside the archive")
        block = index["blocks"][number]
        extent = (index["blocks"][number + 1] - block) * BLOCK
        length = index["exact_sizes"].get(number, extent)
        if block != selected["block"] or extent != selected["extent_size"]:
            raise ValueError("Selected overlay extent disagrees with pin")
        if not 64 <= length <= MAX_PAYLOAD:
            raise ValueError("Selected payload exceeds pilot size bounds")
        raw = read_extent(stream, archive["lba"] * BLOCK, archive["size"], block * BLOCK, length)
    check_identity(identity(raw), selected["encrypted"], "Encrypted overlay")
    payload = decode(raw, block, table)
    check_identity(identity(payload), selected["decoded"], "Decoded overlay")
    header = parse_overlay(payload)
    if header != selected["header"]:
        raise ValueError("Overlay header disagrees with pin")
    descriptors = [s for s in elf.sections if s["name"] == header["name"]]
    if (len(descriptors) != 1 or descriptors[0]["index"] != selected["descriptor_index"]
            or descriptors[0]["type"] != 1 or not descriptors[0]["flags"] & 2
            or descriptors[0]["size"] != 0 or descriptors[0]["address"] != header["load_address"]):
        raise ValueError("Named ELF descriptor does not match overlay")
    ph_index = selected["program_header_index"]
    if not isinstance(ph_index, int) or not 0 <= ph_index < len(elf.program_headers):
        raise ValueError("Invalid overlay program-header index")
    ph = elf.program_headers[ph_index]
    if (ph_index != header["id"] or ph[0] != 0 or ph[4] != 0
            or ph[2] != header["load_address"] or ph[5] != len(payload) + header["bss_size"]):
        raise ValueError("ELF reservation does not match overlay ID/address/size")
    after = iso_path.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError("ISO changed during overlay extraction")
    output_name = selected["output_name"]
    if output_name != header["name"] + ".mwo":
        raise ValueError("Output name disagrees with overlay name")
    destination = output_dir / output_name
    protected = {p.resolve() for p in (iso_path, elf_path, lock_path, overlay_lock_path)}
    if destination.resolve() in protected:
        raise ValueError("Overlay output aliases an input")
    report = {
        "schema_version": 1, "status": "OVERLAY_RECOVERY_PASS",
        "scope": "one reference overlay; not a build, source match or runtime test",
        "reference_lock_sha256": hashlib.sha256(lock_bytes).hexdigest(),
        "overlay_lock_sha256": hashlib.sha256(pilot_bytes).hexdigest(),
        "iso": iso_identity,
        "elf": identity(elf_data),
        "archive": {k: archive[k] for k in ("path", "lba", "size", "sha256")},
        "directory": {"encrypted": identity(raw_directory), "decoded": identity(directory),
                      "entry_count": directory_pin["entry_count"],
                      "exact_size_count": directory_pin["exact_size_count"],
                      "uninterpreted_tail_size": len(directory) - 4 * (directory_pin["entry_count"] + 1 + 2 * directory_pin["exact_size_count"])},
        "overlay": {"archive_index": number, "archive_offset": block * BLOCK,
                    "iso_offset": (archive["lba"] + block) * BLOCK,
                    "extent_size": extent, "encrypted": identity(raw),
                    "decoded": identity(payload), "header": header,
                    "descriptor_index": descriptors[0]["index"],
                    "program_header_index": ph_index, "reserved_size": ph[5],
                    "output_name": output_name, "compression": "none"}}
    if report_path is not None:
        report_path = Path(report_path)
        reject_link(report_path)
        if report_path.resolve() in protected | {destination.resolve()}:
            raise ValueError("Report aliases an input or overlay output")
        expected_report = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if report_path.exists() and report_path.read_text(encoding="utf-8") != expected_report:
            raise ValueError("Existing report differs; choose a fresh report path")
    reject_link(destination)
    if destination.exists():
        check_identity(file_identity(destination), selected["decoded"], "Existing overlay")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        # Validate in memory first, then stage in the intended output directory.
        with tempfile.TemporaryDirectory(prefix=".overlay-", dir=output_dir) as temp:
            stage = Path(temp).resolve()
            if not stage.is_relative_to(output_dir.resolve()):
                raise ValueError("Staging directory escaped overlay output directory")
            staged = stage / output_name
            staged.write_bytes(payload)
            check_identity(file_identity(staged), selected["decoded"], "Staged overlay")
            with destination.open("xb") as stream:
                stream.write(staged.read_bytes())
    if report_path is not None:
        write_report(report_path, report)
    return report


def main(argv=None):
    """Expose only the selected overlay and produce deterministic local evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iso", type=Path, required=True)
    parser.add_argument("--elf", type=Path)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "reference/uljm05800-v102/overlays")
    parser.add_argument("--lock", type=Path, default=ROOT / "config/reference.json")
    parser.add_argument("--overlay-lock", type=Path, default=ROOT / "config/overlay-pilot.json")
    parser.add_argument("--report", type=Path, default=ROOT / "evidence/bucket-02/overlay-recovery.json")
    args = parser.parse_args(argv)
    try:
        report = extract_overlay(args.iso, args.out_dir, elf_path=args.elf,
                                 lock_path=args.lock, overlay_lock_path=args.overlay_lock,
                                 report_path=args.report)
        print(report["status"] + ": " + report["overlay"]["header"]["name"])
        print("Report: " + str(args.report.resolve()))
        return 0
    except (OSError, ValueError, KeyError, TypeError, struct.error) as error:
        print("OVERLAY RECOVERY FAILED: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
