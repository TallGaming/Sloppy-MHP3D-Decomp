"""Synthetic checks for duplicate section names and malformed ELF boundaries."""

from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from elf32 import Elf32


def make_object():
    """Build two functions in separate sections that are both named .text."""
    data = bytearray(512)
    names = b"\0.shstrtab\0.text\0.strtab\0.symtab\0"
    data[52:52 + len(names)] = names
    symbols = b"\0first\0second\0"
    data[96:96 + len(symbols)] = symbols
    data[112:116] = b"ABCD"
    data[116:120] = b"WXYZ"
    struct.pack_into("<IIIBBH", data, 144, 1, 0, 4, 0x12, 0, 2)
    struct.pack_into("<IIIBBH", data, 160, 7, 0, 4, 0x12, 0, 3)
    ident = b"\x7fELF\x01\x01\x01" + bytes(9)
    struct.pack_into("<16sHHIIIIIHHHHHH", data, 0, ident, 1, 8, 1,
                     0, 0, 256, 0, 52, 0, 0, 40, 6, 1)
    sections = [
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (1, 3, 0, 0, 52, len(names), 0, 0, 1, 0),
        (11, 1, 6, 0x1000, 112, 4, 0, 0, 4, 0),
        (11, 1, 6, 0x2000, 116, 4, 0, 0, 4, 0),
        (17, 3, 0, 0, 96, len(symbols), 0, 0, 1, 0),
        (25, 2, 0, 0, 128, 48, 4, 1, 4, 16),
    ]
    for index, section in enumerate(sections):
        struct.pack_into("<10I", data, 256 + index * 40, *section)
    return data


class Elf32Tests(unittest.TestCase):
    def test_function_bytes_use_section_index(self):
        functions = list(Elf32(make_object()).functions())
        self.assertEqual([(fn["name"], fn["bytes"]) for fn in functions],
                         [("first", b"ABCD"), ("second", b"WXYZ")])

    def test_virtual_addresses_select_distinct_sections(self):
        elf = Elf32(make_object())
        self.assertEqual(elf.virtual_bytes(0x2000, 4), b"WXYZ")
        with self.assertRaisesRegex(ValueError, "unmapped"):
            elf.virtual_bytes(0x2002, 4)

    def test_section_table_outside_file(self):
        data = make_object()
        struct.pack_into("<I", data, 32, 500)
        with self.assertRaisesRegex(ValueError, "bounds"):
            Elf32(data)

    def test_function_outside_its_section(self):
        data = make_object()
        struct.pack_into("<I", data, 144 + 8, 8)
        with self.assertRaisesRegex(ValueError, "exceeds its section"):
            list(Elf32(data).functions())

    def test_unterminated_section_name(self):
        data = make_object()
        data[52 + 32] = ord("x")
        # Move the section-name offset to the last byte of the string table.
        struct.pack_into("<I", data, 256 + 2 * 40, 32)
        with self.assertRaisesRegex(ValueError, "terminated"):
            Elf32(data)


if __name__ == "__main__":
    unittest.main()
