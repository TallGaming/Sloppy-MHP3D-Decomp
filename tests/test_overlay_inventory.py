"""Bounded overlay-prefix inventory checks using invented ISO/archive bytes."""

import copy
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import unittest
from unittest import mock

from scripts import inventory_overlays as tool
from scripts.elf32 import Elf32
from tests import test_extract_overlay as invented

BLOCK = 2048


def mapped_elf(table, descriptors=(("sample.ovl", 0x09000000),),
               reservations=((0x09000000, 112),)):
    """Invent a bounded ELF with optional duplicate names/reservations."""
    raw = bytearray(0x1000)
    names = bytearray(b"\0.shstrtab\0.data\0")
    offsets = []
    for name, address in descriptors:
        offsets.append(len(names))
        names += name.encode() + b"\0"
    raw[0x100:0x200] = table
    raw[0x220:0x220 + len(names)] = names
    struct.pack_into("<16sHHIIIIIHHHHHH", raw, 0,
                     b"\x7fELF\x01\x01\x01" + bytes(9), 2, 8, 1,
                     0x08804000, 52, 0x400, 0, 52, 32,
                     1 + len(reservations), 40, 3 + len(descriptors), 1)
    struct.pack_into("<8I", raw, 52, 1, 0x100, 0x08804000, 0, 256, 256, 6, 4)
    for index, (address, size) in enumerate(reservations, 1):
        struct.pack_into("<8I", raw, 52 + 32 * index,
                         0, 0x200, address, 0, 0, size, 7, 4)
    sections = [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                (1, 3, 0, 0, 0x220, len(names), 0, 0, 1, 0),
                (11, 1, 3, 0x08804000, 0x100, 256, 0, 0, 4, 0)]
    sections += [(offset, 1, 2, address, 0x200, 0, 0, 0, 4, 0)
                 for offset, (name, address) in zip(offsets, descriptors)]
    for index, section in enumerate(sections):
        struct.pack_into("<10I", raw, 0x400 + index * 40, *section)
    return bytes(raw)


