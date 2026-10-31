> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3U: compiler transport identity — completed checkpoint

**Both fresh help-only trials satisfy the new bounded debugger contract.**
The unchanged compiler's entire 1,702,912-byte file-backed `.text` matches its
live memory, together with three mapped diagnostic strings including NUL bytes.
The known first instruction advances PC `0x00401000` to `0x00401001`, decreases
ESP `0x7FFF0FFC` to `0x7FFF0FF8`, and saves EBP `0x7FFF1000` in four bytes.
CS remains seven. This checks the observed guest stack effect of one instruction.

Both ordinary and debugger invocations exit zero without timeout or diagnostics;
the inferior explicitly exits zero. Each complete 31,584-byte ordinary help
output matches the historical pin and appears verbatim in debugger output.
Compiler, runner, debugger and all frozen input identities remain unchanged.
Both final independent reviews preceded the status-only input freeze and both
live trials. Neither helper ran another compiler/debugger invocation.

The earlier 3M result remains **INCONCLUSIVE** under its original header-based
criterion. The new section-based contract was independently reviewed and frozen
before execution; it does not reinterpret that historical failure as success.

| Retained result | Fresh private build directory |
| --- | --- |
| `evidence/bucket-03u/trial-1.json` | `build/compiler-transport-xbwdlv2a` |
| `evidence/bucket-03u/trial-2.json` | `build/compiler-transport-c8v91xbl` |

The final driver is 14,332 bytes, SHA-256
`a1192eb0f9e6bd84eed89b29721b014880ac77eaf65ad41dccfd208a18ab9352`.
The profile is 1,980 bytes, SHA-256
`488194115646ddfd7d6babaabf68defe6c5f6b5f1b6a53b3fa1fc9b7f2556033`.
The 1,230-byte freeze SHA-256 is
`6130ac2479474096d16860adbb738a45151c75763389c6504f7e4f5e9efdd574`.
Commands and exact contract are in `COMPILER_TRANSPORT.md`; independent reviews
are `COMPILER_TRANSPORT_IDENTITY_REVIEW.md` and `BUCKET_03U_VALIDATION_NOTES.md`.

All **340 tooling tests pass under WSL, zero skips**, including eleven new
transport controls. Windows runs all 340 cases with 338 passing and two explicit
native-GCC-only skips. A pre-freeze Windows unit failure found that the launch
platform guard intercepted the intended invalid-mapping check. Moving the same
guard after pure static checks, still before process/directory creation, fixes
the test on both hosts. The original failure and an explicitly reconstructed
prior source matching its previously recorded hash are retained. Static input
assertions were also replaced with mandatory checks before the final reviews.

No source was compiled, object produced, optimizer hook validated or IR decoded.
Object-output neutrality still needs a separate invented-fixture experiment.
No game ran; historical compiler/global profile remains unlocked and the archive
initializer remains PARKED. Counts stay one commented-shape function, zero pins
or empty asm, and zero credited matches or linked-source functions. The full-game
byte gate and its eighteen negative checks remain unimplemented.

Completed under timed advance approval, pending later user review. A useful
next bounded question is whether original C++ initialization patterns provide
producer evidence beyond the executable's link/runtime markers; this would be
a separate bucket and would not reopen the parked routine without evidence.
