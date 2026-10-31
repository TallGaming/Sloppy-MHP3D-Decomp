> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3I independent validation

2026-10-30. The validation helper reviewed the single source and profile before
candidate compilation, added invented tooling controls, and independently
audited both trials. **Both valid compilations emit the same 100-byte function
for the complete 68-byte target; the first differing byte is zero.** This is a
failed diagnostic source hypothesis, not a matched or parked game function.

## Pre-compilation review

The approved target is exactly `[0x0886233C, 0x08862380)`, including the return
and its delay slot. The helper read that interval in the existing disassembly
and checked the pinned ELF bytes. Its SHA-256 is
`7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57`.
The independently owned [ARCHIVE_KEY_PROBE_REVIEW.md](ARCHIVE_KEY_PROBE_REVIEW.md)
records calls, tail ingress, branch/return boundaries and type uncertainties.
This validation did not select another function or produce new disassembly.

The one natural C++ candidate describes only two 32-bit fields at observed
receiver offsets `0x2F53C` and `0x2F540`. Unknown prefix bytes and a nonvirtual
partial type preserve those offsets without claiming the original class,
inheritance, earlier fields or complete object size. Scalar-width and partial-
extent checks generate no additional function. The purpose/field comments
explain seed splitting, independent defaults and the observed memory accesses.

The `volatile` qualifiers are a pre-output hypothesis, motivated by the actual
upper-state reload and related public MHP2G declarations. They are not recovered
original qualifiers or synchronization proof. Upper-then-lower writes, the
local low-half test and high-field reload were declared before compilation;
there was no result-driven source permutation. Only one candidate was tried.
No source change was requested during this review or made after results.

| Frozen artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `bench/archive_key_initializer.cpp` | 1806 | `6c4be341bcc3f113b56ccf7494a7b624a550b52f89c9c827eacbbce56e1f71d3` |
| `config/archive-key-probe.json` | 883 | `bcb2a3b159f2ce1f3d6fba2ff9f2d668dade818efab8d79bb4fe6656846bea84` |
| `bench/archive_key_naming.cpp` | 364 | `ba25728588ef85085ccf3c51647f741c17bddbe147e6823e5a654546f7c937c2` |
| Invented naming object | 672 | `d06c4baa5b3c3b49a0c8ed3013df07aea97ac6d093a541d8ab57b62d3ea41ab4` |
| `evidence/bucket-03i/naming-evidence.json` | 701 | `7be69cc48816970a39de0c9880b1f7a94f5ef4dae1d74ee02babec720affd9d3` |

The naming source uses the same class, method and unsigned argument category
with unrelated fields/body. The helper independently found exactly one complete
16-byte executable function, `initialize_key__17ArchiveKeyContextFUi`, in its
ET_REL object. Its identity and empty diagnostics agree with the naming report.
No target-byte similarity was used to select the alias.

The reviewed experiment draft was 1901 bytes, SHA-256
`27f5ea2d60a5c8760eb8f35b683d6bfe5ef448e9f66b90f1dc482d6757e142f1`.
The frozen `config/archive-key-experiment.json` is 1902 bytes, SHA-256
`30b5372dab0d1e2fb9dc0ec4436ca0e78af1922728c5a421499a66e2a4cc5188`.
Reversing only its status-value change reproduces the reviewed draft hash.
The command remains the existing unmodified MW219 pipeline with
`-nostdinc -lang c++ -c -O2`. No flag was added, searched or adopted for a game
build. Earlier fourteen-probe sources/settings remain unchanged.

## Tooling controls

`tests/test_archive_key_probe.py` adds 13 tests using invented bytes. The runner
fixtures retain a valid invented fourteen-probe input graph so the real nested
Bucket 3H validation still runs; the new compiler call is mocked. No original
game bytes or real compiler invocation appear in these tests.

The controls require one exact member symbol and the entire function extent;
reject extra targets/functions and unsupported code relocations; and keep
short/long prefixes or changed words non-exact. They reject changed flags,
addresses, sizes, attempt counts, naming/hypothesis bindings and even a rehashed
naming object whose actual symbol is wrong. Compile failures, warnings,
timeouts, missing/invalid objects and malformed aliases remain unscored with
empty comparisons. Fresh repeat objects, unchanged emitted bytes, pre/post
input pins, protected report aliases and conflicting evidence are checked.

The helper independently ran the new controls and complete suite:
**239 passed, zero skips**. The primary owns the retained full log under
`evidence/bucket-03i/`. These tooling tests are not the future full-game gate's
required 18 negative checks. Their invented exact-result control still records
zero game-match progress.

The helper read the primary's real controls in
`evidence/bucket-03i/verification-summary.json`. Report/input aliasing and a
wrong member symbol each return exit one before a new build directory or
successful report; the alias control preserves the input. These controls were
performed by the primary and were not rerun during this final readback.

## Independent final artifact audit

The two reports `evidence/bucket-03i/archive-key-run-{1,2}.json` are
byte-identical: 1154 bytes, SHA-256
`e937d49b28b94694f7fa8b1c67db88a8c229ec1394f903a03cb6cc4815509e59`.
Their fresh directories are:

- `build/archive-key-probe-h53umlmt`
- `build/archive-key-probe-btnq7jgt`

Each contains exactly one 768-byte object and an empty compile diagnostic log.
Both objects have SHA-256
`1d715acabd4cdec572d40c1905504881a396fa5e11296f1163533b30941d7796`.
The helper independently parsed the exact single member symbol and recomputed
its complete length, hash, equality and first differing byte against the pinned
target. The emitted function is 100 bytes, SHA-256
`193c361fab07498ef61aa22bfa4c417f10bfbfcd0cdb8bd50a591f7838aad2da`.
Both reports accurately record `COMPLETE`, zero exact probes and first difference
zero. `COMPLETE` means valid complete comparison, not byte equality.

The objects retain flags `0x10970001`; the accepted reference's distinct flags
remain untouched. No linked-stage metadata conclusion follows from object
metadata. No relocation word, delay slot, padding or symbol name was patched,
masked or trimmed. The inherited comparator/alias adapter remains unchanged.

The helper recomputed **201 declared local pin records and 11 native dependency
records**, including the source, manifest, interpretation/naming evidence,
original reference ELF and inherited tools/configuration. All match current
bytes. Duplicate declarations are counted as records, not distinct files.
The original ISO was not opened or modified for this audit.

## Final implementation identities and limits

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `scripts/bench_archive_key.py` | 9633 | `30c4b8d9fa18e7eac32b18e3defb86e103cb58996fe9cfb10f33d19b3a7f8535` |
| `tests/test_archive_key_probe.py` | 18541 | `c4999ba24025fb3001208185d8f5c257228020c59e475465e37e06530f34b4cf` |

The failure does not disprove the observed seed/default behavior or uniquely
identify the missing source/toolchain context. It does not authorize another
candidate, qualifier change, flag search or trick. Original class/prototype,
qualifiers, translation unit, game/library ownership and historical tools remain
unresolved. No game source was integrated or linked, and no game was executed.
This diagnostic draft remains visible in the bench and counts as one source
hypothesis; it is not silently promoted to source coverage or labeled as a
parked reconstruction. Match credit, source-linked game functions, parked
functions and matching-trick counts remain zero. Stop at the Bucket 3I checkpoint.
