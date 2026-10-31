"""Six source-experiment controls with invented target/object bytes and mocked GCC/MW calls."""

import copy
import json
import struct
import subprocess
import unittest
from unittest import mock

from scripts import bench_archive_pointer as experiment
from tests import test_archive_key_probe as invented


class ArchivePointerTests(unittest.TestCase):
    def setUp(self):
        self.old = invented.ArchiveRunnerTests(methodName="runTest")
        self.old.setUp()
        self.addCleanup(self.old.doCleanups)
        self.root, self.parent = self.old.root, self.old.parent_fixture
        self.pin = self.parent.pin
        self.grouped = self.parent.write("bench/archive-grouped.cpp", b"/* Invented grouped source. */\n")
        self.pointer = self.parent.write("bench/archive-pointer.cpp", b"/* Invented pointer source. */\n")
        self.object = bytes(invented.fixture())
        self.history = self.parent.write("build/archive-history.o", self.object)
        self.path = self.root / "config/archive-pointer.json"
        self.report = self.root / "evidence/archive-pointer.json"
        self.config = {"status": "frozen_before_source_compilation", "archive_profile": self.pin(self.old.path),
            "historical_object": self.pin(self.history), "common_flags": ["-nostdinc", "-lang", "c++", "-c"],
            "optimization": ["-O2"], "object_symbol": invented.MEMBER,
            "field_offsets": {"lower": 0x2f53c, "upper": 0x2f540},
            "defaults": {"lower": 0x7f8d, "upper": 0x2345}, "declared_trials": 2, "plain_source_budget": 3,
            "forms": [{"id": "flat", "attempt": 1, "source": self.pin(self.old.source)},
                      {"id": "grouped", "attempt": 2, "source": self.pin(self.grouped)},
                      {"id": "pointer", "attempt": 3, "source": self.pin(self.pointer)}]}
        self.save()
        self.outputs = []
        patcher = mock.patch.object(experiment.archive, "compile_profile", side_effect=self.compile_ok)
        self.compile = patcher.start()
        self.addCleanup(patcher.stop)

    def save(self):
        self.path.write_text(json.dumps(self.config))

    def compile_ok(self, profile, source, output, flags, **kwargs):
        self.assertFalse(output.exists(), "Each declared form requires a fresh object")
        self.assertEqual(profile["id"], "mwccpsp_3_0_1_219")
        self.assertEqual(profile["common_flags"], ["-nostdinc", "-lang", "c++", "-c"])
        self.assertEqual(flags, ["-O2"])
        self.assertIn(source, (self.old.source, self.grouped, self.pointer))
        self.outputs.append(output)
        output.write_bytes(self.object)
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def trial(self):
        return experiment.run_archive_pointer(root=self.root, config_path=self.path, report_path=self.report)

    def test_fixed_three_forms_repeat_freshly_and_do_not_modify_the_original_attempt(self):
        original = self.old.path.read_bytes(), self.old.source.read_bytes()
        first, a = self.trial()
        self.report = self.root / "evidence/repeat.json"
        second, b = self.trial()
        self.assertEqual(first, second)
        self.assertNotEqual(a, b)
        self.assertEqual(len(set(self.outputs)), 6)
        self.assertEqual(first["status"], "ARCHIVE_POINTER_INVESTIGATION_COMPLETE")
        self.assertEqual([(x["id"], x["attempt"]) for x in first["forms"]], [("flat", 1), ("grouped", 2), ("pointer", 3)])
        self.assertTrue(all(x["outcome"] == "COMPLETE" and len(x["comparisons"]) == 1 for x in first["forms"]))
        self.assertEqual(first["attempted_source_count"], 3)
        self.assertTrue(first["plain_source_budget_exhausted"])
        self.assertEqual(first["matched_progress"], 0)
        self.assertNotIn(str(self.root), json.dumps(first))
        self.assertEqual((self.old.path.read_bytes(), self.old.source.read_bytes()), original)
        self.assertEqual(json.loads(original[0])["source_attempts"], 1)
        for row in first["forms"]:
            result = row["comparisons"][0]
            self.assertEqual((result["address"], result["target_size"], result["object_symbol"]),
                             (invented.ADDRESS, 68, invented.MEMBER))

    def test_equal_length_wrong_bytes_and_short_or_long_prefixes_never_become_exact(self):
        for size in (64, 72):
            with self.subTest(size=size):
                self.report = self.root / "evidence" / f"size-{size}.json"
                def changed(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    raw = bytearray(self.object)
                    if source == self.grouped:
                        raw[0x100] ^= 1
                    elif source == self.pointer:
                        struct.pack_into("<I", raw, invented.SYMOFF + 16 + 8, size)
                    output.write_bytes(raw); return result
                self.compile.side_effect = changed
                report, _ = self.trial()
                grouped, pointer = report["forms"][1:]
                self.assertFalse(grouped["comparisons"][0]["exact_probe_bytes"])
                self.assertEqual(grouped["comparisons"][0]["compiled_size"], 68)
                self.assertEqual(grouped["comparisons"][0]["first_difference"], 0)
                self.assertFalse(pointer["comparisons"][0]["exact_probe_bytes"])
                self.assertEqual(pointer["comparisons"][0]["compiled_size"], size)
                self.assertEqual(pointer["comparisons"][0]["first_difference"], min(size, 68))
                self.assertFalse(pointer["full_word_difference"]["identical"])
                tail = pointer["full_word_difference"]["word_differences"][-1]
                self.assertEqual(tail["offset"], min(size, 68))
                self.assertIsNone(tail["candidate_bytes_hex"] if size < 68 else tail["control_bytes_hex"])
                self.assertEqual(report["matched_progress"], 0)

    def test_scope_budget_target_extent_and_inherited_original_bindings_fail_before_compile(self):
        original = copy.deepcopy(self.config)
        invalid = [("status", "draft"), ("optimization", ["-O3"]), ("common_flags", ["-lang", "c"]),
                   ("plain_source_budget", 4), ("declared_trials", 3), ("object_symbol", "different_member"),
                   ("field_offsets", {"lower": 1, "upper": 5}), ("defaults", {"lower": 1, "upper": 2}),
                   ("forms", list(reversed(original["forms"]))), ("forms", original["forms"] * 2)]
        for key, value in invalid:
            self.config = copy.deepcopy(original); self.config[key] = value; self.save()
            with self.subTest(key=key), self.assertRaises(ValueError): self.trial()
            self.compile.assert_not_called()
        self.config = copy.deepcopy(original)
        changed = copy.deepcopy(original); changed["forms"][1]["attempt"] = 3
        self.config = changed; self.save()
        with self.assertRaises(ValueError): self.trial()
        self.compile.assert_not_called()
        old = json.loads(self.old.path.read_bytes()); old["target_size"] = 64
        self.old.path.write_text(json.dumps(old)); self.config = copy.deepcopy(original)
        self.config["archive_profile"] = self.pin(self.old.path); self.save()
        with self.assertRaises(ValueError): self.trial()
        self.compile.assert_not_called()

    def test_baseline_drift_stops_forms_but_failed_alternative_keeps_the_other_declared_case(self):
        for failure in ("baseline_byte", "baseline_nonzero", "warning", "missing", "timeout_partial", "relocation", "member"):
            with self.subTest(failure=failure):
                self.report = self.root / "evidence" / (failure + ".json"); self.compile.reset_mock()
                def fail(profile, source, output, flags, **kwargs):
                    failed = source == (self.old.source if failure.startswith("baseline") else self.grouped)
                    if failed and failure == "missing": return {"returncode": 0, "stdout": "", "stderr": ""}
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if not failed: return result
                    if failure == "baseline_byte":
                        raw = bytearray(self.object); raw[-1] ^= 1; output.write_bytes(raw)
                    elif failure == "baseline_nonzero": result["returncode"] = 1
                    elif failure == "warning": result["stderr"] = "Warning: invented"
                    elif failure == "timeout_partial": raise subprocess.TimeoutExpired("invented", 20)
                    elif failure == "member": output.write_bytes(invented.fixture(symbol="wrong_member"))
                    else:
                        raw = bytearray(self.object)
                        struct.pack_into("<I", raw, invented.SHOFF + 5 * 40 + 20, 8)
                        struct.pack_into("<II", raw, 0x280, 0, (1 << 8) | 4); output.write_bytes(raw)
                    return result
                self.compile.side_effect = fail
                report, _ = self.trial()
                self.assertEqual(report["status"], "ARCHIVE_POINTER_INVESTIGATION_INCOMPLETE")
                if failure.startswith("baseline"):
                    self.assertEqual(len(report["forms"]), 1); self.compile.assert_called_once()
                    self.assertEqual(report["attempted_source_count"], 1)
                    self.assertFalse(report["plain_source_budget_exhausted"])
                    rejected = report["forms"][0]
                else:
                    self.assertEqual(len(report["forms"]), 3)
                    self.assertEqual(report["forms"][2]["outcome"], "COMPLETE")
                    self.assertEqual(report["attempted_source_count"], 3)
                    rejected = report["forms"][1]
                self.assertNotIn("comparisons", rejected)
                self.assertNotIn("observation", rejected)
                self.assertNotIn("full_word_difference", rejected)
                if failure == "timeout_partial": self.assertEqual(rejected["object_sha256"], invented.sha(self.object))

    def test_source_reference_tools_or_retained_failure_output_mutation_prevents_publication(self):
        paths = (self.path, self.old.source, self.grouped, self.pointer, self.history, self.old.path,
                 self.old.target, self.old.naming_object, self.old.reference, self.parent.compiler, self.parent.timeout)
        for path in paths:
            before = path.read_bytes()
            with self.subTest(path=path, stage="before"):
                path.write_bytes(before + b"changed")
                try:
                    with self.assertRaises(ValueError): self.trial()
                    self.compile.assert_not_called()
                finally: path.write_bytes(before)
        for path in (self.path, self.grouped, self.old.reference, self.parent.compiler):
            before = path.read_bytes()
            with self.subTest(path=path, stage="after"):
                def mutate(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    path.write_bytes(before + b"changed"); return result
                self.compile.side_effect = mutate
                try:
                    with self.assertRaises(ValueError): self.trial()
                    self.assertFalse(self.report.exists())
                finally: path.write_bytes(before)
        for timeout in (False, True):
            with self.subTest(timeout=timeout):
                self.outputs = []
                def replace(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if source == self.grouped and timeout: raise subprocess.TimeoutExpired("invented", 20)
                    if source == self.pointer: self.outputs[1].write_bytes(b"replaced retained output")
                    return result
                self.compile.side_effect = replace
                with self.assertRaisesRegex(ValueError, "output changed"):
                    self.trial()
                self.assertFalse(self.report.exists())

    def test_report_aliases_or_conflicts_fail_before_new_builds_or_compilation(self):
        before_dirs = set((self.root / "build").glob("archive-pointer-*"))
        for path in (self.path, self.old.source, self.grouped, self.pointer, self.history, self.old.path,
                     self.old.target, self.old.reference, self.parent.compiler):
            self.report = path; before = path.read_bytes()
            with self.subTest(path=path), self.assertRaises(ValueError): self.trial()
            self.compile.assert_not_called(); self.assertEqual(path.read_bytes(), before)
        self.report = self.parent.write("evidence/conflict.json", b"retained evidence")
        with self.assertRaises(ValueError): self.trial()
        self.compile.assert_not_called()
        self.assertEqual(self.report.read_bytes(), b"retained evidence")
        self.assertEqual(set((self.root / "build").glob("archive-pointer-*")), before_dirs)


if __name__ == "__main__":
    unittest.main()
