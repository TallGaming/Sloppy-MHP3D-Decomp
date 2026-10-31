"""Single-overlay recovery checks with invented ISO/archive/ELF bytes.

These validate reference tooling, not the future matching gate's 18 negatives.
The fixture encoder is used only to prepare disposable inputs; fixed decode
vectors independently constrain substitution, endianness and seed advancement.
"""

import copy
import hashlib
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

from scripts import extract_overlay as tool


BLOCK = 2048


def identity(data):
    return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def encode_fixture(plain, block, table):
    """Encode synthetic bytes by reversing the documented archive transform."""
    inverse = bytes(table.index(i) for i in range(256))
    high, low = (block >> 16) or 0x2345, (block & 0xffff) or 0x7f8d
    out = bytearray()
    for (word,) in struct.iter_unpack("<I", plain):
        high = high * 0x2345 % 0xffd9
        low = low * 0x7f8d % 0xfff1
        out += struct.pack("<I", word ^ (high << 16 | low))
    return bytes(out).translate(inverse)


def overlay_bytes(name="sample.ovl", load=0x09000000, code=16, data=16, bss=16):
    raw = bytearray(64 + code + data)
    struct.pack_into("<4s7I", raw, 0, b"MWo3", 1, load, code, data, bss,
                     (load + len(raw)) & 0xffffffff, (load + len(raw)) & 0xffffffff)
    raw[32:32 + len(name)] = name.encode("ascii")
    raw[64:] = bytes((i * 13) % 256 for i in range(code + data))
    return raw


def index_bytes(blocks=(1, 2, 3, 4), sizes=((1, 96),)):
    raw = bytearray(BLOCK)
    words = list(blocks) + [word for pair in sizes for word in pair]
    struct.pack_into("<%dI" % len(words), raw, 0, *words)
    raw[-8:] = b"opaque!!"  # Uninterpreted tail is not an invented terminator.
    return raw


def record(lba, size, name, directory=False):
    raw = bytearray(33 + len(name) + (len(name) % 2 == 0))
    raw[0], raw[25], raw[32] = len(raw), 2 if directory else 0, len(name)
    for offset, value in ((2, lba), (10, size)):
        struct.pack_into("<I", raw, offset, value)
        struct.pack_into(">I", raw, offset + 4, value)
    raw[33:33 + len(name)] = name
    return raw


def archive_iso(archive):
    """Build one bounded ISO9660 USRDIR tree, without borrowing game data."""
    raw = bytearray(26 * BLOCK)
    pvd = 16 * BLOCK
    raw[pvd:pvd + 7] = b"\x01CD001\x01"
    for offset, fmt, value in ((80, "<I", 26), (84, ">I", 26),
                                (128, "<H", BLOCK), (130, ">H", BLOCK)):
        struct.pack_into(fmt, raw, pvd + offset, value)
    root = record(18, BLOCK, b"\0", True)
    raw[pvd + 156:pvd + 156 + len(root)] = root
    directories = {
        18: root + record(18, BLOCK, b"\1", True) + record(19, BLOCK, b"PSP_GAME", True),
        19: record(19, BLOCK, b"\0", True) + record(18, BLOCK, b"\1", True)
            + record(20, BLOCK, b"USRDIR", True),
        20: record(20, BLOCK, b"\0", True) + record(19, BLOCK, b"\1", True)
            + record(22, len(archive), b"DATA.BIN"),
    }
    for lba, directory in directories.items():
        raw[lba * BLOCK:lba * BLOCK + len(directory)] = directory
    raw[22 * BLOCK:22 * BLOCK + len(archive)] = archive
    return bytes(raw)


