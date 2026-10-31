> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Compiler transport identity review — Bucket 3U

This review covers a separately declared help-only transport check using the
existing unmodified MW219 compiler, wibo and host GDB. It authorizes no source
compilation, optimizer hook, IR capture, binary patch or game execution. Bucket
3M's header-based identity result remains INCONCLUSIVE; a later contract does
not retroactively change it.

## Loader-aware rationale

The pinned public wibo source is
[`c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a`](https://github.com/decompals/wibo/tree/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a).
Its loader first attempts the preferred image base, permits another allocation,
zero-fills the image and copies raw section payloads into their mapped RVAs.
It records protection for the header span without copying the original PE
headers there. When necessary it applies relocations. These source facts
explain why a file-backed section comparison is more appropriate than requiring
live MZ/PE signatures for this new check; they do not establish equivalence of
the public source and the pinned release binary.
[Allocation and section loading](https://github.com/decompals/wibo/blob/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a/src/loader.cpp#L408-L487),
[relocation handling](https://github.com/decompals/wibo/blob/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a/src/loader.cpp#L518-L558).

The x86-64 runner's Linux setup switches to the guest stack and enters 32-bit
code using a far jump before returning to host mode. This makes guest register
width an observation to verify rather than an assumption from the host debugger
architecture. A selector value alone does not prove its descriptor or operand
size. [Pinned setup source](https://github.com/decompals/wibo/blob/c1a7d472bd49e5dbaf3fe9aec272461b2e12f68a/src/setup.S#L9-L48).

## Contract assessed before execution

Require the preferred entry at `0x00401000`, exact entire file-backed `.text`
bytes and three predetermined marker strings at file-derived preferred VAs.
No relocation adjustment, ignored mismatch or partial section success is
allowed. Record PC, CS and guest-width registers. A relocated image, unsupported
memory read or missed stop remains INCONCLUSIVE under this bounded contract.

Only after identity succeeds, remove the hardware breakpoint and single-step
the known entry byte `0x55`. Require PC to advance by one, ESP to decrease by
four and the new four-byte stack value to equal the previous low 32 bits of EBP.
This observes one PUSH's behavior without modifying registers or inserting a
software breakpoint. It does not validate later argument decoding, host/API
transitions or any optimizer-stage record layout.

Two fresh trials must each finish ordinary and debugger-assisted help with
exit zero, no timeout/error, complete ordinary output present in the debugger
output, explicit inferior exit zero, and unchanged compiler/runner/debugger
identities before and after. No source or output-object neutrality inference
can follow from help-only invocations. Exact profile/driver review and retained
outcomes will be recorded below once available.

The independent static readback confirms `.text` at file offset `0x400`,
preferred VA `0x00401000`, with 1,702,912 raw bytes and SHA-256
`11ebae9224311b84b66986f5804059204e41592afef1009b1093bcdfea27e550`.
Its first byte is `0x55`. The three preselected complete NUL-terminated strings
and file-backed preferred addresses agree with the pinned compiler:

| Marker | File offset | Preferred VA | Bytes including NUL |
| --- | --- | --- | ---: |
| After IR Optimization | `0x1C7128` | `0x005C9328` | 22 |
| After removecommonsubexpressions | `0x1CE570` | `0x005D0770` | 33 |
| After propagatecopyinstructions | `0x1CE5D9` | `0x005D07D9` | 32 |

The proposed GDB script starts the existing runner first, installs the hardware
entry breakpoint, reads the entire declared text span and markers, and checks
identity before the single step. It deletes breakpoints before stepping,
captures four stack bytes, continues under normal signal policy, records exit
events and independently checks output containment and process completion.
The pinned CS value seven is an additional supported-transport restriction,
not the sole evidence of instruction width.

Pre-execution review found static PE/marker checks written as Python assertions
without rejecting optimized Python. Before freeze, the primary replaced these
with explicit ValueError checks, added a complete raw-text identity check and
strengthened integer-width checks. The POSIX execution guard now follows pure
static validation but still precedes directory creation and all process launch.
The reviewer read back that final change and the eleven invented controls,
including rejection of a wrong mapping under optimized Python. No live
execution preceded the final approval.

Approved exact pre-execution inputs:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `scripts/probe_compiler_transport.py` | 14,332 | `a1192eb0f9e6bd84eed89b29721b014880ac77eaf65ad41dccfd208a18ab9352` |
| `config/compiler-transport.json` | 1,980 | `488194115646ddfd7d6babaabf68defe6c5f6b5f1b6a53b3fa1fc9b7f2556033` |
| `tests/test_compiler_transport.py` | 12,904 | `2c683e07acb1db57a21e15eb31ad66db93fbf6600fb2c09ac945d25293de24b8` |

## Retained outcomes and independent audit

Both exact approvals preceded the freeze at
`2026-10-31T06:50:11.696723+00:00`. The retained
`evidence/bucket-03u/profile-freeze.json` is 1,230 bytes, SHA-256
`6130ac2479474096d16860adbb738a45151c75763389c6504f7e4f5e9efdd574`.
The reviewer rehashed its complete required input set after both trials; all
four files, including the inherited PE parser, remain unchanged.

| Trial | Fresh retained directory | Report SHA-256 (3,023 bytes each) |
| --- | --- | --- |
| 1 | `build/compiler-transport-xbwdlv2a` | `21a274a867ba817e1e9b255b6af091ac4a14bdfadb81a144de6f4badf98b5cf7` |
| 2 | `build/compiler-transport-c8v91xbl` | `24453c21cbce89b2bfb02b735139c46579a3126952d235fc050ad6c39e670cc6` |

Both reports satisfy **VERIFIED_BOUNDED_TRANSPORT** under the new contract.
The reviewer independently compared each retained 1,702,912-byte
`live-text.bin` directly with the pinned executable's entire raw `.text`,
not just with the reported hash. The three complete marker identities agree;
both stops report PC `0x00401000`, CS seven and entry byte `0x55`.

The single CPU step advances PC to `0x00401001`, changes ESP from
`0x7FFF0FFC` to `0x7FFF0FF8`, and reads four saved bytes equal to the previous
EBP `0x7FFF1000`. The logs show the hardware breakpoint and subsequent normal
inferior exit; retained observations agree with the reports. Generated scripts
have exactly one stepi and delete the breakpoint before it. No error or
unexpected signal is recorded. The live header prefix remains zero, as recorded
separately from the new executable-section identity criterion.

Each ordinary invocation yields the pinned 31,584-byte help output, SHA-256
`539587cda84463e05efa58667977ee77a81ac8238f03b3ac0d09cf05be248ce6`.
The reviewer read and hashed all ordinary/debugger stdout/stderr artifacts,
checked complete byte-for-byte output containment, and matched observations
and freeze identities to each report. Both invocations in both trials exit
zero without timeout or stderr. Debugger envelope hashes differ because process
IDs differ; their substantive observations agree. Tool identities are recorded
unchanged before/after. Primary reports the full WSL suite at 340 passing tests
with zero skips; the Windows run has two explicitly native-only skips.

This establishes exact executable-section/marker identity and observation of
one guest instruction's four-byte stack effect in the present host transport.
It does not identify or exercise an optimizer hook, validate PSP IR structures,
prove compiler neutrality while compiling source, prove reproducible runner
source-to-binary provenance, or identify the original game's compiler. The
historical 3M result remains INCONCLUSIVE under its original header criterion.
No source/object was generated, no game ran, no matching credit was granted,
and the parked initializer remains untouched. This helper performed only
static source/artifact review, never the live invocations.
