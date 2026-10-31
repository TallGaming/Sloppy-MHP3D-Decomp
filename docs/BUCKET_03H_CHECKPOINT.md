> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3H checkpoint

2026-10-30. The approved fixed-language-mode experiment is complete.
**C and C++ both reproduce the same six of fourteen target intervals. Thirteen
function bodies are byte-identical across modes; one changes without becoming
exact. This does not identify the original game language or toolchain.**

## Controlled result

Both modes used the existing unmodified Metrowerks 3.0.1 build 219, the unchanged
original fourteen-probe source, and O2. Commands differed only in the language
operand and fresh output path:

```text
wibo mwccpsp.exe -nostdinc -lang c   -c -O2 -o OBJECT SOURCE
wibo mwccpsp.exe -nostdinc -lang c++ -c -O2 -o OBJECT SOURCE
```

All fourteen symbols in each configuration passed complete-function bounds,
uniqueness, section and relocation validation. No instruction trimming, ELF
renaming, source adaptation, wrapper, patch or pooled score was used.

| Probe | Target bytes | C bytes | C++ bytes | Exact in both | C/C++ body |
| --- | ---: | ---: | ---: | --- | --- |
| `probe_0883C4F8` | 16 | 16 | 16 | yes | same |
| `probe_0883C508` | 12 | 12 | 12 | yes | same |
| `probe_08826448` | 16 | 20 | 20 | no | same |
| `probe_0885691C` | 20 | 20 | 20 | yes | same |
| `probe_0885697C` | 16 | 16 | 16 | no | same |
| `probe_08856A14` | 12 | 12 | 12 | yes | same |
| `probe_0885BBFC` | 16 | 16 | 16 | yes | same |
| `probe_08860C9C` | 12 | 12 | 12 | yes | same |
| `probe_08830550` | 52 | 60 | 60 | no | same |
| `probe_08830654` | 36 | 36 | 36 | no | same |
| `probe_0882DA68` | 48 | 44 | 44 | no | same |
| `probe_0883E944` | 48 | 52 | 52 | no | same |
| `probe_08862434` | 72 | 44 | 48 | no | different |
| `probe_0886A58C` | 68 | 68 | 68 | no | same |

The range-check body at `0x08862434` gains `andi v0,v0,0xff` (word `0x304200FF`)
before return in C++ mode. That is a controlled language-mode effect in this
diagnostic. Its 48 bytes still differ from the complete 72-byte target.
None of the six larger probes becomes exact. Same-sized nonexact functions in
the table remain nonexact; size equality is not used as a match criterion.

Both objects retain flags `0x10970001` and the `MW MIPS C Compiler (3.0.0)`
comment. The linked target's metadata remains different and unresolved. No
linker or finalizer was run. These C-compatible isolated bodies do not recreate
class methods, inlining, headers or original translation-unit context, and
cannot confirm or refute C++ as the original language.

## Naming established before C++ target compilation

The invented fixture uses fourteen synthetic names and artificial records with
the required named-type/signature categories. Its bodies contain no target code.
Both reviewers checked the signatures and actual C/C++ object symbols before
the target profile was frozen. Exact observed suffixes were transferred to
paired canonical probe names; no aliases were selected from target-byte results.

The runner supplies those exact names to a derived manifest while leaving the
object and original manifest bytes unchanged. The existing strict comparator
still requires the complete expected function set. Reports retain both canonical
probe names and actual object symbols; missing or ambiguous symbols, unsupported
code relocations or compile failures leave the whole configuration unscored.

## Review artifacts and reproduction

| Artifact | Purpose |
| --- | --- |
| [language-modes.json](../config/language-modes.json) | Frozen commands, maps and input pins |
| [language-naming-fixture.json](../config/language-naming-fixture.json) / [language_mode_naming.c](../bench/language_mode_naming.c) | Invented naming/signature bindings |
| [bench_language_modes.py](../scripts/bench_language_modes.py) | Strict alias adapter, fresh compilation and report integrity |
| [LANGUAGE_MODE_REVIEW.md](LANGUAGE_MODE_REVIEW.md) | Independent naming/profile and final-byte review |
| [test_language_modes.py](../tests/test_language_modes.py) / [BUCKET_03H_VALIDATION_NOTES.md](BUCKET_03H_VALIDATION_NOTES.md) | Failure controls and independent repeat audit |

From `<project-root>`, use fresh report paths for repeat trials:

```powershell
python scripts/bench_language_modes.py --report evidence/bucket-03h/new-trial-1.json
python scripts/bench_language_modes.py --report evidence/bucket-03h/new-trial-2.json
wsl -d Ubuntu -- python3 -m unittest discover -s tests -v
```

The frozen profile is 3848 bytes, SHA-256
`d3c8b6b71710f390b545fec44f1d262d66814c4cec3841dc69057166dfab0a57`.
Both reviewers approved the exact draft before a status-only freeze. Its
historical no-prior-C++-scores declaration records that freeze point.
Naming evidence SHA-256 is
`c44419eca3863b92d50b2053b40aaae3249ae08c7ed84f5774c68e312dc3b7ba`.

The final reports `evidence/bucket-03h/final-language-run-{1,2}.json` are
byte-identical: 18386 bytes, SHA-256
`83b655d51ebb314bda5bdd1534d1a4d76c9af8c1e007d282ff8fa81df7b323af`.
Their fresh objects/logs are retained in `build/language-modes-ek4cadku` and
`build/language-modes-2578h52m`. Each C object exactly reproduces the earlier
accepted Bucket 3D O2 control object, SHA-256
`45d897dee18a5ddc6898a65d0963423dcb81ef2461d49808585c7b3a6f71473a`.
Each C++ object has SHA-256
`0631c7b22afb9f53a5fc057e9e158f3765ba4c0e2623f5ed7f51b96993b0585e`.

Independent audits rechecked all four final objects, 56 complete target
comparisons, 28 direct cross-mode comparisons, naming objects/maps and input
pins. Final diagnostics are empty. Earlier `language-run-*` preparation reports
have the same semantic content, but the final pair above is the checkpoint
evidence.

## Validation and integrity repair

All **226 tooling tests pass under WSL, with no skips**: 209 existing checks plus
17 new language-mode controls. They cover exact alias associations, raw-symbol
reporting, complete bytes/sizes, malformed/extra/missing symbols, unsupported
relocations, all-or-unscored configurations, compile failures/warnings/timeouts,
fresh repeats, changing pins, report preservation and cross-mode output mutation.

During validation, a mocked later compilation exposed a missing final check on
the earlier emitted object. The runner now rechecks every emitted object's bytes
after both invocations, including partial outputs from failed modes. This
integrity repair changed no compiler flags, source, mappings or score criteria.
The final real pair was freshly repeated with the hardened runner and reproduced
the initial semantic reports exactly.

Real report/input-alias and swapped-map controls each returned exit one before
creating a build directory or publishing a successful report. Inputs remained
intact. See `evidence/bucket-03h/verification-summary.json` and `tooling-tests.log`.
These controls are separate from the unimplemented full game's 18 negative tests.

## Decisions preserved

The clean PSP ULJM05800 v1.02 reference, readable-source-first rule, fixed
evidenced toolchain before matching, per-function flag prohibition, visible
parking and library-assembly policy remain unchanged. This investigation
selects no game-build language or settings. Matched/source-linked game functions,
parked functions and counted matching tricks remain zero. Full-game linking,
the complete gate, runtime testing and native-port implementation remain deferred.
Stop for user review; no further experiment or reconstruction is authorized.
