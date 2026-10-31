> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3M independent validation

The helper's checker work is static compiler-tracing feasibility analysis. The
helper executed no compiler, debugger, game, installer or instrumented
compilation, and changed no source, compiler option, tool binary or prior
experiment. The primary later performed the separate help-only debugger probes
reviewed below; those executions are not source compilation or static-checker
behavior.

## Decoder availability

Read-only checks of Windows Python 3.13 and WSL Python 3.14 found no installed
`capstone`, `iced_x86`, `distorm3`, `pefile` or `lief` modules. No dependency was
installed. WSL's existing `/usr/bin/objdump`, GNU binutils 2.46-3ubuntu2,
advertises `pei-i386` and `pe-i386` support. This supplies an available actual
instruction decoder; executing it for static analysis does not execute the PE.

An operand in linearly decoded executable bytes is a bounded static candidate.
It does not establish reachable code, a valid function entry, a callable hook,
an active O2 pass, execution order or instrumentation neutrality. Arbitrary
DWORD matches and pointers in data must remain distinguishable from decoded
code operands.

## Independent marker mapping

The helper read the unchanged 2079232-byte MW219 PE directly, matching compiler
SHA-256 `828f9b30b3ae33c7a0202c2baf48aab49884c60e48c5b3daa2436bc3237368df`.
Its PE header is at file offset `0x80`, machine `0x14C` (i386), with image base
`0x400000`. All twenty previously recorded strings match exact NUL-terminated
bytes inside the file-backed `.data` section. That section has raw-file offset
`0x1ACE00` and RVA `0x1AF000`; for these strings only, RVA is file offset plus
`0x2200`, and preferred VA is file offset plus `0x402200`.

The first marker maps `0x1C7128` → RVA `0x1C9328` → preferred VA `0x5C9328`;
the last maps `0x1CF9C5` → RVA `0x1D1BC5` → preferred VA `0x5D1BC5`.
All intermediate eighteen mappings were checked from the section table too.
Preferred PE addresses are not observed runtime addresses; relocation/load
behavior and reachability are not established by these calculations.

## Existing attribution evidence

The linked game ELF's flags `0x10A23001` and `MW MIPS C Compiler (2.4.1.01)` /
`PSP` comments describe a linked construction stage. In Bucket 3D, SNC objects
have the same flags but no exact original-probe matches under the tested
profile. In Bucket 3L, all eleven MW objects have flags `0x10970001` and comment
`MW MIPS C Compiler (3.0.0)`, despite producing two different complete code
groups. These retained observations directly show why flags and comments alone
do not select a compiler revision or identify every game unit.

The existing thirty-four-function Ghidra export and C++ runtime/demangler
strings remain bounded evidence. A runtime component, SDK wrapper, linker or
middleware producer cannot automatically be attributed to unrelated original
game units. No new game function was analyzed for this review.

## Checker controls and final report audit

The thirteen new tests use an invented PE32 image and known instruction bytes,
not compiler or game bytes. They cover:

- Exact supported PUSH, register MOV, C7 MOV and absolute LEA operand forms;
  precise immediate positions and ModRM/SIB/displacement lengths.
- Relocated data pointers, unsupported/prefixed instruction forms, uncovered
  relocation operands and matching values without relocations. None is promoted
  to a decoded code-reference candidate.
- Overlapping/unordered listing rows, byte drift, nonexecutable mappings and
  invalid instruction lengths; changed/nonterminated/duplicate markers.
- Invalid PE32 headers, section overlaps, image overflow, virtual-only tails,
  malformed/duplicate/unsupported relocation records and out-of-bounds spans.
- Binding the retained listing to the pinned decoder, exact static command and
  compiler identity; provenance drift, report aliases/conflicts, deterministic
  output and preservation of inputs. CLI tests execute neither decoder nor PE.

Review found that the initial C7 whitelist accepted some incorrect encoded
lengths, including a seven-byte register-immediate blob. The primary added exact
ModRM/SIB/displacement length checks; the negative and positive controls now
pass. This validates classification, not arbitrary x86 execution semantics.
Declared provenance also does not itself authenticate instruction boundaries;
the actual retained listing is independently reproduced below.

