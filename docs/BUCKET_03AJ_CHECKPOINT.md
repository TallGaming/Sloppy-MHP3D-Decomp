> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AJ: bounded import-table inventory completed

Both pure parsing trials produce the same 118,999-byte report, SHA256
`23857ab9ad6e7b2350af7dbe6cb7c9a19c046d4f31d2216b81aaef39ce26502b`.
Windows Python 3.13.14 and WSL Python 3.14.4 agree in every semantic report byte.
No original module or native tool executes during this inventory.

| Input | Library declarations | Declared function bindings | Status |
| --- | ---: | ---: | --- |
| Original main ELF | 36 | 297 | Bounded supported import tables |
| Prepared `opnssmp` PRX | 2 | 2 | Bounded supported import tables |

These count declarations/bindings, not unique game functions or credited
decompilation. The main image names include PSP graphics, controller, audio,
storage, networking and security libraries. `opnssmp` declares
`SysMemUserForUser` and `sceResmgr`. Names/NIDs do not establish implementation
ownership or authenticity. No SDK exclusion or assembly manifest changed.

Primary PSPSDK definitions and PPSSPP loader source establish the ordinary
five-word/function-only layout and four-byte NIDs/eight-byte stubs. This reader
intentionally leaves extended records, variable imports, ambiguous mappings and
unsupported caps/alignment/string forms uninterpreted, with decoded totals
withheld. Pointers map only through a unique complete file-backed PT_LOAD
extent; partial/BSS load overlap is conservatively unsupported. No relocation
is applied and no loaded runtime pointer is invented. Raw record words,
attributes/version, NIDs, stub instruction words and mapping evidence remain
in order. Shared file extents are observations, not automatically SDK-invalid.
Neither actual input has alias groups.

Twelve invented ELF/module-info chain tests cover both address models, empty/
zero-count cases, unsupported records/no partial totals, exact end and budget
boundaries, malformed names, ambiguous/BSS/non-load/bridging maps, aliases and
surfaced programming errors. Twelve separate controller/source-loader checks
cover orchestration and preservation. An invented timestamp-valid stale Python
cache returns the deliberately wrong value through ordinary import; the pinned
source loader returns the exact expected value and rejects source drift/links.
The original loader-control revision is preserved with an explicit historical
source association; later main-witness changes leave those loader functions
identical. These checks are not the 18 future full-game build-gate tests.

Before actual parsing, review caught an old report-level whole-byte main-control
witness absent from the pure reader's return. The controller now independently
re-establishes full equality to the pinned original main ELF and the original
section-reader status, then adds that witness before comparing the whole golden
metadata object. No golden field is dropped or normalized. Exact source/tests/
profile reviews and freeze preceded both actual trials.

Independent auditors read original ELF/segment/module-info/table bytes without
using the import parser. They verified all 38 ordinary records and 299 binding
pairs per semantic set, with one auditor checking both four-copy sets explicitly
(76 records / 598 pairs). Names, raw words, pointers, strings and mapping fields
agree. Both reports, preparation-witness associations, source caches and nested
pins pass. See `PSP_IMPORT_TABLE_FORMAT_REVIEW.md` and
`BUCKET_03AJ_VALIDATION_NOTES.md`.

Private evidence is under `evidence/bucket-03aj/`: source manifest/caches,
parser/tests, source-loader checks/history/snapshot, independent controller/raw
audits, exact freeze and two trial receipts. Each receipt pins its fresh private
`build/psp-import-inventory-*/report.json`. The profile is
`config/psp-import-inventory.json`; original preparation sources remain unchanged.

The toolchain remains unlocked, the complete game-code inventory and18-test
build gate remain incomplete, and credited/linked-source counts remain zero.
The parked initializer, its three plain attempts/one commented shape, zero
register pins/empty asm and all earlier evidence remain unchanged. The last
full tooling suite remains 352 WSL passes/no skips; new checks are separate.
No port work begins before matching all game code. Continue only through the
next documented reviewed bucket within the approval ending 16:21:44 UTC.
