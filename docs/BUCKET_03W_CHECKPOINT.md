> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3W: invented C++ producers — completed checkpoint

**All three installed C++ producers work, and each complete fixture object
repeats exactly across two fresh runs.** GNU alone among these exact tested
default profiles emits the selector/priority convention observed in the original
P_v00 sample. MW uses `__sinit_` plus global-object registration; SNC uses
`__sti__` plus destruction registration. Relocation records confirm the calls.

The natural fixture has no matching tricks. Existing O2 profiles remain fixed;
only the predeclared C++ language/frontend selection changes. Complete object
sizes are MW6528, GNU6312 and SNC2456 bytes. Exact hashes and ABI/layout details
are in `CPP_PRODUCER_COMPARISON.md`, with independent reviews in
`CPP_PRODUCER_COMPARISON_REVIEW.md` and `BUCKET_03W_VALIDATION_NOTES.md`.
Private reports, freeze and the reviewed fixed driver are under
`evidence/bucket-03w/`; the two fresh build directories retain all raw outputs.

Both exact reviews preceded the freeze and all six compilations. All inherited
and parked-input pins hold. Pure invented/mocked checks cover object drift/link
rejection, decoder failures, relocation extents and unsupported function extents.
There is no new production tool/test suite; the last full suite remains
**340 WSL passes, zero skips** from 3U.

This prioritizes GNU-compatible C++ investigation without locking a historical
compiler/version/profile or attributing all game units. The fixture does not
match original bytes and does not infer original flags. No original source was
changed, target scored, object linked or game executed. The initializer remains
PARKED; plain/trick budgets and all counters are unchanged. The full-game gate
and eighteen negative checks remain unimplemented; no native-port work.

Completed under timed advance approval, pending later user review. A bounded
follow-up can test the already retained archive draft under the newly supported
GNU C++ lead, using the exact existing fixed profile and unchanged source, with
the historical MW control and prior naming review. New independent 3V/3W
producer evidence supplies the documented revisit reason; it does not authorize
more source forms or a flag search, and parking/credit stay unchanged.
