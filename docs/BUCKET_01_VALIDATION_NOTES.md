> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 1 independent validation notes

Reviewed on 2026-10-30 by the validation helper. This is a reference-tool review,
not a matching-build gate result or a game runtime test. No commits were made.

## Automated checks

From `<project-root>`:

```powershell
python -m unittest discover -s tests -v
```

Result: **49 tests passed** (exit 0): 14 existing checks, 23 new preparation
checks and 12 new mapping checks.

Preparation checks use a small synthetic ISO with `PSP_GAME/PARAM.SFO` and
`PSP_GAME/SYSDIR/EBOOT.BIN`, a synthetic bounded MIPS ELF, and a mocked decryption
helper. They cover:

- Selected/active reference enforcement, full-image and executable identity,
  and metadata identity before tool execution.
- Missing or changed helpers; helper failure, timeout or missing output;
  incorrect plaintext hash; malformed or relocatable ELF output.
- Rechecking the staged encrypted input and helper after execution.
- Preserving the input image and existing evidence; rejecting bad existing
  artifacts; preserving good artifacts after a failed repeat.
- Executing the transformation again on repeat instead of accepting stale output.
- Refusing report/input aliasing, preserving a different existing report, and
  passing empty stdin plus explicit timeouts to subprocesses.

Mapping checks exercise duplicate section names with distinct indices, bounded
ELF parsing, address overflow, PT_LOAD zero-fill versus declared BSS, PT_NULL
metadata, overlay grouping and explicit pairing ambiguity. Zero-sized descriptors
and even descriptors with embedded bytes never count as extracted payloads.
CLI checks reject identity mismatches and preserve conflicting evidence and ELF
input files.

These are **not** the 18 future negative checks for the all-target matching gate.

## Independent checks of real outputs

The validator independently read the actual files without running game code:

- The accepted original ISO still has size 1,207,140,352 and SHA-256
  `20a3b77c76f3729843f4e945fe4f04085edd6f37aa6122399d296d7f2e9c3dd8`,
  matching `config/reference.json`.
- Both `reference/bucket-01/run-1/` and `run-2/` contain EBOOT.BIN/EBOOT.ELF
  with their respective locked sizes and hashes.
- `evidence/bucket-01/preparation-run-1.json` and `preparation-run-2.json`
  are identical JSON reports.
- `evidence/bucket-01/executable-map-v1.json` and
  `executable-map-v1-repeat.json` are byte-identical, SHA-256
  `451fa59db4cb04b14b462d1fecb0f7edef56265d30cfc861c0f6add28db90a96`.
- The final map reports 355 zero-sized overlay descriptors, 12 shared-start
  groups and zero extracted overlay payloads. It does not prove twelve disjoint
  physical slots or a one-to-one association between names and reservation sizes.

## Reviewed source identities

The checks above were run against these source SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `scripts/prepare_reference.py` | `1d28d5f6edb44ac76bab7efe519fb29e14bc9bfbb4da5688ade6d81e8323e607` |
| `scripts/map_executable.py` | `6ae13a47a96fbc7e614929517ae8133b10de009b386a566cb28b7c1aa6c4f693` |
| `scripts/elf32.py` | `766f16f86736ed0a04eb6c1ed439bd8aa96d2aab0b0c99e49055934e2fd45833` |
| `tests/test_prepare_reference.py` | `6f43791554e5b12550e1d41695825f7baf421f8545f1734c38205e0dc1c69d2d` |
| `tests/test_map_executable.py` | `df38431306e95179af20c2903ead2d3381b0df0a0018d20a81c5f5e5f21b7c65` |

No material blocker was found in the reviewed paths. The synthetic helper tests
establish orchestration behavior; the actual two preparation runs establish the
real decryption result. They do not establish a compiler build, game source
coverage, library classifications, archive payload recovery or gameplay fidelity.
