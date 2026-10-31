> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# GCC version comparison review

Bucket 3K compares one newly prepared PSP GCC 1.3.1 kit with the existing 1.7.1
control, using the unchanged original fourteen-probe C source. This independent
review invokes no compiler, assembler or linker and downloads no tools. Exact
diagnostic intervals do not establish original compiler identity or integrated
game-source matching credit.

## Inherited inputs and execution constraints

Read-only preflight confirms these existing identities:

| Input | Bytes | SHA-256 |
| --- | --- | --- |
| `bench/compiler_probes.c` | 4413 | `d5d588c184c7c95a86bb3772e760f9251d33e3e4aabf92dfc0449c6ddc7c7a95` |
| `config/compiler-probes.json` | 8224 | `2a3a7783a11704c870311470cf851434ec1e0a660af29787db48178b2c58ffbc` |
| `config/compiler-families.json` | 46770 | `cb0b3fbd1961380c8cee61a286bce723be7ed13c73e39bd8c949e6c701413dab` |

The existing control identifies its backend as
`3.3.3+allegrex-2.2.2-psp-1.7.1`. It uses unmodified native C `cc1`, not an
assumed complete SDK driver. Its fixed common options are
`-quiet -nostdinc -G 0 -march=allegrex -mtune=allegrex -mel -mabi=eabi`.
The matrix must retain the four whole-bench settings O0, O1, O2 and O3 for each
kit, without per-function flag selection or source changes.

Both profiles must use the same pinned modern GNU assembler in preservation
mode: `-EL -march=allegrex -mabi=eabi -G0 -O0`. This is diagnostic assembly,
not evidence of the historical SDK assembler. The inherited compilation helper
copies the exact source bytes and original basename into fresh native Linux
temporary storage, avoiding the old backend's Windows-mount inode limitation.
It records the emitted assembly hash, checks source/assembly integrity and
refuses stale output objects. No source/header or assembly transformation is
part of this comparison.

Complete fourteen-function configurations are the scoring unit. The inherited
strict comparator checks actual function symbols, executable section indices,
complete sizes, overlaps and code relocations. A malformed/missing function or
unsupported code relocation makes its whole configuration unscored; other
declared settings still retain their explicit outcomes. Rejected settings must
not be presented as zero exact functions or silently omitted.

## New kit provenance and supported inputs

The primary recorded candidate selection before acquisition/help/scoring in
`evidence/bucket-03k/candidate-selection.json`. The selected public catalogue
recipe remains commit `c5f041cdc9610fb5213b7ae3c88cce02f554c4d3`; the date-suffixed
1.3.1 archive URL is retained explicitly. This is a pinned diagnostic acquisition,
not proof that Capcom used that distribution.

The acquired archive is 17194959 bytes, SHA-256
`788b6d2c0ed920da6b1e5a350d23dd7ea05820526e23f9b5b967b3b238ea2e2e`.
Independent read-only inspection found 498 tar members, including 438 regular
files, with no links or zero-byte file payloads. Every payload's size/hash was
checked against the inventory and its extracted file. The 106778-byte
`downloaded-candidate.json` inventory has SHA-256
`72abaf1b4f2f32e07ef51ab90bae588c38cf3eea98e4f1b3a7f4efa2b36685b3`.
Unlike the examined 1.7.1 archive's placeholders, this kit contains nonempty
assembler/linker files. They are outside the experiment's execution path.

The new C backend is 2747032 bytes, SHA-256
`1ee49eca0c5d0d24b818b21fd2cd395c45a50416cdc26ea293964ee2b9e88452`.
Read-only ELF-header inspection confirms a 32-bit little-endian x86 host program
using `/lib/ld-linux.so.2`. The existing pinned native host/dependency environment
must be verified; target Allegrex selection must not be confused with host ISA.

The primary's recorded successful version/help calls identify
`3.3.3+allegrex-2.2.1-psp-1.3.1` and document the common option syntaxes:
quiet/include suppression, optimization level, small-data threshold, endianness,
CPU generation/tuning and ABI. The bundled `specs` agrees on the version and
EABI default. Its driver injects Allegrex generation/tuning and `-mno-ulsw`,
while rejecting user-supplied march/mtune at the driver level. Backend help
independently supports those backend options. Bypassing the driver is therefore
an explicit experimental choice, not a claim that the driver accepts the exact
same command line.

The comparison preserves the existing backend arguments, without newly adding
`-mno-ulsw` from this driver's defaults. Identical explicit options can still
leave different backend defaults; the result covers the declared backend
invocations, not complete SDK-driver pipelines or an isolated optimizer pass.

## Independent pre-score approval

Before target scoring, review approved the 104541-byte draft
`config/gcc-versions.json`, SHA-256
`f8384ff440a031b3b6e6cb05edceebaa3fd44da4c7cd31f563a69f5a709a18c4`,
and 14381-byte `scripts/bench_gcc_versions.py`, SHA-256
`e17a59b87dfc56a6d69d3d31bac5e0e925d20afe3deff59e569461ed676bcbb9`.
Every candidate support-file identity agrees with the independently inspected
inventory. Both profiles' common flags, four optimization levels, assembler
binary and preservation flags agree exactly. The two compiler stages are:

