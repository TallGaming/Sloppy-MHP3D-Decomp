"""Invented object and compiler-family controls; no real compiler invocation.

These tooling checks confer neither matching credit nor historical compiler
attribution and are not the matching build gate's 18 negative checks.
"""

import copy
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts import bench_compiler_families as families
from scripts.bench_compiler import compare_object
from scripts.elf32 import Elf32


SHOFF = 0x400
ALPHA = struct.pack("<2I", 0x03e00008, 0)
BETA = struct.pack("<2I", 0x03e00008, 0x24020001)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def identity(data, path):
    return {"relative_path": path, "size": len(data), "sha256": sha(data)}


def shared_text_object(*, reference=False):
    """Model two indexed functions sharing .text and REL32 .pdr metadata."""
    raw = bytearray(0x700)
    names = b"\0.shstrtab\0.text\0.strtab\0.symtab\0.pdr\0.rel.pdr\0.comment\0"
    strings = b"\0probe_alpha\0probe_beta\0"
    raw[0x100:0x100 + len(names)] = names
    raw[0x180:0x188], raw[0x190:0x198] = ALPHA, BETA
    raw[0x200:0x200 + len(strings)] = strings
    comment = b"Synthetic compiler family\0"
    raw[0x360:0x360 + len(comment)] = comment
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0,
                     b"\x7fELF\x01\x01\x01" + bytes(9), 2 if reference else 1,
                     8, 1, 0x08804000 if reference else 0, 0, SHOFF, 0x10843000,
                     52, 0, 0, 40, 9, 1)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (names.index(b".shstrtab"), 3, 0, 0, 0x100, len(names), 0, 0, 1, 0),
                (names.index(b".text"), 1, 6, 0x08804000 if reference else 0, 0x180, 48, 0, 0, 16, 0),
                (names.index(b".strtab"), 3, 0, 0, 0x200, len(strings), 0, 0, 1, 0),
                (names.index(b".symtab"), 2, 0, 0, 0x240, 48, 3, 1, 4, 16),
                (names.index(b".pdr"), 1, 0, 0, 0x300, 64, 0, 0, 4, 0),
                (names.index(b".rel.pdr"), 9, 0, 0, 0x340, 16, 4, 5, 4, 8),
                (names.index(b".comment"), 1, 0, 0, 0x360, len(comment), 0, 0, 1, 0),
                (0, 1, 0, 0, 0, 0, 0, 0, 1, 0)]
    for index, section in enumerate(sections):
        struct.pack_into("<10I", raw, SHOFF + index * 40, *section)
    for index, (name, value) in enumerate(((1, 0), (13, 16)), 1):
        struct.pack_into("<IIIBBH", raw, 0x240 + index * 16, name,
                         value + (0x08804000 if reference else 0), 8, 0x12, 0, 2)
    struct.pack_into("<4I", raw, 0x340, 0, (1 << 8) | 2, 32, (2 << 8) | 2)
    return raw


def manifest():
    return {"schema_version": 1, "source": "bench/original.c", "probes": [
        {"name": "probe_alpha", "address": 0x08804000, "size": 8,
         "target_sha256": sha(ALPHA), "category": "synthetic", "ownership": "unclassified",
         "boundary_evidence": "Invented full return and delay slot.", "relocations": []},
        {"name": "probe_beta", "address": 0x08804010, "size": 8,
         "target_sha256": sha(BETA), "category": "synthetic", "ownership": "unclassified",
         "boundary_evidence": "Invented full return and delay slot.", "relocations": []}]}


