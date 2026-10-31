"""Invented ELF and mocked compiler controls; no real compiler or game execution."""

import copy
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from unittest import mock

from scripts import bench_language_modes as modes
from scripts.elf32 import Elf32


BASE = 0x08804000
SHOFF = 0x1000
TEXT = 0x200
SYMS = 0x800
REL = 0xc00


def sha(data):
    return hashlib.sha256(data).hexdigest()


def names(count=2):
    return [f"probe_{i:02d}" for i in range(count)]


def aliases(count=2, cpp=False):
    return {name: name + ("__Fi" if cpp else "") for name in names(count)}


def code(index):
    return struct.pack("<2I", 0x03e00008, 0x24020000 | index)


def fixture(*, count=2, reference=False, cpp=False, symbol_names=None):
    """Use exact symbol extents with unclaimed gaps inside one executable section."""
    raw = bytearray(0x1400)
    section_names = b"\0.shstrtab\0.text\0.strtab\0.symtab\0.rel.text\0.comment\0"
    symbols = bytearray(b"\0")
    offsets = []
    for name in (list(aliases(count, cpp).values()) if symbol_names is None else symbol_names):
        offsets.append(len(symbols))
        symbols.extend(name.encode() + b"\0")
    raw[0x100:0x100 + len(section_names)] = section_names
    raw[0x400:0x400 + len(symbols)] = symbols
    comment = b"Invented language compiler\0"
    raw[0xb00:0xb00 + len(comment)] = comment
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0,
                     b"\x7fELF\x01\x01\x01" + bytes(9), 2 if reference else 1,
                     8, 1, BASE if reference else 0, 0, SHOFF, 0x10970001,
                     52, 0, 0, 40, 7, 1)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (section_names.index(b".shstrtab"), 3, 0, 0, 0x100, len(section_names), 0, 0, 1, 0),
                (section_names.index(b".text"), 1, 6, BASE if reference else 0, TEXT, count * 16, 0, 0, 4, 0),
                (section_names.index(b".strtab"), 3, 0, 0, 0x400, len(symbols), 0, 0, 1, 0),
                (section_names.index(b".symtab"), 2, 0, 0, SYMS, (count + 1) * 16, 3, 1, 4, 16),
                (section_names.index(b".rel.text"), 9, 0, 0, REL, 0, 4, 2, 4, 8),
                (section_names.index(b".comment"), 1, 0, 0, 0xb00, len(comment), 0, 0, 1, 0)]
    for index, section in enumerate(sections):
        struct.pack_into("<10I", raw, SHOFF + index * 40, *section)
    for index, offset in enumerate(offsets):
        raw[TEXT + index * 16:TEXT + index * 16 + 8] = code(index)
        struct.pack_into("<IIIBBH", raw, SYMS + (index + 1) * 16,
                         offset, index * 16 + (BASE if reference else 0), 8, 0x12, 0, 2)
    return raw


def manifest(count=2):
    return {"schema_version": 1, "source": "bench/original.c", "probes": [
        {"name": name, "address": BASE + index * 16, "size": 8,
         "target_sha256": sha(code(index)), "ownership": "unclassified invented fixture",
         "category": "synthetic", "boundary_evidence": "Invented complete return/delay slot.",
         "relocations": []}
        for index, name in enumerate(names(count))]}


