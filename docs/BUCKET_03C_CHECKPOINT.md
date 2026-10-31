> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3C checkpoint

2026-10-30. The approved two-source experiment is implemented and validated.
**Neither alternative produces exact target bytes.** The user accepted this
checkpoint with "Ok". A separate compiler-attribution plan is proposed; the
game toolchain remains unlocked and reconstruction has not started.

## Outcome

Both independently reviewed alternatives changed the intended source-control
feature, but neither closes its target mismatch. They remain readable C with
the existing signatures/types and no assembly, register pins, barriers, volatile
qualifiers or unusual expression orders. Each source was frozen before the first
compiler invocation and was not revised after observing results.

| Separate full-bench copy | Changed function | Exact changed probe | Best complete bench score |
| --- | --- | --- | --- |
| Guarded do-while list count | `0x08830654` | 0 / 88 configurations | 6 / 14 |
| Pointer-walking byte reduction | `0x08830550` | 0 / 88 configurations | 6 / 14 |

The list alternative obtains the initial guard/bottom loop but emits 40 bytes
at levels 1/2, including an extra `nop`, versus the target's 36. The pointer scan
obtains pointer induction while its loop comparison/conditional assignment still
differ. Matching size in some configurations is not matching bytes.

All thirteen unchanged functions retain exactly the baseline's compiled bytes
for every build/setting in both alternatives. The rerun baseline report is also
directly byte-identical to the complete accepted Bucket 3 report. Scores and
function shapes were not pooled across independently compiled copies/settings.

No compiler build or settings can be selected from these results, and the
negative outcomes do not by themselves prove that every tested compiler is
wrong. Source spelling, unit context, attribution and configuration remain
unresolved. Do not silently change flags or introduce tricks to increase scores.

## Review locations

| Artifact | Purpose |
| --- | --- |
| [SOURCE_EXPERIMENT.md](SOURCE_EXPERIMENT.md) | Reproduction, comparison guarantees, outcome and limits |
| [SOURCE_HYPOTHESES.md](SOURCE_HYPOTHESES.md) | Pre-run rationale/review, exact freezes and later instruction-level results |
| [Guarded list source](../bench/hypotheses/compiler_probes_guarded_list.c) / [pointer scan source](../bench/hypotheses/compiler_probes_pointer_bytes.c) | Two full-bench copies, one declared body change each |
| [source-hypotheses.json](../config/source-hypotheses.json) | Reviewed freeze, exact body spans and source/input hashes |
| [bench_source_hypotheses.py](../scripts/bench_source_hypotheses.py) | Body-only checks, identical matrix execution and unchanged-control enforcement |
| [test_source_hypotheses.py](../tests/test_source_hypotheses.py) / [BUCKET_03C_VALIDATION_NOTES.md](BUCKET_03C_VALIDATION_NOTES.md) | Failure controls and independent audit |

## Validation performed

- **150 tooling tests passed**: the previous 130 plus 20 source-experiment
  checks. These cover body-only/lexical proof, review and hash pins, complete
  rows/probes, exact-count/flag consistency, control drift, fresh repeated runs,
  source/metadata changes, failed cohorts and report preservation/aliasing.
- Each real experiment compiled three full source cohorts, each with the same
  eleven builds and eight settings: 264 objects and 3,696 target comparisons.
  The two runs therefore produced 528 objects and 7,392 target comparisons.
- Independent validation read all those objects/comparisons and all 4,576
  unchanged-control byte sequences. Source freezes, original source/configuration,
  reference ELF and tool pins remain unchanged.
- Both complete reports are directly byte-identical: 2,034,441 bytes, SHA-256
  `5fceb84ce537f189ea827ac4006b165547cd8a0e7c3dff89d04ae1c027999b35`.
- The guarded alternative changes code in 77/88 rows; the pointer alternative
  changes code in 88/88 rows. Neither changed function is exact anywhere.
- Real report/input-alias and wrong-source-pin controls returned exit 1,
  preserved the inputs and published no successful aggregate report.

Local ignored evidence is under `evidence/bucket-03c/`:
`final-experiment-run-1.json`, `final-experiment-run-2.json`, their logs,
`verification-summary.json` and `tooling-tests.log`. The summary locates both
retained fresh build roots, with all derived metadata and individual cohort
objects/reports. No existing baseline file was replaced.

## Decisions preserved and next review

The clean PSP v1.02 target, readable-source-first rule, fixed-toolchain
requirement, library-assembly policy and all-game-matching-before-port sequence
remain unchanged. No new compiler flags or builds, additional functions/overlays,
library labels or game source integrations were introduced. Both functions have
one original draft plus one reviewed alternative in this experiment; no automatic
permutation or additional source iteration was performed.

Matched/source-linked game functions and matching trick/parking counts remain
zero. The full game byte-match gate and its 18 negative checks are unimplemented;
these 150 tooling checks do not replace them. No game runtime testing,
reconstruction, port implementation, commit or verified tag was performed.

Review this bucket, request revisions, or stop. If accepted, a useful next small
plan is to reassess compiler attribution while holding these source hypotheses
fixed. The linked Metrowerks comment has not proven which compiler produced
these unclassified intervals. No broader compiler-family comparison was performed
or authorized here. Present its concrete evidence/tests/scope before starting;
do not continue changing loops or silently move into Bucket 4.
