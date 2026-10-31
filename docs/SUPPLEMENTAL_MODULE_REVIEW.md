> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Supplemental module-container review — Bucket 3AC

This bucket preserves exactly eight selected payloads in two private sets and
records bounded container metadata. It performs no decryption, decompression,
compiler/game execution or ownership-based exclusion. Copying known containers
does not establish a complete denominator of game code modules.

## Header and wrapper source review

The existing helper is pinned to
[`John-K/pspdecrypt@c156627db7634d395c380c0a9589130f603307fc`](https://github.com/John-K/pspdecrypt/tree/c156627db7634d395c380c0a9589130f603307fc).
Its [`PrxDecrypter.h`](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/PrxDecrypter.h)
defines a packed0x150-byte little-endian PSP_Header. Independently reviewed
field locations include:

| Offset | Field / stored width |
| --- | --- |
| `0x00` | Signature, u32 |
| `0x04/0x06` | Module/compression attributes, u16 each |
| `0x08/0x09` | Module-version low/high bytes |
| `0x0A` | Declared module name,28 raw bytes |
| `0x26/0x27` | Version/segment-count bytes |
| `0x28/0x2C` | Declared ELF/PSP size, u32 each |
| `0x30/0x34` | Entry/module-info offset, u32 each |
| `0x38` | Declared BSS size, signed32 |
| `0x3C/0x44/0x54` | Four segment alignments/addresses/signed sizes |
| `0x78/0x7C` | Devkit version/decrypt mode, u32 each |
| `0xB0` | Declared compressed size, signed32 |
| `0xD0` | Tag, u32 |

Only a complete header beginning with exact`~PSP` magic supports this metadata
interpretation. These fields are declarations, not recovered plaintext, proven
executable entry points or authentication evidence. Signed fields must retain
their interpretation; names require bounded handling without assuming a NUL
terminator. No helper binary or decryption function is invoked.

For wrapper context, the pinned public PPSSPP source
[`c0fd904feefedc66441d4d5d602e46d2fd8e4fd6`, sceKernelModule.cpp:1630](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/HLE/sceKernelModule.cpp#L1630)
recognizes`~SCE`, reads a proposed wrapper length at+4 and conditionally advances
before inspecting the next signature. It does not prescribe a universal0x40
inner offset. This emulator implementation is an external format lead, not
proof of our four entries' layout, validity, SDK origin or original loader
behavior. The approved3AC parser keeps raw`~SCE` containers uninterpreted and
performs no guessed inner-offset parsing.

## Scope and required integrity

Recover exactly the main EBOOT control, BOOT, OPNSSMP and packaged updater EBOOT
from their freshly reproduced ISO paths/extents, plus raw archive entries17–20
using their exact stored lengths. Archive sector padding stays outside payloads,
and raw entries receive no game-archive deobfuscation. All other ISO entries,
including updater DATA.BIN, remain directory metadata only.

The main EBOOT must equal the complete original encrypted control. BOOT may be
labeled zero-filled only after checking every stored byte. Packaged updater
software stays distinct from game-owned matching progress, with no SDK/library
exclusion inferred solely from names, tags, wrappers or directory paths.

Both helpers must review/freeze the exact recovery script/profile before real
recovery, then audit both complete outputs and manifests. Original locks,
catalogue checksums, archive metadata, prefix/control identities and preserved
sources/toolchains/assembly must be checked before/after. Input or extent drift
must prevent success publication; existing conflicting outputs stay preserved.
Exact source review and retained outcomes follow separately when available.

## Exact pre-recovery source/model review

The reviewer approved `scripts/inventory_supplemental_modules.py`,13,670 bytes,
SHA-256 `f4029f998558603f420ac246809c46d52e53cafcbd5772a5dff0879b1bf33de9`,
and `config/supplemental-modules.json`,3,060 bytes, SHA-256
`96d8d9eb2f3904d8ce3f987aaaf92cf90f802c73fe845e482b553ca81ae1ed61`,
subject to completed validation controls and the final two-review freeze.
The parser reads only the declared subset of the reviewed PSP header, preserves
the28-byte raw name and signed fields, and records unauthenticated metadata.
All other signatures, including raw`~SCE`, remain uninterpreted.

The source reproduces the locked ISO directory and previously validated archive
prefix inventory, copies selected raw bytes at exact stored lengths, checks the
entire encrypted main-EBOOT control and counts every payload's nonzero bytes.
No decryption helper is launched and no raw SCE full payload is transformed.
The inherited inventory recheck retains its earlier prefix-sampling behavior;
it is distinct from decoding/recovering these four raw containers.

Before recovery, validation identified a stage-directory redirection gap. The
primary added a link/type guard for the stage directory, absolute output paths,
full stage/output-parent chain checks adjacent to rename and a report-parent
recheck. The reviewer read back those corrections. The atomic publication unit
is the fresh payload bundle plus its manifest; an optional external report is
written afterward. A report failure therefore does not imply that no bundle
was published. Existing conflicting outputs are preserved.

## Complete output and source audit

Both exact approvals preceded the freeze at
`2026-10-31T08:51:58.349266+00:00`. The final script/profile and validation-test
pins remain unchanged. The primary reports352 passing WSL tooling tests with
zero skips, including twelve new supplemental controls.

Both fresh sets under
`reference/uljm05800-v102/supplemental-sets/run-1` and`run-2` contain exactly
eight regular payload files plus their manifest. The reviewer independently
compared all sixteen copies, recomputed full hashes/nonzero counts, checked
both exact file sets/manifests and reread each of the eight exact source
extents directly from the locked ISO/archive. No archive padding enters the
stored payloads. Each set contains10,082,440 payload bytes; copies do not
multiply unique coverage.

Both manifests and external reports are identical8,656-byte JSON artifacts,
SHA-256 `b88187266d7cffa99f5f82ea6902dffde4c3dded119e7f3ef62dd256fafb995a`.
The fresh ISO directory contains fourteen file entries, of which only the four
predeclared ISO payloads were copied. Remaining files stay directory metadata.

| Selected payload | Exact stored bytes | Bounded observation |
| --- | ---: | --- |
| Main EBOOT control | 2,247,664 | Complete prior encrypted control identity reproduced; declared`~PSP` name`MonsterHunterPortable3rd`, tag`D91681F0` |
| BOOT | 2,247,320 | Every byte independently verified zero; full nonzero count0 |
| OPNSSMP | 3,264 | Declared`~PSP` name is one ASCII space, preserved literally; tag`457B8AF0` |
| Packaged updater EBOOT | 5,540,576 | Declared`~PSP` name`updater`, tag`02000000`; kept distinct from game progress |
| Raw archive17 | 20,688 | `~SCE` at offset0; uninterpreted |
| Raw archive18 | 1,120 | `~SCE` at offset0; uninterpreted |
| Raw archive19 | 20,688 | `~SCE` at offset0; uninterpreted |
| Raw archive20 | 1,120 | `~SCE` at offset0; uninterpreted |

The reviewer independently checked the raw name ranges, signed BSS/compressed
fields, tag locations and declared PSP sizes in the three complete`~PSP`
headers. All three declared PSP sizes equal their actual container lengths.
Their declared ELF/compressed sizes are not substituted for recovered code
extents. BOOT's zero-filled label comes from the entire file, not its prefix.
Its SHA-256 is`903a31545cbed615a8d520666805e7c8f6024eb85129f63d51ac0f32089319f1`.

There is one existing main-EBOOT control and seven supplemental payload blobs,
not eight newly identified executable modules. Raw SCE pair members have
different complete hashes despite paired sizes. No inner header, library name,
function range or ownership is inferred for them in3AC. The OPNSSMP whitespace
name and updater label likewise supply no independent library provenance.

No wrapper was unwrapped and no plaintext was decrypted/decompressed. Exact
container recovery, header declarations, library identification and source-
matching coverage remain separate. Complete game-code inventory is explicitly
unestablished; compiler lock, linked source and credited matches remain zero.
The parked initializer and its source-attempt/trick counters remain unchanged.
This helper performed static/public-source/artifact inspection and exact
read-only source comparisons, never compiler/decryptor/game execution.
