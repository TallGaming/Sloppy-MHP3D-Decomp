> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3K checkpoint

2026-10-31. The approved GCC package comparison is complete. **GCC 1.3.1
provides no gain over 1.7.1 on the frozen fourteen C probes. At O1, O2 and O3,
all fourteen complete function bodies are identical between the packages.
Both fresh trials agree and reproduce the historical 1.7.1 control exactly.**

## All declared outcomes

| Whole-bench level | GCC package 1.3.1 | GCC package 1.7.1 | Cross-version bodies |
| --- | --- | --- | --- |
| O0 | Unscored: unsupported code relocations | Unscored: unsupported code relocations | Unscored |
| O1 | 0 / 14 exact target intervals | 0 / 14 | 14 / 14 identical |
| O2 | 1 / 14 | 1 / 14 | 14 / 14 identical |
| O3 | 0 / 14 | 0 / 14 | 14 / 14 identical |

The single O2 exact interval is the existing byte-copy/advance probe at
`0x08826448`. None of the six larger probes becomes exact. These counts concern
complete isolated probe symbols; they confer no game-source match credit or
historical compiler identification. In both packages, O0 has nine local
section-symbol R_MIPS_26 relocations in probe code. The existing comparator
rejects the whole setting, withholding all function scores. No relocation word
was masked, patched or treated as final.

This is a bounded negative result for the declared source/commands. It does not
prove the packages generate identical code generally or exclude either from
unrelated parts of the game. Whole-object bytes differ between versions;
complete validated function bytes are what agree. In each validated level's
objects, the two differing bytes are in the compiler-version comment. Each
version/level's whole object repeats exactly across trials.

## What was frozen before scoring

The new public catalogue package reports GCC
`3.3.3+allegrex-2.2.1-psp-1.3.1`; the unchanged control reports
`3.3.3+allegrex-2.2.2-psp-1.7.1`. The locally downloaded 17194959-byte archive has
SHA-256 `788b6d2c0ed920da6b1e5a350d23dd7ea05820526e23f9b5b967b3b238ea2e2e`.
Independent archive inspection verified all 438 extracted file payloads,
without symlinks or empty files. This pins the preserved catalogue package,
not a vendor-attested historical Capcom installation.

Both versions use their unmodified C backend in native Linux staging, retaining
the exact original source basename and bytes. Their shared command is:

```text
cc1 -quiet -nostdinc -G 0 -march=allegrex -mtune=allegrex -mel -mabi=eabi -O{0,1,2,3} -o probe.s compiler_probes.c
pinned-GNU-as -EL -march=allegrex -mabi=eabi -G0 -O0 -o FRESH_OBJECT probe.s
```

Each optimization level applies to the entire bench. The GNU assembler and
preservation flags remain exactly those of the prior experiment. The new
archive contains actual bundled assembler/linker tools, but they are unused
here. Neither SDK driver pipeline is reconstructed. In particular, the new
driver injects `-mno-ulsw`; this diagnostic preserves the prior explicit backend
flags without adding that option. Equal explicit flags do not prove equal
implicit defaults or equivalence to either full SDK build.

The exact profile, source, target manifest, tools, option evidence and prior
control report were reviewed by both helpers before any new target score.
The invented option preflight used a separate identity function, not game code.
The draft was 104541 bytes, SHA-256
`f8384ff440a031b3b6e6cb05edceebaa3fd44da4c7cd31f563a69f5a709a18c4`.
Only its status value changed for freezing. The frozen profile is 104543 bytes,
SHA-256 `fdb48bb1281b3705d1a3e47ffeeb4f958b43d8e6c905ab9c060a9963979c7e4d`.
The retained pre-score declaration describes that historical freeze point.

## Review artifacts

- [Frozen profile](../config/gcc-versions.json),
  selection (local-only artifact: `evidence/bucket-03k/candidate-selection.json`) and
  freeze record (local-only artifact: `evidence/bucket-03k/profile-freeze.json`)
- Trial 1 (local-only artifact: `evidence/bucket-03k/gcc-versions-run-1.json`) and
  trial 2 (local-only artifact: `evidence/bucket-03k/gcc-versions-run-2.json`)
- [Independent tool/profile/output review](GCC_VERSION_REVIEW.md) and
  [validation notes](BUCKET_03K_VALIDATION_NOTES.md)
- [Runner](../scripts/bench_gcc_versions.py),
  [invented failure controls](../tests/test_gcc_versions.py) and
  verification summary (local-only artifact: `evidence/bucket-03k/verification-summary.json`)
- Full O2 disassembly: GCC 1.3.1 (local-only artifact: `evidence/bucket-03k/psp_gcc_1_3_1-O2.disasm.txt`)
  and GCC 1.7.1 (local-only artifact: `evidence/bucket-03k/psp_gcc_1_7_1-O2.disasm.txt`).
  Full outputs for all four levels, including O0 relocation annotations, are
  retained alongside them.

Fresh roots are `build/gcc-versions-92qhwnnk` and
`build/gcc-versions-wumgidx3`. Both 62185-byte reports have SHA-256
`2c7d6790bca4b6762433f17263da49d0ef81eb924147973b0601f828adfbf55d`.
Six of eight configurations per trial are fully compared; two remain unscored.
Both independent audits checked the 16 retained objects, repeat identities,
168 full target comparisons and 84 cross-version function comparisons. All
compiler/assembler logs are empty. The historical control check includes exact
object hashes, assembly hashes, complete comparison rows and rejection outcomes.

## Validation and decisions preserved

All **271 tooling tests pass under WSL, zero skips**: 258 prior plus 13 new
runner checks. Invented controls cover fixed scope/flags, historical control
drift, complete bodies, failed whole settings, changing inputs, output mutation,
aliases and preserved evidence. Review closed an integrity edge before scoring:
an object left by a timed-out stage must also be snapshotted and rechecked.
Dedicated controls cover those failed partial outputs. No comparator was weakened.

Real report/profile-alias and unapproved-flag controls fail before any new
compilation directory or success report and preserve the original profile.
Independent verification checked 644 local and 11 native pin records, including
all new package files and preserved earlier game-candidate inputs. Duplicate
declarations count as records, not distinct files. The primary independently
reparsed all objects and ran both pre-build failure controls without compiling.

From the project root, reproduction uses fresh report paths:

```powershell
python scripts/bench_gcc_versions.py --report evidence/bucket-03k/new-trial-1.json
python scripts/bench_gcc_versions.py --report evidence/bucket-03k/new-trial-2.json
wsl -d Ubuntu -- python3 -m unittest discover -s tests -v
```

The original fourteen-probe source, prior profiles, strict comparator and the
Bucket 3I game candidate remain unchanged. The earlier pointer-only 3K proposal
was superseded by this explicitly approved compiler comparison; no pointer
variant was implemented. No linker, runtime, flag search, source rewrite or
native-port work occurred. Toolchain attribution and selection remain unresolved;
game-match/source-link/parking/trick counts remain zero. The full-game byte gate
and its required 18 negative checks remain unimplemented. Stop for user review;
no further experiment is authorized by completing this bucket.
