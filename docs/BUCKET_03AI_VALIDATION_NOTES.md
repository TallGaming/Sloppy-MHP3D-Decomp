> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AI independent validation

## Guarded native wrapper and fixed ABI

This reviewer owns `tools/host/kl4e_guarded.c`. It links the unchanged existing
native decoder as an offline data tool; neither original MIPS module code nor
JPCSP's interpreter path is used. The original decoder SHA-256 remains
`117befc155807a632120fbf743188a5b5ee9f924246042a67e2ea82f104af641`.
Its ABI is decompress_kle(output, capacity, stream, reported_end, isKl4e).
The wrapper requires offset-zero KL4E and at least nine input bytes, passes the
exact remainder at input+4 with isKl4e1, and never adds input padding.

The exact wrapper source submitted for review is11,209 bytes, SHA-256
`54924c9fb5dc705bc3b8147d6132c36fc18e67324261e73deac467932a1ed6ae`.
Its fixed CLI is `kl4e_guarded INPUT OUTPUT EXPECTED_SIZE`, where expected size
and actual input are independently bounded to1..16MiB and9..16MiB respectively.
RLIMIT_CORE is zero before input processing, so guard faults do not leave core
files. The controller supplies pinned inputs, complete parent-path guards,
subprocess time/resource bounds and complete input/output hashes.

The input's final real byte directly precedes PROT_NONE; the readable anonymous
region is made read-only before decoding. The underlying C API has no input
length, so an overread at that edge fails the subprocess rather than receiving
fabricated zero padding. Output uses capacity round_up(expected+1,8), with its
end directly against another inaccessible page and an eight-aligned base. This
preserves the absolute address low bits used in literal probabilities and leaves
1..8 sentinel bytes beyond the expected result. A minimum64-byte writable prefix
is also sentinel-filled. Exact returned size, complete prefix/slack sentinel
checks and a bounded endpoint are required before output creation. These are
final unchanged observations and boundary protections, not a universal proof of
malformed-stream memory safety for the original unbounded API.

The endpoint is interpreted only according to the selected decoder branch:
direct copy reports its last source byte, while compressed termination reports
the next cursor. Both offsets are recorded relative to the whole input/body;
no uniform consumption or harmless-trailer claim is made. Input fd and named
path size/inode/timestamps are rechecked. Output uses0600 exclusive/no-follow
creation only after successful decode checks; I/O failure remains a nonzero
result and may retain an owned partial artifact for audit. The JSON result is
explicitly flushed. It never claims an executed module or authenticated bytes.

## Pre-build source and model controls

The second helper independently reviews the exact wrapper and requests no source
change. Pure arithmetic checks cover780 expected-size/page-size combinations
and18 input-length/page-size combinations: capacity strictly exceeds expected,
slack is1..8, the output base is eight-aligned, prefix is at least64, and exact
input/output ends coincide with their trailing guards. Static contract readback
checks the ABI, readonly mapping, core limit and exclusive output. No compiler,
assembler, wrapper or decoder is run by this reviewer before the separate
source/build freeze. These controls do not add to the352-test tooling suite.

## Exact build and invented-boundary review

The helper approves the exact two-build/static-inspection profile before any
native compilation:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `config/kl4e-host-build.json` | 1,516 | `ffa9d26fe6ba0f3769eafbbe1d373bd649ec74c242d7a2948ff5f77d58c7a17b` |
| Fixed build controller | 10,168 | `07c7fcc44d3e0f1bc31dce5e6d0f7d76763a7ae59b20c577072122b463f3d8ce` |

Host gcc uses the fixed O2/c99/Wall/Wextra recipe and no-undefined link. The
complete child environment is PATH/LC_ALL. The preprocessing dependency query
uses the same frontend flags, records actual header inputs before objects are
generated and rechecks them afterward. It never runs the built wrapper. Static
readelf inspection uses the exact pinned resolved tool and requires only the
declared libc/loader runtime with no RPATH/RUNPATH.

Review catches missing immediate source-copy pins, post-readelf artifact/header/
tool checks and spawn metadata; the other reviewer also flags mismatched
preprocessor optimization flags and binary-record/read association. All are
corrected before freeze. Structured spawn handling and thirteen mock-only cases
pass: positive; source pin mismatch; dependency query failure/spawn preventing
objects; build failure; static-reader failure; binary/source/log/header drift;
late pin drift; prior report preservation; and binary mutation between its
identity record and snapshot read. Actual source/tool/runtime verification passes
without compiling or executing anything. These controls do not extend the last
352-test WSL suite or the game gate.

