"""Seven integration controls using invented objects; compilation is mocked."""

import copy
import json
import struct
import subprocess
import unittest
from unittest import mock

from scripts import bench_pointer_reuse as pointer
from tests import test_address_reuse as invented


class PointerReuseTests(unittest.TestCase):
    def setUp(self):
        # Exercise the real inherited 3J/archive/language/family graph.
        self.old = invented.AddressRunnerTests(methodName="runTest")
        self.old.setUp()
        self.addCleanup(self.old.doCleanups)
        self.root, self.pin = self.old.root, self.old.pin
        self.parent = self.old.inherited.parent_fixture
        self.grouped = self.old.grouped
        self.source = self.parent.write("bench/pointer.cpp", b"/* Invented pointer fixture. */\n")
        self.control_bytes = bytes(invented.fixture(invented.repeated_base_words()))
        self.pointer_bytes = bytes(invented.fixture(invented.shared_base_words()))
        self.history = self.parent.write("build/historical-grouped.o", self.control_bytes)
        self.path = self.root / "config/pointer.json"
        self.report = self.root / "evidence/pointer-report.json"
        self.config = {"status": "frozen_before_fixture_compilation", "grouping_profile": self.pin(self.old.path),
            "historical_control": self.pin(self.history), "common_flags": ["-nostdinc", "-lang", "c++", "-c"],
            "optimization": ["-O2"], "object_symbol": invented.MEMBER, "field_offsets": invented.OFFSETS,
            "defaults": {"lower": 0x1357, "upper": 0x2468}, "declared_trials": 2, "named_pointer_only": True,
            "fixtures": [{"id": "grouped", "source": self.pin(self.grouped)},
                         {"id": "pointer", "source": self.pin(self.source)}]}
        self.save()
        self.outputs = []
        patcher = mock.patch.object(pointer.address, "compile_profile", side_effect=self.compile_ok)
        self.compile = patcher.start()
        self.addCleanup(patcher.stop)

    def save(self):
        self.path.write_text(json.dumps(self.config))

    def compile_ok(self, profile, source, output, flags, **kwargs):
        self.assertFalse(output.exists(), "No stale object may enter a trial")
        self.assertEqual(flags, ["-O2"])
        self.assertEqual(profile["common_flags"], ["-nostdinc", "-lang", "c++", "-c"])
        self.assertEqual(profile["id"], "mwccpsp_3_0_1_219")
        self.assertIn(source, (self.grouped, self.source))
        self.outputs.append(output)
        output.write_bytes(self.control_bytes if source == self.grouped else self.pointer_bytes)
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def trial(self):
        return pointer.run_pointer_reuse(root=self.root, config_path=self.path, report_path=self.report)

    def test_fixed_pair_and_fresh_repeat_keep_complete_bytes_separate_from_static_metrics(self):
        before = self.old.path.read_bytes()
        first, a = self.trial()
        self.report = self.root / "evidence/repeat.json"
        second, b = self.trial()
        self.assertEqual(first, second)
        self.assertNotEqual(a, b)
        self.assertEqual(len(set(self.outputs)), 4)
        self.assertEqual(first["status"], "POINTER_REUSE_INVESTIGATION_COMPLETE")
        self.assertEqual([x["id"] for x in first["fixtures"]], ["grouped", "pointer"])
        self.assertTrue(all(x["outcome"] == "OBJECT_VALIDATED" for x in first["fixtures"]))
        self.assertEqual((first["function_comparison"]["grouped_size"], first["function_comparison"]["pointer_size"]), (100, 68))
        self.assertFalse(first["function_comparison"]["identical"])
        self.assertEqual(first["address_comparison"], {"status": "INTERPRETED", "static_site_reduction": 4})
        self.assertEqual(first["matched_progress"], 0)
        self.assertNotIn(str(self.root), json.dumps(first))
        self.assertEqual(self.old.path.read_bytes(), before)
        self.assertFalse(json.loads(before)["cached_pointer_or_reference"])

    def test_new_scope_and_old_no_pointer_scope_are_both_enforced_before_compile(self):
        original = copy.deepcopy(self.config)
        invalid = [("status", "draft"), ("optimization", ["-O3"]), ("common_flags", ["-lang", "c"]),
                   ("object_symbol", "different_member"), ("declared_trials", 3), ("named_pointer_only", False),
                   ("field_offsets", {"lower": 0x20, "upper": 0x24}), ("defaults", {"lower": 1, "upper": 2}),
                   ("fixtures", list(reversed(original["fixtures"]))), ("fixtures", original["fixtures"] * 2)]
        for key, value in invalid:
            self.config = copy.deepcopy(original); self.config[key] = value; self.save()
            with self.subTest(key=key), self.assertRaises(ValueError): self.trial()
            self.compile.assert_not_called()
        self.config = copy.deepcopy(original)
        old_raw = self.old.path.read_bytes(); old = json.loads(old_raw); old["cached_pointer_or_reference"] = True
        self.old.path.write_text(json.dumps(old)); self.config["grouping_profile"] = self.pin(self.old.path); self.save()
        with self.assertRaises(ValueError): self.trial()
        self.compile.assert_not_called()
        self.old.path.write_bytes(old_raw)

    def test_rejected_or_uninterpreted_pointer_cannot_manufacture_an_address_advantage(self):
        for failure in ("nonzero", "warning", "timeout", "timeout_partial", "missing", "invalid", "member", "relocation", "unknown"):
            with self.subTest(failure=failure):
                self.report = self.root / "evidence" / (failure + ".json")
                def fail(profile, source, output, flags, **kwargs):
                    if source == self.grouped: return self.compile_ok(profile, source, output, flags, **kwargs)
                    if failure == "timeout": raise subprocess.TimeoutExpired("invented", 20)
                    if failure == "missing": return {"returncode": 0, "stdout": "", "stderr": ""}
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if failure == "timeout_partial": raise subprocess.TimeoutExpired("invented", 20)
                    if failure == "nonzero": result["returncode"] = 1
                    elif failure == "warning": result["stderr"] = "Warning: invented"
                    elif failure == "invalid": output.write_bytes(b"not ELF")
                    elif failure == "member": output.write_bytes(invented.fixture(symbol="wrong_member"))
                    elif failure == "relocation":
                        raw = bytearray(self.pointer_bytes)
                        struct.pack_into("<I", raw, invented.SHOFF + 5 * 40 + 20, 8)
                        struct.pack_into("<II", raw, 0x280, 0, (1 << 8) | 4); output.write_bytes(raw)
                    else:
                        words = invented.shared_base_words(); words[2] = 0x44020000
                        output.write_bytes(invented.fixture(words))
                    return result
                self.compile.side_effect = fail
                report, _ = self.trial()
                self.assertEqual(len(report["fixtures"]), 2)
                self.assertEqual(report["fixtures"][0]["outcome"], "OBJECT_VALIDATED")
                self.assertEqual(report["address_comparison"], {"status": "UNINTERPRETED", "static_site_reduction": None})
                if failure == "unknown":
                    self.assertEqual(report["fixtures"][1]["outcome"], "OBJECT_VALIDATED")
                    self.assertIsNotNone(report["function_comparison"])
                else:
                    self.assertEqual(report["fixtures"][1]["outcome"], "OUTPUT_REJECTED")
                    self.assertNotIn("observation", report["fixtures"][1])
                    self.assertIsNone(report["function_comparison"])
                    if failure == "timeout_partial":
                        self.assertEqual(report["fixtures"][1]["object_sha256"], invented.sha(self.pointer_bytes))

    def test_entire_historical_object_drift_or_failed_baseline_stops_before_pointer(self):
        for failure in ("unused_byte_drift", "nonzero", "warning", "timeout_partial"):
            with self.subTest(failure=failure):
                self.report = self.root / "evidence" / (failure + ".json")
                self.compile.reset_mock()
                def drift(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if failure == "unused_byte_drift":
                        raw = bytearray(output.read_bytes()); raw[-1] ^= 1; output.write_bytes(raw)
                    elif failure == "nonzero": result["returncode"] = 1
                    elif failure == "timeout_partial": raise subprocess.TimeoutExpired("invented", 20)
                    else: result["stderr"] = "Warning: invented"
                    return result
                self.compile.side_effect = drift
                report, _ = self.trial()
                self.compile.assert_called_once()
                self.assertEqual(len(report["fixtures"]), 1)
                self.assertEqual(report["status"], "POINTER_REUSE_INVESTIGATION_INCOMPLETE")
                self.assertIsNone(report["function_comparison"])
                self.assertIsNone(report["address_comparison"]["static_site_reduction"])
                if failure == "unused_byte_drift": self.assertEqual(report["fixtures"][0]["outcome"], "CONTROL_MISMATCH")
                if failure == "timeout_partial":
                    self.assertEqual(report["fixtures"][0]["object_sha256"], invented.sha(self.control_bytes))
                    self.assertNotIn("observation", report["fixtures"][0])

    def test_retained_valid_and_exception_partial_outputs_are_checked_at_publication(self):
        for stage in ("earlier_valid", "baseline_timeout", "pointer_timeout"):
            with self.subTest(stage=stage):
                self.outputs = []; self.report = self.root / "evidence" / (stage + ".json")
                def emit(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if stage == "earlier_valid" and source == self.source:
                        self.outputs[0].write_bytes(b"replacement baseline")
                    if (stage == "baseline_timeout" and source == self.grouped
                            or stage == "pointer_timeout" and source == self.source):
                        raise subprocess.TimeoutExpired("invented", 20)
                    return result
                self.compile.side_effect = emit
                real_verify, calls = pointer.verify_pointer_inputs, []
                def verified(*args):
                    result = real_verify(*args); calls.append(True)
                    if len(calls) == 2 and stage != "earlier_valid": self.outputs[-1].write_bytes(b"changed partial")
                    return result
                with mock.patch.object(pointer, "verify_pointer_inputs", side_effect=verified):
                    with self.assertRaisesRegex(ValueError, "object changed"):
                        self.trial()
                self.assertFalse(self.report.exists())

    def test_before_and_after_input_pin_mutations_fail_without_outer_report(self):
        paths = (self.path, self.grouped, self.source, self.history, self.old.path,
                 self.old.inherited.path, self.old.inherited.source, self.old.inherited.reference,
                 self.parent.compiler, self.parent.timeout)
        for path in paths:
            before = path.read_bytes()
            with self.subTest(path=path, stage="before"):
                path.write_bytes(before + b"changed")
                try:
                    with self.assertRaises(ValueError): self.trial()
                    self.compile.assert_not_called()
                finally: path.write_bytes(before)
        for path in paths:
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

    def test_report_aliases_and_conflicts_fail_before_any_new_build_or_compilation(self):
        directories = set((self.root / "build").glob("pointer-reuse-*"))
        for path in (self.path, self.grouped, self.source, self.history, self.old.path,
                     self.old.inherited.source, self.old.inherited.reference, self.parent.compiler):
            with self.subTest(path=path):
                self.report = path; before = path.read_bytes()
                with self.assertRaises(ValueError): self.trial()
                self.compile.assert_not_called(); self.assertEqual(path.read_bytes(), before)
        self.report = self.parent.write("evidence/conflict.json", b"retained evidence")
        with self.assertRaises(ValueError): self.trial()
        self.compile.assert_not_called()
        self.assertEqual(self.report.read_bytes(), b"retained evidence")
        self.assertEqual(set((self.root / "build").glob("pointer-reuse-*")), directories)


if __name__ == "__main__":
    unittest.main()
