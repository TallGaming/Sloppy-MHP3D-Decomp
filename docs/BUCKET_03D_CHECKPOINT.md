> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3D checkpoint

2026-10-30. The approved fixed-source compiler-family comparison is implemented
and validated. **The results do not establish the original toolchain.** The user
accepted this checkpoint with "Ok". A separate synthetic link-stage plan is
proposed; reconstruction has not started.

## All declared outcomes

One selected PSP GCC candidate, one PSP SNC candidate and the existing
Metrowerks 219 control compiled the same unchanged fourteen probes. Each used
four independently reviewed, pre-frozen optimization configurations. A dash
below means the entire configuration is unscored, not zero exact probes.

| Setting | GCC 3.3.3 / catalogue 1.7.1 | SNC 1.2.7503.0 | Metrowerks 219 |
| --- | ---: | ---: | ---: |
| `-O0` | — unsupported code relocations | 0 / 14 | 1 / 14 |
| `-O1` | 0 / 14 | 0 / 14 | 6 / 14 |
| `-O2` | 1 / 14 | 0 / 14 | 6 / 14 |
| `-O3` | 0 / 14 | 0 / 14 | 1 / 14 |

All twelve configurations generated objects. Eleven completed strict validation
and full fourteen-function comparisons. GCC `-O0` has nine local section-symbol
`R_MIPS_26` relocations in code, which the existing comparator does not resolve.
It receives no score for any function. The three optimized GCC objects pass
the unchanged comparator and are reported as complete configurations.

The reporting unit was clarified during development, before optimized GCC scores
were read: an unsupported setting does not invalidate a different fully checked
fourteen-probe setting. Every declared failure/outcome remains visible. No
unsupported relocation, function or instruction was skipped to obtain a score.
Earlier development reports that quarantined the entire GCC family are
superseded by the final reviewed pair.

The lone GCC `-O2` exact probe is byte-copy/advance `0x08826448`, also exact under
the Metrowerks control at `-O3`; it is not unique family attribution. Metrowerks
reproduces the same six tiny level-1/2 sequences as before. None of the six
larger probes becomes exact. Sources, target manifest and existing flags were
not changed, and favorable configurations/functions were not pooled.

## Profiles and interpretation

Both new candidates were chosen before help or target scores. The GCC catalogue
identifier `1.7.1` describes a bundle identifying itself as
`3.3.3+allegrex-2.2.2-psp-1.7.1`. Its SDK driver has missing-specs warnings and
the bundle's assembler is empty. The reviewed diagnostic instead uses its
unmodified native backend with explicit pinned GNU assembly; byte-identical
Linux staging avoids the old backend's Windows-mount inode error. This is not
an original SDK driver/linker reconstruction. The fixed assembler preservation
mode was tested with an invented `nop` fixture before target scoring.

SNC's unmodified driver works through wibo with its recorded C defaults and
documented switches; GUI help remains unavailable. Metrowerks uses its existing
profile unchanged. All four control objects reproduce accepted Bucket 3 objects
and per-function comparisons exactly.

SNC's object flags numerically equal the linked executable's flags despite
zero exact probes here. Compiler comments, raw flags and linked-versus-object
metadata cannot establish which family produced each unclassified function.
Original language, ownership, unit context, compiler settings and the complete
assembler/linker chain remain unresolved. No historical or reproducible game
toolchain lock is proposed from this table.

## Review locations

| Artifact | Purpose |
| --- | --- |
| [COMPILER_FAMILY_COMPARISON.md](COMPILER_FAMILY_COMPARISON.md) | Reproduction, frozen pipelines, all outcomes and limitations |
| [COMPILER_ATTRIBUTION.md](COMPILER_ATTRIBUTION.md) | Primary evidence, raw metadata and instruction-level attribution caveats |
| [compiler-families.json](../config/compiler-families.json) | Profile freeze, candidate/subtool/host dependency pins and help evidence |
| [bench_compiler_families.py](../scripts/bench_compiler_families.py) | Native staging, explicit execution, per-configuration rejection and comparisons |
| [compiler_family_smoke.c](../bench/compiler_family_smoke.c) | Invented availability fixture; not another game probe |
| [test_compiler_families.py](../tests/test_compiler_families.py) / [BUCKET_03D_VALIDATION_NOTES.md](BUCKET_03D_VALIDATION_NOTES.md) | Format, execution, integrity/failure checks and independent audit |

The profile freeze was independently approved before target compilation:
SHA-256 `cb0b3fbd1961380c8cee61a286bce723be7ed13c73e39bd8c949e6c701413dab`.
Its historical no-prior-scores declaration remains immutable. All original probe
sources, Bucket 3C alternatives, prior compiler configuration and reference
identities remain unchanged.

## Validation performed

- **174 tooling tests passed under WSL, with no skips**: 150 existing plus
  24 new checks. These cover ELF/symbol assumptions, local section relocation
  rejection, exact profile scope, missing/stale/failed/warning outputs, timeouts,
  source/assembly modification, changed pins, report preservation and the rule
  that a rejected configuration publishes no partial function score.
- Both complete investigations generated twelve objects and eleven scored
  configurations: 24 objects and 308 published full-function comparisons.
  Independent validation read every object/comparison, both GCC `-O0` local
  relocation sets and all twelve declared outcomes per run.
- The two reports are directly byte-identical: 79,888 bytes, SHA-256
  `207ca372b08148174434555111886a0d48cf20e74fa95a278add8c0596b745b2`.
- Independent audit verified 184 local pin records and eleven native dependency/
  tool records. No source, profile, compiler binary or licensing mechanism was
  modified in response to scores.
- Real report/input-alias and wrong-source-pin controls returned exit 1,
  preserved the inputs and published no success report. The wrong pin failed
  before creating a compilation directory.

Final local ignored evidence is under `evidence/bucket-03d/`:
`final-reviewed-family-run-1.json`, `final-reviewed-family-run-2.json`, their
logs, `verification-summary.json`, `tooling-tests.log`, help/preparation logs
and the assembler preservation fixture. The summary locates both retained
fresh build roots. Earlier preparation/old-report-policy runs are not the final
checkpoint evidence.

## Decisions preserved

The clean PSP v1.02 target, readable-source-first rule, fixed-toolchain
requirement, library-assembly policy and all-game-matching-before-port sequence
remain unchanged. No original game source is integrated or credited. Matched/
source-linked game functions and matching trick/parking counts remain zero.
The full byte-match gate and its 18 negative checks remain unimplemented; these
174 tooling tests are separate. No game runtime test, additional overlay
recovery, reconstruction, port implementation, commit or verified tag occurred.

Review this bucket, request changes, or stop. Further relocation support,
compiler options, source/type hypotheses or build-stage experiments require a
new concrete plan and review. Do not infer a toolchain choice from the largest
small-probe score or move silently into Bucket 4.
