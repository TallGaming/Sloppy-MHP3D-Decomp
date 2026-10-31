> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3K independent validation

This bucket compares the original frozen fourteen C probes under GCC package
1.3.1 and the existing package 1.7.1 control. These diagnostic results confer
no game-match, linked-source, runtime, library-identification or toolchain-lock
credit. No helper compiled either real package or executed game code.

## Pre-score review

The helper reviewed the source, inherited family runner, new runner and draft
profile before any new target scores. The final reviewed draft was 104541 bytes,
SHA-256 `f8384ff440a031b3b6e6cb05edceebaa3fd44da4c7cd31f563a69f5a709a18c4`.
It retains the original source/manifest/reference identities, exactly two GCC
packages and all four whole-bench levels O0–O3. Both profiles use identical
supported backend options and the same pinned GNU assembler preservation mode.
The older complete SDK drivers and assemblers are not being reproduced; these
remain diagnostic backend pipelines. The fixed options omit the driver-injected
`-mno-ulsw`; no option was added after viewing target output.

The helper independently ran input verification against that draft, checking
644 project-local pin records and the inherited native dependency pins. These
are declaration counts, not counts of distinct files. They include the complete
438-record new package inventory and six preserved Bucket 3I/3H/3J inputs.
The approved source and prior experiments remain unchanged.

The status-only freeze is 104543 bytes, SHA-256
`fdb48bb1281b3705d1a3e47ffeeb4f958b43d8e6c905ab9c060a9963979c7e4d`.
The recorded freeze precedes candidate target compilation; its source, tools,
commands and evidence match the approved draft.

## Meaningful tooling controls

The new tests use invented ELF bytes and mocked compilation. Their fourteen
functions are independent of game bytes, and real nested input validation runs
against temporary pinned fixtures. Existing ELF/parser tests are reused rather
than reproduced as new coverage. The thirteen tests cover:

- All eight fixed configuration attempts, complete fourteen-function scoring,
  exact command scope, two fresh trials and deterministic reports.
- Nonzero exits, warnings, timeouts, missing or malformed objects, missing
  functions and unsupported code relocations. A rejected setting exposes no
  partial score; complete settings remain separately visible.
- Exact reproduction of the pinned historical 1.7.1 control. A changed control
  object or failed control setting fails the investigation instead of becoming
  a replacement baseline.
- Full body lengths and hashes, including a longer body sharing an exact
  prefix. Padding is not trimmed, and an unscored comparison retains nulls.
- Original source/reference/metadata, tool/archive/support/native dependency
  pins, preserved inputs, invalid profile scope, mutations during the matrix,
  report aliases and conflicting-report preservation.
- Post-matrix checks of every retained emitted object, including an object
  written before a nonzero return or a raised timeout.

During review the helper found that a timeout-written partial object initially
escaped the emitted-object snapshot. The primary fixed capture after every
attempt; the meaningful negative test now rejects a later compiler invocation
that replaces that partial object. The fix changes validation only, without
changing source, flags or the comparator.

The helper ran `python3 -m unittest tests.test_gcc_versions -v` under WSL Ubuntu:
**13 passed, zero skipped**. The owned test file is 19021 bytes, SHA-256
`2203e86e12f48316fc93d1b1eab4111c06a81c3f5c23d4b8b84e73f5f32d5607`.
The helper also ran the complete tooling suite under WSL Ubuntu: **271 passed,
zero skipped**, preserving the prior 258 checks.
These tooling controls are separate from the required full-game gate's eighteen
negative tests, which have not been implemented or passed.

## Repeat artifact audit

The helper independently read both final reports and all sixteen emitted objects
from `build/gcc-versions-92qhwnnk` and `build/gcc-versions-wumgidx3`.
`evidence/bucket-03k/gcc-versions-run-1.json` and `gcc-versions-run-2.json`
are byte-identical: **62185 bytes**, SHA-256
`2c7d6790bca4b6762433f17263da49d0ef81eb924147973b0601f828adfbf55d`.
Each trial's local report equals its external report. All eight corresponding
whole-object hashes reproduce between trials; every compiler log is empty.

| Package | O0 | O1 | O2 | O3 |
| --- | --- | ---: | ---: | ---: |
| GCC 1.3.1 | Unscored: unsupported code relocations | 0/14 | 1/14 | 0/14 |
| GCC 1.7.1 | Unscored: unsupported code relocations | 0/14 | 1/14 | 0/14 |

For each of the four retained O0 objects, the helper verified all fourteen
function symbols and nine executable-section REL records of type `R_MIPS_26`,
each referencing a local `STT_SECTION` symbol. These are unsupported local code
relocations; the earlier external-call resolver does not apply. Neither O0
setting publishes function comparisons, an exact count or a cross-version score.

For the twelve scored objects, the helper independently recomputed all **168
target comparisons** from full symbol extents and the pinned reference: sizes,
hashes, exactness, first differences and per-setting exact totals. The helper
also recomputed **84 cross-version comparisons** from complete function bytes.
All fourteen bodies agree between packages at each of O1, O2 and O3 in both
trials. These are code-body observations; cross-package whole-object identity
is not asserted. The current 1.7.1 attempts and complete scored rows exactly
reproduce the pinned Bucket 3D control, including object and assembly hashes.

Final verification again passes **644 local pin records and 11 native dependency
records**, including the preserved prior sources/profiles. No original ISO was
opened or modified. No source, compiler flag, assembler flag or comparator was
changed after viewing the outputs.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `scripts/bench_gcc_versions.py` | 14381 | `e17a59b87dfc56a6d69d3d31bac5e0e925d20afe3deff59e569461ed676bcbb9` |
| `tests/test_gcc_versions.py` | 19021 | `2203e86e12f48316fc93d1b1eab4111c06a81c3f5c23d4b8b84e73f5f32d5607` |

The unchanged body outputs do not distinguish these two package revisions for
this isolated probe source. They neither identify Capcom's compiler nor exclude
GCC with a different historical translation unit or build configuration. No
setting is selected as the game's toolchain, and no additional source or flag
experiment is performed. Stop at the Bucket 3K review checkpoint.