class LanguageObjectTests(unittest.TestCase):
    def setUp(self):
        self.reference = Elf32(fixture(reference=True))
        self.manifest = manifest()

    def compare(self, raw=None, mapping=None):
        return modes.compare_language_object(bytes(fixture(cpp=True) if raw is None else raw),
                                             self.reference, self.manifest,
                                             aliases(cpp=True) if mapping is None else mapping)

    def test_c_and_cpp_use_explicit_aliases_and_preserve_complete_object_identity(self):
        for cpp in (False, True):
            with self.subTest(cpp=cpp):
                raw = fixture(cpp=cpp)
                before = bytes(raw)
                result = self.compare(raw, aliases(cpp=cpp))
                self.assertEqual(bytes(raw), before)
                self.assertEqual(result["object_sha256"], sha(before))
                self.assertEqual([p["name"] for p in result["comparisons"]], names())
                self.assertEqual([p["object_symbol"] for p in result["comparisons"]], list(aliases(cpp=cpp).values()))
                self.assertTrue(all(p["exact_probe_bytes"] for p in result["comparisons"]))

    def test_mapping_requires_exact_keys_unique_values_and_nonempty_symbol_names(self):
        correct = aliases(cpp=True)
        invalid = [{}, {"probe_00": correct["probe_00"]},
                   dict(correct, unexpected="unwanted"),
                   {"probe_00": correct["probe_00"], "probe_01": correct["probe_00"]},
                   dict(correct, probe_01=""), dict(correct, probe_01=None)]
        for mapping in invalid:
            with self.subTest(mapping=mapping), self.assertRaises(ValueError):
                self.compare(mapping=mapping)

    def test_absent_or_unexpected_object_symbols_cannot_use_demangling_fallback(self):
        for mapping in (aliases(), dict(aliases(cpp=True), probe_01="probe_01__FPCi")):
            with self.subTest(mapping=mapping), self.assertRaises(ValueError):
                self.compare(mapping=mapping)
        raw = fixture(cpp=True)
        struct.pack_into("<I", raw, SYMS + 32, 1)  # Both defined functions have one name.
        with self.assertRaises(ValueError):
            self.compare(raw)

    def test_declared_swapped_aliases_compare_wrong_bytes_instead_of_claiming_equality(self):
        mapping = aliases(cpp=True)
        mapping["probe_00"], mapping["probe_01"] = mapping["probe_01"], mapping["probe_00"]
        result = self.compare(mapping=mapping)
        self.assertTrue(all(not p["exact_probe_bytes"] for p in result["comparisons"]))
        self.assertEqual([p["object_symbol"] for p in result["comparisons"]], list(mapping.values()))

    def test_complete_symbol_size_and_changed_words_are_not_trimmed_or_masked(self):
        raw = fixture(cpp=True)
        struct.pack_into("<I", raw, SYMS + 16 + 8, 12)
        result = self.compare(raw)["comparisons"][0]
        self.assertFalse(result["exact_probe_bytes"])
        self.assertEqual(result["compiled_size"], 12)
        self.assertEqual(result["first_difference"], 8)
        raw = fixture(cpp=True)
        raw[TEXT + 4] ^= 1
        result = self.compare(raw)["comparisons"][0]
        self.assertFalse(result["exact_probe_bytes"])
        self.assertEqual(result["first_difference"], 4)

    def test_rel_and_rela_code_relocations_remain_unsupported(self):
        for kind, size in ((9, 8), (4, 12)):
            with self.subTest(kind=kind):
                raw = fixture(cpp=True)
                struct.pack_into("<I", raw, SHOFF + 5 * 40 + 4, kind)
                struct.pack_into("<I", raw, SHOFF + 5 * 40 + 20, size)
                struct.pack_into("<I", raw, SHOFF + 5 * 40 + 36, size)
                struct.pack_into("<II", raw, REL, 0, (1 << 8) | 4)
                with self.assertRaises(ValueError):
                    self.compare(raw)

    def test_malformed_undefined_overlapping_and_nonexecutable_symbols_are_rejected(self):
        edits = [(SYMS + 16 + 8, "<I", 0), (SYMS + 16 + 4, "<I", 2),
                 (SYMS + 32 + 4, "<I", 0), (SYMS + 16 + 14, "<H", 0),
                 (SHOFF + 2 * 40 + 8, "<I", 2), (SYMS + 16, "<I", 99999)]
        for offset, fmt, value in edits:
            with self.subTest(offset=offset):
                raw = fixture(cpp=True)
                struct.pack_into(fmt, raw, offset, value)
                with self.assertRaises(ValueError):
                    self.compare(raw)

    def test_bad_reference_pin_and_manifest_cannot_be_bypassed_by_aliasing(self):
        self.manifest["probes"][0]["target_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.compare()


class LanguageRunnerTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.report = self.root / "evidence/report.json"
        self.path = self.root / "config/language.json"
        self.source = self.write("bench/original.c", b"/* Invented frozen source; never compiled by these tests. */\n")
        self.naming_source = self.write("bench/naming.c", b"/* Invented naming signatures. */\n")
        self.manifest = manifest(14)
        self.manifest_path = self.write("config/probes.json", json.dumps(self.manifest).encode())
        self.reference = self.write("reference/fixture.elf", fixture(count=14, reference=True))
        self.reference_lock = self.write("config/reference.json", json.dumps({
            "status": "active", "baseline_selected_by_user": True,
            "decrypted_executable": self.pin(self.reference)}).encode())
        self.legacy = self.write("config/legacy.json", b"{}")
        self.compiler = self.write("tools/compiler.exe", b"invented compiler")
        self.runner = self.write("tools/runner", b"invented runner")
        self.support = self.write("tools/support.dll", b"invented support")
        self.timeout = self.write("native/timeout", b"invented timeout")
        self.host = self.write("native/host.so", b"invented host dependency")
        self.profile = {"id": "mwccpsp_3_0_1_219", "status": "runnable", "mode": "wibo_driver",
                        "compiler": self.pin(self.compiler), "runner": self.pin(self.runner),
                        "support_files": [self.pin(self.support)],
                        "common_flags": ["-nostdinc", "-lang", "c", "-c"]}
        self.families = {"baseline_source": self.pin(self.source), "probe_manifest": self.pin(self.manifest_path),
                         "reference_lock": self.pin(self.reference_lock), "existing_candidate_config": self.pin(self.legacy),
                         "pre_score_evidence": [], "profiles": [self.profile],
                         "linux_dependencies": [self.native_pin(self.host)],
                         "linux_utilities": [self.native_pin(self.timeout)]}
        self.family_path = self.write("config/families.json", json.dumps(self.families).encode())
        self.spec = {"fixture": self.pin(self.naming_source), "compiler_families": self.pin(self.family_path),
                     "probe_manifest": self.pin(self.manifest_path), "pairs": [
                         {"canonical_name": name, "fixture_name": f"naming_fixture_{i:02d}",
                          "signature_category": "int(int)"} for i, name in enumerate(names(14))]}
        self.spec_path = self.write("config/naming-spec.json", json.dumps(self.spec).encode())
        self.evidence = {"spec_sha256": self.pin(self.spec_path)["sha256"], "modes": []}
        self.naming_objects = []
        for language, cpp in (("c", False), ("c++", True)):
            mode_id = "cpp" if cpp else "c"
            suffix = "__Fi" if cpp else ""
            symbols = [pair["fixture_name"] + suffix for pair in self.spec["pairs"]]
            path = self.write(f"build/naming-{mode_id}.o", fixture(count=14, symbol_names=symbols))
            self.naming_objects.append(path)
            self.evidence["modes"].append({"id": mode_id,
                "flags": ["-nostdinc", "-lang", language, "-c", "-O2"],
                "object_relative_path": path.relative_to(self.root).as_posix(),
                "object_sha256": self.pin(path)["sha256"],
                "mappings": [{**pair, "suffix": suffix, "fixture_symbol": pair["fixture_name"] + suffix,
                              "object_symbol": pair["canonical_name"] + suffix} for pair in self.spec["pairs"]]})
        self.evidence_path = self.write("evidence/naming.json", json.dumps(self.evidence).encode())
        self.config = {"status": "frozen_before_cpp_target_scoring", "no_cpp_target_scores_observed": True,
                       "family_profiles": self.pin(self.family_path), "source": self.pin(self.source),
                       "probe_manifest": self.pin(self.manifest_path), "reference_lock": self.pin(self.reference_lock),
                       "naming_spec": self.pin(self.spec_path), "naming_source": self.pin(self.naming_source),
                       "naming_evidence": self.pin(self.evidence_path),
                       "naming_objects": [self.pin(p) for p in self.naming_objects],
                       "compiler_profile_id": self.profile["id"], "optimization": ["-O2"],
                       "declared_trials": 2, "probe_count": 14, "modes": [
                           {"id": "c", "common_flags": ["-nostdinc", "-lang", "c", "-c"],
                            "symbol_map": aliases(14)},
                           {"id": "cpp", "common_flags": ["-nostdinc", "-lang", "c++", "-c"],
                            "symbol_map": aliases(14, True)}]}
        self.save()
        patch = mock.patch.object(modes, "compile_profile", side_effect=self.compile_ok)
        self.compile = patch.start()
        self.addCleanup(patch.stop)

    def write(self, path, data):
        result = self.root / path
        result.parent.mkdir(parents=True, exist_ok=True)
        result.write_bytes(data)
        return result

    def pin(self, path):
        data = path.read_bytes()
        return {"relative_path": path.relative_to(self.root).as_posix(), "size": len(data), "sha256": sha(data)}

    def native_pin(self, path):
        return {"linux_path": str(path), "size": path.stat().st_size, "sha256": sha(path.read_bytes())}

    def save(self):
        self.path.write_text(json.dumps(self.config), encoding="utf-8")

    def compile_ok(self, profile, source, output, flags, **kwargs):
        self.assertFalse(output.exists(), "Each mode must start with a fresh object path")
        self.assertEqual(source, self.source)
        self.assertEqual(profile["id"], "mwccpsp_3_0_1_219")
        self.assertEqual(flags, ["-O2"])
        self.assertEqual(profile["timeout_tool"], str(self.timeout))
        cpp = profile["common_flags"][2] == "c++"
        output.write_bytes(fixture(count=14, cpp=cpp))
        return {"returncode": 0, "stdout": "", "stderr": ""}

    def run_trial(self):
        return modes.run_language_modes(root=self.root, config_path=self.path, report_path=self.report)

    def test_fixed_pair_scores_all_fourteen_and_preserves_canonical_symbol_associations(self):
        report, directory = self.run_trial()
        self.assertEqual(self.compile.call_count, 2)
        self.assertEqual(report["matched_progress"], 0)
        self.assertEqual(report["completed_configurations"], 2)
        self.assertEqual([row["id"] for row in report["modes"]], ["c", "cpp"])
        for cpp, row in enumerate(report["modes"]):
            self.assertEqual(row["status"], "COMPLETE")
            self.assertEqual(row["exact_probes"], 14)
            self.assertEqual([p["name"] for p in row["comparisons"]], names(14))
            self.assertEqual([p["object_symbol"] for p in row["comparisons"]], list(aliases(14, cpp).values()))
        self.assertEqual(len(report["mode_byte_comparisons"]), 14)
        self.assertTrue(all(r["identical"] for r in report["mode_byte_comparisons"]))
        self.assertEqual(len(list(directory.glob("*.o"))), 2)
        self.assertEqual(json.loads(self.report.read_text()), report)

    def test_repeated_pair_uses_four_fresh_paths_and_identical_reports(self):
        first, a = self.run_trial()
        before = self.report.read_bytes()
        second, b = self.run_trial()
        self.assertNotEqual(a, b)
        self.assertEqual(first, second)
        self.assertEqual(before, self.report.read_bytes())
        self.assertEqual(len({call.args[2] for call in self.compile.call_args_list}), 4)
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_validate_modes_rejects_swapped_binding_wrong_suffix_and_partial_evidence(self):
        original = copy.deepcopy(self.config)
        for field, value in (("optimization", ["-O3"]), ("probe_count", 13),
                             ("compiler_profile_id", "different"), ("declared_trials", 3),
                             ("modes", list(reversed(original["modes"])))):
            config = copy.deepcopy(original)
            config[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                modes.validate_modes(config, self.families, self.manifest, self.spec, self.evidence)
        config = copy.deepcopy(original)
        mapping = config["modes"][1]["symbol_map"]
        mapping["probe_00"], mapping["probe_01"] = mapping["probe_01"], mapping["probe_00"]
        with self.assertRaises(ValueError):
            modes.validate_modes(config, self.families, self.manifest, self.spec, self.evidence)
        for bad in ("category", "canonical", "suffix", "partial", "flags"):
            evidence = copy.deepcopy(self.evidence)
            row = evidence["modes"][1]["mappings"][0]
            if bad == "category": row["signature_category"] = "void(void)"
            elif bad == "canonical": row["canonical_name"] = "probe_01"
            elif bad == "suffix": row["suffix"] = "wrong"
            elif bad == "partial": evidence["modes"][1]["mappings"].pop()
            else: evidence["modes"][1]["flags"].append("-RTTI off")
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                modes.validate_modes(original, self.families, self.manifest, self.spec, evidence)

    def test_compile_failure_warning_timeout_missing_and_invalid_object_leave_whole_mode_unscored(self):
        for failed_mode in ("c", "c++"):
            for bad in ("nonzero", "warning", "timeout", "missing", "invalid", "partial"):
                with self.subTest(failed_mode=failed_mode, bad=bad):
                    self.report = self.root / "evidence" / f"{failed_mode}-{bad}.json"
                    def fail(profile, source, output, flags, **kwargs):
                        if profile["common_flags"][2] != failed_mode:
                            return self.compile_ok(profile, source, output, flags, **kwargs)
                        if bad == "timeout": raise subprocess.TimeoutExpired("invented", 20)
                        if bad == "missing": return {"returncode": 0, "stdout": "", "stderr": ""}
                        result = self.compile_ok(profile, source, output, flags, **kwargs)
                        if bad == "nonzero": result["returncode"] = 1
                        elif bad == "warning": result["stderr"] = "Warning: invented"
                        elif bad == "invalid": output.write_bytes(b"not ELF")
                        else: output.write_bytes(fixture(count=13, cpp=failed_mode == "c++"))
                        return result
                    self.compile.side_effect = fail
                    report, _ = self.run_trial()
                    failed = report["modes"][0 if failed_mode == "c" else 1]
                    valid = report["modes"][1 if failed_mode == "c" else 0]
                    self.assertEqual(failed["status"], "REJECTED_NO_SCORE")
                    self.assertEqual(failed["comparisons"], [])
                    self.assertNotIn("exact_probes", failed)
                    self.assertEqual(valid["status"], "COMPLETE")
                    self.assertEqual(len(valid["comparisons"]), 14)
                    self.assertEqual(report["completed_configurations"], 1)
                    self.assertEqual(report["mode_byte_comparisons"], [])

    def test_code_relocation_invalidates_entire_mode_even_when_other_functions_match(self):
        def relocate(profile, source, output, flags, **kwargs):
            result = self.compile_ok(profile, source, output, flags, **kwargs)
            if profile["common_flags"][2] == "c++":
                raw = bytearray(output.read_bytes())
                struct.pack_into("<I", raw, SHOFF + 5 * 40 + 20, 8)
                struct.pack_into("<II", raw, REL, 0, (1 << 8) | 4)
                output.write_bytes(raw)
            return result
        self.compile.side_effect = relocate
        report, _ = self.run_trial()
        self.assertEqual(report["modes"][0]["status"], "COMPLETE")
        self.assertEqual(report["modes"][1]["status"], "REJECTED_NO_SCORE")
        self.assertEqual(report["modes"][1]["comparisons"], [])
        self.assertNotIn("exact_probes", report["modes"][1])

    def test_second_compiler_cannot_change_the_first_scored_object_without_invalidating_report(self):
        for first_failed in (False, True):
            with self.subTest(first_failed=first_failed):
                first = []
                def mutate_previous(profile, source, output, flags, **kwargs):
                    result = self.compile_ok(profile, source, output, flags, **kwargs)
                    if first:
                        first[0].write_bytes(b"changed previously retained object")
                    else:
                        first.append(output)
                        if first_failed:
                            result["returncode"] = 1
                    return result
                self.compile.side_effect = mutate_previous
                with self.assertRaises(ValueError):
                    self.run_trial()
                self.assertFalse(self.report.exists())

    def test_undeclared_modes_and_mapping_changes_are_rejected_before_compilation(self):
        original = copy.deepcopy(self.config)
        cases = [("status", "draft"), ("no_cpp_target_scores_observed", False),
                 ("modes", original["modes"][:1]), ("modes", original["modes"] * 2)]
        changed = copy.deepcopy(original["modes"])
        changed[1]["common_flags"].append("-O3")
        cases.append(("modes", changed))
        for key, value in cases:
            with self.subTest(key=key):
                self.config = copy.deepcopy(original)
                self.config[key] = value
                self.save()
                with self.assertRaises(ValueError): self.run_trial()
                self.compile.assert_not_called()

    def test_pins_and_profile_changes_fail_globally_without_outer_report(self):
        paths = (self.source, self.family_path, self.manifest_path, self.reference_lock, self.reference,
                 self.naming_source, self.spec_path, self.evidence_path, *self.naming_objects,
                 self.compiler, self.runner, self.support, self.timeout, self.host)
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

    def test_report_aliases_and_conflicts_preserve_every_input_and_existing_evidence(self):
        paths = (self.path, self.source, self.family_path, self.manifest_path, self.reference_lock,
                 self.reference, self.naming_source, self.spec_path, self.evidence_path,
                 *self.naming_objects, self.compiler, self.runner, self.support)
        for path in paths:
            with self.subTest(path=path.name):
                self.report = path
                before = path.read_bytes()
                with self.assertRaises(ValueError): self.run_trial()
                self.assertEqual(path.read_bytes(), before)
                self.compile.assert_not_called()
        self.report = self.root / "evidence/conflict.json"
        self.report.write_bytes(b"valuable old evidence")
        with self.assertRaises(ValueError): self.run_trial()
        self.assertEqual(self.report.read_bytes(), b"valuable old evidence")


if __name__ == "__main__":
    unittest.main()

