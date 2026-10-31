"""Executable-map semantics and CLI checks using synthetic ELF metadata."""

import hashlib
import io
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

from scripts.map_executable import build_map, main


def make_executable():
    """Build repeated section names and deliberately ambiguous overlay metadata."""
    image = bytearray(0x600)
    section_names = ["", ".shstrtab", ".text", ".text", ".sceStub.text",
                     ".data", ".bss", "alpha.ovl", ".relalpha.ovl",
                     "beta.ovl", "gamma.ovl", ".comment"]
    table = bytearray(b"\0")
    offsets = {"": 0}
    for name in section_names[1:]:
        if name not in offsets:
            offsets[name] = len(table)
            table += name.encode("ascii") + b"\0"
    image[0x100:0x100 + len(table)] = table
    image[0x200:0x220] = bytes(range(32))
    comment = b"Synthetic compiler\0PSP\0"
    image[0x240:0x240 + len(comment)] = comment
    ident = b"\x7fELF\x01\x01\x01" + bytes(9)
    struct.pack_into("<16sHHIIIIIHHHHHH", image, 0, ident, 2, 8, 1,
                     0x08804000, 52, 0x300, 0, 52, 32, 4, 40, len(section_names), 1)
    programs = [
        (1, 0x200, 0x08804000, 0, 0x20, 0x40, 7, 16),
        (0, 0x220, 0x09000000, 0, 0, 0x100, 7, 16),
        (0, 0x220, 0x09000000, 0, 0, 0x200, 7, 16),
        (0, 0x220, 0x09100000, 0, 0, 0x80, 7, 16),
    ]
    for index, program in enumerate(programs):
        struct.pack_into("<8I", image, 52 + index * 32, *program)
    # type, flags, address, file offset, size; indices are intentionally stable.
    descriptions = [
        (0, 0, 0, 0, 0), (3, 0, 0, 0x100, len(table)),
        (1, 6, 0x08804000, 0x200, 4),
        (1, 6, 0x08804004, 0x204, 4),
        (1, 6, 0x08804008, 0x208, 8),
        (1, 3, 0x08804010, 0x210, 16),
        (8, 3, 0x08804020, 0x220, 0x20),
        (1, 7, 0x09000000, 0x220, 0),
        (9, 0, 0, 0x220, 0),
        (1, 7, 0x09000000, 0x220, 0),
        (1, 7, 0x09100000, 0x220, 0),
        (1, 0, 0, 0x240, len(comment)),
    ]
    for index, (kind, flags, address, offset, size) in enumerate(descriptions):
        struct.pack_into("<10I", image, 0x300 + index * 40,
                         offsets[section_names[index]], kind, flags, address,
                         offset, size, 0, 0, 4, 0)
    return image


