> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 1 checkpoint

2026-10-30. Implementation and validation are complete. The user accepted this
checkpoint with "Continue"; Bucket 2 proceeds under its separately presented plan.

## Scope and outcome

The approved scope was reproducible reference preparation, an executable/overlay
metadata map, repeatability checks and failure-path validation. The primary agent
owned preparation/integration, one helper owned mapping, and one owned independent
validation. Shared `scripts/elf32.py` was not changed.

| Output | Review location |
| --- | --- |
| Reproduce the reference and map | [REFERENCE_PREPARATION.md](REFERENCE_PREPARATION.md) |
| Preparation implementation | [prepare_reference.py](../scripts/prepare_reference.py) |
| Helper identity pin | [helper-tools.json](../config/helper-tools.json) |
| Mapping implementation | [map_executable.py](../scripts/map_executable.py) |
| Human-readable executable map | [EXECUTABLE_MAP.md](EXECUTABLE_MAP.md) |
| Independent review and source hashes | [BUCKET_01_VALIDATION_NOTES.md](BUCKET_01_VALIDATION_NOTES.md) |
| Preparation checks | [test_prepare_reference.py](../tests/test_prepare_reference.py) |
| Map checks | [test_map_executable.py](../tests/test_map_executable.py) |

## Validation actually performed

- `python -m unittest discover -s tests -v`: **49 passed, exit 0**.
  This comprises the 14 existing checks, 23 preparation checks and 12 map checks.
- Two real extractions/decryptions into different fresh output directories
  produced directly byte-identical encrypted and decrypted executables.
- Both final preparation reports and both final map reports are byte-identical.
- Running preparation again with correct existing outputs succeeds without
  replacing them and still reruns the helper. The default documented preparation
  and mapping commands were also run successfully.
- The real rejected HD image and a real missing-helper path each caused exit 1
  with no executable artifacts or success report published.
- Synthetic checks cover inactive locks, metadata/hash mismatches, absent/changed
  helpers, failure/timeout/missing output, staged-input/helper tampering, malformed
  ELF, bad existing outputs, conflicting reports, alias paths and ELF range errors.
- The independent validator rehashed the accepted original image and confirmed
  it remains unchanged. Reference input files and pins were not changed.

These are reference-tool controls, not the 18 future matching-gate negative
checks. No game runtime test, compiler selection or matching rebuild was performed.

## Final artifacts and identities

Local ignored evidence is under `evidence/bucket-01/`. Prepared game bytes are
under `reference/bucket-01/final-run-1/` and `final-run-2/`.

| Compared artifact | Size | SHA-256 of each final copy |
| --- | --- | --- |
| EBOOT.BIN | 2,247,664 | `9a4142cbe12086f538046633f59cc9b2bbf024c91b16cbe9710078d1cef91fb5` |
| EBOOT.ELF | 2,247,320 | `755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950` |
| Final preparation report | 1,180 | `17a4288be8405b6c4fd23e6c0e82dcccbadebb6e29949e1eeb1dc3758a07419c` |
| Final executable map | 819,425 | `451fa59db4cb04b14b462d1fecb0f7edef56265d30cfc861c0f6add28db90a96` |

`verification-summary.json` records these comparisons and the real failure
controls. `tooling-tests.log` records the 49-test run. Earlier exploratory reports
are preserved separately; the final filenames above identify this checkpoint.

## Map findings and limits

- 734 section headers and 356 program headers: one PT_LOAD and 355 PT_NULL entries.
- 355 zero-sized allocated overlay descriptors at 12 shared start addresses.
- **Zero overlay payloads extracted; zero game functions credited as matched.**
- Candidate reservation ranges overlap, so the 12 groups are not proof of 12
  disjoint physical slots. All name-to-program candidate pairings remain ambiguous.
- The named `.bss` section has size zero. The larger PT_LOAD non-file range is
  retained as declared memory; it is not treated as a proven complete BSS map.
- The Metrowerks/PSP comment is recorded, without claiming a precise compiler
  build, source language or flags. Game/library boundaries remain unclassified.
- Archive extents, compression, overlay bytes and runtime lifetimes remain unknown.

## Decisions verified

The active reference remains the clean original PSP ULJM05800 v1.02. The rejected
HD reference stays rejected. All game-code matching precedes native-port
implementation; library assembly policy, readable-source-first rules and the
full gate/18-check requirement remain in force. No renderer or port feature was
selected. Minimum hardware and right-stick camera behavior remain open.

## Review decision

Accept Bucket 1, request specific revisions, or stop. Acceptance closes this
checkpoint; the next step would be to present Bucket 2's detailed plan for
recovering one overlay. It does not authorize bulk recovery or later buckets.

Work remains in the local working tree, without a new commit or verified tag.
