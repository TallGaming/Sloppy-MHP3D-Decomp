> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3V: C++ producer fingerprints — completed checkpoint

**The sampled overlay has a concrete static C++ object initialization/cleanup
pattern compatible with GCC's documented selector/priority convention.**
The selected wrapper passes `(1, 65535)`; its dispatcher selects initialization
or cleanup for a global object at the exact declared BSS start. Corrected
selected target bodies are 56 and 20 bytes; an 84-byte selector completes the
three-body scope. Larger preliminary windows containing neighboring methods
remain retained and explicitly labeled.

The object receives a table address with code entries and two preceding zeros.
That layout is compatible evidence, without proving a specific ABI flag or
compiler. Three main-image C++ runtime names also occur in the pinned GNU
runtime archive, so their presence can have a library-only explanation. No
new library ownership is assigned. Other callbacks/callees remain uninspected.

Details are in `CPP_INITIALIZATION_FINGERPRINTS.md`, public-source review in
`CPP_INITIALIZATION_FINGERPRINT_REVIEW.md`, and independent byte/provenance audit
in `BUCKET_03V_VALIDATION_NOTES.md`. Private extracts and a deterministic report
are under `evidence/bucket-03v/`.

Compiler family exclusivity, version, whole-game source language and global
profile remain unproved. All three known families remain hypotheses; no compiler
or game ran in this bucket. The last suite remains **340 passed under WSL, zero
skips** from 3U. No source was rewritten, so the parked initializer, its three
plain attempts/one commented trick, and all four drafts remain unchanged.
Credited matches and linked-source functions remain zero. The full-game gate
and eighteen negative tests are still unimplemented; native-port work is deferred.

Completed within timed advance approval, pending later user review. The next
bounded proposal is an invented C++ static-object producer comparison under
fixed existing O2 profiles, reviewed/frozen before compilation. Resemblance
alone does not reopen the parked archive routine or lock the toolchain.