class FamilyObjectAssumptionTests(unittest.TestCase):
    def setUp(self):
        self.raw = shared_text_object()
        self.reference = Elf32(shared_text_object(reference=True))
        self.probes = manifest()

    def compare(self):
        return compare_object(bytes(self.raw), self.reference, self.probes)

    def test_shared_text_uses_each_symbol_extent_and_leaves_section_gaps_unclaimed(self):
        report = self.compare()
        self.assertTrue(all(p["exact_probe_bytes"] for p in report["comparisons"]))
        self.assertEqual([p["compiled_size"] for p in report["comparisons"]], [8, 8])
        self.assertEqual(len(self.raw[0x180:0x1b0]), 48)
        self.assertEqual(report["compiler_comments"], ["Synthetic compiler family"])

    def test_function_padding_is_not_trimmed_to_make_prefix_exact(self):
        struct.pack_into("<I", self.raw, 0x250 + 8, 12)
        first = self.compare()["comparisons"][0]
        self.assertFalse(first["exact_probe_bytes"])
        self.assertEqual(first["compiled_size"], 12)
        self.assertEqual(first["first_difference"], 8)

    def test_zero_size_symbols_are_not_inferred_from_next_symbol_or_section_end(self):
        struct.pack_into("<I", self.raw, 0x250 + 8, 0)
        with self.assertRaises(ValueError):
            self.compare()

    def test_object_flags_are_recorded_as_metadata_without_forcing_target_identity(self):
        for flags in (0x10843000, 0x10a23001, 0x10970001):
            with self.subTest(flags=flags):
                struct.pack_into("<I", self.raw, 36, flags)
                report = self.compare()
                self.assertEqual(report["elf_flags"], flags)
                self.assertTrue(all(p["exact_probe_bytes"] for p in report["comparisons"]))

    def test_endianness_machine_and_rel_type_must_be_supported(self):
        for offset, fmt, value in ((5, "<B", 2), (18, "<H", 3), (16, "<H", 2)):
            with self.subTest(offset=offset):
                self.raw = shared_text_object()
                struct.pack_into(fmt, self.raw, offset, value)
                with self.assertRaises(ValueError):
                    self.compare()

    def test_overlapping_shared_section_symbols_and_duplicate_names_fail(self):
        for offset, value in ((0x260 + 4, 4), (0x260, 1)):
            with self.subTest(offset=offset):
                self.raw = shared_text_object()
                struct.pack_into("<I", self.raw, offset, value)
                with self.assertRaises(ValueError):
                    self.compare()

    def test_code_relocations_are_rejected_without_masking_even_if_words_look_exact(self):
        for kind in (0, 2, 4, 5, 6, 10, 255):
            with self.subTest(kind=kind):
                self.raw = shared_text_object()
                struct.pack_into("<I", self.raw, SHOFF + 6 * 40 + 28, 2)
                struct.pack_into("<4I", self.raw, 0x340, 0, (1 << 8) | kind, 16, (2 << 8) | kind)
                with self.assertRaises(ValueError):
                    self.compare()

    def test_noncode_pdr_relocation_records_still_require_valid_indices_and_bounds(self):
        for offset, value in ((0x340, 64), (0x344, (99 << 8) | 2),
                              (SHOFF + 6 * 40 + 20, 15),
                              (SHOFF + 6 * 40 + 24, 3)):
            with self.subTest(offset=offset):
                self.raw = shared_text_object()
                struct.pack_into("<I", self.raw, offset, value)
                with self.assertRaises(ValueError):
                    self.compare()

    def test_local_section_mips26_is_not_treated_as_supported_external_jal(self):
        first, second = bytes(self.raw[0x250:0x260]), bytes(self.raw[0x260:0x270])
        struct.pack_into("<IIIBBH", self.raw, 0x250, 0, 0, 0, 3, 0, 2)
        self.raw[0x260:0x270], self.raw[0x270:0x280] = first, second
        struct.pack_into("<I", self.raw, SHOFF + 4 * 40 + 20, 64)
        struct.pack_into("<I", self.raw, SHOFF + 4 * 40 + 28, 2)
        struct.pack_into("<I", self.raw, SHOFF + 6 * 40 + 28, 2)
        struct.pack_into("<4I", self.raw, 0x340, 0, (1 << 8) | 4, 16, (1 << 8) | 4)
        with self.assertRaises(ValueError):
            self.compare()


class FamilyRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.profiles_path = self.root / "profiles.json"
        self.report_path = self.root / "evidence/report.json"
        self.source = self.write("bench/original.c", b"/* Invented header-free source fixture. */\n")
        self.manifest_path = self.write("config/probes.json", json.dumps(manifest()).encode())
        self.reference = self.write("reference/fixture.elf", shared_text_object(reference=True))
        self.reference_lock = self.write("config/reference.json", json.dumps({
            "status": "active", "baseline_selected_by_user": True,
            "decrypted_executable": self.pin(self.reference)
        }).encode())
        self.legacy = self.write("config/legacy.json", b"{}")
        self.runner = self.write("tools/runner", b"invented runner")
        self.support = self.write("tools/support.dll", b"invented support")
        self.assembler = self.write("native/assembler", b"invented assembler")
        self.timeout = self.write("native/timeout", b"invented timeout")
        self.host_lib = self.write("native/library.so", b"invented host dependency")
        self.compilers = [self.write(f"tools/{name}", name.encode()) for name in ("gcc", "snc", "mw")]
        profiles = []
        for index, (name, family) in enumerate((("gcc", "GCC"), ("snc", "SNC"), ("mw", "Metrowerks"))):
            profile = {"id": name, "family": family, "version": "synthetic " + name,
                       "status": "runnable", "compiler": self.pin(self.compilers[index]),
                       "support_files": [self.pin(self.support)], "runner": self.pin(self.runner),
                       "mode": "gcc_backend_native" if name == "gcc" else "wibo_driver",
                       "common_flags": ["-nostdinc", "-c"],
                       "levels": [{"id": f"O{i}", "flags": [f"-O{i}"]} for i in range(4)]}
            if name == "gcc":
                profile.update(assembler=self.native_pin(self.assembler), assembler_flags=["-EL", "-O0"])
            profiles.append(profile)
        self.config = {"status": "profiles_frozen_before_target_scoring", "no_target_scores_observed": True,
                       "baseline_source": self.pin(self.source), "probe_manifest": self.pin(self.manifest_path),
                       "reference_lock": self.pin(self.reference_lock), "existing_candidate_config": self.pin(self.legacy),
                       "pre_score_evidence": [], "profiles": profiles,
                       "linux_dependencies": [self.native_pin(self.host_lib)],
                       "linux_utilities": [self.native_pin(self.timeout)]}
        self.save()
        self.object = bytes(shared_text_object())
        self.real_compile_profile = families.compile_profile
        patcher = mock.patch.object(families, "compile_profile", side_effect=self.compile_ok)
        self.compile = patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def pin(self, path):
        return identity(path.read_bytes(), path.relative_to(self.root).as_posix())

    def native_pin(self, path):
        return {"linux_path": str(path), "size": path.stat().st_size, "sha256": sha(path.read_bytes())}

    def save(self):
        self.profiles_path.write_text(json.dumps(self.config), encoding="utf-8")

    def compile_ok(self, profile, source, output, optimization_flags, **kwargs):
        self.assertFalse(output.exists(), "Every row must start without an object")
        self.assertEqual(source, self.source)
        self.assertEqual(profile["timeout_tool"], str(self.timeout))
        output.write_bytes(self.object)
        return {"returncode": 0, "stdout": "", "stderr": "", "artifacts": {}}

    def run_families(self):
        return families.run_families(root=self.root, profiles_path=self.profiles_path,
                                     report_path=self.report_path)

    def test_complete_fixed_four_level_family_cohorts(self):
        report = self.run_families()
        self.assertEqual(self.compile.call_count, 12)
        self.assertEqual(report["matched_progress"], 0)
        self.assertEqual(report["completed_profiles"], 3)
        self.assertEqual(report["completed_configurations"], 12)
        self.assertEqual(report["declared_configurations"], 12)
        self.assertEqual(json.loads(self.report_path.read_text()), report)
        for family in report["families"]:
            self.assertEqual(family["status"], "COMPLETE")
            self.assertEqual([r["setting"] for r in family["rows"]], ["O0", "O1", "O2", "O3"])
            self.assertEqual([a["setting"] for a in family["attempts"]], ["O0", "O1", "O2", "O3"])
            self.assertTrue(all(r["exact_probes"] == 2 for r in family["rows"]))
        self.assertEqual([c.args[3] for c in self.compile.call_args_list],
                         [[f"-O{i}"] for _ in range(3) for i in range(4)])

    def test_repeated_matrix_uses_fresh_objects_and_identical_pathfree_report(self):
        first = self.run_families()
        raw = self.report_path.read_bytes()
        second = self.run_families()
        self.assertEqual(first, second)
        self.assertEqual(raw, self.report_path.read_bytes())
        self.assertEqual(len({c.args[2] for c in self.compile.call_args_list}), 24)
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_failed_configuration_has_no_score_and_other_complete_configurations_remain(self):
        def fail(profile, source, output, flags, **kwargs):
            result = self.compile_ok(profile, source, output, flags, **kwargs)
            if profile["id"] == "gcc" and flags == ["-O2"]:
                result["returncode"] = 1
            return result
        self.compile.side_effect = fail
        report = self.run_families()
        self.assertEqual(report["completed_profiles"], 2)
        self.assertEqual(report["partial_profiles"], 1)
        self.assertEqual(report["completed_configurations"], 11)
        self.assertEqual(report["declared_configurations"], 12)
        bad = report["families"][0]
        self.assertEqual(bad["status"], "INCOMPLETE_SETTINGS")
        self.assertEqual([r["setting"] for r in bad["rows"]], ["O0", "O1", "O3"])
        self.assertTrue(all(len(r["comparisons"]) == 2 for r in bad["rows"]))
        self.assertEqual(bad["failed_setting"], "O2")
        self.assertEqual(self.compile.call_count, 12)
        self.assertEqual([a["setting"] for a in bad["attempts"]], ["O0", "O1", "O2", "O3"])
        self.assertTrue(all("exact_probes" not in a and "comparisons" not in a for a in bad["attempts"]))
        self.assertTrue(all(x["status"] == "COMPLETE" for x in report["families"][1:]))

    def test_warning_missing_timeout_bad_elf_and_unsupported_relocation_have_no_configuration_score(self):
        for failure in ("warning", "missing", "timeout", "bad_elf", "code_relocation"):
            with self.subTest(failure=failure):
                self.report_path = self.root / "evidence" / (failure + ".json")
                def fail(profile, source, output, flags, **kwargs):
                    if profile["id"] != "gcc" or flags != ["-O1"]:
                        return self.compile_ok(profile, source, output, flags, **kwargs)
                    if failure == "timeout":
                        raise subprocess.TimeoutExpired("invented", 20)
                    if failure == "missing":
                        return {"returncode": 0, "stdout": "", "stderr": ""}
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if failure == "warning":
                        result["stderr"] = "Warning: invented issue"
                    elif failure == "bad_elf":
                        output.write_bytes(b"not ELF")
                    else:
                        bad = shared_text_object()
                        struct.pack_into("<I", bad, SHOFF + 6 * 40 + 28, 2)
                        struct.pack_into("<4I", bad, 0x340, 0, (1 << 8) | 5, 16, (2 << 8) | 5)
                        output.write_bytes(bad)
                    return result
                self.compile.side_effect = fail
                report = self.run_families()
                self.assertEqual(report["families"][0]["status"], "INCOMPLETE_SETTINGS")
                self.assertEqual([r["setting"] for r in report["families"][0]["rows"]], ["O0", "O2", "O3"])
                self.assertEqual(report["completed_profiles"], 2)

    def test_family_with_all_four_configurations_rejected_has_no_score(self):
        def fail(profile, source, output, flags, **kwargs):
            result = self.compile_ok(profile, source, output, flags, **kwargs)
            if profile["id"] == "gcc":
                result["returncode"] = 1
            return result
        self.compile.side_effect = fail
        report = self.run_families()
        family = report["families"][0]
        self.assertEqual(family["status"], "UNAVAILABLE_NO_SCORE")
        self.assertEqual(family["rows"], [])
        self.assertEqual(len(family["attempts"]), 4)
        self.assertEqual(self.compile.call_count, 12)

    def test_explicit_unavailable_profile_is_not_executed_or_given_zero_score(self):
        self.config["profiles"][0].update(status="unavailable", reason="Invented dependency unavailable")
        self.save()
        report = self.run_families()
        self.assertEqual(self.compile.call_count, 8)
        row = report["families"][0]
        self.assertEqual(row["status"], "UNAVAILABLE_NO_SCORE")
        self.assertEqual(row["rows"], [])
        self.assertIn("reason", row)
        self.assertNotIn("exact_probes", row)

    def test_invalid_freeze_profiles_or_levels_fail_before_compilation(self):
        original = copy.deepcopy(self.config)
        bad_configs = []
        for field, value in (("status", "pending"), ("no_target_scores_observed", False), ("profiles", [])):
            bad = copy.deepcopy(original)
            bad[field] = value
            bad_configs.append(bad)
        bad = copy.deepcopy(original)
        bad["profiles"].append(bad["profiles"][0])
        bad_configs.append(bad)
        for key, value in (("levels", [{"id": "O5", "flags": ["-O5"]}]), ("mode", "PATH_fallback")):
            bad = copy.deepcopy(original)
            bad["profiles"][0][key] = value
            bad_configs.append(bad)
        for bad in bad_configs:
            self.config = bad
            self.save()
            with self.assertRaises(ValueError):
                self.run_families()
            self.compile.assert_not_called()
            self.assertFalse(self.report_path.exists())

    def test_local_subtool_and_native_dependency_pins_fail_globally(self):
        for path in (self.source, self.manifest_path, self.reference_lock, self.legacy,
                     self.runner, self.compilers[0], self.support, self.assembler, self.timeout,
                     self.host_lib, self.reference):
            with self.subTest(path=path.name):
                original = path.read_bytes()
                path.write_bytes(original + b"changed")
                with self.assertRaises(ValueError):
                    self.run_families()
                self.compile.assert_not_called()
                self.assertFalse(self.report_path.exists())
                path.write_bytes(original)

    def test_changed_input_or_freeze_during_compilation_invalidates_entire_report(self):
        for path in (self.source, self.manifest_path, self.reference_lock, self.profiles_path,
                     self.compilers[0], self.support, self.assembler, self.timeout, self.host_lib,
                     self.reference):
            with self.subTest(path=path.name):
                original = path.read_bytes()
                def mutate(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    path.write_bytes(original + b"changed")
                    return result
                self.compile.side_effect = mutate
                with self.assertRaises(ValueError):
                    self.run_families()
                self.assertFalse(self.report_path.exists())
                path.write_bytes(original)

    def test_unpinned_or_relative_timeout_cannot_use_path_fallback(self):
        for utilities in ([], [{**self.native_pin(self.timeout), "linux_path": "timeout"}]):
            self.config["linux_utilities"] = utilities
            self.save()
            with self.assertRaises(ValueError):
                self.run_families()
            self.compile.assert_not_called()
            self.assertFalse(self.report_path.exists())

    def test_report_conflicts_and_input_aliases_preserve_files(self):
        self.report_path.parent.mkdir()
        self.report_path.write_bytes(b"valuable evidence")
        with self.assertRaises(ValueError):
            self.run_families()
        self.assertEqual(self.report_path.read_bytes(), b"valuable evidence")
        for path in (self.source, self.manifest_path, self.reference_lock, self.profiles_path,
                     self.runner, self.compilers[0], self.support, self.reference):
            with self.subTest(path=path.name):
                original = path.read_bytes()
                self.report_path = path
                with self.assertRaises(ValueError):
                    self.run_families()
                self.assertEqual(path.read_bytes(), original)

    def test_driver_invocation_uses_pinned_absolute_timeout_and_empty_stdin(self):
        profile = dict(self.config["profiles"][1], timeout_tool=str(self.timeout))
        output = self.root / "fresh.o"
        result = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        with mock.patch.object(families.subprocess, "run", return_value=result) as run:
            actual = self.real_compile_profile(profile, self.source, output, ["-O2"], root=self.root, timeout=3)
        command = run.call_args.args[0]
        self.assertEqual(command[:3], [str(self.timeout), "3s", str(self.runner)])
        self.assertEqual(command[3], str(self.compilers[1]))
        self.assertIn("-O2", command)
        self.assertIs(run.call_args.kwargs["stdin"], subprocess.DEVNULL)
        self.assertLessEqual(run.call_args.kwargs["timeout"], 8)
        self.assertFalse(run.call_args.kwargs.get("shell", False))
        self.assertEqual(actual["returncode"], 0)

    def test_driver_refuses_preexisting_object_before_invocation(self):
        profile = dict(self.config["profiles"][1], timeout_tool=str(self.timeout))
        output = self.write("stale.o", self.object)
        with mock.patch.object(families.subprocess, "run") as run:
            with self.assertRaises(ValueError):
                self.real_compile_profile(profile, self.source, output, ["-O2"], root=self.root, timeout=3)
        run.assert_not_called()
        self.assertEqual(output.read_bytes(), self.object)


@unittest.skipUnless(os.name == "posix", "Native GCC staging controls run under WSL/Linux")
class NativeGccStagingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.source = self.root / "original_fixture.c"
        self.source_bytes = b"/* Invented staging fixture. */\nint f(void) { return 1; }\n"
        self.source.write_bytes(self.source_bytes)
        self.profile = {"mode": "gcc_backend_native", "timeout_tool": "/pinned/timeout",
                        "compiler": {"relative_path": "tools/cc1"},
                        "common_flags": ["-quiet", "-nostdinc"],
                        "assembler": {"linux_path": "/pinned/assembler"},
                        "assembler_flags": ["-EL", "-O0"]}
        self.assembly = b".set noreorder\n.text\nf:\n jr $ra\n nop\n"
        self.mutation = None
        self.stages = []

    def stage(self, command, **kwargs):
        cwd = Path(kwargs["cwd"])
        self.stages.append(command[2])
        self.assertTrue(cwd.is_relative_to(Path("/tmp").resolve()))
        self.assertEqual(command[:2], ["/pinned/timeout", "2s"])
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertFalse(kwargs.get("shell", False))
        if command[2] == str(self.root / "tools/cc1"):
            self.assertEqual(command[-1], self.source.name)
            self.assertEqual((cwd / self.source.name).read_bytes(), self.source_bytes)
            (cwd / command[command.index("-o") + 1]).write_bytes(self.assembly)
        else:
            self.assertEqual(command[2], "/pinned/assembler")
            assembly = Path(command[-1])
            self.assertEqual(assembly.read_bytes(), self.assembly)
            Path(command[command.index("-o") + 1]).write_bytes(b"invented object bytes")
            if self.mutation == "source":
                (cwd / self.source.name).write_bytes(b"altered staged source")
            elif self.mutation == "assembly":
                assembly.write_bytes(b"altered assembly")
        return subprocess.CompletedProcess(command, 0, stdout="", stderr="")

    def test_native_staging_preserves_source_basename_bytes_and_fixed_subtools(self):
        with mock.patch.object(families.subprocess, "run", side_effect=self.stage):
            result = families.compile_profile(self.profile, self.source, self.root / "out.o", ["-O1"],
                                              root=self.root, timeout=2)
        self.assertEqual(result["returncode"], 0)
        self.assertEqual(result["artifacts"]["assembly_sha256"], sha(self.assembly))
        self.assertEqual(self.stages, [str(self.root / "tools/cc1"), "/pinned/assembler"])
        self.assertEqual(self.source.read_bytes(), self.source_bytes)

    def test_assembler_cannot_change_staged_source_or_assembly_silently(self):
        for mutation in ("source", "assembly"):
            with self.subTest(mutation=mutation):
                self.mutation = mutation
                with mock.patch.object(families.subprocess, "run", side_effect=self.stage):
                    with self.assertRaises(ValueError):
                        families.compile_profile(self.profile, self.source, self.root / (mutation + ".o"),
                                                 ["-O1"], root=self.root, timeout=2)
                self.assertEqual(self.source.read_bytes(), self.source_bytes)


if __name__ == "__main__":
    unittest.main()
