"""Known-overlay recovery integrity checks using a genuine invented lock chain."""

import copy
import hashlib
import json
import os
from pathlib import Path
import struct
import unittest
from unittest import mock

from scripts import recover_overlay_set as tool
from tests import test_overlay_inventory as prior
from tests import test_extract_overlay as invented


class AddressSpanTests(unittest.TestCase):
    def test_raw_span_records_words_without_semantics_and_unsupported_is_uninterpreted(self):
        data = bytearray(invented.overlay_bytes())
        header = tool.inventory.parse_header(data[:64], len(data))
        header.update(raw_0x18=header["load_address"] + 80, raw_0x1c=header["load_address"] + 88)
        struct.pack_into("<II", data, 80, header["load_address"] + 64, 0x12345679)
        result = tool.observe_address_span(header, data)
        self.assertEqual(result["status"], "BOUNDED_RAW_SPAN")
        self.assertEqual(result["span_size"], 8)
        self.assertTrue(result["words"][0]["within_declared_code"])
        self.assertFalse(result["words"][1]["word_aligned"])
        self.assertFalse(result["all_values_in_declared_code"])
        for start, end in ((100, 96), (0, 132), (1, 4), (-4, 0), (96, 100)):
            bad = dict(header, raw_0x18=header["load_address"] + start,
                       raw_0x1c=header["load_address"] + end)
            with self.subTest(start=start, end=end):
                result = tool.observe_address_span(bad, data)
                self.assertEqual(result["status"], "UNINTERPRETED")
                self.assertIsNone(result["words"])
        header["raw_0x18"] = header["raw_0x1c"] = header["load_address"] + len(data)
        result = tool.observe_address_span(header, data)
        self.assertEqual(result["words"], [])
        self.assertIsNone(result["all_values_in_declared_code"])


