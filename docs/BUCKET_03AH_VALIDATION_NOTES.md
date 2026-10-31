> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AH independent validation

## Scope and public metadata compatibility

This bucket is authorized under the renewed11:21:44-16:21:44UTC work window.
It tests only the exact absent-tag capability identified in3AG. Preserve the
original helper/source/lock, unchanged OPNSSMP input and every earlier failure.
An isolated helper may add only the source-proven public metadata array and
exact tag entry. No dispatch forcing, header repair, signature/hash bypass,
sign-check preprocessing, game source/profile change or module execution is
part of this scope. Build options for this host tool do not select a PSP game
compiler or change per-function matching flags.

The helper independently verifies the pinned public
[JPCSP KeyVault source](https://github.com/jpcsp/jpcsp/blob/48f107aea7b021d51ebaf2fda4007ceb6f47bb03/src/jpcsp/crypto/KeyVault.java)
identity:61,070 bytes, SHA-256
`ea4251df06ab578270acb42e96778e526dcee6fc63b26b307e8f7f6fe6c1085b`.
Exactly one keys636_1 definition has16 integer elements, each in0-255. Its
canonical octet SHA-256 is
`4b4f08ec3e437fb71171a063705fefad2de462fc7348cc68b4d6fd44aeedf3fd`.
The separately pinned PRX source binds that symbol to exact tag457B8AF0/code5B
and associates the USER_MODULE tag path with type6. The octets are neither
printed in this report nor substituted into the original helper. Recognition
and representation compatibility do not guarantee successful decryption.

## Required build and run guards

Stage A must use a clean separate pinned source tree, with no reused object or
binary. Review the exact two-addition delta and unchanged cryptographic/control
flow, freeze source/build recipe, recheck all original and isolated inputs after
building, then pin the new binary and runtime closure before any execution.
Candidate execution needs its own later review/freeze.

Stage B requires exact whole raw-output reproduction of the known main and
successful type2 preparation controls before unchanged OPNSSMP in each trial.
Use fresh case paths and one fixed invocation per case, strict reported tag/type/
output-size checks, full failed/partial output retention and end identity checks.
Exit zero alone never counts. Non-gzip output stays raw/uninterpreted; no new
KL4E decoder is adopted in this bucket. No helper build or execution is launched
by this reviewer.

## Exact pre-build review

The independent isolation audit verifies all34 baseline files against both the
pinned source archive and original checkout byte-for-byte. The candidate differs
only in PrxDecrypter.cpp through two exact CRLF insertions,305 and43 bytes: one
public16-octet u8 array and one three-field tag/array/code entry. All unchanged
bytes, including dispatch and cryptographic algorithms, remain identical. The
array's canonical digest matches the public definition. No source tree contains
prebuilt objects or binaries.

The source manifest is16,507 bytes, SHA-256
`2f4d7feb855d990e512e98265e6d4e9b1968b3164041d4a72ed03490530a3b4e`.
Candidate PrxDecrypter.cpp is55,472 bytes, SHA-256
`7f53d0c1b1f9a618449577a673f17ea2bc6b2fa9ea9e98e2c536f5730e6d5288`.
The original remains55,124 bytes with its prior digest. The source archive has
34 regular members with no extra build artifacts. An earlier source-isolation
preflight failed a one-sided newline comparison before any build; its partial
tree and failure evidence remain preserved. The corrected v2 comparison is exact
on both sides, rather than silently normalizing the isolated source.

The reviewed host Makefile uses -O3 and libz/libcrypto. The planned command fixes
CC/CXX to pinned native gcc/g++ and uses fresh staged copies for baseline and
candidate twice. This is host-tool capability work, not a PSP game compiler/flag
experiment. The helper approves the exact build inputs below before four fresh host builds
(two baseline/candidate pairs), with no output-helper execution:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `config/opnssmp-tag-build.json` | 2,900 | `c57359c8347e344ea7ba4f8f1ccf1a7d831a320b7ebd024ab8d9062125396b34` |
| Fixed build driver | 12,581 | `d4b3ffed32714a5666b06e1fa9d021e294ca65c327bc3ce8709f0ec85a86dd0b` |

Review identifies that inherited make/include environment and binary-only
snapshots would leave invisible recipe inputs and earlier staged source/log
mutation unchecked. The primary supplies the entire child environment using
only PATH/LC_ALL, rejects known invoking-session overrides, immediately pins
copied source bytes, checks full path chains, and retains all source/generated
product/log/stage snapshots through later builds and publication. Failed or
timeout builds retain partial products; over-bound files use streamed identity
checks. A successful case requires exactly the34 source inputs and16 declared
products. Diagnostic failure writes preserve existing evidence and use exclusive
creation with path guards.

Two malformed/changed public-metadata controls, four actual forbidden-environment
checks and fourteen mocked build scenarios pass. The latter cover a positive,
failed build, timeout, spawn exception with partial output, missing/extra product,
staged source mutation, prior source/binary/log mutation, late pin drift, invalid
native-header output, source-pin mismatch before launch and existing report
preservation. The mocked child receives exactly the declared two-variable
environment; no actual host compiler, make process or built helper runs during
review. Real read-only nested source/tool/runtime checks pass. These inline
controls are separate from the last352-test WSL suite and unimplemented full
game gate. Candidate execution still needs a separate exact binary/runtime and
Stage B profile review/freeze.

## Stage A actual build audit

Both fresh host build pairs complete. The helper independently verifies all136
staged source copies against the pinned34-file variant inventories and all64
generated products. Every product repeats byte-for-byte within its variant,
including all objects and the complete helper binary. Between baseline and
candidate, only PrxDecrypter.o and the final executable differ.

| Variant | Complete binary bytes | SHA-256 |
| --- | ---: | --- |
| Baseline, both trials | 229,584 | `05d323b28b3ceed86a42d019767ddcdae3e40f85dacebe25a5fe7d86f2b02c98` |
| Candidate, both trials | 229,632 | `9101c7dfc5c4667b5a400b947b94ec3e5b584b7a877cc41ab0983b0571528920` |

Both baseline binaries equal the original helper in full, independently of their
copied source identities. Pure ELF64 reading verifies native x86-64 headers,
bounded program records and the same interpreter/direct dependency set as the
original: /lib64/ld-linux-x86-64.so.2 and libz/libcrypto/libstdc++/libgcc_s/libc.
No RPATH or RUNPATH is present. This is a static read, not a candidate launch;
Stage B must still pin the runtime closure/bindings before execution.

All four make stages return zero without timeout/spawn failure. Exact commands,
complete PATH/LC_ALL child environments, stdout/stderr/stage identities and source
immutability agree with the fixed recipe. Twelve compiler warnings per build
are retained, not silenced: nine OpenSSL deprecations, one old-style SHA1 function
definition and two ec.c signing-path overread warnings. They are not twelve
OpenSSL warnings and are not hidden as a clean/no-diagnostic build. The same
original source produces the baseline and candidate observations. This is a
host-tool build diagnostic, separate from fixed game-compiler warning gates.

The unchanged libkirk source defaults g_checkEcdsa to0, and its CMD1 signature
checks are conditional on that flag. No new verification bypass is added, but
preserving the existing algorithm/checks does not establish signature
authentication. Successful helper bytes later must remain unauthenticated and
must not identify a module's owner merely from a declared name.

The build roots are `opnssmp-tool-build-qrdhoof6` and
`opnssmp-tool-build-e4v9kodi`. Their2,254-byte reports have SHA-256
`57f9770028a70342adf5ed18045004d32ca37a70572720630ce937a8ea6c240d`
and `ba114a8c0a9b201ee40c4e1830353d68a1f2328fb18683027c46801752679d79`.
Path-bearing reports/log scheduling are not required to be identical; whole
products are. The713-byte pre-build freeze has SHA-256
`1d5a855bb054bdb14f960eb9b5cb34ead7075000f7975efe2f8d3f0b2deda1af`.
Fresh nested source/host/runtime/preserved-input and exact freeze checks pass.
No output helper or original module is executed during this build stage.

## Stage B exact pre-execution review

After the build/output audit, the helper approves these separate exact Stage B
inputs before any new-helper execution:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `config/opnssmp-tag-experiment.json` | 9,328 | `63a8d7f6337c19c828d642ba7033919bb147857af2f4186c6f242ea6dd9ed4e0` |
| Fixed control-first runner | 10,949 | `3cdc1eb26e8d50dee2b89e1ab8692fda787df6db375095b9ad7e714173f34348` |

Each trial selects its own byte-identical candidate build and first reproduces
five complete historical controls: known main plus all four successful archive
preparations. Both full raw and full prepared outputs/status/errors must match
3AD. Only then may unchanged OPNSSMP run once. Twelve helper invocations total
are declared. Runtime bindings/closure are reused only after exact verification;
all212 unique build-source/product/log records, candidate/baseline associations
and golden case paths/hashes/statuses are pinned and checked. Public type6 is an
observed-success expectation, not a forced invocation argument.

Twelve mock-only execution scenarios pass: both trial selections, control
nonzero/raw/prepared mismatch blocking OPNSSMP, failed/timeout-partial OPNSSMP,
unexpected reported type, wrong raw length, earlier-log mutation, late pin drift
and existing report preservation. A valid unknown KL4E-prefixed raw output stays
uninterpreted with no prepared ELF or new decompression. The inherited exact
command/time/stream and all-output identity guards run directly around a mocked
subprocess; no real helper is launched by the reviewer.

A final valid-input check and seven in-memory semantic/profile negatives also
pass: candidate/baseline records swapped between fresh builds, golden output
copy order or case swapped, expected status changed, duplicated artifact path
and wrong public expected type. These tests alter no real metadata files. The
final driver explicitly binds all212 artifact identities, both selected builds
and every historical control to its originating report, and guards/snapshots
case paths immediately before each invocation. Existing build/helper/source/
runtime and golden pins pass. The exact separate experiment freeze must still
precede actual execution; source compatibility/build success is not OPNSSMP
preparation or authentication.

## Stage B actual output audit

Both fresh Stage B trials complete with their separately built/pinned candidate
copies. The helper independently reads all twelve encrypted inputs/raw outputs,
stdout/stderr/stage/case records, and all ten prepared control files. Every
control's complete raw and prepared bytes and expected parser status/error match
the original3AD golden files. All five controls precede OPNSSMP in both trials.
Each exact command uses its trial's candidate helper, unchanged input, -o and
20-second bound; all twelve recorded exits are zero with empty stderr and no
timeout/spawn exception. Complete per-case bytes, streams and outcomes reproduce
across trials. No reviewer invokes a helper or codec.

OPNSSMP now naturally reports tag457B8AF0/type6 without forcing a type or altering
its original3,264-byte input/header. Both raw outputs are exactly2,926 bytes,
SHA-256 `baa08abb7d5aef2fff636f0eecfd01f49a67f1fe887d6a55e1f14cc3a307dfe5`.
That size matches the original declared PRX-data length. The raw prefix is KL4E,
consistent with the earlier compression-selector lead. No KL4E decompression is
attempted. The existing raw-ELF/gzip interpreter returns the explicit unsupported
encoding error; both outcomes remain `HELPER_SUCCESS_OUTPUT_UNINTERPRETED`, with
prepared_elf null and no prepared.elf file. The declared3,550-byte ELF length
remains unvalidated. The aggregate records source/type agreement and does not
claim signature authentication, module execution or a parsed ELF.

This validates the narrowly added lookup capability through retained controls
and repeat raw output, not every later format/preprocessing requirement. The
original3AD OPNSSMP failure messages and empty outputs are independently rechecked
unchanged. Both rebuilt baseline binaries equal the original old helper exactly;
no fresh old-helper negative invocation is claimed. The older failed result is
preserved alongside the new capability-version outcome.

The experiment roots are `opnssmp-tag-experiment-65cqzh4b` and
`opnssmp-tag-experiment-48guzbtw`. Their290,472-byte reports have SHA-256
`cbb01166e5f108a361beaeaf85c52346a1e9f221e982539124a8fd17a2148e5c`
and `ff2d1645b7468992aa339458d7f19a454ed2d3d960a2ae5795d4a11eaee40f01`.
The803-byte pre-execution experiment freeze has SHA-256
`3cff6462662bce976359cf23067dd489ebb55a26216eecca7f1e25fb4ce07ab1`.
Report paths differ; complete input/output/stream identities and outcomes are
the repeat controls. Final nested verification checks all212 build source/
product/log identities, original/new helper identities, runtime bindings,
source inventories, golden/prerequisite records and both exact freezes.

No new compression format, key guessing, source variant, forced type,
sign-check processing or changed cryptographic algorithm is introduced. The
preexisting ECDSA default still limits authentication claims. No original
module/game is executed or emulated; ownership remains UNCLASSIFIED and complete
code inventory remains open. The historical PSP game toolchain stays unlocked,
initializer stays PARKED, and the three plain/one commented-shape/zero pins/zero
empty-asm/zero match/source-link totals do not change. The last352-test WSL suite
is unchanged; review controls and host builds do not implement the full clean
game build or its eighteen required negative checks. Any bounded offline KL4E
work needs its own source/bounds/repeatability review and freeze after closure.

