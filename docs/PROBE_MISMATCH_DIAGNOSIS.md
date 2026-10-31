> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Diagnosis of two frozen compiler probes

Bucket 3B, 2026-10-30. Neither mismatch currently contradicts the probe's
ordinary-input behavior. The strongest observed differences are loop lowering,
induction variables, conditional moves and delay-slot scheduling. They do not
yet identify the historical compiler or flags. The source, manifest and original
matrix remain unchanged; no game function is credited as matched.

## Evidence and reproducibility

Inputs are the pinned main ELF and `evidence/eboot-v102.disasm.txt`, the frozen
bench and manifest, and the repeat-verified matrix under `evidence/bucket-03/`.
`verification-summary.json` identifies the object directories. Analysis used
`build/bench-bucket03-6dfxf3bd`; the objects listed below and their selected
symbol bytes were checked against the matrix's SHA-256 values before inspection.

For example, this reads an existing object without compiling or changing it:

```powershell
wsl -d Ubuntu -- mips-linux-gnu-objdump -d <project-root>/build/bench-bucket03-6dfxf3bd/0-2.o
```

Object names are zero-based candidate/setting indices from
`config/compiler-candidates.json`: `0-2.o` is build 121/O1, `0-4.o` is 121/O3,
`0-5.o` is 121/O4, `0-6.o` is 121/O4-p, `3-4.o` is 147/O3, and `5-4.o` and
`5-5.o` are 180/O3 and O4. `0-0.o` supplies an unoptimized comparison.
The system objdump is an inspection aid, not a selected build-tool component.
Game bytes and full disassembly stay local and ignored.

Both probes are non-exact in all 88 existing rows (eleven candidates, eight
settings). Sizes below summarize the whole matrix; equal size is not equality.

| Existing whole-bench setting | Six-byte target: 52 bytes | List-count target: 36 bytes |
| --- | ---: | ---: |
| default / O0 | 100 or 104 | 72 |
| O1 / O2 | 60 | 36 |
| O3 | 52 | 28 or 32 |
| O4 / O4-s | 56 | 28 or 32 |
| O4-p | 56 | 28 |

## Six-byte reduction: `0x08830550`

The 52-byte target reads exactly six consecutive signed bytes through `a0` and
returns zero if all are zero, otherwise one in `v0`. There is no early exit or
memory write. The target advances the pointer, increments a separate counter,
compares the counter with the fixed value six, and conditionally assigns one
using `movn`. The original signedness of the containing field and whether the
return type was `bool`, `int` or another zero/one convention remain unknown.

The frozen C scans six indexed elements and conditionally sets a local result.
Its ordinary-input semantics agree with those observations. Build 121/O1 and
O2 instead keep the base pointer, form `base + index` every iteration, test the
signed index against six with `slti`, and use a branch around assignment. O3
removes the entry jump and reaches 52 bytes, but still uses indexed addressing,
`slti` and a branch rather than the target's pointer induction, equality test
and `movn`. Builds 180 and later schedule branch-likely delay slots differently;
their 52-byte O3 shape is also not the target. O4 hoists a constant but still
does not produce the target control flow. This is more than register renaming.

The entry has 34 direct JAL sites. Static call-site review found the pointer in
`a0` and consumers testing `v0` for zero/nonzero. Examples include an incoming
argument at `0x0882DE4C`, arrays of records stepped by 332 bytes at
`0x0882E6CC`, a 332-byte record copy guarded by the result at `0x08831C40`,
and the two adjacent tests at `0x08835830`/`0x08835844`. Other contexts step
by 8, 12, 14, 144 or 168 bytes. The six tested bytes are therefore often a
prefix/subfield of a larger record, rather than a six-element allocation.
These contexts support a six-byte address/identifier validity test; they do not
establish the original name or owning library.

No caller passes an independently observed method receiver alongside the byte
pointer, and the callee reads no second argument or vtable. A C++ member whose
object begins with those bytes would still be possible. Changing language mode
or choosing an original prototype is not justified by these observations alone.

## Linked-list count: `0x08830654`

The 36-byte target initializes `v0` to zero, checks `a0` for null, then repeatedly
loads the next pointer from offset zero, increments the count and tests the
new pointer. It returns zero for null. No other node fields are touched. The
frozen `while (node != 0)` draft expresses that behavior for a valid terminating
list. Count signedness, typedefs, allocation ownership and cycle behavior are
not distinguished by the body.

All eleven O1/O2 objects produce the same 36-byte sequence, but its entry jumps
to the loop's bottom test instead of guarding entry and then testing after the
load/count body. The extra entry jump replaces the target's initial null guard;
equal size conceals different branch displacements and layout. O3/O4 can move
initialization or the next-pointer load into delay slots and use branch-likely;
O4-p places the count increment in a loop-branch delay slot. These shorter
28/32-byte forms remain semantically plausible and byte-different. There is no
call relocation or missing global symbol that could explain this leaf mismatch.

