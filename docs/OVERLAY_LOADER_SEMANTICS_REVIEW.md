> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Overlay loader semantics review — Bucket 3T

This is read-only static analysis, bounded to at most three loader candidates,
one caller and one representative routine referenced by an overlay word span.
The parked archive-seed initializer stays out of scope. No game/compiler runs,
source/profile changes or matching credit are part of this review.

## Related-format evidence: confirmed external construction

The cached MHP2G source is pinned to
[`5b98acfd014090b07c81e6b17f376a5eba986083`](https://github.com/tclamb/mhp2g-decomp/tree/5b98acfd014090b07c81e6b17f376a5eba986083).
The reviewer rehashed the two relevant cache files against
`evidence/bucket-03g/public-source-manifest.json`:

| Public file | Bytes | SHA-256 |
| --- | ---: | --- |
| `configure.py` | 32,855 | `a7326aa4daaf9b114d3461252239c97b0de52c5820de9d90d47e511c80cec403` |
| `tools/splat_ext/ctor.py` | 897 | `11d5df4f831c7369f17ba059b695f9f50083f2f69dd83a2bfb8282cd49588b01` |

The external evidence is stronger than a parser's chosen names:

- [`configure.py:624–631`](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/configure.py#L624)
  explicitly emits the eight header words. The final pair, at offsets `0x18`
  and `0x1C`, contains the overlay's generated static-init start/end symbols.
- [`configure.py:655–663`](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/configure.py#L655)
  places those symbols immediately around the selected overlay's `.ctor`
  section, then aligns the data end to `0x80`. Its separate `.init` input
  section precedes that pointer-range construction.
- [`ctor.py:6–10`](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/tools/splat_ext/ctor.py#L6)
  treats that related game's segment as references to `__sinit_` routines and
  emits it into `.ctor`; later lines configure word/reference disassembly.

These are confirmed facts about the pinned MHP2G reconstruction/build scripts.
Their header producer and section handling provide a concrete hypothesis for
our otherwise raw words. They do not prove that MHP3's consumer performs the
same calls, that every referenced word is a function entry, or that the exact
historical linker/compiler/source-unit conventions transfer.

Our earlier observed layout is compatible with this construction: in 303 MHP3
images `raw_0x18` is stored-end minus 128, while 52 have an empty span at the
stored end. That compatibility is corroborating layout evidence, not consumer
semantics. MHP2G's addresses, sizes, overlay groups, class fields, original-name
claims and compiler switches remain separate from the PSP v1.02 reference.

## Original-game consumer review

The reviewer checked every instruction word in the following complete main-image
ranges against the pinned ELF, then rechecked the retained extracts and report.
The main ELF is 2,247,320 bytes, SHA-256
`755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950`.
Analytical function names below are descriptive, not recovered symbols.

| Range, exclusive end | Bytes | SHA-256 |
| --- | ---: | --- |
| Ordered calls `0x0891512C–0x089151A0` | 116 | `ccf8695931b9cd0676fa72519d2cf8e457c3f2b999da37ed6c57253312bc7aa6` |
| Pair-table helper `0x089151A0–0x08915200` | 96 | `effbe5ff1b521c048835ef797b3059dae3e769cf5b31d127b94af9a775b8a6e4` |
| Header consumer `0x08915200–0x08915270` | 112 | `61a079015ccd36d600300862fe9beb08dbe21a5f7b103da29b613a0dcfb6e63b` |
| Caller `0x088E64A8–0x088E6544` | 156 | `c5758b4cc353236e61d29ea9a11811a999674956b515c96d814fa43ec5715b43` |

These ranges include their return or terminal-jump delay slots. Internal branch
targets stay within their respective functions. No additional callee bodies
were inspected.

The consumer saves the header pointer and incoming second argument. It reads
header `+0x14`, calls two cache imports, and conditionally invokes
`0x0880C468` with `(header + incoming_second_argument, 0, header[0x14])`.
This call is consistent with clearing declared BSS, but its callee and the
second argument's provenance as an image length are not proven in this scope.
Both conditional paths then load header `+0x18` and `+0x1C` into the first two
arguments of the ordered-call helper; the other two arguments are zero.

The loop compares unsigned `begin < end`, loads a word at the iterator, calls
that address through JALR, increments the iterator by four, and continues while
it remains below the end. Its `bnezl` at `0x08915170` loads the next word only
in a taken delay slot: on loop exit that load is annulled. A valid aligned
range is therefore consumed in forward order with an exclusive end. An empty
range, or unsigned begin at/above end, skips the callbacks. No explicit callback
argument setup occurs; a language-level `void(void)` prototype is unproved.

Afterward the loop forwards its saved third/fourth arguments to the pair-table
helper. That helper searches up to sixteen stride-eight records whose first
word is zero, writes the first argument there, and writes the second argument
followed by second-argument-minus-twelve to the other word. It returns an index
or minus one. In this consumer path both saved arguments are zero. This is not
evidence of registering an overlay ID; its wider role and ownership remain
unclassified.

The original import records independently associate stubs `0x08960C70` and
`0x08960C80` with `UtilsForUser` NIDs `0x79D1C3FA` and `0x920F104A`.
The pinned community PSPSDK
[`UtilsForUser.S`](https://github.com/pspdev/pspsdk/blob/460920c0c650ffcdf912863bc170430d08142c37/src/user/UtilsForUser.S)
names these `sceKernelDcacheWritebackAll` and
`sceKernelIcacheInvalidateAll`. Its retained source is 2,697 bytes, SHA-256
`e3369b30079249a64d1e4b8ed30185abc77bc08b3f504faaf9572316ab89cd51`.
These import identities do not identify the surrounding wrapper as SDK code.

## Caller and one pointed routine

The main-text direct J/JAL scan finds one call to the consumer, the JAL at
`0x088E6510`. Its caller obtains the header pointer from a table indexed by
the incoming third argument. It obtains the consumer's second argument from
an opaque indirect call via another object's function table at offset `0x14`.
No body behind that virtual call was examined. The caller finally records a
masked sixteen-bit input ID and tail-jumps to the instruction-cache import.

The 52-byte table at `0x08A1BE90` has SHA-256
`c8814794679ef14200631d9499647e4e928cd43159b1620e8f0ef0adce5cb1fe`.
Its first word is `0x08804000`; its remaining twelve distinct words equal
exactly the set of load addresses across all 355 recovered overlay headers.
The reviewer independently recomputed that equality from the complete recovery
manifest. This links the caller to the known overlay starts without proving
slot-zero eligibility, index bounds, load completion, capacities or lifetimes.
The sole-direct-call result excludes neither indirect callers nor overlay code.

The one representative is recovered entry 4590, `P_v00.ovl`, loaded at
`0x09E7CF80`. Its range `[0x09E7D300, 0x09E7D304)` holds `0x09E7D134`.
The full 1,024-byte payload was checked against its recorded SHA-256
`680fb098d6aedba108a88c59baa2eb2951aa6f6ffd8f6a13f444575f18f12a3c`.
The sixteen bytes at `[0x09E7D134, 0x09E7D144)` have SHA-256
`99c966228bfb1cd9b8917afea85e03e0d0820c1cb74f0bb6979e437e2663d0d4`.
This four-instruction wrapper sets arguments to one and **65535** (ORI, not
signed minus one), then tail-jumps to `0x09E7D0E0` with a NOP delay slot.
The terminal jump supplies a natural wrapper boundary; the target body was
deliberately not inspected. It corroborates an initialization interpretation
without identifying the ultimate initialization behavior or historical source.

## Result and remaining limits

The original code establishes the pair's operational role: an ordered range of
four-byte callable addresses consumed from the selected overlay header. The
load-path context, pointed wrapper and related game's explicit `.ctor`
construction strongly support describing it as an overlay initialization-call
range. They do not establish that every entry is a C++ constructor, recover
callback signatures, prove source language/compiler build, or identify runtime
library ownership. The 340 stored entries across 303 alternative images are
not 340 unique functions or a runtime trace; 52 images have empty ranges.

No inspected routine verifies header magic, callback alignment/executable
bounds, pointer-range length or table-index bounds. Earlier recovery checks
establish stored-file properties, not original runtime defenses. The opaque
size-like return and fill-call arguments do not prove the entire load/zeroing
chain. Shared starts and the 169 reservation ambiguities remain unchanged.

Retained evidence is `evidence/bucket-03t/loader-analysis.json`, 3,331 bytes,
SHA-256 `5c4b8242f6cc5ee178ad8377435237ea73fedf7c272e05283e9b3b140a0800c3`.
The reviewer audited its complete extracted main ranges, table, import NIDs,
representative payload/word/wrapper and public-source pins. No game/compiler
execution or source-match credit follows. Frozen manifests retain
`raw_0x18/raw_0x1c`; the parked initializer and earlier profiles stay unchanged.
