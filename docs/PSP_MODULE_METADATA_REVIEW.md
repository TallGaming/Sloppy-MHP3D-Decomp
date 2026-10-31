> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# PSP module metadata review â€” Bucket 3AE

This is a separate, metadata-only interpretation of retained prepared files. It
preserves the generic ELF reader and the historical 3AD uninterpreted results.
It does not relocate, load, execute, authenticate or assign ownership to a module.

## Primary format evidence, before interpretation

The [ELF gABI program-header definition](https://gabi.xinuos.com/elf/07-pheader.html)
places the `p_filesz <= p_memsz` requirement in the **PT_LOAD** definition. Other
program headers may describe supplementary metadata; their memory size is not a
universal upper bound on their file extent. This does not waive file bounds.
A processor-specific relocation segment with file bytes and zero memory size
therefore must not be rejected merely by applying a load-segment rule to it.

The pinned [PPSSPP types](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/ELF/PSPElfTypes.h#L189-L202)
define `PT_PSPREL1=0x700000A0` and `PT_PSPREL2=0x700000A1`.
Its [loader](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/ELF/ElfReader.cpp#L699-L727)
checks filesz against memsz inside the PT_LOAD branch. The
[sectionless relocation dispatch](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/ELF/ElfReader.cpp#L838-L855)
handles the two PSP types separately. This supports naming their metadata type;
it does not authorize applying or validating relocation contents in this bucket.
Unknown types must remain explicit, with bounded file extents.

The [PSPSDK module-info declaration](https://github.com/pspdev/pspsdk/blob/460920c0c650ffcdf912863bc170430d08142c37/src/user/pspmoduleinfo.h#L16-L31)
has this layout with PSP 32-bit pointers:

| Offset | Stored field | Width |
| --- | --- | --- |
| 0 | modattribute | unsigned 16-bit |
| 2 | modversion | two bytes |
| 4 | modname | 27 bytes |
| 31 | terminal | one separate byte |
| 32 | gp_value | raw 32-bit value |
| 36 / 40 | ent_top / ent_end | raw 32-bit values |
| 44 / 48 | stub_top / stub_end | raw 32-bit values |

The full structure is **52 bytes**. The name and terminal must not be silently
combined or trimmed into the encrypted ~PSP header's different name layout.
The [declaration macro](https://github.com/pspdev/pspsdk/blob/460920c0c650ffcdf912863bc170430d08142c37/src/user/pspmoduleinfo.h#L48-L69)
places it in `.rodata.sceModuleInfo`, aligned 16, and orders version bytes minor,
major. The header itself states that some definitions were extrapolated from
Japanese Puzzle Bobble debugging information. This is a primary community
implementation definition, not a Sony provenance certificate for these files.

The pinned [PPSSPP lookup](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/ELF/ElfReader.cpp#L575-L586)
first finds the named section, then, when none was found, uses the first program
header's **`p_paddr & 0x7FFFFFFF` as a file offset** and checks the full structure
against file size. This supports a narrowly declared fallback for these
sectionless PRX files. Preserve the raw field, mask, resulting offset and lookup
method. Require it within the first file-backed PT_LOAD extent as an additional
local safety bound; do not manufacture a named section or treat stored pointers
as already relocated addresses. The emulator fallback itself is broader than
this proposed local rule and does not prove universal PSP-format validity.

The exact four cached texts and hashes are recorded in
`evidence/bucket-03ae/helper-map-format-sources.json`. Their SHA256 values are:

- gABI: `91787676e5dcbec67e3a9415cd43944aac9e7ed57515b81a36c3f8c1c0dce2e1`.
- PSPSDK header: `5deac4bc897124a187ff268570410faf8c81a72a8fca65b0aa2e651a14ca9d26`.
- PPSSPP types: `f7188e7f5a8a99424eb5b94e513c9df75f9f20d090befba101c9ba13f634e91c`.
- PPSSPP reader: `35f21f76022eae454b4486eb40c51a5d4c122165f69fbe7ce2fdde378ec9d952`.

## Bounded preflight and review scope

`raw-program-header-preflight.json` records four ET_PSP_PRX (`0xFFA0`),
sectionless candidates. Each has two PT_LOAD headers satisfying the load-size
constraint and a PT_PSPREL2 header whose memsz is zero. Its filesz is 1968 bytes
for entries 17/19 and 50 bytes for 18/20. These actual distinctions explain why
relaxing the old generic reader wholesale would be the wrong operation. The old
reader remains frozen and these earlier failure outcomes remain historical facts.

The proposed first-header file offsets 31184 (font-named inputs) and 608
(BASE64-named inputs) are supported by the lookup rule only after validating
52 bytes in their first load extents. Declared names remain unauthenticated and
ownership unclassified. No compiler attribution follows from the absence of
sections or comments; any comments actually present must be preserved verbatim.

## Independent pre-execution review

The separate reader directly validates ELF32/MIPS headers, up to 512 program
headers, every declared file extent and PT_LOAD alignment/memory extents. It
retains unknown nonload types, and identifies PSPREL2 bytes without parsing or
applying them. For sectioned inputs it independently bounds section/name tables
before asking the unchanged generic reader for optional section interpretation.
The main control must reproduce the full pinned EBOOT ELF and its existing
section-reader result. No input header or section is patched.

Review corrections made before final runs included the main's 356-header table
limit, preserving the 27-byte name/terminal split, raw fallback mask provenance,
immediate pins on bytes actually parsed, complete parent-link guards, and
late report publication checks. The profile binds both preparation-report cases
to their exact prepared-file paths and identities, rather than relying on a
matching filename. The five cases and two retained copies per case are fixed.
The exception diagnostic path also requires the same guarded publication rule.

Final pre-execution approval covered reader 13,372 bytes SHA256
`4c4c66aab76f5f1a58223c5f38b0cdcbdeeeb6cd889af8f8be0f7a3e807f7998` and
profile 6,398 bytes SHA256
`cfcabd67c778169e63568a8ab550fa08bff940dd4ddb191c51dbf4b6673ab7e1`.
The final exception path uses guarded exclusive diagnostic creation.
Neither this review nor a later bounded metadata status retroactively changes the 3AD generic-reader rejection or authenticates the prepared module.


## Frozen actual outcome: bounded failure

The frozen two reads both stopped on the **main control before PRX metadata
interpretation**, with `ValueError: PT_LOAD alignment/congruence is invalid`.
Each retained `metadata-trial-N-failure.json` is 114 bytes, SHA256
`87a72e70e4e074d9bfd3c703cca851100d7dd67562a3660bf4669a661942f664`.
There is no normal metadata report and no four-module success claim. The freeze
records both exact reviewed inputs and precedes these trials. Neither frozen
reader nor generic reader was amended to make this outcome disappear.

Independent bounded original-header readback confirms main PT_LOAD 0 has
file offset 0x2CB4, vaddr 0x08804000, filesz 0x217ED0, memsz 0x01679D80 and
p_align 0x10. Its offset remainder 4 differs from its address remainder 0. The
added generic ELF paging congruence requirement was therefore too strong for
this PSP metadata model; the pre-execution review failed to distinguish it
from the actual PSP byte-copy path. This is a model failure, not evidence that
the known main bytes changed or became invalid.

For a separately reviewed correction, the pinned
[loader allocation path](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/ELF/ElfReader.cpp#L641-L677)
uses p_align in first-load allocation and may warn for a requested relocated
address. A non-power-of-two value falls back to ordinary allocation. The
[copy path](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/ELF/ElfReader.cpp#L704-L735)
checks byte bounds and load sizes, then copies p_offset-derived bytes to the
vaddr-derived destination; it does not require their file/address remainders
to agree. For metadata-only reading, retain congruence and alignment shape as
observations, preserve file/load bounds, and make no paging or loader-validity
guarantee. That prospective correction is outside the frozen 3AE outcome.

The four 3AD expanded files remain retained and uninterpreted under their
historical reader result. No compiler, module or game execution, relocation,
SDK ownership exclusion, full-code inventory claim or match credit occurred.
