> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# PSP import-table format review — Bucket 3AJ

Both frozen byte-parser trials agree: 36 main import declarations/297 function
bindings and two OPNSSMP declarations/two bindings. These are declared imports,
not unique game functions or library implementation ownership.

This is a declaration inventory for the existing main ELF and prepared OPNSSMP
container. A library name/NID describes a requested binding, not implementation
ownership, authentication, successful runtime linking or a compiler selection.
No export parsing, relocation, relabeling or original-code execution belongs here.

## Pinned primary record definitions

The [PSPSDK load-core declaration](https://github.com/pspdev/pspsdk/blob/460920c0c650ffcdf912863bc170430d08142c37/src/kernel/psploadcore.h#L231-L252)
explicitly defines record length in 32-bit words. With PSP 32-bit pointers the core
record has these stored fields:

| Byte offset | Stored field | Width |
| --- | --- | --- |
| 0 | Library-name pointer | u32 |
| 4 | Minimum version | two raw bytes |
| 6 | Import attributes | u16 |
| 8 | Record length | u8, multiplied by 4 bytes |
| 9 | Variable count | u8 |
| 10 | Function count | u16 |
| 12 | Function-NID array pointer | u32 |
| 16 | Function-stub array pointer | u32 |
| 20 | Optional variable-stub pointer | u32, only where record length includes it |

Its C structure includes the optional sixth word; that does not make every
on-disk record 24 bytes. The [SDK tool structure](https://github.com/pspdev/pspsdk/blob/460920c0c650ffcdf912863bc170430d08142c37/tools/prxtypes.h#L50-L59)
is the 20-byte core and combines version/attributes into one raw word. Preserve
both version bytes and attributes without inventing reserved-bit masks.

[PPSSPP's corresponding fields](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/HLE/sceKernelModule.cpp#L179-L205)
agree. Its loader advances a u32 pointer by the record's length, and recognizes
5/6-word entries plus a seventh unknown word. Its acceptance/warning behavior
is emulator policy, not a complete format certificate. The bounded parser's
approved subset is **five words, zero variables**. Short/zero lengths, extension
words, variable forms or other unsupported declarations must remain explicit;
no silently skipped entries or complete-looking total may follow a failure.

The [function loop](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/HLE/sceKernelModule.cpp#L1150-L1169)
uses one 4-byte NID and one 8-byte stub per function. Variable imports instead
use the optional pointer to (addr,NID) pairs and further relocation references.
This bucket does not interpret those forms. Preserve raw record words and every
observed function stub's two instruction words; do not synthesize a desired
instruction sequence or infer a function name from a NID alone.

The [SDK stub macro](https://github.com/pspdev/pspsdk/blob/460920c0c650ffcdf912863bc170430d08142c37/src/base/pspstub.s#L37-L53)
emits a two-word return/NOP sequence. The
[alternative import macro](https://github.com/pspdev/pspsdk/blob/460920c0c650ffcdf912863bc170430d08142c37/src/base/pspimport.s#L23-L40)
initially emits two metadata words, while the
[fixup tool](https://github.com/pspdev/pspsdk/blob/460920c0c650ffcdf912863bc170430d08142c37/tools/psp-fixup-imports.c#L648-L672)
checks the 8:4 stub/NID size ratio and later rewrites those words. These are
pipeline examples; they do not require our original file stubs to match one
shape and do not identify its producer.

All six public source texts, immutable commits, URL/path metadata, sizes and
SHA256 identities are in `evidence/bucket-03aj/helper-map-import-sources.json`.
The manifest has a `files` array and contains no original game bytes. Public
source instructions/macros are evidence only; none were executed.

## File mapping and interpretation limits

For the main ET_EXEC image, stored addresses are declared linked virtual
addresses. For PRX, keep unrelocated raw virtual addresses and do not guess a
runtime base. A nonempty range maps only if exactly one file-backed PT_LOAD
covers all bytes **and no other PT_LOAD memory extent intersects any requested
byte**. The implementation conservatively includes another load's BSS-only
intersection in this ambiguity rule; it does not assert universal SDK invalidity. The file offset is p_offset+(rawVA−p_vaddr). A second partial overlap is
ambiguous even if one segment fully covers the range or both contain equal
bytes. Do not map through PT_NULL reservations, relocation segments or the
memsz-only BSS tail; do not bridge adjacent segments.

The raw p_paddr-based module-info file-offset rule is a separate provenance path,
not a virtual-address conversion. Raw imports_begin/end come from the existing
bounded 52-byte module-info observations. Recompute that metadata exactly against
the old main and prepared OPNSSMP golden reports before using it. A pointer
requiring a relocation not interpreted here may remain unmapped/uninterpreted;
that does not establish a corrupt SDK format or permission to repair it.

Bound table bytes, record progress/count, function totals, string search lengths,
NID extents and stub extents. Strings need a terminator inside a uniquely mapped
file-backed range; no host strlen-style scan beyond that bound. Preserve array/
name sharing and exact aliases as declarations, without silently deduplicating
bindings or calling shared pointers invalid. Overlaps the implementation cannot
represent must remain explicitly unsupported. A failed mapping/record means
incomplete interpretation and no invented complete totals.

## Independent implementation review status

Final pre-parse approval covered:

- Parser `import_tables.py`, 11,681 bytes, SHA256
  `d55c8cc95e665bdd54209ebe7f346a36621b42f05636fba132006fe3ee3541ea`.
- Invented tests `test_import_tables.py`, 11,961 bytes, SHA256
  `b7e938bf1eed23c29ac69895b2b06724ae7625c67afd9a838d27bad7e43b0c8f`.
- Controller `read_import_inventory.py`, 11,281 bytes, SHA256
  `19be3c48ffb5ff8132a697b44530f2c3556397104c8592c1386b9ff02f7613bf`.
- Profile `config/psp-import-inventory.json`, 4,196 bytes, SHA256
  `6ff07a9f5436edad3f84f9be1dd96d9d18d4d0b1d9351f5e51ab84abf251e76c`.

The full parser, twelve invented ELF-chain tests, controller and profile were
independently read. The supported resource bounds are 512 records, 4,096 total
function bindings and 256 name bytes including the terminator. Table/NID/stub
word alignment and printable-ASCII names are conservative supported-subset
constraints, not a universal SDK-format validity claim. Empty import spans and
zero-function records avoid dereferencing empty arrays. Unsupported records,
range/name failures and budgets leave both decoded totals null, including after
a supported prefix. Unexpected programming exceptions propagate as failures.

Alias groups are connected overlaps of **file extents**, not pairwise runtime
alias proofs or deduplicated functions. Exact sharing and suffix-string sharing
remain observations, with each declared binding counted separately on a fully
supported table. Tests preserve duplicate NIDs and arbitrary original stub words.
They cover actual ELF/module-info chains, both address models, zero counts,
unsupported forms, bounds/alignment, name caps/terminators, additional load/BSS
intersections, function budgets and metadata byte identity.

The controller pins all six primary sources and three metadata dependencies,
recomputes full old metadata exactly, and compiles verified Python source bytes
instead of accepting stale pyc. Four retained synthetic source-loader artifacts
were independently rehashed: equal-length cached 22, pinned 11 and changed 33
sources plus timestamp-mode bytecode. The report records stale ordinary import,
verified-source execution and changed/redirected source rejection. It records the earlier controller identity
`958df8761c0fc366c3f74d81752b375c73a059a1f1242cc061121434da1d68ed`;
the historical `source-loader-controller-snapshot.py` now resolves that exact
full-file hash without editing the original control report. Independent AST
comparison confirms guard/regular/check_record/load_module unchanged in the
final controller; `source-loader-controller-history.json` records the association. It reads no game input and is not a game gate test.

Final source/input snapshots gate the separate trial receipt; semantic JSON
contains no host path/trial identity while receipt metadata records the Python
host. Approval permits only two pure parsing calls after exact freeze. The
proposed Windows/WSL repeats test deterministic pure-byte interpretation,
not gameplay or native-module behavior. Matching source/flags, parked drafts,
ownership policy and zero credited game matches remain unchanged.


Before final freeze, independent review caught that the historical main golden
report adds a whole-byte-control witness after its pure metadata reader returns.
The final controller pins the original reference/lock, requires both main copies
to equal that complete original ELF, re-establishes its old section-reader status
and only then adds the exact witness before comparing the full golden metadata.
No golden field is removed or normalized, and no input/header is changed. This
pre-execution correction adds evidence rather than weakening the comparison.


## Frozen actual results and independent byte audit

The Windows Python 3.13.14 and WSL Python 3.14.4 trials produce identical semantic
reports: 118,999 bytes, SHA256
`23857ab9ad6e7b2350af7dbe6cb7c9a19c046d4f31d2216b81aaef39ce26502b`.
Host/trial/output paths appear only in separate receipts. Both input cases are
`BOUNDED_IMPORT_TABLES`; all observed records fit the preselected five-word,
zero-variable subset. No cap or format rule was changed after reading them.

| Input | Import record bytes / file offset | Declared records | Function bindings |
| --- | --- | --- | --- |
| Original main | 720 / 1441792 | 36 | 297 |
| Prepared OPNSSMP | 40 / 716 | 2 | 2 |

OPNSSMP declares requests to `SysMemUserForUser` and `sceResmgr`, one binding
each. The names do not authenticate or identify the ownership of OPNSSMP's own
implementation. Counts are per-input binding declarations; they are not a
cross-module unique-library count or a unique game-function denominator.

Independent auditing used raw ELF headers and file bytes, not the parser being
validated. It selected original module-info locations, reconstructed PT_LOAD
mapping evidence, and compared all 38 records, 299 NIDs, every two-word stub,
string, raw version/attribute and file-offset mapping. Both complete input copies
per case were rehashed and compared. Actual referenced extents have no alias
groups under the declared file-overlap model; this does not prove a universal
absence of runtime aliases. The first/last main records and both OPNSSMP records
also have individually recorded bounded byte identities.

The separate audit is `helper-map-independent-byte-audit.json`, 2,589 bytes,
SHA256 `1e70b281c532dab79560593be5abd3f713bf30155cb062067ac78371547e2145`.
All 25 current config/source-cache input pins and the exact freeze inputs remain
unchanged. Historical source-loader evidence has an exact restored source
snapshot and independently equal loader/pin ASTs; the validator's additional
current-controller checks cover false totals, wrong goldens/reference, late
input/report/link drift and receipt preservation. None is a full-game gate test.

This bucket establishes bounded declared import inventories for exactly these
two images. It applies no relocation, executes no native tool or original module,
resolves no function names, changes no symbols, excludes no SDK/game code and
earns no matched/source-linked functions. Compiler/source budgets, visible
initializer parking and the outstanding full build/18-negative-check gate stay
unchanged.
