> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Synthetic link-stage provenance

Bucket 3E, 2026-10-30. This experiment asks what the available SNC linker does
to three invented compiler objects. It does not identify the game's linker or
turn its compiler-looking banner into per-function attribution. No game binary,
target probe, overlay or native-port code is linked here.

## Linker and help evidence

The existing `toolchains/pspsnc_1.2.7503.0/pspld.exe` identifies itself as
version 2.7.63.0. It is a 339968-byte PE32 executable, SHA-256
`46e6068518d96fd8b3d7ffe3e7ab0f1aa1c7e85f580a9f32de0aa65ac7daf534`.
Native Windows `--help` prints its full CLI with return code one; the saved
transcript is `evidence/bucket-03e/native-linker-long-help.json`. Help's exit
code is not permission to accept a failing link.

The source reviewer also obtained the help text through wibo with a terminal.
Other wibo invocations produced empty output or an exception during cleanup;
neither establishes a licensing problem or a usable linking environment.
The reviewed profile therefore uses the same unmodified linker through native
Windows interop. No alternate linker or binary patch is introduced.

Direct PE imports are `VERSION.dll`, `KERNEL32.dll` and `SHELL32.dll`.
The bundled `demangle.dll` is pinned; its hash is
`604a24a0c72e9307fe68fd3b106a168dfb9914758f90c4070b1a6796a4b8de1c`.
The profile records relevant SysWOW64 DLLs, KERNELBASE/NTDLL and the Windows
build. This is an explicit dependency scope, not a complete Windows snapshot.
Strings naming optional DLLs do not demonstrate that they were loaded, and a
missing optional demangler is not evidence of a license failure.

## Independent review before linking

The reviewed draft is `config/synthetic-link.json`, draft SHA-256
`1c8fa7ec74b6e19a7fa5dba0d2bc228ebfb6b1e6bc8f3c6d574452dfab349a85`.
Both independent reviewers approved it before linking. The primary changed only
its status to freeze it, producing SHA-256
`dc0017e2a922011fa51c59ab477baab74d805481d6ec56e53ff156b0da31094f`;
`evidence/bucket-03e/profile-freeze.json` records that sequence. It selects
only `bench/compiler_family_smoke.c`, SHA-256
`4fae81ae773148d74eb76914f823cd3f4946ff498e76eabb5c2b21db39d63702`:
one unsigned argument, one addition, one return, no headers or external calls.
Each of the three existing family profiles supplies a fresh O0 object without
source, macro or compiler-flag changes.

The same documented linker options apply to all three inputs:

```text
pspld.exe -comment -e family_smoke -Wall -Werror -t -T LAYOUT -Map MAP -o ELF OBJECT
```

Actual help defines `-comment` as retaining comment sections, `-e` as selecting
the entry symbol, `-T` as selecting the script, `-Map`/`-t` as map/file tracing,
and `-Wall`/`-Werror` as warning controls. There are no SDK/runtime libraries,
library-search paths, strip options, warning suppression or family-specific
linker switches. Native links must return zero; unsupported inputs remain
explicit failures rather than triggering a replacement profile.

The single shared layout is `bench/synthetic_link.ld`, SHA-256
`d4a7a44addfd7f70d88b09fe9d6058e21058d700b1bafcebd10cd373eba1ab55`.
It selects `family_smoke` and places `.text`/`.text.*` at `0x08804000`, followed
by data/BSS and register/ABI metadata. It explicitly accounts for `.comment`,
`.pdr`, `.mdebug.eabi32`, `.gnu.attributes` and Metrowerks `.mwcats` metadata.
Nonallocated metadata has address zero. No discard clause strips unsupported
input metadata to force acceptance. This is a bare synthetic layout, not an
original game layout or an executable prepared for runtime use.

Pre-link inventory in `prelink-object-inventory.json` supports this common
layout and exposes format differences. GCC's function symbol is 44 bytes in a
48-byte `.text` section; that four-byte section tail is separate from the
complete function extent. SNC and Metrowerks function extents are 24 and 28
bytes. The corresponding `.pdr` and `.mwcats` relocations concern metadata,
not outgoing calls from this invented function. Input headers and metadata
remain unchanged before linking.

The source reviewer approved this exact command/layout before link outputs were
observed. The primary owns the freeze, orchestration and result publication;
the independent validator owns format/failure controls. This review executed
help only and performed no compilation or linking.

## Results: all three links failed

The final fresh reports are `evidence/bucket-03e/final-link-run-1.json` and
`final-link-run-2.json`. They are byte-identical, 13377 bytes, SHA-256
`fbe206a40ae6f4efcaf9e91c54faa7281c7648bc84d4931289e76945d4338af7`.
Artifacts are retained under `build/synthetic-link-4cs9z75u` and
`build/synthetic-link-sepjo2c6`. The source reviewer independently checked all
six object/function hashes, all six link logs and the four partial maps against
the report. Source, compiler profiles, linker configuration and layout stayed
unchanged after the first failure; no binary header was normalized or stripped.

| Input producer | Compilation | Native linker result in both runs | Linked ELF |
| --- | --- | --- | --- |
| GCC | Return code zero; valid 44-byte function | 255; internal linker exception | None |
| SNC | Return code zero; valid 24-byte function | 255; internal linker exception | None |
| Metrowerks 219 | Return code zero; valid 28-byte function | 1; alignment-zero internal error, linking aborted | None |

The input-stage metadata remains observable:

| Input object | Raw ELF flags | `.comment` |
| --- | --- | --- |
| GCC | `0x10843000` | `GCC: (GNU) 3.3.3+allegrex-2.2.2-psp-1.7.1` |
| SNC | `0x10A23001` | Absent |
| Metrowerks | `0x10970001` | `MW MIPS C Compiler (3.0.0)` |

GCC and SNC produced partial maps placing the function at `0x08804000`; GCC's
map distinguishes its 44-byte function from its 48-byte text section. These
are intermediate placement records, not verified ELF entry points or executable
load mappings. Metrowerks failed before producing a map. Each `-t` log names
only its own object, twice; the partial maps contain that object and internal
linker bookkeeping. No SDK, startup or archive-library object was observed in
these traces. This is a bounded trace observation, not an exhaustive file-access
audit or proof that a successful library-free executable was built.

The Metrowerks error names no offending section. Its input has ordinary metadata
sections with `sh_addralign = 0`; the
[generic ELF section-header definition](https://gabi.xinuos.com/elf/03-sheader.html#section-header-table-entry)
allows both zero and one to mean no alignment constraint. That provides context,
not an isolated cause for this linker's failure. A section's alignment field is
also distinct from a nonallocated metadata section's zero address in the script.
The two generic internal exceptions expose no demonstrated root cause. These
outcomes do not establish that the linker fundamentally rejects SNC, GCC,
Metrowerks or every possible bare layout.

There is no output ELF whose flags, comments, code or entry/load mapping can be
compared. Function-byte preservation after linking is therefore **unmeasured**;
the report's zero preserved-function count does not mean that three functions
were observed to change. The experiment cannot say whether this linker copies,
changes or introduces a compiler banner, including the game's `2.4.1.01` string.
It establishes only reproducible failures of this exact declared pipeline.

No further layout, compiler option, linker or metadata-edit experiment follows
inside this bucket. A later reviewed investigation would be needed to isolate
the failures. The original game's linker/compiler attribution remains open,
the toolchain remains unlocked, and matched-game-function credit remains zero.
