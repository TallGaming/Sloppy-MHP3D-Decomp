> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3U independent validation

## Separately declared help-only contract

This new transport check preserves Bucket 3M's INCONCLUSIVE header-based result.
It does not retrospectively waive that result or reuse it as success. The new
contract independently requires exact complete file-backed executable bytes and
three mapped complete diagnostic strings, followed by precisely one observed
PUSH EBP step and ordinary help completion. No source is compiled, optimizer
hook installed, IR decoded, object neutrality inferred or game run.

Before any live invocation, the helper independently verifies the pinned PE's
preferred entry `0x00401000`, entry byte `0x55`, all 1,702,912 file-backed .text
bytes and all three exact label-plus-NUL mappings. Virtual zero padding is not
substituted for file-backed bytes; no relocation mask or speculative base shift
is allowed. Full .text SHA-256 is
`11ebae9224311b84b66986f5804059204e41592afef1009b1093bcdfea27e550`.
The selected strings are After IR Optimization, After removecommonsubexpressions,
and After propagatecopyinstructions, with identities fixed in the profile.
Current compiler, standalone wibo and GDB identities also verify without launch.

The final pre-execution approved script is 14,332 bytes, SHA-256
`a1192eb0f9e6bd84eed89b29721b014880ac77eaf65ad41dccfd208a18ab9352`.
The 1,980-byte profile is SHA-256
`488194115646ddfd7d6babaabf68defe6c5f6b5f1b6a53b3fa1fc9b7f2556033`.
Both reviewers identify assertion-only static guards as a problem before
execution. The primary replaces them with explicit errors; optimized Python
therefore retains the PE/text/marker checks. Strict guest-register, PC/CS and
saved-word types prevent numeric coercions from standing in for observations.

The generated debugger flow establishes the hardware breakpoint stop, verifies
identity before stepping, removes breakpoints and requests one single step. It
requires PC+1, unchanged guest CS, ESP-4 and exactly four bytes equal to the
previous guest EBP. An eight-byte push is a failure even if its low word matches.
The script neither writes registers nor calls arbitrary guest expressions. It
continues to normal unchanged help, requires explicit inferior exit0 and no
error/signal/timeout, and checks tool/frozen-input identities again afterward.

## Meaningful controls

Eleven new tests use invented observations and PE bytes, with no compiler or
GDB launch. They cover exact positive identity/stack effects, full .text mutation
and truncation despite a correct entry byte, missing/reordered/altered strings,
wrong stop/PC/CS, guest-width and type failures, 64-bit-push delta, stack underflow,
wrong saved EBP/size, observation errors/signals and missing/multiple/failing exit
events. Process completion, pinned ordinary-help output, containment, diagnostics,
timeout and tool integrity are tested independently of the guest observation.

Freeze controls require exactly the four declared immutable inputs and both
final review acknowledgments. Invented PE mapping/tool mismatches fail before any
process launch. A child Python process with -O and process launch explicitly
forbidden confirms wrong mapping still fails; it invokes neither compiler nor
debugger. Both generated GDB Python blocks parse even with quoted path names.

Independent execution passes **11 new tests and all 340 tooling tests, zero
skipped**, preserving 329 previous checks. These are transport tooling controls,
not the full-game gate's eighteen negative tests. The new test file is 12,904
bytes, SHA-256
`2c683e07acb1db57a21e15eb31ad66db93fbf6600fb2c09ac945d25293de24b8`.

The primary initially finds that Windows rejects the -O regression at the POSIX
guard before reaching the intended invalid-mapping check. Before any live trial,
the same guard is moved after pure static verification but still before build
creation or process launch. The helper reviews the exact change and independently
passes all eleven transport controls on both Windows Python and WSL. The initial
full WSL 340-pass result predates this harmless ordering correction; the final
platform suite is reported separately by the primary. Criteria/profile/test bytes
remain unchanged, and the initial Windows failure is retained.

## Actual two-trial audit

Both primary-run fresh trials pass the frozen contract. Their build directories
are `build/compiler-transport-xbwdlv2a` and `build/compiler-transport-c8v91xbl`.
The 1,230-byte freeze record, SHA-256
`6130ac2479474096d16860adbb738a45151c75763389c6504f7e4f5e9efdd574`,
contains both exact final review acknowledgments and all four required input
pins. Independent post-run verification reproduces every frozen input and the
compiler/wibo/GDB identities. No live probe is run by this helper.

| Trial | Report bytes | Report SHA-256 |
| --- | ---: | --- |
| 1 | 3,023 | `21a274a867ba817e1e9b255b6af091ac4a14bdfadb81a144de6f4badf98b5cf7` |
| 2 | 3,023 | `24453c21cbce89b2bfb02b735139c46579a3126952d235fc050ad6c39e670cc6` |

Both retained live-text dumps equal all 1,702,912 original file-backed .text bytes,
not only their hashes or the entry prefix. Each marker observation matches its
complete static label-plus-NUL identity and mapped VA, with bytes_equal true.
The exact frozen debugger script reads and compares those memory ranges. Raw
marker and saved-stack-byte dumps are not separately retained; their observed
identities/value/length are recorded in observation.json and audited against the
pinned read logic and expected static values. This review does not pretend to
perform a second live memory read.

The two observations are identical:

| Observation | Before | After one PUSH EBP |
| --- | --- | --- |
| PC | `0x00401000` | `0x00401001` |
| CS | 7 | 7 |
| ESP | `0x7FFF0FFC` | `0x7FFF0FF8` |
| Prior EBP / saved four-byte value | `0x7FFF1000` | `0x7FFF1000` |

Each event sequence is host-start StopEvent, identified hardware BreakpointEvent,
then a single StopEvent for the requested step. The debugger text independently
shows the entry address, next address and normal inferior exit. Both observations
record exits [0], no errors and no unexpected signals. Both process return codes
are zero, with no timeout and empty stderr. The complete 31,584-byte ordinary help
output, SHA-256
`539587cda84463e05efa58667977ee77a81ac8238f03b3ac0d09cf05be248ce6`,
is pinned, byte-identical between trials and occurs unchanged inside each
debugger stdout. PID/build-path differences are retained in logs/reports; those
whole reports are not claimed byte-identical.

The primary's final WSL log confirms **340 tests passed, zero skipped** on the
frozen source. The Windows full-suite log runs 340 tests successfully with **two
native GCC staging tests skipped**, because those controls require WSL/Linux.
Those results are reported distinctly. The helper also passes all eleven new
transport controls on both hosts before live trials. The initial Windows -O
preflight failure and reconstructed prior source remain explicitly preserved.

Both current header prefixes remain zero. The original 3M record is reread and
still INCONCLUSIVE under its original PE-header criterion. The new result is
only VERIFIED_BOUNDED_TRANSPORT for the separately frozen text/marker/one-step
contract. It does not validate optimizer hooks, diagnostic-call activation, pass
layouts, IR capture, full debugger portability or object neutrality. No source
or object was generated, no game executed, no toolchain selected and no matching
progress credited.
