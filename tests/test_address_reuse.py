"""Invented ELF/static-address controls; compilation is always mocked."""

import copy
import hashlib
import json
import struct
import subprocess
import unittest
from unittest import mock

from scripts import bench_address_reuse as reuse
from tests import test_archive_key_probe as inherited


MEMBER = "initialize_key__17ArchiveKeyContextFUi"
OFFSETS = {"lower": 0x1A120, "upper": 0x1A124}
SHOFF = 0x400
SYMOFF = 0x200
CODEOFF = 0x600


def sha(data):
    return hashlib.sha256(data).hexdigest()


def r(rs, rt, rd, function, shift=0):
    return (rs << 21) | (rt << 16) | (rd << 11) | (shift << 6) | function


def i(opcode, rs, rt, immediate):
    return (opcode << 26) | (rs << 21) | (rt << 16) | (immediate & 0xffff)


def address_pair(register=8):
    return [i(15, 0, 2, 2), r(4, 2, register, 0x21)]


def shared_base_words():
    """One affine base, two optional stores; constants and offsets are invented."""
    return [*address_pair(), r(0, 5, 3, 2, 16), i(12, 5, 9, 0xffff),
            i(43, 8, 3, 0xa124), i(43, 8, 9, 0xa120),
            i(5, 9, 0, 3), 0, i(9, 0, 2, 0x1357), i(43, 8, 2, 0xa120),
            i(35, 8, 2, 0xa124), i(5, 2, 0, 3), 0,
            i(9, 0, 2, 0x2468), i(43, 8, 2, 0xa124), 0x03e00008, 0]


def repeated_base_words():
    """Five distinct materialization sites, same four possible access traces."""
    return [r(0, 5, 3, 2, 16), i(12, 5, 9, 0xffff),
            *address_pair(), i(43, 8, 3, 0xa124),
            *address_pair(), i(43, 8, 9, 0xa120),
            i(5, 9, 0, 5), 0, i(9, 0, 2, 0x1357),
            *address_pair(), i(43, 8, 2, 0xa120),
            *address_pair(), i(35, 8, 2, 0xa124),
            i(5, 2, 0, 5), 0, i(9, 0, 2, 0x2468),
            *address_pair(), i(43, 8, 2, 0xa124), 0x03e00008, 0]


def fixture(words=None, symbol=MEMBER):
    if words is None:
        words = shared_base_words()
    code = struct.pack("<" + "I" * len(words), *words)
    raw = bytearray(0x1800)
    names = b"\0.shstrtab\0.text\0.strtab\0.symtab\0.rel.text\0.comment\0"
    strings = b"\0" + symbol.encode() + b"\0unexpected\0"
    raw[0x80:0x80 + len(names)] = names
    raw[CODEOFF:CODEOFF + len(code)] = code
    raw[0x180:0x180 + len(strings)] = strings
    comment = b"Invented address fixture\0"
    raw[0x300:0x300 + len(comment)] = comment
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0,
                     b"\x7fELF\x01\x01\x01" + bytes(9), 1, 8, 1, 0, 0, SHOFF,
                     0x10970001, 52, 0, 0, 40, 7, 1)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (names.index(b".shstrtab"), 3, 0, 0, 0x80, len(names), 0, 0, 1, 0),
                (names.index(b".text"), 1, 6, 0, CODEOFF, len(code), 0, 0, 4, 0),
                (names.index(b".strtab"), 3, 0, 0, 0x180, len(strings), 0, 0, 1, 0),
                (names.index(b".symtab"), 2, 0, 0, SYMOFF, 32, 3, 1, 4, 16),
                (names.index(b".rel.text"), 9, 0, 0, 0x280, 0, 4, 2, 4, 8),
                (names.index(b".comment"), 1, 0, 0, 0x300, len(comment), 0, 0, 1, 0)]
    for index, section in enumerate(sections):
        struct.pack_into("<10I", raw, SHOFF + index * 40, *section)
    struct.pack_into("<IIIBBH", raw, SYMOFF + 16, 1, 0, len(code), 0x12, 0, 2)
    return raw


