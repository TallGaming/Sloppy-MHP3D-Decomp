#!/usr/bin/env python3
"""Read-only inventory of a candidate ISO or save-data folder.

Hashes and metadata describe the supplied bytes. They do not authenticate a
release, select a compiler, or accept an input as the matching reference.
Only the optional JSON report is written; game files are always opened read-only.
"""

import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys


SECTOR_SIZE = 2048
CHUNK_SIZE = 8 * 1024 * 1024


def hash_region(stream, offset, size):
    """Hash exactly one bounded file region, rejecting truncated input."""
    stream.seek(offset)
    digest = hashlib.sha256()
    remaining = size
    while remaining:
        chunk = stream.read(min(CHUNK_SIZE, remaining))
        if not chunk:
            raise ValueError("Input ended before the declared region boundary")
        digest.update(chunk)
        remaining -= len(chunk)
    return digest.hexdigest()


def parse_sfo(data):
    """Decode bounded PARAM.SFO records, preserving binary values as hex."""
    if len(data) < 20 or data[:4] != b"\0PSF":
        raise ValueError("Not a complete PARAM.SFO header")
    _, version, keys, values, count = struct.unpack_from("<4s4I", data)
    table_end = 20 + count * 16
    if not table_end <= keys <= values <= len(data):
        raise ValueError("PARAM.SFO table offsets are invalid")
    result = {}
    for index in range(count):
        key_offset, fmt, length, capacity, value_offset = struct.unpack_from(
            "<HHIII", data, 20 + index * 16
        )
        start = keys + key_offset
        if not keys <= start < values:
            raise ValueError("PARAM.SFO key offset is invalid")
        end = data.find(b"\0", start, values)
        if end < 0:
            raise ValueError("PARAM.SFO key is not terminated")
        key = data[start:end].decode("utf-8")
        if key in result:
            raise ValueError("Duplicate PARAM.SFO key: " + key)
        start = values + value_offset
        if length > capacity or start + capacity > len(data):
            raise ValueError("PARAM.SFO value exceeds its declared bounds")
        raw = data[start:start + length]
        if fmt == 0x404:
            if length != 4:
                raise ValueError("PARAM.SFO integer has invalid size")
            value = struct.unpack("<I", raw)[0]
        elif fmt == 0x204:
            value = raw.rstrip(b"\0").decode("utf-8")
        else:
            value = {"format": fmt, "hex": raw.hex()}
        result[key] = value
    return {"version": version, "values": result}


def describe_region(stream, offset, size, name):
    """Describe a file's identity and inspect recognized metadata only."""
    record = {"path": name, "size": size,
              "sha256": hash_region(stream, offset, size)}
    stream.seek(offset)
    record["header_hex"] = stream.read(min(size, 16)).hex()
    if Path(name).name.upper().split(";")[0] == "PARAM.SFO" and size:
        if size > 16 * 1024 * 1024:
            raise ValueError("PARAM.SFO exceeds the metadata size limit")
        stream.seek(offset)
        record["sfo"] = parse_sfo(stream.read(size))
    if Path(name).name.upper().split(";")[0] == "BOOT.BIN":
        # A zero placeholder is not an unwrapped executable.
        stream.seek(offset)
        remaining = size
        all_zero = True
        while remaining:
            chunk = stream.read(min(CHUNK_SIZE, remaining))
            if not chunk:
                raise ValueError("BOOT.BIN region is truncated")
            all_zero = all_zero and not any(chunk)
            remaining -= len(chunk)
        record["all_zero"] = all_zero
    return record


