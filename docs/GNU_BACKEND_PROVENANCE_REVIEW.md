> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# GNU backend provenance review — Bucket 3Y

This bounded review separates upstream compiler features, PSP build leads and
actual retained assembly. It changes no flags, source forms or tool binaries.
The original initializer remains PARKED; no original function is compiled or
compared in this bucket.

## Bounded primary-source scope

Initially two upstream files were examined at each of three pinned releases:
`gcc/config/mips/mips.c` and `gcc/reorg.c`. Their complete public text, URLs,
byte counts and SHA-256 values are recorded under `helper-map-*` in
`evidence/bucket-03y/helper-map-public-sources.json`. Annotated release tags
were dereferenced to actual commits before fetching files. Two narrow recorded
scope amendments then permitted the directly required3.3.3 and3.4.6 MIPS target
headers, bringing the backend-source total to eight. No broader source query or
compiler experiment followed from those amendments.

| Release | Exact upstream commit | MIPS backend / delay reorganization |
| --- | --- | --- |
| 3.3.3 | `0cf7278b8ebcf154c6c9ee8977cdb1aafa599111` | [mips.c](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/config/mips/mips.c), [reorg.c](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/reorg.c) |
| 3.4.6 | `6018a82534694970fb27a6846b15d370b392085f` | [mips.c](https://github.com/gcc-mirror/gcc/blob/6018a82534694970fb27a6846b15d370b392085f/gcc/config/mips/mips.c), [reorg.c](https://github.com/gcc-mirror/gcc/blob/6018a82534694970fb27a6846b15d370b392085f/gcc/reorg.c) |
| 4.3.5 | `ec031872b213f39e5e82019408c79cf6cca010d1` | [mips.c](https://github.com/gcc-mirror/gcc/blob/ec031872b213f39e5e82019408c79cf6cca010d1/gcc/config/mips/mips.c), [reorg.c](https://github.com/gcc-mirror/gcc/blob/ec031872b213f39e5e82019408c79cf6cca010d1/gcc/reorg.c) |

In upstream3.3.3, `mips_move_1word` can print integer constants as `li`
pseudoinstructions (mips.c:2278–2290); the final encoding can therefore involve
assembler expansion. Its generic `dbr_schedule` explicitly searches for delay
slot fills using simple/eager filling and relaxation (reorg.c:3613–3618,
3695–3706). No MIPS sibling-call hook appears in this selected backend file;
that absence alone does not establish every target configuration's behavior.

Upstream3.4.6 has an explicit `mips_add_offset` path that leaves a
sixteen-bit low displacement and materializes the excess high part
(mips.c:1789–1848). `mips_move_integer` constructs constants from a sequence
chosen by `mips_build_integer` (1960–1982). Its sibling-call hook returns the
target's eligibility condition (3366–3373); explicit-relocation operation moves
delay scheduling into target reorganization (4952–4958). These are capabilities
and conditional paths, not a prediction that an arbitrary C expression uses one.

Upstream4.3.5 retains the high/low offset split and constructed integer moves
(mips.c:2306–2333,2491–2519). Its sibling-call hook additionally checks ISA-mode
interworking conditions (5628–5655). The MIPS reorganization calls
`dbr_schedule` conditionally (11558–11566), while generic reorg.c:4049–4066
contains its delayed-branch gate/pass. Delay filling is thus a compiler activity
in these sources, not inherently an assembler-only transformation.

The official [GCC3.4 MIPS release notes](https://gcc.gnu.org/gcc-3.4/changes.html#MIPS)
describe substantial backend changes and sibling jumps enabled in the explicit-
relocation abicalls context. That context must not be generalized into proof of
PSP EABI defaults or a claim that one version always tail-calls. Target macros,
machine-description patterns and vendor patches are outside this bounded scope;
the selected files do not prove complete source-to-installed-binary provenance.

The two added headers provide a specific algorithm distinction. In3.3.3,
[`mips.h:3239–3253`](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/config/mips/mips.h#L3239)
implements large register-plus-constant addressing by materializing
`offset & ~0x7fff` and leaving `offset & 0x7fff` in the memory operand.
For the earlier3X offset`0x2F53C`, that is exactly`0x28000 + 0x753C`.
For this bucket's invented offset`0x1A120`, it gives`0x18000 + 0x2120`.
These predictions agree with the previously observed3X and current retained
fixture outputs without proving the installed vendor backend's source identity.

In3.4.6,
[`mips.h:1983–1987`](https://github.com/gcc-mirror/gcc/blob/6018a82534694970fb27a6846b15d370b392085f/gcc/config/mips/mips.h#L1983)
defines high as`(value + 0x8000) & ~0xffff`, and low as`value - high`.
Combined with the inspected`mips_add_offset`, this permits`0x30000 - 0xAC4`
for`0x2F53C`, the canonical high/signed-low decomposition seen in the earlier
original target. Its
[`TARGET_SIBCALLS` condition](https://github.com/gcc-mirror/gcc/blob/6018a82534694970fb27a6846b15d370b392085f/gcc/config/mips/mips.h#L289)
also explicitly depends on MIPS16, abicalls and explicit-relocation context.
The formulas and capability condition are source facts; actual expression
lowering, vendor patches and whole-program compiler attribution remain unproved.

## Verified PSP version lead

The community Minimalist PSPSDK build recipe at
[`pmlopes/minpsp@cfc3435509fefb0e05cb55acf2c2deb34b592399`](https://github.com/pmlopes/minpsp/blob/cfc3435509fefb0e05cb55acf2c2deb34b592399/toolchain.sh)
explicitly selects GCC4.3.5 and PSPSDK0.10.1. Its commit timestamp is
`2010-11-26T12:47:11Z`. The reviewer pinned this dated build metadata in
`helper-map-minpsp-pre_release-source.json`; a later2013 snapshot still selects
GCC4.3.5. This is a concrete contemporaneous community PSP recipe, not a verified
installed binary, complete patched source closure or evidence that Capcom/Sony
used it. No compiler archive was acquired or built. The3.4.6 source comparison
is an upstream feature baseline, not a verified PSP compiler release lead.

## Capture path reviewed before execution

The existing invented `bench/address_reuse_grouped.cpp` stays1,200 bytes,
SHA-256 `04662faba3e8e68506928bb2d2623d25cf5e6a93f8f9fb1bde3e3dd223908094`.
It has invented offsets/defaults, not the parked original initializer's body.
The exact existing GNU cc1plus/O2 and diagnostic assembler profile is inherited
from3W without changing any option or source byte.

The reviewer approved the profile `config/gnu-assembly-capture.json`,1,011 bytes,
SHA-256 `0d0e70fe7629a9f76a7f51083270b5219a09533f9d656cdb092c4e11cc29a262`,
and ignored driver `evidence/bucket-03y/capture_gnu_assembly.py`,11,374 bytes,
SHA-256 `043bf0c4caebc7b8c2d669afcae88f5ad4a7d2ba29f6769585829eb791f7a4b5`.
The capture path mirrors ordinary native/tmp staging, source basename,
`probe.s`, argv/cwd/timeouts and assembler invocation. It adds only a read/copy
of assembly. Input/staged-source/assembly/output identities, links, earlier
outputs and partial failures are checked; decoder uncertainty is explicit.
Both reviews and a freeze must precede exactly four invented compilations.

## Retained capture and instruction attribution

Both approvals preceded the freeze at`2026-10-31T07:40:01.120626+00:00`.
The retained freeze is871 bytes, SHA-256
`bb617549ec8d2172a94e86e19f6d7bf1afb306e0456cf01ccbae917f0f500e79`.
Both ordinary/capture pairs complete successfully in fresh directories
`build/gnu-assembly-capture-cjxdcgvg` and
`build/gnu-assembly-capture-4nu26rfp`. The reviewer independently compared all
four complete objects, both verbatim assembly copies and their report/freeze
identities. Every object is identical:1,204 bytes, SHA-256
`22690e399773b59c25a0b3966312c5f6465c9d96690d5a91dba274b78ee80523`.
Both captured assemblies are995 bytes, SHA-256
`9c1aabe61e5c0de8e02071f3759d294a1936833266514bd964d17281512a1078`;
ordinary-path assembly hashes agree. Frozen inputs remain unchanged.

The complete64-byte function has SHA-256
`938610c5f086bf6422c724621a7955766f22fd3fc156e7fd68a2fadc7182be4e`.
The raw compiler output already specifies`li $2,65536`, ORI`0x8000` and ADDU,
then field displacements8480/8484. Consequently the selected`0x18000` base
and positive low offsets exist before assembly. The assembler encodes the
single-instruction LI as LUI; it did not invent the overall base/offset split.
No MOVE pseudo appears, so this fixture supplies no empirical MOVE-expansion
comparison.

Both conditional BNE/default-LI pairs already appear together in the compiler's
assembly under`.set noreorder` and`.set nomacro`. Their placement is therefore
compiler output, rather than newly scheduled assembler behavior in this run.
Conversely the final`j $31` appears under reorder with no explicit delay NOP;
the complete object's final NOP is added during assembly. The commented`#nop`
near the volatile load is not an emitted instruction. These distinctions show
why compiler output and assembler output must both be retained. No extra flag
or assembler experiment was needed or performed.

The reports are3,451 bytes each: trial1 SHA-256
`21cddb1b1f29c6e485385eec99a2502d531ac896fe8d30e0723780c1a0389b84`,
trial2 SHA-256
`3ade8a7bcd903fbe74a6f7b5afd07d4244aacf7082d559e53a56872cdf9d3a1f`.
All compiler/assembler stages and decoders return zero without diagnostics.
The captured function contains no calls, so it does not empirically test
sibling-call eligibility or explain every earlier original/fixture call choice.

## Citation correction and bounded conclusion

The closed3V review's source content/hashes remain valid, but its line counting
used Python`splitlines()`, which treats GCC form-feed page separators as extra
lines. GitHub anchors count newline characters. Citation-only replay of the
same pinned3V sources establishes the corrected anchors:
[`decl2.c:2228`](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/cp/decl2.c#L2228)
for parameter identifiers,2233 for the helper-name definition,2459 for the
selector/priority guard,2675 for wrapper generation;
[`tree.h:1608`](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/tree.h#L1608)
for default priority65535; and
[`tree.c:4372`](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/tree.c#L4372)
for file-function naming. The correction is retained in
`helper-map-3v-citation-erratum.json`; no closed3V artifact was rewritten and no
semantic finding changes. All3Y line references use newline-only counting.

There is now source-backed reason to distinguish pre/post3.4 MIPS address
algorithms and investigate a contemporaneous PSP4.3.5 build lead. There is no
evidence yet that a newly provisioned compiler reproduces the original code,
and no binary was acquired or tested. Target NOPs do not identify a historical
optimization default; tail jumps do not uniquely identify a frontend version.
No per-function flag adjustment, source revision, compiler lock or match credit
follows. The helper performed static/public-text review and retained-byte checks
only; no compiler or game was executed by this helper.
