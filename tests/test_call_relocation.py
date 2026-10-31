"""Narrow external JAL relocation controls built entirely from invented bytes.

These tests do not link an object, compare game functions, or implement the
matching build gate's 18 negative checks. Non-code metadata stays unapplied.
"""

import copy
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts import bench_direct_call as fixture_bench
from scripts.analyze_reference import validate_export
from scripts.call_relocation import apply_mips26, relocate_function
from scripts.elf32 import Elf32


SHOFF = 0x400
CODE = struct.pack("<7I", 0x27bdfff0, 0xafbf000c, 0x0c000000, 0,
                   0x8fbf000c, 0x03e00008, 0x27bd0010)


def make_object():
    """Create a call plus an unrelated data relocation; no game-derived bytes."""
    raw = bytearray(0x700)
    names = b"\0.shstrtab\0.text\0.strtab\0.symtab\0.rel.text\0.mwcats\0.rel.mwcats\0"
    symbols = b"\0fixture_call\0fixture_external\0"
    raw[0x100:0x100 + len(names)] = names
    raw[0x180:0x180 + len(CODE)] = CODE
    raw[0x200:0x200 + len(symbols)] = symbols
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0,
                     b"\x7fELF\x01\x01\x01" + bytes(9), 1, 8, 1, 0, 0,
                     SHOFF, 0x10970001, 52, 0, 0, 40, 8, 1)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (names.index(b".shstrtab"), 3, 0, 0, 0x100, len(names), 0, 0, 1, 0),
                (names.index(b".text"), 1, 6, 0, 0x180, len(CODE), 0, 0, 4, 0),
                (names.index(b".strtab"), 3, 0, 0, 0x200, len(symbols), 0, 0, 1, 0),
                (names.index(b".symtab"), 2, 0, 0, 0x240, 48, 3, 1, 4, 16),
                (names.index(b".rel.text"), 9, 0, 0, 0x300, 8, 4, 2, 4, 8),
                (names.index(b".mwcats"), 1, 0, 0, 0x320, 4, 0, 0, 4, 0),
                (names.index(b".rel.mwcats"), 9, 0, 0, 0x330, 8, 4, 6, 4, 8)]
    for index, section in enumerate(sections):
        struct.pack_into("<10I", raw, SHOFF + index * 40, *section)
    struct.pack_into("<IIIBBH", raw, 0x250, 1, 0, len(CODE), 0x12, 0, 2)
    struct.pack_into("<IIIBBH", raw, 0x260, 14, 0, 0, 0x10, 0, 0)
    struct.pack_into("<II", raw, 0x300, 8, (2 << 8) | 4)
    struct.pack_into("<II", raw, 0x330, 0, (1 << 8) | 2)
    return raw


class Mips26InstructionTests(unittest.TestCase):
    def test_known_external_address_vectors(self):
        self.assertEqual(apply_mips26(0x0c000000, 0x08810008, 0x08840000), 0x0e210000)
        self.assertEqual(apply_mips26(0x0c000001, 0x08810008, 0x08840000), 0x0e210001)
        # A low field of 0x03ffffff is a signed 28-bit byte addend of minus four.
        self.assertEqual(apply_mips26(0x0fffffff, 0x08810008, 0x08840000), 0x0e20ffff)

    def test_region_comes_from_delay_slot_address_not_call_address(self):
        self.assertEqual(apply_mips26(0x0c000000, 0x0ffffffc, 0x10000000), 0x0c000000)
        with self.assertRaises(ValueError):
            apply_mips26(0x0c000000, 0x0ffffffc, 0x0ffffffc)
        with self.assertRaises(ValueError):
            apply_mips26(0x0c000000, 0x0ffffff8, 0x10000000)

    def test_rejects_non_jal_alignment_and_32bit_input_range(self):
        for word, place, symbol in ((0x08000000, 0x08810008, 0x08840000),
                                    (0, 0x08810008, 0x08840000),
                                    (-1, 0x08810008, 0x08840000),
                                    (0x10c000000, 0x08810008, 0x08840000),
                                    (0x0c000000, 0x08810009, 0x08840000),
                                    (0x0c000000, 0x08810008, 0x08840002),
                                    (0x0c000000, -4, 0x08840000),
                                    (0x0c000000, 0x100000000, 0x08840000),
                                    (0x0c000000, 0x08810008, -4),
                                    (0x0c000000, 0x08810008, 0x100000000),
                                    (True, 0x08810008, 0x08840000),
                                    (0x0c000000, False, 0x08840000),
                                    (0x0c000000, 0x08810008, False)):
            with self.subTest(word=word, place=place, symbol=symbol):
                with self.assertRaises(ValueError):
                    apply_mips26(word, place, symbol)

    def test_addend_result_cannot_wrap_underflow_or_jump_regions(self):
        for word, place, symbol in ((0x0c000001, 0xffffff00, 0xfffffffc),
                                    (0x0fffffff, 0x08810008, 0),
                                    (0x0c000001, 0x0ffffff0, 0x0ffffffc),
                                    (0x0c000000, 0xfffffffc, 0)):
            with self.subTest(word=word, place=place, symbol=symbol):
                with self.assertRaises(ValueError):
                    apply_mips26(word, place, symbol)


