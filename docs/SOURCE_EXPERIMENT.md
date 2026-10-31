> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Reproduce the two-source experiment

Bucket 3C tests two independently reviewed C hypotheses while preserving the
original fourteen-probe bench. The outcome is negative: neither alternative
emits its target bytes in any of the tested configurations. These are source
experiments, not integrated game functions or a game-toolchain selection.

## Command and frozen inputs

From `<project-root>`, with the existing pinned tools and verified ELF:

```powershell
python scripts/bench_source_hypotheses.py --report evidence/bucket-03c/my-review.json
python -m unittest discover -s tests -v
```

[source-hypotheses.json](../config/source-hypotheses.json) records the freeze,
input identities, two declared functions, body spans and body/prefix/suffix
hashes. Its SHA-256 is
`a6d2ffde2156713897932638f8422947c7752276243926aaf8beb772c4dd4745`.
Both alternatives received independent readability/semantic review before any
compiler invocation. [SOURCE_HYPOTHESES.md](SOURCE_HYPOTHESES.md) records that
review, the original predictions and the later results separately.

Each alternative is a full source copy that changes only one function body.
The driver verifies every outside byte, including signatures, comments, types
and the other thirteen functions. It preserves the original source and target/
candidate configuration files. Derived local metadata changes only the source
path/hash and its manifest hash. No source or flag override is exposed by the CLI.

## Controlled comparison

The unchanged lower-level bench compiles three source cohorts: baseline,
guarded-list and pointer-byte scan. Each uses all eleven pinned compiler builds
and the same eight existing whole-bench settings. One complete experiment
produces 264 fresh objects and 3,696 full-function comparisons against target
bytes. It also checks 2,288 unchanged-control pairs across the two alternatives.

Compiled symbol sizes/hashes for each of the thirteen controls must equal the
baseline at every build/setting. Missing/duplicate matrix rows, mismatched flags
or targets, inconsistent exact counts and changed controls fail the experiment.
The reused bench rejects unresolved code relocations, warnings, failures, stale
or missing objects and invalid symbol bounds. Input pins and freeze metadata
are checked again before aggregate publication. No padding or instructions are
trimmed, and no relocation word is ignored.

Every run gets a new ignored `build/source-hypotheses-*` directory. It retains
the original lower-level reports, derived metadata, objects, logs and aggregate
report. A failed experiment may retain completed individual cohort evidence,
but no successful aggregate report is published. Existing conflicting named
reports and input aliases are refused. Random build paths and timestamps are
excluded from the semantic aggregate, allowing direct repeat comparisons.

## What the experiment found

Both fresh experiments agree byte for byte. The new baseline cohort also equals
the complete accepted Bucket 3 report. Every unchanged control retained its
bytes. Each alternative's best whole-bench score remains **6/14**, and each
changed function remains nonexact in **all 88** build/setting combinations.

The guarded list version changes emitted bytes in 77/88 rows. At levels 1 and
2 it produces the intended guarded loop but has 40 bytes instead of the target's
36, including an extra `nop` before the backedge. The pointer-byte alternative
changes code in 88/88 rows and obtains pointer induction, while signed loop-limit
tests and conditional branches remain different from the target. Equal size in
some rows is not identity. See the reviewed instruction-level analysis in
[SOURCE_HYPOTHESES.md](SOURCE_HYPOTHESES.md).

The alternatives were not revised after seeing these results. No favorable
pieces from different source copies or settings were pooled into an uncompiled
combined score. The observed source effects are real; they do not establish the
original spelling, ownership, language or compiler settings, nor eliminate every
tested compiler as a possibility.

The current evidence does not justify a toolchain lock. Further work needs a new
reviewed plan rather than another implicit source/flag search. A useful next
direction is to reassess compiler attribution with the source held fixed: the
linked Metrowerks comment alone has not established the compiler of these
unclassified functions. No broader compiler-family test was performed here.