The exact wrapper source remains frozen at its approved identity. Invented
native execution and real OPNSSMP decoding each need their separately reviewed
controller/profile and freezes after these build artifacts are audited.

## Actual host-build audit

Both fresh host builds complete without executing either output. The helper
independently checks four staged source copies, all twenty retained build
artifacts and276 header-pin observations (the same138 unique headers per build).
Both binaries are21,384 bytes, SHA-256
`20d9ee7162765e3af8797f7bd8d9dfbffed6cbb14e37a4380e9a8d17fc2d25c9`.
Pure ELF64 reading independently confirms native x86-64, only libc.so.6, the
default /lib64/ld-linux-x86-64.so.2 interpreter and no RPATH/RUNPATH. Exact
dependency-query/build/static commands and their zero exits agree with the
profile. The original decoder's one line219 signedness warning is retained in
both builds; the wrapper source and decoder are unchanged.

The roots are `kl4e-host-build-2fxl2twz` and `kl4e-host-build-uxaz36az`.
Their3,000-byte reports have SHA-256
`dfc3cfecffbc008a84e4a40defd961486f6778e54e14c54a5719eb9a1df0cd40`
and `c1f6eca9ab19e185d8db0bbf91e5ea514d9d5af1d816a569507a5659bcde528e`.
The488-byte build freeze has SHA-256
`39f15688b84ddf678ba3a6e0830c46bd4360eb5265d8253e641fc498d425d0a8`.
Nested source/header/tool/runtime and exact freeze identities pass after audit.
No native wrapper/decoder is run by the reviewer.

## Invented-control execution review

After build audit, the helper approves only the separate invented-control stage:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `config/kl4e-host-experiment.json` | 2,484 | `73fca5a2b03c7bcc6206f85ea24d897f25770f54601d9ec1069fab15f9980ee7` |
| Fixed execution controller | 17,119 | `0eaf39ea3c9b3ee91d2a4a93de7000f86379387860b80f611d03341c98658ca6` |

Review requests structured spawn records, full parent guards, input/output-state
checks immediately beside launch, captured stdout/stderr identity bindings and
snapshots tying accepted output to the final bytes after metadata/late pin
checks. These guards are present in the approved source. One protocol positive
and eleven malformed guard/endpoint/stream/output negatives pass. Five full
mocked matrix/preservation/drift scenarios and four spawn/timeout/prelaunch-input/
late-stream scenarios also pass. The mock positive traverses all seventeen cases:
fifteen simulated native calls and two real controller-level symlink rejections.
No native executable is invoked during review.

The frozen real control plan has six direct-copy sizes, wrong magic, short
header, invalid expected-size arguments, truncated input guard fault, count
exactly equal to capacity, returned-size mismatch, existing output preservation,
a trailing-bytes endpoint observation and two controller path redirections.
Successful direct-copy controls do not independently validate compressed-stream
semantics or every malformed back-reference path. The two path rejections are
controller checks, not native symlink invocations. Any signal/error/timeout is a
retained rejection, never decoded output or a matching-gate negative result.

## Actual invented controls audit

All seventeen actual invented controls pass, comprising fifteen native calls
and two controller-only path rejections. The helper independently audits all87
retained artifact pins, source fixtures, outputs, streams, native outcomes and
result records. Seven positive direct-copy cases produce the exact complete
payloads with aligned capacity and unchanged sentinels. Eight negative native
cases match their frozen exit/signal expectations. Truncated direct copy reaches
SIGSEGV exactly, with no prepared output or core. Existing output bytes and both
redirect targets are preserved. No native tool is re-executed by the reviewer.

The trailing-bytes control is deliberately an observation: input size22 and
reported last-copy offset11 with outputABC. It does not establish full
consumption or a general harmless-trailer rule. The actual native positives are
direct-copy mode, not independent compressed/back-reference validation. Full
input/output guards and branch-specific endpoint semantics agree with the C
source and reports.

The40,428-byte controls report has SHA-256
`32bb46740c2f2a859290da2bb0fdb4ee91892223868f5549706d717b768ce40d`.
The503-byte pre-execution controls freeze has SHA-256
`87fc53a2558e1e85192a25a86ad244a4e6ea07b3570abaef508a28546dbc72ef`.
Fresh input/source/helper/runtime checks pass; original decoder and wrapper
remain unchanged. No actual OPNSSMP payload is attempted during this stage.

## Actual-input preparation review

