> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AF independent validation

## Separate model and exact review

Preserve both failed3AE trials, their frozen reader/profile and the original
Elf32 reader. The pinned PSP copy-loader loop bounds file offset/length and
copies PT_LOAD bytes to declared destinations; it does not prove conventional
paging congruence. This separately versioned reader records alignment shape and
file/address modulo agreement as observations. It never repairs headers, moves
bytes, maps memory, applies relocations or executes a module. No paging validity
or successful original-console loading is claimed.

The helper reads the pinned source's copy/bounds loop and independently diffs
this version against frozen3AE. Changes are limited to the explicitly declared
alignment observation/model, new profile/version/status bindings and preservation
pins. All file/table/string bounds, PT_LOAD file/memory and32-bit range checks,
module-info selection, exact actual-read identity and report-path guards remain.

The helper approves these exact inputs before both five-case metadata runs:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `config/psp-copy-loader-metadata.json` | 7,427 | `a32c4f32522b0da1bc2261e90252724f50b797eb1799624a790ef51021ca558e` |
| Separate fixed reader | 14,102 | `dabefc096a5f5bf5fe35a4a90d24451ec052a0fc4205d17f0a2b0e52922f4826` |

## Meaningful independent controls

Four invented positives exercise alignment0,1,3,16. Zero/one has no modulo
claim; non-power-of-two and noncongruent values remain explicitly recorded, and
all cases deny a paging-alignment guarantee. Ten malformed cases still reject:
load file size beyond memory,32-bit load-memory overflow, load/non-load file
bounds, malformed/excessive program tables, wrong machine/version and
inconsistent sectionless fields. The prior reader's section/string/NOBITS/
module-info bounds are unchanged by the exact diff.

Six mock-only run controls pass: positive with noncongruent main control;
actual-read hash mismatch; late input/model pin drift; main-control mismatch;
existing report preservation; and redirected report parent. Negatives publish
no new normal report. Actual nested input verification passes, including all
prepared bytes, primary-source/cache identities, generic reader, failed3AE
artifacts and parked source/profile pins. No helper launches any compiler,
decryptor, module or actual metadata-output run before freeze. These controls
are separate from the last352-test WSL suite and unimplemented matching gate.

## Actual repeat audit

Both frozen runs complete the same five-case suite. The helper independently
reads all ten complete prepared-input copies and reproduces all metadata from
their unchanged bytes. Every program record is checked directly against its raw
32-byte table entry, with each declared file extent and its full hash bounded;
PT_LOAD file/memory and32-bit destination-range constraints remain valid. All
736 program records across both trials are covered. This is metadata checking,
not a guest-memory load or relocated image reconstruction.

The known main ELF remains byte-exact, with356 program headers and734 sections.
Its first PT_LOAD offset0x2CB4/VA0x08804000/alignment16 noncongruence is explicitly
recorded with paging_alignment_guaranteed false. Both controls pass without
changing that input. Section733's exact comment strings remain
`MW MIPS C Compiler (2.4.1.01)` and `PSP`; these preserve linked metadata and do
not identify every original source unit's compiler.

Each of the four candidate PRX files has three program headers, typed
PT_LOAD/PT_LOAD/0x700000A1, and declares no section table. Both loads pass the
retained file/memory bounds. The relocation2 record has file bytes but memsz0;
its contents remain uninterpreted and unapplied. No section names or compiler
comments are invented for these sectionless files.

| Candidate | Complete input bytes / SHA-256 | Module-info file offset | Bounded declared name | Raw relocation2 bytes |
| --- | --- | ---: | --- | ---: |
| Archive17 | 35,232 / `9d6c771861b8dec4ed74284809e6853d5e738f794a7c5d3052ac288a23dc71cb` | 31,184 | sceFont_Library | 1,968 |
| Archive18 | 1,138 / `7e49891b16f453c09433249953f9a1330555525e6a51201f63e4b3a6abbd3807` | 608 | sceBASE64_Library | 50 |
| Archive19 | 35,232 / `3eb3b7f83442370533647b46365be49463256931196610175119959729b4e466` | 31,184 | sceFont_Library | 1,968 |
| Archive20 | 1,138 / `129e8e7a5231a81ba919d751c2ff0b1f03f95996a27d766732bf4f5bf61085bc` | 608 | sceBASE64_Library | 50 |

All eight52-byte module-info copies fit entirely inside the first file-backed
load, selected only by the pinned header0 p_paddr-mask rule. Direct raw decoding
agrees with names, separate zero terminal, attributes6 and version bytes[1,1].
The five raw GP/export/import fields are33136/30916/30952/30960/31020 for the font
pair and32752/404/436/444/444 for the base64 pair. They stay raw fields: no pointer
mapping, export/import enumeration, symbol attribution or relocations are
reconstructed. The same declared name does not make two differing complete
payloads identical or prove SDK ownership. All ownership remains UNCLASSIFIED;
metadata is not authenticated.

Both422,021-byte reports are byte-identical with SHA-256
`c9490f6a2d0cee5214c5935aa6ac6b23dd8385dac6e773c922b498657d3c0514`.
The766-byte pre-execution freeze has SHA-256
`3ea02e37ab6ac4765dfc9df51428eb03150ce64295aaa7a13782717039f54d85`.
Final nested input/freeze verification passes, including the original generic
reader, all prepared-byte/source/compiler/parking pins and both unchanged3AE
failure artifacts. The failed3AE applicability result remains failed under its
own frozen model. No3AD decryption or helper call is repeated. OPNSSMP still has
no prepared ELF after its prior failure.

This version establishes repeatable bounded metadata for the declared inputs,
not successful original-console loading, SDK exclusions, a historical compiler
lock, original source matches or a complete game-code inventory. No module is
executed, no source/flags/attempt counters change, the initializer remains
PARKED, and no native-port work begins. The last352-test WSL suite is unchanged;
these controls and metadata reports do not implement the full-build gate or its
eighteen required negatives. Stop at this bounded checkpoint for handoff by
the agreed09:52UTC deadline.
