> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Archive key-advance source review — Bucket 3AK

The frozen bytes support a 140-byte straight-line leaf that advances two 32-bit
archive states and returns their packed new key. Arithmetic agrees with the
related public method, but its volatile memory-access order does not transfer.
No new source attempt or compiler run occurred.

This is read-only analysis of the different entry 0x08862700. It does not reopen
the parked initializer, create a source draft, select flags or execute original
MIPS instructions. The target/caller extraction must be frozen before new
original-byte interpretation. Source-attempt and matching counters stay fixed.

## Existing public source: facts and mathematical behavior

The pinned MHP2G reconstruction at commit
`5b98acfd014090b07c81e6b17f376a5eba986083` provides
[FileSys::next_decryption_key](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/src/eboot/file_sys.cpp#L277-L282).
It performs these ordered operations:

1. Read the lower field; multiply by 0x7F8D and reduce modulo 0xFFF1; store lower.
2. Read upper; multiply by 0x2345 and reduce modulo 0xFFD9; retain that result in a
   local `next_upper` and store it to upper.
3. Return `(next_upper << 16) + key_lower`, reading lower again.

Its [field declarations](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/include/file_sys.hpp#L43-L50)
are volatile u32. Therefore this reconstructed source predicts lower load/store,
upper load/store, then lower reload, with no final upper reload. A class with
nonvirtual member entry is its external source model; that does not prove the
MHP3 class, member names, original qualifiers or compiler.

Unsigned 32-bit multiplication wraps before remainder in that source. For the
ordinary 16-bit-state domain, both products fit even signed 32-bit range:
65535×32653=2139914355 and 65535×9029=591715515. Each modular result is below
65536, so combining post-update halves by addition is well defined as u32.
For arbitrary corrupted/full-width field values, ignoring multiplication wrap
would describe a different algorithm. The source does not substitute defaults
after these updates: zero is possible and must not be silently corrected.

The observed shared arithmetic constants are source leads already associated
with this archive algorithm; they do not establish identical original function
boundaries, exact memory access order or full-input signedness in MHP3. Those
must come from the frozen target bytes and bounded callers. The external source
is reconstructed C++, not independently established historical Capcom source.
No matching or source participation claim transfers from another project.

The two existing public files were rehashed against their earlier manifest:
file_sys.cpp 17,508 bytes SHA256
`56fe632dde444067f99e401f58b97d7506a9efd13a7b962537e0baab223b9e02`;
file_sys.hpp 1,760 bytes SHA256
`a10cd2f9ca3dd78f60f5d3d662da625ac2f9ab4a69fd38fc9b879239129f7a97`.
`evidence/bucket-03ak/helper-map-public-context.json` records exact immutable
URLs, commits and cache paths. Source statements are evidence only; no external
build command or source instruction was executed.

## Original-byte scope and review status

The plan permits at most 512 target bytes and two 96-byte direct-call-site windows,
including the known JAL site 0x08862870. Before extraction, review the exact ELF
identity, selected ranges and driver. Afterward distinguish a complete function,
return delay slot, padding and neighboring code; a first return alone is
insufficient. Record update/return types, hidden receiver and qualifiers as
hypotheses wherever machine evidence does not establish them. No new candidate
compilation or shape is authorized by this source-only review.


## Exact pre-extraction approval and retained evidence

Independent scope approval covered profile `config/archive-key-advance-review.json`,
2,384 bytes, SHA256
`c36ec396072fc012bc1b07c8630bc1f2fad0b683f9f4baf16538f3a76a6f8494`,
and extractor `extract_key_advance.py`, 10,544 bytes, SHA256
`cda5ee31629380e1cb01199273c95f3c0fc8192a8544bbee1917590b91f9cad5`.
All nine source/reference/listing/preservation pins were independently checked
before extraction. The fixed 512-byte target and 96-byte known-caller window
overlap; the complete retained evidence covers 128 unique original word addresses,
not an expanded second function search. No target bytes were interpreted by this
reviewer before freeze notice.

`bounded-static.json` is 28,636 bytes, SHA256
`4bee7365fa9f53854827b34e22daa46cc245ea8627ff8e6e1e63a8bd6036ad9f`.
Its automatic first-return result remains labeled unreviewed in that original
artifact. The independent human findings below establish the narrower bounded
body without rewriting that historical automatic observation.

## Bounded original body, caller and data flow

The callable interval is **[0x08862700, 0x0886278C)**, 140 bytes, SHA256
`0ff874a4e619b6a6202257c13125a9ed1ed5dab4c45cbc0242eb9ad5f0a3261f`.
All 35 words form straight-line arithmetic/field accesses, followed by JR_RA at
0x08862784 and its NOP delay slot at 0x08862788. There is no preceding branch,
call, stack adjustment or `ra` write in this body. The next original
word at 0x0886278C starts a neighboring stack prologue; there is no intervening
padding, and the return NOP is not counted as alignment filler. The bounded
caller JAL at 0x08862870 decodes to this exact entry; afterward its v0 result is
XORed into the current data word. This supports the key-return role. It does not
establish a complete whole-program call graph or a C++ class identity.

The target adds 0x30000 to the incoming a0 for addressing, then accesses two
word fields at effective offsets 0x2F540 (upper) and 0x2F53C (lower). Its observable
memory sequence is:

1. Read upper, then lower, once each.
2. Compute both new values entirely in registers.
3. Store upper, then lower.
4. Return `(new_upper << 16) + new_lower` from retained register results.

There is no post-store field reload. The public MHP2G method instead performs
its lower volatile load/store before the upper load/store and reloads lower in
the return. Consequently copying that reconstructed volatile statement order
would not represent this target's access sequence. Ordinary nonvolatile fields
with compiler scheduling, or volatile fields explicitly snapshotted into locals,
are both compatible hypotheses. The target does not select one qualifier model.
The incoming pointer is consistent with a hidden receiver or an explicit C-style
context argument; class/field names, virtualness and original source types remain
unproved.

## Arithmetic proof without execution

Both initial MULT low words implement multiplication modulo 2^32, regardless of
the instruction's signed high half. Let P be either resulting 32-bit product.
The unsigned high multiply followed by shift 15 computes floor(P×M/2^47):

| State | Multiplier | Modulus d | Reciprocal M | d×M−2^47 |
| --- | --- | --- | --- | --- |
| Lower | 0x7F8D | 0xFFF1 | 0x80078071 | 31073 |
| Upper | 0x2345 | 0xFFD9 | 0x801382F9 | 3089 |

For each row, M=ceil(2^47/d) and (2^32−1)×(d×M−2^47)<2^47. Hence the reciprocal
quotient equals floor(P/d) for every unsigned 32-bit P: the positive reciprocal
error is too small to cross the next integer even for a remainder d−1. The upper
MTLO/MSUB/MFLO sequence retains the low word of P−quotient×0xFFD9. The lower
shift/sub/add sequence forms quotient×(65536−16+1)=quotient×0xFFF1 and subtracts
it. Both are exact unsigned remainders; the final packed addition uses disjoint
post-reduction 16-bit halves. No MIPS interpreter or original routine execution
was used for this symbolic reasoning.

Independent raw-byte audit compared every frozen window/hash/word and the known
JAL encoding directly to the pinned ELF. It also checked both freeze inputs.
`helper-map-independent-review.json` records the result (732 bytes, SHA256
`4b08daccbac65d411b424f11f7117c168d7b68d93f3b638ae9f6e10d71ee7c2d`).

The boundary and arithmetic are sufficiently clear to support one separately
planned plain-source diagnostic with explicit qualifier/layout hypotheses.
Nothing here creates that draft, chooses a compiler, attributes SDK ownership,
reopens the parked initializer or earns a matched/source-linked function. All
compiler flags, source budgets, parking/trick totals and runtime/port limits
remain unchanged.
