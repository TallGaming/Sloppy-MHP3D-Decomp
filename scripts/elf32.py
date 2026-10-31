"""Small, bounded ELF32 little-endian MIPS reader for local matching tools.

Section indices are preserved: Metrowerks objects can have several different
sections all named .text, so selecting code by name alone is incorrect.
"""

import struct


class Elf32:
    """Read sections and symbol extents without executing the supplied binary."""

    def __init__(self, data):
        if len(data) < 52 or data[:7] != b"\x7fELF\x01\x01\x01":
            raise ValueError("Expected ELF32 little-endian version 1")
        self.data = data
        header = struct.unpack_from("<16sHHIIIIIHHHHHH", data)
        self.file_type, machine = header[1:3]
        if machine != 8 or header[8] != 52:
            raise ValueError("Expected a standard ELF32 MIPS header")
        self.entry = header[4]
        self.flags = header[7]
        self.program_headers = []
        phoff, phsize, phcount = header[5], header[9], header[10]
        if phcount:
            if phsize != 32:
                raise ValueError("Unsupported ELF program-header size")
            self.region(phoff, phsize * phcount)
            for index in range(phcount):
                values = struct.unpack_from("<8I", data, phoff + index * phsize)
                if values[4] > values[5]:
                    raise ValueError("ELF segment file size exceeds memory size")
                self.region(values[1], values[4])
                self.program_headers.append(values)
        shoff, shsize, shcount, shstrings = header[6], *header[11:14]
        if shsize != 40 or not shcount or not 0 < shstrings < shcount:
            raise ValueError("Unsupported ELF section-header layout")
        self.region(shoff, shsize * shcount)
        self.sections = []
        for index in range(shcount):
            values = struct.unpack_from("<10I", data, shoff + index * shsize)
            section = dict(zip(
                ("name_offset", "type", "flags", "address", "offset", "size",
                 "link", "info", "alignment", "entry_size"), values
            ))
            section["index"] = index
            if section["type"] != 8:  # NOBITS memory has no bytes in the file.
                self.region(section["offset"], section["size"])
            self.sections.append(section)
        names = self.sections[shstrings]
        if names["type"] != 3:
            raise ValueError("ELF section names do not use a string table")
        table = self.section_data(names)
        for section in self.sections:
            section["name"] = self.string(table, section["name_offset"])

    def region(self, offset, size):
        """Return an exact bounded range; silently truncated slices are errors."""
        if offset < 0 or size < 0 or offset + size > len(self.data):
            raise ValueError("ELF region exceeds file bounds")
        return self.data[offset:offset + size]

    @staticmethod
    def string(table, offset):
        """Read one terminated string inside its declared table."""
        if not 0 <= offset < len(table):
            raise ValueError("ELF string offset exceeds its table")
        end = table.find(b"\0", offset)
        if end < 0:
            raise ValueError("ELF string is not terminated")
        return table[offset:end].decode("utf-8")

    def section_data(self, section):
        """Read file-backed bytes; NOBITS must not be mistaken for stored data."""
        if section["type"] == 8:
            raise ValueError("NOBITS has no file-backed data")
        return self.region(section["offset"], section["size"])

    def functions(self):
        """Yield defined function symbols using their actual section indices."""
        for table in self.sections:
            if table["type"] != 2:
                continue
            if (table["entry_size"] != 16 or table["size"] % 16
                    or not 0 < table["link"] < len(self.sections)):
                raise ValueError("Invalid ELF symbol-table layout")
            strings = self.sections[table["link"]]
            if strings["type"] != 3:
                raise ValueError("ELF symbol names do not use a string table")
            names = self.section_data(strings)
            for record in struct.iter_unpack("<IIIBBH", self.section_data(table)):
                name, value, size, info, other, section_index = record
                if info & 15 != 2 or section_index == 0:
                    continue
                if not 0 < section_index < len(self.sections):
                    raise ValueError("ELF function section index is invalid")
                section = self.sections[section_index]
                offset = value if self.file_type == 1 else value - section["address"]
                if offset < 0 or offset + size > section["size"]:
                    raise ValueError("ELF function exceeds its section")
                yield {"name": self.string(names, name), "size": size,
                       "section_index": section_index, "section_offset": offset,
                       "bytes": self.section_data(section)[offset:offset + size]}

    def virtual_bytes(self, address, size):
        """Read bytes from a unique allocated section at the linked address."""
        candidates = [s for s in self.sections if s["flags"] & 2 and s["type"] != 8
                      and s["address"] <= address
                      and address + size <= s["address"] + s["size"]]
        if len(candidates) != 1:
            raise ValueError("Virtual range is unmapped or ambiguous")
        section = candidates[0]
        offset = address - section["address"]
        return self.section_data(section)[offset:offset + size]