class RelocateFunctionTests(unittest.TestCase):
    def setUp(self):
        self.raw = make_object()
        self.calls = [{"offset": 8, "symbol": "fixture_external", "addend": 0}]
        self.symbols = {"fixture_external": 0x08840000}

    def relocate(self):
        return relocate_function(bytes(self.raw), function_name="fixture_call",
                                 load_address=0x08810000, symbols=self.symbols,
                                 expected_calls=self.calls)

    def test_patches_only_declared_word_and_reports_unapplied_metadata(self):
        original = bytes(self.raw)
        result = self.relocate()
        expected = bytearray(CODE)
        struct.pack_into("<I", expected, 8, 0x0e210000)
        self.assertEqual(result["bytes"], expected)
        self.assertEqual(result["bytes"][:8], CODE[:8])
        self.assertEqual(result["bytes"][12:], CODE[12:])
        self.assertEqual(len(result["relocations"]), 1)
        self.assertEqual(len(result["non_code_relocations"]), 1)
        self.assertEqual(bytes(self.raw), original)
        self.assertEqual(result, self.relocate())

    def test_section_relative_offset_is_translated_to_function_relative_offset(self):
        self.raw[0x180:0x180 + len(CODE) + 4] = bytes(4) + CODE
        struct.pack_into("<I", self.raw, SHOFF + 2 * 40 + 20, len(CODE) + 4)
        struct.pack_into("<I", self.raw, 0x250 + 4, 4)
        struct.pack_into("<I", self.raw, 0x300, 12)
        result = self.relocate()
        self.assertEqual(len(result["bytes"]), len(CODE))
        self.assertEqual(struct.unpack_from("<I", result["bytes"], 8)[0], 0x0e210000)

    def test_positive_and_negative_implicit_addends_must_match_declared_plan(self):
        for word, addend, expected in ((0x0c000001, 4, 0x0e210001),
                                       (0x0fffffff, -4, 0x0e20ffff)):
            with self.subTest(addend=addend):
                struct.pack_into("<I", self.raw, 0x188, word)
                self.calls[0]["addend"] = addend
                self.assertEqual(struct.unpack_from("<I", self.relocate()["bytes"], 8)[0], expected)
                self.calls[0]["addend"] = 0
                with self.assertRaises(ValueError):
                    self.relocate()

    def test_absent_extra_duplicate_or_wrong_call_plans_are_rejected(self):
        cases = [[], [self.calls[0], self.calls[0]],
                 [{"offset": 4, "symbol": "fixture_external", "addend": 0}],
                 [{"offset": 8, "symbol": "different_symbol", "addend": 0}],
                 [{"offset": 9, "symbol": "fixture_external", "addend": 0}],
                 [{"offset": 24, "symbol": "fixture_external", "addend": 0}],
                 [{"offset": -4, "symbol": "fixture_external", "addend": 0}]]
        for calls in cases:
            with self.subTest(calls=calls):
                self.calls = calls
                with self.assertRaises(ValueError):
                    self.relocate()

    def test_external_assignments_are_explicit_and_aligned(self):
        for symbols in ({}, {"fixture_external": 0x08840002},
                        {"fixture_external": -4}, {"fixture_external": 0x100000000},
                        {"fixture_external": 0x18840000},
                        {"fixture_external": 0x08840000, "unexpected": 0x08850000}):
            with self.subTest(symbols=symbols):
                self.symbols = symbols
                with self.assertRaises(ValueError):
                    self.relocate()

    def test_external_symbol_must_be_unique_undefined_global_default_visibility(self):
        changes = [(0x260 + 4, "<I", 4), (0x260 + 8, "<I", 4),
                   (0x260 + 12, "<B", 0), (0x260 + 12, "<B", 0x20),
                   (0x260 + 12, "<B", 0x13), (0x260 + 13, "<B", 2),
                   (0x260 + 14, "<H", 2)]
        for offset, fmt, value in changes:
            with self.subTest(offset=offset, value=value):
                self.raw = make_object()
                struct.pack_into(fmt, self.raw, offset, value)
                with self.assertRaises(ValueError):
                    self.relocate()
        self.raw = make_object()
        self.raw[0x270:0x280] = self.raw[0x260:0x270]
        struct.pack_into("<I", self.raw, SHOFF + 4 * 40 + 20, 64)
        with self.assertRaises(ValueError):
            self.relocate()

    def test_global_undefined_function_symbol_type_is_also_supported(self):
        self.raw[0x260 + 12] = 0x12
        self.assertEqual(struct.unpack_from("<I", self.relocate()["bytes"], 8)[0], 0x0e210000)

    def test_unsupported_code_type_rela_or_non_jal_never_gets_masked(self):
        for relocation_type in (0, 2, 5, 6, 10, 255):
            with self.subTest(relocation_type=relocation_type):
                self.raw = make_object()
                struct.pack_into("<I", self.raw, 0x304, (2 << 8) | relocation_type)
                with self.assertRaises(ValueError):
                    self.relocate()
        self.raw = make_object()
        struct.pack_into("<I", self.raw, SHOFF + 5 * 40 + 4, 4)
        struct.pack_into("<I", self.raw, SHOFF + 5 * 40 + 20, 12)
        struct.pack_into("<I", self.raw, SHOFF + 5 * 40 + 36, 12)
        with self.assertRaises(ValueError):
            self.relocate()
        self.raw = make_object()
        struct.pack_into("<I", self.raw, 0x188, 0x08000000)
        with self.assertRaises(ValueError):
            self.relocate()

    def test_duplicate_relocation_records_fail(self):
        self.raw[0x308:0x310] = self.raw[0x300:0x308]
        struct.pack_into("<I", self.raw, SHOFF + 5 * 40 + 20, 16)
        with self.assertRaises(ValueError):
            self.relocate()

    def test_duplicate_places_across_relocation_sections_fail(self):
        for section in (5, 7):
            with self.subTest(section=section):
                self.raw = make_object()
                original = SHOFF + section * 40
                self.raw[SHOFF + 8 * 40:SHOFF + 9 * 40] = self.raw[original:original + 40]
                struct.pack_into("<H", self.raw, 48, 9)
                with self.assertRaises(ValueError):
                    self.relocate()

    def test_noncode_relocations_are_only_validated_reported_rel32(self):
        for kind in (0, 4, 5, 255):
            with self.subTest(kind=kind):
                self.raw = make_object()
                struct.pack_into("<I", self.raw, 0x334, (1 << 8) | kind)
                with self.assertRaises(ValueError):
                    self.relocate()
        self.raw = make_object()
        struct.pack_into("<I", self.raw, SHOFF + 7 * 40 + 4, 4)
        struct.pack_into("<I", self.raw, SHOFF + 7 * 40 + 20, 12)
        struct.pack_into("<I", self.raw, SHOFF + 7 * 40 + 36, 12)
        with self.assertRaises(ValueError):
            self.relocate()

    def test_relocation_table_links_indices_offsets_and_truncation_are_checked(self):
        changes = [(SHOFF + 5 * 40 + 20, 7), (SHOFF + 5 * 40 + 36, 4),
                   (SHOFF + 5 * 40 + 24, 3), (SHOFF + 5 * 40 + 28, 99),
                   (SHOFF + 5 * 40 + 16, len(self.raw) - 4),
                   (0x304, (99 << 8) | 4), (0x300, len(CODE)), (0x300, 9),
                   (0x330, 4), (0x334, (99 << 8) | 2)]
        for offset, value in changes:
            with self.subTest(offset=offset, value=value):
                self.raw = make_object()
                struct.pack_into("<I", self.raw, offset, value)
                with self.assertRaises(ValueError):
                    self.relocate()

    def test_call_delay_word_must_be_inside_selected_function(self):
        struct.pack_into("<I", self.raw, 0x250 + 8, 12)
        with self.assertRaises(ValueError):
            self.relocate()

    def test_function_symbol_layout_bounds_and_duplicate_names_are_checked(self):
        changes = [(16, "<H", 2), (18, "<H", 3),
                   (SHOFF + 2 * 40 + 8, "<I", 2),
                   (0x250 + 4, "<I", 4), (0x250 + 8, "<I", 0),
                   (0x250 + 8, "<I", len(CODE) - 1), (0x250 + 14, "<H", 0)]
        for offset, fmt, value in changes:
            with self.subTest(offset=offset, value=value):
                self.raw = make_object()
                struct.pack_into(fmt, self.raw, offset, value)
                with self.assertRaises(ValueError):
                    self.relocate()
        self.raw = make_object()
        self.raw[0x270:0x280] = self.raw[0x250:0x260]
        struct.pack_into("<I", self.raw, SHOFF + 4 * 40 + 20, 64)
        with self.assertRaises(ValueError):
            self.relocate()

    def test_function_load_address_cannot_be_unaligned_or_overflow(self):
        for address in (-4, 0x08810001, 0x100000000, 0xfffffff0):
            with self.subTest(address=address):
                with self.assertRaises(ValueError):
                    relocate_function(bytes(self.raw), function_name="fixture_call",
                                      load_address=address, symbols=self.symbols,
                                      expected_calls=self.calls)


class DirectCallRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.candidates_path = self.root / "candidates.json"
        self.fixture_path = self.root / "fixture.json"
        self.report_path = self.root / "evidence/report.json"
        self.source = self.write("bench/fixture.c", b"/* Invented direct-call source. */\n")
        self.runner = self.write("tools/runner", b"invented runner")
        self.compilers = [self.write("tools/first.exe", b"invented first compiler"),
                          self.write("tools/second.exe", b"invented second compiler")]
        self.support = self.write("tools/support.dll", b"invented support")
        self.object = bytes(make_object())
        self.candidates = {"status": "investigation_only_not_locked",
                           "runner": self.pin(self.runner),
                           "candidates": [{"id": "first", "compiler": self.pin(self.compilers[0]),
                                           "support_files": [self.pin(self.support)]},
                                          {"id": "second", "compiler": self.pin(self.compilers[1]),
                                           "support_files": []}]}
        self.fixture = {"status": "invented_fixture_only_not_game_toolchain_lock",
                        "source": self.pin(self.source),
                        "flags": ["-nostdinc", "-lang", "c", "-c", "-O2"],
                        "function_name": "fixture_call", "load_address": 0x08810000,
                        "symbols": {"fixture_external": 0x08840000},
                        "expected_calls": [{"offset": 8, "symbol": "fixture_external", "addend": 0}],
                        "expected_resolved_word": 0x0e210000}
        self.save()
        patcher = mock.patch.object(fixture_bench, "compile_probe", side_effect=self.compile_ok)
        self.compiler = patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def pin(self, path):
        data = path.read_bytes()
        return {"relative_path": path.relative_to(self.root).as_posix(),
                "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}

    def save(self):
        self.candidates_path.write_text(json.dumps(self.candidates), encoding="utf-8")
        self.fixture["candidate_config_sha256"] = hashlib.sha256(self.candidates_path.read_bytes()).hexdigest()
        self.fixture_path.write_text(json.dumps(self.fixture), encoding="utf-8")

    def compile_ok(self, compiler, runner, source, output, flags, **kwargs):
        self.assertFalse(output.exists(), "Each candidate needs a fresh object path")
        output.write_bytes(self.object)
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def run_fixture(self):
        return fixture_bench.run_fixture(root=self.root, fixture_lock_path=self.fixture_path,
                                         candidates_path=self.candidates_path, report_path=self.report_path)

    def assert_no_report(self):
        self.assertFalse(self.report_path.exists())
        self.assertEqual(list((self.root / "build").rglob("report.json")), [])

    def test_complete_fixture_uses_same_flags_and_records_real_resolved_bytes(self):
        report = self.run_fixture()
        self.assertEqual(self.compiler.call_count, 2)
        self.assertTrue(all(call.args[4] == self.fixture["flags"] for call in self.compiler.call_args_list))
        self.assertTrue(all(call.args[2] == self.source for call in self.compiler.call_args_list))
        self.assertEqual(report["matched_progress"], 0)
        self.assertEqual(len(report["results"]), 2)
        for row in report["results"]:
            self.assertEqual(row["object_sha256"], hashlib.sha256(self.object).hexdigest())
            self.assertEqual(row["function_size"], len(CODE))
            self.assertEqual(row["relocations"][0]["resolved_word"], 0x0e210000)
            self.assertEqual(len(row["non_code_relocations"]), 1)
        self.assertEqual(json.loads(self.report_path.read_text()), report)
        self.assertEqual(len(list((self.root / "build").rglob("*.resolved.bin"))), 2)

    def test_repeat_fixture_uses_fresh_paths_and_identical_reports(self):
        first = self.run_fixture()
        raw = self.report_path.read_bytes()
        second = self.run_fixture()
        self.assertEqual(first, second)
        self.assertEqual(raw, self.report_path.read_bytes())
        self.assertEqual(len({call.args[3] for call in self.compiler.call_args_list}), 4)
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_source_runner_compiler_support_and_candidate_pins_are_enforced(self):
        for path in (self.source, self.runner, self.compilers[0], self.support, self.candidates_path):
            with self.subTest(path=path.name):
                old = path.read_bytes()
                path.write_bytes(old + b"changed")
                with self.assertRaises(ValueError):
                    self.run_fixture()
                self.compiler.assert_not_called()
                self.assert_no_report()
                path.write_bytes(old)

    def test_wrong_status_empty_or_duplicate_candidates_fail_without_compilation(self):
        original = self.candidates["candidates"]
        for rows in ([], [original[0], original[0]]):
            self.candidates["candidates"] = rows
            self.save()
            with self.assertRaises(ValueError):
                self.run_fixture()
            self.compiler.assert_not_called()
        self.candidates["candidates"] = original
        self.candidates["status"] = "locked"
        self.save()
        with self.assertRaises(ValueError):
            self.run_fixture()
        self.candidates["status"] = "investigation_only_not_locked"
        self.fixture["status"] = "game_match"
        self.save()
        with self.assertRaises(ValueError):
            self.run_fixture()
        self.compiler.assert_not_called()
        self.assert_no_report()

    def test_compile_failure_or_warning_rejects_even_a_valid_object(self):
        for code, diagnostic in ((1, "compile failed"), (0, "Warning: synthetic issue")):
            with self.subTest(code=code):
                def fail(*args, **kwargs):
                    self.compile_ok(*args, **kwargs)
                    return {"returncode": code, "stdout": "", "stderr": diagnostic}
                self.compiler.side_effect = fail
                with self.assertRaises(ValueError):
                    self.run_fixture()
                self.assert_no_report()

    def test_missing_output_and_timeout_never_reuse_stale_objects(self):
        self.write("build/stale.o", self.object)
        self.compiler.side_effect = lambda *args, **kwargs: {"returncode": 0, "stdout": "", "stderr": ""}
        with self.assertRaises(ValueError):
            self.run_fixture()
        self.assert_no_report()
        self.compiler.side_effect = subprocess.TimeoutExpired("invented", 20)
        with self.assertRaises((ValueError, subprocess.TimeoutExpired)):
            self.run_fixture()
        self.assert_no_report()

    def test_second_candidate_failure_never_publishes_partial_scores(self):
        def fail_second(*args, **kwargs):
            result = self.compile_ok(*args, **kwargs)
            if args[0] == self.compilers[1]:
                result["returncode"] = 1
            return result
        self.compiler.side_effect = fail_second
        with self.assertRaises(ValueError):
            self.run_fixture()
        self.assertEqual(self.compiler.call_count, 2)
        self.assert_no_report()

    def test_invalid_object_unsupported_call_and_wrong_independent_word_fail(self):
        self.object = b"not ELF"
        with self.assertRaises(ValueError):
            self.run_fixture()
        self.assert_no_report()
        bad = make_object()
        struct.pack_into("<I", bad, 0x304, (2 << 8) | 5)
        self.object = bytes(bad)
        with self.assertRaises(ValueError):
            self.run_fixture()
        self.assert_no_report()
        self.object = bytes(make_object())
        self.fixture["expected_resolved_word"] ^= 1
        self.save()
        with self.assertRaises(ValueError):
            self.run_fixture()
        self.assert_no_report()

    def test_changed_inputs_during_compilation_invalidate_report(self):
        for path in (self.source, self.runner, self.compilers[0], self.support,
                     self.fixture_path, self.candidates_path):
            with self.subTest(path=path.name):
                old = path.read_bytes()
                def change(*args, **kwargs):
                    result = self.compile_ok(*args, **kwargs)
                    path.write_bytes(old + b"changed")
                    return result
                self.compiler.side_effect = change
                with self.assertRaises(ValueError):
                    self.run_fixture()
                self.assert_no_report()
                path.write_bytes(old)

    def test_existing_report_conflict_and_input_aliases_are_preserved(self):
        self.report_path.parent.mkdir()
        self.report_path.write_bytes(b"valuable prior evidence")
        with self.assertRaises(ValueError):
            self.run_fixture()
        self.assertEqual(self.report_path.read_bytes(), b"valuable prior evidence")
        for path in (self.source, self.runner, self.compilers[0], self.support,
                     self.fixture_path, self.candidates_path):
            with self.subTest(path=path.name):
                original = path.read_bytes()
                self.report_path = path
                with self.assertRaises(ValueError):
                    self.run_fixture()
                self.assertEqual(path.read_bytes(), original)

    def test_failed_repeat_preserves_previous_success_report(self):
        self.run_fixture()
        original = self.report_path.read_bytes()
        self.compiler.side_effect = subprocess.TimeoutExpired("invented", 20)
        with self.assertRaises((ValueError, subprocess.TimeoutExpired)):
            self.run_fixture()
        self.assertEqual(self.report_path.read_bytes(), original)


class ValidateGhidraExportTests(unittest.TestCase):
    def setUp(self):
        raw = make_object()
        struct.pack_into("<H", raw, 16, 2)
        struct.pack_into("<I", raw, SHOFF + 2 * 40 + 12, 0x08810000)
        struct.pack_into("<I", raw, 0x188, 0x0e204000)  # JAL to first target.
        self.reference = Elf32(raw)
        self.probes = [{"address": 0x08810000, "size": 8,
                        "target_sha256": hashlib.sha256(raw[0x180:0x188]).hexdigest()},
                       {"address": 0x08810014, "size": 8,
                        "target_sha256": hashlib.sha256(raw[0x194:0x19c]).hexdigest()}]
        self.export = {"language_id": "Allegrex:LE:32:default", "compiler_spec_id": "default",
                       "executable_sha256": hashlib.sha256(raw).hexdigest(), "image_base": "08810000",
                       "memory_blocks": [{"name": ".text", "start": "08810000", "end": "0881001b",
                                          "size": 28, "initialized": True, "execute": True}],
                       "targets": [{"address": "08810000", "size": 8,
                                    "memory_sha256": self.probes[0]["target_sha256"],
                                    "function_at_start": "08810000",
                                    "call_references": [{"site": "08810008", "caller": "08810008"}]},
                                   {"address": "08810014", "size": 8,
                                    "memory_sha256": self.probes[1]["target_sha256"],
                                    "function_at_start": "08810014", "call_references": []}],
                       "functions": [{"entry": "08810000", "body_min": "08810000", "body_max": "08810007",
                                      "body_address_count": 8, "decompile_completed": True},
                                     {"entry": "08810008", "body_min": "08810008", "body_max": "08810013",
                                      "body_address_count": 12, "decompile_completed": True},
                                     {"entry": "08810014", "body_min": "08810014", "body_max": "0881001b",
                                      "body_address_count": 8, "decompile_completed": True}]}

    def validate(self, data=None):
        return validate_export(self.export if data is None else data, self.reference, self.probes)

    def test_correct_import_bytes_and_raw_jal_scan_produce_bounded_summary(self):
        summary = self.validate()
        self.assertEqual(summary["exported_function_count"], 3)
        self.assertEqual(summary["completed_decompilations"], 3)
        self.assertEqual(summary["verified_targets"][0]["direct_call_sites"], [0x08810008])
        self.assertEqual(summary["verified_targets"][0]["caller_entries"], [0x08810008])

    def test_processor_identity_base_and_text_mapping_must_agree(self):
        changes = [("language_id", "MIPS:BE:32:default"), ("compiler_spec_id", "other"),
                   ("executable_sha256", "0" * 64), ("image_base", "08810004")]
        for field, value in changes:
            with self.subTest(field=field):
                data = copy.deepcopy(self.export)
                data[field] = value
                with self.assertRaises(ValueError):
                    self.validate(data)
        for field, value in (("start", "08810004"), ("end", "08810017"),
                             ("size", 24), ("initialized", False)):
            with self.subTest(field=field):
                data = copy.deepcopy(self.export)
                data["memory_blocks"][0][field] = value
                with self.assertRaises(ValueError):
                    self.validate(data)

    def test_target_hash_function_body_and_completion_cannot_be_assumed(self):
        for collection, field, value in (("targets", "memory_sha256", "0" * 64),
                                         ("targets", "function_at_start", None),
                                         ("targets", "size", 4),
                                         ("functions", "body_address_count", 4),
                                         ("functions", "body_max", "08810003"),
                                         ("functions", "decompile_completed", False)):
            with self.subTest(collection=collection, field=field):
                data = copy.deepcopy(self.export)
                data[collection][0][field] = value
                with self.assertRaises(ValueError):
                    self.validate(data)
        for collection in ("targets", "functions"):
            data = copy.deepcopy(self.export)
            data[collection].append(data[collection][0])
            with self.assertRaises(ValueError):
                self.validate(data)

    def test_missing_extra_duplicate_and_unexported_direct_callers_fail(self):
        calls = self.export["targets"][0]["call_references"]
        for value in ([], calls + calls, [{"site": "0881000c", "caller": "08810008"}],
                      [{"site": "08810008", "caller": None}],
                      [{"site": "08810008", "caller": "08820000"}]):
            with self.subTest(calls=value):
                data = copy.deepcopy(self.export)
                data["targets"][0]["call_references"] = value
                with self.assertRaises(ValueError):
                    self.validate(data)

    def test_existing_function_outside_call_site_cannot_be_reported_as_caller(self):
        self.export["targets"][0]["call_references"][0]["caller"] = "08810014"
        with self.assertRaises(ValueError):
            self.validate()
        self.export["targets"][0]["call_references"][0]["caller"] = "08810008"
        self.export["functions"][1]["decompile_completed"] = False
        with self.assertRaises(ValueError):
            self.validate()


if __name__ == "__main__":
    unittest.main()
