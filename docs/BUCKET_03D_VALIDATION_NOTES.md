> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3D independent validation notes

The validation helper independently reviewed the bounded candidate selection and
local archives before target scoring. This is compiler-family investigation,
not game-source integration, matching credit, runtime testing or a toolchain lock.
No commits were made.

## Selection and archive review

The pre-help selection record names only `psp-gcc-1.7.1` and
`pspsnc_1.2.7503.0`, plus existing Metrowerks build 219 as the control. It pins
catalogue commit `c5f041cdc9610fb5213b7ae3c88cce02f554c4d3` and prohibits silent
candidate substitution. The original fourteen-probe source is required; the two
Bucket 3C alternatives are outside this comparison.

Read-only archive inspection confirmed:

| Candidate archive | Size | SHA-256 |
| --- | ---: | --- |
| `psp-gcc-1.7.1.tar.gz` | 7412657 | `55d4267b1d74855157501d5fd61ed31b68d961a737306b5831b582a2d58f3484` |
| `pspsnc_1.2.7503.0.tar.gz` | 6823980 | `0d10a4b387e45b62369eea21b6693fc5517335033bf65e65aa7b543a916f4d6d` |

The GCC archive contains 144 files, no symlinks and seven zero-byte placeholders,
including its `as` and `ld`. It contains real ELF driver/backend binaries; the
backend path names GCC `3.3.3+allegrex-2.2.2-psp-1.7.1`, also reported in the
recorded version output. The catalogue identifier is not the underlying GCC
version. The driver reports missing PSP specs/postprocessing tools; they must
not be silently substituted with dummy files or hidden fallbacks.

The SNC archive contains 21 files, no symlinks or empty files, and separate PE
driver/frontend/backend/assembler tools plus support DLLs. Recorded help
documents optimization levels 0 through 5, compile-to-object mode and GP-size
control. Only the declared levels 0 through 3 belong to this experiment.

## Profile review and validation

The independent pre-score review approved pending-profile SHA-256
`bb7fd95b18f22ea316c2d71fb60e3e73b82e7730fc73245a8c3b955bc58cb64f`
for a status-only transition to the final freeze. All 184 local pin records
(181 unique files) and eleven native Linux tool/dependency files matched their
size and SHA-256 pins before target scoring. Exactly the original source,
manifest, reference and accepted Metrowerks configuration are pinned.

The reviewed whole-bench modes are:

- GCC's unmodified bundled C backend, explicit Allegrex/EABI/little-endian/G0
  switches derived from its bundled specs, and a separately pinned modern GNU
  assembler. Exact source bytes retain the original filename in native Linux
  temporary staging, avoiding the old backend's DrvFS stat/inode failure.
  The incomplete SDK driver is not used. This is a diagnostic backend/assembler
  combination, not an authenticated historical SDK pipeline.
- SNC's unmodified driver and complete supplied subtool/DLL bundle through the
  pinned wibo runner, using `-c -G0`, C selected by the `.c` source extension and
  the recorded command trace. Unsupported GUI help is disclosed; no undocumented
  header-search switch is invented for the header-free source.
- Existing Metrowerks build 219 with its unchanged `-nostdinc -lang c -c` control
  profile and pinned compiler/support DLL/wibo.

Each family has only four whole-bench optimization levels, O0 through O3. These
names do not assert equivalent optimizations across families. GCC's assembler
uses one fixed O0 preservation mode, not compiler delay-slot suppression. The
validator independently read assembler help and checked its invented fixture:
all four declared words, including three explicit NOPs, remain within the exact
16-byte function symbol. No instruction is removed from subsequent comparisons.

The final freeze is 46770 bytes, SHA-256
`cb0b3fbd1961380c8cee61a286bce723be7ed13c73e39bd8c949e6c701413dab`.
Before approving target execution, the validator reconstructed the earlier
pending bytes by restoring its status and LF serialization; this exactly
reproduced the approved pending hash. Thus only freeze status and line endings
changed, with no profile/source/flag/tool change. The frozen
`no_target_scores_observed` field describes that historical pre-score review;
it is not a statement that the completed experiment has no results.

No target bench was executed by the validation helper.

## Automated checks

From `<project-root>`:

```powershell
wsl -d Ubuntu -- python3 -m unittest discover -s tests -v
```

Result: **174 tests passed** (exit 0, no skips): all 150 existing checks and 24
new family checks. The new checks comprise nine object-format controls, thirteen
family-runner controls and two native Linux staging controls. Fixtures contain
invented sources, objects and tool bytes. Compiler/assembler subprocesses are
mocked; no real target compilation occurs in these tests.

The new checks cover:

- Complete indexed function extents in a shared `.text` section with alignment
  gaps and non-code `.pdr` metadata. Extra bytes inside a function are not trimmed;
  zero-sized symbols are not inferred from the next symbol or section end.
- Unsupported endianness/machine/file type, overlapping or duplicate symbols,
  malformed metadata relocation indices/bounds, and every code relocation fail.
  A local STT_SECTION `R_MIPS_26` is explicitly rejected rather than sent to the
  earlier external-JAL resolver. Object flags remain metadata, not an attribution
  shortcut or a forced equality condition with the linked executable.
