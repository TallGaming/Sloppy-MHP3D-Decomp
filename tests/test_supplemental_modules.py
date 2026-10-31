"""Invented container recovery controls; no original ISO or executable runs."""

import copy
import io
import json
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

from scripts import inventory_supplemental_modules as subject


def model():
    """Four ISO files and four exact archive bodies, with visible sector padding."""
    image = bytearray(16 * 2048)
    files, expected = [], {}
    for number, (path, filename, _) in enumerate(subject.ISO_SELECTION, 1):
        raw = bytes(352) if number == 2 else b"~PSP" + bytes([number]) * 348
        image[number * 2048:number * 2048 + len(raw)] = raw
        files.append({"path": path, "lba": number, **subject.pilot.identity(raw)})
        expected[filename] = raw
    archive = {"lba": 8, "size": 4 * 2048}
    entries = [{} for _ in range(21)]
    for block, number in enumerate(subject.ARCHIVE_SELECTION):
        raw = b"~SCE" + bytes([number]) * (93 + block)
        start = (8 + block) * 2048
        image[start:start + 2048] = b"\xee" * 2048
        image[start:start + len(raw)] = raw
        entries[number] = {"archive_index": number, "stored_length": len(raw),
            "extent_size": 2048, "prefix_size": 64, "raw_magic": b"~SCE".hex(),
            "raw_prefix_sha256": subject.pilot.identity(raw[:64])["sha256"], "block": block}
        expected[f"archive-entry-{number:04d}.bin"] = raw
    return bytes(image), files, archive, entries, expected


