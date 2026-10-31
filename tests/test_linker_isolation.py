"""Invented two-layout controls; compiler and linker calls are always mocked."""

import copy
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts import bench_linker_isolation as isolation


EXPLICIT = 0x08804000
OBSERVED = 0x00102000
CODE = struct.pack("<3I", 0x24820001, 0x03e00008, 0)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fixture(address=None):
    linked = address is not None
    address = address or 0
    raw = bytearray(0x400)
    names = b"\0.shstrtab\0.text\0.strtab\0.symtab\0.comment\0"
    strings = b"\0family_smoke\0"
    comment = b"Invented tool\0"
    raw[0x80:0x80 + len(names)] = names
    raw[0x100:0x10c] = CODE
    raw[0x120:0x120 + len(strings)] = strings
    raw[0x180:0x180 + len(comment)] = comment
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0, b"\x7fELF\x01\x01\x01" + bytes(9),
                     2 if linked else 1, 8, 1, address, 52 if linked else 0, 0x200,
                     0x10a23001, 52, 32 if linked else 0, 1 if linked else 0, 40, 6, 1)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (names.index(b".shstrtab"), 3, 0, 0, 0x80, len(names), 0, 0, 1, 0),
                (names.index(b".text"), 1, 6, address, 0x100, len(CODE), 0, 0, 4, 0),
                (names.index(b".strtab"), 3, 0, 0, 0x120, len(strings), 0, 0, 1, 0),
                (names.index(b".symtab"), 2, 0, 0, 0x140, 32, 3, 1, 4, 16),
                (names.index(b".comment"), 1, 0, 0, 0x180, len(comment), 0, 0, 1, 0)]
    for i, section in enumerate(sections):
        struct.pack_into("<10I", raw, 0x200 + i * 40, *section)
    struct.pack_into("<IIIBBH", raw, 0x150, 1, address, len(CODE), 0x12, 0, 2)
    if linked:
        struct.pack_into("<8I", raw, 52, 1, 0x100, address, address, len(CODE), len(CODE), 5, 4)
    return raw


class IsolationAssessmentTests(unittest.TestCase):
    def test_default_observes_validated_placement_instead_of_assuming_explicit_base(self):
        result = isolation.assess_case(fixture(), fixture(OBSERVED), {"expected_entry_address": None})
        self.assertEqual(result["status"], "PRESERVED")
        self.assertEqual(result["output"]["entry"], OBSERVED)
        self.assertNotEqual(result["output"]["entry"], EXPLICIT)

    def test_explicit_case_keeps_its_prefrozen_address_requirement(self):
        case = {"expected_entry_address": EXPLICIT}
        self.assertEqual(isolation.assess_case(fixture(), fixture(EXPLICIT), case)["status"], "PRESERVED")
        with self.assertRaises(ValueError):
            isolation.assess_case(fixture(), fixture(OBSERVED), case)

    def test_default_still_requires_entry_symbol_and_unique_executable_mapping(self):
        for offset, fmt, value in ((24, "<I", OBSERVED + 4), (44, "<H", 0),
                                    (52 + 4, "<I", 0x104), (52 + 24, "<I", 4),
                                    (0x150, "<I", 0)):
            with self.subTest(offset=offset):
                bad = fixture(OBSERVED)
                struct.pack_into(fmt, bad, offset, value)
                with self.assertRaises(ValueError):
                    isolation.assess_case(fixture(), bad, {"expected_entry_address": None})

    def test_changed_complete_code_remains_a_finding_at_observed_default_address(self):
        bad = fixture(OBSERVED)
        bad[0x100] ^= 1
        result = isolation.assess_case(fixture(), bad, {"expected_entry_address": None})
        self.assertEqual(result["status"], "CODE_CHANGED")
        self.assertFalse(result["complete_function_bytes_equal"])


class IsolationRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.path = self.root / "config/isolation.json"
        self.report_path = self.root / "evidence/report.json"
        self.source = self.write("bench/fixture.c", b"/* Invented SNC fixture. */\n")
        self.old_layout = self.write("bench/old.ld", b"ENTRY(family_smoke)\n")
        self.minimal = self.write("bench/minimal.ld", b"ENTRY(family_smoke)\nSECTIONS { .text 0x08804000 : { *(.text) } }\n")
        self.linker = self.write("tools/linker.exe", b"invented linker")
        self.support = self.write("tools/support.dll", b"invented support")
        self.compiler = self.write("tools/compiler.exe", b"invented compiler")
        self.runner = self.write("tools/runner", b"invented runner")
        self.timeout = self.write("native/timeout", b"invented timeout")
        self.native = self.write("native/windows.dll", b"invented dependency")
        self.old_source = self.write("bench/unused.c", b"unused invented source")
        self.manifest = self.write("config/manifest.json", b"{}")
        self.reference = self.write("config/reference.json", b"{}")
        self.legacy = self.write("config/legacy.json", b"{}")
        profile = {"id": "psp_snc_1_2_7503", "status": "runnable", "mode": "wibo_driver",
                   "compiler": self.pin(self.compiler), "runner": self.pin(self.runner),
                   "support_files": [self.pin(self.support)], "common_flags": ["-c", "-G0"]}
        family_config = {"baseline_source": self.pin(self.old_source), "probe_manifest": self.pin(self.manifest),
                         "reference_lock": self.pin(self.reference), "existing_candidate_config": self.pin(self.legacy),
                         "pre_score_evidence": [], "profiles": [profile], "linux_dependencies": [],
                         "linux_utilities": [self.native_pin(self.timeout)]}
        self.family_path = self.write("config/families.json", json.dumps(family_config).encode())
        common = ["-comment", "-e", "family_smoke", "-Wall", "-Werror", "-t"]
        prefix, tail = ["{linker}", *common], ["-Map", "{map}", "-o", "{output}", "{object}"]
        base = {"family_profiles": self.pin(self.family_path), "source": self.pin(self.source),
                "layout": self.pin(self.old_layout), "linker": self.pin(self.linker),
                "support_files": [self.pin(self.support)], "native_windows_dependencies": [self.native_pin(self.native)],
                "prelink_evidence": [], "profile_ids": [profile["id"]], "optimization": ["-O0"],
                "entry_symbol": "family_smoke", "text_address": EXPLICIT, "no_libraries": True,
                "runner": "wsl_native_windows_interop", "common_link_flags": common,
                "timeout_seconds": 2, "windows_project_root": "D:\\invented-project"}
        self.base_path = self.write("config/baseline.json", json.dumps(base).encode())
        self.config = {"status": "frozen_before_isolation_outputs", "no_isolation_link_outputs_observed": True,
                       "baseline_experiment": self.pin(self.base_path), "minimal_layout": self.pin(self.minimal),
                       "compiler_profile_id": profile["id"], "optimization": ["-O0"], "entry_symbol": "family_smoke",
                       "common_link_flags": common, "cases": [
                           {"id": "default_layout", "expected_entry_address": None, "command_template": prefix + tail},
                           {"id": "minimal_explicit_layout", "expected_entry_address": EXPLICIT,
                            "command_template": prefix + ["-T", "{layout}"] + tail}],
                       "compile_once_per_trial": True, "same_object_for_both_cases": True,
                       "no_libraries": True, "runner": base["runner"], "trial_count": 2, "timeout_seconds": 2}
        self.save()
        compile_patch = mock.patch.object(isolation, "compile_profile", side_effect=self.compile_ok)
        link_patch = mock.patch.object(isolation, "link_fixture", side_effect=self.link_ok)
        self.compile = compile_patch.start()
        self.link = link_patch.start()
        self.addCleanup(compile_patch.stop)
        self.addCleanup(link_patch.stop)

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def pin(self, path):
        data = path.read_bytes()
        return {"relative_path": path.relative_to(self.root).as_posix(), "size": len(data), "sha256": sha(data)}

    def native_pin(self, path):
        return {"linux_path": str(path), "size": path.stat().st_size, "sha256": sha(path.read_bytes())}

    def save(self):
        self.path.write_text(json.dumps(self.config), encoding="utf-8")

    def compile_ok(self, profile, source, output, flags, **kwargs):
        self.assertFalse(output.exists())
        self.assertEqual(profile["id"], "psp_snc_1_2_7503")
        self.assertEqual(source, self.source)
        self.assertEqual(flags, ["-O0"])
        output.write_bytes(fixture())
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def link_ok(self, config, obj, output, map_path, **kwargs):
        self.assertEqual(obj.read_bytes(), fixture())
        self.assertFalse(output.exists())
        self.assertFalse(map_path.exists())
        explicit = "-T" in config["command_template"]
        output.write_bytes(fixture(EXPLICIT if explicit else OBSERVED))
        map_path.write_text("Invented map.\n")
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def run_trial(self):
        return isolation.run_isolation(root=self.root, config_path=self.path, report_path=self.report_path)

    def test_compile_once_and_use_identical_object_for_both_prefrozen_cases(self):
        report, directory = self.run_trial()
        self.assertEqual(self.compile.call_count, 1)
        self.assertEqual(self.link.call_count, 2)
        self.assertEqual(len({c.args[1] for c in self.link.call_args_list}), 1)
        self.assertEqual(len(list(directory.glob("*.o"))), 1)
        self.assertEqual([c["status"] for c in report["cases"]], ["PRESERVED", "PRESERVED"])
        self.assertEqual(report["cases"][0]["output"]["entry"], OBSERVED)
        self.assertEqual(report["cases"][1]["output"]["entry"], EXPLICIT)
        self.assertEqual(report["matched_progress"], 0)
        self.assertEqual(json.loads(self.report_path.read_text()), report)

    def test_repeat_trials_have_fresh_objects_and_identical_pathfree_reports(self):
        first, a = self.run_trial()
        raw = self.report_path.read_bytes()
        second, b = self.run_trial()
        self.assertNotEqual(a, b)
        self.assertEqual(self.compile.call_count, 2)
        self.assertEqual(len({c.args[1] for c in self.link.call_args_list}), 2)
        self.assertEqual(first, second)
        self.assertEqual(raw, self.report_path.read_bytes())
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_unreviewed_extra_reordered_or_changed_cases_fail_before_tools(self):
        original = copy.deepcopy(self.config)
        bad_cases = [original["cases"][:1], list(reversed(original["cases"])), original["cases"] * 2]
        changed = copy.deepcopy(original["cases"])
        changed[0]["command_template"].append("-lSDK")
        bad_cases.append(changed)
        for field, value in [("status", "draft"), ("no_isolation_link_outputs_observed", False),
                             ("optimization", ["-O1"]), ("same_object_for_both_cases", False),
                             ("compile_once_per_trial", False), ("compiler_profile_id", "different"),
                             *[("cases", cases) for cases in bad_cases]]:
            with self.subTest(field=field):
                self.config = copy.deepcopy(original)
                self.config[field] = value
                self.save()
                with self.assertRaises(ValueError): self.run_trial()
                self.compile.assert_not_called()
                self.link.assert_not_called()

    def test_compile_failure_warning_timeout_and_missing_or_invalid_object_leave_two_not_run_cases(self):
        for mode in ("nonzero", "warning", "timeout", "missing", "invalid"):
            with self.subTest(mode=mode):
                self.report_path = self.root / "evidence" / (mode + ".json")
                def fail(profile, source, output, flags, **kwargs):
                    if mode == "timeout": raise subprocess.TimeoutExpired("invented", 2)
                    if mode == "missing": return {"returncode": 0, "stdout": "", "stderr": ""}
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if mode == "nonzero": result["returncode"] = 1
                    elif mode == "warning": result["stderr"] = "Warning: invented"
                    else: output.write_bytes(b"not ELF")
                    return result
                self.compile.side_effect = fail
                report, _ = self.run_trial()
                self.assertEqual(len(report["cases"]), 2)
                self.assertTrue(all(c["status"] == "NOT_RUN_COMPILE_FAILED" for c in report["cases"]))
                self.link.assert_not_called()

    def test_failed_default_case_does_not_hide_valid_explicit_case_or_recompile_input(self):
        def fail_default(config, obj, output, map_path, **kwargs):
            result = self.link_ok(config, obj, output, map_path, **kwargs)
            if "-T" not in config["command_template"]:
                result["returncode"] = 255
            return result
        self.link.side_effect = fail_default
        report, _ = self.run_trial()
        self.assertEqual([c["status"] for c in report["cases"]], ["LINK_FAILED", "PRESERVED"])
        self.assertEqual(self.compile.call_count, 1)
        self.assertEqual(report["preserved_cases"], 1)

    def test_warning_timeout_missing_output_or_map_never_claims_case_preservation(self):
        for mode in ("warning", "timeout", "output", "map"):
            with self.subTest(mode=mode):
                self.report_path = self.root / "evidence" / (mode + ".json")
                def fail(config, obj, output, map_path, **kwargs):
                    if mode == "timeout": raise subprocess.TimeoutExpired("invented", 2)
                    result = self.link_ok(config, obj, output, map_path, **kwargs)
                    if mode == "warning": result["stderr"] = "Warning: invented"
                    else: (output if mode == "output" else map_path).unlink()
                    return result
                self.link.side_effect = fail
                report, _ = self.run_trial()
                self.assertEqual(report["preserved_cases"], 0)
                self.assertEqual(len(report["cases"]), 2)

    def test_changed_shared_object_is_fatal_before_second_case_and_outer_report(self):
        def mutate(config, obj, output, map_path, **kwargs):
            result = self.link_ok(config, obj, output, map_path, **kwargs)
            obj.write_bytes(b"mutated shared input")
            return result
        self.link.side_effect = mutate
        with self.assertRaises(ValueError): self.run_trial()
        self.assertEqual(self.link.call_count, 1)
        self.assertFalse(self.report_path.exists())

    def test_global_pins_are_checked_before_and_after_linking(self):
        paths = (self.base_path, self.minimal, self.source, self.linker, self.support,
                 self.family_path, self.compiler, self.native)
        for path in paths:
            with self.subTest(path=path.name, stage="before"):
                original = path.read_bytes()
                path.write_bytes(original + b"changed")
                with self.assertRaises(ValueError): self.run_trial()
                self.compile.assert_not_called()
                path.write_bytes(original)
        for path in (*paths, self.path):
            with self.subTest(path=path.name, stage="after"):
                original = path.read_bytes()
                def mutate(*args, **kwargs):
                    result = self.link_ok(*args, **kwargs)
                    path.write_bytes(original + b"changed")
                    return result
                self.link.side_effect = mutate
                with self.assertRaises(ValueError): self.run_trial()
                self.assertFalse(self.report_path.exists())
                path.write_bytes(original)

    def test_report_conflicts_and_inherited_input_aliases_preserve_files(self):
        self.report_path.parent.mkdir()
        self.report_path.write_bytes(b"valuable evidence")
        with self.assertRaises(ValueError): self.run_trial()
        self.assertEqual(self.report_path.read_bytes(), b"valuable evidence")
        for path in (self.path, self.base_path, self.minimal, self.source, self.linker,
                     self.support, self.family_path, self.compiler, self.native):
            with self.subTest(path=path.name):
                self.report_path = path
                before = path.read_bytes()
                with self.assertRaises(ValueError): self.run_trial()
                self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
