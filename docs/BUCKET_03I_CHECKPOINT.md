> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3I checkpoint

2026-10-30. The approved one-candidate archive-key experiment is complete.
**Both fresh trials produce the same valid 100-byte function against the complete
68-byte target. The candidate is NONEXACT. No source revision, flag search or
matching trick followed the result.**

## What was established

The selected seed initializer occupies `[0x0886233C, 0x08862380)`, including its
return delay slot. Existing disassembly, direct calls/tail ingress and the
neighboring return/prologue support this complete boundary. Its 68-byte hash is
`7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57`.

The target uses a receiver in `a0` and a 32-bit seed in `a1`, split with a logical
shift and mask; the original declared signedness is unknown. It stores the
upper seed half at receiver offset `0x2F540`, the masked lower half at `0x2F53C`,
substitutes low default `0x7F8D` if the local lower value is zero, then reloads
the upper field and substitutes `0x2345` if that read is zero. Accesses are
32-bit. No null check, original class identity or total object size was inferred.

One natural C++ candidate models only these fields and the unknown prefix. It
declares volatile state as a **pre-output hypothesis**, supported by the actual
upper reload and pinned MHP2G declarations. The qualifier and class name remain
uncertain. A local lower half preserves the observed absence of a low-field
reread; the upper-then-lower write order preserves the observed access sequence.
The partial-layout assertions do not invent an original full class.

Both reviewers approved the source, layout and complete target. An invented
small-record method established the exact symbol
`initialize_key__17ArchiveKeyContextFUi` before target compilation. The single
source and command were then frozen. Both trials used unchanged MW219/C++/O2:

```text
wibo mwccpsp.exe -nostdinc -lang c++ -c -O2 -o OBJECT SOURCE
```

## Observed mismatch

| Measure | Result in both trials |
| --- | --- |
| Complete target | 68 bytes |
| Complete candidate symbol | 100 bytes |
| First differing byte | Offset 0 |
| Exact intervals | 0 / 1 |
| Compiler diagnostics | Empty; exit zero |
| Output metadata | ET_REL, flags `0x10970001`, MW comment `3.0.0` |

The target computes `receiver + 0x30000` once and retains it. The candidate
recomputes that base before each of five word accesses. Five LUI/ADDU pairs
instead of one account for the extra eight instructions, or 32 bytes. Register
choices, instruction scheduling and branch displacements also differ. The
observed accesses/defaults agree with the hypothesis; byte equality does not.

This does not isolate compiler revision, optimization policy, qualifier modeling
or original source/translation-unit context as the cause. No alternate model or
manual address-base shape was tried. The candidate remains visibly retained as
a failed diagnostic hypothesis. It is not an integrated game rewrite or a
silently parked function; the approved experiment allowed one source candidate.

## Review artifacts and reproduction

| Artifact | Purpose |
| --- | --- |
| [archive_key_initializer.cpp](../bench/archive_key_initializer.cpp) | One readable, commented NONEXACT candidate |
| [archive-key-probe.json](../config/archive-key-probe.json) / [archive-key-experiment.json](../config/archive-key-experiment.json) | Complete target, exact member symbol and frozen inputs/command |
| [archive_key_naming.cpp](../bench/archive_key_naming.cpp) | Invented member-naming fixture |
| [bench_archive_key.py](../scripts/bench_archive_key.py) | Fresh compilation and unchanged strict complete-byte comparison |
| [ARCHIVE_KEY_PROBE_REVIEW.md](ARCHIVE_KEY_PROBE_REVIEW.md) | Independent boundary, source and final-output review |
| [test_archive_key_probe.py](../tests/test_archive_key_probe.py) / [BUCKET_03I_VALIDATION_NOTES.md](BUCKET_03I_VALIDATION_NOTES.md) | Failure controls and independent artifact audit |
| [OUTSIDE_SUGGESTIONS_REVIEW.md](OUTSIDE_SUGGESTIONS_REVIEW.md) | Supplied advice assessed against actual project status and requirements |

From `<project-root>`, use fresh report paths:

```powershell
python scripts/bench_archive_key.py --report evidence/bucket-03i/new-trial-1.json
python scripts/bench_archive_key.py --report evidence/bucket-03i/new-trial-2.json
wsl -d Ubuntu -- python3 -m unittest discover -s tests -v
```

The candidate is 1806 bytes, SHA-256
`6c4be341bcc3f113b56ccf7494a7b624a550b52f89c9c827eacbbce56e1f71d3`.
The frozen profile is 1902 bytes, SHA-256
`30b5372dab0d1e2fb9dc0ec4436ca0e78af1922728c5a421499a66e2a4cc5188`.
Its historical pre-compilation declaration records the status-only freeze point.

Both reports `evidence/bucket-03i/archive-key-run-{1,2}.json` are byte-identical:
1154 bytes, SHA-256
`e937d49b28b94694f7fa8b1c67db88a8c229ec1394f903a03cb6cc4815509e59`.
Fresh roots are `build/archive-key-probe-h53umlmt` and
`build/archive-key-probe-btnq7jgt`. Each 768-byte object has SHA-256
`1d715acabd4cdec572d40c1905504881a396fa5e11296f1163533b30941d7796`;
its complete 100-byte function has SHA-256
`193c361fab07498ef61aa22bfa4c417f10bfbfcd0cdb8bd50a591f7838aad2da`.

## Validation and scope

All **239 tooling tests pass under WSL, with no skips**: 226 existing plus 13
new archive-probe controls. Invented tests cover complete member identity,
extra targets/functions, byte/length mismatches, relocations, invalid naming
evidence, fixed scope/attempt/flag bindings, compiler failures, warnings,
timeouts, missing output, changing pins/object bytes and report preservation.
Real report/input-alias and wrong-member controls return exit one before new
compilation directories or success reports. See the local verification summary
and tooling log in `evidence/bucket-03i/`.

Independent audit verified both complete target/object comparisons, unchanged
source and naming evidence, and 201 local/11 native pin records. The original
fourteen-probe bench and all prior profiles remain unchanged. Outside advice
was treated as reference: no assembly injection, new flags, linker, normalized
acceptance rule, emulator installation or runtime test was adopted.

The clean PSP ULJM05800 v1.02 target, readable-source-first rule, library-assembly
policy, stuck rule and fixed-toolchain requirement remain in force. Original
language and full toolchain remain unproven. Matched/source-linked game functions,
parked functions and counted tricks remain zero. The full game gate and its
18 negative checks remain unimplemented; runtime and port work remain deferred.
Stop for user review. No second source attempt or further bucket is authorized.
