"""Source-cohort controls with invented sources and mocked compiler matrices.

These checks validate a bounded experiment, not historical source, a toolchain
lock, game matching or the future matching gate's 18 negative checks.
"""

import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from scripts import bench_source_hypotheses as experiment


ALPHA = "probe_08830550"
BETA = "probe_08830654"
SOURCE = (b"typedef unsigned int u32;\n\n/* First invented probe. */\n"
          b"u32 probe_08830550(u32 value)\n{\n    return value + 1;\n}\n\n"
          b"/* Second invented probe. */\nu32 probe_08830654(u32 value)\n"
          b"{\n    return value + 2;\n}\n")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def pin(data, relative_path):
    return {"relative_path": relative_path, "size": len(data), "sha256": digest(data)}


def variant_source(name):
    if name == ALPHA:
        return SOURCE.replace(b"return value + 1;", b"return value == 0 ? 1 : value + 1;")
    return SOURCE.replace(b"return value + 2;", b"return value == 0 ? 2 : value + 2;")


def comparison(name, compiled):
    target = b"A" * 8 if name == ALPHA else b"B" * 8
    return {"name": name, "address": 0x1000 if name == ALPHA else 0x2000,
            "target_size": 8, "compiled_size": len(compiled),
            "target_sha256": digest(target), "compiled_sha256": digest(compiled),
            "exact_probe_bytes": compiled == target,
            "first_difference": None if compiled == target else 0}


def matrix(changed=None):
    results = []
    for candidate in ("first", "second"):
        for setting in ("O1", "O2"):
            alpha = b"D" * 8 if changed == ALPHA else b"A" * 8
            beta = b"B" * 8 if changed == BETA else b"C" * 8
            functions = [comparison(ALPHA, alpha), comparison(BETA, beta)]
            results.append({"candidate": candidate, "setting": setting,
                            "flags": ["-nostdinc", "-lang", "c", "-c", "-" + setting],
                            "version": "synthetic", "comparisons": functions,
                            "exact_probes": sum(c["exact_probe_bytes"] for c in functions),
                            "object_sha256": digest(alpha + beta), "elf_flags": 0x10970001,
                            "compiler_comments": ["Synthetic compiler"]})
    return {"schema_version": 1, "status": "COMPILER_BENCH_COMPLETE",
            "matched_progress": 0, "probe_count": 2,
            "source_sha256": digest(SOURCE if changed is None else variant_source(changed)),
            "results": results}


class SourceChangeTests(unittest.TestCase):
    def test_span_includes_outer_braces_and_nested_control_flow(self):
        source = b"int nested(int x)\n{\n if (x) { ++x; }\n return x;\n}\n"
        start, end = experiment.body_span(source, "nested")
        self.assertEqual(source[start:end], source[source.index(b"{"):source.rindex(b"}") + 1])

    def test_comments_strings_and_characters_cannot_spoof_function_or_braces(self):
        source = (b"/* decoy(int x) { } */\n"
                  b"const char *outside = \"decoy() { }\";\n"
                  b"int decoy(int x);\n"
                  b"int decoy(int x)\n{\n"
                  b" const char *inside = \"quote \\\" }\";\n"
                  b" char brace = '}'; /* } */\n return x;\n}\n")
        start, end = experiment.body_span(source, "decoy")
        self.assertEqual(source[start:start + 2], b"{\n")
        self.assertTrue(source[start:end].endswith(b"return x;\n}"))

    def test_missing_duplicate_and_unterminated_tokens_fail(self):
        for source, name in ((SOURCE, "absent"), (SOURCE + SOURCE, ALPHA),
                             (b"int broken() { /* never ends", "broken"),
                             (b'int broken() { const char *s = "oops; }', "broken"),
                             (b"int broken() { if (1) { return 0; }", "broken")):
            with self.subTest(name=name, size=len(source)):
                with self.assertRaises(ValueError):
                    experiment.body_span(source, name)

    def test_change_evidence_pins_only_declared_body_and_preserves_other_bytes(self):
        alternative = variant_source(ALPHA)
        result = experiment.validate_source_change(SOURCE, alternative, ALPHA)
        a, b = result["baseline_span"]
        c, d = result["alternative_span"]
        self.assertEqual(SOURCE[:a], alternative[:c])
        self.assertEqual(SOURCE[b:], alternative[d:])
        self.assertEqual(result["baseline_body_sha256"], digest(SOURCE[a:b]))
        self.assertEqual(result["alternative_body_sha256"], digest(alternative[c:d]))
        self.assertEqual(result["unchanged_prefix_sha256"], digest(SOURCE[:a]))
        self.assertEqual(result["unchanged_suffix_sha256"], digest(SOURCE[b:]))

    def test_noop_signature_comment_and_second_body_changes_are_rejected(self):
        alternative = variant_source(ALPHA)
        variants = [SOURCE, alternative.replace(b"typedef unsigned", b"typedef signed"),
                    alternative.replace(b"First invented", b"Changed purpose"),
                    alternative.replace(b"value + 2;", b"value + 3;")]
        for data in variants:
            with self.subTest(size=len(data)):
                with self.assertRaises(ValueError):
                    experiment.validate_source_change(SOURCE, data, ALPHA)


