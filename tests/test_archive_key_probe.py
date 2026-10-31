"""One-function investigation controls with invented bytes and mocked compilation."""

import copy
import hashlib
import json
import struct
import subprocess
import unittest
from unittest import mock

from scripts import bench_archive_key as probe
from scripts.elf32 import Elf32
from tests import test_language_modes as inherited


ADDRESS = 0x0886233C
CANONICAL = "archive_key_initialize"
MEMBER = "initialize_key__17ArchiveKeyContextFUi"
SHOFF = 0x400
SYMOFF = 0x200
CODE = struct.pack("<17I", 0x24020007, *([0] * 14), 0x03e00008, 0)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fixture(*, reference=False, symbol=MEMBER):
    """This invented 68-byte function is unrelated to the original instruction bytes."""
    raw = bytearray(0x700)
    names = b"\0.shstrtab\0.text\0.strtab\0.symtab\0.rel.text\0.comment\0"
    strings = b"\0" + symbol.encode() + b"\0unexpected_function\0"
    raw[0x80:0x80 + len(names)] = names
    raw[0x100:0x100 + len(CODE)] = CODE
    raw[0x180:0x180 + len(strings)] = strings
    comment = b"Invented archive probe\0"
    raw[0x300:0x300 + len(comment)] = comment
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0,
                     b"\x7fELF\x01\x01\x01" + bytes(9), 2 if reference else 1,
                     8, 1, ADDRESS if reference else 0, 0, SHOFF, 0x10970001,
                     52, 0, 0, 40, 7, 1)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (names.index(b".shstrtab"), 3, 0, 0, 0x80, len(names), 0, 0, 1, 0),
                (names.index(b".text"), 1, 6, ADDRESS if reference else 0, 0x100, len(CODE) + 8, 0, 0, 4, 0),
                (names.index(b".strtab"), 3, 0, 0, 0x180, len(strings), 0, 0, 1, 0),
                (names.index(b".symtab"), 2, 0, 0, SYMOFF, 32, 3, 1, 4, 16),
                (names.index(b".rel.text"), 9, 0, 0, 0x280, 0, 4, 2, 4, 8),
                (names.index(b".comment"), 1, 0, 0, 0x300, len(comment), 0, 0, 1, 0)]
    for index, section in enumerate(sections):
        struct.pack_into("<10I", raw, SHOFF + 40 * index, *section)
    struct.pack_into("<IIIBBH", raw, SYMOFF + 16, 1, ADDRESS if reference else 0,
                     len(CODE), 0x12, 0, 2)
    return raw


def manifest():
    return {"schema_version": 1, "source": "bench/candidate.cpp", "probes": [{
        "name": CANONICAL, "address": ADDRESS, "size": len(CODE), "target_sha256": sha(CODE),
        "category": "synthetic", "ownership": "unclassified invented fixture",
        "boundary_evidence": "Invented full function, no original game bytes.", "relocations": []}]}


class ArchiveObjectTests(unittest.TestCase):
    def compare(self, data):
        return probe.compare_archive_object(bytes(data), Elf32(fixture(reference=True)), manifest(), MEMBER)

    def test_complete_member_symbol_is_required_without_renaming_object_bytes(self):
        raw = fixture()
        before = bytes(raw)
        result = self.compare(raw)
        self.assertEqual(bytes(raw), before)
        self.assertEqual(result["object_sha256"], sha(before))
        row = result["comparisons"][0]
        self.assertEqual(row["name"], CANONICAL)
        self.assertEqual(row["object_symbol"], MEMBER)
        self.assertTrue(row["exact_probe_bytes"])
        with self.assertRaises(ValueError):
            self.compare(fixture(symbol="initialize_key__17ArchiveKeyContextFi"))

    def test_short_prefix_or_longer_complete_symbol_cannot_be_reported_exact(self):
        for size in (len(CODE) - 4, len(CODE) + 4):
            with self.subTest(size=size):
                raw = fixture()
                struct.pack_into("<I", raw, SYMOFF + 16 + 8, size)
                row = self.compare(raw)["comparisons"][0]
                self.assertFalse(row["exact_probe_bytes"])
                self.assertEqual(row["compiled_size"], size)

    def test_extra_function_and_unresolved_code_relocation_reject_entire_object(self):
        more_targets = manifest()
        more_targets["probes"] *= 2
        with self.assertRaises(ValueError):
            probe.compare_archive_object(fixture(), Elf32(fixture(reference=True)), more_targets, MEMBER)
        raw = fixture()
        extra_name = 1 + len(MEMBER) + 1
        struct.pack_into("<IIIBBH", raw, SYMOFF + 32, extra_name, len(CODE), 8, 0x12, 0, 2)
        struct.pack_into("<I", raw, SHOFF + 4 * 40 + 20, 48)
        with self.assertRaises(ValueError):
            self.compare(raw)
        raw = fixture()
        struct.pack_into("<I", raw, SHOFF + 5 * 40 + 20, 8)
        struct.pack_into("<II", raw, 0x280, 0, (1 << 8) | 4)
        with self.assertRaises(ValueError):
            self.compare(raw)


