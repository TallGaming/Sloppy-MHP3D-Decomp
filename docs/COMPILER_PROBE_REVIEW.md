> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Fixed PSP compiler probe review

Bucket 3, 2026-10-30. `bench/compiler_probes.c` and
`config/compiler-probes.json` define the same fixed set for every candidate and
whole-bench configuration. Source was frozen before the new candidate runs.
No expression, signature or flag is to be tuned in response to a probe's score.
These are compiler-investigation hypotheses, not integrated game source or
credited matches.

## Reviewed intervals

All 14 intervals come from the pinned main ELF, SHA-256
`755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950`.
The manifest records their exact sizes, target hashes and direct-call evidence.
They contain 444 bytes in total. The eight earlier leaf probes remain as
low-information controls; six additions exercise longer control/data flow.

| Probe address | Bytes | Observed behavior / role in bench |
| --- | ---: | --- |
| `0x0883C4F8` | 16 | Byte nonzero test; original control retained. |
| `0x0883C508` | 12 | Byte clear; original control retained. |
| `0x08826448` | 16 | Copy byte and advance input; original control retained. |
| `0x0885691C` | 20 | Clear mixed-width fields; original control retained. |
| `0x0885697C` | 16 | Set one byte; original control retained. |
| `0x08856A14` | 12 | Return constant 128; original control retained. |
| `0x0885BBFC` | 16 | Subtract five and mask to a byte; original control retained. |
| `0x08860C9C` | 12 | Read unsigned byte field; original control retained. |
| `0x08830550` | 52 | Reduce six byte tests to one Boolean without early exit. |
| `0x08830654` | 36 | Follow offset-zero pointers and count until null. |
| `0x0882DA68` | 48 | Count zero-terminated 16-bit units. |
| `0x0883E944` | 48 | Zero-field branch plus signed division and byte conversion. |
| `0x08862434` | 72 | Unsigned start/end bounds with two return paths. |
| `0x0886A58C` | 68 | Count sixty packed bits using indexing and shifts. |

Each start has at least one incoming direct JAL in
`evidence/eboot-v102.disasm.txt`. Review included instructions before and after
the proposed interval, every path to a return, and its delay slot. The manifest
records example caller addresses and the next observed block. A static scan
found no direct external branch or jump into any interval's interior. The
`0x08862434` range includes both returns: stopping at its first return would
incorrectly omit the false-result block at `0x0886246C`.

These observations support bounded comparison, but do not prove historical
function symbols, absence of indirect interior entries, or exact source-level
boundaries. The byte-copy control writes its result in the return delay slot;
that store is included. All other final delay slots here are nops.

## Source interpretation and exclusions

Each probe starts with a purpose comment and uses ordinary C, with no assembly,
register pins, barriers, order tricks or intrinsics. Struct padding describes
observed field offsets; it is not a reconstruction of the original types.

The unused first argument in `0x0885BBFC`, `0x0882DA68` and `0x08862434` remains
explicit so the used values occupy their observed argument registers. It may
have been an object pointer, but that interpretation is unproven. The signed
six-byte load and signed 16-bit field follow observed instructions; their
original typedefs and application meanings remain unknown. The division probe
models ordinary nonzero-divisor inputs; invalid-input behavior has not been
validated. The address probe uses unsigned wrapping addition because the
observed `addu` does so; it must not be described as an overflow-safe range check.

No outgoing calls, global-address references or external code relocations occur
in these selected intervals. Every manifest `relocations` list is empty. The
runner must reject unexpected object relocations rather than ignore or mask
them. Calls and floating-point/VFPU code are deliberately absent from this
slice: adding them would require separately justified ABI, function boundaries
and relocation handling. No additional overlays were recovered or used.

Game-versus-SDK-versus-third-party ownership is **unclassified for every probe**.
Location among other game-looking functions is not attribution. The results
therefore describe unclassified compiler probes and must not contribute to
game-function coverage or override the library-assembly policy. No old probe
was dropped because of an unfavorable compiler result.

## Interpretation limits

The main executable's `MW MIPS C Compiler (2.4.1.01)` banner supports compiler
family investigation; it does not select the historical build, language mode,
optimization configuration, assembler or linker. An ignored first argument or
indirect dispatch could be consistent with C++ methods, but also admits other
explanations. This review makes no C-versus-C++ selection.

Even fourteen exact probe byte sequences would only establish that a candidate
can emit these small intervals from the stated hypotheses and settings. They
do not prove those hypotheses were the original source, identify the historical
toolchain uniquely, reconstruct object placement, or validate gameplay. Longer
functions, calls, floating point, relocation/link behavior and full reconstruction
remain outside this probe set. Report full-byte equality separately from size
or instruction agreement, and expose ties between candidates.

The primary agent owns compiler runs and the comparison checkpoint; independent
validation owns the bench tests. This review itself executed no compiler and
performed no runtime test. Exact build/flags remain proposals until the user's
Bucket 3 checkpoint review.
