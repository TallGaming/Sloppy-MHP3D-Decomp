"""Invented fourteen-function objects and mocked GCC; no real compiler runs."""

import copy
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts import bench_gcc_versions as gcc
from scripts.bench_compiler import compare_object
from scripts.elf32 import Elf32
from tests import test_language_modes as invented


class GccVersionRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.path = self.root / "config/gcc.json"
        self.report = self.root / "evidence/result.json"
        self.source = self.write("bench/original.c", b"/* Invented fixed source; no game bytes. */\n")
        self.manifest = invented.manifest(14)
        self.manifest_path = self.write_json("config/probes.json", self.manifest)
        self.reference = self.write("reference/invented.elf", invented.fixture(count=14, reference=True))
        self.lock = self.write_json("config/reference.json", {"status": "active", "baseline_selected_by_user": True,
                                      "decrypted_executable": self.pin(self.reference)})
        self.legacy = self.write("config/legacy.json", b"{}")
        self.assembler = self.write("native/assembler", b"invented assembler")
        self.timeout = self.write("native/timeout", b"invented timeout")
        self.host = self.write("native/lib.so", b"invented native dependency")
        self.control_compiler = self.write("tools/control/cc1", b"invented control backend")
        self.candidate_compiler = self.write("tools/candidate/cc1", b"invented candidate backend")
        self.support = self.write("tools/candidate/support", b"invented support")
        self.archive = self.write("tools/candidate.zip", b"invented archive")
        self.control = self.profile("psp_gcc_1_7_1", "gcc 3.3.3+allegrex-2.2.2-psp-1.7.1", self.control_compiler)
        self.candidate = self.profile("psp_gcc_1_3_1", "gcc 3.3.3+allegrex-2.2.1-psp-1.3.1", self.candidate_compiler)
        self.candidate.update(archive=self.pin(self.archive), support_files=[self.pin(self.candidate_compiler), self.pin(self.support)])
        self.families = {"baseline_source": self.pin(self.source), "probe_manifest": self.pin(self.manifest_path),
                         "reference_lock": self.pin(self.lock), "existing_candidate_config": self.pin(self.legacy),
                         "profiles": [self.control], "pre_score_evidence": [],
                         "linux_dependencies": [self.native_pin(self.host)], "linux_utilities": [self.native_pin(self.timeout)]}
        self.family_path = self.write_json("config/families.json", self.families)
        self.selection = self.write_json("evidence/selection.json", {"candidate": "psp-gcc-1.3.1", "declared_trials": 2})
        self.inventory = self.write_json("evidence/inventory.json", {"selection_sha256": self.pin(self.selection)["sha256"],
            "archive": self.pin(self.archive), "files": self.candidate["support_files"]})
        self.preflight = self.write("evidence/preflight.json", b"{}")
        self.preflight_source = self.write("bench/preflight.c", b"/* Invented availability fixture. */\n")
        self.help = self.write("evidence/help.txt", b"invented pinned help")
        self.preserved = self.write("bench/preserved.cpp", b"/* Earlier immutable experiment. */\n")
        self.object = bytes(invented.fixture(count=14))
        self.historic = self.historic_family()
        self.history = self.write_json("evidence/control.json", {"families": [self.historic],
            "profiles_sha256": self.pin(self.family_path)["sha256"], "source_sha256": self.pin(self.source)["sha256"],
            "manifest_sha256": self.pin(self.manifest_path)["sha256"], "reference_sha256": self.pin(self.reference)["sha256"],
            "probe_count": 14})
        self.config = {"schema_version": 1, "status": "frozen_before_candidate_target_scoring",
            "no_candidate_target_scores_observed": True, "family_profiles": self.pin(self.family_path),
            "source": self.pin(self.source), "probe_manifest": self.pin(self.manifest_path), "reference_lock": self.pin(self.lock),
            "control_report": self.pin(self.history), "tool_inventory": self.pin(self.inventory), "selection": self.pin(self.selection),
            "preflight_source": self.pin(self.preflight_source), "preflight_evidence": self.pin(self.preflight),
            "pre_score_evidence": [self.pin(self.help)], "preserved_inputs": [self.pin(self.preserved)],
            "control_profile_id": self.control["id"], "candidate": self.candidate, "declared_trials": 2, "probe_count": 14}
        self.save()
        patcher = mock.patch.object(gcc, "compile_profile", side_effect=self.compile_ok)
        self.compile = patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def write_json(self, relative, data):
        return self.write(relative, json.dumps(data).encode())

    def pin(self, path):
        return {"relative_path": path.relative_to(self.root).as_posix(), "size": len(path.read_bytes()), "sha256": invented.sha(path.read_bytes())}

    def native_pin(self, path):
        return {"linux_path": str(path), "size": len(path.read_bytes()), "sha256": invented.sha(path.read_bytes())}

    def profile(self, name, version, compiler):
        return {"id": name, "family": "GCC", "version": version, "mode": "gcc_backend_native", "status": "runnable",
            "compiler": self.pin(compiler), "support_files": [], "common_flags": copy.deepcopy(gcc.COMMON),
            "assembler": self.native_pin(self.assembler), "assembler_flags": copy.deepcopy(gcc.ASSEMBLER),
            "levels": copy.deepcopy(gcc.LEVELS)}

    def historic_family(self):
        comparison = compare_object(self.object, Elf32(self.reference.read_bytes()), self.manifest)
        return {"id": self.control["id"], "declared_settings": 4, "completed_settings": 4,
            "attempts": [{"setting": level["id"], "status": "OBJECT_VALIDATED", "object_sha256": invented.sha(self.object)} for level in gcc.LEVELS],
            "rows": [{"setting": level["id"], "flags": gcc.COMMON + level["flags"], "assembler_flags": gcc.ASSEMBLER,
                      "exact_probes": 14, "artifacts": {}, **comparison} for level in gcc.LEVELS]}

    def save(self):
        self.write_json(self.path.relative_to(self.root).as_posix(), self.config)

    def compile_ok(self, profile, source, output, flags, **kwargs):
        self.assertFalse(output.exists(), "Every setting must use a fresh object path")
        self.assertEqual(source, self.source)
        self.assertEqual(profile["common_flags"], gcc.COMMON)
        self.assertEqual(profile["assembler_flags"], gcc.ASSEMBLER)
        self.assertEqual(profile["assembler"], self.control["assembler"])
        self.assertEqual(profile["timeout_tool"], str(self.timeout))
        self.assertIn(flags, [[f"-O{i}"] for i in range(4)])
        output.write_bytes(self.object)
        return {"returncode": 0, "stdout": "", "stderr": "", "artifacts": {}}

    def trial(self):
        return gcc.run_gcc_versions(root=self.root, config_path=self.path, report_path=self.report)

    def test_all_eight_frozen_configurations_validate_full_fourteen_function_sets(self):
        report, directory = self.trial()
        self.assertEqual(self.compile.call_count, 8)
        self.assertEqual(report["completed_configurations"], 8)
        self.assertEqual(report["declared_configurations"], 8)
        self.assertTrue(report["historical_control_reproduced"])
        self.assertEqual(report["matched_progress"], 0)
        self.assertEqual([v["id"] for v in report["versions"]], [self.candidate["id"], self.control["id"]])
        for version in report["versions"]:
            self.assertEqual([a["setting"] for a in version["attempts"]], [f"O{i}" for i in range(4)])
            self.assertTrue(all(len(row["comparisons"]) == 14 and row["exact_probes"] == 14 for row in version["rows"]))
        self.assertTrue(all(row["identical_functions"] == 14 for row in report["cross_version"]))
        self.assertEqual(len(list(directory.glob("*.o"))), 8)
        self.assertEqual(json.loads(self.report.read_bytes()), report)

    def test_two_trials_use_sixteen_fresh_paths_and_identical_pathfree_reports(self):
        first, a = self.trial()
        raw = self.report.read_bytes()
        second, b = self.trial()
        self.assertNotEqual(a, b)
        self.assertEqual(first, second)
        self.assertEqual(raw, self.report.read_bytes())
        self.assertEqual(len({c.args[2] for c in self.compile.call_args_list}), 16)
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_failed_candidate_setting_retains_all_attempts_but_has_no_partial_score(self):
        for failure in ("nonzero", "warning", "timeout", "missing", "invalid", "missing_function", "relocation"):
            with self.subTest(failure=failure):
                self.report = self.root / "evidence" / (failure + ".json")
                def fail(profile, source, output, flags, **kwargs):
                    if profile["id"] != self.candidate["id"] or flags != ["-O1"]:
                        return self.compile_ok(profile, source, output, flags, **kwargs)
                    if failure == "timeout":
                        raise subprocess.TimeoutExpired("invented", 20)
                    if failure == "missing":
                        return {"returncode": 0, "stdout": "", "stderr": ""}
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if failure == "nonzero": result["returncode"] = 1
                    elif failure == "warning": result["stderr"] = "Warning: invented diagnostic"
                    elif failure == "invalid": output.write_bytes(b"not ELF")
                    elif failure == "missing_function": output.write_bytes(invented.fixture(count=13))
                    else:
                        raw = invented.fixture(count=14)
                        struct.pack_into("<I", raw, invented.SHOFF + 5 * 40 + 20, 8)
                        struct.pack_into("<II", raw, invented.REL, 0, (1 << 8) | 4)
                        output.write_bytes(raw)
                    return result
                self.compile.side_effect = fail
                report, _ = self.trial()
                candidate = report["versions"][0]
                self.assertEqual([r["setting"] for r in candidate["rows"]], ["O0", "O2", "O3"])
                self.assertEqual(len(candidate["attempts"]), 4)
                rejected = candidate["attempts"][1]
                self.assertEqual(rejected["status"], "REJECTED_NO_SCORE")
                self.assertNotIn("exact_probes", rejected)
                self.assertNotIn("comparisons", rejected)
                self.assertEqual(report["cross_version"][1], {"setting": "O1", "status": "UNSCORED", "identical_functions": None, "comparisons": None})
                self.assertTrue(report["historical_control_reproduced"])

    def test_changed_control_output_or_failure_is_fatal_instead_of_accepting_new_baseline(self):
        for failure in ("changed_byte", "nonzero"):
            with self.subTest(failure=failure):
                def fail(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if profile["id"] == self.control["id"] and flags == ["-O2"]:
                        if failure == "nonzero": result["returncode"] = 1
                        else:
                            raw = bytearray(self.object)
                            raw[invented.TEXT + 4] ^= 1
                            output.write_bytes(raw)
                    return result
                self.compile.side_effect = fail
                with self.assertRaisesRegex(ValueError, "control"):
                    self.trial()
                self.assertFalse(self.report.exists())

    def test_both_complete_versions_compare_whole_sizes_without_trimming(self):
        def changed(profile, source, output, flags, **kwargs):
            result = self.compile_ok(profile, source, output, flags, **kwargs)
            if profile["id"] == self.candidate["id"]:
                raw = bytearray(self.object)
                struct.pack_into("<I", raw, invented.SYMS + 16 + 8, 12)
                output.write_bytes(raw)
            return result
        self.compile.side_effect = changed
        report, _ = self.trial()
        for row in report["cross_version"]:
            first = row["comparisons"][0]
            self.assertFalse(first["identical"])
            self.assertEqual((first["candidate_size"], first["control_size"], first["first_difference"]), (12, 8, 8))
            self.assertEqual(row["identical_functions"], 13)

    def test_scope_flags_version_levels_or_inventory_changes_fail_before_compile(self):
        original = copy.deepcopy(self.config)
        changes = [("status", "pending"), ("no_candidate_target_scores_observed", False), ("declared_trials", 1),
                   ("probe_count", 13), ("control_profile_id", "other")]
        bads = []
        for key, value in changes:
            bad = copy.deepcopy(original); bad[key] = value; bads.append(bad)
        for key, value in (("id", "other"), ("version", "different"), ("mode", "driver"),
                           ("common_flags", gcc.COMMON + ["-fno-delayed-branch"]),
                           ("assembler_flags", gcc.ASSEMBLER[:-1]), ("levels", list(reversed(gcc.LEVELS))),
                           ("support_files", original["candidate"]["support_files"][:1])):
            bad = copy.deepcopy(original); bad["candidate"][key] = value; bads.append(bad)
        for bad in bads:
            self.config = bad; self.save()
            with self.subTest(bad=bad), self.assertRaises(ValueError): self.trial()
            self.compile.assert_not_called()
            self.assertFalse(self.report.exists())

    def test_preexisting_local_and_native_pin_mismatches_fail_globally(self):
        for path in (self.source, self.manifest_path, self.lock, self.reference, self.family_path, self.history,
                     self.selection, self.inventory, self.preflight, self.preflight_source, self.help, self.archive,
                     self.candidate_compiler, self.support, self.control_compiler, self.assembler, self.timeout, self.host,
                     self.preserved):
            with self.subTest(path=path):
                raw = path.read_bytes(); path.write_bytes(raw + b"changed")
                try:
                    with self.assertRaises(ValueError): self.trial()
                    self.compile.assert_not_called()
                    self.assertFalse(self.report.exists())
                finally: path.write_bytes(raw)

    def test_pin_or_freeze_mutation_during_trial_prevents_all_publication(self):
        for path in (self.source, self.reference, self.path, self.family_path, self.history,
                     self.candidate_compiler, self.control_compiler, self.assembler, self.preserved):
            with self.subTest(path=path):
                raw = path.read_bytes()
                def mutate(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    path.write_bytes(raw + b"changed")
                    return result
                self.compile.side_effect = mutate
                try:
                    with self.assertRaises((ValueError, json.JSONDecodeError)): self.trial()
                    self.assertFalse(self.report.exists())
                finally: path.write_bytes(raw)

    def test_later_compile_cannot_modify_valid_or_failed_retained_object(self):
        for failure in (None, "nonzero", "timeout"):
            with self.subTest(failure=failure):
                emitted = []
                def mutate(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    emitted.append(output)
                    if len(emitted) == 1 and failure == "nonzero": result["returncode"] = 1
                    if len(emitted) == 1 and failure == "timeout": raise subprocess.TimeoutExpired("invented", 20)
                    if len(emitted) == 2: emitted[0].write_bytes(b"replacement object")
                    return result
                self.compile.side_effect = mutate
                with self.assertRaisesRegex(ValueError, "object changed"):
                    self.trial()
                self.assertFalse(self.report.exists())

    def test_report_aliases_preserve_every_declared_input_before_compile(self):
        for path in (self.path, self.source, self.reference, self.family_path, self.history, self.inventory,
                     self.candidate_compiler, self.control_compiler, self.support, self.preserved):
            with self.subTest(path=path):
                raw = path.read_bytes(); self.report = path
                with self.assertRaises(ValueError): self.trial()
                self.compile.assert_not_called()
                self.assertEqual(path.read_bytes(), raw)

    def test_existing_conflicting_report_is_preserved(self):
        self.report.parent.mkdir(parents=True, exist_ok=True)
        self.report.write_bytes(b"retained evidence")
        with self.assertRaises(ValueError): self.trial()
        self.assertEqual(self.report.read_bytes(), b"retained evidence")

    def test_historical_report_cannot_be_rebound_to_wrong_source_or_partial_outcomes(self):
        original = json.loads(self.history.read_bytes())
        for changed in ("source", "missing_attempt", "count"):
            bad = copy.deepcopy(original)
            if changed == "source": bad["source_sha256"] = "0" * 64
            elif changed == "missing_attempt": bad["families"][0]["attempts"].pop()
            else: bad["families"][0]["completed_settings"] = 3
            self.history.write_text(json.dumps(bad))
            self.config["control_report"] = self.pin(self.history); self.save()
            with self.subTest(changed=changed), self.assertRaises(ValueError): self.trial()
            self.compile.assert_not_called()

    def test_cross_version_unscored_or_incomplete_set_never_manufactures_zero_score(self):
        functions = {name: invented.code(i) for i, name in enumerate(invented.names(14))}
        self.assertEqual(gcc.compare_versions(None, functions), {"status": "UNSCORED", "identical_functions": None, "comparisons": None})
        with self.assertRaises(ValueError): gcc.compare_versions(dict(list(functions.items())[:13]), functions)


if __name__ == "__main__":
    unittest.main()