```text
{version-cc1} -quiet -nostdinc -G 0 -march=allegrex -mtune=allegrex -mel -mabi=eabi -O{0,1,2,3} -o probe.s compiler_probes.c
{pinned-GNU-as} -EL -march=allegrex -mabi=eabi -G0 -O0 -o {fresh-version-level-object} {unchanged-emitted-assembly}
```

Each level applies to the complete unchanged bench. Neither bundled SDK
assembler, SDK driver, linker nor runtime library is substituted.

The primary first compiled only `bench/gcc_version_fixture.c`, an invented
307-byte unsigned-word identity function, SHA-256
`a474a0bd1f4387f6c99e2b6de87ff03b5e17ecc62a796ebdbe8026772158447f`.
Its option-preflight evidence is 12452 bytes, SHA-256
`a563e2f21cb8a56182fbe11bd390ab36b95c52f194f65e8441a964c724b4da52`.
Independent parsing/rechecking of both 1132-byte objects confirms one complete
8-byte function with the same function SHA-256
`e7f105b76f82936ad81b02ee2a012dbcfe69ed893238588250523d37b6504efa`.
Their comments identify their respective versions. This establishes a runnable
option path for that tiny invented input, not target matching or equivalence of
implicit backend behavior.

The reviewed runner retains all eight declared attempt outcomes, scores only
complete validated settings, and records exact assembly/object/function hashes.
It checks new/inherited/preserved inputs before and after execution, guards
report aliases, and checks every retained output's bytes again before reporting,
including partial objects left when a stage raises. Its 1.7.1 control must
reproduce the complete prior 3D attempts and scored rows, including assembly
hashes; disagreement fails the trial rather than silently accepting drift.
The frozen 3I/3J sources/profiles are preserved inputs, not new compile targets.

The final 104543-byte profile has SHA-256
`fdb48bb1281b3705d1a3e47ffeeb4f958b43d8e6c905ab9c060a9963979c7e4d`.
Replacing only its freeze-status value reconstructs the exact approved draft
digest. The reviewed runner and all source/options remain unchanged.

## Final repeated artifact audit

The reviewer independently rehashed and reparsed all sixteen retained objects
under `build/gcc-versions-92qhwnnk` and `build/gcc-versions-wumgidx3`, then
reapplied the unchanged complete-function comparator. All 168 scored target
comparisons and 84 supported cross-version comparisons agree with the reports.
All sixteen compiler/assembler diagnostic logs are empty. Both 1.7.1 control
attempt lists and complete scored-row dictionaries exactly reproduce the prior
3D evidence, including whole-object and assembly hashes.

The two `evidence/bucket-03k/gcc-versions-run-*.json` reports are byte-identical:
62185 bytes, SHA-256
`2c7d6790bca4b6762433f17263da49d0ef81eb924147973b0601f828adfbf55d`.
Every declared setting is retained in each trial:

| Package | Setting | Outcome in each repeat | Exact diagnostic intervals |
| --- | --- | --- | --- |
| 1.3.1 | O0 | Unsupported code relocations; unscored | Unknown; no partial score |
| 1.3.1 | O1 | Complete fourteen-function comparison | 0/14 |
| 1.3.1 | O2 | Complete fourteen-function comparison | 1/14 |
| 1.3.1 | O3 | Complete fourteen-function comparison | 0/14 |
| 1.7.1 control | O0 | Unsupported code relocations; unscored | Unknown; no partial score |
| 1.7.1 control | O1 | Complete fourteen-function comparison | 0/14 |
| 1.7.1 control | O2 | Complete fourteen-function comparison | 1/14 |
| 1.7.1 control | O3 | Complete fourteen-function comparison | 0/14 |

Independent relocation inspection confirms nine `R_MIPS_26` records against
local unnamed section symbols in each O0 object. The strict comparator rejects
these; no relocation masking, body trimming or manual substitute score is used.
That is a comparison-format limitation, not a compiler failure.

At each fully validated level O1, O2 and O3, all fourteen complete function
bodies are byte-identical between versions. The corresponding whole objects
have equal sizes (2416, 2400 and 2400 bytes respectively); their only byte
differences are two bytes within the GCC `.comment` version text. This explains
why distinct object hashes do not represent different code here. Raw flags are
`0x10843001` throughout. The sole O2 exact interval is the already known
`probe_08826448`; there is no new diagnostic exact interval or game-match credit.

This fixed bench does not distinguish the two backends at its supported levels.
The result neither proves their general equivalence nor rules either version
into or out of MHP3's historical toolchain. The preserved archive initializer and
invented address-reuse fixtures were not recompiled or rescored in this bucket.
No new source attempt, settings search, linking or runtime testing followed
the results. Stop at the review checkpoint.

## Interpretation limits

The package labels 1.3.1 and 1.7.1 both describe GCC 3.3.3-based Allegrex kits;
they are not GCC language-version numbers. Different backend/tool inventory
identities do not guarantee distinct output for this limited bench. Conversely,
an exact interval would not establish the original source text, types, ownership,
compiler flags, complete SDK pipeline or historical compiler version. The
fourteen functions retain their existing unclassified ownership and source
hypotheses. Tool availability, raw byte identity, integrated source coverage,
full-build matching and runtime validation remain separate claims.