class OverlayHeaderTests(unittest.TestCase):
    def test_header_uses_stored_size_not_prefix_or_sector_and_keeps_raw_words(self):
        payload = bytes(invented.overlay_bytes())
        header = tool.parse_header(payload[:64], len(payload))
        self.assertEqual((header["code_size"], header["data_size"], header["bss_size"]),
                         (16, 16, 16))
        self.assertEqual(header["raw_0x18"], 0x09000060)
        self.assertEqual(header["raw_0x1c"], 0x09000060)
        self.assertNotIn("entry_address", header)
        with self.assertRaises(ValueError):
            tool.parse_header(payload[:64], BLOCK)
        with self.assertRaises(ValueError):
            tool.parse_header(payload, len(payload))

    def test_malformed_claims_reject_bounds_lengths_alignment_and_names(self):
        good = bytes(invented.overlay_bytes())
        cases = [(good[:63], 96), (good[:64], 63), (good[:64], 95)]
        for offset, value in ((8, 0xFFFFFFFC), (8, 0x09000001),
                              (12, 15), (12, 0xFFFFFFFC), (20, 0xFFFFFFFF)):
            bad = bytearray(good[:64]); struct.pack_into("<I", bad, offset, value)
            cases.append((bytes(bad), 96))
        for name in (b"../x.ovl\0", b"dir/x.ovl\0", b"\xff.ovl\0", b"no_extension\0", b"x" * 32):
            bad = bytearray(good[:64]); bad[32:64] = name.ljust(32, b"\0")
            cases.append((bytes(bad), 96))
        for prefix, length in cases:
            with self.subTest(prefix=prefix.hex(), length=length), self.assertRaises(ValueError):
                tool.parse_header(prefix, length)

    def test_associations_preserve_all_candidates_and_independent_id_agreement(self):
        data = bytes(invented.overlay_bytes())
        header = tool.parse_header(data[:64], len(data))
        elf = Elf32(mapped_elf(bytes(range(256)),
                              descriptors=(("sample.ovl", 0x09000000), ("sample.ovl", 0x09000000)),
                              reservations=((0x09000000, 112), (0x09000000, 112),
                                            (0x09000000, 116), (0x09000004, 112))))
        result = tool.associations(header, 96, elf)
        self.assertEqual(result["descriptor_candidates"], [3, 4])
        self.assertEqual(result["reservation_candidates"], [1, 2])
        self.assertTrue(result["header_id_agrees_with_reservation_index"])
        self.assertTrue(result["reservation_value_ambiguity"])
        header["id"] = 99
        self.assertFalse(tool.associations(header, 96, elf)["header_id_agrees_with_reservation_index"])
        header["load_address"] += 4
        self.assertEqual(tool.associations(header, 96, elf)["descriptor_candidates"], [])

    def test_scan_short_entries_never_rounds_past_exact_length_or_reads_empty_extent(self):
        lengths = (0, 1, 3, 4, 63, 64, 65)
        index = {"blocks": [0, 0, 1, 2, 3, 4, 5, 6],
                 "exact_sizes": dict(enumerate(lengths))}
        with mock.patch.object(tool.pilot, "read_extent", wraps=tool.pilot.read_extent) as reads:
            result = tool.scan_prefixes(io.BytesIO(b"X" * (6 * BLOCK)), 0, 6 * BLOCK,
                                       index, bytes(range(256)), Elf32(mapped_elf(bytes(range(256)))))
        self.assertEqual([c.args[4] for c in reads.call_args_list], [1, 3, 4, 63, 64, 64])
        self.assertEqual([r["decoded_prefix_size"] for r in result["entries"]], [0, 0, 0, 4, 60, 64, 64])
        self.assertEqual(result["prefix_bytes_read"], 199)
        self.assertEqual(result["maximum_entry_prefix_bytes_read"], 64)
        self.assertEqual(result["full_overlay_payloads_recovered"], 0)
        with self.assertRaises(ValueError):
            tool.scan_prefixes(io.BytesIO(bytes(63)), 0, BLOCK,
                               {"blocks": [0, 1], "exact_sizes": {}},
                               bytes(range(256)), Elf32(mapped_elf(bytes(range(256)))))

    def test_raw_encoded_and_malformed_mwo3_claims_are_all_visible(self):
        table = bytes(reversed(range(256)))
        payload = bytes(invented.overlay_bytes())
        archive = bytearray(3 * BLOCK)
        archive[:64] = payload[:64]
        archive[BLOCK:BLOCK + 64] = invented.encode_fixture(payload[:64], 1, table)
        archive[2 * BLOCK:2 * BLOCK + 4] = b"MWo3"
        index = {"blocks": [0, 1, 2, 3], "exact_sizes": {0: 96, 1: 96, 2: 4}}
        report = tool.scan_prefixes(io.BytesIO(archive), 0, len(archive), index,
                                    table, Elf32(mapped_elf(table)))
        self.assertEqual([(r["archive_index"], r["encoding"]) for r in report["overlays"]],
                         [(0, "raw"), (1, "deobfuscated")])
        self.assertEqual([(r["archive_index"], r["encoding"]) for r in report["invalid_overlay_candidates"]], [(2, "raw")])
        self.assertEqual(report["coverage"]["multiply_matched_descriptor_indexes"], [3])
        self.assertEqual(report["status"], "OVERLAY_PREFIX_INVENTORY_INCOMPLETE")
        self.assertFalse(report["coverage"]["complete_game_code_inventory_established"])