class CohortComparisonTests(unittest.TestCase):
    def setUp(self):
        self.baseline = matrix()
        self.reports = {"alpha": matrix(ALPHA), "beta": matrix(BETA)}
        self.variants = [{"id": "alpha", "changed_function": ALPHA},
                         {"id": "beta", "changed_function": BETA}]

    def compare(self):
        return experiment.compare_cohorts(self.baseline, self.reports, self.variants)

    def test_reports_changed_function_and_exact_scores_without_promoting_source_claims(self):
        report = self.compare()
        self.assertEqual(len(report["variants"]), 2)
        for row in report["variants"]:
            self.assertEqual(row["control_comparisons"], 4)
            self.assertEqual(len(row["results"]), 4)
            self.assertTrue(all(c["function_bytes_changed"] for c in row["results"]))
        self.assertTrue(all(row["alternative_exact_probes"] == 0
                            for row in report["variants"][0]["results"]))
        self.assertTrue(all(row["alternative_exact_probes"] == 2
                            for row in report["variants"][1]["results"]))

    def test_missing_duplicate_or_extra_matrix_rows_fail(self):
        for mode in ("missing", "duplicate", "extra"):
            with self.subTest(mode=mode):
                self.reports = {"alpha": matrix(ALPHA), "beta": matrix(BETA)}
                rows = self.reports["alpha"]["results"]
                if mode == "missing":
                    rows.pop()
                elif mode == "duplicate":
                    rows.append(copy.deepcopy(rows[0]))
                else:
                    extra = copy.deepcopy(rows[0])
                    extra["candidate"] = "unexpected"
                    rows.append(extra)
                with self.assertRaises(ValueError):
                    self.compare()

    def test_row_flags_probe_sets_and_scores_must_agree(self):
        changes = [("flags", ["-O9"]), ("exact_probes", 99)]
        for field, value in changes:
            with self.subTest(field=field):
                self.reports = {"alpha": matrix(ALPHA), "beta": matrix(BETA)}
                self.reports["alpha"]["results"][0][field] = value
                with self.assertRaises(ValueError):
                    self.compare()
        for mode in ("missing", "duplicate", "renamed"):
            with self.subTest(mode=mode):
                self.reports = {"alpha": matrix(ALPHA), "beta": matrix(BETA)}
                probes = self.reports["alpha"]["results"][0]["comparisons"]
                if mode == "missing":
                    probes.pop()
                elif mode == "duplicate":
                    probes.append(copy.deepcopy(probes[0]))
                else:
                    probes[1]["name"] = "unexpected"
                with self.assertRaises(ValueError):
                    self.compare()

    def test_control_hash_size_and_target_identity_changes_invalidate_cohort(self):
        for field, value in (("compiled_sha256", "0" * 64), ("compiled_size", 12),
                             ("target_sha256", "0" * 64), ("target_size", 12),
                             ("address", 0x3000)):
            with self.subTest(field=field):
                self.reports = {"alpha": matrix(ALPHA), "beta": matrix(BETA)}
                self.reports["alpha"]["results"][0]["comparisons"][1][field] = value
                with self.assertRaises(ValueError):
                    self.compare()

    def test_variant_ids_and_changed_functions_must_be_unambiguous(self):
        for variants, reports in ((self.variants, {"alpha": matrix(ALPHA)}),
                                  ([self.variants[0], self.variants[0]], self.reports),
                                  ([{"id": "alpha", "changed_function": "missing"}],
                                   {"alpha": matrix(ALPHA)})):
            with self.subTest(variants=variants):
                self.variants, self.reports = variants, reports
                with self.assertRaises(ValueError):
                    self.compare()

    def test_partial_or_credit_bearing_baseline_is_not_a_valid_control(self):
        for field, value in (("status", "PARTIAL"), ("matched_progress", 1)):
            with self.subTest(field=field):
                self.baseline = matrix()
                self.baseline[field] = value
                with self.assertRaises(ValueError):
                    self.compare()


class ExperimentRunnerTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.experiment_path = self.root / "config/source-hypotheses.json"
        self.report_path = self.root / "evidence/experiment.json"
        self.base = self.write("bench/compiler_probes.c", SOURCE)
        self.sources = [self.write("bench/hypotheses/alpha.c", variant_source(ALPHA)),
                        self.write("bench/hypotheses/beta.c", variant_source(BETA))]
        self.candidate_path = self.write("config/compiler-candidates.json", json.dumps({
            "status": "investigation_only_not_locked", "source_sha256": digest(SOURCE),
            "manifest_sha256": "pending", "candidates": [{"id": "first"}, {"id": "second"}],
            "settings": [{"id": "O1", "flags": ["-O1"]}, {"id": "O2", "flags": ["-O2"]}]
        }).encode())
        self.manifest_path = self.write("config/compiler-probes.json", json.dumps({
            "schema_version": 1, "source": "bench/compiler_probes.c",
            "probes": [{"name": ALPHA}, {"name": BETA}]
        }).encode())
        self.lock_path = self.write("config/reference.json", json.dumps({
            "status": "active", "baseline_selected_by_user": True
        }).encode())
        candidates = json.loads(self.candidate_path.read_bytes())
        candidates["manifest_sha256"] = digest(self.manifest_path.read_bytes())
        self.candidate_path.write_text(json.dumps(candidates), encoding="utf-8")
        self.config = {"status": "reviewed_frozen_source_experiment_not_toolchain_lock",
                       "reviewed_before_compilation": True,
                       "baseline": self.file_pin(self.base),
                       "candidate_config": self.file_pin(self.candidate_path),
                       "probe_manifest": self.file_pin(self.manifest_path),
                       "reference_lock": self.file_pin(self.lock_path),
                       "variants": [{"id": "alpha", "changed_function": ALPHA,
                                     "source": self.file_pin(self.sources[0]),
                                     "change": experiment.validate_source_change(SOURCE, self.sources[0].read_bytes(), ALPHA)},
                                    {"id": "beta", "changed_function": BETA,
                                     "source": self.file_pin(self.sources[1]),
                                     "change": experiment.validate_source_change(SOURCE, self.sources[1].read_bytes(), BETA)}]}
        self.save()
        patcher = mock.patch.object(experiment, "run_bench", side_effect=self.good_bench)
        self.bench = patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def file_pin(self, path):
        return pin(path.read_bytes(), path.relative_to(self.root).as_posix())

    def save(self):
        self.experiment_path.write_text(json.dumps(self.config), encoding="utf-8")

    def good_bench(self, **kwargs):
        manifest = json.loads(Path(kwargs["manifest_path"]).read_bytes())
        source = manifest["source"]
        changed = None if source == "bench/compiler_probes.c" else (ALPHA if source.endswith("alpha.c") else BETA)
        return matrix(changed)

    def run_experiment(self):
        return experiment.run_experiment(root=self.root, experiment_path=self.experiment_path,
                                         report_path=self.report_path)

    def test_three_complete_cohorts_preserve_original_metadata_and_source(self):
        paths = [self.base, self.candidate_path, self.manifest_path, self.lock_path, *self.sources]
        before = {p: p.read_bytes() for p in paths}
        report = self.run_experiment()
        self.assertEqual(self.bench.call_count, 3)
        self.assertEqual(report["matched_progress"], 0)
        self.assertEqual(json.loads(self.report_path.read_text()), report)
        self.assertEqual(before, {p: p.read_bytes() for p in paths})
        for index, call in enumerate(self.bench.call_args_list):
            if index:
                self.assertNotEqual(Path(call.kwargs["candidates_path"]), self.candidate_path)
            derived = json.loads(Path(call.kwargs["candidates_path"]).read_bytes())
            original = json.loads(before[self.candidate_path])
            self.assertEqual(derived["settings"], original["settings"])
            self.assertEqual(derived["candidates"], original["candidates"])

    def test_repeat_uses_fresh_derived_paths_and_identical_report(self):
        first = self.run_experiment()
        data = self.report_path.read_bytes()
        second = self.run_experiment()
        self.assertEqual(first, second)
        self.assertEqual(data, self.report_path.read_bytes())
        self.assertEqual(len({str(c.kwargs["report_path"]) for c in self.bench.call_args_list}), 6)
        derived = [c.kwargs["manifest_path"] for i, c in enumerate(self.bench.call_args_list) if i % 3]
        self.assertEqual(len(set(derived)), 4)
        self.assertNotIn(str(self.root), json.dumps(first))

    def test_wrong_status_variant_count_and_source_pins_prevent_compilation(self):
        original = copy.deepcopy(self.config)
        reserved = copy.deepcopy(original["variants"])
        reserved[0]["id"] = "baseline"
        for change in ({"status": "locked"}, {"reviewed_before_compilation": False},
                       {"variants": original["variants"][:1]},
                       {"variants": original["variants"] * 2}, {"variants": reserved}):
            self.config = {**copy.deepcopy(original), **change}
            self.save()
            with self.assertRaises(ValueError):
                self.run_experiment()
            self.bench.assert_not_called()
            self.assertFalse(self.report_path.exists())
        self.config = original
        self.save()
        for path in (self.base, *self.sources, self.candidate_path, self.manifest_path, self.lock_path):
            with self.subTest(path=path.name):
                before = path.read_bytes()
                path.write_bytes(before + b"changed")
                with self.assertRaises(ValueError):
                    self.run_experiment()
                self.bench.assert_not_called()
                self.assertFalse(self.report_path.exists())
                path.write_bytes(before)

    def test_repinning_extra_body_edit_cannot_bypass_declared_change(self):
        self.sources[0].write_bytes(variant_source(ALPHA).replace(b"value + 2;", b"value + 3;"))
        self.config["variants"][0]["source"] = self.file_pin(self.sources[0])
        self.save()
        with self.assertRaises(ValueError):
            self.run_experiment()
        self.bench.assert_not_called()
        self.assertFalse(self.report_path.exists())

    def test_frozen_change_evidence_cannot_be_silently_recomputed(self):
        self.config["variants"][0]["change"]["baseline_body_sha256"] = "0" * 64
        self.save()
        with self.assertRaises(ValueError):
            self.run_experiment()
        self.bench.assert_not_called()
        self.assertFalse(self.report_path.exists())

    def test_lower_bench_failure_or_changed_control_never_publishes_partial_cohort(self):
        self.bench.side_effect = [matrix(), ValueError("compiler warned")]
        with self.assertRaises(ValueError):
            self.run_experiment()
        self.assertFalse(self.report_path.exists())
        bad = matrix(ALPHA)
        bad["results"][0]["comparisons"][1]["compiled_sha256"] = "0" * 64
        self.bench.side_effect = [matrix(), bad, matrix(BETA)]
        with self.assertRaises(ValueError):
            self.run_experiment()
        self.assertFalse(self.report_path.exists())

    def test_row_missing_from_every_cohort_cannot_silently_shrink_matrix(self):
        def incomplete(**kwargs):
            report = self.good_bench(**kwargs)
            report["results"].pop()
            return report
        self.bench.side_effect = incomplete
        with self.assertRaises(ValueError):
            self.run_experiment()
        self.assertFalse(self.report_path.exists())

    def test_original_or_variant_changes_during_cohort_prevent_report(self):
        for path in (self.base, *self.sources, self.candidate_path, self.manifest_path,
                     self.lock_path, self.experiment_path):
            with self.subTest(path=path.name):
                before = path.read_bytes()
                def mutate(**kwargs):
                    result = self.good_bench(**kwargs)
                    path.write_bytes(before + b"changed")
                    return result
                self.bench.side_effect = mutate
                with self.assertRaises(ValueError):
                    self.run_experiment()
                self.assertFalse(self.report_path.exists())
                path.write_bytes(before)

    def test_report_conflict_and_input_aliases_preserve_originals(self):
        self.report_path.parent.mkdir()
        self.report_path.write_bytes(b"valuable evidence")
        with self.assertRaises(ValueError):
            self.run_experiment()
        self.assertEqual(self.report_path.read_bytes(), b"valuable evidence")
        for path in (self.base, *self.sources, self.candidate_path, self.manifest_path,
                     self.lock_path, self.experiment_path):
            with self.subTest(path=path.name):
                self.report_path = path
                before = path.read_bytes()
                with self.assertRaises(ValueError):
                    self.run_experiment()
                self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
