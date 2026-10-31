> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3M: compiler-tracing feasibility — review checkpoint

The approved feasibility investigation is complete. Static compiler anchors are
mapped, and a help-only debugger probe can stop at the expected entry bytes.
**A verified compiler identity/optimizer-hook/IR capture is not established.**
This does not resolve which original compiler or source context produced the
68-byte archive initializer. No toolchain is selected and no game match is claimed.

## Reviewable outputs

| Output | Result |
| --- | --- |
| `scripts/inspect_compiler_trace.py` | Strict PE32 mapping, relocation and decoded-operand analysis; never executes the compiler. |
| `evidence/bucket-03m/static-reference-candidates.json` | Twenty exact diagnostic markers map to 27 relocated, decoded `PUSH imm32` operands. All 55987 HIGHLOW relocations were independently checked. |
| `docs/COMPILER_TRACE_FEASIBILITY_REVIEW.md` | Pinned debugger/wibo source review, guest-mode and mapping requirements, and bounded help-probe outcomes. |
| `docs/BUCKET_03M_VALIDATION_NOTES.md` | Independent real decoder reproduction, operand/report audit, thirteen new controls and help-evidence audit. |
| `docs/PSP_PROJECT_RESEARCH.md` | Requested Yakumo review at commit `b61852aef10870400320b96d92a14136ac17b051`; seven pinned public text snapshots. |
| `evidence/bucket-03m/verification-summary.json` | Final file hashes, preserved inputs, outcome limits and separate progress counters. |

The 42792-byte static report has SHA-256
`0e8ae104dd85f96eccb0584c3acdf6f598d09e756ed9fc8902a257c3b3722a5b`.
The independent reviewer reproduced the entire 27624804-byte listing using the
same pinned GNU objdump command, then reproduced the report without executing
the compiler. Some marker strings have multiple code references. None by itself
identifies a unique callable pass boundary, pass activation, pass order or IR
layout. Unsupported operand forms remain unclassified.

## Help-only transport observation

Both declared attempts and complete streams are retained. Only documented
`-help` requests were made; no C/C++ source was compiled or object generated.

1. Attempt 1's ordinary help exits 0; GDB rejects a hardware breakpoint before
   the inferior exists. No debugger-assisted compiler launch occurs. This
   startup failure is retained, rather than treated as a tracing limitation.
2. Attempt 2 starts the runner, installs a hardware breakpoint and stops at
   `0x401000`, CS 7, with the exact expected sixteen entry bytes. Ordinary and
   debugger-assisted help both exit 0, with empty stderr; ordinary output is
   preserved verbatim within debugger output. Compiler, wibo and GDB hashes
   remain unchanged.

The predeclared identity check also required live DOS/PE headers. Reads at the
inferred image base return zeros, so the result remains **INCONCLUSIVE**.
Pinned wibo loader source zeroes the image and copies sections without copying
those headers, which is consistent with this observation. We did not relax the
criterion afterward. A later loader-aware identity contract would need review
before another probe. Hardware stopping and normal help completion establish
neither correct guest-stack interpretation nor instrumentation-neutral objects.

The public PS2 tracing project has no validated ready-made PSP/wibo profile.
Its IR structures and hook addresses cannot be imported into this PSP compiler.
Existing ELF flags, runtime strings and linked banners remain attribution leads,
not proof of a compiler revision for every original game unit.

## Validation and decisions to verify

The primary and validation helper each ran the complete tooling suite:
**296 tests passed, zero skips**, including thirteen new static-checker tests.
Review caught and fixed incorrect C7 operand-length acceptance; the actual 27
references remain unchanged. Decoder provenance and report alias/conflict
controls also pass. These tests are separate from the unimplemented full-game
gate and its required eighteen negative tests.

The compiler binaries, game draft, earlier profiles and flags remain unchanged.
No tool installation, binary patch, game execution, linker experiment or port
implementation occurred. Game matches, linked source, parked functions,
register pins, empty-asm lines and matching-only source shapes all remain zero.
The single retained archive draft remains one unmodified source hypothesis.

Yakumo supplies useful archive/overlay and later platform-boundary references,
with HD-specific limits documented in the research. Its static-recompilation
approach does not satisfy our readable-original-source/full-byte gate.
The PSP v1.02 target, readable-source-first policy, fixed settings and
matching-before-port decision remain in force.

Stop here for output review. No next bucket, new matching candidate, full tracing
port or native-port implementation is approved by this checkpoint. Possible
follow-ups are a reviewed loader-aware help identity check, a bounded PSP
archive/overlay cross-check informed by Yakumo, or a separately planned source
context experiment. Present one concrete plan before any implementation.