class OverlayInventoryTests(unittest.TestCase):
    def setUp(self):
        self.fixture = invented.ExtractOverlayTests(methodName="runTest")
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        f = self.fixture
        self.root, self.iso, self.elf = f.root, f.iso, f.elf
        self.config_path = self.root / "inventory.json"
        self.report_path = self.root / "inventory-report.json"
        self.config = {"schema_version": 1, "status": "frozen_before_inventory",
                       "reference_lock": self.pin(f.lock_path), "pilot_lock": self.pin(f.pilot_path),
                       "maximum_prefix_bytes": 64, "expected_named_descriptors": 1,
                       "full_payload_recovery": False, "interpret_final_address_words": False}
        self.save()

    def pin(self, path):
        return {"relative_path": path.relative_to(self.root).as_posix(),
                **invented.identity(path.read_bytes())}

    def save(self):
        self.config_path.write_text(json.dumps(self.config))

    def refresh(self):
        f = self.fixture
        f.lock["size"] = self.iso.stat().st_size
        f.lock["sha256"] = hashlib.sha256(self.iso.read_bytes()).hexdigest()
        f.lock["decrypted_executable"] = invented.identity(self.elf.read_bytes())
        f.pilot["reference_sha256"] = f.lock["sha256"]
        f.save_locks()
        self.config["reference_lock"] = self.pin(f.lock_path)
        self.config["pilot_lock"] = self.pin(f.pilot_path)
        self.save()

    def inventory(self, report=True):
        return tool.inventory_overlays(self.iso, root=self.root, config_path=self.config_path,
                                       elf_path=self.elf, report_path=self.report_path if report else None)

    def test_full_real_parser_pipeline_is_repeatable_bounded_and_read_only(self):
        before = {p: p.read_bytes() for p in (self.iso, self.elf, self.fixture.lock_path,
                                             self.fixture.pilot_path, self.config_path)}
        with mock.patch.object(tool.pilot, "read_extent", wraps=tool.pilot.read_extent) as reads:
            first = self.inventory()
        self.assertEqual([c.args[4] for c in reads.call_args_list], [BLOCK, 64, 64, 64])
        self.assertEqual(first["status"], "OVERLAY_PREFIX_INVENTORY_COMPLETE")
        self.assertEqual(first["coverage"]["entry_count"], 3)
        self.assertEqual(first["coverage"]["valid_overlay_headers"], 1)
        header = first["overlays"][0]
        self.assertEqual((header["archive_index"], header["encoding"]), (1, "deobfuscated"))
        self.assertEqual(header["header_bytes_hex"], self.fixture.plain[:64].hex())
        self.assertEqual(header["descriptor_candidates"], [3])
        self.assertEqual(header["reservation_candidates"], [1])
        self.assertEqual(first["full_overlay_payloads_recovered"], 0)
        self.assertEqual(first["matched_progress"], 0)
        self.assertFalse(first["runtime_tested"])
        second_path = self.root / "repeat.json"
        second = tool.inventory_overlays(self.iso, root=self.root, config_path=self.config_path,
                                         elf_path=self.elf, report_path=second_path)
        self.assertEqual(first, second)
        self.assertEqual(self.report_path.read_bytes(), second_path.read_bytes())
        for path, data in before.items(): self.assertEqual(path.read_bytes(), data)
        self.assertFalse(self.fixture.output.exists())

    def test_catalogue_lock_checks_all_digests_but_fresh_iso_uses_supported_fields(self):
        f = self.fixture
        f.lock.update(tool.pilot.file_identity(self.iso))
        f.save_locks()
        self.config["reference_lock"] = self.pin(f.lock_path)
        self.save()
        report = self.inventory(False)
        self.assertEqual(report["status"], "OVERLAY_PREFIX_INVENTORY_COMPLETE")
        for field in ("sha1", "md5", "crc32"):
            original = f.lock[field]
            f.lock[field] = "0" * len(original)
            f.save_locks()
            self.config["reference_lock"] = self.pin(f.lock_path)
            self.save()
            with self.subTest(field=field), mock.patch.object(tool, "scan_prefixes") as scan:
                with self.assertRaises(ValueError): self.inventory()
                scan.assert_not_called()
            f.lock[field] = original
        self.assertFalse(self.report_path.exists())

    def test_wrong_identities_scope_directory_table_and_descriptor_set_fail_closed(self):
        f = self.fixture
        for key, value in (("maximum_prefix_bytes", 65), ("full_payload_recovery", True),
                           ("interpret_final_address_words", True), ("status", "review"),
                           ("expected_named_descriptors", 2)):
            old = copy.deepcopy(self.config); self.config[key] = value; self.save()
            with self.subTest(key=key), self.assertRaises(ValueError): self.inventory()
            self.config = old; self.save()
        for path in (self.iso, self.elf, f.lock_path, f.pilot_path):
            old = path.read_bytes(); path.write_bytes(old + b"tampered")
            with self.subTest(path=path.name), self.assertRaises((ValueError, json.JSONDecodeError)): self.inventory()
            path.write_bytes(old)
        for section, field, value in (("archive", "lba", 23), ("decode_table", "elf_address", 0x08804004),
                                      ("directory", "decoded_sha256", "0" * 64),
                                      ("directory", "entry_count", 4)):
            old = copy.deepcopy(f.pilot); f.pilot[section][field] = value; self.refresh()
            with self.subTest(section=section, field=field), self.assertRaises(ValueError): self.inventory()
            f.pilot = old; self.refresh()
        self.assertFalse(self.report_path.exists())

    def test_duplicate_map_and_malformed_claim_remain_explicit_incomplete_reports(self):
        f = self.fixture
        self.elf.write_bytes(mapped_elf(f.table,
            descriptors=(("sample.ovl", 0x09000000), ("sample.ovl", 0x09000000)),
            reservations=((0x09000000, 112), (0x09000000, 112))))
        self.config["expected_named_descriptors"] = 2; self.refresh()
        report = self.inventory(False)
        self.assertEqual(report["status"], "OVERLAY_PREFIX_INVENTORY_INCOMPLETE")
        self.assertEqual(report["overlays"][0]["descriptor_candidates"], [3, 4])
        self.assertEqual(report["overlays"][0]["reservation_candidates"], [1, 2])
        self.assertEqual(report["coverage"]["unresolved_overlay_indexes"], [0])
        archive = bytearray(f.archive)
        bad = bytearray(f.plain[:64]); bad[32:64] = b"../evil.ovl\0".ljust(32, b"\0")
        archive[2 * BLOCK:2 * BLOCK + 64] = invented.encode_fixture(bad, 2, f.table)
        self.iso.write_bytes(invented.archive_iso(archive))
        f.pilot["archive"].update(invented.identity(archive)); self.refresh()
        report = self.inventory()
        self.assertEqual(report["status"], "OVERLAY_PREFIX_INVENTORY_INCOMPLETE")
        self.assertEqual(len(report["invalid_overlay_candidates"]), 1)
        self.assertEqual(report["invalid_overlay_candidates"][0]["archive_index"], 1)
        self.assertEqual(report["overlays"], [])
        self.assertEqual(json.loads(self.report_path.read_text()), report)

    def test_report_aliases_and_conflicts_reject_before_prefix_reads(self):
        for path in (self.iso, self.elf, self.fixture.lock_path, self.fixture.pilot_path, self.config_path):
            before = path.read_bytes()
            with self.subTest(path=path.name), mock.patch.object(tool, "scan_prefixes") as scan:
                with self.assertRaises(ValueError):
                    tool.inventory_overlays(self.iso, root=self.root, config_path=self.config_path,
                                            elf_path=self.elf, report_path=path)
                scan.assert_not_called()
            self.assertEqual(path.read_bytes(), before)
        self.report_path.write_bytes(b"prior evidence")
        with mock.patch.object(tool, "scan_prefixes") as scan, self.assertRaises(ValueError): self.inventory()
        scan.assert_not_called()
        self.assertEqual(self.report_path.read_bytes(), b"prior evidence")

    def test_post_scan_input_mutations_even_iso_with_restored_mtime_prevent_publication(self):
        for path in (self.iso, self.elf, self.fixture.lock_path, self.fixture.pilot_path, self.config_path):
            original = path.read_bytes(); before = path.stat(); scan = tool.scan_prefixes
            def mutate(*args, **kwargs):
                result = scan(*args, **kwargs)
                raw = bytearray(path.read_bytes()); raw[-1] ^= 1; path.write_bytes(raw)
                os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
                return result
            with self.subTest(path=path.name), mock.patch.object(tool, "scan_prefixes", side_effect=mutate):
                with self.assertRaises(ValueError): self.inventory()
            self.assertFalse(self.report_path.exists())
            path.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