class AddressAnalysisTests(unittest.TestCase):
    def analyze(self, words, **kwargs):
        return reuse.analyze_address_paths(struct.pack("<" + "I" * len(words), *words), OFFSETS, **kwargs)

    def assert_unknown(self, result):
        self.assertEqual(result["status"], "UNINTERPRETED")
        self.assertIsNone(result["large_base_site_count"])
        self.assertIsNone(result["large_base_sites"])
        self.assertIsNone(result["access_traces"])

    def test_shared_and_repeated_bases_validate_all_four_access_paths_and_static_site_union(self):
        shared = self.analyze(shared_base_words())
        repeated = self.analyze(repeated_base_words())
        self.assertEqual(shared["status"], "INTERPRETED")
        self.assertEqual(repeated["status"], "INTERPRETED")
        self.assertEqual(shared["large_base_site_count"], 1)
        self.assertEqual(shared["large_base_sites"], [4])
        self.assertEqual(repeated["large_base_site_count"], 5)
        self.assertEqual(len(shared["access_traces"]), 4)
        self.assertEqual(shared["access_traces"], repeated["access_traces"])
        self.assertEqual(sorted(len(t) for t in shared["access_traces"]), [3, 4, 4, 5])

    def test_small_addiu_chain_cannot_manufacture_a_zero_large_base_advantage(self):
        words = [i(9, 4, 8, 0x7fff), *([i(9, 8, 8, 0x7fff)] * 3), i(9, 8, 8, 4),
                 *shared_base_words()[2:]]
        self.assert_unknown(self.analyze(words))

    def test_unused_large_address_arithmetic_does_not_inflate_memory_base_site_count(self):
        words = [*address_pair(15), *shared_base_words()]
        result = self.analyze(words)
        self.assertEqual(result["status"], "INTERPRETED")
        self.assertEqual(result["large_base_site_count"], 1)
        self.assertEqual(result["large_base_sites"], [12])

    def test_unknown_instructions_calls_loops_and_bad_delays_leave_no_partial_counts(self):
        for word in (0x44020000, i(3, 0, 0, 0), i(5, 9, 0, -1), 0x03c00008):
            with self.subTest(word=hex(word)):
                words = shared_base_words()
                words[2] = word
                self.assert_unknown(self.analyze(words))
        for position in (7, 12, 16):
            with self.subTest(position=position):
                words = shared_base_words()
                words[position] = i(9, 0, 10, 1)
                self.assert_unknown(self.analyze(words))

    def test_unresolved_loaded_or_masked_bases_do_not_keep_old_receiver_provenance(self):
        for clobber in (i(12, 8, 8, 0xffff), i(35, 8, 8, 0xa124),
                        r(5, 0, 8, 0x21), i(15, 0, 8, 2)):
            with self.subTest(clobber=hex(clobber)):
                words = shared_base_words()
                words[2] = clobber
                self.assert_unknown(self.analyze(words))

    def test_forward_branch_skipping_a_base_definition_is_not_interpreted_from_only_good_path(self):
        words = [i(4, 5, 0, 3), 0, *shared_base_words()]
        # Taken edge reaches the body with t0 undefined; fall-through sets t0.
        self.assert_unknown(self.analyze(words))

    def test_wrong_offsets_access_order_and_clobbered_return_address_fail_closed(self):
        for position, replacement in ((4, i(43, 8, 3, 0xa120)),
                                      (5, i(43, 8, 9, 0xa122)),
                                      (10, i(35, 8, 2, 0xa128)),
                                      (2, i(9, 0, 31, 1))):
            with self.subTest(position=position):
                words = shared_base_words()
                words[position] = replacement
                self.assert_unknown(self.analyze(words))

    def test_zero_register_is_immutable_and_unknown_skipped_code_is_not_silently_accepted(self):
        words = [i(15, 0, 0, 7), *shared_base_words()]
        result = self.analyze(words)
        self.assertEqual(result["status"], "INTERPRETED")
        self.assertEqual(result["large_base_site_count"], 1)
        words = shared_base_words() + [0x44020000]
        self.assert_unknown(self.analyze(words))

    def test_loads_kill_return_provenance_but_cannot_overwrite_zero(self):
        words = shared_base_words()
        words[10] = i(35, 8, 31, 0xa124)
        words[11] = i(5, 31, 0, 3)
        self.assert_unknown(self.analyze(words))
        words = shared_base_words()
        words[10] = i(35, 8, 0, 0xa124)
        words[11] = i(5, 3, 0, 3)
        words.insert(11, r(8, 0, 8, 0x21))
        result = self.analyze(words)
        self.assertEqual(result["status"], "INTERPRETED")
        self.assertEqual(result["large_base_site_count"], 1)

    def test_state_and_path_limits_and_invalid_lengths_fail_without_counts(self):
        for kwargs in ({"max_states": 1}, {"max_paths": 1}):
            with self.subTest(kwargs=kwargs):
                self.assert_unknown(self.analyze(shared_base_words(), **kwargs))
        for code in (b"", b"\0", bytes(516)):
            with self.subTest(length=len(code)):
                self.assert_unknown(reuse.analyze_address_paths(code, OFFSETS))

    def test_full_object_validation_precedes_address_analysis_and_preserves_all_code_bytes(self):
        raw = fixture(shared_base_words())
        result = reuse.inspect_address_fixture(bytes(raw), MEMBER, OFFSETS)
        self.assertEqual(result["sha256"], sha(raw))
        self.assertEqual(result["function"]["size"], 68)
        self.assertEqual(result["address_analysis"]["status"], "INTERPRETED")
        self.assertEqual(bytes.fromhex(result["function"]["bytes_hex"]), struct.pack("<17I", *shared_base_words()))
        for offset, fmt, value in ((16, "<H", 2), (SYMOFF + 16 + 8, "<I", 0),
                                    (SYMOFF + 16 + 4, "<I", 4),
                                    (SHOFF + 2 * 40 + 8, "<I", 2)):
            with self.subTest(offset=offset):
                bad = bytearray(raw)
                struct.pack_into(fmt, bad, offset, value)
                with self.assertRaises(ValueError):
                    reuse.inspect_address_fixture(bad, MEMBER, OFFSETS)
        bad = fixture()
        struct.pack_into("<I", bad, SHOFF + 5 * 40 + 20, 8)
        struct.pack_into("<II", bad, 0x280, 0, (1 << 8) | 4)
        with self.assertRaises(ValueError):
            reuse.inspect_address_fixture(bad, MEMBER, OFFSETS)