class ExecutableMapTests(unittest.TestCase):
    def test_map_is_deterministic_and_preserves_duplicate_section_indices(self):
        image = make_executable()
        report = build_map(image)
        self.assertEqual(report, build_map(image))
        self.assertEqual(report["source"]["sha256"], hashlib.sha256(image).hexdigest())
        self.assertEqual(report["named_region_section_indices"]["main_code"], [2, 3])
        self.assertEqual(report["sections"][2]["offset"], 0x200)
        self.assertEqual(report["sections"][3]["offset"], 0x204)
        self.assertEqual(report["counts"]["sections"], 12)
        self.assertEqual(report["counts"]["program_headers"], 4)

    def test_overlay_descriptors_are_not_extracted_payloads(self):
        report = build_map(make_executable())
        self.assertEqual(report["counts"]["overlay_descriptors"], 3)
        self.assertEqual(report["counts"]["overlay_start_groups"], 2)
        self.assertEqual(report["counts"]["zero_sized_overlay_descriptors"], 3)
        self.assertEqual(report["counts"]["extracted_overlay_payloads"], 0)
        self.assertEqual(report["counts"]["descriptors_with_embedded_bytes"], 0)
        self.assertTrue(all(not item["payload_extracted"]
                            for item in report["overlay_descriptors"]))
        self.assertNotIn(".relalpha.ovl", [item["name"]
                                           for item in report["overlay_descriptors"]])

    def test_shared_address_metadata_is_explicitly_ambiguous(self):
        report = build_map(make_executable())
        descriptors = {item["name"]: item for item in report["overlay_descriptors"]}
        self.assertEqual(descriptors["alpha.ovl"]["matching_program_indices"], [1, 2])
        self.assertEqual(descriptors["beta.ovl"]["matching_program_indices"], [1, 2])
        self.assertEqual(descriptors["alpha.ovl"]["pairing_status"], "ambiguous_candidates")
        self.assertEqual(descriptors["gamma.ovl"]["matching_program_indices"], [3])
        self.assertEqual(descriptors["gamma.ovl"]["pairing_status"], "unique_candidate")
        slot = report["overlay_start_groups"][0]
        self.assertEqual(slot["address"], 0x09000000)
        self.assertEqual(slot["descriptor_count"], 2)
        self.assertEqual(slot["max_reserved_size"], 0x200)

    def test_nonzero_descriptor_size_does_not_claim_extraction(self):
        image = make_executable()
        struct.pack_into("<I", image, 0x300 + 7 * 40 + 20, 4)
        report = build_map(image)
        self.assertEqual(report["counts"]["descriptors_with_embedded_bytes"], 1)
        self.assertEqual(report["counts"]["extracted_overlay_payloads"], 0)

    def test_load_zero_fill_is_not_replaced_by_zero_sized_bss_section(self):
        image = make_executable()
        struct.pack_into("<I", image, 0x300 + 6 * 40 + 20, 0)
        report = build_map(image)
        load = report["load_segments"][0]
        self.assertEqual(load["zero_fill_range"],
                         {"start": 0x08804020, "end": 0x08804040, "size": 0x20})
        self.assertEqual(report["counts"]["load_segments"], 1)
        self.assertEqual(report["program_headers"][1]["type_name"], "PT_NULL")

    def test_overlay_name_alone_does_not_make_a_code_descriptor(self):
        for field, value in (("type", 8), ("flags", 0)):
            with self.subTest(field=field):
                image = make_executable()
                offset = 4 if field == "type" else 8
                struct.pack_into("<I", image, 0x300 + 7 * 40 + offset, value)
                report = build_map(image)
                self.assertEqual(report["counts"]["overlay_descriptors"], 2)

    def test_non_executable_elf_is_rejected(self):
        image = make_executable()
        struct.pack_into("<H", image, 16, 1)
        with self.assertRaisesRegex(ValueError, "ET_EXEC"):
            build_map(image)

    def test_truncated_section_table_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "bounds"):
            build_map(make_executable()[:0x320])

    def test_virtual_address_overflow_is_rejected(self):
        image = make_executable()
        struct.pack_into("<I", image, 52 + 8, 0xFFFFFFF0)
        with self.assertRaisesRegex(ValueError, "address space"):
            build_map(image)

    def test_cli_checks_identity_and_preserves_different_existing_report(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            elf = root / "synthetic.elf"
            data = make_executable()
            elf.write_bytes(data)
            lock = root / "reference.json"
            settings = {"status": "active", "baseline_selected_by_user": True,
                        "decrypted_executable": {"relative_path": "unused",
                                                 "size": len(data),
                                                 "sha256": hashlib.sha256(data).hexdigest()}}
            lock.write_text(json.dumps(settings), encoding="utf-8")
            report = root / "map.json"
            arguments = ["--elf", str(elf), "--lock", str(lock), "--out", str(report)]
            with mock.patch("sys.stdout", new_callable=io.StringIO):
                self.assertEqual(main(arguments), 0)
                before = report.read_bytes()
                self.assertEqual(main(arguments), 0)
                self.assertEqual(report.read_bytes(), before)
            report.write_text("existing evidence", encoding="utf-8")
            with mock.patch("sys.stderr", new_callable=io.StringIO):
                self.assertNotEqual(main(arguments), 0)
            self.assertEqual(report.read_text(encoding="utf-8"), "existing evidence")
            self.assertEqual(elf.read_bytes(), data)

    def test_cli_hash_mismatch_creates_no_report(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            elf = root / "synthetic.elf"
            data = make_executable()
            elf.write_bytes(data)
            lock = root / "reference.json"
            lock.write_text(json.dumps({"status": "active", "baseline_selected_by_user": True,
                                       "decrypted_executable": {"size": len(data),
                                                                "sha256": "0" * 64}}))
            report = root / "map.json"
            with mock.patch("sys.stderr", new_callable=io.StringIO):
                result = main(["--elf", str(elf), "--lock", str(lock), "--out", str(report)])
            self.assertNotEqual(result, 0)
            self.assertFalse(report.exists())

    def test_cli_report_cannot_replace_its_elf_input(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            elf = root / "synthetic.elf"
            data = make_executable()
            elf.write_bytes(data)
            lock = root / "reference.json"
            lock.write_text(json.dumps({"status": "active", "baseline_selected_by_user": True,
                                       "decrypted_executable": {"size": len(data),
                                                                "sha256": hashlib.sha256(data).hexdigest()}}))
            with mock.patch("sys.stderr", new_callable=io.StringIO):
                result = main(["--elf", str(elf), "--lock", str(lock), "--out", str(elf)])
            self.assertNotEqual(result, 0)
            self.assertEqual(elf.read_bytes(), data)


if __name__ == "__main__":
    unittest.main()
