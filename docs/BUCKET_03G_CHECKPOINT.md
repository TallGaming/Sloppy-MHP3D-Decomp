> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3G checkpoint

2026-10-30. The approved read-only MHP2G/MHP3 comparison is complete.
**There is a concrete compiler-input fingerprint agreement and useful engine
structure evidence, but no original-language proof or complete toolchain lock.**
The bucket ends with one experiment proposal; it has not been executed.

## Evidence and limits

The public reference is `tclamb/mhp2g-decomp` commit
`5b98acfd014090b07c81e6b17f376a5eba986083`, targeting ULJM05500. Our target remains
the clean PSP ULJM05800 v1.02 image. The external project describes a reconstructed
pipeline; its configuration is not recovered Capcom build documentation.

| Finding | Confirmed evidence | What remains unknown |
| --- | --- | --- |
| Compiler input | Our unmodified MW219 EXE has SHA-1 `3dc756594b1a46d27203c27a3c38e7c868eb3419`, matching the external script's pre-patch guard. | The compiler/settings of each MHP3 unit; the complete historical chain |
| Build stages | MHP2G declares C++ compilation, conditional assembly integration, a VFPU adapter, distinct assembly conversions, MW linking and finalization. | Complete available/pinned linker and finalizer binaries and their effects on MHP3 metadata |
| Overlay container | Both describe 64-byte MWo3 headers, stored text/data and nonstored BSS. | MHP3-wide loader/lifetime rules; identical code or class layouts |
| Pilot differences | Our movie overlay data begins at file offset `0x4C8`; the external configuration uses `0x480`. Load addresses also differ. | Cross-game function correspondence, despite equal total payload size and BSS |
| Header words `0x18`/`0x1C` | Both MHP3 words equal stored-byte end. MHP2G emits initializer-range boundaries at those positions. | An empty initializer range is consistent with our bytes, but not proven; legacy parser labels remain provisional. |
| Archive algorithms | Existing MHP3 decoding evidence has concrete seed/update/substitution/XOR counterparts in public MHP2G source. | Byte identity, source-unit context, original class receiver and compiler attribution |
| Archive differences | MHP3 has 5955 entries and 1289 exact-size pairs; MHP2G declares 6602 and 812. | The MHP3 directory tail remains uninterpreted; no foreign index or class layout is imported. |
| Language/ABI | MHP2G source declares virtual classes; our existing evidence supports investigating C++ engine structures. | Our isolated C-compatible probes and analysis signatures do not recover MHP3 classes or distinguish its original language. |

The ordinary MHP2G compiled-object path is distinct from its retained-assembly
and `INCLUDE_ASM` paths. Its object conversions must not be treated as a universal
recipe for compiler output. It also patches tools and uses failure-tolerant link
options. None was adopted here, and none is a verified SNC crash fix. Comparing
linked MHP3 metadata with relocatable compiler metadata still has an unresolved
stage difference. No additional linker attempts were made.

The existing networking leaves have no bounded equivalent bodies in the public
headers inspected. They remain unclassified hypotheses; no foreign method names,
SDK ownership or source correspondence was assigned.

## Review artifacts and verification

| Artifact | Purpose |
| --- | --- |
| [MHP2G_PIPELINE_COMPARISON.md](MHP2G_PIPELINE_COMPARISON.md) | Independent stage/provenance review, availability gaps and proposed experiment |
| [MHP3_STRUCTURAL_COMPARISON.md](MHP3_STRUCTURAL_COMPARISON.md) | Independent header/archive/language/ABI comparison and manifest audit |
| `evidence/bucket-03g/public-source-manifest.json` | Exact URLs, commits and hashes for 22 public text snapshots, including submodule references |
| `evidence/bucket-03g/comparison-inputs.json` | 32 existing-input pins and bounded ELF/header/probe observations |

The comparison manifest is 11723 bytes, SHA-256
`40d06cf5dbd324202b24a4126ce1924a782fc773c6f3ae0ba0bef2e2d53dc514`.
The final public-source manifest SHA-256 is
`ad2dec350ec0accd30415478292b04a2b1440e60091b7b2ef7a68e83987a66c7`.
Independent audit verified all 32 input records and 22 cached public text records,
all fourteen target interval hashes, the recovered overlay/header, the existing
34-function export and the compiler guard agreement. Source text was read as
data; no external build, parser, patch or setup script was executed.

No new tests were needed for this documentation/read-only comparison. The last
performed full tooling run remains **209 passed, zero skips, in Bucket 3F**.
This bucket adds no new test-run, disassembly, function-analysis or runtime claim.

## One proposed next experiment — awaiting separate approval

Use the existing unmodified MW219 and unchanged original fourteen-probe source.
At fixed O2, compare the existing C command with one otherwise identical command
using C++ mode. This changes only the language-mode variable across the complete
bench; it adopts none of MHP2G's optimization/inlining flags, headers, wrappers
or patches. It is toolchain investigation, not a per-function flag adjustment
or a selected game-build configuration.

Before scoring, use an invented naming fixture to establish and independently
review exact C++ symbol-to-probe mapping. Freeze source/manifest/compiler/runner
pins, both commands, that mapping and complete-function checks. Require all
fourteen unique functions and supported relocations or leave the entire
configuration unscored. Run two fresh repeats of both cases; retain failures,
compare complete bytes and audit repeatability without editing source or pooling
favorable results. Do not execute this proposal inside Bucket 3G.

The experiment can establish whether language mode changes these isolated bodies.
Equal bytes would show that the probes do not discriminate this variable;
differences would show a controlled mode effect. Neither outcome establishes or
refutes the original language, class context, inlining or complete toolchain.

## Decisions preserved

Readable source first, fixed evidenced toolchain before matching, no per-function
flag changes, visible parking, and the SDK/third-party assembly policy remain
unchanged. No new compiler/linker was provisioned, no source or binary patched,
and no game code compiled, linked or executed. Matched/source-linked game
functions, parked functions and counted matching tricks remain zero. The full
game gate and its 18 negative checks remain unimplemented. Native-port work is
deferred. Stop for user review; the proposed experiment needs its own approval.
