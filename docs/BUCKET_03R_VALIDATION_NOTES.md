> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3R independent validation

## Reviewed scope and method

This inventories only the first at most 64 stored bytes of each archive entry,
using the existing pinned ISO/archive/directory/decode-table/ELF identities. Raw
prefixes are kept distinct from deobfuscated prefixes. Only complete words are
decoded: a short exact length is never rounded into sector padding and an empty
extent causes no read. This is header coverage of known descriptors, not full
payload recovery, a complete game-code inventory, runtime testing or a match.

Before the real inventory, the helper reviews the implementation and fixed draft
profile. The draft profile is 772 bytes, SHA-256
`b04bb23944d1f9149a622516383f8a97ce6302c8e3215410eff0221aeb76b8a3`.
The reviewed implementation is 14,673 bytes, SHA-256
`84f18d2bc0e44b0f0bfd2a493603f946b65ad36bc44eef3c40027607c7613942`.
Only status freezing is expected before the real scan.

The header parser validates the independently known stored length rather than
mistaking the 64-byte prefix or sector extent for payload size. It bounds memory
ranges, validates word alignment where required and a terminated ASCII filename,
and retains fields 0x18/0x1C under raw names without semantic attribution. Every
raw/deobfuscated MWo3 claim stays visible as either a valid header or an explicit
invalid candidate. All name/base descriptor and size/base PT_NULL candidates are
reported; duplicate value matches stay ambiguous. Header ID agreement is separate
association evidence, not a reason to discard other value-compatible candidates.

The helper identifies that size/mtime-only post-scan ISO verification would admit
changed bytes with a restored timestamp. The primary adds a final full identity
check and repeats link checks before publication. The corresponding invented
mutation control now passes without changing earlier extraction code or locks.

## Meaningful tooling controls

Eleven new tests use invented archive bytes and bounded ELF/ISO fixtures, including
the actual ISO parser and inherited identity guards. No real image is mutated and
no compiler is invoked. Controls cover:

- Complete header size, raw address fields, malformed lengths/alignment/overflow,
  unsafe names, non-ASCII names and truncation.
- Exact short lengths 0/1/3/4/63/64/65, empty extents, truncated streams and floor-
  to-word decoding; no prefix read exceeds 64 or an entry's exact length.
- Raw and encoded valid claims plus malformed short MWo3 claims; no claimed
  malformed overlay disappears from the incomplete report.
- Duplicate descriptors/reservations and independent header-ID agreement, with
  unresolved and multiply matched cases kept explicit.
- Full invented ISO-to-report behavior, deterministic repeated evidence, source
  preservation and no payload output.
- Scope/identity/directory/decode-table/reference failures, report/input aliases,
  conflicting reports and post-scan mutations of all protected inputs, including
  ISO mutations with restored size and timestamp.

Independent execution passes **11 new tests, zero skipped**, and **320 tests in
the full suite, zero skipped**, preserving the previous 309 checks. These tooling
tests do not implement the full-game gate or its eighteen negative tests.
`tests/test_overlay_inventory.py` is 16,235 bytes, SHA-256
`a28bf14e2fa0a1e45981b5c6844f8b88fa5813ccbb0aa9ae837ac8fd59826b66`.

## Preserved preflight failure and correction

The primary's first actual invocation fails before entry-prefix scanning because
its fresh ISO inspector returns size/SHA-256 while the full catalogue lock also
requests SHA-1/MD5/CRC32. This is preserved in
`evidence/bucket-03r/first-invocation-failure.json`, with the initial implementation
snapshot. No report or decoded entry-prefix output is published. The primary
corrects only the inspector's expected field subset, adding a clarifying comment;
full `file_identity` catalogue checks before and after scanning remain unchanged.
The profile stays frozen, SHA-256
`bddd4163726e3b303a05fb2b0fa725e3f3d2ba016657288c0c11f6c2e6cd796f`.

Before another real scan, this helper independently reviews that exact diff and
adds a catalogue-shaped invented lock. It reproduces the same SHA-1 error against
the preserved initial implementation; the corrected implementation accepts that
same fixture. Wrong SHA-1, MD5 and CRC32 values still fail before prefix scanning.
All eleven new controls and 320 full-suite tests pass after the correction.
The approved corrected source is 14,869 bytes, SHA-256
`628643e527cdd88e5c266047e744534ce446713e97fdd37d041d6b48db13d24e`.
This correction changes preflight metadata handling before any actual prefix
result is observed; it does not relax payload/header acceptance.

## Actual reference audit

Both fresh reports are byte-identical: 3,380,121 bytes, SHA-256
`a7a3b1e7b88aefd342a4fdc4924200570496cd62abb241bd093165f5d383991f`.
Independent read-only validation rechecks the actual full ISO catalogue digest
set, pinned ELF, decode table and both reference locks. It parses the pinned
archive directory and reads every entry's exact bounded raw prefix itself. An
independently written byte-substitution/modular-XOR decoder, without calling the
scanner or its decode helper, reproduces every reported raw/decoded prefix hash,
magic value and candidate index.

There are 5,955 entries: 5,952 prefixes of 64 bytes and three empty extents, for
380,928 raw/decoded prefix bytes. There are zero raw MWo3 claims and exactly 355
deobfuscated MWo3 headers, with no malformed MWo3 claim. All seven numeric header
fields, filenames, declared stored lengths and header bytes are independently
checked. In particular, the earlier pilot entry 101 remains `movie_task.ovl`.

Each header maps to exactly one original named zero-sized descriptor by name and
base, and the 355 descriptors are covered bijectively. Every value-compatible
PT_NULL size/base candidate set is independently recomputed; all 355 header IDs
agree with an observed candidate index. This does not make value matching unique:
169 headers have multiple reservation candidates.

| Reservation candidates for one header | Header count |
| ---: | ---: |
| 1 | 186 |
| 2 | 16 |
| 3 | 6 |
| 4 | 12 |
| 5 | 5 |
| 6 | 6 |
| 8 | 8 |
| 26 | 26 |
| 90 | 90 |

The twelve distinct named starts remain groups, not proven disjoint slots. Two
headers extend beyond the next distinct named start; these flags also reproduce
independently. Neither sizes nor start spacing establish capacity, simultaneity
or load lifetime. Fields 0x18/0x1C remain uninterpreted raw addresses.

The successful status establishes complete header coverage of the existing 355
named descriptors under this scan. It does not identify code hidden in other
archive forms, prove function boundaries/ownership, or establish a complete
all-module code inventory. No full overlay payload is recovered, no source linked
or matched, and no compiler or game code is executed. ISO metadata is unchanged
after the independent readback; matching remains zero and the earlier initializer
remains visibly parked.