class ContainerTests(unittest.TestCase):
    def setUp(self):
        self.image, self.files, self.archive, self.entries, self.expected = model()

    def records(self, **overrides):
        values = dict(stream=io.BytesIO(self.image), iso_size=len(self.image), files=self.files,
            archive=self.archive, entries=self.entries,
            control_bytes=self.expected["main-eboot-control.bin"])
        values.update(overrides)
        return subject.payload_records(**values)

    def test_declared_header_is_bounded_and_never_authenticated_or_code_extent(self):
        for raw in [b"", b"~SCE" + bytes(400), b"~PSP" + bytes(331)]:
            self.assertEqual(subject.describe_header(raw)["status"], "UNINTERPRETED")
        raw = bytearray(352)
        raw[:4] = b"~PSP"
        raw[10:17] = b"example"
        struct.pack_into("<I", raw, 0x28, 0xffffffff)
        struct.pack_into("<I", raw, 0x2c, len(raw))
        struct.pack_into("<i", raw, 0x38, -1)
        struct.pack_into("<I", raw, 0xd0, 0x12345678)
        row = subject.describe_header(bytes(raw))
        self.assertEqual(row["module_name"], "example")
        self.assertEqual(row["declared_bss_size"], -1)
        self.assertEqual(row["declared_tag_hex"], "12345678")
        self.assertTrue(row["declared_psp_size_equals_actual"])
        self.assertFalse(row["metadata_authenticated"])
        self.assertFalse(row["declared_sizes_are_validated_code_extents"])
        self.assertIsNone(row["code_extent"])

    def test_exact_eight_payloads_exclude_padding_and_audit_every_boot_byte(self):
        records = self.records()
        self.assertEqual(len(records), 8)
        self.assertEqual({name: raw for name, raw, _ in records}, self.expected)
        self.assertTrue(records[1][2]["entire_payload_zero"])
        changed = bytearray(self.image)
        changed[2 * 2048 + 351] = 1
        files = copy.deepcopy(self.files)
        files[1].update(subject.pilot.identity(bytes(changed[2 * 2048:2 * 2048 + 352])))
        boot = self.records(stream=io.BytesIO(changed), files=files)[1][2]
        self.assertEqual(boot["full_nonzero_byte_count"], 1)
        self.assertFalse(boot["entire_payload_zero"])

    def test_selected_iso_missing_duplicate_hash_and_out_of_bounds_fail(self):
        variants = [self.files[1:], self.files + [self.files[0]]]
        for key, value in [("size", subject.MAX_PAYLOAD + 1), ("lba", 1000), ("sha256", "0" * 64)]:
            files = copy.deepcopy(self.files)
            files[0][key] = value
            variants.append(files)
        for files in variants:
            with self.subTest(files=files), self.assertRaises(ValueError):
                self.records(files=files)
        with self.assertRaises(ValueError):
            self.records(stream=io.BytesIO(self.image[:3000]))

    def test_archive_exact_length_extent_index_and_prefix_guards_fail(self):
        for key, value in [("stored_length", 63), ("stored_length", 2049),
                           ("stored_length", subject.MAX_PAYLOAD + 1), ("archive_index", 18),
                           ("prefix_size", 63), ("raw_magic", "00000000"),
                           ("raw_prefix_sha256", "0" * 64), ("block", 1000)]:
            entries = copy.deepcopy(self.entries)
            entries[17][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                self.records(entries=entries)

    def test_main_eboot_control_requires_complete_bytes(self):
        for raw in [self.expected["main-eboot-control.bin"][:-1], b"x" * 352]:
            with self.assertRaises(ValueError):
                self.records(control_bytes=raw)

    def test_stage_rejects_missing_extra_changed_and_linked_products(self):
        records = self.records()
        for mode in ["missing", "extra", "changed", "manifest", "linked_manifest", "linked_stage"]:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                stage = root / "stage"
                stage.mkdir()
                for name, raw, _ in records:
                    (stage / name).write_bytes(raw)
                (stage / "manifest.json").write_bytes(b"manifest")
                if mode == "missing": (stage / records[0][0]).unlink()
                if mode == "extra": (stage / "unexpected").write_bytes(b"x")
                if mode == "changed": (stage / records[0][0]).write_bytes(b"changed")
                if mode == "manifest": (stage / "manifest.json").write_bytes(b"changed")
                if mode.startswith("linked"):
                    target = stage / "manifest.json" if mode == "linked_manifest" else stage
                    saved = root / "saved"
                    target.rename(saved)
                    try: target.symlink_to(saved, target_is_directory=mode == "linked_stage")
                    except OSError:
                        if os.name == "nt": continue
                        raise
                with self.assertRaises(ValueError):
                    subject.audit_stage(stage, records, b"manifest")


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "config").mkdir()
        (self.root / "evidence").mkdir()
        self.image, self.files, archive, entries, self.expected = model()
        self.iso = self.root / "invented.iso"
        self.iso.write_bytes(self.image)
        self.output_parent = self.root / "reference/uljm05800-v102/supplemental-sets"
        self.config = {"output_parent_relative_path": str(self.output_parent.relative_to(self.root)),
            "inventory_profile": {"relative_path": "config/inventory.json"},
            "main_control": {"relative_path": "control.bin"}}
        self.profile = self.root / "config/supplemental.json"
        self.profile.write_text(json.dumps(self.config))
        (self.root / "control.bin").write_bytes(self.expected["main-eboot-control.bin"])
        self.lock = subject.pilot.file_identity(self.iso)
        self.known = {"archive": archive, "entries": entries}
        self.supplied = ({}, self.known, self.lock, {}, {"files": self.files})
        self.verify = mock.patch.object(subject, "verify_inputs", return_value=self.supplied).start()
        self.inventory = mock.patch.object(subject.inventory, "inventory_overlays", return_value=self.known).start()
        self.inspect = mock.patch.object(subject.pilot, "inspect_iso", return_value={**self.lock, "files": self.files}).start()
        self.addCleanup(mock.patch.stopall)

    def recover(self, name="one", **kwargs):
        return subject.recover_supplemental(self.iso, self.output_parent / name,
            root=self.root, config_path=self.profile, **kwargs)

    def test_fresh_repeat_sets_and_manifests_are_exact_and_deterministic(self):
        one = self.recover()
        two = self.recover("two")
        self.assertEqual(one, two)
        self.assertEqual(one["payload_count"], 8)
        for name, raw in self.expected.items():
            self.assertEqual((self.output_parent / "one" / name).read_bytes(), raw)
            self.assertEqual((self.output_parent / "two" / name).read_bytes(), raw)
        self.assertEqual((self.output_parent / "one/manifest.json").read_bytes(),
                         (self.output_parent / "two/manifest.json").read_bytes())
        self.assertEqual(self.iso.read_bytes(), self.image)

    def test_existing_destination_and_report_are_preserved(self):
        self.recover()
        saved = (self.output_parent / "one/manifest.json").read_bytes()
        with self.assertRaises(ValueError): self.recover()
        report = self.root / "evidence/report.json"
        report.write_bytes(b"preserve")
        with self.assertRaises(ValueError): self.recover("two", report_path=report)
        self.assertEqual(report.read_bytes(), b"preserve")
        self.assertEqual((self.output_parent / "one/manifest.json").read_bytes(), saved)

    def test_report_alias_and_output_escape_fail_before_inventory(self):
        for report in [self.iso, self.profile, self.root.parent / "escape.json"]:
            with self.subTest(report=report), self.assertRaises(ValueError):
                self.recover(report_path=report)
        with self.assertRaises(ValueError):
            subject.recover_supplemental(self.iso, self.root / "elsewhere",
                root=self.root, config_path=self.profile)
        self.inventory.assert_not_called()

    def test_late_iso_mutation_with_restored_size_and_mtime_blocks_publication(self):
        before = self.iso.stat()
        def verify(*args):
            if self.verify.call_count == 2:
                changed = bytearray(self.image); changed[-1] ^= 1
                self.iso.write_bytes(changed)
                os.utime(self.iso, ns=(before.st_atime_ns, before.st_mtime_ns))
            return self.supplied
        self.verify.side_effect = verify
        with self.assertRaises(ValueError): self.recover()
        self.assertFalse((self.output_parent / "one").exists())

    def test_fresh_inventory_directory_and_late_pin_mismatch_block_publication(self):
        self.inventory.return_value = {"different": True}
        with self.assertRaises(ValueError): self.recover()
        self.inventory.return_value = self.known
        self.inspect.return_value = {**self.lock, "files": []}
        with self.assertRaises(ValueError): self.recover()
        self.inspect.return_value = {**self.lock, "files": self.files}
        self.verify.side_effect = [self.supplied, ValueError("pinned source changed")]
        with self.assertRaises(ValueError): self.recover()
        self.assertFalse((self.output_parent / "one").exists())

    def test_late_staged_mutation_and_manifest_link_are_rejected(self):
        for mode in ["payload", "extra", "manifest_link"]:
            with self.subTest(mode=mode):
                self.verify.reset_mock()
                def verify(*args):
                    if self.verify.call_count == 2:
                        stage = next(self.output_parent.glob(".supplemental-*"))
                        if mode == "payload": (stage / "boot.bin").write_bytes(b"changed")
                        elif mode == "extra": (stage / "unexpected").write_bytes(b"x")
                        else:
                            path = stage / "manifest.json"
                            saved = self.root / "saved-manifest"
                            saved.write_bytes(path.read_bytes()); path.unlink()
                            try: path.symlink_to(saved)
                            except OSError:
                                if os.name == "nt": raise ValueError("host symlink privilege unavailable")
                                raise
                    return self.supplied
                self.verify.side_effect = verify
                with self.assertRaises(ValueError): self.recover()
                self.assertFalse((self.output_parent / "one").exists())


if __name__ == "__main__":
    unittest.main()