class AddressRunnerTests(unittest.TestCase):
    def setUp(self):
        self.inherited = inherited.ArchiveRunnerTests(methodName="runTest")
        self.inherited.setUp()
        self.addCleanup(self.inherited.doCleanups)
        self.root = self.inherited.root
        self.pin = self.inherited.parent_fixture.pin
        self.direct = self.inherited.parent_fixture.write("bench/direct.cpp", b"/* Invented direct fixture. */\n")
        self.grouped = self.inherited.parent_fixture.write("bench/grouped.cpp", b"/* Invented grouped fixture. */\n")
        self.path = self.root / "config/reuse.json"
        self.report = self.root / "evidence/reuse-report.json"
        self.config = {"status": "frozen_before_fixture_compilation", "no_fixture_compilation_observed": True,
                       "archive_profile": self.pin(self.inherited.path),
                       "common_flags": ["-nostdinc", "-lang", "c++", "-c"], "optimization": ["-O2"],
                       "object_symbol": MEMBER, "field_offsets": OFFSETS,
                       "defaults": {"lower": 0x1357, "upper": 0x2468}, "word_width": 4,
                       "record_extent": 0x1A128, "declared_trials": 2,
                       "fixtures": [{"id": "direct", "source": self.pin(self.direct)},
                                    {"id": "grouped", "source": self.pin(self.grouped)}],
                       "grouping_only": True, "cached_pointer_or_reference": False}
        self.save()
        patch = mock.patch.object(reuse, "compile_profile", side_effect=self.compile_ok)
        self.compile = patch.start()
        self.addCleanup(patch.stop)

    def save(self):
        self.path.write_text(json.dumps(self.config))

    def compile_ok(self, profile, source, output, flags, **kwargs):
        self.assertFalse(output.exists())
        self.assertEqual(profile["id"], "mwccpsp_3_0_1_219")
        self.assertEqual(profile["common_flags"], ["-nostdinc", "-lang", "c++", "-c"])
        self.assertEqual(flags, ["-O2"])
        self.assertIn(source, (self.direct, self.grouped))
        output.write_bytes(fixture(repeated_base_words() if source == self.direct else shared_base_words()))
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def run_trial(self):
        return reuse.run_address_reuse(root=self.root, config_path=self.path, report_path=self.report)

    def test_both_complete_functions_and_interpreted_static_metrics_are_reported_separately(self):
        report, directory = self.run_trial()
        self.assertEqual(self.compile.call_count, 2)
        self.assertEqual([row["outcome"] for row in report["fixtures"]], ["OBJECT_VALIDATED"] * 2)
        self.assertEqual(report["function_comparison"]["direct_size"], 100)
        self.assertEqual(report["function_comparison"]["grouped_size"], 68)
        self.assertFalse(report["function_comparison"]["identical"])
        self.assertEqual(report["address_comparison"], {"status": "INTERPRETED", "static_site_reduction": 4})
        self.assertEqual(report["matched_progress"], 0)
        self.assertEqual(len(list(directory.glob("*.o"))), 2)
        self.assertEqual(json.loads(self.report.read_text()), report)

    def test_repeat_uses_four_new_object_paths_and_identical_reports(self):
        first, a = self.run_trial()
        raw = self.report.read_bytes()
        second, b = self.run_trial()
        self.assertNotEqual(a, b)
        self.assertEqual(first, second)
        self.assertEqual(raw, self.report.read_bytes())
        self.assertEqual(len({call.args[2] for call in self.compile.call_args_list}), 4)
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_each_compiler_failure_retains_the_other_case_without_a_zero_or_reuse_advantage(self):
        for failed_source in (self.direct, self.grouped):
            for bad in ("nonzero", "warning", "timeout", "missing", "invalid", "member", "relocation"):
                with self.subTest(failed=failed_source.name, bad=bad):
                    self.report = self.root / "evidence" / (failed_source.stem + bad + ".json")
                    def fail(profile, source, output, flags, **kwargs):
                        if source != failed_source:
                            return self.compile_ok(profile, source, output, flags, **kwargs)
                        if bad == "timeout": raise subprocess.TimeoutExpired("invented", 20)
                        if bad == "missing": return {"returncode": 0, "stdout": "", "stderr": ""}
                        result = self.compile_ok(profile, source, output, flags, **kwargs)
                        if bad == "nonzero": result["returncode"] = 1
                        elif bad == "warning": result["stderr"] = "Warning: invented"
                        elif bad == "invalid": output.write_bytes(b"not ELF")
                        elif bad == "member": output.write_bytes(fixture(symbol="wrong_member"))
                        else:
                            raw = bytearray(output.read_bytes())
                            struct.pack_into("<I", raw, SHOFF + 5 * 40 + 20, 8)
                            struct.pack_into("<II", raw, 0x280, 0, (1 << 8) | 4)
                            output.write_bytes(raw)
                        return result
                    self.compile.side_effect = fail
                    report, _ = self.run_trial()
                    rejected, valid = (report["fixtures"] if failed_source == self.direct else reversed(report["fixtures"]))
                    self.assertEqual(rejected["outcome"], "OUTPUT_REJECTED")
                    self.assertNotIn("observation", rejected)
                    self.assertEqual(valid["outcome"], "OBJECT_VALIDATED")
                    self.assertIsNone(report["function_comparison"])
                    self.assertEqual(report["address_comparison"], {"status": "UNINTERPRETED", "static_site_reduction": None})

    def test_valid_objects_with_unknown_analysis_keep_whole_bytes_but_never_get_an_advantage(self):
        for both_unknown in (False, True):
            with self.subTest(both_unknown=both_unknown):
                self.report = self.root / "evidence" / ("both-unknown.json" if both_unknown else "one-unknown.json")
                def unknown(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if both_unknown or source == self.grouped:
                        words = shared_base_words()
                        words[2] = 0x44020000
                        output.write_bytes(fixture(words))
                    return result
                self.compile.side_effect = unknown
                report, _ = self.run_trial()
                self.assertTrue(all(row["outcome"] == "OBJECT_VALIDATED" for row in report["fixtures"]))
                self.assertIsNotNone(report["function_comparison"])
                self.assertEqual(report["function_comparison"]["identical"], both_unknown)
                self.assertEqual(report["address_comparison"], {"status": "UNINTERPRETED", "static_site_reduction": None})
                result = report["fixtures"][1]["observation"]["address_analysis"]
                self.assertIsNone(result["large_base_site_count"])

    def test_complete_function_padding_is_not_trimmed_even_if_static_analysis_agrees(self):
        def padded(profile, source, output, flags, **kwargs):
            result = self.compile_ok(profile, source, output, flags, **kwargs)
            words = shared_base_words() + ([0] if source == self.grouped else [])
            output.write_bytes(fixture(words))
            return result
        self.compile.side_effect = padded
        report, _ = self.run_trial()
        self.assertFalse(report["function_comparison"]["identical"])
        self.assertEqual(report["function_comparison"]["direct_size"], 68)
        self.assertEqual(report["function_comparison"]["grouped_size"], 72)
        self.assertEqual(report["address_comparison"], {"status": "INTERPRETED", "static_site_reduction": 0})

    def test_unreviewed_third_reordered_cached_or_changed_cases_fail_before_tools(self):
        original = copy.deepcopy(self.config)
        invalid = [("status", "draft"), ("no_fixture_compilation_observed", False),
                   ("common_flags", ["-lang", "c"]), ("optimization", ["-O3"]),
                   ("object_symbol", "other"), ("declared_trials", 3), ("word_width", 2),
                   ("record_extent", 0x1A130), ("cached_pointer_or_reference", True),
                   ("grouping_only", False), ("field_offsets", {"lower": 0x20, "upper": 0x24}),
                   ("defaults", {"lower": 1, "upper": 2}),
                   ("fixtures", list(reversed(original["fixtures"]))),
                   ("fixtures", original["fixtures"] * 2)]
        for field, value in invalid:
            with self.subTest(field=field):
                self.config = copy.deepcopy(original)
                self.config[field] = value
                self.save()
                with self.assertRaises(ValueError): self.run_trial()
                self.compile.assert_not_called()

    def test_mutated_inputs_or_earlier_output_invalidate_outer_report(self):
        old = self.inherited
        paths = (self.path, self.direct, self.grouped, old.path, old.source, old.target,
                 old.naming_source, old.naming_evidence, old.naming_object, old.reference,
                 old.parent_fixture.source, old.parent_fixture.compiler)
        for path in paths:
            with self.subTest(path=path.name, stage="before"):
                before = path.read_bytes()
                path.write_bytes(before + b"changed")
                with self.assertRaises(ValueError): self.run_trial()
                self.compile.assert_not_called()
                path.write_bytes(before)
        for path in paths:
            with self.subTest(path=path.name, stage="after"):
                before = path.read_bytes()
                def mutate(*args, **kwargs):
                    result = self.compile_ok(*args, **kwargs)
                    path.write_bytes(before + b"changed")
                    return result
                self.compile.side_effect = mutate
                with self.assertRaises(ValueError): self.run_trial()
                self.assertFalse(self.report.exists())
                path.write_bytes(before)
        first = []
        def mutate_object(*args, **kwargs):
            result = self.compile_ok(*args, **kwargs)
            if first: first[0].write_bytes(b"changed prior fixture output")
            else: first.append(args[2])
            return result
        self.compile.side_effect = mutate_object
        with self.assertRaises(ValueError): self.run_trial()
        self.assertFalse(self.report.exists())

    def test_new_and_inherited_report_aliases_and_conflicts_preserve_evidence(self):
        old = self.inherited
        paths = (self.path, self.direct, self.grouped, old.path, old.source, old.target,
                 old.naming_source, old.naming_evidence, old.naming_object, old.reference,
                 old.parent_fixture.source, old.parent_fixture.compiler)
        for path in paths:
            with self.subTest(path=path.name):
                self.report = path
                before = path.read_bytes()
                with self.assertRaises(ValueError): self.run_trial()
                self.assertEqual(path.read_bytes(), before)
                self.compile.assert_not_called()
        self.report = self.root / "evidence/conflicting-address-report.json"
        self.report.write_bytes(b"valuable evidence")
        with self.assertRaises(ValueError): self.run_trial()
        self.assertEqual(self.report.read_bytes(), b"valuable evidence")


if __name__ == "__main__":
    unittest.main()
