> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Metrowerks archive-candidate version review

Bucket 3L tests the unchanged 3I C++ archive-key candidate against the eleven
already pinned unmodified PSP Metrowerks 3.0.1 builds. This independent review
downloads no tools and invokes no compiler, assembler or linker. It changes no
source, field qualifier, symbol mapping, comparator or earlier profile.

## Inherited source and target

| Input | Bytes | SHA-256 |
| --- | --- | --- |
| `bench/archive_key_initializer.cpp` | 1806 | `6c4be341bcc3f113b56ccf7494a7b624a550b52f89c9c827eacbbce56e1f71d3` |
| `config/archive-key-probe.json` | 883 | `bcb2a3b159f2ce1f3d6fba2ff9f2d668dade818efab8d79bb4fe6656846bea84` |
| `config/archive-key-experiment.json` | 1902 | `30b5372dab0d1e2fb9dc0ec4436ca0e78af1922728c5a421499a66e2a4cc5188` |
| `config/compiler-candidates.json` | 12142 | `9ba0d75472c7a1ceb45ffdbc46c50d3ffa119c3315be0e93c2f9f8ada4099147` |

The complete target remains **[0x0886233C, 0x08862380)**, 68 bytes,
SHA-256 `7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57`.
The exact object name remains `initialize_key__17ArchiveKeyContextFUi`, bound by
3I's invented naming evidence. An older compiler producing a different name
must be rejected rather than matched through a discovered alias.

The candidate's partial receiver type and volatile fields remain explicitly
declared source hypotheses. This bucket adds no new source attempt. The prior
build-219 control produced a complete 100-byte function, SHA-256
`193c361fab07498ef61aa22bfa4c417f10bfbfcd0cdb8bd50a591f7838aad2da`,
inside object SHA-256
`1d715acabd4cdec572d40c1905504881a396fa5e11296f1163533b30941d7796`.
It was nonexact against the target; reproducing it is an integrity control.

## Pre-score constraints

The declared builds are 121, 134, 139, 147, 151, 180, 192, 201, 205, 210 and
219. Only their compiler identity may vary. Each must use its existing pinned
support DLL and the same pinned wibo environment, source bytes and C++/O2
arguments as 3I. No compiler patch, wrapper conversion, added assembler,
linker, SDK library, source alternative or per-function flag choice is allowed.

Each of eleven cases must retain an explicit outcome in both fresh trials.
The inherited strict comparator must validate the exact unique symbol and
complete executable function, reject unresolved code relocations and compare
all target bytes without trimming or padding substitution. Input/output hashes
must be checked around execution; the build-219 row must reproduce historical
object bytes and comparison details. A failed configuration is unscored, not a
zero-byte or partial match.

Before scoring, independent review approved the 7030-byte draft
`config/mw-archive-versions.json`, SHA-256
`da60d7ac014b168ac3e24fd3288d209151efe88b7aa4fbc320768687c78718e1`,
and 12085-byte `scripts/bench_mw_archive_versions.py`, SHA-256
`e91ab759de119ef5cedd11fd1f33b533bc38cce5d0660fa5c7af3dfc525178ce`.
Fifty-two new-profile/catalogue local pins were independently rehashed, including
all existing archives, help records, compiler/support files and runner. The
inherited strict archive profile additionally binds source, receiver hypothesis,
invented naming evidence and selected reference. No tool was downloaded or
executed by this reviewer.

Each invocation uses the same compilation helper and compiler-directory working
directory behavior as 3I:

```text
{pinned-wibo} {version-mwccpsp.exe} -nostdinc -lang c++ -c -O2 -o {fresh-version-object} {unchanged-candidate-source}
```

The runner preserves all eleven outcomes and rejects warnings, failed/missing
outputs and strict-comparison failures without manufacturing partial scores.
Pre/post input checks and final retained-object byte checks include partial
outputs from raised subprocess failures. The build-219 control must reproduce
the historical return status, flags, object hash, complete comparison, ELF flags
and comments. Any control drift prevents publication. Recorded differences from
219 compare complete instruction words/lengths; they do not normalize code,
infer aliases or treat size equality as byte equality.