The reviewer agrees with explicitly pinning elf32.py, prepare_reference.py and
inspect_input.py before metadata interpretation, while preserving the frozen
controls controller/profile. After controls audit, these exact additional inputs
are approved before the separately frozen two real payload attempts:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Actual-stage adapter | 5,449 | `c8ebd85ae4c3301c0beb48f66522c23807aaf6a12a7871bc12238db0ce3f3bc6` |
| `actual-imports.json` | 647 | `c36ed571ca08d5afc15d2ce33c312062dbc108ea6914a8be6424220bf726c8c9` |

The adapter checks the exact three project imports before loading the controller
and at its existing before-decode/after-metadata checkpoints. A final separate
acceptance witness binds the preliminary raw report, all case artifact hashes
and import pins. A raw controller report alone is preliminary and cannot grant
accepted preparation. The fixed decoder, metadata reader and frozen controls
controller are unchanged. Transcript paths are guarded beside exclusive writing;
raw report bytes are rechecked before the witness.

Nine mocked adapter scenarios pass: valid and uninterpreted witnesses, preimport
and late import-pin rejection, artifact/report drift, controller failure,
redirected transcript parent and existing witness preservation. An additional
focused case preserves the exact nonempty partial controller transcript on
failure and creates no witness. The three actual import identities agree with
their prior frozen pins. No real decoder or actual controller is invoked by the
reviewer. Approval is exactly one fixed3550-byte expected output attempt per
retained2926-byte input/helper copy, then the pinned3AF metadata reader; no
source/codec/flag variation is authorized.

## Actual complete output and witness audit

Both separately frozen actual attempts pass, with two complete3,550-byte outputs
of SHA-256 `2b4c5af91c7be885054e997bd05a51d8d5d7d544098b2395dc6d893e0e374599`.
The helper independently checks full output equality, original2926-byte KL4E
inputs and3AH report bindings, exact helper selections/arguments, every case
artifact and both final witness/report associations. Native exit is zero with
empty stderr, no timeout/spawn failure and no core. The wrapper reports expected
and returned3550, capacity3552, eight-aligned base,544 unchanged prefix sentinel
bytes and two unchanged slack sentinel bytes. Exact input bytes are used without
padding. The compressed cursor is reported at raw offset2926/body offset2922;
uniform-input-consumption remains explicitly false despite that numerical end
position. These are bounded final observations, not universal codec safety or
runtime behavior proof.

The pinned3AF reader independently reproduces both metadata records. The output
is sectionless PSP PRX type0xFFA0, with PT_LOAD file/memory sizes3032/3032 and
136/144, plus bounded PSPREL2 file size206/memsz0. All file extents and load-memory
ranges are checked directly from original output program-table bytes. No
relocations are applied. The52-byte module-info declaration at file760 has name
opnssmp, attributes0 and version bytes[129,1]. GP32896, exports532..548 and
imports556..596 remain raw fields; no address mapping, export/import
reconstruction, ownership or authentication is inferred. No compiler comments
or section names are invented for the sectionless output.

The preliminary5,988-byte reports have SHA-256
`a2718b5b4448555f344aa2fe36f2aee52ffd617a22b9228f6103442d7b339cf9`
and `e9f30f347166fb469809c00eaf5213232a15f011a59d380168cc976ec0571480`.
Their matching925-byte acceptance witnesses have SHA-256
`a0bba6cfe138bfb54e6b8edc6d145fffb2e2f79aee1533f2b465452d9951a54a`
and `7ceb5c191ac0a38dae4b3bcbc83199ae338893e8b0bed339297856f6ef10ae66`.
Each witness accepts only its exact preliminary report and pinned dependencies;
report paths differ while complete output and metadata repeat.

The785-byte actual freeze has SHA-256
`075779349be5c046e7795fee6e21888e61df63f879112650aa272d5ee9a0da60`;
the1,089-byte adapter freeze has SHA-256
`c8fa2d77391010136a68950e4bb7b8fbc747b7b7dc9d7b19dda12ae8a311f190`.
Final source, native helper, runtime, dependency and actual-input pins remain
valid. A separate read-only check also confirms all seven prior runtime lookup
bindings, seven runtime files and loader cache identity unchanged. The reviewer
performs no decoder rerun. Earlier3AD/3AH failures/partial outcomes remain
preserved rather than overwritten by this newly supported preparation.

This establishes one repeatable bounded host preparation and metadata result.
It is not an independent second-decoder cross-check, cryptographic signature
authentication, positive SDK ownership, original module execution or a gameplay
runtime test. The original C decoder and wrapper source remain unchanged from
their respective reviewed freezes. No game compiler flags, source attempts,
parked initializer, matching-shape counters or native-port implementation change.
The last352-test tooling suite is unchanged; seventeen invented controls are
separate from the unimplemented full-game build gate and its eighteen negatives.

