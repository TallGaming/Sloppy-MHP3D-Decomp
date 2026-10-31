> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Toolchain investigation

No game compiler or optimization flags are locked yet. Never change flags to
match an individual function once the project configuration is established.

## Current Bucket 3M result

The [tracing-feasibility checkpoint](BUCKET_03M_CHECKPOINT.md) maps twenty
diagnostic markers to 27 decoded relocated operands, with independent real
decoder reproduction. All 296 tooling tests pass. A bounded help-only hardware
breakpoint reaches expected entry bytes, but live DOS/PE header checks fail;
identity remains INCONCLUSIVE. Pinned wibo loader source provides a plausible
header-mapping explanation. No optimizer hook, IR layout or instrumented-object
neutrality is validated. No source/flags/tools changed, and no source was compiled.
The compiler remains unlocked. Yakumo's HD static recompilation supplies archive
and port-reference leads, not an original compiler. Stop for output review.

## Earlier Bucket 3L result

The [eleven-build C++ archive comparison](BUCKET_03L_CHECKPOINT.md) finds two
output groups under the same fixed O2/source: tested builds 121–151 produce
identical 124-byte bodies, while 180–219 produce identical 100-byte bodies.
None matches the 68-byte target. The older group has three extra unconditional
branch/NOP pairs; both retain five field-base calculations. Both fresh trials
and the historical build-219 control reproduce exactly. All 283 tooling tests
pass with zero skips. No source, prior profile, comparator or flags changed,
and no new tool was downloaded. Compiler attribution remains unresolved.
Stop at the output checkpoint before another experiment.

## Earlier Bucket 3K result

The [GCC package comparison](BUCKET_03K_CHECKPOINT.md) finds no gain from the
newly pinned 1.3.1 package over existing 1.7.1. At O1/O2/O3 all fourteen complete
function bodies agree across packages, and both score 0/1/0 exact intervals.
Both O0 settings remain unscored for unsupported code relocations. Two fresh
trials reproduce all outputs and the prior 1.7.1 control exactly. The same
explicit backend and pinned GNU assembler settings were used; neither complete
SDK driver pipeline was reconstructed. All 271 tooling tests pass with no skips.
The toolchain remains unlocked; stop at the output checkpoint.

## Earlier Bucket 3J result

The [invented direct/grouped fixture pair](BUCKET_03J_CHECKPOINT.md) produces
identical whole objects and 100-byte functions in both fresh trials under
unchanged MW219/C++/O2. Each retains five static large-base ADDU sites; grouping
alone changes nothing here. Full disassemblies and bounded static analysis are
retained separately. All 258 tooling tests pass with no skips. No game source,
compiler settings or attribution conclusion changed. Await output review.

## Earlier Bucket 3I result

The [single natural archive-key candidate](BUCKET_03I_CHECKPOINT.md) is NONEXACT:
100-byte complete function versus the 68-byte target in both fresh trials,
using unchanged MW219/C++/O2. Boundary, field offsets, access order and unsigned
defaults were reviewed before compilation; class identity and volatile qualifier
remain hypotheses. The output repeats field-base calculation five times where
the target computes it once. This records a concrete code-generation difference
without attributing its cause to a particular flag, compiler revision or source
context. No source revision or flag search occurred. All 239 tooling tests pass.
The toolchain remains unlocked and full-game match credit remains zero.

## Earlier Bucket 3H result

The approved [fixed language-mode comparison](BUCKET_03H_CHECKPOINT.md) used
unmodified MW219, the unchanged fourteen-probe source and O2. Both C and C++
score the same six exact target intervals. Thirteen complete function bodies
are identical; the unsigned range check gains one ANDI in C++ and remains
nonexact. Invented-fixture naming was independently reviewed and frozen before
C++ target compilation. Both final trials agree; 226 tooling tests pass.
No language, full toolchain, game-build flags or match credit is selected.
The linked-versus-object metadata gap and translation-unit context remain open.

## Earlier Bucket 3G result

The [same-series pipeline comparison](BUCKET_03G_CHECKPOINT.md) is complete.
Our raw MW219 compiler matches the pre-patch SHA-1 guard declared by the pinned
MHP2G project; its full pipeline, patches, language mode, overlay addresses and
historical attribution are not thereby established for MHP3. Source-supported
archive/overlay similarities provide useful investigation leads, with documented
differences. No settings were adopted or new toolchain experiment executed.
The proposed fixed C/C++ mode comparison was separately approved as Bucket 3H.
The toolchain remains unlocked. All prior evidence remains unchanged.

## Earlier Bucket 3D result

