> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AK independent validation

## Fixed scope before extraction

This bucket reviews a different archive arithmetic entry, `0x08862700`. The
parked initializer and its four source drafts remain unchanged. No new source
form, compilation, flags, runtime or matching credit belongs to this review.

Review is limited to one original target window of at most 512 bytes and at most
two direct-call-site windows of 96 bytes each. The input ELF, existing public
counterpart and extraction scope must be pinned and reviewed before new original
bytes are extracted. This reviewer will not expand an ambiguous window silently.

The first `jr ra` is a boundary candidate. Independently trace internal branch
targets, delay slots and possible fall-through before accepting a body extent;
separate subsequent alignment words and neighboring code. Review each load/store,
arithmetic width/sign, constants, update order and the returned register against
the raw instructions. A reconstructed public method can suggest source/types;
it cannot establish the original compiler, ownership or exact class declaration.

The existing matching counters stay at one PARKED initializer, three plain
attempts, one commented matching shape, zero pins/empty-asm lines and zero
credited game matches. No gate result follows from a static analysis report.

## Exact pre-extraction approval

The reviewed profile fixes `0x08862700` plus 512 bytes, and one 96-byte caller
window at `0x08862840`, containing the declared `jal` at `0x08862870`. That caller
window lies within the target window, so the extraction covers 128 distinct
original word addresses. The original ELF/reference, existing full listing,
two public MHP2G source snapshots and their old manifest, fixed bounded I/O
helper, compiler profile and assembly manifest are pinned. Full input identity
and fixed-scope verification pass without extracting any new target body.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `config/archive-key-advance-review.json` | 2,384 | `c36ec396072fc012bc1b07c8630bc1f2fad0b683f9f4baf16538f3a76a6f8494` |
| `evidence/bucket-03ak/extract_key_advance.py` | 10,544 | `cda5ee31629380e1cb01199273c95f3c0fc8192a8544bbee1917590b91f9cad5` |

Nine invented orchestration cases pass: the positive case, missing/mismatched/
duplicate instruction listing, insufficient text extent, wrong direct-call
word, late input mutation, late report mutation and preservation of an existing
report. Nine transfer-encoding controls also pass. All fixture instruction and
ELF bytes are invented; no original MIPS instructions execute. The positive
case confirms that the first-return extent is still explicitly an unreviewed
candidate, not an automatic function-boundary proof. A late report failure can
retain its failed artifact; it is not an accepted final analysis result.

The controls are retained in `helper-validation-preflight.json`, 566 bytes,
SHA-256 `0e565b3f661257a5a9f540b7c75695f3b8b7a6cbda1ff347840a2fbe87cb61ec`.
Approval covers only the separately frozen bounded extraction. No original
target body was extracted or decoded by this reviewer before that freeze.

## Original-byte and boundary readback after freeze

The frozen extraction report is 28,636 bytes, SHA-256
`4bee7365fa9f53854827b34e22daa46cc245ea8627ff8e6e1e63a8bd6036ad9f`.
This reviewer independently reads the original ELF section declarations and
compares every extracted word and listing address against the original bytes.
All 128 distinct words match; the 24 caller words are the declared overlapping
subset. No new disassembler, compiler, MIPS interpreter or module is run.

The bounded entry body is 140 bytes at `[0x08862700, 0x0886278C)`, original file
offset 398,260, SHA-256
`0ff874a4e619b6a6202257c13125a9ed1ed5dab4c45cbc0242eb9ad5f0a3261f`.
Manual encoding review covers all 35 words: the first 33 are straight-line
arithmetic, loads and stores, followed by `jr ra` at `0x08862784` and its NOP
delay slot at `0x08862788`. There is no internal branch, call, indirect transfer
or exception before the return. At `0x0886278C` the next word is a stack-frame
prologue, with no intervening padding word. This supports the 140-byte bounded
entry body; it does not establish global symbol ownership or uniqueness of all
possible entry points elsewhere in the executable.

## Arithmetic and memory observations

The receiver is adjusted by `0x30000` before signed displacement accesses. The
two word fields are therefore at receiver offsets `0x2F540` (upper) and
`0x2F53C` (lower). Upper loads first, then lower. Their products use multipliers
`0x2345` and `0x7F8D`, retaining the low 32-bit product in each case. The signed
`mult` instructions do not establish signed source fields: their low word is
identical for signed and unsigned multiplication. The subsequent quotient
construction explicitly uses unsigned high multiplication and logical shifts.

The two literal reciprocal calculations are independently proved to divide the
full unsigned 32-bit product domain by `0xFFD9` and `0xFFF1` respectively:

| Divisor d | Reciprocal M | M*d - 2^47 |
| --- | --- | ---: |
| `0xFFD9` | `0x801382F9` | 3,089 |
| `0xFFF1` | `0x80078071` | 31,073 |

Each M equals ceil(2^47/d). For either positive error e in the table,
`(2^32-1)*e < 2^47`. Thus floor(n*M/2^47) equals floor(n/d) for every unsigned
32-bit n: the reciprocal error cannot cross the next quotient boundary. This is
a proof about the decoded constants, not execution or interpretation of original
MIPS instructions. The upper remainder uses `mtlo`/`msub` and `mflo`; only the low
word matters, so no unobserved HI value is needed. The lower reconstruction
subtracts q*(65536-16+1), which is q*`0xFFF1`.

The upper and lower remainders are retained in registers. The return word is
upper shifted left 16 plus lower. The upper field is stored first, then lower;
neither field is reloaded after those stores. The remainder bounds keep lower
below 65536, so the observed addition has the expected disjoint low-half role.

## Caller and public-source limits

The direct call at `0x08862870` has original word `0x0E2189C0`, which independently
decodes to entry `0x08862700`, followed by a NOP delay slot. Within the fixed
caller window, a word is loaded before the call; returned `v0` is XORed with it
and the result stored. Byte substitution loads/stores are also visible. The
local backward branch targets `0x08862818`, with a NOP delay slot. This selected
96-byte excerpt does not contain the full caller, complete receiver-argument
setup or every byte-substitution operation; those are not claimed as proved.

The pinned public MHP2G `next_decryption_key` method agrees on multipliers,
divisors and returned upper/low composition. Its source access sequence differs:
lower is written first, upper second, then the declared volatile lower field is
reloaded in the return expression. MHP3 instead reads upper first, writes upper
first and returns retained values. The public header's volatile qualifiers,
class layout and source statement order therefore cannot be transferred as
proof of this game's source. The field offsets are observed in MHP3 bytes;
names, exact class membership and qualifiers remain source hypotheses.

This evidence supports a separately planned readable arithmetic diagnostic with
explicitly stated type/access hypotheses. No draft or compiler run occurs in
3AK, and none is authorized by this validation note alone.

## Final evidence and status

`helper-validation-direct-audit.json` is 1,500 bytes, SHA-256
`2b36112d5af749c2b2877180a12836b8672401d9a68f3b65b0ce3fd65d9c849b`.
The original input pins, fixed scope, public-source association, compiler/
assembly preservation records and final freeze all still verify after readback.
The extraction report correctly retains its initial unreviewed candidate label;
this separate human review supplies the bounded boundary conclusion without
rewriting the frozen extraction. No game match, source attempt, language/compiler
attribution, library exclusion or runtime validation is credited. The parked
initializer and every matching counter remain unchanged.
