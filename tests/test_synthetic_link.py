"""Invented ELF/link controls, never real compiler or linker execution.

These validate evidence and failures; they are not a game build or the matching
gate's eighteen negative checks. Native subprocesses are mocked throughout.
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

from scripts import bench_synthetic_link as link


SHOFF = 0x300
ADDRESS = 0x08804000
CODE = struct.pack("<3I", 0x24820001, 0x03e00008, 0)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def pin(data, path):
    return {"relative_path": path, "size": len(data), "sha256": sha(data)}


def fixture_elf(*, linked=False):
    """Create a single defined function, raw comment bytes and explicit mapping."""
    raw = bytearray(0x600)
    names = b"\0.shstrtab\0.text\0.strtab\0.symtab\0.comment\0.pdr\0.rel.pdr\0"
    strings = b"\0family_smoke\0"
    comment = b"\0Invented compiler\xff\0"
    raw[0x100:0x100 + len(names)] = names
    raw[0x180:0x18c] = CODE
    raw[0x1b0:0x1b0 + len(strings)] = strings
    raw[0x240:0x240 + len(comment)] = comment
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0,
                     b"\x7fELF\x01\x01\x01" + bytes(9), 2 if linked else 1, 8, 1,
                     ADDRESS if linked else 0, 52 if linked else 0, SHOFF, 0x10843001,
                     52, 32 if linked else 0, 1 if linked else 0, 40, 8, 1)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (names.index(b".shstrtab"), 3, 0, 0, 0x100, len(names), 0, 0, 1, 0),
                (names.index(b".text"), 1, 6, ADDRESS if linked else 0, 0x180, 16, 0, 0, 16, 0),
                (names.index(b".strtab"), 3, 0, 0, 0x1b0, len(strings), 0, 0, 1, 0),
                (names.index(b".symtab"), 2, 0, 0, 0x200, 32, 3, 1, 4, 16),
                (names.index(b".comment"), 1, 0, 0, 0x240, len(comment), 0, 0, 1, 0),
                (names.index(b".pdr"), 1, 0, 0, 0x270, 4, 0, 0, 4, 0),
                (names.index(b".rel.pdr"), 9, 0, 0, 0x280, 8, 4, 6, 4, 8)]
    for index, section in enumerate(sections):
        struct.pack_into("<10I", raw, SHOFF + index * 40, *section)
    struct.pack_into("<IIIBBH", raw, 0x210, 1, ADDRESS if linked else 0, len(CODE), 0x12, 0, 2)
    struct.pack_into("<II", raw, 0x280, 0, (1 << 8) | 2)
    if linked:
        struct.pack_into("<8I", raw, 52, 1, 0x180, ADDRESS, ADDRESS, 16, 16, 5, 16)
    return raw


class SyntheticElfTests(unittest.TestCase):
    def test_preserved_complete_function_and_raw_metadata_are_separate_observations(self):
        before, after = fixture_elf(), fixture_elf(linked=True)
        struct.pack_into("<I", after, 36, 0x10a23001)
        after[0x241] ^= 1
        result = link.compare_linked_fixture(before, after, ADDRESS)
        self.assertEqual(result["status"], "PRESERVED")
        self.assertTrue(result["complete_function_bytes_equal"])
        self.assertFalse(result["flags_equal"])
        self.assertFalse(result["comments_equal"])
        self.assertEqual(result["input"]["comments"], [b"\0Invented compiler\xff\0".hex()])
        self.assertEqual(result["output"]["function"]["size"], len(CODE))

    def test_changed_word_or_extra_function_padding_is_a_code_changed_finding(self):
        for mode in ("word", "size"):
            with self.subTest(mode=mode):
                after = fixture_elf(linked=True)
                if mode == "word":
                    after[0x180] ^= 1
                else:
                    struct.pack_into("<I", after, 0x210 + 8, 16)
                result = link.compare_linked_fixture(fixture_elf(), after, ADDRESS)
                self.assertEqual(result["status"], "CODE_CHANGED")
                self.assertFalse(result["complete_function_bytes_equal"])

    def test_nonzero_symbol_offset_maps_to_its_actual_entry_and_file_bytes(self):
        before, after = fixture_elf(), fixture_elf(linked=True)
        for raw in (before, after):
            raw[0x180:0x190] = bytes(4) + CODE
        struct.pack_into("<I", before, 0x210 + 4, 4)
        struct.pack_into("<I", after, 0x210 + 4, ADDRESS + 4)
        struct.pack_into("<I", after, 24, ADDRESS + 4)
        result = link.compare_linked_fixture(before, after, ADDRESS + 4)
        self.assertEqual(result["status"], "PRESERVED")
        self.assertEqual(result["output"]["function"]["section_offset"], 4)

    def test_wrong_type_machine_endian_and_truncated_tables_are_rejected(self):
        for offset, fmt, value in ((16, "<H", 1), (18, "<H", 3), (5, "<B", 2),
                                    (32, "<I", 0x5f0)):
            with self.subTest(offset=offset):
                data = fixture_elf(linked=True)
                struct.pack_into(fmt, data, offset, value)
                with self.assertRaises(ValueError):
                    link.inspect_fixture(data, 2)

    def test_missing_duplicate_zero_size_and_nonexecutable_functions_are_rejected(self):
        for offset, fmt, value in ((0x210, "<I", 0), (0x210 + 8, "<I", 0),
                                    (0x210 + 8, "<I", 10), (0x210 + 8, "<I", 20),
                                    (SHOFF + 2 * 40 + 8, "<I", 2), (0x210 + 14, "<H", 0)):
            with self.subTest(offset=offset, value=value):
                data = fixture_elf()
                struct.pack_into(fmt, data, offset, value)
                with self.assertRaises(ValueError):
                    link.inspect_fixture(data, 1)
        data = fixture_elf()
        data[0x220:0x230] = data[0x210:0x220]
        struct.pack_into("<I", data, SHOFF + 4 * 40 + 20, 48)
        with self.assertRaises(ValueError):
            link.inspect_fixture(data, 1)

    def test_entry_alignment_address_overflow_and_declared_entry_mismatch_fail(self):
        after = fixture_elf(linked=True)
        struct.pack_into("<I", after, 24, ADDRESS + 4)
        with self.assertRaises(ValueError):
            link.inspect_fixture(after, 2)
        for address in (-4, ADDRESS + 1, 2**32, ADDRESS + 4):
            with self.subTest(address=address):
                with self.assertRaises(ValueError):
                    link.compare_linked_fixture(fixture_elf(), fixture_elf(linked=True), address)
        after = fixture_elf(linked=True)
        for offset in (24, SHOFF + 2 * 40 + 12, 0x210 + 4, 52 + 8):
            struct.pack_into("<I", after, offset, 0xfffffff8)
        with self.assertRaises(ValueError):
            link.inspect_fixture(after, 2)

    def test_load_mapping_requires_file_coverage_correct_offset_and_execute_permission(self):
        for offset, value in ((44, 0), (52 + 4, 0x190), (52 + 16, 8), (52 + 24, 4)):
            with self.subTest(offset=offset, value=value):
                after = fixture_elf(linked=True)
                if offset == 44:
                    struct.pack_into("<H", after, offset, value)
                else:
                    struct.pack_into("<I", after, offset, value)
                with self.assertRaises(ValueError):
                    link.inspect_fixture(after, 2)

    def test_duplicate_and_partial_load_mappings_are_ambiguous(self):
        for second in ((1, 0x180, ADDRESS, ADDRESS, 16, 16, 5, 16),
                       (1, 0x184, ADDRESS + 4, ADDRESS + 4, 4, 4, 5, 4),
                       (1, 0x184, ADDRESS + 4, ADDRESS + 4, 0, 4, 5, 4)):
            with self.subTest(second=second):
                after = fixture_elf(linked=True)
                struct.pack_into("<H", after, 44, 2)
                struct.pack_into("<8I", after, 84, *second)
                with self.assertRaises(ValueError):
                    link.inspect_fixture(after, 2)

    def test_duplicate_or_partially_overlapping_allocated_sections_are_ambiguous(self):
        for address, size in ((ADDRESS, 16), (ADDRESS + 4, 4)):
            with self.subTest(address=address):
                after = fixture_elf(linked=True)
                # Reuse the otherwise unrelated metadata section as an alias.
                struct.pack_into("<I", after, SHOFF + 6 * 40 + 8, 6)
                struct.pack_into("<I", after, SHOFF + 6 * 40 + 12, address)
                struct.pack_into("<I", after, SHOFF + 6 * 40 + 20, size)
                with self.assertRaises(ValueError):
                    link.inspect_fixture(after, 2)

    def test_code_relocations_and_malformed_noncode_records_are_rejected(self):
        changes = [(SHOFF + 7 * 40 + 28, 2), (0x280, 4), (0x284, (99 << 8) | 2),
                   (SHOFF + 7 * 40 + 20, 7), (SHOFF + 7 * 40 + 24, 3)]
        for offset, value in changes:
            with self.subTest(offset=offset, value=value):
                data = fixture_elf()
                struct.pack_into("<I", data, offset, value)
                with self.assertRaises(ValueError):
                    link.inspect_fixture(data, 1)


class SyntheticLinkRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.config_path = self.root / "config/link.json"
        self.report_path = self.root / "evidence/report.json"
        self.source = self.write("bench/smoke.c", b"/* Invented single-function source. */\n")
        self.layout = self.write("bench/layout.ld", b"ENTRY(family_smoke)\nSECTIONS { .text 0x08804000 : { *(.text) } }\n")
        self.linker = self.write("tools/pspld.exe", b"invented linker")
        self.support = self.write("tools/support.dll", b"invented support")
        self.compiler = self.write("tools/compiler", b"invented compiler")
        self.runner = self.write("tools/runner", b"invented runner")
        self.timeout = self.write("native/timeout", b"invented timeout")
        self.native = self.write("native/windows.dll", b"invented Windows dependency")
        self.baseline = self.write("bench/unused.c", b"/* Invented unused old bench. */\n")
        self.manifest = self.write("config/unused-probes.json", b"{}")
        self.reference = self.write("config/unused-reference.json", b"{}")
        self.legacy = self.write("config/legacy.json", b"{}")
        profiles = [{"id": name, "family": name, "mode": "wibo_driver",
                     "compiler": self.pin(self.compiler), "runner": self.pin(self.runner),
                     "support_files": [self.pin(self.support)], "common_flags": ["-c"]}
                    for name in ("gcc", "snc", "mw")]
        self.families = {"baseline_source": self.pin(self.baseline), "probe_manifest": self.pin(self.manifest),
                         "reference_lock": self.pin(self.reference), "existing_candidate_config": self.pin(self.legacy),
                         "pre_score_evidence": [], "profiles": profiles, "linux_dependencies": [],
                         "linux_utilities": [self.native_pin(self.timeout)]}
        self.family_path = self.write("config/families.json", json.dumps(self.families).encode())
        self.config = {"status": "frozen_before_link_outputs", "no_link_outputs_observed": True,
                       "family_profiles": self.pin(self.family_path), "source": self.pin(self.source),
                       "layout": self.pin(self.layout), "linker": self.pin(self.linker),
                       "support_files": [self.pin(self.support)], "native_windows_dependencies": [self.native_pin(self.native)],
                       "prelink_evidence": [], "profile_ids": [p["id"] for p in profiles],
                       "optimization": ["-O0"], "entry_symbol": "family_smoke", "text_address": ADDRESS,
                       "no_libraries": True, "runner": "wsl_native_windows_interop", "windows_project_root": "D:\\invented-project",
                       "common_link_flags": ["-comment", "-e", "family_smoke", "-Wall", "-Werror", "-t"],
                       "command_template": ["{linker}", "-comment", "-e", "family_smoke", "-Wall", "-Werror", "-t",
                                            "-T", "{layout}", "-Map", "{map}", "-o", "{output}", "{object}"],
                       "timeout_seconds": 2}
        self.save()
        self.real_link = link.link_fixture
        compile_patch = mock.patch.object(link, "compile_profile", side_effect=self.compile_ok)
        linker_patch = mock.patch.object(link, "link_fixture", side_effect=self.link_ok)
        self.compile = compile_patch.start()
        self.linker_mock = linker_patch.start()
        self.addCleanup(compile_patch.stop)
        self.addCleanup(linker_patch.stop)

    def write(self, path, data):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        return destination

    def pin(self, path):
        return pin(path.read_bytes(), path.relative_to(self.root).as_posix())

    def native_pin(self, path):
        return {"linux_path": str(path), "size": path.stat().st_size, "sha256": sha(path.read_bytes())}

    def save(self):
        self.config_path.write_text(json.dumps(self.config), encoding="utf-8")

    def compile_ok(self, profile, source, output, flags, **kwargs):
        self.assertFalse(output.exists())
        self.assertEqual(flags, ["-O0"])
        self.assertEqual(source, self.source)
        output.write_bytes(fixture_elf())
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def link_ok(self, config, obj, output, map_path, **kwargs):
        self.assertFalse(output.exists())
        self.assertFalse(map_path.exists())
        self.assertEqual(obj.read_bytes(), fixture_elf())
        output.write_bytes(fixture_elf(linked=True))
        map_path.write_text("Invented map; no library inputs.\n")
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def run_experiment(self):
        return link.run_experiment(root=self.root, config_path=self.config_path, report_path=self.report_path)

    def test_three_synthetic_preserved_outcomes_use_same_layout_flags_and_original_inputs(self):
        report, directory = self.run_experiment()
        self.assertEqual(self.compile.call_count, 3)
        self.assertEqual(self.linker_mock.call_count, 3)
        self.assertEqual(report["preserved_functions"], 3)
        self.assertEqual(report["matched_progress"], 0)
        self.assertTrue(all(r["status"] == "PRESERVED" for r in report["families"]))
        self.assertEqual(json.loads(self.report_path.read_text()), report)
        self.assertEqual(len(list(directory.glob("*.o"))), 3)

    def test_repeat_runs_use_fresh_objects_and_identical_pathfree_reports(self):
        first, a = self.run_experiment()
        raw = self.report_path.read_bytes()
        second, b = self.run_experiment()
        self.assertNotEqual(a, b)
        self.assertEqual(first, second)
        self.assertEqual(self.report_path.read_bytes(), raw)
        self.assertEqual(len({call.args[2] for call in self.compile.call_args_list}), 6)
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_compile_failures_warnings_timeouts_and_invalid_objects_never_reach_linker(self):
        for mode in ("nonzero", "warning", "timeout", "missing", "invalid"):
            with self.subTest(mode=mode):
                self.report_path = self.root / "evidence" / (mode + ".json")
                def fail(profile, source, output, flags, **kwargs):
                    if mode == "timeout":
                        raise subprocess.TimeoutExpired("invented", 2)
                    if mode == "missing":
                        return {"returncode": 0, "stdout": "", "stderr": ""}
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if mode == "nonzero": result["returncode"] = 1
                    elif mode == "warning": result["stderr"] = "Warning: invented"
                    else: output.write_bytes(b"not ELF")
                    return result
                self.compile.side_effect = fail
                report, _ = self.run_experiment()
                self.assertEqual(report["preserved_functions"], 0)
                self.assertTrue(all(row["status"] != "PRESERVED" for row in report["families"]))
                self.linker_mock.assert_not_called()

    def test_nonzero_or_warning_link_is_not_success_even_with_valid_output(self):
        for mode in ("nonzero", "warning"):
            with self.subTest(mode=mode):
                self.report_path = self.root / "evidence" / (mode + ".json")
                def fail(*args, **kwargs):
                    result = self.link_ok(*args, **kwargs)
                    result["returncode"] = 1 if mode == "nonzero" else 0
                    result["stderr"] = "Warning: invented" if mode == "warning" else "link failed"
                    return result
                self.linker_mock.side_effect = fail
                report, _ = self.run_experiment()
                self.assertEqual(report["preserved_functions"], 0)
                self.assertTrue(all(r["status"] == "LINK_FAILED" for r in report["families"]))

    def test_missing_link_output_map_or_timeout_is_retained_as_explicit_failure(self):
        for mode in ("output", "map", "timeout"):
            with self.subTest(mode=mode):
                self.report_path = self.root / "evidence" / (mode + ".json")
                def fail(config, obj, output, map_path, **kwargs):
                    if mode == "timeout": raise subprocess.TimeoutExpired("invented", 2)
                    result = self.link_ok(config, obj, output, map_path, **kwargs)
                    (output if mode == "output" else map_path).unlink()
                    return result
                self.linker_mock.side_effect = fail
                report, _ = self.run_experiment()
                self.assertEqual(report["preserved_functions"], 0)
                self.assertEqual(len(report["families"]), 3)

    def test_linked_code_change_and_wrong_mapping_are_findings_without_input_rewriting(self):
        for mode in ("code", "entry"):
            with self.subTest(mode=mode):
                self.report_path = self.root / "evidence" / (mode + ".json")
                def change(config, obj, output, map_path, **kwargs):
                    result = self.link_ok(config, obj, output, map_path, **kwargs)
                    data = bytearray(output.read_bytes())
                    if mode == "code": data[0x180] ^= 1
                    else: struct.pack_into("<I", data, 24, ADDRESS + 4)
                    output.write_bytes(data)
                    return result
                self.linker_mock.side_effect = change
                report, directory = self.run_experiment()
                self.assertEqual(report["preserved_functions"], 0)
                self.assertTrue(all(row["status"] == ("CODE_CHANGED" if mode == "code" else "VALIDATION_FINDING")
                                    for row in report["families"]))
                self.assertTrue(all(p.read_bytes() == fixture_elf() for p in directory.glob("*.o")))

    def test_linker_cannot_mutate_input_object_and_still_claim_preservation(self):
        def mutate(config, obj, output, map_path, **kwargs):
            result = self.link_ok(config, obj, output, map_path, **kwargs)
            obj.write_bytes(b"modified object")
            return result
        self.linker_mock.side_effect = mutate
        report, _ = self.run_experiment()
        self.assertEqual(report["preserved_functions"], 0)
        self.assertTrue(all(r["status"] == "VALIDATION_FINDING" for r in report["families"]))

    def test_wrong_freeze_or_profile_scope_fails_before_tools(self):
        for field, value in (("status", "draft"), ("no_link_outputs_observed", False),
                             ("optimization", ["-O1"]), ("no_libraries", False),
                             ("profile_ids", ["gcc"]), ("runner", "unreviewed_runner")):
            with self.subTest(field=field):
                original = copy.deepcopy(self.config)
                self.config[field] = value
                self.save()
                with self.assertRaises(ValueError): self.run_experiment()
                self.compile.assert_not_called()
                self.linker_mock.assert_not_called()
                self.config = original

    def test_every_local_and_native_pin_is_enforced_before_linking(self):
        for path in (self.source, self.layout, self.linker, self.support, self.family_path,
                     self.compiler, self.runner, self.timeout, self.native):
            with self.subTest(path=path.name):
                before = path.read_bytes()
                path.write_bytes(before + b"changed")
                with self.assertRaises(ValueError): self.run_experiment()
                self.compile.assert_not_called()
                self.linker_mock.assert_not_called()
                path.write_bytes(before)

    def test_changed_profile_or_inputs_during_linking_invalidates_outer_report(self):
        for path in (self.source, self.layout, self.linker, self.support, self.family_path,
                     self.compiler, self.native, self.config_path):
            with self.subTest(path=path.name):
                before = path.read_bytes()
                def change(*args, **kwargs):
                    result = self.link_ok(*args, **kwargs)
                    path.write_bytes(before + b"changed")
                    return result
                self.linker_mock.side_effect = change
                with self.assertRaises(ValueError): self.run_experiment()
                self.assertFalse(self.report_path.exists())
                path.write_bytes(before)

    def test_existing_report_and_input_aliases_are_preserved(self):
        self.report_path.parent.mkdir()
        self.report_path.write_bytes(b"valuable prior evidence")
        with self.assertRaises(ValueError): self.run_experiment()
        self.assertEqual(self.report_path.read_bytes(), b"valuable prior evidence")
        for path in (self.source, self.layout, self.linker, self.support, self.family_path,
                     self.compiler, self.config_path):
            with self.subTest(path=path.name):
                self.report_path = path
                before = path.read_bytes()
                with self.assertRaises(ValueError): self.run_experiment()
                self.assertEqual(path.read_bytes(), before)

    def test_native_link_command_is_identical_and_has_empty_stdin_timeout_and_no_shell(self):
        obj = self.write("build/input.o", fixture_elf())
        output, map_path = obj.with_suffix(".elf"), obj.with_suffix(".map")
        with mock.patch.object(link.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, "", "")) as run:
            self.real_link(self.config, obj, output, map_path, root=self.root)
        command = run.call_args.args[0]
        self.assertEqual(command[0], str(self.linker))
        self.assertEqual(command[1:7], self.config["common_link_flags"])
        self.assertIs(run.call_args.kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(run.call_args.kwargs["timeout"], 2)
        self.assertFalse(run.call_args.kwargs.get("shell", False))
        output.write_bytes(b"existing output")
        with self.assertRaises(ValueError): self.real_link(self.config, obj, output, map_path, root=self.root)


if __name__ == "__main__":
    unittest.main()
