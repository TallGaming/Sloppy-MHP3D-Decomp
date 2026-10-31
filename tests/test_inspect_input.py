"""Synthetic format/error tests for the inspector, independent of game bytes.

These are input-tool tests. They are not the future 18 build-gate negative checks.
"""

import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest

from scripts.inspect_input import inspect_path, parse_sfo, SECTOR_SIZE


def make_sfo():
    """Build a minimal one-string SFO with independently known offsets."""
    return (struct.pack("<4s4I", b"\0PSF", 0x101, 36, 42, 1)
            + struct.pack("<HHIII", 0, 0x204, 5, 5, 0)
            + b"TITLE\0test\0")


def make_record(lba, length, name, flags=0):
    """Build an ISO directory record with both endian copies populated."""
    record = bytearray(33 + len(name) + (len(name) % 2 == 0))
    record[0] = len(record)
    struct.pack_into("<I", record, 2, lba)
    struct.pack_into(">I", record, 6, lba)
    struct.pack_into("<I", record, 10, length)
    struct.pack_into(">I", record, 14, length)
    record[25] = flags
    record[32] = len(name)
    record[33:33 + len(name)] = name
    return record


def make_iso():
    """Build a tiny ISO with an SFO and a four-byte zero BOOT.BIN."""
    image = bytearray(21 * SECTOR_SIZE)
    pvd = 16 * SECTOR_SIZE
    image[pvd:pvd + 7] = b"\x01CD001\x01"
    struct.pack_into("<I", image, pvd + 80, 21)
    struct.pack_into(">I", image, pvd + 84, 21)
    struct.pack_into("<H", image, pvd + 128, SECTOR_SIZE)
    struct.pack_into(">H", image, pvd + 130, SECTOR_SIZE)
    root = make_record(18, SECTOR_SIZE, b"\0", 2)
    image[pvd + 156:pvd + 156 + len(root)] = root
    records = (root + make_record(18, SECTOR_SIZE, b"\1", 2)
               + make_record(19, len(make_sfo()), b"PARAM.SFO")
               + make_record(20, 4, b"BOOT.BIN"))
    image[18 * SECTOR_SIZE:18 * SECTOR_SIZE + len(records)] = records
    image[19 * SECTOR_SIZE:19 * SECTOR_SIZE + len(make_sfo())] = make_sfo()
    return image


class InspectorTests(unittest.TestCase):
    def test_sfo_string(self):
        self.assertEqual(parse_sfo(make_sfo())["values"], {"TITLE": "test"})

    def test_sfo_truncated_header(self):
        with self.assertRaisesRegex(ValueError, "header"):
            parse_sfo(b"\0PSF")

    def test_sfo_value_outside_file(self):
        data = bytearray(make_sfo())
        struct.pack_into("<I", data, 32, 1000)
        with self.assertRaisesRegex(ValueError, "bounds"):
            parse_sfo(data)

    def test_sfo_unterminated_key(self):
        data = bytearray(make_sfo())
        data[41] = ord("x")
        with self.assertRaisesRegex(ValueError, "terminated"):
            parse_sfo(data)

    def test_iso_inventory_hashes_and_placeholder(self):
        image = make_iso()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.iso"
            path.write_bytes(image)
            report = inspect_path(path)
        self.assertEqual(report["sha256"], hashlib.sha256(image).hexdigest())
        self.assertFalse(report["baseline_accepted"])
        files = {entry["path"]: entry for entry in report["files"]}
        self.assertEqual(set(files), {"/PARAM.SFO", "/BOOT.BIN"})
        self.assertEqual(files["/PARAM.SFO"]["sfo"]["values"]["TITLE"], "test")
        self.assertEqual(files["/PARAM.SFO"]["sha256"], hashlib.sha256(make_sfo()).hexdigest())
        self.assertTrue(files["/BOOT.BIN"]["all_zero"])

    def test_iso_out_of_bounds_extent(self):
        image = make_iso()
        offset = 18 * SECTOR_SIZE + 68
        struct.pack_into("<I", image, offset + 2, 1000)
        struct.pack_into(">I", image, offset + 6, 1000)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.iso"
            path.write_bytes(image)
            with self.assertRaisesRegex(ValueError, "exceeds"):
                inspect_path(path)

    def test_iso_disagreeing_endian_copies(self):
        image = make_iso()
        struct.pack_into(">I", image, 16 * SECTOR_SIZE + 84, 20)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.iso"
            path.write_bytes(image)
            with self.assertRaisesRegex(ValueError, "disagree"):
                inspect_path(path)

    def test_iso_directory_cycle(self):
        image = make_iso()
        record = make_record(18, SECTOR_SIZE, b"LOOP", 2)
        offset = 18 * SECTOR_SIZE + 68
        image[offset:offset + len(record)] = record
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.iso"
            path.write_bytes(image)
            with self.assertRaisesRegex(ValueError, "cycle"):
                inspect_path(path)

    def test_cli_preserves_existing_report(self):
        script = Path(__file__).resolve().parents[1] / "scripts" / "inspect_input.py"
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "PARAM.SFO"
            source.write_bytes(make_sfo())
            report = Path(folder) / "report.json"
            report.write_text("existing evidence", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(script), str(source), "--out", str(report)],
                capture_output=True, text=True, timeout=10
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("INSPECTION FAILED", result.stderr)
            self.assertEqual(report.read_text(encoding="utf-8"), "existing evidence")
            self.assertEqual(source.read_bytes(), make_sfo())


if __name__ == "__main__":
    unittest.main()
