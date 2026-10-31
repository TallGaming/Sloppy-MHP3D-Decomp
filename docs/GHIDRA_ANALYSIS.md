> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Pinned PSP analysis in Ghidra

Bucket 3B uses a local, headless Ghidra project for the verified main ELF.
Analysis outputs and inferred pseudocode are research artifacts, not reconstructed
game source. No game code is executed or uploaded.

## Tools and project

[analysis-tools.json](../config/analysis-tools.json) pins:

| Tool | Version | Primary release |
| --- | --- | --- |
| Ghidra | 12.2 | [NSA release](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.2_build) |
| Allegrex processor extension | 21.5, built for Ghidra 12.2 | [Extension release](https://github.com/kotcrab/ghidra-allegrex/releases/tag/v21.5) |
| Portable Linux JDK | Temurin 25.0.5+8 | [Adoptium release](https://github.com/adoptium/temurin25-binaries/releases/tag/jdk-25.0.5%2B8) |

Archives and extracted tools live under ignored `toolchains/`. The local
`analysis-file-manifest.json` pins 5,751 installed files/symlinks, derived from
the hash-verified archives. Its own identity is pinned in the tracked tool
configuration. The wrapper verifies the installed files, archives, export
script and reference before and after analysis. These are analysis-tool pins;
the game's compiler/assembler/linker remain unlocked.

The tested environment is WSL Ubuntu, launched from PowerShell by the wrapper.
It uses the portable Linux JDK and a project-local Java user directory. A native
Windows GUI installation has not been configured or tested.

## Reproduce with fresh paths

From `<project-root>`:

```powershell
python scripts/analyze_reference.py --project-dir reference/ghidra/my-review --export evidence/bucket-03b/my-review.json --report evidence/bucket-03b/my-review-summary.json
```

Use project-relative paths and fresh names. Existing project/evidence paths are
refused. The saved project is `reference/ghidra/my-review/mhp3rd.gpr`, accompanied
by its `.rep` directory; keep both together. A compatible Ghidra installation
can open that project. The exported JSON includes local pseudocode hypotheses;
the summary contains only verification metadata. Logs sit beside the summary.
The wrapper limits total execution and auto-analysis time and never modifies
the pinned executable.

The loader must identify `PSP Executable (ELF)` with processor
`Allegrex:LE:32:default`, compiler specification `default`, image base
`0x08804000`. The wrapper checks the complete main `.text` mapping, both selected
probe memory hashes, exact function extents and successful target decompilation.
It cross-checks direct-call sites against a separate scan of the original JAL
instructions, requires their exported caller bodies to cover the sites, and
requires those caller decompilations to complete.

## Bounded selection and limits

The selection is the six-byte reduction at `0x08830550`, the list count at
`0x08830654`, their direct callers, and six neighboring functions. The initial
analysis exported 34 distinct functions: 34 reduction call sites in 26 callers,
one list-count caller, the two targets and the neighboring helpers. Repeated
fresh-project results are recorded in the bucket checkpoint.

The two target function bodies have the reviewed 52/36-byte extents. Ghidra's
pseudocode supports their basic loop semantics and the wireless peer-list
context; [PROBE_MISMATCH_DIAGNOSIS.md](PROBE_MISMATCH_DIAGNOSIS.md) separates
those observations from original-source hypotheses.

Inferred prototypes are incomplete. Some displayed caller pseudocode omits a
pointer argument that the assembly passes in `a0`; generic signature fields and
raw `int *`/`undefined4` types are not original declarations. Pseudocode loop
spelling does not identify the original source or compiler flags.

The loader skips the zero-sized overlay descriptors. Its workspace does not
represent every runtime memory reservation from the original program headers.
Some data blocks inherit executable permissions from the ELF's broad load flags;
that does not establish that their contents are code. Auto-analysis reports
warnings involving unloaded overlay targets and an uninitialized address. These
limits remain explicit even when every selected decompilation completes. Use the
ELF map for reservation evidence, and do not treat this as whole-program or
runtime validation.
