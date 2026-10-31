"""Standalone invented ELF tests: no game, compiler, SDK or private evidence."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

PATH = Path(__file__).resolve().parents[1] / "tools/repro/compare_function.py"
spec = importlib.util.spec_from_file_location("public_repro", PATH)
tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


def fixture(*, reference=False, code=bytes.fromhex("0800e00300000000")):
    """One invented function plus bounded symbol/REL and metadata sections."""
    raw = bytearray(0x600)
    names = b"\0.shstrtab\0.text\0.strtab\0.symtab\0.rel.text\0.metadata\0"
    raw[0x100:0x100 + len(names)] = names
    raw[0x200:0x200 + len(code)] = code
    strings = b"\0one\0other\0"
    raw[0x240:0x240 + len(strings)] = strings
    ident = b"\x7fELF\x01\x01\x01" + bytes(9)
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0, ident, 2 if reference else 1, 8, 1,
                     0x1000 if reference else 0, 0, 0x400, 0, 52, 0, 0, 40, 7, 1)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (names.index(b".shstrtab"), 3, 0, 0, 0x100, len(names), 0, 0, 1, 0),
                (names.index(b".text"), 1, 6, 0x1000 if reference else 0, 0x200, len(code), 0, 0, 4, 0),
                (names.index(b".strtab"), 3, 0, 0, 0x240, len(strings), 0, 0, 1, 0),
                (names.index(b".symtab"), 2, 0, 0, 0x280, 48, 3, 1, 4, 16),
                (names.index(b".rel.text"), 9, 0, 0, 0x300, 0, 4, 2, 4, 8),
                (names.index(b".metadata"), 1, 0, 0, 0x340, 8, 0, 0, 4, 0)]
    for i, values in enumerate(sections):
        struct.pack_into("<10I", raw, 0x400 + 40 * i, *values)
    struct.pack_into("<IIIBBH", raw, 0x290, 1, 0x1000 if reference else 0, len(code), 0x12, 0, 2)
    return raw


class PublicReproTests(unittest.TestCase):
    def test_inspection_without_reference_makes_no_comparison_or_credit(self):
        raw = bytes(fixture())
        report = tool.compare_function(raw, "initializer")
        self.assertEqual(report["status"], "OBJECT_INSPECTED_REFERENCE_NOT_SUPPLIED")
        self.assertIsNone(report["comparison"])
        self.assertEqual(report["inspection"]["function"]["symbol"], "one")
        self.assertEqual(report["inspection"]["function"]["size"], 8)
        self.assertEqual(report["inspection"]["object"], tool.identity(raw))
        self.assertFalse(report["game_match_credit"])
        self.assertFalse(report["source_participation_proved"])
        self.assertNotIn(raw[0x200:0x208].hex(), json.dumps(report))

    def test_private_reference_requires_complete_pinned_identity(self):
        with self.assertRaisesRegex(ValueError, "exact pinned"):
            tool.compare_function(bytes(fixture()), "initializer", bytes(fixture(reference=True)))

    def test_full_pinned_synthetic_reference_comparison_and_target_hash(self):
        obj, reference = bytes(fixture()), bytes(fixture(reference=True))
        invented_case = {"address": 0x1000, **tool.identity(reference[0x200:0x208])}
        with mock.patch.object(tool, "REFERENCE_IDENTITY", tool.identity(reference)), \
                mock.patch.dict(tool.CASES, {"initializer": invented_case}):
            report = tool.compare_function(obj, "initializer", reference)
            self.assertTrue(report["comparison"]["exact_diagnostic_body"])
            self.assertIsNone(report["comparison"]["first_difference"])
            self.assertFalse(report["game_match_credit"])
            damaged = reference[:-1] + b"changed"
            with self.assertRaisesRegex(ValueError, "exact pinned"):
                tool.compare_function(obj, "initializer", damaged)
            with mock.patch.dict(tool.CASES, {"initializer": {**invented_case, "sha256": "0" * 64}}):
                with self.assertRaisesRegex(ValueError, "interval identity"):
                    tool.compare_function(obj, "initializer", reference)

    def test_prefix_lengths_and_changed_words_never_become_exact(self):
        for compiled, target, difference in ((b"abcd", b"abcdxxxx", 4), (b"abcdxxxx", b"abcd", 4),
                                              (b"abXd", b"abcd", 2)):
            with self.subTest(compiled=compiled, target=target):
                result = tool.compare_complete(compiled, target)
                self.assertFalse(result["exact_diagnostic_body"])
                self.assertEqual(result["first_difference"], difference)

    def test_extra_zero_weak_local_duplicate_and_hidden_functions_rejected(self):
        changes = [(0x2A0, "<IIIBBH", (5, 0, 0, 0x12, 0, 2)),
                   (0x29C, "<B", (0x22,)), (0x29C, "<B", (0x02,)),
                   (0x29D, "<B", (2,)), (0x2A0, "<IIIBBH", (1, 0, 0, 0, 0, 0)),
                   (0x298, "<I", (0,))]
        for offset, fmt, values in changes:
            raw = fixture(); struct.pack_into(fmt, raw, offset, *values)
            with self.subTest(offset=offset, values=values), self.assertRaises(ValueError):
                tool.compare_function(bytes(raw), "initializer")

    def test_extent_alignment_executable_type_and_symbol_metadata_bounds(self):
        changes = [(0x294, "<I", (1,)), (0x298, "<I", (6,)), (0x298, "<I", (12,)),
                   (0x400 + 2 * 40 + 8, "<I", (2,)), (0x400 + 2 * 40 + 4, "<I", (8,)),
                   (0x400 + 4 * 40 + 24, "<I", (99,)), (0x400 + 4 * 40 + 36, "<I", (12,)),
                   (0x400 + 4 * 40 + 4, "<I", (11,)), (16, "<H", (2,)), (18, "<H", (3,))]
        for offset, fmt, values in changes:
            raw = fixture(); struct.pack_into(fmt, raw, offset, *values)
            with self.subTest(offset=offset, values=values), self.assertRaises(ValueError):
                tool.compare_function(bytes(raw), "key-advance")

    def test_nonzero_rel_and_rela_code_relocations_rejected_without_masking(self):
        for rela in (False, True):
            for kind in (1, 2, 4, 5, 6, 255):
                raw = fixture(); width = 12 if rela else 8
                struct.pack_into("<I", raw, 0x400 + 5 * 40 + 4, 4 if rela else 9)
                struct.pack_into("<I", raw, 0x400 + 5 * 40 + 20, width)
                struct.pack_into("<I", raw, 0x400 + 5 * 40 + 36, width)
                struct.pack_into("<IIi" if rela else "<II", raw, 0x300, *(0, 0x100 | kind, 0) if rela else (0, 0x100 | kind))
                with self.subTest(rela=rela, kind=kind), self.assertRaisesRegex(ValueError, "code relocations"):
                    tool.compare_function(bytes(raw), "initializer")

    def test_malformed_relocation_tables_symbols_places_and_links_rejected(self):
        for mutation in ("truncated", "link", "target", "symbol", "place"):
            raw = fixture(); struct.pack_into("<I", raw, 0x400 + 5 * 40 + 20, 8)
            struct.pack_into("<II", raw, 0x300, 0, 0x102)
            if mutation == "truncated": struct.pack_into("<I", raw, 0x400 + 5 * 40 + 20, 7)
            elif mutation == "link": struct.pack_into("<I", raw, 0x400 + 5 * 40 + 24, 3)
            elif mutation == "target": struct.pack_into("<I", raw, 0x400 + 5 * 40 + 28, 99)
            elif mutation == "symbol": struct.pack_into("<I", raw, 0x304, 0x9902)
            else: struct.pack_into("<I", raw, 0x300, 8)
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                tool.compare_function(bytes(raw), "initializer")

    def test_noncode_relocations_remain_unapplied_and_symbol_other_bits_retained(self):
        raw = fixture()
        struct.pack_into("<B", raw, 0x29D, 4)
        struct.pack_into("<I", raw, 0x400 + 5 * 40 + 20, 8)
        struct.pack_into("<I", raw, 0x400 + 5 * 40 + 28, 6)
        struct.pack_into("<II", raw, 0x300, 0, 0x102)
        original = bytes(raw)
        report = tool.compare_function(original, "initializer")
        self.assertEqual(report["inspection"]["non_code_relocations_retained_unapplied"], 1)
        self.assertEqual(report["inspection"]["function"]["raw_symbol_other"], 4)
        self.assertEqual(bytes(raw), original)
        self.assertFalse(report["relocations_applied_or_masked"])

    def test_cli_success_and_failure_have_no_native_or_private_inputs(self):
        with tempfile.TemporaryDirectory() as name:
            obj = Path(name) / "invented.o"; obj.write_bytes(fixture())
            stdout, stderr = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                self.assertEqual(tool.main(["--object", str(obj), "--case", "key-advance"]), 0)
            self.assertIsNone(json.loads(stdout.getvalue())["comparison"])
            obj.write_bytes(b"malformed invented data")
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(tool.main(["--object", str(obj), "--case", "initializer"]), 2)
            self.assertEqual(stdout.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
