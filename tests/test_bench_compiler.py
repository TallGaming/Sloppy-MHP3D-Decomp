"""Compiler-investigation checks using invented ELF/probe/tool fixtures only.

No real compiler or game code is executed. These tests do not implement the
matching build gate's 18 negatives and never confer source-match credit.
"""

import hashlib
import io
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts import bench_compiler as bench
from scripts.elf32 import Elf32


ALPHA = bytes.fromhex("0800e00300000000")
BETA = bytes.fromhex("0800e00301000224")
SHOFF = 0x400


def pin(data, relative_path=None):
    value = {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    if relative_path is not None:
        value["relative_path"] = relative_path
    return value


def synthetic_elf(*, reference=False):
    """Use repeated .text names and indexed symbols, as Metrowerks objects do."""
    raw = bytearray(0x600)
    names = b"\0.shstrtab\0.text\0.strtab\0.symtab\0.rel.text\0.comment\0"
    raw[0x100:0x100 + len(names)] = names
    raw[0x200:0x208], raw[0x210:0x218] = ALPHA, BETA
    symbols = b"\0probe_alpha\0probe_beta\0"
    raw[0x240:0x240 + len(symbols)] = symbols
    comment = b"Synthetic compiler\0"
    raw[0x340:0x340 + len(comment)] = comment
    ident = b"\x7fELF\x01\x01\x01" + bytes(9)
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0, ident, 2 if reference else 1,
                     8, 1, 0x08804000 if reference else 0, 0, SHOFF,
                     0x10970001, 52, 0, 0, 40, 8, 1)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (names.index(b".shstrtab"), 3, 0, 0, 0x100, len(names), 0, 0, 1, 0),
                (names.index(b".text"), 1, 6, 0x08804000 if reference else 0,
                 0x200, 8, 0, 0, 4, 0),
                (names.index(b".text"), 1, 6, 0x08804010 if reference else 0,
                 0x210, 8, 0, 0, 4, 0),
                (names.index(b".strtab"), 3, 0, 0, 0x240, len(symbols), 0, 0, 1, 0),
                (names.index(b".symtab"), 2, 0, 0, 0x280, 48, 4, 1, 4, 16),
                (names.index(b".rel.text"), 9, 0, 0, 0x300, 0, 5, 2, 4, 8),
                (names.index(b".comment"), 1, 0, 0, 0x340, len(comment), 0, 0, 1, 0)]
    for index, section in enumerate(sections):
        struct.pack_into("<10I", raw, SHOFF + index * 40, *section)
    for index, (name, value, section) in enumerate(((1, 0x08804000 if reference else 0, 2),
                                                 (13, 0x08804010 if reference else 0, 3)), 1):
        struct.pack_into("<IIIBBH", raw, 0x280 + index * 16, name, value, 8, 0x12, 0, section)
    return raw


def manifest():
    probes = []
    for name, address, data in (("probe_alpha", 0x08804000, ALPHA),
                                ("probe_beta", 0x08804010, BETA)):
        probes.append({"name": name, "address": address, "size": len(data),
                       "target_sha256": pin(data)["sha256"], "category": "synthetic_control",
                       "boundary_evidence": "Invented complete return plus delay slot.",
                       "ownership": "unclassified synthetic fixture", "relocations": []})
    return {"schema_version": 1, "source": "bench/probes.c", "probes": probes}


