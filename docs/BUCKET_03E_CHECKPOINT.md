> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3E checkpoint

2026-10-30. The approved synthetic link-stage experiment has reached its review
checkpoint. **All three links failed under the frozen shared profile. No linked
executable was produced, so the experiment does not resolve metadata provenance
or establish a toolchain lock.** Further experiments require a separate plan.

## Declared outcomes

Every trial freshly compiled the unchanged invented `compiler_family_smoke.c`
using the three existing family profiles at O0. Both reviewers approved the same
entry, layout and command before any link output. The only subsequent profile
change was its status from draft to frozen.

| Input compiler | Complete function | Link exit | Observed result |
| --- | ---: | ---: | --- |
| GCC 3.3.3 / catalogue 1.7.1 | 44 bytes | 255 | Internal linker exception; partial map, no ELF |
| SNC 1.2.7503.0 | 24 bytes | 255 | Internal linker exception; partial map, no ELF |
| Metrowerks 3.0.1 build 219 | 28 bytes | 1 | Internal zero-section-alignment error; no map or ELF |

The same unmodified SNC `pspld` 2.7.63.0 handled all three inputs. Its documented
options explicitly retained comments, selected `family_smoke`, requested a map
and file trace, and treated warnings as errors. One invented script placed text
at `0x08804000` and retained compiler metadata. No libraries, stripping, input
header changes or family-specific adjustments were introduced after failures.

The GCC and SNC partial maps place the function at the intended address, but a
partial map cannot validate an executable entry, stored instruction bytes,
segment mapping, flags or comment propagation. The Metrowerks diagnostic does
not identify the offending section. These failures describe this exact linker,
host, input and script combination; they do not establish that a compiler
family or every object from it is incompatible with the linker.

## Reproduction and evidence

From `<project-root>`, run:

```powershell
python scripts/bench_synthetic_link.py --report evidence/bucket-03e/new-trial.json
wsl -d Ubuntu -- python3 -m unittest discover -s tests -v
```

The script uses WSL for the unchanged compiler profiles and native Windows
interop for the existing linker. Wibo could print help through a terminal but
did not complete reliably; the native invocation was selected before linking.
The five recorded SysWOW64 dependency pins and Windows build describe a limited
host dependency scope, not a complete Windows installation snapshot.

| Artifact | Purpose |
| --- | --- |
| [synthetic-link.json](../config/synthetic-link.json) | Frozen inputs, linker, host dependency scope and exact command |
| [synthetic_link.ld](../bench/synthetic_link.ld) | Single shared invented layout |
| [bench_synthetic_link.py](../scripts/bench_synthetic_link.py) | Fresh builds, bounded ELF checks and explicit failure reporting |
| [LINK_STAGE_PROVENANCE.md](LINK_STAGE_PROVENANCE.md) | Independent pre-link review and metadata interpretation |
| [test_synthetic_link.py](../tests/test_synthetic_link.py) | Invented format and failure controls |
| [BUCKET_03E_VALIDATION_NOTES.md](BUCKET_03E_VALIDATION_NOTES.md) | Independent validation and repeat audit |

The frozen profile is 3423 bytes, SHA-256
`dc0017e2a922011fa51c59ab477baab74d805481d6ec56e53ff156b0da31094f`.
The source, layout, original compiler-family profiles and compiler flags stayed
unchanged. The historical `no_link_outputs_observed` declaration records the
freeze point; it is not a live statement after execution.

The final reports, `evidence/bucket-03e/final-link-run-{1,2}.json`, are directly
byte-identical: 13377 bytes, SHA-256
`fbe206a40ae6f4efcaf9e91c54faa7281c7648bc84d4931289e76945d4338af7`.
Fresh artifacts are retained in `build/synthetic-link-4cs9z75u` and
`build/synthetic-link-sepjo2c6`. Earlier pre-link inventory and the initial trial
remain preparation evidence, separate from this final pair.

Real report/input-alias and wrong-source-pin controls both returned exit 1,
preserved inputs, created no compilation directory and published no successful
report. See `evidence/bucket-03e/verification-summary.json`. The driver completing
an investigation with explicit failed rows is not a successful link.

All **196 tooling tests pass under WSL, with no skips**: 174 existing checks plus
22 new synthetic-link tests. The new controls cover complete function extents,
metadata changes without code changes, malformed symbols/relocations, entry and
section/load mappings, partial overlaps, failed/warning/missing/stale outputs,
timeouts, input mutation, changed pins, report preservation and fresh repeat
builds. These use invented fixtures and mocked tool execution; they are separate
from real repeated trials and from the future game's 18 gate-negative checks.

## Decisions preserved

The reference remains clean PSP ULJM05800 v1.02. Readable source comes first;
per-function compiler-flag changes remain forbidden. SDK and positively
identified third-party code stays labeled assembly. No game source was linked,
no game was executed and native-port implementation remains deferred until all
game code matches.

Matched functions, source-linked game functions, parked functions and counted
matching tricks remain zero. The complete game-build gate and its required 18
negative checks remain unimplemented. GCC's earlier game-probe O0 relocation
limitation remains unresolved and unscored. Stop here for user review; this
checkpoint does not authorize another linker profile, wider investigation or
Bucket 4.
