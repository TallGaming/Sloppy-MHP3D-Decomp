> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3F checkpoint

2026-10-30. The approved two-case SNC linker diagnosis is implemented.
**Both the default layout and minimal explicit layout raise an internal linker
exception in both fresh trials. No executable was produced.** This narrows the
failure conditions but does not establish a root cause or working toolchain.

## Controlled comparison

Each trial compiled the unchanged invented `compiler_family_smoke.c` once with
the existing SNC O0 profile. Both cases consumed that identical object, checked
before and after linking. The same unmodified `pspld` 2.7.63.0, native Windows
interop, entry symbol, comment preservation, trace/map and warning options were
used. Both reviewers approved the cases before any new link output.

| Case | Layout policy | Exit, both trials | Observed result |
| --- | --- | ---: | --- |
| Default layout | No `-T`; observe the linker's placement | 255 | Internal exception; partial map; no ELF |
| Minimal explicit layout | Four SNC payload-section clauses; text at `0x08804000` | 255 | Internal exception; partial map; no ELF |

The default partial maps place the 24-byte function at zero; the explicit maps
place it at `0x08804000`. Partial maps cannot validate an executable's entry,
instructions, load mappings, flags or comment propagation. No function-byte
preservation measurement after linking is available.

The larger Bucket 3E explicit script is therefore not required for this observed
failure. Removing it or replacing it with the minimal script did not yield a
successful link. These two cases do not isolate individual script clauses,
address effects, object features, host compatibility or the internal fault's
cause. They do not show that every SNC object or available linker is unusable.
The historical game's linker and source-unit compiler attribution remain open.

No case was adjusted after its result. Compiler flags, source, input headers,
all earlier layouts/profiles and accepted evidence remain unchanged. No SDK or
runtime library was requested, and no game binary was linked or executed.

## Reproduction and retained evidence

From `<project-root>`, run each trial with a fresh report path:

```powershell
python scripts/bench_linker_isolation.py --report evidence/bucket-03f/new-trial-1.json
python scripts/bench_linker_isolation.py --report evidence/bucket-03f/new-trial-2.json
wsl -d Ubuntu -- python3 -m unittest discover -s tests -v
```

| Artifact | Purpose |
| --- | --- |
| [linker-isolation.json](../config/linker-isolation.json) | Two frozen cases and inherited tool/input pins |
| [synthetic_link_minimal.ld](../bench/synthetic_link_minimal.ld) | Minimal explicit SNC-only diagnostic layout |
| [bench_linker_isolation.py](../scripts/bench_linker_isolation.py) | One immutable object per trial, two fresh case directories and strict validation |
| [LINKER_FAILURE_ISOLATION.md](LINKER_FAILURE_ISOLATION.md) | Independent provenance and failure interpretation |
| [test_linker_isolation.py](../tests/test_linker_isolation.py) | Invented isolation/failure controls |
| [BUCKET_03F_VALIDATION_NOTES.md](BUCKET_03F_VALIDATION_NOTES.md) | Independent repeat and integrity audit |

The frozen profile is 2033 bytes, SHA-256
`ddf78aa4d06d042e1a7f56765377e6e73b47c2931f6ed479536af280780e1f54`.
Its historical pre-output declaration records the freeze point. The minimal
layout is 306 bytes, SHA-256
`ff22d32c21f218aad04f04f78b8cfc355186c9ac62d9bfd6b420416e867a1f8d`.

Final reports `evidence/bucket-03f/isolation-run-{1,2}.json` are byte-identical:
3904 bytes, SHA-256
`bafda38fab6e86013a2c6e8f7f2ea18c0cc71ae49300b84ddddefbeca22ec81c`.
Their artifacts are in `build/linker-isolation-w8h8e0us` and
`build/linker-isolation-9stye3hw`. Each trial has one fresh object and two distinct
sets of link outputs/logs; there are four partial maps and no linked ELFs.

A copy of the shared crash dump was retained after the final trial, with its
identity and attribution limits in `evidence/bucket-03f/crash-artifact.json`.
Independent bounded reads found exception `0xC0000005`, a read at address
`0x1C`, with the faulting instruction inside `pspld.exe` at RVA `0x104A2`.
The extracted fields are in `evidence/bucket-03f/crash-summary.json`; schema
references and interpretation are in the provenance review. This is additional
diagnostic material, not proof of the exception context of every link attempt
or the root cause. No new link was run to regenerate it.

Real report/input-alias and wrong-layout-pin controls returned exit one, kept
inputs intact, created no compilation directory and published no successful
report. Records are in `evidence/bucket-03f/verification-summary.json`.

All **209 tooling tests pass under WSL with no skips**: 196 existing checks plus
13 new isolation tests. The new invented controls cover default-address
observation with strict mapping, the explicit base requirement, full-function
changes, exactly two reviewed cases, one compilation/shared object per trial,
fresh repeats, compiler/linker failures, input mutation, changing pins and report
preservation. They use mocked tools; their positive controls do not imply that
the real linker succeeded. The future game's 18 gate-negative checks remain
separate.

## Decisions preserved

The clean PSP ULJM05800 v1.02 reference, readable-source-first rule, fixed
compiler flags and library-assembly policy remain in force. The toolchain is
unlocked. Matched and source-linked game functions, parked functions and counted
matching tricks remain zero. The full game gate and its required 18 negative
checks remain unimplemented. Game execution and native-port implementation
remain deferred.

Stop for user review. Another linker experiment, tool, source/flag search or
reconstruction bucket requires its own approved plan.
