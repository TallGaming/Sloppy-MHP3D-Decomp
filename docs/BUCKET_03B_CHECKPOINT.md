> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3B checkpoint

2026-10-30. The approved Ghidra setup, two-probe diagnosis and controlled
direct-call diagnostic are implemented and validated. The user accepted this
checkpoint with "Ok". The game toolchain remains unlocked; reconstruction has
not started. A bounded follow-up experiment is proposed separately.

## Result

Ghidra is useful here: its PSP import and selected decompilations cross-check
our static understanding and caller context. It does not recover original
declarations or explain the original compiler settings automatically.

- Pinned Ghidra 12.2, Allegrex extension 21.5 and portable Temurin JDK 25.0.5+8
  are installed locally. The tested interface is headless analysis under WSL
  Ubuntu; a native Windows GUI installation is not configured/tested.
- Two fresh saved projects import the same verified ELF using the PSP loader,
  `Allegrex:LE:32:default` and base `0x08804000`. Their exports are byte-identical.
  All 34 selected target/caller/neighbor decompilations completed.
- Both target memory hashes and exact 52/36-byte function bodies agree with
  the frozen bench. Ghidra identifies the same 34 direct reduction calls in
  26 callers and the list-count helper's one direct caller.
- The 36-byte list-count probe differs from every tested level-1/2 object in
  exactly **one instruction at offset 4**, governing loop entry. The reduction
  probe has wider induction/comparison/conditional-assignment differences.
- Neighbor/caller/import evidence places the code in a MAC-address/adhoc-peer
  context. The Sony imports are identified; ownership of the local wrappers
  remains unclassified. No original C/C++ declaration is established.
- A separate invented direct-call fixture emits ordinary external `R_MIPS_26`
  REL/JAL calls across all eleven compilers. The narrow resolver changes only
  the declared call word and validates explicit addresses/addends. Non-code
  `.mwcats` relocation metadata is reported unapplied. This is not an object linker.

The fourteen original game probes, their manifest and candidate flags remain
unchanged. No source permutation, new game configuration, matching trick or
additional overlay was introduced. The fixture's fixed `-O2` configuration is
solely a diagnostic and does not select game flags.

## Review locations

| Artifact | Purpose |
| --- | --- |
| [GHIDRA_ANALYSIS.md](GHIDRA_ANALYSIS.md) | Setup identities, reproduction, saved project locations and limitations |
| [analysis-tools.json](../config/analysis-tools.json) | Archive, installed-manifest, runtime and export-script pins |
| [analyze_reference.py](../scripts/analyze_reference.py) / [ExportProbeAnalysis.java](../scripts/ghidra/ExportProbeAnalysis.java) | Fresh import, bounded export, memory/caller checks and preservation |
| [PROBE_MISMATCH_DIAGNOSIS.md](PROBE_MISMATCH_DIAGNOSIS.md) | Instruction differences, caller context and inference limits |
| [CALL_RELOCATION.md](CALL_RELOCATION.md) | Actual emitted form, supported arithmetic and exclusions |
| [direct_call_fixture.c](../bench/direct_call_fixture.c) / [direct-call-fixture.json](../config/direct-call-fixture.json) | Invented fixture and fixed diagnostic plan |
| [call_relocation.py](../scripts/call_relocation.py) / [bench_direct_call.py](../scripts/bench_direct_call.py) | Narrow resolver and fresh candidate runs |
| [test_call_relocation.py](../tests/test_call_relocation.py) / [BUCKET_03B_VALIDATION_NOTES.md](BUCKET_03B_VALIDATION_NOTES.md) | Synthetic controls and independent audit |

## Validation performed

**130 tooling tests passed**: the previous 95 plus 35 new checks (19 relocation,
11 fixture-runner and 5 Ghidra-export validation). These are separate from the
future matching gate's 18 negative checks.

| Repeated output | Size | SHA-256 |
| --- | ---: | --- |
| Ghidra selected-analysis export | 68,494 | `a2957127574e6791345caee470056ca1a64a7fe218335492ee4f291e3db8a091` |
| Ghidra verification summary | 2,287 | `0dab17818765568f1140f50920cafd2daedcd9eadb1518eae747495e47c416f1` |
| Eleven-candidate direct-call report | 9,867 | `5e99ad0c3ab2eef48313f9b8f0420a6eaedf769f53b05307a208a20de129c463` |

Each pair is directly byte-identical. Independent validation checked both
Ghidra exports against actual ELF instructions and both targets/callers, all
22 fixture objects/resolved outputs, 5,751 installed tool files/links, three
archives, script pins and report provenance. Current validation also requires
caller bodies to contain their reported sites and decompilation to complete.
The original executable remains hash-identical after analysis.

Real existing-analysis-path and fixture-report/input-alias controls returned
exit 1 and preserved the earlier artifacts/inputs. Final evidence is in ignored
`evidence/bucket-03b/verification-summary.json`, `tooling-tests.log`,
`ghidra-final-run-{1,2}.json`, their `-summary.json` and log files, and
`final-call-run-{1,2}.json`. The two saved projects are
`reference/ghidra/final-run-1/mhp3rd.gpr` and `final-run-2/mhp3rd.gpr`, each
with its companion `.rep` directory. Database files themselves are not claimed
byte-identical; timestamps/caches are not matching targets.

## Limits and decisions preserved

Ghidra's automatic types/signatures remain hypotheses. Some caller pseudocode
omits an `a0` argument seen in assembly. Its workspace omits runtime reservation
blocks/actual overlay payloads; inherited executable flags on data do not prove
code. Auto-analysis warnings involve unloaded overlay targets and an uninitialized
address. Completed selected analysis is not whole-program or runtime validation.

Only the actual external zero-addend call form was emitted by this fixture;
nonzero addends and address-boundary cases were exercised with invented ABI
vectors. Other code relocations, local/weak/section symbols and full linking
remain unsupported. The frozen game bench still rejects unresolved code
relocations. No original game code was relocated by this diagnostic.

The PSP v1.02 baseline, readable-source-first rule, fixed-toolchain requirement,
library-assembly policy and matching-before-port sequence remain unchanged.
Matched/source-linked game functions and matching trick/parking counts remain
zero. The full byte-match gate and its 18 checks remain unimplemented. No game
runtime test, reconstruction, native-port work, commit or verified tag occurred.

The findings justify more precise source/control-flow hypotheses, but no compiler
build or flags can be locked from this evidence. Review this bucket, request
changes, or stop. If accepted, present a small follow-up source-hypothesis/compiler
experiment before implementation; retain the frozen baseline and apply every
declared configuration consistently. Acceptance does not authorize Bucket 4.
