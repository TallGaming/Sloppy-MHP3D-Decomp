> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AK: new archive arithmetic routine reviewed

The bounded review establishes a 140-byte straight-line leaf body at
`[0x08862700, 0x0886278C)`, file offset `0x613B4`, SHA256
`0ff874a4e619b6a6202257c13125a9ed1ed5dab4c45cbc0242eb9ad5f0a3261f`.
Its return at `0x08862784` includes the NOP delay slot at `0x08862788`. The next
word starts a neighboring stack prologue; no padding is included in this body.
Both independent instruction/control-flow reviews accept this extent. The raw
extractor report retains its original UNREVIEWED candidate label; this checkpoint
records the subsequent human review rather than rewriting that earlier result.

The original loads the upper field at incoming A0+`0x2F540`, then the lower at
A0+`0x2F53C`, once each. It computes both results in registers, stores upper then
lower and returns `(next_upper << 16) + next_lower`, without a field reload.
The products wrap to 32 bits before unsigned reductions:

| State half | Multiplier | Modulus |
| --- | --- | --- |
| Upper | `0x2345` | `0xFFD9` |
| Lower | `0x7F8D` | `0xFFF1` |

Signed MULT's low word supplies the same product modulo 2^32. Subsequent
unsigned high multiplies and shifts use reciprocal constants `0x801382F9` and
`0x80078071`. Both equal ceil(2^47/modulus). Their positive error terms are
3089 and 31073, respectively, and `(2^32-1)*error < 2^47`; this bounds the
quotient exactly for every 32-bit product. Allegrex MSUB and the lower
shift/subtract/add sequence recover the remainders. This is static arithmetic
analysis, not original MIPS execution or a runtime behavior test.

The existing public MHP2G method agrees mathematically, but its declared
volatile fields imply lower update/store first, then upper update/store and
a final lower reload. That sequence differs from this target. It must not be
copied unchanged as an exact source shape. Ordinary fields permitting compiler
reordering and explicit snapshots of volatile fields remain plausible source
hypotheses. The actual qualifiers, complete class and implicit C++ receiver are
not established by these bytes.

The known call at `0x08862870` targets this entry. Its bounded context XORs V0
with a preloaded word and stores the result, agreeing with the archive-key role.
The selected 96-byte window does not establish the complete caller body or
where its A0 receiver originated. No stronger caller claim is made.

The frozen scope was one 512-byte target window and one overlapping 96-byte
caller window: 128 unique original word addresses. Both reviewers verified
original bytes, the existing listing, all 35 body instructions, return/delay,
neighbor boundary, caller word and input/preservation pins. No instruction was
interpreted as executable game code, and no new native tool was installed.

Private evidence is in `evidence/bucket-03ak/`: exact scope/source profile and
freeze, bounded extractor/report, independent preflight/raw audits and final
assessment. Source comparison is `ARCHIVE_KEY_ADVANCE_SOURCE_REVIEW.md`;
independent validation is `BUCKET_03AK_VALIDATION_NOTES.md`. The profile is
`config/archive-key-advance-review.json`. The public source cache and prior
archive evidence remain unchanged.

No game draft was created or compiled. The parked initializer and four drafts
stay untouched, with the same three plain attempts/one commented shape, zero
register pins/empty asm and zero credited/linked-source functions. The historical
toolchain, complete code inventory and full-game gate remain open. Last full
tooling suite: 352 WSL passes, no skips; new static/preflight checks are separate.

The next proposal is one natural readable C++ diagnostic for this different
routine under existing fixed profiles, with unchanged probe controls and no
per-function flag choices. It requires its own source/profile review and freeze
before compilation, within the current approval ending 16:21:44 UTC. Native-port
implementation remains deferred until all game code matches.
