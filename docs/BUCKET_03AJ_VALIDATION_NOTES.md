> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AJ independent validation

## Scope and inherited metadata contract

Read only the existing main ELF and newly prepared OPNSSMP PRX. Preserve every
closed reader/controller/input and the two3AI output witnesses. This bucket
interprets declared import records, not relocations, exports, runtime memory or
library implementations. A declared name/NID is not authentication or SDK/source
ownership and removes no original game-code obligation.

The3AF contract supplies bounded raw PT_LOAD fields and52-byte module-info
metadata. A pointer in this bucket may map only through exactly one file-backed
PT_LOAD interval covering its entire requested extent. BSS/memory-only bytes,
non-load records and overlay descriptors provide no stored-byte mapping. Main
ET_EXEC absolute fields and a PRX's unrelocated raw fields must remain distinct;
no relocation/base is synthesized. Mapping evidence must retain the raw value,
program index and exact file offset, without asserting a loaded runtime address.

## Independent failure/control plan

After primary-source layout review, exercise a fixed ordinary import record in
absolute and zero-based address models. Preserve empty spans/zero-count records
without fake array dereferences or silent record removal. Test exact segment-end
strings/arrays, missing terminators, overlong/nonASCII names, short/zero/overshoot
record sizes, count/span overflow and unsupported variable/extended forms.
Unsupported forms must leave the whole result explicitly incomplete or
uninterpreted, with no manufactured decoded total.

Test ambiguous and partially overlapping PT_LOAD ranges, memory-only/non-load
addresses, and whole-array spans crossing segment boundaries. Avoid mapping an
array piecemeal. Reject or explicitly preserve unsupported overlap among record,
name, NID and stub extents rather than reading aliases as independent structures.
Duplicate NIDs and all exact stub words must remain visible, with no deduplication
or assumed jr/syscall shape. Invented tests and pin/report-preservation controls
must precede any actual new import parsing.

## Exact pre-execution review

The primary assigns this reviewer the pure parser and its invented tests after
initial planning. The implemented API is inspect_import_tables(raw, metadata).
It returns BOUNDED_IMPORT_TABLES only for complete supported declarations;
expected format/mapping failures return UNINTERPRETED with both decoded totals
null, raw bounds/record evidence and a reason/code. Unexpected programming
errors propagate. Metadata must bind the exact raw input hash and come from the
unchanged bounded3AF contract. No file I/O or native execution occurs inside
the parser.

Initial source/tests submitted for independent review:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `evidence/bucket-03aj/import_tables.py` | 11,681 | `d55c8cc95e665bdd54209ebe7f346a36621b42f05636fba132006fe3ee3541ea` |
| `evidence/bucket-03aj/test_import_tables.py` | 11,961 | `b7e938bf1eed23c29ac69895b2b06724ae7625c67afd9a838d27bad7e43b0c8f` |

Only ordinary five-word records with zero variables are decoded. Attribute and
version bytes remain raw; no unrelated module-attribute enum or reserved-bit
mask is applied. Bounds are512 records,4096 function bindings per record and in
total, and256 stored name bytes including NUL. Empty mapped names remain explicit
empty declarations. Zero functions cause no NID/stub pointer dereference. Exact
NID order/duplicates and both raw stub words are retained; no instruction shape
is required or normalized.

The conservative mapping policy also rejects a second PT_LOAD's partial or BSS
intersection. This is this inspector's unsupported/ambiguous local model, not a
claim that the PSP SDK forbids that layout. Distinct reason codes separate
ambiguous load intersections from unmapped/memory-only extents. Supported shared
names/NID/stub bytes remain observations in bounded connected file-overlap
groups; group membership does not assert that every pair aliases. This avoids a
quadratic report expansion and never deduplicates declared bindings.

All twelve invented fixture tests pass without skips. The fixtures are real
bounded ELF/program/module-info chains interpreted through the unchanged3AF
reader before invoking this parser. They cover both address models, empty spans,
zero counts, unsupported/truncated records with no partial totals, name budgets/
terminators/ASCII, exact boundaries, duplicate/partial/BSS load overlaps,
non-load/memory-only/bridging extents, count budgets, shared/suffix extents,
duplicate NIDs/arbitrary stub words, stale metadata and surfaced programming
exceptions. These twelve tests are separate from the last352-test repository
suite and the unimplemented full-game gate. Neither actual main nor OPNSSMP
imports have been parsed by this reviewer before independent review/freeze.

The primary independently reviewed the whole parser and ran all twelve tests on
Windows. This reviewer ran them under WSL. The exact parser/test identities above
remain unchanged.

## Controller controls before actual parsing

