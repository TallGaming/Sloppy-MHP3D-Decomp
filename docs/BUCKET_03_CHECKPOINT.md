> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3 checkpoint

2026-10-30. The user accepted this compiler-investigation output with "Ok".
**The toolchain milestone remains unmet: no compiler, flags, assembler or linker
is locked.** A follow-up plan is proposed; executable reconstruction has not started.

## Outcome and proposal

Eleven pinned Metrowerks PSP builds were compared using the same fourteen
reviewed, frozen plain-C probes and eight whole-bench settings. The bench covers
444 target bytes; ownership is unclassified for every probe. There were no
source permutations, per-function flags or matching tricks.

Every build scores 6/14 exact probe sequences at `-O1` and `-O2`, and 1/14 at
the other tested settings. All six newly added larger probes remain nonexact.
Equal scores conceal differences between compiler builds; none is identified
as the original toolchain. The metadata and linking questions are also unresolved.

**Recommendation: keep the toolchain unlocked.** Review this evidence, then
plan a small follow-up investigation before reconstruction. Do not select an
optimization level just because it wins this limited table. These source drafts
are hypotheses; mismatches can reflect source/types, unit context or compiler
configuration, and do not by themselves reject every tested compiler.

## Review locations

| Artifact | Purpose |
| --- | --- |
| [COMPILER_INVESTIGATION.md](COMPILER_INVESTIGATION.md) | Reproduction, full setting/build groups, limits and follow-up proposal |
| [compiler_probes.c](../bench/compiler_probes.c) | Fourteen readable source hypotheses, frozen before the new results |
| [compiler-probes.json](../config/compiler-probes.json) and [COMPILER_PROBE_REVIEW.md](COMPILER_PROBE_REVIEW.md) | Target hashes, function boundary evidence, semantics and exclusions |
| [compiler-candidates.json](../config/compiler-candidates.json) | Compiler/DLL/runner/archive pins and the complete matrix |
| [bench_compiler.py](../scripts/bench_compiler.py) | Fresh compilation, section-indexed comparison and failure handling |
| [test_bench_compiler.py](../tests/test_bench_compiler.py) and [BUCKET_03_VALIDATION_NOTES.md](BUCKET_03_VALIDATION_NOTES.md) | Synthetic controls and independent audit |

## Validation performed

- **95 tooling tests passed**, including 25 new bench checks and all 70 prior
  tests. The fixtures test invented ELF/symbol/relocation layouts, duplicate or
  missing functions, malformed boundaries, stale/missing objects, failed/warning
  compiler invocations, timeout, changed inputs/DLLs and conflicting reports.
- Two fresh complete matrix runs each compiled 88 objects and compared 1,232
  probe sequences. Their reports are directly byte-identical: 552,555 bytes,
  SHA-256 `9e36e6753a49730eb90fa66cfc31f19bef726e541a853eb85cb9504abbecb046`.
- Independent validation checked all 176 retained objects and 2,464 comparisons
  against their symbols, actual bytes, target pins and report fields. It also
  verified runner/compiler/support files, archives, help output and provenance.
- Real wrong-DLL-pin and intentionally invalid-option controls returned exit 1
  without a success report. The invalid option is solely a failure control,
  outside the scored matrix. No selected compiler flags were changed.
- A help-output hash discrepancy was caught and corrected before the final
  runs: the pins now hash actual saved bytes, including their line endings.

Local ignored evidence is under `evidence/bucket-03/`: `final-bench-run-1.json`,
`final-bench-run-2.json`, their logs, `verification-summary.json`, compiler help
output, and `tooling-tests.log`. The summary locates both retained fresh build
directories. The source and probe manifest stayed fixed across all comparisons.

## Decisions preserved and outstanding evidence

The clean original PSP ULJM05800 v1.02 remains the matching reference; HD and
translation support stay deferred. Readable source comes first. Compiler flags
will be fixed once a configuration is established. SDK/third-party code still
requires positive identification before library-assembly treatment. All original
game code must match before native-port implementation.

The target's compiler comment and ELF flags differ from the tested objects;
their different build stages have not been reconciled by a controlled linker
experiment. C++ support-looking strings do not prove the game code's original
language. Calls, globals/relocations, floating point, VFPU, original unit context,
assembler/linker and full executable layout are outside the present bench.
None of these gaps is silently resolved by the six exact tiny controls.

Matched and source-linked game functions remain zero. Matching trick/parking
counts remain zero. The full game gate and its 18 negative checks remain
unimplemented; the 95 tooling tests are separate. No game runtime testing,
additional overlay recovery, reconstruction, port implementation, commit or
verified tag was performed in this bucket.

Review outcome: accept this investigation, request revisions, or stop. Acceptance
does **not** establish a toolchain or authorize Bucket 4. The recommended next
step is a separately presented follow-up investigation plan addressing unit/
ownership evidence, call/global relocations and link/metadata requirements.