class ArchiveRunnerTests(unittest.TestCase):
    def setUp(self):
        # Reuse a fully valid invented 3H input graph; inherited validation is
        # real, not mocked. Only the new experiment's compiler call is replaced.
        self.parent_fixture = inherited.LanguageRunnerTests(methodName="runTest")
        self.parent_fixture.setUp()
        self.addCleanup(self.parent_fixture.doCleanups)
        old = self.parent_fixture
        self.root = old.root
        self.reference = old.reference
        raw = bytearray(self.reference.read_bytes())
        elf = Elf32(raw)
        raw[0xd00:0xd00 + len(CODE)] = CODE
        struct.pack_into("<H", raw, 48, 8)
        struct.pack_into("<10I", raw, inherited.SHOFF + 7 * 40,
                         elf.sections[2]["name_offset"], 1, 6, ADDRESS, 0xd00, len(CODE), 0, 0, 4, 0)
        self.reference.write_bytes(raw)
        lock = json.loads(old.reference_lock.read_bytes())
        lock["decrypted_executable"] = old.pin(self.reference)
        old.reference_lock.write_text(json.dumps(lock))
        old.families["reference_lock"] = old.pin(old.reference_lock)
        old.family_path.write_text(json.dumps(old.families))
        old.spec["compiler_families"] = old.pin(old.family_path)
        old.spec_path.write_text(json.dumps(old.spec))
        old.evidence["spec_sha256"] = old.pin(old.spec_path)["sha256"]
        old.evidence_path.write_text(json.dumps(old.evidence))
        old.config.update(reference_lock=old.pin(old.reference_lock), family_profiles=old.pin(old.family_path),
                          naming_spec=old.pin(old.spec_path), naming_evidence=old.pin(old.evidence_path))
        old.save()
        self.source = old.write("bench/candidate.cpp", b"/* Invented one-candidate source. */\n")
        self.target = old.write("config/key-target.json", json.dumps(manifest()).encode())
        self.naming_source = old.write("bench/member-naming.cpp", b"/* Invented member signature. */\n")
        self.naming_object = old.write("build/member-naming.o", fixture())
        self.naming = {"source": old.pin(self.naming_source), "object": old.pin(self.naming_object),
                       "flags": ["-nostdinc", "-lang", "c++", "-c", "-O2"],
                       "object_symbol": MEMBER, "canonical_name": CANONICAL, "diagnostic": ""}
        self.naming_evidence = old.write("evidence/member-naming.json", json.dumps(self.naming).encode())
        self.hypothesis_data = {"source": old.pin(self.source), "target_manifest": old.pin(self.target),
                                "naming_fixture": old.pin(self.naming_source), "attempt_count": 1,
                                "matching_tricks": 0}
        self.hypothesis = old.write("evidence/key-hypothesis.json", json.dumps(self.hypothesis_data).encode())
        self.config = {"status": "frozen_before_archive_candidate_compilation",
                       "no_archive_candidate_compilation_observed": True,
                       "language_profile": old.pin(old.path), "source": old.pin(self.source),
                       "target_manifest": old.pin(self.target), "source_hypothesis": old.pin(self.hypothesis),
                       "naming_source": old.pin(self.naming_source), "naming_evidence": old.pin(self.naming_evidence),
                       "naming_object": old.pin(self.naming_object),
                       "common_flags": ["-nostdinc", "-lang", "c++", "-c"], "optimization": ["-O2"],
                       "canonical_name": CANONICAL, "object_symbol": MEMBER,
                       "target_address": ADDRESS, "target_size": len(CODE),
                       "declared_trials": 2, "source_attempts": 1}
        self.path = old.write("config/key-experiment.json", json.dumps(self.config).encode())
        self.report = self.root / "evidence/key-report.json"
        patch = mock.patch.object(probe, "compile_profile", side_effect=self.compile_ok)
        self.compile = patch.start()
        self.addCleanup(patch.stop)

    def save(self):
        self.path.write_text(json.dumps(self.config))

    def compile_ok(self, profile, source, output, flags, **kwargs):
        self.assertFalse(output.exists(), "Do not reuse an object from an earlier trial")
        self.assertEqual(profile["id"], "mwccpsp_3_0_1_219")
        self.assertEqual(profile["common_flags"], ["-nostdinc", "-lang", "c++", "-c"])
        self.assertEqual(source, self.source)
        self.assertEqual(flags, ["-O2"])
        output.write_bytes(fixture())
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def run_trial(self):
        return probe.run_archive_key(root=self.root, config_path=self.path, report_path=self.report)

    def test_exact_single_complete_member_is_diagnostic_only(self):
        report, directory = self.run_trial()
        self.compile.assert_called_once()
        self.assertEqual(report["outcome"], "COMPLETE")
        self.assertEqual(report["exact_probes"], 1)
        self.assertEqual(report["matched_progress"], 0)
        self.assertEqual(len(report["comparisons"]), 1)
        self.assertEqual(report["comparisons"][0]["object_symbol"], MEMBER)
        self.assertEqual(len(list(directory.glob("*.o"))), 1)
        self.assertEqual(json.loads(self.report.read_text()), report)

    def test_fresh_repeat_object_paths_produce_identical_pathfree_reports(self):
        first, a = self.run_trial()
        raw = self.report.read_bytes()
        second, b = self.run_trial()
        self.assertNotEqual(a, b)
        self.assertEqual(first, second)
        self.assertEqual(raw, self.report.read_bytes())
        self.assertEqual(len({call.args[2] for call in self.compile.call_args_list}), 2)
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_changed_function_bytes_remain_a_complete_nonexact_result(self):
        def change(*args, **kwargs):
            result = self.compile_ok(*args, **kwargs)
            output = args[2]
            raw = bytearray(output.read_bytes())
            raw[0x100] ^= 1
            output.write_bytes(raw)
            return result
        self.compile.side_effect = change
        report, _ = self.run_trial()
        self.assertEqual(report["outcome"], "COMPLETE")
        self.assertEqual(report["exact_probes"], 0)
        self.assertEqual(report["comparisons"][0]["first_difference"], 0)

    def test_nonzero_warning_timeout_missing_invalid_extra_and_relocated_objects_never_score(self):
        for bad in ("nonzero", "warning", "timeout", "missing", "invalid", "extra", "relocation", "alias"):
            with self.subTest(bad=bad):
                self.report = self.root / "evidence" / (bad + ".json")
                def fail(*args, **kwargs):
                    if bad == "timeout": raise subprocess.TimeoutExpired("invented", 20)
                    if bad == "missing": return {"returncode": 0, "stdout": "", "stderr": ""}
                    result = self.compile_ok(*args, **kwargs)
                    output = args[2]
                    raw = bytearray(output.read_bytes())
                    if bad == "nonzero": result["returncode"] = 1
                    elif bad == "warning": result["stderr"] = "Warning: invented"
                    elif bad == "invalid": raw = b"not ELF"
                    elif bad == "alias": raw = fixture(symbol="wrong_member")
                    elif bad == "extra":
                        struct.pack_into("<IIIBBH", raw, SYMOFF + 32, 1, 0, 4, 0x12, 0, 2)
                        struct.pack_into("<I", raw, SHOFF + 4 * 40 + 20, 48)
                    else:
                        struct.pack_into("<I", raw, SHOFF + 5 * 40 + 20, 8)
                        struct.pack_into("<II", raw, 0x280, 0, (1 << 8) | 4)
                    output.write_bytes(raw)
                    return result
                self.compile.side_effect = fail
                report, _ = self.run_trial()
                self.assertEqual(report["outcome"], "REJECTED_NO_SCORE")
                self.assertEqual(report["comparisons"], [])
                self.assertNotIn("exact_probes", report)

    def test_unreviewed_flags_function_extent_and_attempt_count_fail_before_compile(self):
        original = copy.deepcopy(self.config)
        invalid = [("status", "draft"), ("no_archive_candidate_compilation_observed", False),
                   ("common_flags", ["-nostdinc", "-lang", "c", "-c"]),
                   ("optimization", ["-O3"]), ("source_attempts", 2), ("declared_trials", 3),
                   ("target_address", ADDRESS + 4), ("target_size", len(CODE) - 4),
                   ("canonical_name", "other"), ("object_symbol", "other_member")]
        for field, value in invalid:
            with self.subTest(field=field):
                self.config = copy.deepcopy(original)
                self.config[field] = value
                self.save()
                with self.assertRaises(ValueError): self.run_trial()
                self.compile.assert_not_called()

    def test_forged_hypothesis_and_naming_bindings_fail_even_with_updated_file_pins(self):
        old = self.parent_fixture
        for field, value in (("attempt_count", 2), ("matching_tricks", 1),
                             ("source", old.pin(self.naming_source))):
            with self.subTest(field=field):
                before = self.hypothesis.read_bytes()
                value_hypothesis = dict(self.hypothesis_data, **{field: value})
                self.hypothesis.write_text(json.dumps(value_hypothesis))
                self.config["source_hypothesis"] = old.pin(self.hypothesis)
                self.save()
                with self.assertRaises(ValueError): self.run_trial()
                self.compile.assert_not_called()
                self.hypothesis.write_bytes(before)
        self.config["source_hypothesis"] = old.pin(self.hypothesis)
        for field, value in (("object_symbol", "wrong_member"), ("canonical_name", "wrong"),
                             ("diagnostic", "Warning: invented"), ("flags", ["-O3"])):
            with self.subTest(field=field):
                before = self.naming_evidence.read_bytes()
                self.naming_evidence.write_text(json.dumps(dict(self.naming, **{field: value})))
                self.config["naming_evidence"] = old.pin(self.naming_evidence)
                self.save()
                with self.assertRaises(ValueError): self.run_trial()
                self.compile.assert_not_called()
                self.naming_evidence.write_bytes(before)

    def test_rehashed_naming_object_still_requires_the_exact_observed_member(self):
        old = self.parent_fixture
        self.naming_object.write_bytes(fixture(symbol="wrong_member"))
        self.config["naming_object"] = old.pin(self.naming_object)
        self.naming["object"] = self.config["naming_object"]
        self.naming_evidence.write_text(json.dumps(self.naming))
        self.config["naming_evidence"] = old.pin(self.naming_evidence)
        self.save()
        with self.assertRaises(ValueError):
            self.run_trial()
        self.compile.assert_not_called()

    def test_inputs_and_profiles_are_pinned_before_and_after_compilation(self):
        old = self.parent_fixture
        paths = (self.source, self.target, self.hypothesis, self.naming_source, self.naming_evidence,
                 self.naming_object, old.path, old.source, old.family_path, old.reference_lock,
                 self.reference, old.compiler, old.runner, old.support, old.timeout)
        for path in paths:
            with self.subTest(path=path.name, stage="before"):
                before = path.read_bytes()
                path.write_bytes(before + b"changed")
                with self.assertRaises(ValueError): self.run_trial()
                self.compile.assert_not_called()
                path.write_bytes(before)
        for path in (*paths, self.path):
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

    def test_changed_emitted_object_invalidates_the_outer_report(self):
        real_compare = probe.compare_archive_object
        def mutate(data, reference, target, symbol):
            result = real_compare(data, reference, target, symbol)
            self.compile.call_args.args[2].write_bytes(b"changed after comparison")
            return result
        with mock.patch.object(probe, "compare_archive_object", side_effect=mutate):
            with self.assertRaises(ValueError): self.run_trial()
        self.assertFalse(self.report.exists())

    def test_report_aliases_and_conflicts_preserve_new_and_inherited_inputs(self):
        old = self.parent_fixture
        for path in (self.path, self.source, self.target, self.hypothesis, self.naming_source,
                     self.naming_evidence, self.naming_object, old.path, old.source, self.reference,
                     old.family_path, old.compiler, old.runner, old.support):
            with self.subTest(path=path.name):
                self.report = path
                before = path.read_bytes()
                with self.assertRaises(ValueError): self.run_trial()
                self.assertEqual(path.read_bytes(), before)
                self.compile.assert_not_called()
        self.report = self.root / "evidence/valuable-report.json"
        self.report.write_bytes(b"valuable evidence")
        with self.assertRaises(ValueError): self.run_trial()
        self.assertEqual(self.report.read_bytes(), b"valuable evidence")


if __name__ == "__main__":
    unittest.main()
