> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AE independent validation

## Review contract

Preserve the frozen generic Elf32 reader and every3AD rejection. This separate
PSP metadata reader must not normalize, patch or reinterpret an input merely to
make the old reader accept it. Apply load-memory constraints to PT_LOAD only,
validate every real file extent, preserve non-load/unknown program records as
raw metadata and never turn them into memory mappings or applied relocations.
Sections, strings and named module-info fields require bounded exact extents;
NOBITS remains metadata with no stored bytes. Missing or unsupported structures
stay explicitly uninterpreted. Module names/comments are producer/runtime clues,
not automatic SDK ownership or exclusion.

After both reviews and the exact freeze, compare ten retained main/candidate
prepared-byte copies across both3AD sets and audit deterministic metadata
reports. No further decryption, compiler/module execution, source/profile change,
initializer revisit, library exclusion, match credit or native-port work occurs.

## Exact source/profile review and controls

The helper approves these exact inputs before the two actual metadata runs:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `config/psp-module-metadata.json` | 6,398 | `cfcabd67c778169e63568a8ab550fa08bff940dd4ddb191c51dbf4b6673ab7e1` |
| Separate fixed reader | 13,372 | `4c4c66aab76f5f1a58223c5f38b0cdcbdeeeb6cd889af8f8be0f7a3e807f7998` |

The original generic `scripts/elf32.py` remains exactly 5,614 bytes with SHA-256
`766f16f86736ed0a04eb6c1ed439bd8aa96d2aab0b0c99e49055934e2fd45833`.
No copy of an input header is patched. The source-backed sectionless PRX rule
uses only header0's p_paddr masked by0x7FFFFFFF as a file offset, then locally
requires all52 module-info bytes inside that first file-backed PT_LOAD. Missing
or invalid selection stays uninterpreted. The source review distinguishes the
27-byte name from its separate terminal byte, records the unmodified physical
field and mask, and reconstructs no exports/imports.

Before freeze this helper identifies that an optional generic-reader failure
could bypass independent bounds on file-backed sections. The primary adds
explicit raw section-table, every file-backed extent, section-name table and
all section-name string checks before that optional interpretation. The other
reviewer requests exact bytes pinned immediately upon read, full parent link
guards and a guarded exclusive diagnostic-failure write. These guards appear in
the approved source. Unsupported non-load semantics remain explicit data.

Invented pure controls pass ordinary ELF, sectionless PRX, unknown non-load with
file bytes/memsz0, high-bit p_paddr masking, out-of-first-load module info staying
uninterpreted and NOBITS without file bytes. Eighteen malformed header/program/
section cases reject: unsupported type/machine/version, malformed or excessive
program tables, load file/memory overflow, alignment/congruence errors, non-load
file bounds, inconsistent sectionless fields, section table/file extent/string
bounds and short/invalid identification. Invalid separate module-name terminal
and nonASCII name remain uninterpreted without creating ownership claims.

Six mock-only run scenarios pass: full positive, actual-read byte-pin mismatch,
late pin drift, main-control mismatch, existing report preservation and report
parent redirection. All negatives publish no new normal report. Actual prior
source/preparation/parking pins verify read-only. No helper launches a compiler,
decrypter, module or actual metadata-output run before freeze. These inline
controls do not add to the last352-test tooling suite or implement the matching
gate's eighteen negatives.

## Actual repeat audit

Both frozen actual runs fail at the known main ELF control before any candidate
metadata is appended. No normal metadata report is published, and no new parsed
PRX/module outcome follows. The helper independently reproduces the exact error:
`PT_LOAD alignment/congruence is invalid`.

The main ELF's first PT_LOAD has file offset11,444 (0x2CB4), virtual address
0x08804000, file size2,195,152, memory size23,567,744 and declared alignment16.
Its file offset remainder is4 while its virtual-address remainder is0. All
recorded bytes remain original. The invented controls had tested rejection of
this condition; they had not established that applying the conventional
congruence rule was appropriate to this particular PSP loader/container. The
first real mandatory control exposes that unsupported model assumption. Preserve
the failed source/profile/freeze rather than quietly changing this reader.
Any separately source-backed copy-loader metadata model needs its own reviewed
plan and freeze, with noncongruence recorded as an observation rather than
claimed paged-ELF validity.

Both 114-byte failure records are byte-identical with SHA-256
`87a72e70e4e074d9bfd3c703cca851100d7dd67562a3660bf4669a661942f664`.
They record `UNINTERPRETED_FAILURE` with the exact ValueError. The 741-byte
pre-execution freeze has SHA-256
`4c7b6e91422e32a25992d183fee5b061b242aa698ceb943ee68c3e1847140f2a`.
The helper verifies absence of both normal trial reports, the frozen reader and
profile identities, all ten original prepared-byte pins and preserved source/
compiler/parking identities. The old generic Elf32 reader remains unchanged,
and all3AD results remain as recorded.

This bucket ends as a failed metadata-reader applicability check, not a successful
module inventory. Neither trial reaches new PRX metadata output. No input
header is repaired, no helper/decryptor reruns, no original code executes, and no
ownership exclusion, compiler attribution, source attempt, matching credit or
port implementation is added. The last352-test WSL suite is unchanged; the
inline controls are separate from the unimplemented full-build/18-negative gate.
Stop this version and preserve the reviewable failed checkpoint.
