> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3T: original overlay initialization — completed checkpoint

**The original executable consumes header words `0x18`/`0x1C` as an ordered
initialization-call range.** They are no longer merely unexplained addresses.
No source was rewritten and no game code was executed.

Three bounded runtime/consumer ranges, one load-time caller and one recovered
callback were inspected. Every main-image instruction equals its original ELF
word. The caller's table contains the root address followed by exactly all
twelve known overlay load starts. The sole direct main-text call to the header
consumer is retained and independently verified. The representative callback
sets arguments `1` and `65535` before a tail jump; its target was not inspected.

`OVERLAY_LOADER_ANALYSIS.md` records the exact data flow, branch-likely delay
slots, ordering, original import NIDs and limits. The related MHP2G `.ctor`
link-layout comparison is in `OVERLAY_LOADER_SEMANTICS_REVIEW.md`; independent
original-byte and control-flow checks are in `BUCKET_03T_VALIDATION_NOTES.md`.
Private extracts/report are under `evidence/bucket-03t/`.

This establishes initialization callback bounds, not that every entry is an
individual C++ constructor. The caller's opaque return value, registry helper
ownership, complete module inventory and slot capacities/lifetimes remain
unresolved. The original 3R/3S raw reports stay unchanged. No new production
tooling was added; the last full tooling suite remains **329 passed, zero skips**
from 3S, separate from this bucket's static checks.

Decisions preserved: original PSP v1.02 first, readable source, no per-function
flag changes, private evidence, source participation plus all-module byte gate
required before credit, and matching all game code before port implementation.
Counters remain one parked routine, one commented-shape function, zero register
pins, zero empty-asm lines, zero credited matches and zero linked-source functions.
The historical compiler/global profile is still unlocked; full-game gate and
eighteen negative tests are still unimplemented.

Completed within the user's timed advance approval, pending their later review.
A separately planned next bucket may improve the compiler-debugger identity
check using the verified runner's section-loading behavior; that must preserve
3M's inconclusive result and require new independently reviewed criteria.