- Fixed four-level profiles, unique declared IDs, pre-score freeze state, input/
  compiler/subtool/assembler/runner/host dependency pins and explicit absolute
  timeout selection. Missing pins cannot silently select PATH tools.
- Fresh objects and repeatable path-free reports; invalid objects, warnings,
  failure, timeout or unsupported relocations withhold the entire affected
  configuration's score. All four declared outcomes remain visible, while other
  complete full-probe configurations remain reportable. An entirely unavailable
  family gets no zero score or invented function comparisons.
- Global input/pin/freeze changes invalidate the whole report. Report aliases
  and conflicting evidence preserve existing files.
- Native GCC staging preserves exact source bytes and basename; the pinned
  compiler, assembler and timeout paths are explicit. Post-assembler changes to
  either staged source or assembly are detected, and the original source remains
  unchanged. The driver wrapper uses empty stdin and bounded subprocess timeouts.

Review prompted checking staged source and assembly again after the assembler;
that protection is present and tested. After discovering GCC O0's unsupported
relocations, and before the primary or validator read optimized GCC target
scores, reporting was corrected to retain all complete configurations alongside
every rejected outcome. The earlier whole-family quarantine would have hidden
valid configurations. No frozen source, profile, flag or comparator changed.

The reporting unit is a complete fourteen-probe configuration: a rejected level
cannot publish favorable partial function scores, while fully validated levels
stay visible beside its failure. This separates comparison support from whether
a compiler itself can execute. Global pin failures remain fatal. These are
tooling tests, not the matching gate's eighteen future negative checks.

## Independent audit of final repeat runs

The authoritative reports are
`evidence/bucket-03d/final-reviewed-family-run-1.json` and
`final-reviewed-family-run-2.json`. They are byte-identical: 79888 bytes,
SHA-256 `207ca372b08148174434555111886a0d48cf20e74fa95a278add8c0596b745b2`.
Their object/report directories are:

- `build/compiler-families-ccyz2g6z/`
- `build/compiler-families-uqp5ae_2/`

The validator independently read all **24 objects and 308 published function
comparisons**. Every reported object/function hash, complete symbol size, target
hash, exact boolean, first differing byte and exact count agrees with the actual
object and pinned reference. Every published row uses its frozen family flags
and assembler profile. All four settings were attempted for each family in both
runs: twelve declared outcomes per run, eleven complete comparison rows and one
explicitly rejected configuration.

| Setting | GCC diagnostic pipeline | SNC | Metrowerks 219 control |
| --- | --- | ---: | ---: |
| O0 | Unsupported code relocations; no score | 0/14 | 1/14 |
| O1 | 0/14 | 0/14 | 6/14 |
| O2 | 1/14 | 0/14 | 6/14 |
| O3 | 0/14 | 0/14 | 1/14 |

Both GCC O0 objects contain nine code `R_MIPS_26` relocations against local
STT_SECTION symbols. The validator checked those records directly. This form
requires different handling from the external undefined-global JAL diagnostic;
no words were masked, ignored or resolved speculatively. O0 publishes no score
or partial function comparisons. O1/O2/O3 contain no such code relocations and
pass the unchanged complete-symbol comparator. GCC therefore compiled all four
levels but has an incomplete comparison profile, not a nonworking compiler.

Metrowerks control function comparisons equal the previously accepted build-219
results at the same four levels. No favorable settings or source alternatives
are pooled into a new whole-project configuration. `matched_progress` stays zero.

All 184 local pin records and eleven native dependencies/tools were independently
rechecked after the final runs. The original source/manifest/accepted candidate
configuration remain pinned and unchanged, as do both unused Bucket 3C source
alternatives. The reference ELF also retains its pinned identity.

## Metadata and conclusions

The observed object flags are GCC `0x10843001`, SNC `0x10A23001` and Metrowerks
`0x10970001`. SNC's numeric flags agree with the linked target, but its tested
objects have no `.comment` compiler strings; Metrowerks objects contain
`MW MIPS C Compiler (3.0.0)`. These are different-stage observations alongside
the target's linked Metrowerks-looking banner. Neither flags nor tiny probe
scores establish the historical compiler, original source, language or ownership.

Reviewed implementation identities:

| File | SHA-256 |
| --- | --- |
| `scripts/bench_compiler_families.py` | `d91b2e3b77f627527997ca50922d069afd9d1b0dff5e0b26ae230831894b8510` |
| `tests/test_compiler_families.py` | `e345f9e6ee0073311ee47045dec73f37dbd87eba6b0bf1aaf4aeb2023c4ea0e3` |
| `config/compiler-families.json` | `cb0b3fbd1961380c8cee61a286bce723be7ed13c73e39bd8c949e6c701413dab` |

No material blocker remains in the reviewed diagnostic paths. The GCC O0
comparison limitation is explicit. No new relocation support, source edits,
compiler-flag sweep, game integration, library classification, runtime test or
match credit was introduced. A complete game build chain remains unestablished;
further investigation needs the next separately reviewed bucket.