class CompareObjectTests(unittest.TestCase):
    def setUp(self):
        self.object = synthetic_elf()
        self.reference = Elf32(synthetic_elf(reference=True))
        self.manifest = manifest()

    def compare(self, data=None):
        return bench.compare_object(bytes(self.object if data is None else data),
                                    self.reference, self.manifest)

    def test_exact_probe_sequences_use_distinct_section_indices(self):
        report = self.compare()
        self.assertEqual(report["object_sha256"], pin(self.object)["sha256"])
        self.assertEqual(report["compiler_comments"], ["Synthetic compiler"])
        self.assertEqual([p["name"] for p in report["comparisons"]],
                         ["probe_alpha", "probe_beta"])
        self.assertTrue(all(p["exact_probe_bytes"] for p in report["comparisons"]))
        self.assertTrue(all(p["first_difference"] is None for p in report["comparisons"]))

    def test_partial_byte_agreement_is_never_exact(self):
        self.object[0x214] ^= 1
        report = self.compare()
        self.assertTrue(report["comparisons"][0]["exact_probe_bytes"])
        self.assertFalse(report["comparisons"][1]["exact_probe_bytes"])
        self.assertEqual(report["comparisons"][1]["first_difference"], 4)

    def test_different_symbol_length_is_not_a_prefix_match(self):
        struct.pack_into("<I", self.object, SHOFF + 3 * 40 + 20, 12)
        struct.pack_into("<I", self.object, 0x2a0 + 8, 12)
        result = self.compare()["comparisons"][1]
        self.assertFalse(result["exact_probe_bytes"])
        self.assertEqual(result["compiled_size"], 12)
        self.assertEqual(result["first_difference"], 8)

    def test_object_requires_rel_and_mips_elf(self):
        for offset, value in ((16, 2), (18, 3)):
            with self.subTest(offset=offset):
                raw = bytearray(self.object)
                struct.pack_into("<H", raw, offset, value)
                with self.assertRaises(ValueError):
                    self.compare(raw)

    def test_missing_unexpected_duplicate_and_overlapping_symbols_fail(self):
        changes = [((0x2a0, "<I", 0),),  # Empty second symbol name.
                   ((0x2a0, "<I", 1),),  # Duplicate alpha, not dict overwrite.
                   ((0x2a0 + 14, "<H", 0),),  # Undefined/missing beta.
                   ((0x2a0 + 14, "<H", 2),)]  # Distinct names overlap .text index2.
        for edits in changes:
            with self.subTest(edits=edits):
                raw = bytearray(self.object)
                for offset, fmt, value in edits:
                    struct.pack_into(fmt, raw, offset, value)
                with self.assertRaises(ValueError):
                    self.compare(raw)

    def test_nonexecutable_out_of_bounds_unaligned_or_empty_functions_fail(self):
        changes = [(SHOFF + 2 * 40 + 8, "<I", 2),
                   (0x290 + 4, "<I", 4), (0x290 + 8, "<I", 0),
                   (0x290 + 8, "<I", 6)]
        for offset, fmt, value in changes:
            with self.subTest(offset=offset, value=value):
                raw = bytearray(self.object)
                struct.pack_into(fmt, raw, offset, value)
                with self.assertRaises(ValueError):
                    self.compare(raw)

    def test_rel_and_rela_code_relocations_cannot_be_called_exact(self):
        for kind, size in ((9, 8), (4, 12)):
            with self.subTest(kind=kind):
                raw = bytearray(self.object)
                struct.pack_into("<I", raw, SHOFF + 6 * 40 + 4, kind)
                struct.pack_into("<I", raw, SHOFF + 6 * 40 + 20, size)
                struct.pack_into("<I", raw, SHOFF + 6 * 40 + 36, size)
                struct.pack_into("<II", raw, 0x300, 0, (1 << 8) | 4)
                with self.assertRaises(ValueError):
                    self.compare(raw)

    def test_malformed_relocation_metadata_is_rejected_even_before_comparison(self):
        changes = [(SHOFF + 6 * 40 + 36, 4), (SHOFF + 6 * 40 + 24, 4),
                   (SHOFF + 6 * 40 + 28, 99), (0x304, (99 << 8) | 4),
                   (0x300, 8)]
        for offset, value in changes:
            with self.subTest(offset=offset, value=value):
                raw = bytearray(self.object)
                struct.pack_into("<I", raw, SHOFF + 6 * 40 + 20, 8)
                struct.pack_into("<II", raw, 0x300, 0, (1 << 8) | 4)
                struct.pack_into("<I", raw, offset, value)
                with self.assertRaises(ValueError):
                    self.compare(raw)

    def test_manifest_hash_ranges_names_and_relocation_policy_fail_closed(self):
        changes = [(0, "target_sha256", "0" * 64), (0, "address", 0x09900000),
                   (0, "size", 0), (0, "size", 6), (0, "relocations", [{"type": 4}]),
                   (1, "name", "probe_alpha"), (1, "address", 0x08804000)]
        for index, field, value in changes:
            with self.subTest(field=field, value=value):
                self.manifest = manifest()
                self.manifest["probes"][index][field] = value
                with self.assertRaises(ValueError):
                    self.compare()

    def test_empty_manifest_cannot_create_a_vacuous_exact_result(self):
        self.manifest["probes"] = []
        with self.assertRaises(ValueError):
            self.compare()


class BenchRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.report_path = self.root / "evidence/report.json"
        self.build = self.root / "build"
        self.config_path = self.root / "candidates.json"
        self.manifest_path = self.root / "probes.json"
        self.lock_path = self.root / "reference.json"
        self.object = bytes(synthetic_elf())
        self.manifest = manifest()
        source = b"/* Invented investigation probes. */\nvoid probe_alpha(void) {}\nvoid probe_beta(void) {}\n"
        self.source = self.write("bench/probes.c", source)
        self.elf = self.write("reference/fixture.elf", synthetic_elf(reference=True))
        self.runner = self.write("tools/runner", b"invented runner")
        self.compilers = [self.write("tools/first.exe", b"invented first compiler"),
                          self.write("tools/second.exe", b"invented second compiler")]
        self.support = self.write("tools/support.dll", b"invented compiler support")
        self.config = {"status": "investigation_only_not_locked",
                       "runner": {**pin(self.runner.read_bytes(), "tools/runner"),
                                  "environment": "WSL Ubuntu"},
                       "common_flags": ["-nostdinc", "-lang", "c", "-c"],
                       "settings": [{"id": "O0", "flags": ["-O0"]},
                                    {"id": "O1", "flags": ["-O1"]}],
                       "candidates": [{"id": "first", "compiler": pin(self.compilers[0].read_bytes(), "tools/first.exe"),
                                       "support_files": [pin(self.support.read_bytes(), "tools/support.dll")], "version": "synthetic1"},
                                      {"id": "second", "compiler": pin(self.compilers[1].read_bytes(), "tools/second.exe"),
                                       "support_files": [], "version": "synthetic2"}],
                       "source_sha256": pin(source)["sha256"]}
        self.lock = {"status": "active", "baseline_selected_by_user": True,
                     "decrypted_executable": pin(self.elf.read_bytes(), "reference/fixture.elf")}
        self.save_config()
        self.real_compile = bench.compile_probe
        self.compiler_patch = mock.patch.object(bench, "compile_probe", side_effect=self.compile_ok)
        self.compiler = self.compiler_patch.start()
        self.addCleanup(self.compiler_patch.stop)

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def save_config(self):
        self.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        self.config["manifest_sha256"] = pin(self.manifest_path.read_bytes())["sha256"]
        self.config_path.write_text(json.dumps(self.config), encoding="utf-8")
        self.lock_path.write_text(json.dumps(self.lock), encoding="utf-8")

    def compile_ok(self, compiler, runner, source, output, flags, **kwargs):
        self.assertFalse(output.exists(), "Object must be absent before compilation")
        output.write_bytes(self.object)
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def run_bench(self):
        return bench.run_bench(root=self.root, candidates_path=self.config_path,
                               manifest_path=self.manifest_path, lock_path=self.lock_path,
                               report_path=self.report_path, build_parent=self.build, timeout=2)

    def test_same_probe_source_and_whole_settings_for_all_candidates(self):
        report = self.run_bench()
        self.assertEqual(self.compiler.call_count, 4)
        self.assertEqual([call.args[4] for call in self.compiler.call_args_list],
                         [self.config["common_flags"] + setting["flags"]
                          for _ in self.compilers for setting in self.config["settings"]])
        self.assertTrue(all(call.args[2] == self.source for call in self.compiler.call_args_list))
        self.assertEqual(report["matched_progress"], 0)
        self.assertEqual(json.loads(self.report_path.read_text()), report)

    def test_empty_or_duplicate_candidate_setting_matrix_fails_before_compile(self):
        for collection in ("candidates", "settings"):
            original = self.config[collection]
            for value in ([], [original[0], original[0]]):
                with self.subTest(collection=collection, count=len(value)):
                    self.config[collection] = value
                    self.save_config()
                    with self.assertRaises(ValueError):
                        self.run_bench()
                    self.compiler.assert_not_called()
                    self.assertFalse(self.report_path.exists())
            self.config[collection] = original

    def test_repeat_matrix_uses_fresh_objects_and_identical_pathfree_reports(self):
        first = self.run_bench()
        data = self.report_path.read_bytes()
        second = self.run_bench()
        outputs = [call.args[3] for call in self.compiler.call_args_list]
        self.assertEqual(len(set(outputs)), 8)
        self.assertEqual(first, second)
        self.assertEqual(data, self.report_path.read_bytes())
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_inactive_reference_rejected_without_compiler_execution(self):
        self.lock["status"] = "rejected"
        self.save_config()
        with self.assertRaises(ValueError):
            self.run_bench()
        self.compiler.assert_not_called()
        self.assertFalse(self.report_path.exists())

    def test_every_pinned_input_is_verified_before_compile(self):
        for path in (self.source, self.elf, self.runner, self.compilers[0], self.support,
                     self.manifest_path):
            with self.subTest(path=path.name):
                before = path.read_bytes()
                path.write_bytes(before + b"changed")
                with self.assertRaises(ValueError):
                    self.run_bench()
                self.compiler.assert_not_called()
                self.assertFalse(self.report_path.exists())
                path.write_bytes(before)

    def test_missing_source_or_tool_never_uses_existing_objects(self):
        self.build.mkdir()
        (self.build / "stale.o").write_bytes(self.object)
        self.source.unlink()
        with self.assertRaises((ValueError, OSError)):
            self.run_bench()
        self.compiler.assert_not_called()
        self.assertFalse(self.report_path.exists())

    def test_compile_failure_rejects_even_valid_object_and_emits_no_report(self):
        def fail(*args, **kwargs):
            self.compile_ok(*args, **kwargs)
            return {"returncode": 1, "stdout": "", "stderr": "synthetic compiler failure"}
        self.compiler.side_effect = fail
        with self.assertRaises(ValueError):
            self.run_bench()
        self.assertFalse(self.report_path.exists())
        logs = list(self.build.rglob("*.log"))
        self.assertTrue(logs)
        self.assertIn("synthetic compiler failure", logs[0].read_text())

    def test_warning_rejects_even_valid_object_and_emits_no_report(self):
        def warn(*args, **kwargs):
            self.compile_ok(*args, **kwargs)
            return {"returncode": 0, "stdout": "", "stderr": "Warning : synthetic issue"}
        self.compiler.side_effect = warn
        with self.assertRaises(ValueError):
            self.run_bench()
        self.assertFalse(self.report_path.exists())

    def test_missing_object_does_not_fall_back_to_prior_build(self):
        self.build.mkdir()
        (self.build / "stale.o").write_bytes(self.object)
        self.compiler.side_effect = lambda *args, **kwargs: {"returncode": 0, "stdout": "", "stderr": ""}
        with self.assertRaises(ValueError):
            self.run_bench()
        self.assertFalse(self.report_path.exists())

    def test_timeout_emits_no_success_report(self):
        self.compiler.side_effect = subprocess.TimeoutExpired("synthetic", 2)
        with self.assertRaises((ValueError, subprocess.TimeoutExpired)):
            self.run_bench()
        self.assertFalse(self.report_path.exists())

    def test_changed_source_or_tools_during_matrix_prevents_report(self):
        for path in (self.source, self.runner, self.compilers[0], self.support, self.manifest_path,
                     self.config_path, self.elf):
            with self.subTest(path=path.name):
                original = path.read_bytes()
                def mutate(*args, **kwargs):
                    result = self.compile_ok(*args, **kwargs)
                    path.write_bytes(original + b"changed")
                    return result
                self.compiler.side_effect = mutate
                with self.assertRaises(ValueError):
                    self.run_bench()
                self.assertFalse(self.report_path.exists())
                path.write_bytes(original)

    def test_unexpected_function_or_invalid_object_cannot_publish_partial_scores(self):
        for data in (b"not ELF", bytes(synthetic_elf(reference=True))):
            with self.subTest(size=len(data)):
                self.object = data
                with self.assertRaises(ValueError):
                    self.run_bench()
                self.assertFalse(self.report_path.exists())

    def test_conflicting_existing_report_is_preserved(self):
        self.report_path.parent.mkdir()
        self.report_path.write_bytes(b"valuable existing report")
        with self.assertRaises(ValueError):
            self.run_bench()
        self.assertEqual(self.report_path.read_bytes(), b"valuable existing report")

    def test_report_cannot_alias_any_input(self):
        for path in (self.config_path, self.manifest_path, self.lock_path, self.source,
                     self.elf, self.runner, self.compilers[0], self.support):
            with self.subTest(path=path.name):
                self.report_path = path
                original = path.read_bytes()
                with self.assertRaises(ValueError):
                    self.run_bench()
                self.assertEqual(path.read_bytes(), original)

    def test_real_invocation_uses_empty_stdin_bounded_timeout_and_no_shell(self):
        result = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        with mock.patch.object(bench, "runtime_root", return_value="/synthetic/root"), \
                mock.patch.object(bench.subprocess, "run", return_value=result) as run:
            actual = self.real_compile(self.compilers[0], self.runner, self.source,
                                       self.root / "out.o", ["-c"], timeout=2,
                                       root=self.root, distro="Ubuntu")
        self.assertEqual(actual, {"returncode": 0, "stdout": "", "stderr": ""})
        kwargs = run.call_args.kwargs
        self.assertIs(kwargs["stdin"], subprocess.DEVNULL)
        self.assertGreater(kwargs["timeout"], 0)
        self.assertLessEqual(kwargs["timeout"], 7)
        self.assertFalse(kwargs.get("shell", False))
        self.assertIn("2s", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
