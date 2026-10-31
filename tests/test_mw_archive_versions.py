"""Invented archive objects and mocked MW matrix; no real compiler execution."""

import copy
import json
import struct
import subprocess
import unittest
from unittest import mock

from scripts import bench_mw_archive_versions as matrix
from scripts.bench_archive_key import compare_archive_object
from scripts.elf32 import Elf32
from tests import test_archive_key_probe as invented


class MwArchiveVersionRunnerTests(unittest.TestCase):
    def setUp(self):
        # Keep the actual inherited archive/language/family validation enabled.
        self.inherited = invented.ArchiveRunnerTests(methodName="runTest")
        self.inherited.setUp()
        self.addCleanup(self.inherited.doCleanups)
        archive = self.inherited
        old = archive.parent_fixture
        self.old, self.root = old, old.root
        self.source, self.reference = archive.source, archive.reference
        self.path = self.root / "config/mw-versions.json"
        self.report = self.root / "evidence/mw-report.json"
        self.object = bytes(invented.fixture())
        self.catalogue = {"runner": old.pin(old.runner), "candidates": []}
        self.versions = []
        for index, name in enumerate(matrix.IDS):
            compiler = old.compiler if index == 10 else old.write(f"tools/{name}/compiler.exe", name.encode())
            support = old.profile["support_files"] if index == 10 else [old.pin(old.write(f"tools/{name}/support.dll", b"support " + name.encode()))]
            packed = old.write(f"tools/{name}.tar.gz", b"invented archive " + name.encode())
            help_path = old.write(f"evidence/{name}-help.txt", b"invented help " + name.encode())
            self.catalogue["candidates"].append({"id": name, "version": "invented " + name,
                "compiler": old.pin(compiler), "support_files": support,
                "archive_sha256": old.pin(packed)["sha256"], "help_evidence": help_path.relative_to(self.root).as_posix(),
                "help_sha256": old.pin(help_path)["sha256"]})
            self.versions.append({"id": name, "archive": old.pin(packed), "help": old.pin(help_path)})
        old.legacy.write_text(json.dumps(self.catalogue))
        old.families["existing_candidate_config"] = old.pin(old.legacy)
        old.family_path.write_text(json.dumps(old.families))
        old.spec["compiler_families"] = old.pin(old.family_path)
        old.spec_path.write_text(json.dumps(old.spec))
        old.evidence["spec_sha256"] = old.pin(old.spec_path)["sha256"]
        old.evidence_path.write_text(json.dumps(old.evidence))
        old.config.update(family_profiles=old.pin(old.family_path), naming_spec=old.pin(old.spec_path),
                          naming_evidence=old.pin(old.evidence_path))
        old.save()
        archive.config["language_profile"] = old.pin(old.path)
        archive.save()
        comparison = compare_archive_object(self.object, Elf32(self.reference.read_bytes()), invented.manifest(), invented.MEMBER)
        self.history_data = {"status": "ARCHIVE_KEY_INVESTIGATION_COMPLETE", "outcome": "COMPLETE", "returncode": 0,
            "profile_sha256": old.pin(archive.path)["sha256"], "source_sha256": old.pin(self.source)["sha256"],
            "reference_sha256": old.pin(self.reference)["sha256"], "flags": archive.config["common_flags"] + ["-O2"],
            "exact_probes": 1, **comparison}
        self.history = old.write("evidence/archive-history.json", json.dumps(self.history_data).encode())
        self.preserved = old.write("bench/earlier.cpp", b"/* Invented preserved earlier source. */\n")
        self.config = {"status": "frozen_before_matrix_target_scoring", "no_matrix_target_scores_observed": True,
            "archive_profile": old.pin(archive.path), "compiler_candidates": old.pin(old.legacy),
            "historical_control": old.pin(self.history), "common_flags": archive.config["common_flags"],
            "optimization": ["-O2"], "declared_trials": 2, "source_attempts": 1,
            "versions": self.versions, "preserved_inputs": [old.pin(self.preserved)]}
        self.save()
        patcher = mock.patch.object(matrix, "compile_profile", side_effect=self.compile_ok)
        self.compile = patcher.start()
        self.addCleanup(patcher.stop)

    def save(self):
        self.path.write_text(json.dumps(self.config))

    def compile_ok(self, profile, source, output, flags, **kwargs):
        self.assertFalse(output.exists(), "Every declared version needs a fresh output")
        self.assertEqual(source, self.source)
        self.assertEqual(flags, ["-O2"])
        self.assertEqual(profile["common_flags"], ["-nostdinc", "-lang", "c++", "-c"])
        self.assertEqual(profile["runner"], self.catalogue["runner"])
        candidate = next(c for c in self.catalogue["candidates"] if c["id"] == profile["id"])
        self.assertEqual(profile["compiler"], candidate["compiler"])
        self.assertEqual(profile["support_files"], candidate["support_files"])
        self.assertEqual(profile["timeout_tool"], str(self.old.timeout))
        output.write_bytes(self.object)
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def trial(self):
        return matrix.run_mw_archive_versions(root=self.root, config_path=self.path, report_path=self.report)

    def test_exact_eleven_cases_preserve_member_flags_and_all_outcomes(self):
        report, directory = self.trial()
        self.assertEqual(self.compile.call_count, 11)
        self.assertEqual([r["id"] for r in report["versions"]], matrix.IDS)
        self.assertEqual(report["declared_cases"], 11)
        self.assertEqual(report["completed_cases"], 11)
        self.assertTrue(report["historical_control_reproduced"])
        self.assertEqual(report["matched_progress"], 0)
        for row in report["versions"]:
            self.assertEqual(row["outcome"], "COMPLETE")
            self.assertEqual(row["exact_probes"], 1)
            self.assertEqual(len(row["comparisons"]), 1)
            self.assertEqual(row["comparisons"][0]["object_symbol"], invented.MEMBER)
        self.assertTrue(all(r["identical"] for r in report["differences_from_219"]))
        self.assertEqual(len(list(directory.glob("*.o"))), 11)
        self.assertEqual(json.loads(self.report.read_bytes()), report)

    def test_two_trials_use_twenty_two_fresh_paths_and_pathfree_identical_reports(self):
        first, a = self.trial(); before = self.report.read_bytes()
        second, b = self.trial()
        self.assertNotEqual(a, b)
        self.assertEqual(first, second)
        self.assertEqual(before, self.report.read_bytes())
        self.assertEqual(len({c.args[2] for c in self.compile.call_args_list}), 22)
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_each_failed_case_is_unscored_and_other_ten_cases_remain_visible(self):
        for failed_index in (0, 5, 9):
            for failure in ("nonzero", "warning", "timeout", "missing", "invalid", "symbol", "extra", "relocation"):
                with self.subTest(index=failed_index, failure=failure):
                    self.report = self.root / "evidence" / f"failure-{failed_index}-{failure}.json"
                    def fail(profile, source, output, flags, **kwargs):
                        if profile["id"] != matrix.IDS[failed_index]:
                            return self.compile_ok(profile, source, output, flags, **kwargs)
                        if failure == "timeout": raise subprocess.TimeoutExpired("invented", 20)
                        if failure == "missing": return {"returncode": 0, "stdout": "", "stderr": ""}
                        result = self.compile_ok(profile, source, output, flags, **kwargs)
                        raw = bytearray(self.object)
                        if failure == "nonzero": result["returncode"] = 1
                        elif failure == "warning": result["stderr"] = "Warning: invented issue"
                        elif failure == "invalid": raw = b"invalid ELF"
                        elif failure == "symbol": raw = invented.fixture(symbol="wrong_member")
                        elif failure == "extra":
                            struct.pack_into("<IIIBBH", raw, invented.SYMOFF + 32, 1, 0, 4, 0x12, 0, 2)
                            struct.pack_into("<I", raw, invented.SHOFF + 4 * 40 + 20, 48)
                        else:
                            struct.pack_into("<I", raw, invented.SHOFF + 5 * 40 + 20, 8)
                            struct.pack_into("<II", raw, 0x280, 0, (1 << 8) | 4)
                        output.write_bytes(raw)
                        return result
                    self.compile.side_effect = fail
                    report, _ = self.trial()
                    self.assertEqual(report["completed_cases"], 10)
                    self.assertEqual(len(report["versions"]), 11)
                    bad = report["versions"][failed_index]
                    self.assertEqual(bad["outcome"], "REJECTED_NO_SCORE")
                    self.assertNotIn("exact_probes", bad)
                    self.assertNotIn("comparisons", bad)
                    diff = report["differences_from_219"][failed_index]
                    self.assertEqual(diff, {"id": matrix.IDS[failed_index], "status": "UNSCORED", "identical": None, "word_differences": None})
                    self.assertTrue(report["historical_control_reproduced"])

    def test_build_219_changed_bytes_metadata_or_failure_invalidates_entire_report(self):
        for changed in ("bytes", "metadata", "failure"):
            with self.subTest(changed=changed):
                def drift(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if profile["id"] == matrix.IDS[-1]:
                        if changed == "failure": result["returncode"] = 1
                        else:
                            raw = bytearray(self.object)
                            if changed == "bytes": raw[0x100] ^= 1
                            else: struct.pack_into("<I", raw, 36, 0x10843000)
                            output.write_bytes(raw)
                    return result
                self.compile.side_effect = drift
                with self.assertRaisesRegex(ValueError, "219 control"):
                    self.trial()
                self.assertFalse(self.report.exists())

    def test_changed_equal_size_body_has_actual_word_difference_not_size_only(self):
        def change(profile, source, output, flags, **kwargs):
            result = self.compile_ok(profile, source, output, flags, **kwargs)
            if profile["id"] == matrix.IDS[0]:
                raw = bytearray(self.object); raw[0x100 + 4] = 0x27; output.write_bytes(raw)
            return result
        self.compile.side_effect = change
        report, _ = self.trial()
        diff = report["differences_from_219"][0]
        self.assertFalse(diff["identical"])
        self.assertEqual((diff["candidate_size"], diff["control_size"]), (68, 68))
        self.assertEqual(diff["word_differences"], [{"offset": 4, "candidate_bytes_hex": "27000000", "control_bytes_hex": "00000000"}])
        self.assertEqual(report["versions"][0]["exact_probes"], 0)

    def test_longer_complete_member_is_not_trimmed_to_target_or_control(self):
        def longer(profile, source, output, flags, **kwargs):
            result = self.compile_ok(profile, source, output, flags, **kwargs)
            if profile["id"] == matrix.IDS[0]:
                raw = bytearray(self.object)
                struct.pack_into("<I", raw, invented.SYMOFF + 16 + 8, 72)
                output.write_bytes(raw)
            return result
        self.compile.side_effect = longer
        report, _ = self.trial()
        row = report["versions"][0]["comparisons"][0]
        self.assertFalse(row["exact_probe_bytes"])
        self.assertEqual((row["compiled_size"], row["first_difference"]), (72, 68))
        diff = report["differences_from_219"][0]
        self.assertEqual(diff["word_differences"][-1], {"offset": 68, "candidate_bytes_hex": "00000000", "control_bytes_hex": None})

    def test_unreviewed_scope_flags_count_order_or_archive_binding_fail_before_compile(self):
        original = copy.deepcopy(self.config)
        invalid = [("status", "pending"), ("no_matrix_target_scores_observed", False), ("declared_trials", 1),
                   ("source_attempts", 2), ("optimization", ["-O3"]), ("common_flags", ["-lang", "c"]),
                   ("versions", list(reversed(original["versions"]))), ("versions", original["versions"][:10])]
        for key, value in invalid:
            self.config = copy.deepcopy(original); self.config[key] = value; self.save()
            with self.subTest(key=key), self.assertRaises(ValueError): self.trial()
            self.compile.assert_not_called()
        self.config = copy.deepcopy(original)
        self.config["versions"][0]["archive"] = self.config["versions"][1]["archive"]
        self.save()
        with self.assertRaises(ValueError): self.trial()
        self.compile.assert_not_called()

    def test_nested_source_target_naming_tool_and_native_pins_fail_globally(self):
        old, a = self.old, self.inherited
        paths = [self.source, self.reference, a.path, a.target, a.hypothesis, a.naming_source, a.naming_evidence,
                 a.naming_object, old.path, old.manifest_path, old.spec_path, old.evidence_path, old.reference_lock,
                 old.family_path, old.legacy, old.runner, old.compiler, old.support, old.timeout, old.host,
                 self.history, self.preserved]
        paths += [self.root / self.catalogue["candidates"][0]["compiler"]["relative_path"],
                  self.root / self.catalogue["candidates"][0]["support_files"][0]["relative_path"],
                  self.root / self.versions[0]["archive"]["relative_path"], self.root / self.versions[0]["help"]["relative_path"]]
        for path in paths:
            with self.subTest(path=path):
                before = path.read_bytes(); path.write_bytes(before + b"changed")
                try:
                    with self.assertRaises(ValueError): self.trial()
                    self.compile.assert_not_called()
                    self.assertFalse(self.report.exists())
                finally: path.write_bytes(before)

    def test_changed_inputs_during_matrix_prevent_publication(self):
        for path in (self.source, self.reference, self.path, self.inherited.target, self.old.compiler,
                     self.old.runner, self.old.timeout, self.preserved):
            with self.subTest(path=path):
                before = path.read_bytes()
                def mutate(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    path.write_bytes(before + b"changed")
                    return result
                self.compile.side_effect = mutate
                try:
                    with self.assertRaises(ValueError): self.trial()
                    self.assertFalse(self.report.exists())
                finally: path.write_bytes(before)

    def test_later_case_cannot_modify_valid_nonzero_or_timeout_partial_object(self):
        for failure in (None, "nonzero", "timeout"):
            with self.subTest(failure=failure):
                emitted = []
                def replace(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    emitted.append(output)
                    if len(emitted) == 1 and failure == "nonzero": result["returncode"] = 1
                    if len(emitted) == 1 and failure == "timeout": raise subprocess.TimeoutExpired("invented", 20)
                    if len(emitted) == 2: emitted[0].write_bytes(b"replacement object")
                    return result
                self.compile.side_effect = replace
                with self.assertRaisesRegex(ValueError, "object changed"):
                    self.trial()
                self.assertFalse(self.report.exists())

    def test_report_aliases_and_conflicting_existing_report_preserve_inputs(self):
        for path in (self.path, self.source, self.reference, self.inherited.path, self.inherited.naming_object,
                     self.old.path, self.old.compiler, self.old.legacy, self.history, self.preserved,
                     self.root / self.catalogue["candidates"][0]["compiler"]["relative_path"]):
            with self.subTest(path=path):
                before = path.read_bytes(); self.report = path
                with self.assertRaises(ValueError): self.trial()
                self.compile.assert_not_called()
                self.assertEqual(path.read_bytes(), before)
        self.report = self.root / "evidence/conflict.json"; self.report.write_bytes(b"retained evidence")
        with self.assertRaises(ValueError): self.trial()
        self.assertEqual(self.report.read_bytes(), b"retained evidence")

    def test_historical_control_wrong_binding_is_rejected_before_compile(self):
        for changed in ("source_sha256", "profile_sha256", "reference_sha256", "flags", "comparisons"):
            bad = copy.deepcopy(self.history_data)
            bad[changed] = [] if changed in ("flags", "comparisons") else "0" * 64
            self.history.write_text(json.dumps(bad)); self.config["historical_control"] = self.old.pin(self.history); self.save()
            with self.subTest(changed=changed), self.assertRaises(ValueError): self.trial()
            self.compile.assert_not_called()


if __name__ == "__main__":
    unittest.main()