The [fixed-source family comparison](COMPILER_FAMILY_COMPARISON.md) adds one
GCC and one SNC candidate to the old Metrowerks 219 control. All twelve declared
configurations were attempted; eleven are fully compared. Exact-probe counts
at levels 0/1/2/3 are GCC unscored/0/1/0, SNC 0/0/0/0 and Metrowerks 1/6/6/1.
GCC level 0 has unsupported local code relocations; it is not assigned a score.
No source, profile flags or comparator checks were changed to obtain scores.
The original toolchain remains unidentified and unlocked. See
[BUCKET_03D_CHECKPOINT.md](BUCKET_03D_CHECKPOINT.md) for review and limits.

## Earlier Bucket 3 result

The [reviewed compiler investigation](COMPILER_INVESTIGATION.md) supersedes the
initial eight-probe experiment below. It compares eleven pinned Metrowerks PSP
builds on fourteen fixed plain-C probes and eight whole-bench settings. All
builds reach only 6/14 exact probe sequences at levels 1 and 2; none reproduces
the six larger probes. Scores do not uniquely identify a build or settings.
The current proposal is **no toolchain lock yet**, with a focused follow-up
investigation before reconstruction. Source language and assembler/linker chain
also remain unresolved. Existing candidate pins describe experiments, not a
selected toolchain. No game functions are matched.

## Direct evidence from the active PSP reference

The user selected ULJM05800 v1.02. Its full image matches the size, CRC32, MD5
and SHA-1 in the Redump catalogue mirrored by libretro. See HANDOFF.md and
`config/reference.json` for hashes.

The executable decrypts to ELF32 little endian, entry `0x088214C8`, with main
`.text` at `0x08804000`, file offset `0x2CB4`, size `0x15C9E8`.

At file offset `0x224A74`, `.comment` contains exactly:

```text
MW MIPS C Compiler (2.4.1.01)\0PSP\0
```

This is direct evidence for Metrowerks MIPS/PSP tooling. It does not identify
the exact compiler executable/build, optimization flags, or original language.
Do not treat `2.4.1.01` as a proven release selection. The ELF's generic MIPS
machine/flags display in GNU readelf also does not identify the exact PSP ISA.

The next step is a representative bench of simple, well-understood game
functions, excluding SDK/runtime functions. Compare linked bytes at their
original addresses across candidate compiler builds and project-wide settings.
Resolve file boundaries and section alignment before attributing differences
to compiler flags. Record negative results so failed candidates are not retried
without new evidence.

## Supporting helper already built

This is a decryption helper, not the compiler that will build game source:

- Upstream: https://github.com/John-K/pspdecrypt (GPL-3.0).
- Commit: `c156627db7634d395c380c0a9589130f603307fc`.
- Local ignored checkout: `toolchains/pspdecrypt`.
- Built with `make CC=gcc CXX=g++` under WSL Ubuntu.
- WSL dependencies installed: `libssl-dev`, `zlib1g-dev`.
- Successful reference transformation: encrypted EBOOT.BIN SHA-256
  `9a4142cbe12086f538046633f59cc9b2bbf024c91b16cbe9710078d1cef91fb5`
  to ELF SHA-256
  `755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950`.

No upstream helper source has been copied into reconstructed game source.
No compiler from the PS1 reference project has been selected for this project.

## Working compiler candidate and compatibility runner

Candidate `mwccpsp_3.0.1_219` reports version 3.0.1 build 219, runtime built
August 24, 2006. The download is the archive declared by
[decomp.me's compiler configuration](https://github.com/decompme/compilers/blob/main/platforms/psp/mwccpsp_3.0.1_219/Dockerfile).
Hashes are in `config/compiler-investigation.json`.

A native Windows compile opened FLEXlm License Finder without generating an
object. It was terminated. Use [wibo](https://github.com/decompals/wibo) 1.2.0
under WSL Ubuntu: the candidate compiles there successfully without the dialog.
The compiler executable and bundled DLL were not modified. `-nostdinc` suppresses
the search for SDK headers; the initial source probes include no external headers.

The following describes the historical initial experiment, not the current
runner's fourteen-probe matrix. Current reproduction commands are in
[COMPILER_INVESTIGATION.md](COMPILER_INVESTIGATION.md).

Original command:

```powershell
python scripts/bench_compiler.py
```

This verifies the runner, compiler and decrypted reference hashes and compiles
the same eight provisional leaf probes in a new directory for each run. It
compares real section-indexed function bytes and rejects unresolved relocations
in probe code. Duplicate `.text` section names in Metrowerks objects are handled
by index rather than by selecting the first section with that name.

| Build 219 setting | Exact probe byte sequences |
| --- | --- |
| `-O0` | 1/8 |
| `-O1` | 6/8 |
| `-O2` | 6/8 |
| `-O3` | 1/8 |
| `-O4` | 1/8 |
| `-O4,p` | 1/8 |
| `-O4,s` | 1/8 |

This is an initial identification matrix, not per-function tuning. No setting
is selected. These tiny functions cannot distinguish exact builds, and the
probes' boundaries, signatures and game/library ownership are provisional.
No game function receives match credit from this bench. A representative bench
and the full linked byte-identical gate are still required.
