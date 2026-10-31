> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Original overlay initialization ranges

Bucket 3T, 2026-10-31. Read-only static evidence from the pinned PSP v1.02
executable and the recovered `P_v00.ovl`; no game code was run or rewritten.
The analytical names below are descriptive labels, not recovered symbols.

## What the original code establishes

The original consumer at `[0x08915200, 0x08915270)` loads header words `0x18`
and `0x1C` and passes them unchanged as the first two arguments to
`[0x0891512C, 0x089151A0)`. That helper treats them as the beginning and
exclusive end of an array of four-byte function addresses. It tests unsigned
`begin < end`, calls each stored address, advances by four, and repeats while
the iterator remains below the end. It performs no null, alignment or executable
range checks in this inspected code.

The loop's `bnezl` at `0x08915170` loads the next address in its taken delay
slot; the load is annulled when leaving the loop. This matters when assessing
whether the end address is read. There is no explicit per-element argument setup:
the calls are consistent with initialization callbacks, but this alone does not
prove their language-level signatures.

After the calls, the helper passes its saved third/fourth arguments to
`[0x089151A0, 0x08915200)`, which searches sixteen two-word records and writes
the arguments into a selected record, then overwrites the second word with
`argument_2 - 12`. Its full purpose and ownership remain unclassified. The
header consumer supplies zero for both arguments. We do not rename this code
as Sony SDK or a particular C++ runtime from this resemblance alone.

## Load-time context and ordering

The consumer first reads header `+0x14`, then calls import stubs `0x08960C70`
and `0x08960C80`. The original import table associates these with `UtilsForUser`
NIDs `0x79D1C3FA` and `0x920F104A`. The pinned community PSPSDK import declarations
identify those NIDs as `sceKernelDcacheWritebackAll` and
`sceKernelIcacheInvalidateAll`, respectively
([declarations at pinned revision](https://github.com/pspdev/pspsdk/blob/460920c0c650ffcdf912863bc170430d08142c37/src/user/UtilsForUser.S)).

When header `+0x14` is nonzero, the consumer calls `0x0880C468` with destination
`header + incoming_argument_2`, fill value zero, and length `header[0x14]`.
This is consistent with clearing declared BSS before initialization callbacks.
The fill callee was not analyzed in this bucket. When the length is zero, the
`beqzl` delay slot loads the initialization start; otherwise the start is loaded
after the call, so both paths provide the same header field to the range helper.

The sole direct J/JAL call to this consumer in the main `.text` is at
`0x088E6510`, inside `[0x088E64A8, 0x088E6544)`. The caller selects the header
address from the table at `0x08A1BE90`. That table has thirteen inspected words:
the main root address `0x08804000`, followed by exactly the twelve distinct
load starts present in all 355 known overlay headers. The caller's final tail
jump goes to `0x08960C80` after the consumer returns.

The caller forwards an opaque virtual call's return value as the consumer's
second argument. Its callee was not inspected, so that return value is not
proven to be a stored-image length here. This caller also does not prove index
bounds, the eligibility of slot zero, archive-load completion or overlay
lifetime/capacity. The table agreement supplies the overlay association without
claiming those additional behaviors.

## One representative callback and the related project

Recovered entry 4590, `P_v00.ovl`, has one word in its header range:
`[0x09E7D300, 0x09E7D304)`, containing `0x09E7D134`. Its sixteen-byte callback
sets the first argument to `1`, the second to `65535` using ORI, and tail-jumps
to `0x09E7D0E0`. That callee was deliberately not inspected. This is an
initialization wrapper consistent with C++ static initialization machinery;
it does not identify a source filename, class, historical compiler build or
global optimization profile.

The pinned related MHP2G reconstruction explicitly emits these two header words
around its `.ctor` section and names them static-initializer bounds. Its
reconstructed link script is corroboration, not our primary proof of MHP3
behavior. Precise source references and differences are in
`OVERLAY_LOADER_SEMANTICS_REVIEW.md`.

## Evidence and limits

Retained private extracts and `loader-analysis.json` are under
`evidence/bucket-03t/`; `analyze_loader.py` checks every retained main-image
instruction against its original ELF word, verifies the complete recovered
payload, compares the table with all known starts, and independently scans
direct J/JAL targets. The JSON report is 3331 bytes, SHA-256
`5c4b8242f6cc5ee178ad8377435237ea73fedf7c272e05283e9b3b140a0800c3`.
The independent audit is `BUCKET_03T_VALIDATION_NOTES.md`.

The known images contain 340 table entries across 303 nonempty ranges and
52 empty ranges. These are entries across alternative images, not 340 proven
unique functions or a trace of calls in one run. The frozen 3R/3S manifests
retain their raw field names and historical uncertainty; this later evidence
adds interpretation without rewriting those observations.

No function receives source-match credit. Library ownership, complete code-module
coverage, compiler/global profile and runtime behavior remain unresolved. The
archive initializer remains visibly parked with all source drafts preserved.
