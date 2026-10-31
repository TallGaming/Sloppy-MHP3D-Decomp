> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3L checkpoint

2026-10-31. The approved eleven-build Metrowerks comparison is complete.
**None produces the original 68-byte initializer under the unchanged natural
C++ source and fixed O2 command. Five tested builds produce one identical
124-byte body; the other six produce the existing identical 100-byte body.
Both fresh trials reproduce all outcomes and the historical build-219 control.**

## Complete outcomes

| Tested build | Complete function | Exact target bytes | Same body as 219 |
| --- | ---: | --- | --- |
| 121 | 124 bytes | No | No |
| 134 | 124 bytes | No | No |
| 139 | 124 bytes | No | No |
| 147 | 124 bytes | No | No |
| 151 | 124 bytes | No | No |
| 180 | 100 bytes | No | Yes |
| 192 | 100 bytes | No | Yes |
| 201 | 100 bytes | No | Yes |
| 205 | 100 bytes | No | Yes |
| 210 | 100 bytes | No | Yes |
| 219 | 100 bytes | No | Yes |

All eleven cases validate the exact raw member symbol and complete executable
extent, without unsupported code relocations. No case is omitted or assigned
partial credit. Each differs from the complete target beginning at byte zero.
Compiler diagnostics are empty and all return codes are zero. Corresponding
whole objects and full function bytes repeat exactly across trials.

The first group has 784-byte objects, SHA-256
`dedc7a696787a92047605277693ab1b3b6174e4b7a06633adb2f75077a3bb77b`,
and 124-byte functions, SHA-256
`7ce91b0e3c662a669d6f6d390548f387449bfb3421d03a0c5ee632d7ab1b565e`.
The second group has 768-byte objects, SHA-256
`1d715acabd4cdec572d40c1905504881a396fa5e11296f1163533b30941d7796`,
and 100-byte functions, SHA-256
`193c361fab07498ef61aa22bfa4c417f10bfbfcd0cdb8bd50a591f7838aad2da`.
All retain flags `0x10970001` and comment `MW MIPS C Compiler (3.0.0)`.
These are observed groups for this input; untested intervening builds and the
compiler's internal pass changes remain unknown.

## Actual instruction differences

The 124-byte body places the default-value stores in separate blocks, using
three additional unconditional branches and their NOP delay slots. Those six
words account for its extra 24 bytes relative to the 100-byte body. Branch
conditions, block order and displacements differ. The complete aligned comparison
records 22 differing word positions against 219, including the longer extent;
equal size or a word count is never treated as byte equality.

Both output groups retain five LUI `0x3` plus receiver-ADDU field-base pairs.
The original retains a single shared base and occupies 68 bytes. Register
choices, scheduling and branch displacements still differ from the target;
removing address instructions would not establish complete byte identity.
These observations do not identify an aliasing mechanism or backend pass order.
The forward-only invented-fixture checker from 3J was neither expanded nor used
to classify the older output's backward transfers. This comparison uses full
function bytes and separately inspected disassembly.

- Original complete 68-byte target (local-only artifact: `evidence/bucket-03l/target.disasm.txt`)
- Build 121 complete 124-byte output (local-only artifact: `evidence/bucket-03l/mwccpsp_3.0.1_121.disasm.txt`)
- Build 219 complete 100-byte output (local-only artifact: `evidence/bucket-03l/mwccpsp_3.0.1_219.disasm.txt`)

All eleven complete candidate disassemblies are retained alongside these files.
Their objdump identity, commands and output hashes are in the verification summary.

## Frozen scope and evidence

No source revision or new compiler download occurred. The single 1806-byte
candidate remains SHA-256
`6c4be341bcc3f113b56ccf7494a7b624a550b52f89c9c827eacbbce56e1f71d3`.
Its field/type/volatile/class hypotheses, exact raw member name and complete
target `[0x0886233C,0x08862380)` remain those reviewed in 3I. There is still one
source hypothesis; comparing eleven compilers adds no distinct source draft.
All tools come from the unchanged installed candidate catalogue, with executable,
DLL, archive, help and runner hashes verified before and after each matrix.