def executable(table):
    """Create one allocated overlay descriptor and its indexed reservation."""
    raw = bytearray(0x500)
    names = b"\0.shstrtab\0.data\0sample.ovl\0"
    raw[0x100:0x200] = table
    raw[0x220:0x220 + len(names)] = names
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0,
                     b"\x7fELF\x01\x01\x01" + bytes(9), 2, 8, 1,
                     0x08804000, 52, 0x300, 0, 52, 32, 2, 40, 4, 1)
    struct.pack_into("<8I", raw, 52, 1, 0x100, 0x08804000, 0, 256, 256, 6, 4)
    struct.pack_into("<8I", raw, 84, 0, 0x200, 0x09000000, 0, 0, 112, 7, 4)
    for index, values in enumerate(((0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                                     (1, 3, 0, 0, 0x220, len(names), 0, 0, 1, 0),
                                     (11, 1, 3, 0x08804000, 0x100, 256, 0, 0, 4, 0),
                                     (17, 1, 7, 0x09000000, 0x200, 0, 0, 0, 4, 0))):
        struct.pack_into("<10I", raw, 0x300 + 40 * index, *values)
    return raw


class OverlayFormatTests(unittest.TestCase):
    def test_decode_fixed_vectors_advance_before_first_little_endian_word(self):
        self.assertEqual(tool.decode(bytes(12), 0, bytes(range(256))),
                         bytes.fromhex("19ed1dae1dead18c0d2b547c"))
        # Reversed substitution turns ff into 00 before the XOR sequence.
        self.assertEqual(tool.decode(b"\xff" * 12, 0, bytes(reversed(range(256)))),
                         bytes.fromhex("19ed1dae1dead18c0d2b547c"))
        self.assertNotEqual(tool.decode(bytes(4), 1, bytes(range(256))),
                            tool.decode(bytes(4), 0x10000, bytes(range(256))))

    def test_decode_rejects_bad_seeds_partial_words_and_nonpermutations(self):
        cases = [(bytes(4), -1, bytes(range(256))),
                 (bytes(4), 0x100000000, bytes(range(256))),
                 (bytes(3), 0, bytes(range(256))),
                 (bytes(4), 0, bytes(256)), (bytes(4), 0, bytes(255))]
        for args in cases:
            with self.subTest(args=(len(args[0]), args[1], len(args[2]))):
                with self.assertRaises(ValueError):
                    tool.decode(*args)

    def test_index_keeps_exact_sizes_distinct_from_sector_extents(self):
        parsed = tool.parse_index(index_bytes(), 4 * BLOCK, entry_count=3, exact_size_count=1)
        self.assertEqual(parsed, {"blocks": [1, 2, 3, 4], "exact_sizes": {1: 96}})

    def test_index_rejects_invalid_counts_sizes_and_boundaries(self):
        cases = [(index_bytes(), 4 * BLOCK, 0, 1),
                 (index_bytes(), 4 * BLOCK, 3, 4),
                 (index_bytes(), 4 * BLOCK, 1000, 0),
                 (index_bytes()[:-1], 4 * BLOCK, 3, 1),
                 (index_bytes(), 4 * BLOCK - 1, 3, 1),
                 (index_bytes((2, 2, 3, 4)), 4 * BLOCK, 3, 1),
                 (index_bytes((1, 3, 2, 4)), 4 * BLOCK, 3, 1),
                 (index_bytes((1, 2, 3, 5)), 4 * BLOCK, 3, 1),
                 (index_bytes(sizes=((3, 96),)), 4 * BLOCK, 3, 1),
                 (index_bytes(sizes=((1, 0),)), 4 * BLOCK, 3, 1),
                 (index_bytes(sizes=((1, BLOCK + 1),)), 4 * BLOCK, 3, 1),
                 (index_bytes(sizes=((1, 96), (1, 96))), 4 * BLOCK, 3, 2)]
        for data, size, entries, exact in cases:
            with self.subTest(size=size, entries=entries, exact=exact):
                with self.assertRaises(ValueError):
                    tool.parse_index(data, size, entry_count=entries, exact_size_count=exact)

    def test_overlay_storage_excludes_bss_and_preserves_provisional_address_words(self):
        header = tool.parse_overlay(overlay_bytes())
        self.assertEqual(header["name"], "sample.ovl")
        self.assertEqual(header["code_size"], 16)
        self.assertEqual(header["data_size"], 16)
        self.assertEqual(header["bss_size"], 16)
        self.assertEqual(header["end_address"], 0x09000060)

    def test_overlay_rejects_truncation_padding_bad_magic_names_and_overflow(self):
        good = overlay_bytes()
        cases = [good[:63], good[:-1], good + b"\0" * 4, b"BAD!" + good[4:],
                 overlay_bytes("../bad.ovl"), overlay_bytes(load=0xfffffff0)]
        unterminated = bytearray(good)
        unterminated[32:64] = b"A" * 32
        cases.append(unterminated)
        nonascii = bytearray(good)
        nonascii[32] = 0xff
        cases.append(nonascii)
        for data in cases:
            with self.subTest(size=len(data)):
                with self.assertRaises(ValueError):
                    tool.parse_overlay(data)

    def test_region_reads_are_bounded_and_reject_short_streams(self):
        self.assertEqual(tool.read_extent(io.BytesIO(b"0123456789"), 2, 8, 1, 3), b"345")
        for offset, length in ((-1, 1), (0, -1), (7, 2)):
            with self.assertRaises(ValueError):
                tool.read_extent(io.BytesIO(bytes(10)), 2, 8, offset, length)
        with self.assertRaises(ValueError):
            tool.read_extent(io.BytesIO(bytes(5)), 2, 8, 0, 8)


class ExtractOverlayTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name).resolve()
        self.iso = self.root / "synthetic.iso"
        self.elf = self.root / "synthetic.elf"
        self.output = self.root / "overlays"
        self.report_path = self.root / "report.json"
        self.lock_path = self.root / "reference.json"
        self.pilot_path = self.root / "pilot.json"
        self.table = bytes(reversed(range(256)))
        self.plain = bytes(overlay_bytes())
        self.directory = bytes(index_bytes())
        self.encrypted = encode_fixture(self.plain, 2, self.table)
        self.raw_directory = encode_fixture(self.directory, 0, self.table)
        archive = bytearray(b"X" * (4 * BLOCK))
        archive[:BLOCK] = self.raw_directory
        archive[2 * BLOCK:2 * BLOCK + len(self.encrypted)] = self.encrypted
        self.archive = bytes(archive)
        self.iso.write_bytes(archive_iso(self.archive))
        self.elf.write_bytes(executable(self.table))
        self.lock = {"status": "active", "baseline_selected_by_user": True,
                     **identity(self.iso.read_bytes()),
                     "decrypted_executable": identity(self.elf.read_bytes())}
        self.pilot = {"reference_sha256": self.lock["sha256"],
                      "archive": {"iso_path": "/PSP_GAME/USRDIR/DATA.BIN", "lba": 22,
                                  **identity(self.archive)},
                      "decode_table": {"elf_offset": 0x100, "elf_address": 0x08804000,
                                       **identity(self.table)},
                      "directory": {**identity(self.raw_directory),
                                    "decoded_sha256": identity(self.directory)["sha256"],
                                    "entry_count": 3, "exact_size_count": 1},
                      "overlay": {"archive_index": 1, "block": 2, "extent_size": BLOCK,
                                  "encrypted": identity(self.encrypted), "decoded": identity(self.plain),
                                  "header": tool.parse_overlay(self.plain), "descriptor_index": 3,
                                  "program_header_index": 1, "output_name": "sample.ovl.mwo"}}
        self.save_locks()

    def save_locks(self):
        self.lock_path.write_text(json.dumps(self.lock), encoding="utf-8")
        self.pilot_path.write_text(json.dumps(self.pilot), encoding="utf-8")

    def extract(self):
        return tool.extract_overlay(self.iso, self.output, elf_path=self.elf,
                                    lock_path=self.lock_path, overlay_lock_path=self.pilot_path,
                                    report_path=self.report_path)

    def assert_unpublished(self):
        self.assertFalse((self.output / "sample.ovl.mwo").exists())
        self.assertFalse(self.report_path.exists())

    def test_full_pipeline_recovers_exactly_one_unpadded_payload_and_preserves_sources(self):
        before = (self.iso.read_bytes(), self.elf.read_bytes())
        with mock.patch.object(tool, "read_extent", wraps=tool.read_extent) as reads:
            report = self.extract()
        self.assertEqual([(call.args[3], call.args[4]) for call in reads.call_args_list],
                         [(0, BLOCK), (2 * BLOCK, 96)])
        self.assertEqual(sorted(p.name for p in self.output.iterdir()), ["sample.ovl.mwo"])
        self.assertEqual((self.output / "sample.ovl.mwo").read_bytes(), self.plain)
        self.assertEqual((self.iso.read_bytes(), self.elf.read_bytes()), before)
        self.assertEqual(report["overlay"]["extent_size"], BLOCK)
        self.assertEqual(report["overlay"]["decoded"]["size"], 96)
        self.assertEqual(report["overlay"]["reserved_size"], 112)
        self.assertEqual(report["overlay"]["descriptor_index"], 3)
        self.assertEqual(report["overlay"]["program_header_index"], 1)
        self.assertEqual(report["overlay"]["compression"], "none")
        self.assertEqual(json.loads(self.report_path.read_text()), report)

    def test_repeat_runs_redecode_and_emit_identical_evidence(self):
        with mock.patch.object(tool, "decode", wraps=tool.decode) as decode:
            first = self.extract()
            evidence = self.report_path.read_bytes()
            second = self.extract()
        self.assertEqual(decode.call_count, 4)
        self.assertEqual(first, second)
        self.assertEqual(self.report_path.read_bytes(), evidence)

    def test_inactive_unselected_or_foreign_reference_is_rejected(self):
        for change in ({"status": "rejected"}, {"baseline_selected_by_user": False},
                       {"sha256": "0" * 64}):
            with self.subTest(change=change):
                old = copy.deepcopy(self.lock)
                self.lock.update(change)
                self.save_locks()
                with self.assertRaises(ValueError):
                    self.extract()
                self.assert_unpublished()
                self.lock = old

    def test_changed_iso_and_elf_fail_before_publication(self):
        for path in (self.iso, self.elf):
            with self.subTest(path=path.name):
                before = path.read_bytes()
                path.write_bytes(before[:-1] + bytes([before[-1] ^ 1]))
                with self.assertRaises(ValueError):
                    self.extract()
                self.assert_unpublished()
                path.write_bytes(before)

    def test_each_archive_transform_and_output_pin_is_enforced(self):
        mutations = [("archive", "sha256", "0" * 64), ("archive", "lba", 21),
                     ("decode_table", "sha256", "0" * 64),
                     ("decode_table", "elf_offset", 0xffff),
                     ("decode_table", "elf_address", 0x08804004),
                     ("directory", "sha256", "0" * 64),
                     ("directory", "decoded_sha256", "0" * 64),
                     ("directory", "size", tool.MAX_DIRECTORY + BLOCK),
                     ("overlay", "archive_index", 3), ("overlay", "block", 3),
                     ("overlay", "extent_size", 2 * BLOCK),
                     ("overlay", "descriptor_index", 2),
                     ("overlay", "program_header_index", 0),
                     ("overlay", "output_name", "../outside.mwo")]
        for section, field, value in mutations:
            with self.subTest(section=section, field=field):
                old = copy.deepcopy(self.pilot)
                self.pilot[section][field] = value
                self.save_locks()
                with self.assertRaises(ValueError):
                    self.extract()
                self.assert_unpublished()
                self.pilot = old
        for section in ("encrypted", "decoded"):
            with self.subTest(section=section):
                old = copy.deepcopy(self.pilot)
                self.pilot["overlay"][section]["sha256"] = "0" * 64
                self.save_locks()
                with self.assertRaises(ValueError):
                    self.extract()
                self.assert_unpublished()
                self.pilot = old

    def test_repinned_elf_requires_executable_and_allocated_progbits_descriptor(self):
        edits = [(16, "<H", 1), (0x300 + 3 * 40 + 4, "<I", 8),
                 (0x300 + 3 * 40 + 8, "<I", 0),
                 (0x300 + 3 * 40 + 12, "<I", 0x09000004),
                 (84 + 20, "<I", 116)]
        original = self.elf.read_bytes()
        for offset, fmt, value in edits:
            with self.subTest(offset=offset, value=value):
                raw = bytearray(original)
                struct.pack_into(fmt, raw, offset, value)
                self.elf.write_bytes(raw)
                self.lock["decrypted_executable"] = identity(raw)
                self.save_locks()
                with self.assertRaises(ValueError):
                    self.extract()
                self.assert_unpublished()

    def test_header_pin_disagreement_never_publishes(self):
        self.pilot["overlay"]["header"]["load_address"] += 4
        self.save_locks()
        with self.assertRaises(ValueError):
            self.extract()
        self.assert_unpublished()

    def test_payload_limit_fails_before_reading_or_decoding_selected_entry(self):
        with mock.patch.object(tool, "MAX_PAYLOAD", 64), \
                mock.patch.object(tool, "read_extent", wraps=tool.read_extent) as reads, \
                mock.patch.object(tool, "decode", wraps=tool.decode) as decode:
            with self.assertRaises(ValueError):
                self.extract()
        self.assertEqual(reads.call_count, 1)  # Only the bounded directory.
        self.assertEqual(decode.call_count, 1)
        self.assert_unpublished()

    def test_existing_conflicting_payload_is_preserved_and_no_report_written(self):
        self.output.mkdir()
        destination = self.output / "sample.ovl.mwo"
        destination.write_bytes(b"valuable existing file")
        with self.assertRaises(ValueError):
            self.extract()
        self.assertEqual(destination.read_bytes(), b"valuable existing file")
        self.assertFalse(self.report_path.exists())

    def test_existing_conflicting_report_prevents_payload_publication(self):
        self.report_path.write_bytes(b"valuable prior evidence")
        with self.assertRaises(ValueError):
            self.extract()
        self.assertEqual(self.report_path.read_bytes(), b"valuable prior evidence")
        self.assertFalse((self.output / "sample.ovl.mwo").exists())

    def test_failed_repeat_preserves_prior_good_outputs(self):
        self.extract()
        payload = (self.output / "sample.ovl.mwo").read_bytes()
        report = self.report_path.read_bytes()
        self.pilot["overlay"]["decoded"]["sha256"] = "0" * 64
        self.save_locks()
        with self.assertRaises(ValueError):
            self.extract()
        self.assertEqual((self.output / "sample.ovl.mwo").read_bytes(), payload)
        self.assertEqual(self.report_path.read_bytes(), report)

    def test_report_aliasing_inputs_or_payload_is_rejected(self):
        for path in (self.iso, self.elf, self.lock_path, self.pilot_path,
                     self.output / "sample.ovl.mwo"):
            with self.subTest(path=path.name):
                self.report_path = path
                with self.assertRaises(ValueError):
                    self.extract()
                self.assertFalse((self.output / "sample.ovl.mwo").exists())

    def test_staged_identity_failure_never_publishes(self):
        actual_identity = tool.file_identity
        def bad_stage(path):
            actual = actual_identity(path)
            if path.name == "sample.ovl.mwo" and path.parent.name.startswith(".overlay-"):
                actual["sha256"] = "0" * 64
            return actual
        with mock.patch.object(tool, "file_identity", side_effect=bad_stage):
            with self.assertRaises(ValueError):
                self.extract()
        self.assert_unpublished()
        self.assertEqual(list(self.output.iterdir()), [])

    def test_cli_reports_failure_without_evidence_for_bad_input(self):
        args = ["--iso", str(self.iso), "--elf", str(self.elf), "--lock", str(self.lock_path),
                "--overlay-lock", str(self.pilot_path), "--out-dir", str(self.output),
                "--report", str(self.report_path)]
        self.pilot["directory"]["decoded_sha256"] = "0" * 64
        self.save_locks()
        with mock.patch("sys.stderr", new_callable=io.StringIO) as error:
            self.assertEqual(tool.main(args), 1)
        self.assertIn("OVERLAY RECOVERY FAILED", error.getvalue())
        self.assert_unpublished()


if __name__ == "__main__":
    unittest.main()
