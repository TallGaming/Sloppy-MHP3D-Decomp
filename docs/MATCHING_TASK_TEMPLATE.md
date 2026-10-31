# Matching task record template

Copy this into a task/issue or PR description; it is a template, not an active
claim on a function. Follow the [matching guide](MATCHING_GUIDE.md). Do not paste
original game bytes, disassembly, private logs, keys or proprietary tools here.

## Identity and scope

- Task/issue, contributor and coordination status:
- Planned bucket and review checkpoint:
- Target version and local reference identity:
- Module/overlay identity and load context:
- Analysis name; whether an original name is known:
- Address interval, exclusive end, local file mapping:
- Complete original interval size/SHA256 and boundary evidence:
- Ownership classification, evidence and uncertainty:
- Related types/callees/source units; assumptions still open:
- Existing source attempts/parked history, if any:

## Fixed inputs and hypothesis

- Locked pipeline/profile identity, or explicitly DIAGNOSTIC/unlocked:
- Tool versions/hashes and exact commands:
- Source path/size/SHA256; relevant headers/config identities:
- Plain-source hypothesis and behavior description:
- Expected observation and stopping rule:

## Attempt log

| Attempt | Category: plain / documented shape / repeat | Source identity | Hypothesis/change | Complete result | Time |
| --- | --- | --- | --- | --- | --- |
| Fill in | Fill in | Fill in | Fill in | Size/hash/exactness or failure | Fill in |

Record failed attempts too. Separate source changes from compiler-setting
diagnostics; never tune settings per game function or restart a parked budget.

## Validation and disposition

- Complete object/function comparison; relocation/link handling:
- Fresh source-to-object-to-target participation proof, or unavailable:
- Full clean game-gate command/result, or NOT IMPLEMENTED/unavailable:
- Eighteen negative-check command/results, or NOT IMPLEMENTED/unavailable:
- Other tooling/runtime checks actually performed, with scope and skips:
- Changes to register-pin, empty-asm-line and commented-shape-function totals:
- Assembly manifest/layout/status records changed:
- Remaining mismatches, uncertainties and best retained draft:
- Proposed status: diagnostic / parked / ready for integrated review:
- Maintainer decision and next checkpoint:

An exact isolated body is still diagnostic. Match credit requires reviewed
readable source, source participation, the complete clean build and its gate
checks. A parked task remains unfinished and visible in HANDOFF.