def inspect_iso(path):
    """Inventory the primary ISO9660 tree and hash every file and the image."""
    size = path.stat().st_size
    with path.open("rb") as stream:
        stream.seek(16 * SECTOR_SIZE)
        pvd = stream.read(SECTOR_SIZE)
        if len(pvd) != SECTOR_SIZE or pvd[:7] != b"\x01CD001\x01":
            raise ValueError("Expected a primary ISO9660 descriptor at sector 16")
        if struct.unpack_from("<H", pvd, 128)[0] != SECTOR_SIZE:
            raise ValueError("Unsupported ISO9660 logical block size")
        if struct.unpack_from(">H", pvd, 130)[0] != SECTOR_SIZE:
            raise ValueError("ISO9660 logical block size copies disagree")
        volume_blocks = struct.unpack_from("<I", pvd, 80)[0]
        if volume_blocks != struct.unpack_from(">I", pvd, 84)[0]:
            raise ValueError("ISO9660 volume size copies disagree")
        volume_size = volume_blocks * SECTOR_SIZE
        if not 17 * SECTOR_SIZE <= volume_size <= size:
            raise ValueError("ISO9660 volume size exceeds the input")
        files = []
        seen_directories = set()
        seen_paths = set()

        def bounds(lba, length):
            offset = lba * SECTOR_SIZE
            if offset + length > volume_size:
                raise ValueError("ISO9660 extent exceeds the declared volume")
            return offset

        def extent(record):
            if len(record) < 34:
                raise ValueError("ISO9660 directory record is truncated")
            lba = struct.unpack_from("<I", record, 2)[0]
            length = struct.unpack_from("<I", record, 10)[0]
            if (lba != struct.unpack_from(">I", record, 6)[0]
                    or length != struct.unpack_from(">I", record, 14)[0]):
                raise ValueError("ISO9660 extent field copies disagree")
            bounds(lba, length)
            return lba, length

        def walk(lba, length, prefix, depth):
            if depth > 32 or len(seen_paths) > 100000:
                raise ValueError("ISO9660 directory traversal limit exceeded")
            if (lba, length) in seen_directories:
                raise ValueError("ISO9660 directory cycle or repeated extent")
            seen_directories.add((lba, length))
            if length > 16 * 1024 * 1024:
                raise ValueError("ISO9660 directory exceeds the size limit")
            stream.seek(bounds(lba, length))
            data = stream.read(length)
            pos = 0
            while pos < length:
                record_size = data[pos]
                if not record_size:
                    pos = (pos // SECTOR_SIZE + 1) * SECTOR_SIZE
                    continue
                if (record_size < 34 or pos + record_size > length
                        or pos % SECTOR_SIZE + record_size > SECTOR_SIZE):
                    raise ValueError("Invalid ISO9660 directory record boundary")
                record = data[pos:pos + record_size]
                pos += record_size
                name_size = record[32]
                if not name_size or 33 + name_size > record_size:
                    raise ValueError("Invalid ISO9660 filename length")
                name = record[33:33 + name_size]
                if name in (b"\0", b"\1"):
                    continue
                child_lba, child_size = extent(record)
                if record[25] & 0x80:
                    raise ValueError("Multi-extent ISO9660 files are unsupported")
                name = name.decode("ascii")
                if "/" in name or "\\" in name or name in (".", ".."):
                    raise ValueError("Invalid ISO9660 path component")
                child = prefix + "/" + name
                if child in seen_paths:
                    raise ValueError("Duplicate ISO9660 path: " + child)
                seen_paths.add(child)
                if record[25] & 2:
                    walk(child_lba, child_size, child, depth + 1)
                else:
                    entry = describe_region(
                        stream, bounds(child_lba, child_size), child_size, child
                    )
                    entry["lba"] = child_lba
                    files.append(entry)

        root_size = pvd[156]
        if root_size < 34 or 156 + root_size > len(pvd):
            raise ValueError("Invalid ISO9660 root record")
        root = pvd[156:156 + root_size]
        if not root[25] & 2:
            raise ValueError("ISO9660 root record is not a directory")
        walk(*extent(root), "", 0)
        return {"kind": "iso9660", "path": str(path), "size": size,
                "sha256": hash_region(stream, 0, size),
                "system_id": pvd[8:40].decode("ascii").rstrip(),
                "volume_id": pvd[40:72].decode("ascii").rstrip(),
                "baseline_accepted": False,
                "files": sorted(files, key=lambda entry: entry["path"])}


def inspect_path(path):
    """Dispatch between an image, a single file, and a local data directory."""
    if path.is_symlink():
        raise ValueError("Symbolic link inputs are unsupported")
    path = path.resolve(strict=True)
    if path.is_file() and path.suffix.lower() == ".iso":
        return inspect_iso(path)
    files = []
    candidates = sorted(path.rglob("*")) if path.is_dir() else [path]
    for candidate in candidates:
        if candidate.is_symlink():
            raise ValueError("Symbolic links in an input directory are unsupported")
        if candidate.is_file():
            name = (candidate.relative_to(path).as_posix()
                    if path.is_dir() else candidate.name)
            with candidate.open("rb") as stream:
                files.append(describe_region(stream, 0, candidate.stat().st_size, name))
    return {"kind": "directory" if path.is_dir() else "file", "path": str(path),
            "baseline_accepted": False, "files": files}


def main():
    """Print an inventory, or create a new report without overwriting evidence."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        report = inspect_path(args.input)
        encoded = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with args.out.open("x", encoding="utf-8") as stream:
                stream.write(encoded)
            print("Inventory written to " + str(args.out.resolve()))
        else:
            print(encoded, end="")
        return 0
    except (OSError, ValueError, struct.error) as error:
        print("INSPECTION FAILED: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
