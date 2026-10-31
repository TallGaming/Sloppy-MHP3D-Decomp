> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Compiler trace feasibility review — Bucket 3M

This is a static feasibility review and an audit of bounded help-only host
checks, not a compiler-stage trace or another compilation.
The existing unmodified PSP Metrowerks 219 under pinned wibo is a plausible
subject for future investigation. The public PS2 debugger is a useful design
reference, but it supplies neither a supported PSP profile nor a validated
wibo capture path. No original compiler pass, AST or register-allocation state
has been observed by this review.

## Reviewed identities and support boundary

The public debugger snapshot is
[`Raikaru/mwccps2-debugger@5ea1631d07e62d1aa48cf28b373a1c6315be665b`](https://github.com/Raikaru/mwccps2-debugger/tree/5ea1631d07e62d1aa48cf28b373a1c6315be665b).
Its documented live profiles concern particular **MWCCPS2** executables.
The b210 profile, for example, binds `mwccps2.exe` to SHA-256
`286548490e2e902cfef21dcf39cd5af23766731585d90dea747f8781eadcafd7`.
That is not our PSP219 executable. Nearby version numbers and shared diagnostic
strings do not establish interchangeable globals, instruction records or hooks.
The repository also describes a separately prepared PS2 2.4 profile; that
preparation is outside our unmodified-tool scope.
[README](https://github.com/Raikaru/mwccps2-debugger/blob/5ea1631d07e62d1aa48cf28b373a1c6315be665b/README.md),
[b210 identity and layout](https://github.com/Raikaru/mwccps2-debugger/blob/5ea1631d07e62d1aa48cf28b373a1c6315be665b/profiles/mwcps2-3.0.1-b210.json).

Our existing `config/compiler-candidates.json` pins the **x86_64** wibo 1.2.0
runner, 7,256,672 bytes, SHA-256
`13f86a2d618f0dbe67179d349625345eabf9b46450295cb4c904e49f6aff85af`.
Its public source tag resolves to
[`c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a`](https://github.com/decompals/wibo/tree/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a).
This source inspection does not prove a reproducible source-to-release-binary
build. Prior successful compiler runs establish the pinned runner's usefulness
for compilation; they do not establish tracing support.

## What the public collector actually requires

The public collector binds executable identity, loaded-image checks, stage
addresses, globals and structure layouts. It uses GDB Python to install
auto-continuing breakpoints, read inferior memory and obtain stack information
from `$esp`. A PSP port needs independently established function identity,
entry/return conventions, pointer widths, record fields, block/instruction
links and opcode/operand interpretation. Public PS2 offsets must remain
untrusted for PSP until checked. Bounds, cycle checks and unknown-field handling
are useful reusable principles, rather than proof of identical IR.
[Collector](https://github.com/Raikaru/mwccps2-debugger/blob/5ea1631d07e62d1aa48cf28b373a1c6315be665b/gdb/mwccps2_b210_snapshot.py),
[bounded model](https://github.com/Raikaru/mwccps2-debugger/blob/5ea1631d07e62d1aa48cf28b373a1c6315be665b/gdb/b210_snapshot_model.py).

Its transport implementation accepts Windows-native GDB and retrowin32 command
construction. Wine/wibo capability checks deliberately report
`validated_for_b210_gdb_snapshots = False`, including after successful tool
launch. There is no implemented wibo capture transport in this snapshot.
Launching GDB itself through wibo, or having a working `gdb --version`, would
not establish a working compiler/inferior capture pair.
[Transport](https://github.com/Raikaru/mwccps2-debugger/blob/5ea1631d07e62d1aa48cf28b373a1c6315be665b/transports/gdb.py),
[capability boundary](https://github.com/Raikaru/mwccps2-debugger/blob/5ea1631d07e62d1aa48cf28b373a1c6315be665b/transports/capabilities.py#L82-L107).

The architecture requires identity validation before hooks and comparison of
complete direct versus instrumented object bytes. A missing pass remains
missing: an optimization level need not invoke every scheduler hook. Even a
successful candidate trace cannot recover the retail game's historical compiler
state. This review does not adopt the public project's automatic source search.
[Architecture and extension requirements](https://github.com/Raikaru/mwccps2-debugger/blob/5ea1631d07e62d1aa48cf28b373a1c6315be665b/docs/architecture.md).

## Why Linux GDB plus wibo is plausible, and still unproven

Wibo maps a PE image into its own process, resolves imports/TLS, then invokes
the guest entry point. This makes host-debugger observation of guest addresses
conceptually possible; it is not an emulated PSP program. The compiler itself
is host x86 code, and its generated MIPS instructions are data being analyzed.
[Guest entry](https://github.com/decompals/wibo/blob/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a/src/main.cpp#L441-L477).

Two concrete issues prevent assuming the public command works unchanged:

- Wibo tries the PE preferred base but permits another allocation and applies
  relocations. Hooks must use verified live mappings, not assumed absolute VAs.
  A debugger stopped at its own loader entry has not yet reached a loaded
  compiler. The public `file compiler.exe; starti` sequence is not a Linux
  wibo-loader transport.
  [PE allocation and relocation](https://github.com/decompals/wibo/blob/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a/src/loader.cpp#L430-L454).
- The x64 runner makes far jumps into 32-bit guest code and maintains guest
  stack/segment state. A future GDB must interpret instruction bytes, PC,
  arguments, stack and pointers correctly at guest stops and across host API
  transitions. Whether the installed WSL/GDB combination does this correctly,
  and permits the required tracing, has not been tested here.
  [Mode transitions](https://github.com/decompals/wibo/blob/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a/src/setup.S#L9-L54),
  [Linux guest segment setup](https://github.com/decompals/wibo/blob/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a/src/setup_linux.cpp).

Wibo's debug logging is wrapper/API diagnostics, not a compiler IR trace.
Its `IsDebuggerPresent` stub returns false; that neither prevents a Linux
debugger attaching nor proves attachment works. No debugger-installation,
host-permission or exception-handling compatibility claim follows from that
stub.
[Debug API implementation](https://github.com/decompals/wibo/blob/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a/dll/kernel32/debugapi.cpp#L8-L11).

## Static hooks versus a future capture

The local `evidence/bucket-03m/static-reference-candidates.json` report records
twenty selected markers and 27 `DECODED_RELOCATED_LABEL_OPERAND` references.
Every accepted reference in this actual image is a `PUSH_IMM32`; the analyzer's
broader whitelist does not mean those other forms were observed. The report
requires a file-backed PE mapping, a HIGHLOW relocation at the operand, an
objdump-decoded instruction boundary, matching raw instruction bytes and a
characterized opcode form. The independent review read the unchanged compiler
SHA-256 as `828f9b30b3ae33c7a0202c2baf48aab49884c60e48c5b3daa2436bc3237368df`.
The report SHA-256 is
`0e8ae104dd85f96eccb0584c3acdf6f598d09e756ed9fc8902a257c3b3722a5b`.

For example, the selected ordinary common-subexpression marker has references
at preferred VAs `0x004AF7CC`, `0x004AF8DC` and `0x004AF98C`; the ordinary
propagation marker has three different references. Multiple uses make a string
insufficient to select a unique pass boundary. Linear decoding and immediate
relocation corroborate these operands without establishing reachability,
containing-function boundaries or pass activation.

A diagnostic string and a machine-code reference are **candidate anchors**.
Even a recognizable sequence naming common-subexpression removal, propagation,
peephole optimization or scheduling does not prove the hook's before/after
position, which optimization levels execute it, the current-function pointer,
or the associated IR layout. Nor does it establish which pass caused our
five-versus-one address-base difference.

### Help-only transport check: method reviewed before execution

The updated 3M plan permits a declared bounded host capability check. One
hardware breakpoint at the preferred PE entry, while the existing compiler
receives only its documented help request under unchanged wibo, is coherent
for that limited purpose. The reviewer independently reads entry RVA `0x1000`,
preferred VA `0x00401000`, and its first sixteen file-backed bytes as
`5589e56aff6898815d0068f011400064`. A meaningful positive observation needs
matching live PE headers/base and entry bytes as well as PC/CS, exact debugger
and invocation provenance, bounded continuation and normal help completion.
A hit at that numeric address alone is insufficient identification. A relocated
image, missing hit, ptrace restriction or unsupported register presentation
must remain a bounded negative/inconclusive outcome rather than proof that
tracing is impossible. Hardware breakpoints avoid patching guest instructions.
No source is compiled and no object-neutrality claim is possible from help.
This paragraph preserves the proposed method before its results below.

### Retained outcomes and independent audit

Attempt 1, recorded in `evidence/bucket-03m/help-probe-summary.json`, fails
before inferior launch: GDB rejects the hardware breakpoint without a live
target. Its message is `No hardware breakpoint support in the target.` This
does not establish that hardware breakpoints are unavailable after launch.

Attempt 2 was separately declared in `help-probe-plan-2.json` (SHA-256
`c4ba430ea1687cec2dc79efa9d7b0faa2b2cc50cc99a05b8e41daa4519b3ca97`).
It starts wibo with `starti`, then sets the hardware breakpoint and continues.
The retained `build/compiler-trace-help-pcbhgjq6/probe.gdb`,
`debugger-help.stdout` and `entry-observation.json` agree with
`evidence/bucket-03m/help-probe-summary-2.json`:

- GDB logs breakpoint 1 at `0x00401000`; the observation records PC
  `0x00401000`, CS `7` and the exact expected sixteen entry bytes.
- Both ordinary and debugger-assisted help invocations exit 0 without timeout.
  The complete ordinary stdout occurs verbatim inside the debugger stdout;
  their hashes agree with the summary. Current compiler and wibo hashes still
  match their pins. The summary records the debugger unchanged as well.
- The inferred base is `0x00400000`, but the live DOS magic and PE signature
  are zero. Therefore the required image identity remains **INCONCLUSIVE**.
  The observed CS is a selector value, not independent validation of its
  descriptor, all guest registers or stack decoding.

The zero headers have a specific public-source explanation: pinned wibo
`loader.cpp:455` zeroes the allocated image; lines 459–465 record header-page
protection, and lines 477–515 load section payloads without copying the PE
headers into that span. This source behavior is consistent with the observation.
It neither proves source-to-release-binary equivalence nor satisfies the
predeclared header criterion after the fact.
[Exact loader code](https://github.com/decompals/wibo/blob/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a/src/loader.cpp#L455-L515).

The result is a genuine narrow positive observation—hardware stopping at the
expected code bytes while help completes—inside an inconclusive identity check.
It is not a verified PSP optimizer hook, decoded IR capture or object-neutrality
test. No source/object was generated and no game ran. The existing criterion
was retained, and no additional probe was performed by this helper or requested
as part of this review. A future identity method would need its own prior
review rather than relabeling this result.

If separately approved, a later compilation trace should establish only a
bounded transport contract on an invented fixture: identify the exact loaded
compiler, reach one validated guest hook, read a bounded known memory/argument
record with correct widths, complete successfully, and reproduce the complete
ordinary object's bytes. Failure, unvalidated mappings or unsupported register
interpretation must produce no trace conclusion. Full IR/scheduler capture
would require another reviewed PSP-specific profile after that prerequisite.

This helper performed none of those live steps or the proposed help probe.
No binary preparation, installation, changed flags, source revision, match
credit or toolchain lock is implied. Local static hook evidence is integrated
by the primary's Bucket 3M report; this document assesses its public-source and
host prerequisites rather than substituting PS2 layouts for local evidence.