In the O1/O2 sequence, the initial result-clear instruction and the loop's
load/increment/back-edge/return instructions agree byte for byte with the target.
The sole differing instruction is at offset `0x04`: target `beqz` skips to the
return for null, while the object unconditionally branches to the bottom test.
The matrix therefore reports first differing byte four. This localizes the
list mismatch to loop-entry lowering rather than a node-layout or calling-ABI
disagreement; it still fails whole-interval byte equality.

Its only direct JAL caller is at `0x08830764`, in the function starting at
`0x088306D4`. The caller queries an imported peer-list API for a buffer length,
caps the local buffer at 2736 bytes, queries again with the buffer at `sp + 8`,
passes that list pointer in `a0`, and stores the returned count through its
second incoming pointer. It then calls `0x08830678`, which follows the same
offset-zero links and copies six bytes from node offset 132 to output records
with an eight-byte stride. This supplies a much stronger node interpretation
than an isolated generic pointer-chasing loop.

## Intervening code, imports and ownership

The surrounding helpers provide consistent address/peer context:

| Start | Static observation |
| --- | --- |
| `0x08830584` | Compares six bytes against a global address and returns comparison-nonzero. The global is outside file-backed section bytes; its value is not assumed. |
| `0x088305B4` | Compares two six-byte ranges and returns comparison-nonzero. |
| `0x088305DC` | Calls a copy-like helper with length six and returns zero. |
| `0x08830604` | Calls the WLAN address import into a local buffer, then copies six bytes on success. |
| `0x08830678` | Walks nodes and copies the six-byte field at offset 132. |
| `0x088306D4` | Retrieves a peer list, counts it, copies its addresses and calls another helper with the buffer/length. |

The main ELF's `.lib.stub` and NID arrays independently associate stub
`0x089610D0` with library `sceWlanDrv`, NID `0x0C622081`, and stub `0x08961110`
with `sceNetAdhocctl`, NID `0xE162CB14`. Public PSPSDK
[WLAN import declarations](https://github.com/pspdev/pspsdk/blob/master/src/wlan/sceWlanDrv.S)
and [adhoc-control import declarations](https://github.com/pspdev/pspsdk/blob/master/src/net/sceNetAdhocctl.S)
name those imports `sceWlanGetEtherAddr` and `sceNetAdhocctlGetPeerList`.
The [peer-list header](https://github.com/pspdev/pspsdk/blob/master/src/net/pspnet_adhocctl.h)
declares the length/output-buffer arguments and a peer prefix consisting of a
next pointer, 128-byte nickname and six-byte MAC address. That prefix agrees
with the observed offsets on PSP's 32-bit ABI. The header is community evidence;
its complete layout is not assumed to reproduce the game's historical SDK.

The imports are positively identified SDK interfaces. Calling them does not
identify the local wrappers or these two probes as Sony SDK code. They could
belong to game networking glue or another library; no matching library object,
original symbol, map file or source provenance has established ownership.
Adjacency supports a networking-helper cluster, not a proven translation unit.
Both probes remain unclassified, and the language/toolchain lock remains open.
If this cluster came from a separately compiled library, its compiler/settings
could differ from the game's own units; these probes alone cannot establish a
game-wide configuration.

## Ghidra cross-check

The initial export is `evidence/bucket-03b/ghidra-initial.json`, produced using
the PSP Executable ELF loader and `Allegrex:LE:32:default`. Its image base is
`0x08804000`, and the two target memory hashes agree with the frozen manifest.
The recovered target bodies end at `0x08830583` and `0x08830677`, agreeing with
the reviewed 52/36-byte intervals. It lists the same 34 reduction JAL sites in
26 distinct caller functions and the list helper's one caller at
`0x088306D4`. All 34 selected target/caller/neighbor decompilations completed.

Ghidra recovers a six-iteration, pointer-advancing byte scan and a null-terminated
offset-zero pointer count. Its peer-list caller and neighboring six-byte copy
agree with the independently reviewed assembly. Its output supports the existing
ordinary-input semantics; it supplies no original symbol, library attribution,
historical compiler setting or language evidence. In particular, its choice of
a `for` loop for the list helper does not recover the original spelling or
explain why the frozen compiler output uses a different loop-entry branch.

Automatic types need care. The export's `signature_hypothesis` fields still say
generic `undefined FUN_x()` even when pseudocode headers infer parameters and
return values. Some caller pseudocode omits a pointer argument: for example,
`0x0882DE24` displays a no-argument call to the byte probe although the assembly
passes its incoming `a0` pointer. Other callers and the target pseudocode show
the pointer. The inferred `int *` list is a raw pointer-to-first-word model,
not a recovered peer struct; inferred `int` versus `undefined4` results do not
settle signedness. Treat call-site registers and verified memory reads as the
evidence when these displays disagree.

The primary agent owns fresh-project repetition and the final analysis wrapper's
validation. Loader/analysis warnings concern unloaded overlay references and an
uninitialized address; completed selected decompilations do not prove a complete
or correctly typed whole-program analysis. No pseudocode has been promoted to
game source, and no additional overlay was recovered.

No new compiler configuration or source alternative was run for this diagnosis.
A justified later experiment would separately declare natural loop/prototype
hypotheses and test them across a fixed whole-bench configuration; current
results do not authorize per-function flags or source shaping to improve scores.