The same established execution helper and compiler working-directory behavior
as 3I use the fixed command for every build:

```text
wibo VERSION/mwccpsp.exe -nostdinc -lang c++ -c -O2 -o FRESH_OBJECT bench/archive_key_initializer.cpp
```

Both helpers reviewed the exact 7030-byte draft before scoring, SHA-256
`da60d7ac014b168ac3e24fd3288d209151efe88b7aa4fbc320768687c78718e1`.
Only its status value changed for freezing. The final profile is 7029 bytes,
SHA-256 `dd7e64f430030098e590d6ab82170b015fd1a0ceadd0cce58395d413461dc339`.
Its pre-score declaration records the historical freeze point, not the current
absence of results.

| Artifact | Purpose |
| --- | --- |
| [mw-archive-versions.json](../config/mw-archive-versions.json) / freeze record (local-only artifact: `evidence/bucket-03l/profile-freeze.json`) | Exact eleven cases and immutable inherited inputs |
| [bench_mw_archive_versions.py](../scripts/bench_mw_archive_versions.py) | Fresh complete comparisons, rejected-case retention and output integrity |
| Trial 1 (local-only artifact: `evidence/bucket-03l/mw-archive-versions-run-1.json`) / trial 2 (local-only artifact: `evidence/bucket-03l/mw-archive-versions-run-2.json`) | Every declared outcome and actual word differences from 219 |
| [MW_ARCHIVE_VERSION_REVIEW.md](MW_ARCHIVE_VERSION_REVIEW.md) | Independent pre-score and full-artifact review |
| [BUCKET_03L_VALIDATION_NOTES.md](BUCKET_03L_VALIDATION_NOTES.md) / [tests](../tests/test_mw_archive_versions.py) | Meaningful invented failure controls and repeat audit |
| Verification summary (local-only artifact: `evidence/bucket-03l/verification-summary.json`) / test log (local-only artifact: `evidence/bucket-03l/tooling-tests.log`) | Primary audit, real failure controls and disassembly provenance |

Fresh roots are `build/mw-archive-versions-zvq4q_dh` and
`build/mw-archive-versions-vuhu7uvb`. Both 28320-byte reports have SHA-256
`da591776f3c67ac849be85511da9bcb7d7b875b262b5befdbb47efb2cf101f5c`.

## Validation and checkpoint

All **283 tooling tests pass under WSL, zero skips**: 271 prior plus twelve
new runner tests. Invented controls keep the actual nested input verification
enabled and mock only compilation. They cover the exact matrix/source/flags,
full function lengths and changed words, naming/relocation failures, historical
219 drift, changed pins, retained timeout partials, output mutation and report
preservation. Earlier strict comparators and profiles remain unchanged.

Both independent audits checked all 22 objects and complete target comparisons,
repeat hashes and full comparisons against 219. Validation checked 610 aligned
word positions, 253 local pin records and eleven native dependency records.
The primary separately reinspected the objects and ran real report/profile-alias
and wrong-optimization controls. Both reject before a new compilation directory
or success report, preserving the frozen input. No compiler was rerun for audits.

From the project root, reproduce with fresh report names:

```powershell
python scripts/bench_mw_archive_versions.py --report evidence/bucket-03l/new-trial-1.json
python scripts/bench_mw_archive_versions.py --report evidence/bucket-03l/new-trial-2.json
wsl -d Ubuntu -- python3 -m unittest discover -s tests -v
```

This rules out an exact result from these eleven invocations of this source.
It does not exclude Metrowerks generally, recover original source context or
select a game compiler/configuration. Readable-source-first, fixed-toolchain,
library-assembly and stuck-rule requirements remain in force. Source-link,
game-match, parking and counted trick totals remain zero. The full-game gate
and its required 18 negative checks remain unimplemented; runtime and native-port
work remain deferred. Stop for user review; no further experiment is authorized.
