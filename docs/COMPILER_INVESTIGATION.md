> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Compiler investigation: fixed PSP probe matrix

Bucket 3, 2026-10-30. This investigation does not lock the game toolchain or
credit matched game functions. Its proposal is to keep the toolchain unlocked
and resolve the evidence gaps in another small investigation slice before
executable reconstruction.

## Reproduce

Run from `<project-root>`:

```powershell
python scripts/bench_compiler.py --report evidence/bucket-03/reviewed-bench.json
python -m unittest discover -s tests -v
```

Prerequisites are Python 3.10+, WSL Ubuntu with `timeout`, the prepared pinned
PSP ELF, the pinned wibo runner and the eleven compiler bundles listed in
[compiler-candidates.json](../config/compiler-candidates.json). These tools
are already present locally. The bench verifies them; it does not install them.
For another machine, that configuration records archive URLs and SHA-256s,
compiler/DLL hashes and runner identity. Keep binaries in ignored `toolchains/`.
Original SDK headers are unnecessary for these header-free probes.

The command uses a new `build/bench-bucket03-*` directory for every matrix,
preserving all objects, diagnostic logs and an internal report. The named report
contains no random build paths or timestamps. An existing different report is
refused. Input/compiler failures, warnings, missing objects, unexpected symbols
or unresolved probe-code relocations invalidate the matrix; partial scores are
not published. Tools, sources, reference and metadata are checked again after
compilation to reject changes during the matrix. The compatibility runner gets
empty stdin and bounded timeouts; compilers are not launched natively on Windows.

## Fixed scope

The [plain-C source](../bench/compiler_probes.c) was frozen before viewing the
new results. [compiler-probes.json](../config/compiler-probes.json) pins fourteen
intervals totaling 444 target bytes; [COMPILER_PROBE_REVIEW.md](COMPILER_PROBE_REVIEW.md)
records boundary evidence and semantic uncertainty. The original eight tiny
probes remain, followed by six probes covering reductions, pointer traversal,
terminated-unit counting, signed division, unsigned range branches and bit counting.

Every probe is unclassified as game, SDK or third-party code. The bench is a
compiler experiment, not an integration of these drafts as reconstructed game
source. Calls, global relocations, floating point, VFPU, C++ constructs, inlining
between original units and full linking are absent. The C language mode describes
the experiment and does not select the original game's language.

The [decomp.me PSP compiler catalogue](https://github.com/decompme/compilers/tree/c5f041cdc9610fb5213b7ae3c88cce02f554c4d3/platforms/psp)
supplied eleven Metrowerks candidates: builds 121, 134, 139, 147, 151, 180, 192,
201, 205, 210 and 219 of version 3.0.1. This is the tested candidate population,
not proof that it contains the historical compiler. Both the compiler and each
bundled support DLL are pinned. Version/help output was recorded locally.

Each candidate compiles the entire source under the same eight configurations:
default, `-O0`, `-O1`, `-O2`, `-O3`, `-O4`, `-O4,p`, `-O4,s`. Common flags are
`-nostdinc -lang c -c`. This is 88 configurations and 1,232 probe comparisons
per complete matrix. There are no per-function flags, source permutations,
register pins or barriers.

## Results and interpretation

Every tested build has the following exact full-symbol byte counts:

| Whole-bench setting | Exact probe sequences |
| --- | --- |
| Default / `-O0` | 1 / 14 |
| `-O1` / `-O2` | 6 / 14 |
| `-O3` / `-O4` / `-O4,p` / `-O4,s` | 1 / 14 |

All six larger probes remain nonexact under every tested configuration. The six
exact sequences at levels 1 and 2 all come from the original tiny controls.
Correct size alone is insufficient: for example, some pointer traversal and
bit-count bodies have the right size but different instructions/registers.
Reports preserve the first differing byte and complete function hashes, with no
padding trimming or relocation masking.

Equal counts do not mean identical compiler output. Comparing all compiled
probe bodies groups the builds as follows:

| Setting family | Groups with identical probe-body bytes within the group |
| --- | --- |
| Default / level 0 | 121; 134; 139/147/151; 180/192/201/205/210/219 |
| Levels 1 and 2 | 121/134/139/147/151; 180/192/201/205/210/219 |
| Levels 3 and 4, including speed/space | 121/134/139; 147/151; 180/192/201/205/210/219 |

These are observed groups for this bench, not general equivalence classes of
compiler builds. No build is established as the game's compiler, and level 1 or
2 must not be selected merely because it wins this limited score table.

The local compiler help states that level 3 adds scheduling and several other
optimizations together. It provides no documented independent scheduling switch
in the collected help. The target's instruction layout motivates further study;
it does not authorize inventing a pragma, disabling scheduling per function or
choosing undocumented settings to force these probes to match. No such change
was made in this bucket.

## Metadata, language and linking gaps

The target's `.comment` contains `MW MIPS C Compiler (2.4.1.01)` and `PSP`,
whereas all tested compiler objects contain `MW MIPS C Compiler (3.0.0)`.
Target ELF flags are `0x10A23001`; object flags are `0x10970001`. These are
direct observations at different build stages. No controlled matching-linker
experiment explains the transformation, so the mismatch is neither ignored nor
treated as proof that all eleven compilers are wrong.

The target has no symbol tables. It contains C++ runtime/demangler-looking
strings, including typeinfo/vtable descriptions and exception class names.
These suggest linked C++ support but cannot distinguish game C++ from runtime
or other library code. The original game language remains unresolved. Positive
library identification remains required before leaving code as library assembly.

The candidate bundles contain the compiler and support DLL, not an assembler or
linker. Local GNU `mips-linux-gnu-as`/`ld` are available for inspection/future
experiments; `psp-as`, `psp-ld`, `mwasmpsp` and `mwldpsp` were not found in the
checked local tool locations. No assembler/linker, options, ABI/data layout,
patches or complete reconstruction chain has been established by this bench.

## Proposal for the checkpoint

**Do not lock a compiler or flags yet.** Keep these eleven candidates and the
negative results pinned. Keep the source frozen; do not turn the six larger
hypotheses into tuning exercises. There is no defensible single toolchain choice
from the present results, and no source match receives credit.

The recommended next small slice, subject to user review, is to justify original
unit/ownership and language evidence for a few adjacent functions, add explicit
call/global relocation handling with synthetic controls, and study the executable
link/metadata requirements. Use those facts to declare a bounded follow-up
comparison rather than a blind flag sweep. Its concrete plan must be presented
before implementation. Bucket 4 reconstruction should wait until the required
toolchain proposal can be reviewed on stronger evidence.
