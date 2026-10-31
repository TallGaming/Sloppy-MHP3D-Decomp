> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Fixed-source compiler-family comparison

Bucket 3D compares one PSP GCC candidate, one PSP SNC candidate and the existing
Metrowerks 219 control. The original fourteen-probe source and target manifest
are unchanged. The two Bucket 3C alternatives are not part of this score table.
This investigation does not select the historical compiler or a game toolchain.

## Reproduce

From `<project-root>` in PowerShell, using fresh project-relative report names:

```powershell
python scripts/bench_compiler_families.py --report evidence/bucket-03d/my-family-review.json
wsl -d Ubuntu -- python3 -m unittest discover -s tests -v
```

The wrapper launches the same script under WSL Ubuntu. Its
[compiler-families.json](../config/compiler-families.json) profile freeze is
46,770 bytes, SHA-256
`cb0b3fbd1961380c8cee61a286bce723be7ed13c73e39bd8c949e6c701413dab`.
It was independently approved before target scoring. The immutable
`no_target_scores_observed: true` field describes that historical freeze point;
it is not a claim that later reports contain no scores.

Each run creates an ignored `build/compiler-families-*` directory with every
object, per-setting diagnostics and a semantic report. Existing conflicting
reports and input aliases are refused. The driver verifies source, manifest,
reference, candidate/support binaries, archives, host dependencies and frozen
metadata before and after execution. The original compiler configuration and
all three frozen C source files remain unchanged.

## Reviewed profiles and preparation limits

| Family | Exact tested candidate | Compilation path |
| --- | --- | --- |
| GCC | Catalogue `psp-gcc-1.7.1`, identifying itself as GCC `3.3.3+allegrex-2.2.2-psp-1.7.1` | Bundled native Linux `cc1`, then explicit pinned GNU MIPS assembler |
| SNC | `pspsnc 1.2.7503.0` | Unmodified driver and its bundled `pspcq`/`pspas` stages through pinned wibo |
| Metrowerks | `3.0.1 build 219` | Existing unmodified compiler/DLL through the same pinned wibo |

The new candidates were selected before help, object generation or scores from
the [pinned public catalogue](https://github.com/decompme/compilers/tree/c5f041cdc9610fb5213b7ae3c88cce02f554c4d3/platforms/psp).
The higher available GCC catalogue identifier was chosen; it was not assumed to
be the underlying GCC version. No second candidate was substituted for a result.

GCC's bundle contains an empty assembler placeholder, and its SDK driver warns
about absent `pspspecs`/related link utilities. No dummy SDK files or modified
driver were used. The reviewed diagnostic invokes the supplied backend directly
with `-quiet -nostdinc -G 0 -march=allegrex -mtune=allegrex -mel -mabi=eabi`.
Those target defaults are supported by the bundled specs/help. The source is
header-free and has no conditional preprocessor code needing driver macros.
The old 32-bit backend cannot stat the Windows mount reliably, so an exact-byte
copy with the original basename is staged on native Linux `/tmp`; both source
and emitted assembly are checked for changes through the assembler stage.

The explicit assembler is GNU Binutils `2.45.90.20260125`, configured for
`mips-linux-gnu`, using fixed `-EL -march=allegrex -mabi=eabi -G0 -O0`.
Its `-O0` is assembly preservation, not the backend optimization level and not
a compiler delay-slot-disabling option. An invented four-word fixture confirms
that three explicit `nop` instructions are preserved. This modern assembler
pipeline is not the original SDK driver/assembler or an established game build.

SNC uses documented `-c -G0` and its `.c` language default, observed in the
invented-fixture driver trace. Its GUI help topics fail under wibo; the short
CLI help and actual subtool trace establish the switches used. No undocumented
include-suppression switch was added, and default SDK include paths are unused
by this source. Metrowerks retains its old `-nostdinc -lang c -c` profile.

Every profile receives exactly `-O0`, `-O1`, `-O2` and `-O3` in separate whole-
bench compilations. These names do not imply equivalent transformations across
families. No per-function flags, extra settings, source edits, instruction
trimming or alternate compiler candidates were introduced after the freeze.

## All declared outcomes

Each numeric entry below is a complete fourteen-function comparison. A dash
means no score, not zero exact functions.

| Optimization | GCC | SNC | Metrowerks control |
| --- | ---: | ---: | ---: |
| `-O0` | — unsupported code relocations | 0 / 14 | 1 / 14 |
| `-O1` | 0 / 14 | 0 / 14 | 6 / 14 |
| `-O2` | 1 / 14 | 0 / 14 | 6 / 14 |
| `-O3` | 0 / 14 | 0 / 14 | 1 / 14 |

All twelve configurations were attempted; eleven passed complete object/symbol/
relocation validation. GCC `-O0` generates an object with nine local section-
symbol `R_MIPS_26` relocations in code. The existing comparator deliberately
rejects them. The external-global/JAL resolver from Bucket 3B does not cover
this local form, so no affected words were ignored or treated as equal.
No score is reported for the entire `-O0` configuration, including its simpler
functions. The other three GCC configurations pass the unmodified full-symbol
checks and can be reported independently.

The reporting unit was corrected during development: an initial family-wide
quarantine would have hidden these three valid configurations. Before either
reviewer read their optimized target scores, the policy was corrected to report
all declared outcomes, with scores only for complete configurations. Inputs,
profile flags and comparator checks stayed frozen. Earlier development reports
are superseded by `final-reviewed-family-run-{1,2}.json`.

The GCC `-O2` exact sequence is the byte-copy/advance probe `0x08826448`, also
exact under Metrowerks `-O3`; this is not unique compiler attribution. The six
Metrowerks level-1/2 sequences are the same tiny controls as before. None of the
six larger probes becomes exact. Favorable functions/settings were not pooled
into a synthetic family score or an uncompiled mixed-source result.

## Evidence and interpretation

Two complete runs produce twelve objects each and eleven scored configurations
each: 24 objects and 308 published full-function comparisons. The two reports
are byte-identical: 79,888 bytes, SHA-256
`207ca372b08148174434555111886a0d48cf20e74fa95a278add8c0596b745b2`.
All four Metrowerks objects and their per-function comparisons reproduce the
accepted control exactly. Independent validation and test coverage are recorded
in [BUCKET_03D_VALIDATION_NOTES.md](BUCKET_03D_VALIDATION_NOTES.md).

[COMPILER_ATTRIBUTION.md](COMPILER_ATTRIBUTION.md) compares metadata and actual
instruction differences. SNC objects have the same numeric flags as the linked
target yet no exact probes in these profiles. The linked Metrowerks-looking
comment, object comments and differing platform flag conventions do not prove
which compiler produced every unclassified interval. Original language, unit
context, ownership, settings and the full assembler/linker chain remain open.

These results do not justify a toolchain lock or a further implicit flag sweep.
GCC's unscored local relocation form needs a separately reviewed implementation
if pursued; it is not a reason to weaken comparison. Stronger original-unit/
type/build-stage evidence is also needed before converting a probe score into
a project configuration. No game matching, reconstruction or runtime credit is
claimed.
