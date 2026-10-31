> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Isolated OPNSSMP tag capability review — Bucket 3AH

Stage A reviews a minimal host-tool capability addition. The existing helper,
its lock, original input, compiler profiles and earlier failure artifacts remain
unchanged. No helper or compiler invocation was performed by this reviewer.

## Exact public metadata and representation

At pinned JPCSP commit `48f107aea7b021d51ebaf2fda4007ceb6f47bb03`,
[PRX.java](https://github.com/jpcsp/jpcsp/blob/48f107aea7b021d51ebaf2fda4007ceb6f47bb03/src/jpcsp/crypto/PRX.java#L135-L146)
maps tag `0x457B8AF0` to `keys636_1` and scramble code `0x5B`. Its
[USER_MODULE dispatch](https://github.com/jpcsp/jpcsp/blob/48f107aea7b021d51ebaf2fda4007ceb6f47bb03/src/jpcsp/crypto/PRX.java#L405-L425)
selects type 6 for that exact tag. Mode 4 is the source's USER_MODULE value,
consistent with this input's declared header. This establishes a concrete
capability hypothesis; it does not authenticate the header or guarantee output.

The pinned [KeyVault.java declaration](https://github.com/jpcsp/jpcsp/blob/48f107aea7b021d51ebaf2fda4007ceb6f47bb03/src/jpcsp/crypto/KeyVault.java#L306)
is exactly 16 Java int elements, each in 0..255. Their canonical ordered octets
have SHA256 `4b4f08ec3e437fb71171a063705fefad2de462fc7348cc68b4d6fd44aeedf3fd`.
The three-argument TAG_INFO constructor assigns that array directly; it does not
use the separate four-argument constructor's 144-byte word expansion. The old
helper's TAG_INFO2 expects a pointer to 16 unsigned octets and an 8-bit code.
Consequently a same-order `const u8` array and one three-field exact-tag entry
are representable without changing an algorithm. No identical old-helper u8
array was found during source inspection.

The cached KeyVault text is 61,070 bytes, SHA256
`ea4251df06ab578270acb42e96778e526dcee6fc63b26b307e8f7f6fe6c1085b`.
Exact URL/commit/line/representation metadata is in
`evidence/bucket-03ah/helper-map-key-metadata-source.json`; PRX.java remains the
pinned 3AG public text. No key bytes are reproduced in this report.

The minimal isolated change must add only that public array and the exact
`{ tag, key, code }` entry. It must not set a forced type or seed, replace another
tag, modify the input/header, add preprocessing, weaken integrity checks or
change dispatch. The existing helper already attempts types 0/1/2/5/6; a type 6
attempt becomes reachable through ordinary existing control flow when lookup
metadata exists. Its existing SHA comparison and KIRK processing remain; the ECDSA
authentication limitation below is preserved too.
The source already has a disabled padding rejection; preserving it is not a
new bypass, but the new helper must not be described as implementing checks
that its unchanged source does not enforce.

JPCSP's optional sign-check preprocessing depends on an external caller boolean;
its applicability to this local file remains unproved. Later compression handling
is separately bounded: 0x0201 suggests a possible KL4E stage, but no raw inner
magic or successful decode is established in Stage A. The optional emulator path
that runs supplied MIPS decompressor code is outside static preparation scope.

## Pre-build review status

The isolated source review independently checked all 34 baseline files against
both the frozen source tar and original local checkout, and all 34 candidate
pins. Only `PrxDecrypter.cpp` differs: removing exactly a 305-byte public-array/
comment insertion and a 43-byte table entry reconstructs the original bytes.
The original CRLF bytes remain intact. The candidate source is 55,472 bytes,
SHA256 `7f53d0c1b1f9a618449577a673f17ea2bc6b2fa9ea9e98e2c536f5730e6d5288`.
Its 16 octets and three-field entry agree exactly with the source metadata.
`evidence/bucket-03ah/source-isolation.json` records the archive/file identities.

An earlier extraction preflight stopped on an inappropriate normalized-source
comparison against raw CRLF archive bytes; its failure and partial prefix remain
preserved. No build occurred before the corrected strict-byte isolation review.
Final pre-build approval covered
`evidence/bucket-03ah/build_tag_capability.py` (12,581 bytes, SHA256
`d4b3ffed32714a5666b06e1fa9d021e294ca65c327bc3ce8709f0ec85a86dd0b`)
and `config/opnssmp-tag-build.json` (2,900 bytes, SHA256
`c57359c8347e344ea7ba4f8f1ccf1a7d831a320b7ebd024ab8d9062125396b34`).
The fixed recipe is original Makefile with `/usr/bin/make -j4`, explicit native
GCC/G++ commands and unchanged host O3 options. Each trial builds baseline and
candidate in fresh private directories. These are host-tool settings, not PSP
compiler options or a game-toolchain lock.

Review corrections before execution include a complete child environment of
PATH/LC_ALL only, full parent-path guards, exclusive report/failure publication,
and snapshots of staged source, generated objects/binary, logs and stage records
across later builds and final publication. Success requires exactly 34 source
files and 16 declared generated products. A failed build retains diagnostics
and partial products without becoming a successful helper. The native ELF64
header check does not execute the output. Compiler/backend/assembler/linker/make
identities and bindings are pinned; this is not a complete host OS or every
system-header/static-library snapshot. This review does not authorize a guessed
algorithm change or a game/module execution. Stage B requires its own frozen
new-helper binary/runtime identities, controls, input/output contract and both
reviews before any candidate helper invocation.


## Stage A actual builds and independent audit

Two fresh trials each built baseline and candidate successfully. All 136 staged
source copies and 64 generated products were independently checked; each case
contains exactly the declared 34 source files and 16 products. All per-variant
repeat products agree. Only `PrxDecrypter.o` and the linked helper differ between
baseline and candidate. Both baseline binaries are 229,584 bytes, SHA256
`05d323b28b3ceed86a42d019767ddcdae3e40f85dacebe25a5fe7d86f2b02c98`,
byte-identical to the existing helper. Both candidate binaries are 229,632 bytes,
SHA256 `9101c7dfc5c4667b5a400b947b94ec3e5b584b7a877cc41ab0983b0571528920`.
Native headers are ELF64/x86-64; no candidate execution is implied by that check.
The retained roots are `build/opnssmp-tool-build-qrdhoof6` and
`build/opnssmp-tool-build-e4v9kodi`. Reports, all logs and stage identities agree
with their actual bytes. Reports differ by declared trial/root as expected.

Each identical stderr log contains 12 warnings: nine OpenSSL deprecations in
IPL/other helper source, one old-style function definition in `libkirk/SHA1.c`,
and two `memcpy` overread warnings in the ECDSA signing routine in `libkirk/ec.c`.
They were retained, not suppressed. Source dispatch sends the selected type 6
decryption to `KIRK_CMD_DECRYPT_PRIVATE`/CMD1; the warned signing routine belongs
to CMD16 and is not called along that path. No unrelated warning fix belongs
to this metadata-only patch.

There is also a material existing
[authentication limit](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/libkirk/kirk_engine.c#L265-L309):
`g_checkEcdsa` defaults to 0 and CMD1's ECDSA checks are conditional on it. This
isolated source delta changes neither that default nor the existing disabled
padding rejection. A successful later decrypt therefore must not be called
signature authenticated. The helper's active type 6 SHA check and control/output
checks are useful, but do not substitute for authentication. No bypass or new
option is being added to overcome a failure.

Stage B remains separately reviewable: pin these fresh candidate binaries and
the runtime closure, require complete prior main/type 2 raw-output controls
before OPNSSMP, retain every actual output, and accept no process-exit-only
success or unsupported compression interpretation.


## Separate Stage B pre-execution review

Final approval covered `evidence/bucket-03ah/run_tag_capability.py`, 10,949 bytes,
SHA256 `3cdc1eb26e8d50dee2b89e1ab8692fda787df6db375095b9ad7e714173f34348`,
and `config/opnssmp-tag-experiment.json`, 9,328 bytes,
SHA256 `63a8d7f6337c19c828d642ba7033919bb147857af2f4186c6f242ea6dd9ed4e0`.
Each trial uses its separately built candidate, bound to its own build report.
All five complete main/type 2 raw and prepared controls must match 3AD before
OPNSSMP. Expected type 6 is recorded as an observation check, never forced.
Only existing raw-ELF/gzip interpretation is permitted; unsupported output is
retained. Authentication is explicitly false.

Independent static ELF64 parsing confirms the four built helpers have the
original helper's five DT_NEEDED names. All 212 source/product/log artifact pins
and twenty golden raw/prepared output copies were checked against their own
3AD cases. Read-only WSL hashing rechecked seven runtime files, seven resolver
bindings and the linker cache. The inherited runtime closure is consistent;
it is not a complete system snapshot.

Final review corrections place earlier-output snapshot verification and new
case path guards immediately before every helper call, including the OPNSSMP
boundary; config/report/failure paths are guarded and exclusively published.
Known output/status/error/path/hash records bind to their original preparation
case, not just equal-sized files. Partial helper failures and oversized regular
outputs retain identities and remain unaccepted. No candidate helper was
invoked by this reviewer. Actual Stage B outcomes are recorded below.


## Stage B actual outcome: raw capability established, format still bounded

Both six-call trials complete with all five prior controls exact before OPNSSMP.
The unchanged OPNSSMP input naturally succeeds with type 6, agreeing with the
preselected public mapping. Both new raw payloads are 2,926 bytes, SHA256
`baa08abb7d5aef2fff636f0eecfd01f49a67f1fe887d6a55e1f14cc3a307dfe5`,
and begin with literal `KL4E`. The exact success log, rc 0, empty stderr, complete
input identity and declared data length agree. No forced type, extra sign-check
stage, hash bypass, input edit or algorithm change was used.

The existing raw-ELF/gzip interpreter rejects that payload as unsupported and
retains `HELPER_SUCCESS_OUTPUT_UNINTERPRETED`. There is no `prepared.elf`, no
signature-authentication claim, no established code extent or SDK exclusion.
Literal magic is a format lead, not proof of a fully decoded valid module. The
old helper failure and all 3AD/3AE outcomes remain preserved, with the original
helper lock still pointing to its original binary.

Independent read-only checks audited all 12 staged inputs, 12 raw outputs,
10 complete golden prepared outputs, 24 stdout/stderr files and corresponding
stage/case records. All per-case repeat input/output/log bytes agree. The eight
gzip control copies pass a complete-stream CRC audit and equal their known
prepared bytes. Both freeze records still match the actual source/profile
identities. No helper or KL4E code was invoked by this reviewer.

Retained reports `experiment-trial-{1,2}.json` are 290,472 bytes each, SHA256
`cbb01166e5f108a361beaeaf85c52346a1e9f221e982539124a8fd17a2148e5c` and
`ff2d1645b7468992aa339458d7f19a454ed2d3d960a2ae5795d4a11eaee40f01`.
Their expected trial/root/command paths differ; payloads repeat exactly. The
first root is `build/opnssmp-tag-experiment-65cqzh4b`; the second is
`build/opnssmp-tag-experiment-48guzbtw`.

The narrow missing-tag capability hypothesis is supported by these controlled
outputs. Further progress requires separately reviewed native bounded KL4E
preparation, retaining the current raw payload and using no supplied MIPS
interpreter. That work was not performed here. The historical game toolchain,
source budgets, parked initializer, ownership policy, full-gate requirement and
zero credited match/source-link counters remain unchanged.
