"""Invented i386 PE and listing controls; no compiler or debugger execution."""

import copy
import hashlib
import json
from pathlib import Path
import struct
import tempfile
import unittest
from unittest import mock

from scripts import inspect_compiler_trace as trace


BASE = 0x400000
OPT = 0x98
SECTIONS = 0x178
TEXT, DATA, RELOCS = 0x200, 0x400, 0x600
MARKER = {"file_offset": DATA + 0x20, "text": "After invented stage"}
TARGET = BASE + 0x2020


def relocation_blocks(entries):
    groups = {}
    for place, kind in entries:
        groups.setdefault(place & ~0xfff, []).append((kind << 12) | (place & 0xfff))
    output = bytearray()
    for page, records in sorted(groups.items()):
        if len(records) % 2: records.append(0)
        output.extend(struct.pack("<II", page, 8 + 2 * len(records)))
        output.extend(struct.pack("<" + "H" * len(records), *records))
    return bytes(output)


def fixture():
    """Construct known encodings, unsupported forms, data pointers and unrelocated hits."""
    raw = bytearray(0x800)
    raw[:2] = b"MZ"
    struct.pack_into("<I", raw, 60, 0x80)
    raw[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", raw, 0x84, 0x14c, 3, 0, 0, 0, 0xe0, 0x102)
    struct.pack_into("<H", raw, OPT, 0x10b)
    struct.pack_into("<I", raw, OPT + 16, 0x1000)
    struct.pack_into("<I", raw, OPT + 28, BASE)
    struct.pack_into("<II", raw, OPT + 56, 0x4000, 0x200)
    struct.pack_into("<I", raw, OPT + 92, 16)
    for index, (name, rva, file_offset, flags) in enumerate(((b".text", 0x1000, TEXT, 0x60000020),
            (b".data", 0x2000, DATA, 0xc0000040), (b".reloc", 0x3000, RELOCS, 0x42000040))):
        off = SECTIONS + index * 40
        struct.pack_into("<8sIIII", raw, off, name, 0x200, rva, 0x200, file_offset)
        struct.pack_into("<I", raw, off + 36, flags)
    immediate = struct.pack("<I", TARGET)
    instructions = [(b"\x68" + immediate, "push marker"), (b"\xb8" + immediate, "mov eax,marker"),
        (b"\xc7\x05" + struct.pack("<I", BASE + 0x2080) + immediate, "mov [destination],marker"),
        (b"\x8d\x05" + immediate, "lea eax,[marker]"),
        (b"\x05" + immediate, "add eax,marker"),
        (b"\xf3\x68" + immediate, "repz push marker"),
        (b"\x68" + immediate, "push unrelocated_value")]
    listing, cursor = [], 0
    for code, assembly in instructions:
        raw[TEXT + cursor:TEXT + cursor + len(code)] = code
        listing.append(f" {BASE + 0x1000 + cursor:x}:  {code.hex(' ')}  {assembly}")
        cursor += len(code)
    marker = MARKER["text"].encode() + b"\0"
    raw[DATA + 0x20:DATA + 0x20 + len(marker)] = marker
    struct.pack_into("<II", raw, DATA + 0x60, TARGET, TARGET)
    relocations = relocation_blocks([(0x1001, 3), (0x1006, 3), (0x1010, 3), (0x1016, 3),
                                      (0x101b, 3), (0x1021, 3), (0x2060, 3)])
    raw[RELOCS:RELOCS + len(relocations)] = relocations
    struct.pack_into("<II", raw, OPT + 96 + 5 * 8, 0x3000, len(relocations))
    return raw, "\n".join(listing) + "\n"


class CompilerTraceTests(unittest.TestCase):
    def setUp(self):
        self.raw, self.listing = fixture()

    def analyze(self, raw=None, markers=None, listing=None):
        return trace.analyze(bytes(self.raw if raw is None else raw), [MARKER] if markers is None else markers,
                             self.listing if listing is None else listing)

    def test_characterized_operands_data_pointers_and_unknowns_stay_separate(self):
        report = self.analyze()
        self.assertEqual(report["candidate_operand_count"], 4)
        label = report["markers"][0]
        self.assertEqual((label["file_offset"], label["rva"], label["preferred_va"]), (DATA + 0x20, 0x2020, TARGET))
        refs = label["references"]
        self.assertEqual(len(refs), 7)
        self.assertEqual([r["form"] for r in refs[:4]], ["PUSH_IMM32", "MOV_REG_IMM32", "MOV_RM_IMM32", "LEA_ABSOLUTE_DISP32"])
        self.assertEqual([r["status"] for r in refs[4:]], ["UNCLASSIFIED", "UNCLASSIFIED", "RELOCATED_DATA_POINTER"])
        self.assertFalse(report["live_hooks_validated"])
        self.assertFalse(report["pass_order_observed"])
        self.assertFalse(report["compiler_executed"])

    def test_missing_relocations_cannot_promote_dword_hits_to_code_references(self):
        struct.pack_into("<II", self.raw, OPT + 96 + 5 * 8, 0, 0)
        report = self.analyze()
        self.assertEqual(report["candidate_operand_count"], 0)
        self.assertEqual(report["markers"][0]["references"], [])

    def test_uncovered_operand_and_shifted_instruction_cannot_be_classified(self):
        lines = self.listing.splitlines()
        report = self.analyze(listing="\n".join(lines[1:]))
        ref = report["markers"][0]["references"][0]
        self.assertEqual(ref["status"], "UNCLASSIFIED")
        self.assertEqual(report["candidate_operand_count"], 3)
        for bad in ({"va": 0x1000, "raw": b"\xb9\x68" + struct.pack("<I", TARGET), "assembly": "unsupported blob"},
                    {"va": 0x1000, "raw": b"\x05" + struct.pack("<I", TARGET), "assembly": "add"}):
            self.assertIsNone(trace.label_operand(bad, 0x1001, TARGET))

    def test_c7_modrm_sib_displacement_lengths_are_characterized_exactly(self):
        immediate = struct.pack("<I", TARGET)
        valid = [b"\xc7\xc0" + immediate, b"\xc7\x00" + immediate,
                 b"\xc7\x40\x04" + immediate, b"\xc7\x80\x04\0\0\0" + immediate,
                 b"\xc7\x04\x24" + immediate, b"\xc7\x04\x25\x04\0\0\0" + immediate]
        for code in valid:
            with self.subTest(code=code.hex()):
                self.assertEqual(trace.label_operand({"va": 0x1000, "raw": code}, 0x1000 + len(code) - 4, TARGET), "MOV_RM_IMM32")
        for code in (b"\xc7\xc0\x90" + immediate, b"\xc7\x80" + immediate,
                     b"\xc7\x04" + immediate, b"\xc7\x0c\x24" + immediate,
                     b"\x66\xc7\x00" + immediate, b"\xc7\xc0" + immediate + b"\x90"):
            with self.subTest(code=code.hex()):
                self.assertIsNone(trace.label_operand({"va": 0x1000, "raw": code}, 0x1000 + len(code) - 4, TARGET))

    def test_wrong_operand_position_target_or_prefix_is_not_a_code_candidate(self):
        immediate = struct.pack("<I", TARGET)
        for code, operand in ((b"\x68" + immediate, 0x1002), (b"\xb8" + immediate, 0x1000),
                              (b"\x8d\x45" + immediate, 0x1002),
                              (b"\x67\x68" + immediate, 0x1002)):
            self.assertIsNone(trace.label_operand({"va": 0x1000, "raw": code}, operand, TARGET))
        self.assertIsNone(trace.label_operand({"va": 0x1000, "raw": b"\x68" + immediate}, 0x1001, TARGET + 1))

    def test_listing_byte_drift_overlaps_order_nonexec_and_invalid_lengths_fail(self):
        lines = self.listing.splitlines()
        bads = [self.listing.replace("68 20 20 40 00", "68 21 20 40 00", 1),
                self.listing + lines[0] + "\n", "\n".join(reversed(lines)),
                f"{TARGET:x}:  {self.raw[DATA + 0x20:DATA + 0x24].hex(' ')}  data\n",
                f"{BASE + 0x1000:x}:  {'90 ' * 16} nop\n",
                f"{BASE + 0x1000:x}:  68 20 20 40 00  \n"]
        for listing in bads:
            with self.subTest(listing=listing[:70]), self.assertRaises(ValueError): self.analyze(listing=listing)

    def test_marker_duplicate_wrong_bytes_missing_nul_and_executable_mapping_fail(self):
        with self.assertRaises(ValueError): self.analyze(markers=[MARKER, MARKER])
        bad = copy.deepcopy(MARKER); bad["text"] = "wrong"
        with self.assertRaises(ValueError): self.analyze(markers=[bad])
        raw = bytearray(self.raw); raw[MARKER["file_offset"] + len(MARKER["text"])] = 1
        with self.assertRaises(ValueError): self.analyze(raw)
        struct.pack_into("<I", raw, SECTIONS + 40 + 36, 0xe0000040)
        with self.assertRaises(ValueError): self.analyze(raw)

    def test_pe_header_section_overlaps_image_overflow_and_virtual_tails_fail(self):
        mutations = [(0x84, "<H", 0x8664), (OPT, "<H", 0x20b), (OPT + 28, "<I", 0xfffff000),
                     (SECTIONS + 40 + 12, "<I", 0x1100), (SECTIONS + 40 + 20, "<I", TEXT),
                     (SECTIONS + 16, "<I", 0x1000), (OPT + 92, "<I", 17)]
        for offset, fmt, value in mutations:
            raw = bytearray(self.raw); struct.pack_into(fmt, raw, offset, value)
            with self.subTest(offset=offset), self.assertRaises(ValueError): trace.Pe32(raw)
        raw = bytearray(self.raw); struct.pack_into("<I", raw, SECTIONS + 40 + 8, 0x300)
        pe = trace.Pe32(raw)
        with self.assertRaises(ValueError): pe.rva_mapping(0x2200, 4)
        for offset, length in ((-1, 1), (TEXT, 0), (TEXT + 0x1ff, 2), (0, 2)):
            with self.subTest(offset=offset), self.assertRaises(ValueError): pe.file_mapping(offset, length)

    def test_relocation_type_duplicate_truncation_or_unmapped_location_fail(self):
        mutations = [(RELOCS + 8, "<H", 0x5001), (RELOCS + 10, "<H", 0x3001),
                     (RELOCS + 4, "<I", 9), (RELOCS, "<I", 0x1001),
                     (RELOCS, "<I", 0x9000)]
        for offset, fmt, value in mutations:
            raw = bytearray(self.raw); struct.pack_into(fmt, raw, offset, value)
            with self.subTest(offset=offset, value=value), self.assertRaises(ValueError): trace.Pe32(raw).highlow_relocations()
        raw = bytearray(self.raw); struct.pack_into("<I", raw, OPT + 96 + 5 * 8 + 4, 7)
        with self.assertRaises(ValueError): trace.Pe32(raw).highlow_relocations()

    def test_repeat_analysis_is_deterministic_and_input_bytes_unchanged(self):
        before = bytes(self.raw)
        first = self.analyze(); second = self.analyze()
        self.assertEqual(first, second)
        self.assertEqual(bytes(self.raw), before)
        self.assertEqual(first["compiler_sha256"], hashlib.sha256(before).hexdigest())


class TraceArtifactControls(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        raw, text = fixture()
        self.data = bytes(raw)
        self.listing_bytes = text.encode()
        self.compiler = self.root / "invented-compiler.exe"
        self.compiler.write_bytes(self.data)
        self.listing = self.root / "invented.objdump.txt"
        self.listing.write_bytes(self.listing_bytes)
        self.tool = self.root / "invented-objdump"
        self.tool.write_bytes(b"Invented decoder identity; never executed")
        self.markers = self.root / "markers.json"
        self.markers.write_text(json.dumps({"compiler": self.pin(self.data), "markers": [MARKER]}))
        self.provenance = {"tool": {"linux_path": str(self.tool), **self.pin(self.tool.read_bytes())},
            "command": [str(self.tool), "-d", "-w", "-Mintel", str(self.compiler)], "returncode": 0,
            "stderr": "", "stdout_sha256": self.pin(self.listing_bytes)["sha256"],
            "compiler_sha256": self.pin(self.data)["sha256"]}
        self.provenance_path = self.root / "provenance.json"
        self.provenance_path.write_text(json.dumps(self.provenance))
        self.report = self.root / "report.json"

    @staticmethod
    def pin(data):
        return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}

    def run_cli(self):
        argv = ["inspect_compiler_trace.py", "--compiler", str(self.compiler), "--markers", str(self.markers),
            "--listing", str(self.listing), "--decoder-provenance", str(self.provenance_path), "--report", str(self.report)]
        with mock.patch("sys.argv", argv), mock.patch("builtins.print"):
            trace.main()

    def test_repeat_cli_is_deterministic_without_executing_the_pinned_decoder(self):
        self.run_cli()
        first = self.report.read_bytes()
        self.run_cli()
        self.assertEqual(self.report.read_bytes(), first)
        report = json.loads(first)
        self.assertEqual(report["candidate_operand_count"], 4)
        self.assertFalse(report["compiler_executed"])
        self.assertFalse(report["live_hooks_validated"])
        self.assertNotIn(str(self.root), first.decode())
        self.assertEqual(self.compiler.read_bytes(), self.data)

    def test_declared_decoder_command_listing_input_and_tool_drift_are_rejected(self):
        variants = []
        for field, value in (("returncode", 1), ("stderr", "warning"), ("stdout_sha256", "0" * 64),
                             ("compiler_sha256", "0" * 64)):
            p = copy.deepcopy(self.provenance); p[field] = value; variants.append(p)
        for index, value in ((1, "-D"), (3, "-Matt"), (4, str(self.root / "other.exe"))):
            p = copy.deepcopy(self.provenance); p["command"][index] = value; variants.append(p)
        for p in variants:
            with self.subTest(provenance=p), self.assertRaises(ValueError):
                trace.validate_listing_provenance(p, self.listing_bytes, self.data, self.compiler)
        self.tool.write_bytes(self.tool.read_bytes() + b"changed")
        with self.assertRaises(ValueError): self.run_cli()
        self.assertFalse(self.report.exists())

    def test_report_alias_conflict_and_changed_pe_pin_preserve_input_artifacts(self):
        for path in (self.compiler, self.listing, self.markers, self.provenance_path):
            with self.subTest(path=path):
                before = path.read_bytes(); self.report = path
                with self.assertRaises(ValueError): self.run_cli()
                self.assertEqual(path.read_bytes(), before)
        self.report = self.root / "report.json"
        self.report.write_bytes(b"retained evidence")
        with self.assertRaises(ValueError): self.run_cli()
        self.assertEqual(self.report.read_bytes(), b"retained evidence")
        self.report.unlink()
        self.compiler.write_bytes(self.data + b"changed")
        with self.assertRaises(ValueError): self.run_cli()
        self.assertFalse(self.report.exists())


if __name__ == "__main__":
    unittest.main()