The helper ran the thirteen new tests under WSL Ubuntu: **13 passed, zero
skipped**. The complete tooling suite also passes: **296 tests, zero skipped**,
preserving all 283 earlier checks. These are not the required full-game gate's
eighteen negative tests, and no trace-neutrality check is claimed.

The helper independently parsed all **55987 HIGHLOW relocation records**,
rechecked the twenty exact marker mappings and verified all **27 reference
candidates** against their PE bytes and relocation operands. Every actual
candidate is a five-byte `PUSH imm32` instruction; no arbitrary matching DWORD
was accepted as a code reference. The helper also checked all **189 context
instruction records** against executable file-backed bytes. Marker reference
counts are one each for the first fourteen, then 4, 3, 1, 1, 3 and 1.

The retained report is **42792 bytes**, SHA-256
`0e8ae104dd85f96eccb0584c3acdf6f598d09e756ed9fc8902a257c3b3722a5b`.
The decoder listing is **27624804 bytes**, SHA-256
`00312d4c3e07a3966bb9e3d5703b7ded9d55d36d5f3b18ca8542264fb30714fa`.
The helper verified the native decoder's 415760 bytes and SHA-256
`44f07f8da860b15bd4dec909f229dec536595fb170a616fe3ab29c7b21c9736f`
against retained provenance. No compiler was invoked for these checks.

The helper then independently ran only that pinned GNU `objdump` static command,
capturing output in memory. It returned zero with empty stderr and reproduced
the entire retained listing byte for byte. Re-analysis using the hardened
checker reproduces the retained report exactly. This supplies genuine decoder
boundaries for the bounded static candidates without executing the compiler.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `scripts/inspect_compiler_trace.py` | 14350 | `42c9712696b3a2fd4f0a6a17ff1368b8f322ea67b9816968e90113b9409f51c7` |
| `tests/test_compiler_trace_feasibility.py` | 14049 | `69e054c2dc179feebb8916cf0c153c5ab2ffb4fc8002f04dbd301bf7c9521083` |

Twenty marker strings and twenty-seven supported static operands make a
bounded tracing investigation plausible. They do not establish live hooks,
internal IR/register layouts, pass ordering, O2 activation, a working debugger
transport or unchanged object output under instrumentation. No captured
optimizer/IR trace or instrumentation-neutrality result exists. No library/game
ownership, original compiler, selected flags or matching progress is inferred.
Stop at the Bucket 3M review checkpoint.

## Primary help-only debugger probes: read-only integration audit

The helper read both `help-probe-summary.json` and `help-probe-summary-2.json`,
their plans and retained streams, plus the second trial's GDB script and entry
observation. The helper reran no help command, compiler, debugger or test.
Both plans specify only `mwccpsp.exe -help` through the pinned runner; no source
or object output is requested. The helper independently verifies both plan
hashes, all retained stdout/stderr hashes, the current compiler/runner/GDB pins
and the second observation's equality to its summary.

Attempt 1 fails before launching the inferior: GDB reports no hardware-breakpoint
support at that stage, and produces no entry observation. Its summary remains
**INCONCLUSIVE**. Attempt 2 starts the runner first, then sets a hardware
breakpoint. The log records a stop at `0x401000`, with captured CS 7 and the
expected sixteen entry bytes `5589e56aff6898815d0068f011400064`; the helper checks
those bytes against the compiler's file-backed entry. However, the required
inferred-base header reads are `0000` for MZ and `00000000` for PE, with PE
offset zero. The script correctly requires every identity check before setting
`IDENTIFIED_COMPILER_ENTRY_REACHED`, so this observation also stays
**INCONCLUSIVE**. Matching PC and entry bytes do not waive the failed header
checks or establish the loader/guest-memory model.

The second ordinary and debugger-assisted help commands exit zero without
stderr. The ordinary help stdout is preserved verbatim inside the debugger
stdout, followed by a normal inferior exit. That verifies the retained help
observation, not optimizer reachability or unchanged compiled objects. No source
was compiled, no object was generated or compared for instrumentation neutrality,
and no IR/register trace was captured. All summary fields for source
compilation, game execution, object neutrality and IR validation remain false.
The static checker itself still never executes the compiler.
