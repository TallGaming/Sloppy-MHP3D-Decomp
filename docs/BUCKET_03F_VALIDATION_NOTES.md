> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3F independent validation

2026-10-30. The validation helper reviewed the profile before linking, added
invented tooling controls, and independently read the two final trials. **All
four real links failed with exit 255 and no ELF.** Nothing in these trials
validates a linked function or locks the historical toolchain.

## Review before results

The reviewed draft `config/linker-isolation.json` was 2032 bytes, SHA-256
`afc431a0bb038eeb5491abe8a7cbe653e9931b46059b0025694733c1817f75bb`.
The final frozen profile is 2033 bytes, SHA-256
`ddf78aa4d06d042e1a7f56765377e6e73b47c2931f6ed479536af280780e1f54`.
Replacing only its status value with the draft status reproduces the reviewed
draft hash. `evidence/bucket-03f/profile-freeze.json` records both pre-link
reviews. No Bucket 3F link output had been observed before that freeze; the
earlier Bucket 3E failures motivated this bounded comparison.

The minimal script is 306 bytes, SHA-256
`ff22d32c21f218aad04f04f78b8cfc355186c9ac62d9bfd6b420416e867a1f8d`.
It retains the SNC `.text`, `.rodata`, `.data` and nonallocated `.reginfo`
payload sections without discard or library clauses. The default case omits
`-T`; the explicit case adds this script and fixes text at `0x08804000`.
The same entry symbol, warning policy, comments, map/trace options, compiler
profile, O0 setting, invented source and native Windows linker are inherited
from Bucket 3E. Each trial compiles once, then uses that same object for both
cases. The script and address policy are a combined experimental change; the
cases do not isolate a particular clause or exception cause.

For a hypothetical successful default link, placement is obtained from the
unique function in the output ELF, then checked against its entry and executable
section/PT_LOAD mappings. It is not assumed to equal the explicit address.
The unchanged Bucket 3E comparator checks every byte in the complete function,
with no trimming, masking or relocation workaround.

## Tooling controls

`tests/test_linker_isolation.py` contains 13 tests using invented ELF bytes and
mocked compiler/linker calls. They cover:

- Default placement distinct from the explicit address, while retaining strict
  symbol, entry and executable-load mapping requirements.
- An explicit-address mismatch and changed complete function bytes.
- One compilation and one immutable shared object per trial, fresh repeat
  directories and identical reports that omit generated directory paths.
- Rejection of unreviewed, additional, reordered or changed cases and flags.
- Compile failures, warnings, timeouts, missing/invalid objects and two honest
  not-run case outcomes.
- Independent case outcomes, warnings, timeouts and missing ELF/map files.
- Fatal shared-object mutation before the second case and before report writing.
- Input/profile pins checked before and after work, report conflicts and aliases
  that preserve existing evidence and inputs.

The helper independently ran the new test module: **13 passed, zero skips**.
It also ran `wsl -d Ubuntu -- python3 -m unittest discover -s tests`:
**209 passed, zero skips**. The primary retained the full log in
`evidence/bucket-03f/tooling-tests.log`. These are tooling checks, not the
required 18 negative checks for the future full-game matching gate.

The primary's real report/input-alias and wrong-layout-pin controls returned
exit one without a new build directory or successful report. The helper reviewed
their records in `evidence/bucket-03f/verification-summary.json`; it did not
rerun links to repeat those controls.

## Independent final artifact audit

The two final reports, `evidence/bucket-03f/isolation-run-1.json` and
`isolation-run-2.json`, are byte-identical: 3904 bytes, SHA-256
`bafda38fab6e86013a2c6e8f7f2ea18c0cc71ae49300b84ddddefbeca22ec81c`.
The helper inspected their retained artifacts in:

- `build/linker-isolation-w8h8e0us`
- `build/linker-isolation-9stye3hw`

Each directory contains exactly one `snc-smoke.o`, one compile log and two
separate case log/map pairs. Both objects are 616 bytes, SHA-256
`c0b233c8c2049470ca92516735aa2e51cf02beaef95825fc62108f1b5ddaee1f`.
Their parsed metadata exactly equals `report.input`: ET_REL, flags
`0x10a23001`, no comments, and a 24-byte `family_smoke` function. Its complete
instruction-byte hash is
`16146464e212b5009c239afc25965b8a3760fe36ec770dd1e43286f2771eff05`.
Both case records in each report name this same input hash.

All four link logs report an internal linker exception. All four case records
have `LINK_FAILED`, exit 255, and no output hash. No `*.elf` exists in either
trial directory. Each report records zero preserved cases and zero game-match
progress. The four partial maps list the fixture at zero under the default
layout and `0x08804000` under the explicit layout. They are diagnostic artifacts,
not validated ELF placement, load mappings or post-link instruction bytes.
The trace text names the single invented input; no SDK/runtime library was
requested. The final trial's separately retained shared crash dump is outside
this helper's artifact audit and is not used here to infer a root cause.

The helper recomputed every declared current input identity: **193 local pin
records and 16 native dependency records matched**. This includes the inherited
original source/probe/reference configuration and compiler/support files, as
well as the two new local pins. Duplicate declared pin records are counted as
records, not distinct files. No original ISO was opened or modified for this
audit. Windows DLL pins describe the recorded dependencies, not a complete OS
snapshot.

## Final implementation identities and limits

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `scripts/bench_linker_isolation.py` | 9986 | `56f8c5c165559f297204f872b2ead84729e18635ae6188704695b19696f299b9` |
| `tests/test_linker_isolation.py` | 17000 | `b3eab91e8cc86f186b22cd24cfb39abc0d20682fdde7ffa597617f581b2b97a8` |
| Unchanged `scripts/bench_synthetic_link.py` | 15511 | `a5b0c1872102ee8735888678f8eb5649abad7b3c2481b8057d863a9aa36d1cad` |

The observed exception does not require the larger Bucket 3E layout. It also
persists with no explicit script and with the minimal script. This does not
identify a faulty section, host dependency, linker implementation detail or
historical game toolchain, nor show that all SNC objects cannot link. No source,
flags, headers or profile was revised in response to a result. No game code was
compiled, linked or executed. Game match credit, source-link credit, parked
functions and counted matching tricks remain zero; native-port work and the
full-game gate remain deferred. Stop at the Bucket 3F review checkpoint.
