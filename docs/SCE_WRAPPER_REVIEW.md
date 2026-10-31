> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Declared SCE-wrapper review — Bucket 3AD

Stage A uses the four retained raw containers and offset-zero OPNSSMP metadata.
It performs no decryption or module execution. Any later decryption-helper
stage requires successful Stage A audits and its own exact review/freeze.

## Pinned public loader model and limits

The exact public source is
[`hrydgard/ppsspp@c0fd904feefedc66441d4d5d602e46d2fd8e4fd6`, Core/HLE/sceKernelModule.cpp](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/HLE/sceKernelModule.cpp).
The reviewer cached its161,724-byte text at
`evidence/bucket-03ad/helper-map-ppsspp-sceKernelModule.cpp.txt`, SHA-256
`457010fded39ca050064149bcf35016c7fec98eee14e1893fb56b8f3261e5142`.
The adjacent `helper-map-loader-source.json` records URL/commit/hash; all line
references count LF newlines only.

The loader rejects original buffers shorter than eight bytes
([1606–1614](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/HLE/sceKernelModule.cpp#L1606)).
For`~SCE` it reads a little-endian unsigned32-bit proposed header length at+4;
when that value is smaller than the original buffer length it advances by the
declared value and reduces the remaining length
([1630–1638](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/HLE/sceKernelModule.cpp#L1630)).
It then checks the next signature and a complete PSP-header size before taking
its encrypted-PSP path
([1644–1647](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/HLE/sceKernelModule.cpp#L1644)).

This source supplies a declared-offset model, not a universal0x40 wrapper or
proof that our entries are valid modules. The shown branch does not itself
establish a positive/minimum declared wrapper length or safe remaining bytes
for every later read. Our bounded parser must independently reject malformed
lengths and require a complete exact-offset0x150-byte`~PSP` header before
eligibility. No magic search, guessed offset, field repair or wrapper library-
info decoding is justified. This external emulator code is not evidence of
original-game runtime behavior or SDK ownership.

## Stage A contract before implementation outputs

Require both preserved3AC sets and their complete raw input identities to agree.
Interpret the length only after original magic/size checks, bound the unsigned
value strictly inside its payload and preserve its declared value. Record the
exact declared wrapper and remaining-byte identities. An unsupported inner
signature or short header remains uninterpreted and ineligible; declared names,
tags and sizes are unauthenticated metadata rather than recovered code extents.

OPNSSMP is a separate offset-zero candidate; main EBOOT remains a positive
reference control. Neither is silently substituted for an archive entry.
Two fresh Stage A reports/copies must preserve the exact selected bytes and all
source/toolchain/assembly locks. Public source and parser/profile pins must be
frozen after both reviews and before real evaluation. Stage B remains unstarted
until its own prerequisite audit and explicit frozen contract.

Exact script/profile review and retained outcomes will be recorded below.

## Exact Stage A review before evaluation

The reviewer approved profile`config/sce-wrapper-model.json`,1,516 bytes,
SHA-256 `abc44e51d6f922ab55100b6b985b90c31cadbdab204a820aea2690b66413a841`,
and final ignored driver`inspect_sce_wrappers.py`,9,192 bytes, SHA-256
`e0fcc53579404af4ea6f6b2f68683c76a69352e936aaadc59cac6b7739331b99`.
The unsigned declared length must be positive, at most the local1MiB bound and
strictly smaller than the original payload. The actual remaining bytes are
copied verbatim even when their format is unsupported; only complete exact-
offset`~PSP` headers become eligible. No convenient inner magic is searched for.

The source verifies both complete supplemental sets and all sixteen payload
copies first, pins the helper header/public-loader source and preserves all
earlier game/compiler/assembly inputs through inherited guards. OPNSSMP remains
a separate offset-zero candidate. Temporary output is an exact fresh set plus
manifest, audited before one same-parent rename. External report publication
occurs afterward and is a separate atomic operation.

Before freeze, review added a final original-snapshot recheck after late input
verification and full report-parent path-chain validation before exclusive
report creation. This reviewer read back and approved those corrections before
real evaluation. The stage does not invoke a decryption helper or any module;
Stage B still needs both output audits and a separate exact contract/freeze.

## Stage A retained-output audit

Both fresh sets at`reference/uljm05800-v102/sce-wrapper-sets/run-1` and`run-2`
contain five exact candidate files and their manifest. The reviewer independently
read each original raw input's length field, compared the complete remainder
bytes with both output copies, checked all raw PSP name/tag fields and verified
the final freeze pins. Both manifests and external reports are identical9,016-
byte JSON, SHA-256
`8405266c9100e45d0bab3c8c34600ee4e9575001abeae4a05cb52d463c17e105`.

| Input | Actual declared offset | Remaining bytes | Declared PSP name / tag |
| --- | ---: | ---: | --- |
| Archive17 | 64 | 20,624 | `sceFont_Library` / `457B06F0` |
| Archive18 | 64 | 1,056 | `sceBASE64_Library` / `457B06F0` |
| Archive19 | 64 | 20,624 | `sceFont_Library` / `457B06F0` |
| Archive20 | 64 | 1,056 | `sceBASE64_Library` / `457B06F0` |
| OPNSSMP | 0, standalone | 3,264 | One literal ASCII space / `457B8AF0` |

The64-byte offsets are now measured declarations, not a guessed fixed wrapper
size. All five exact-boundary payloads have complete`~PSP` headers and are
eligible for a bounded static-preparation feasibility attempt. The two paired
names/sizes do not establish equal decrypted bytes, unique library counts or
Sony ownership. No module code has been decrypted or executed in Stage A.

These results justify preparing an exact Stage B contract for all five inputs
and the original EBOOT positive control. At that checkpoint this reviewer had
not approved helper execution. The later stage must pin existing helper/dependency identities,
require the original EBOOT control before any candidate in each trial and retain
all diagnostics/partial artifacts. A helper's return0 alone cannot establish
decryption success; actual output identity and format validity must be assessed
separately. No unsupported-input retry, alternate offset or library attribution
follows automatically.

## Exact Stage B pre-execution review

After the independent Stage A audit, this reviewer approved
`config/module-static-preparation.json`,5,078 bytes, SHA-256
`64e74c98f2560e6e0eb49d79976198850b1e748066cd4145243cab724f240784`,
and final ignored driver`prepare_module_candidates.py`,14,310 bytes, SHA-256
`75b928004528783e5c6ee3227b9ee5a9771a421b056f6d4322c204fc95fad162`.
Approval covers two fresh trials, each with the exact original EBOOT positive
control before all five candidates: twelve unchanged helper invocations with
only input and`-o` output, twenty-second limits, no module execution.

The existing helper is229,584 bytes, SHA-256
`05d323b28b3ceed86a42d019767ddcdae3e40f85dacebe25a5fe7d86f2b02c98`.
The reviewer independently parsed its static DT_NEEDED list and rehashed the
seven declared native loader/libraries, lookup bindings and loader cache. The
guard rejects loader override environments and sets LC_ALL=C. These pins do
not claim a complete host-OS snapshot or historical source-to-binary build.

Pinned helper CLI source calls PRX decryption and writes its returned size,
then reaches normal main return0; therefore exit status cannot substitute for
actual artifact validation. Pinned PRX source supplies the exact successful
tag/type message. The new driver requires that complete message, exit0, no
timeout/stderr, an actual regular output, and exact declared compressed length.
Unsupported output retains a distinct failure/uninterpreted status. The main
positive control additionally requires complete known plaintext ELF identity.

The plan explicitly permits raw ELF bytes or one bounded complete gzip member.
The latter must satisfy CRC/end-of-stream, reject concatenated/trailing or
unconsumed input, stay within16MiB and yield the exact declared ELF length.
No trimming, heuristic decompression or second encoding attempt occurs. Parsed
ELF container/type/bounds status remains separate from helper success and from
ownership; a prepared-byte file may be retained even if full ELF interpretation
fails. No candidate entry point is invoked or relocation applied.

Before freeze, validation strengthened retention of oversized regular outputs
with streamed identities and checks across later cases, spawn-failure logs,
and snapshots of stdout/stderr/stage/case-result files. This reviewer read back
and approved the final hash above. Both output audits and exact reviews must
precede the separate preparation freeze; no Stage A result was relabeled.

## Stage B repeat/artifact audit

Both declared control-first trials complete in
`build/module-static-prep-hxse0az7` and `build/module-static-prep-8z373w8d`.
The reviewer independently compared all twelve staged inputs with their frozen
reference/wrapper source bytes, verified all raw outputs/stdout/stderr against
report identities, and compared corresponding artifacts across fresh trials.
All final preparation-freeze inputs remain unchanged.

Both main EBOOT positive controls produce the complete known2,247,320-byte ELF,
SHA-256 `755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950`,
before the five new inputs are attempted. The four archive inputs each report
tag`457B06F0`/type2 success and yield exactly the compressed length declared in
their source header. Independent zlib readback confirms one complete CRC-valid
gzip member, no trailing input and exact declared expanded length in each case.

| Candidate | Raw helper bytes | Retained expanded bytes | Expanded SHA-256 |
| --- | ---: | ---: | --- |
| Archive17 | 20,276 | 35,232 | `9d6c771861b8dec4ed74284809e6853d5e738f794a7c5d3052ac288a23dc71cb` |
| Archive18 | 707 | 1,138 | `7e49891b16f453c09433249953f9a1330555525e6a51201f63e4b3a6abbd3807` |
| Archive19 | 20,275 | 35,232 | `3eb3b7f83442370533647b46365be49463256931196610175119959729b4e466` |
| Archive20 | 706 | 1,138 | `129e8e7a5231a81ba919d751c2ff0b1f03f95996a27d766732bf4f5bf61085bc` |

All four expanded buffers begin with ELF magic and reproduce exactly between
trials. The frozen generic ELF parser rejects each with
`ELF segment file size exceeds memory size`. Consequently their recorded status
is **HELPER_SUCCESS_OUTPUT_UNINTERPRETED**, not bounded ELF-container success.
The expanded files/hashes remain retained; this stage does not relax that
parser, reinterpret unsupported program headers or establish library ownership.
Paired sizes/names do not justify deduplicating the four distinct hashes.

OPNSSMP prints`Decryption failed for tag 457B8AF0` while returning0 and creating
an empty output in both trials. The stronger artifact/message checks correctly
retain **HELPER_FAILED_OR_UNINTERPRETED**, with no prepared file. This real
negative outcome demonstrates why process exit status alone was insufficient.
No alternate seed, tag, helper, offset or retry was attempted.

Both reports are289,755 bytes:

- `preparation-trial-1.json`: SHA-256
  `60f6d7ec4a68f9e0e7856c6873e4bebbca8162b4bbe391b19061288e1a035517`.
- `preparation-trial-2.json`: SHA-256
  `8ef61c9c85e67ec2869dce7f2724b3aac8a03d034095fc86b4838ab9c4bac40d`.

The feasibility investigation is complete, while no new candidate receives
complete ELF-interpretation status under the existing parser. Any PSP-specific
program-header investigation requires a separate bounded plan; it must preserve
the frozen parser and these failure statuses. Decryption/helper success,
expanded-byte identity, ELF interpretation, library identification and matching
credit remain different outcomes. No module entry point or code was executed.
Complete game-code inventory, original toolchain lock, linked source and credited
matches remain unestablished/zero; the parked initializer and all attempt/trick
counters are unchanged. This helper performed static/public-source/artifact
inspection and bounded CRC/byte checks only, never helper/module/compiler
execution.