The initial controller compared freshly calculated main metadata directly with
the complete old 3AF report. That report also contains a run-level
`known_main_whole_byte_control_exact` annotation, which the pure metadata reader
does not produce. Review caught this schema mismatch before any actual import
parsing. The correction pins the old reference lock/main reference and verifies
both complete main copies against the original bytes. Only after repeating that
whole-byte control and requiring the original generic-reader section status does
the controller recreate the annotation and compare the complete golden metadata.
No golden field is discarded or normalized.

Final pre-execution identities reviewed:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `evidence/bucket-03aj/read_import_inventory.py` | 11,281 | `19be3c48ffb5ff8132a697b44530f2c3556397104c8592c1386b9ff02f7613bf` |
| `config/psp-import-inventory.json` | 4,196 | `6ff07a9f5436edad3f84f9be1dd96d9d18d4d0b1d9351f5e51ab84abf251e76c` |

Twelve independent invented controls pass, retained in
`evidence/bucket-03aj/helper-validation-controller-controls.json`. Three checks
prove that the final controller executes pinned source bytes despite a valid
stale bytecode cache, and rejects changed or redirected source. Nine orchestration
cases cover complete success, an explicitly unsupported input with null totals,
rejection of leaked partial totals, wrong golden metadata, wrong original main
bytes, late input mutation, late report mutation, a redirected report and
preservation of an existing receipt. These cases use invented ELF bytes and
mocked orchestration; no original import tables or native tools were executed.
They are not full-game negative gate checks.

The final controller/profile are approved for the separately frozen two pure
parsing trials. The renewed window ends 16:21:44 UTC; retain the two-input scope.

## Actual frozen report readback

The primary ran the two pure parsing trials after the exact freeze. Windows
Python 3.13.14 and WSL Python 3.14.4 produce byte-identical semantic reports:
118,999 bytes, SHA-256
`23857ab9ad6e7b2350af7dbe6cb7c9a19c046d4f31d2216b81aaef39ce26502b`.
Separate receipts retain each Python environment and the correct source-copy
and semantic-report identities. The freeze is 593 bytes, SHA-256
`a28ce5e6623c2ebf9f8f8f77738608395bac8aa97c5d8d1c9f8fb1fd055f2507`.

This reviewer independently unpacked the raw ELF headers/program tables,
module-info import bounds and every ordinary record, name, NID and two-word
stub. The audit does not import or call the new import parser. The main's named
module-info section is at file offset 1,442,516; its raw import span is
144,053,068 through 144,053,788 (720 bytes). OPNSSMP's masked first-header
physical field identifies module info at file offset 760; its raw import span
is 556 through 596 (40 bytes). Each pointer extent maps wholly through exactly
one file-backed PT_LOAD, with no additional load intersection. The raw record
words, names including NUL, version bytes, uninterpreted attributes, array
lengths/order and all stub words equal the retained reports.

| Input | Declared libraries | Declared function bindings | Actual overlapping extents |
| --- | ---: | ---: | ---: |
| Main control | 36 | 297 | 0 |
| OPNSSMP | 2 | 2 | 0 |

OPNSSMP's declared names are `SysMemUserForUser` and `sceResmgr`, one binding
each. This identifies two import declarations. It establishes neither library
implementation ownership nor a loaded runtime address or unique game-function
count. Both results remain `BOUNDED_IMPORT_TABLES`, ownership `UNCLASSIFIED`.
No relocations were applied, exports parsed, stub opcodes normalized, module
instructions executed or code excluded from the future matching denominator.

Across both complete source-copy sets the independent audit checks 76 records
and 598 NID/stub pairs. It also verifies all 30 directly referenced pinned files,
the exact semantic report repeats, both receipt associations and the four
unchanged source-loader/pin function ASTs between the retained historical
controller snapshot and final controller. The original loader-control report
remains attached to its original snapshot; the current-controller controls are
separate. The final controller's complete nested input verification and freeze
verification also pass after readback.

Independent retained evidence:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `helper-validation-controller-controls.json` | 850 | `943f75bcab1e81be92bb7b55854d4787cdc5990462294aa000ae30c1f796401c` |
| `helper-validation-direct-audit.py` | 9,774 | `eafa4643029412482e9c156e2fc546432e94db5daa230790f4458ab6d572b735` |
| `helper-validation-direct-audit.json` | 9,283 | `9645aebfc25afe669ccbcde5fcd63e6c5ded1fe2ee7a733418f5f2802ae82e59` |

These findings add bounded metadata, with no source-match or full-build credit.
The archive initializer remains visibly PARKED: three plain attempts and one
commented matching shape; zero register pins, zero empty-asm lines and zero
credited game functions. The repository's last 352-test WSL result is separate
from this bucket's twelve invented parser tests and controller controls. The
full-game byte-identical build and eighteen required negative gate checks remain
unimplemented.