The final 7029-byte profile has SHA-256
`dd7e64f430030098e590d6ab82170b015fd1a0ceadd0cce58395d413461dc339`.
Replacing only its freeze-status value reconstructs the exact approved draft
digest above. The reviewed runner, source, flags and inherited inputs remain
unchanged.

## Final repeated output audit

Independent read-only review rehashed/reparsed all twenty-two objects under
`build/mw-archive-versions-zvq4q_dh` and `build/mw-archive-versions-vuhu7uvb`.
It reapplied the exact-member strict comparator against the complete pinned
target, verified each report's full comparison and word differences from 219,
and checked empty compiler logs. All eleven cases validate in each trial;
none matches the target, with the first differing byte at offset zero. No
failed or partially scored case is omitted.

The two `evidence/bucket-03l/mw-archive-versions-run-*.json` reports are identical:
28320 bytes, SHA-256
`da591776f3c67ac849be85511da9bcb7d7b875b262b5befdbb47efb2cf101f5c`.
The historical build-219 control reproduces all checked fields exactly.

| Tested builds | Complete function | Whole object | Target exactness |
| --- | --- | --- | --- |
| 121, 134, 139, 147, 151 | 124 bytes; identical within this group and across repeats | 784 bytes; identical within this group and across repeats | None exact against 68 bytes |
| 180, 192, 201, 205, 210, 219 | 100 bytes; identical within this group and across repeats | 768 bytes; identical within this group and across repeats | None exact against 68 bytes |

The 124-byte function SHA-256 is
`7ce91b0e3c662a669d6f6d390548f387449bfb3421d03a0c5ee632d7ab1b565e`;
its whole-object SHA-256 is
`dedc7a696787a92047605277693ab1b3b6174e4b7a06633adb2f75077a3bb77b`.
The 100-byte group reproduces the prior 219 function/object hashes above.
All objects retain flags `0x10970001` and comment
`MW MIPS C Compiler (3.0.0)` despite the two distinct code outputs.

Manual inspection of the retained full disassemblies identifies actual control
flow differences, rather than inferring equivalence from lengths:

| Property | 124-byte group | 100-byte group |
| --- | --- | --- |
| Zero-default blocks | Placed out of line, reached by zero branches. | Inline, skipped by nonzero branches. |
| Additional unconditional transfers | B/NOP pairs at `0x3C/0x40`, `0x54/0x58`, `0x6C/0x70`. | No corresponding unconditional transfers. |
| Large field-base ADDU sites | `0x0C`, `0x18`, `0x2C`, `0x4C`, `0x64`. | `0x0C`, `0x18`, `0x30`, `0x3C`, `0x54`. |
| Complete JR/NOP return | `0x74/0x78`. | `0x5C/0x60`. |

Those three extra branch/delay-slot pairs account for the 24-byte function
length difference. Both forms still compute the large receiver base separately
at five field-access sites. Both retain word accesses at offsets `0x2F53C`
and `0x2F540` and the same seed/default constants. This does not remove the
address-reuse difference from the 68-byte target.

These are manual static observations. The earlier forward-only address checker
was not expanded to accept the older form's backward transfers. Full candidate
disassemblies and the bounded target disassembly are retained under
`evidence/bucket-03l/`; the latter includes exactly the selected interval.
No runtime behavior or compiler-backend mechanism is thereby proven.

## Interpretation limits

This is one source/field-layout hypothesis at one fixed diagnostic setting.
Within each observed group these invocations do not distinguish the revisions
for this candidate. The difference between the tested groups does not locate
the change to an exact intervening compiler build or recover the original
class, types, source text, complete translation unit, compiler flags or linker.
Compiler revision, source shape and missing compilation context remain separate
possibilities. No interval result alone selects the game's toolchain or earns
full-game matching credit. No source revision, further compiler invocation,
settings search or linking followed the results. Runtime behavior was not
tested. Stop at the review checkpoint.