class RecoverOverlaySetTests(unittest.TestCase):
    def setUp(self):
        self.base = prior.OverlayInventoryTests(methodName="runTest")
        self.base.setUp()
        self.addCleanup(self.base.doCleanups)
        self.f = self.base.fixture
        self.root, self.iso, self.elf = self.base.root, self.base.iso, self.base.elf
        self.f.lock["decrypted_executable"]["relative_path"] = self.elf.name
        self.f.save_locks()
        self.base.config["reference_lock"] = self.base.pin(self.f.lock_path)
        self.base.save()
        self.known_path = self.root / "known-inventory.json"
        self.config_path = self.root / "recovery.json"
        self.preserved = self.root / "parked-source.cpp"
        self.preserved.write_bytes(b"/* Invented preserved draft, not game source. */")
        self.config = {"status": "frozen_before_recovery", "maximum_payload_bytes": 2 * 1024 * 1024,
                       "maximum_raw_address_span_bytes": 128, "declared_trials": 2,
                       "output_parent_relative_path": "reference/known-sets", "expected_overlay_count": 1,
                       "preserved_inputs": [self.base.pin(self.preserved)]}
        self.output = self.root / "reference/known-sets/set-1"
        self.report_path = self.root / "recovery-report.json"
        self.freeze_inventory()

    def freeze_inventory(self):
        self.f.save_locks()
        self.base.config["reference_lock"] = self.base.pin(self.f.lock_path)
        self.base.config["pilot_lock"] = self.base.pin(self.f.pilot_path)
        self.base.save()
        self.known = self.base.inventory(False)
        self.known_path.write_text(json.dumps(self.known, indent=2, sort_keys=True) + "\n")
        self.config.update(inventory_profile=self.base.pin(self.base.config_path),
                           inventory_report=self.base.pin(self.known_path))
        self.save()

    def save(self):
        self.config_path.write_text(json.dumps(self.config))

    def recover(self, output=None, report=True):
        return tool.recover_overlay_set(self.iso, output or self.output, root=self.root,
                    config_path=self.config_path, report_path=self.report_path if report else None)

    def assert_unpublished(self):
        self.assertFalse(self.output.exists())
        self.assertFalse(self.report_path.exists())
        parent = self.output.parent
        if parent.exists(): self.assertEqual(list(parent.iterdir()), [])

    def test_complete_payload_and_code_data_hashes_repeat_with_bss_only_metadata(self):
        original = {p:p.read_bytes() for p in (self.iso, self.elf, self.config_path,
                     self.base.config_path, self.known_path, self.f.lock_path, self.f.pilot_path, self.preserved)}
        with mock.patch.object(tool.pilot, "read_extent", wraps=tool.pilot.read_extent) as reads:
            first = self.recover()
        self.assertEqual([c.args[4] for c in reads.call_args_list], [2048, 64, 64, 64, 96])
        self.assertEqual(first["recovered_overlay_count"], 1)
        self.assertEqual(first["total_stored_bytes"], 96)
        self.assertTrue(first["movie_pilot_full_identity_reproduced"])
        row = first["modules"][0]
        self.assertEqual(row["relative_path"], "entry-0001-sample.ovl.mwo")
        self.assertEqual((self.output / row["relative_path"]).read_bytes(), self.f.plain)
        self.assertEqual(row["decoded"], invented.identity(self.f.plain))
        self.assertEqual(row["encoded"], invented.identity(self.f.encrypted))
        self.assertEqual(row["code"], invented.identity(self.f.plain[64:80]))
        self.assertEqual(row["data"], invented.identity(self.f.plain[80:]))
        self.assertEqual(row["bss_size"], 16)
        self.assertEqual(first["matched_progress"], 0)
        self.assertFalse(first["runtime_tested"])
        self.assertFalse(first["complete_game_code_inventory_established"])
        self.assertEqual(json.loads((self.output / "manifest.json").read_bytes()), first)
        second = self.recover(self.output.with_name("set-2"), False)
        self.assertEqual(first, second)
        for name in (row["relative_path"], "manifest.json"):
            self.assertEqual((self.output / name).read_bytes(), (self.output.with_name("set-2") / name).read_bytes())
        for path, data in original.items(): self.assertEqual(path.read_bytes(), data)

    def test_same_names_at_distinct_indexes_do_not_collide_or_replace(self):
        f = self.f
        second = bytes(invented.overlay_bytes(load=0x09000100))
        directory = bytes(invented.index_bytes(sizes=((0, 96), (1, 96))))
        encoded_directory = invented.encode_fixture(directory, 0, f.table)
        archive = bytearray(f.archive)
        archive[:2048] = encoded_directory
        archive[2048:2048 + 96] = invented.encode_fixture(second, 1, f.table)
        self.iso.write_bytes(invented.archive_iso(archive))
        self.elf.write_bytes(prior.mapped_elf(f.table,
            descriptors=(("sample.ovl", 0x09000000), ("sample.ovl", 0x09000100)),
            reservations=((0x09000000, 112), (0x09000100, 112))))
        f.lock.update(invented.identity(self.iso.read_bytes()))
        f.lock["decrypted_executable"].update(invented.identity(self.elf.read_bytes()))
        f.pilot["reference_sha256"] = f.lock["sha256"]
        f.pilot["archive"].update(invented.identity(archive))
        f.pilot["directory"].update(invented.identity(encoded_directory),
            decoded_sha256=invented.identity(directory)["sha256"], exact_size_count=2)
        self.base.config["expected_named_descriptors"] = 2
        self.config["expected_overlay_count"] = 2
        self.freeze_inventory()
        report = self.recover()
        self.assertEqual([x["archive_index"] for x in report["modules"]], [0, 1])
        self.assertEqual((self.output / "entry-0000-sample.ovl.mwo").read_bytes(), second)
        self.assertEqual((self.output / "entry-0001-sample.ovl.mwo").read_bytes(), f.plain)

    def test_scope_bad_frozen_set_and_pilot_whole_body_drift_fail_without_publication(self):
        for key, value in (("maximum_payload_bytes", 4 * 1024 * 1024), ("maximum_raw_address_span_bytes", 256),
                           ("declared_trials", 1), ("expected_overlay_count", 2), ("status", "review")):
            original = copy.deepcopy(self.config); self.config[key] = value; self.save()
            with self.subTest(key=key), self.assertRaises(ValueError): self.recover()
            self.config = original; self.save(); self.assert_unpublished()
        known = copy.deepcopy(self.known)
        for change in ("duplicate", "length", "header", "prefix", "incomplete"):
            altered = copy.deepcopy(known)
            if change == "duplicate": altered["overlays"].append(copy.deepcopy(altered["overlays"][0]))
            elif change == "length": altered["overlays"][0]["stored_length"] = 2 * 1024 * 1024 + 4
            elif change == "header": altered["overlays"][0]["header"]["raw_0x18"] += 4
            elif change == "prefix": altered["entries"][1]["raw_prefix_sha256"] = "0" * 64
            else: altered["status"] = "OVERLAY_PREFIX_INVENTORY_INCOMPLETE"
            self.known_path.write_text(json.dumps(altered)); self.config["inventory_report"] = self.base.pin(self.known_path); self.save()
            with self.subTest(change=change), self.assertRaises(ValueError): self.recover()
            self.assert_unpublished()
        self.f.pilot["overlay"]["decoded"]["sha256"] = "0" * 64
        self.freeze_inventory()
        with self.assertRaises(ValueError): self.recover()
        self.assert_unpublished()

    def test_unsupported_address_span_does_not_drop_a_valid_image(self):
        archive = bytearray(self.f.archive); payload = bytearray(self.f.plain)
        struct.pack_into("<II", payload, 24, 0, 0xFFFFFFFF)
        encoded = invented.encode_fixture(payload, 2, self.f.table)
        archive[4096:4096 + len(encoded)] = encoded
        self.iso.write_bytes(invented.archive_iso(archive))
        self.f.lock.update(invented.identity(self.iso.read_bytes()))
        self.f.pilot["reference_sha256"] = self.f.lock["sha256"]
        self.f.pilot["archive"].update(invented.identity(archive))
        self.f.pilot["overlay"]["encrypted"] = invented.identity(encoded)
        self.f.pilot["overlay"]["decoded"] = invented.identity(payload)
        self.freeze_inventory()
        report = self.recover()
        self.assertEqual(report["modules"][0]["raw_address_span"]["status"], "UNINTERPRETED")
        self.assertEqual((self.output / report["modules"][0]["relative_path"]).read_bytes(), payload)

    def test_existing_output_aliases_paths_and_evidence_fail_before_payload_read(self):
        self.output.mkdir(parents=True); sentinel = self.output / "valuable"; sentinel.write_bytes(b"keep")
        with mock.patch.object(tool.inventory, "inventory_overlays") as scan, self.assertRaises(ValueError): self.recover()
        scan.assert_not_called(); self.assertEqual(sentinel.read_bytes(), b"keep")
        sentinel.unlink(); self.output.rmdir()
        for output in (self.root / "outside", self.output.parent / "bad.name", self.output.parent / "../escape"):
            with self.subTest(output=str(output)), mock.patch.object(tool.inventory, "inventory_overlays") as scan:
                with self.assertRaises(ValueError): self.recover(output)
                scan.assert_not_called()
        for path in (self.iso, self.elf, self.config_path, self.base.config_path,
                     self.known_path, self.f.lock_path, self.f.pilot_path, self.preserved, self.output / "report.json"):
            with self.subTest(path=str(path)), self.assertRaises(ValueError):
                tool.recover_overlay_set(self.iso, self.output, root=self.root, config_path=self.config_path, report_path=path)
        self.report_path.write_bytes(b"prior evidence")
        with self.assertRaises(ValueError): self.recover()
        self.assertEqual(self.report_path.read_bytes(), b"prior evidence")
        self.assertFalse(self.output.exists())

    def test_input_changes_after_payload_decode_reject_even_restored_iso_timestamp(self):
        for path in (self.iso, self.elf, self.config_path, self.base.config_path,
                     self.known_path, self.f.lock_path, self.f.pilot_path, self.preserved):
            old = path.read_bytes(); stat = path.stat(); observe = tool.observe_address_span
            def mutate(*args):
                result = observe(*args)
                raw = bytearray(path.read_bytes()); raw[-1] ^= 1; path.write_bytes(raw)
                os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
                return result
            with self.subTest(path=path.name), mock.patch.object(tool, "observe_address_span", side_effect=mutate):
                with self.assertRaises(ValueError): self.recover()
            self.assert_unpublished(); path.write_bytes(old)

    def test_final_staged_payload_manifest_extra_file_and_links_prevent_publication(self):
        for mode in ("payload", "manifest", "extra", "manifest_link", "stage_link"):
            verify = tool.verify_inputs; count = 0
            def mutate(root, config):
                nonlocal count
                result = verify(root, config); count += 1
                if count == 2:
                    stage = next(self.output.parent.glob(".overlay-set-*"))
                    if mode == "payload":
                        p = next(stage.glob("*.mwo")); raw = bytearray(p.read_bytes()); raw[-1] ^= 1; p.write_bytes(raw)
                    elif mode == "manifest": (stage / "manifest.json").write_bytes(b"tampered")
                    elif mode == "extra": (stage / "unexpected").write_bytes(b"not declared")
                    elif mode == "manifest_link":
                        p = stage / "manifest.json"; saved = self.root / "manifest-copy.json"; saved.write_bytes(p.read_bytes()); p.unlink(); p.symlink_to(saved)
                    else:
                        moved = self.output.parent / "retained-stage"; stage.rename(moved); stage.symlink_to(moved, target_is_directory=True)
                return result
            with self.subTest(mode=mode), mock.patch.object(tool, "verify_inputs", side_effect=mutate):
                with self.assertRaises((ValueError, OSError)): self.recover()
            self.assertFalse(self.output.exists())
            self.assertFalse(self.report_path.exists())
            retained = self.output.parent / "retained-stage"
            if mode == "stage_link":
                # TemporaryDirectory may refuse cleanup of the injected link;
                # verify no target traversal, then remove our test artifacts.
                links = list(self.output.parent.glob(".overlay-set-*"))
                for link in links:
                    self.assertTrue(link.is_symlink())
                    link.unlink()
                self.assertTrue((retained / "manifest.json").is_file())
                self.assertTrue(next(retained.glob("*.mwo")).is_file())
                for path in retained.iterdir(): path.unlink()
                retained.rmdir()
            self.assert_unpublished()

    def test_external_report_failure_leaves_complete_verified_bundle_with_its_manifest(self):
        write = tool.pilot.write_report
        def fail_external(path, report):
            if Path(path) == self.report_path: raise OSError("Invented external evidence failure")
            return write(path, report)
        with mock.patch.object(tool.pilot, "write_report", side_effect=fail_external):
            with self.assertRaises(OSError): self.recover()
        self.assertFalse(self.report_path.exists())
        report = json.loads((self.output / "manifest.json").read_bytes())
        self.assertEqual(report["recovered_overlay_count"], 1)
        self.assertEqual((self.output / report["modules"][0]["relative_path"]).read_bytes(), self.f.plain)


if __name__ == "__main__":
    unittest.main()
