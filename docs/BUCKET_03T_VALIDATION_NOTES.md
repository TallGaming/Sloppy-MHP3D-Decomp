> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3T independent static validation

## Scope and original-byte identity

The bounded review inspects three original loader/runtime ranges, one caller and
one representative pointed routine. Preliminary listing searches also reject
same-offset request-record/vtable coincidences; those excerpts do not establish
header consumers. No new Ghidra analysis, compiler, linker, game execution or
source/profile change is performed. Ownership of the three runtime bodies remains
unclassified; import identification does not classify their callers as Sony SDK.

Every retained main-ELF instruction word is independently compared with the
pinned original ELF bytes, including all branch/jump delay slots. The exact five
reviewed ranges are:

| Analysis label | Original range, exclusive end | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Ordered call range | `0x0891512C..0x089151A0` | 116 | `ccf8695931b9cd0676fa72519d2cf8e457c3f2b999da37ed6c57253312bc7aa6` |
| Post-range table helper | `0x089151A0..0x08915200` | 96 | `effbe5ff1b521c048835ef797b3059dae3e769cf5b31d127b94af9a775b8a6e4` |
| Header consumer | `0x08915200..0x08915270` | 112 | `61a079015ccd36d600300862fe9beb08dbe21a5f7b103da29b613a0dcfb6e63b` |
| One caller | `0x088E64A8..0x088E6544` | 156 | `c5758b4cc353236e61d29ea9a11811a999674956b515c96d814fa43ec5715b43` |
| One P_v00 pointed routine | `0x09E7D134..0x09E7D144` | 16 | `99c966228bfb1cd9b8917afea85e03e0d0820c1cb74f0bb6979e437e2663d0d4` |

The 3,331-byte retained `loader-analysis.json` has SHA-256
`5c4b8242f6cc5ee178ad8377435237ea73fedf7c272e05283e9b3b140a0800c3`.
Its raw extracts and listing hashes reproduce independently. Analysis labels are
not recovered original function names, and adjacent return/prologue boundaries
are static observations rather than runtime coverage.

## Header-to-indirect-call dataflow

The consumer saves its first argument as the header pointer in s2 and the second
as s1. It reads the word at header+0x14 into s0. After two cache import calls, a
zero value branches directly to range processing; otherwise it calls an external
routine with a0=header+s1, a1=0 and a2=that word. This is consistent with clearing
a trailing BSS range, but the called clearing implementation is outside this
bucket and is not newly identified as a library function.

At `0x0891522C`, BEQZL's start-word load in the delay slot executes only when
s0 is zero. The nonzero path reloads the start word after the external call at
`0x08915244`. Both paths therefore deliver header+0x18 as a0 and header+0x1C as
a1 to `0x0891512C`; a2 and a3 are explicitly zero, the latter in the JAL delay
slot. This original dataflow establishes that the two fields are used as the
begin/end addresses of an ordered indirect-call range, rather than a single
callable entry address.

The range helper copies start/end into preserved iterator/end registers. An
unsigned start<end check skips an empty or reversed range. For a nonempty range
it loads one word at the iterator, JALRs through that word, increments by four
and compares unsigned against end. The back-edge BNEZL loads the next pointer
only on the taken path; it does not read past end on exit. JALR has a NOP delay
slot. There is no per-word null/sentinel check, alignment check or per-element
argument setup in this loop. The pointed routine may inherit argument-register
values; this review does not invent a zero-argument ABI contract.

After the range, the helper forwards its saved original a2/a3 to the 16-slot
post-range table helper. That helper scans eight-byte slots using the first word
as its occupancy test, stores its arguments and finally overwrites its second
stored word with a1-12. The current header consumer passes zero/zero. A destructor
registration or other high-level purpose is not established by this review.

## One caller, load-start table and cache identities

A raw J/JAL opcode scan of original .text, independent of disassembler labels,
finds exactly one direct reference to the header consumer: JAL at `0x088E6510`.
Indirect references elsewhere are not ruled out. Its caller indexes a table with
the original a2, takes the selected word as the consumer's header pointer, and
forwards the return value of an earlier virtual call (vtable offset 0x14) as the
consumer's second argument. The virtual callee is outside the approved scope;
its returned value is not independently proven to be a stored-image length here.
The caller does not locally validate the table index or prove slot-zero usage.

The 52-byte table at `0x08A1BE90` has SHA-256
`c8814794679ef14200631d9499647e4e928cd43159b1620e8f0ef0adce5cb1fe`.
Its thirteen words equal `0x08804000` followed by the twelve distinct overlay
load addresses from the frozen recovery manifest. These are observed load starts,
not disjoint capacities or proven lifetime/allocation rules.

The original import records independently bind `0x08960C70` to UtilsForUser NID
`0x79D1C3FA` and `0x08960C80` to NID `0x920F104A`. The pinned pspsdk
UtilsForUser import declarations at commit
`460920c0c650ffcdf912863bc170430d08142c37` name them
`sceKernelDcacheWritebackAll` and `sceKernelIcacheInvalidateAll` respectively.
The retained 2,697-byte source snapshot verifies SHA-256
`e3369b30079249a64d1e4b8ed30185abc77bc08b3f504faaf9572316ab89cd51`.
Thus cache-call names have import evidence; that evidence attributes neither the
three inspected runtime bodies nor every game source unit to an SDK/compiler.

## Recovered images and the one pointed routine

All 340 raw word observations are reread directly from the frozen recovered
images and compared with the manifest, including the 52 empty ranges. Both sets'
710 complete payload-file identities and the preserved source/assembly/profile
pins reproduce. Pointer triples (archive index, word address, stored value),
serialized as compact JSON, have SHA-256
`3223429c5d1b9441e88a6fcf552879305f3de880f3d83101f4412f0fad30595d`.
Every value is aligned and in its image's declared code range. This proves none
of the other 339 candidate function boundaries or bodies; only one is inspected.

In entry 4590, `P_v00.ovl`, the word at `0x09E7D300` is `0x09E7D134`.
The selected sixteen-byte routine loads a0=1, uses ORI to load a1=0xFFFF
(**65535, not -1**), then tail-jumps to `0x09E7D0E0` with a NOP delay slot.
The tail target body is not inspected. Its shape is consistent with an
initialization wrapper but cannot alone identify constructors, original classes,
source language or compiler. Related-project constructor names remain
corroboration, not imported identities.

The new firm result is the original header fields' ordered indirect-call-range
use. C++ constructor attribution remains a stronger hypothesis with limits,
not a recovered source declaration or a compiler lock. No image or callback is
executed. Source matching/linking/runtime progress remains zero; the archive
initializer stays PARKED. The preceding 329 passing tooling tests are the last
regression result, separate from this static audit and the future full-game gate.
