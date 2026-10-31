> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3C independent validation notes

The validation helper reviewed both source alternatives before cohort compilation
and approved their exact hashes for freezing. This is a controlled source-shape
experiment, not game-source integration, matching credit or runtime testing.
No commits were made.

## Pre-compilation source review

The baseline remains SHA-256
`d5d588c184c7c95a86bb3772e760f9251d33e3e4aabf92dfc0449c6ddc7c7a95`.
Independent byte comparisons establish:

| Full source copy | Size | SHA-256 | Only changed function |
| --- | ---: | --- | --- |
| `bench/hypotheses/compiler_probes_guarded_list.c` | 4460 | `ed2c865775d70d857cec9f8f825ecb5a5925bf4d09379c10465f886602c7b1d1` | `probe_08830654` body |
| `bench/hypotheses/compiler_probes_pointer_bytes.c` | 4425 | `2cd8899bd3ad3060e77cb0131c990f6f14ae4fd86879689a560b42f20dfb6ddf` | `probe_08830550` body |

The guarded-list copy preserves every byte outside baseline body range
`[2598, 2713)`, replacing it with variant range `[2598, 2760)`. The pointer-byte
copy preserves every byte outside `[2155, 2326)`, replacing it with
`[2155, 2338)`. These are zero-based, end-exclusive byte offsets. Signatures,
typedefs, purpose/uncertainty comments and the other thirteen function bodies
are unchanged in each copy.

Both changes are ordinary readable C:

- The guarded list returns zero for null. For a valid terminating list, its
  guarded do-while performs the same next-pointer reads and unsigned count
  increments as the baseline while loop. Ownership, typedefs and cycle handling
  remain unresolved.
- The pointer walk reads the same six valid signed-byte elements and retains
  ordinary conditional assignment of the zero/one result. Advancing the local
  pointer after the sixth read produces a valid one-past pointer under the stated
  input-domain assumption; it performs no extra read or external pointer write.

There are no assembly statements, register pins, barriers, volatile qualifiers,
changed types or unusual expression orders. Both exact source hashes were
approved before any new compiler output was inspected. Equality, if observed,
will not prove historical source, ownership, language or compiler configuration.

## Automated and real-output validation

From `<project-root>`:

```powershell
python -m unittest discover -s tests -v
```

Result: **150 tests passed** (exit 0): all 130 existing checks and 20 new
source-experiment checks. Tests use invented source/report fixtures and mock the
lower compiler bench; the validator did not execute a real compiler.

The new checks cover:

- Named body extents, nested control flow, comments, strings, quoted braces and
  prototypes. Missing/duplicate definitions, unterminated tokens, unchanged
  alternatives and changes to signatures, comments, typedefs or another body fail.
- Exact source/body/prefix/suffix identity, the pre-compilation review flag, two
  distinct alternatives and rejection of reserved `baseline` IDs. Repinning an
  unrelated body edit or changing the frozen body evidence cannot bypass checks.
- Complete matrix rows, flags, versions, probe sets and exact-count accounting.
  Missing, duplicate or extra rows/probes fail, including a row omitted from
  every cohort. Partial or credit-bearing baselines cannot become controls.
- Unchanged control sizes and hashes plus target identities must agree. Source
  changes are reported separately from exact probe counts; a higher synthetic
  score is not promoted into a source, ownership or compiler conclusion.
- All three cohorts preserve the original source/metadata. Derived variant
  metadata retains candidate/settings lists, and repeat runs use fresh report
  and derived-file paths with identical path-free outer reports.
- Wrong pins, changed inputs during a cohort, lower-bench failure or changed
  control bytes prevent a successful outer report. Conflicting evidence and
  report/input aliases preserve existing files.

Review found no material implementation blocker. The primary also identified a
reserved-ID collision risk in the aggregate report and added a `baseline`-ID
guard; the negative case is covered. The inherited bench retains its existing
compiler failure/warning, stale-object, symbol and relocation checks. These
150 tests are not the future matching gate's 18 negative checks.

## Independent audit of the two actual runs

The validator read both complete reports, all **528 compiler objects and 7392
function comparisons**, without running another compilation. The reports are
byte-identical: 2034441 bytes, SHA-256
`5fceb84ce537f189ea827ac4006b165547cd8a0e7c3dff89d04ae1c027999b35`.

Reports:

- `evidence/bucket-03c/final-experiment-run-1.json`
- `evidence/bucket-03c/final-experiment-run-2.json`

Retained object/report roots:

- `build/source-hypotheses-baxmplm9/`
- `build/source-hypotheses-q9__7fl_/`

Each root contains baseline, guarded-list and pointer-byte cohorts: 88 rows and
14 complete symbols per cohort. For every actual object, its hash, function
names, complete function sizes/hashes, target hashes, exact flags, first differing
bytes and exact counts agree with the report and pinned ELF. Candidate IDs,
versions and all whole-bench flags agree with the original pinned configuration.

Control checking also compared actual function bytes directly across cohorts:
all 4576 unchanged control sequences agree, comprising 1144 checks per alternative
per run. The repeated baseline report equals the complete accepted Bucket 3
baseline. Both alternative source hashes and the baseline/configuration/manifest/
reference-lock hashes still match their pre-compilation freeze. The reference
ELF and all 23 runner/compiler/support-file pins were independently rechecked.

Neither alternative produces its changed target exactly in any of the 88 rows.
The guarded-list body changes emitted bytes in 77 rows; its eleven O4-p rows
remain identical to the original list probe. The pointer-byte body changes
emitted bytes in all 88 rows. Each complete bench retains the same exact-count
table as baseline: 6/14 at O1/O2 and 1/14 at other tested settings. No functions
or settings were pooled into an uncompiled combined result.

The guarded-list O1/O2 output is 40 bytes rather than the target's 36. The
pointer-byte output reaches the target's 52-byte size at O4/O4-p/O4-s but still
differs in instructions. These observations show source-dependent code-generation
effects; they neither establish historical source nor falsify ordinary-input
semantic equivalence. No source revision or extra setting was introduced after
the freeze, and the original source/manifest/candidate configuration remain
unchanged.

## Reviewed implementation identities and limits

| File | SHA-256 |
| --- | --- |
| `scripts/bench_source_hypotheses.py` | `4d74bc9da8a7688ed86b7737282e27db536aea1e5c031d60fe4ab83d7b756596` |
| `tests/test_source_hypotheses.py` | `02e1df2f387b1e36bf28f7d57dea0bf63fa6dd15cd9ccaef48ce9cfbff038ba0` |
| `config/source-hypotheses.json` | `a6d2ffde2156713897932638f8422947c7752276243926aaf8beb772c4dd4745` |

No material blocker remains in the reviewed experiment paths. The source
alternatives remain prereviewed hypotheses; the experiment selects neither a
historical compiler/flags nor an original language or library owner. No game
function is integrated or credited as matched, no full executable is rebuilt,
and no game runtime testing is claimed. Further source alternatives or toolchain
experiments require the next separately reviewed bucket.
