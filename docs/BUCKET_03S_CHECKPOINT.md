> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3S: complete known-overlay recovery — completed checkpoint

**All 355 known overlay images have been recovered twice, with every complete
byte matching across the two fresh sets.** The original movie pilot is included,
so this adds354 unique images to the earlier one. No code was executed or
rewritten, and no matching-source credit is claimed.

| Per-set content | Bytes |
| --- | ---: |
| Header bytes | 22720 |
| Declared code regions | 8284380 |
| Declared data regions | 6785764 |
| Complete stored images | 15092864 |
| BSS, metadata only | 6558848 |

Outputs are `reference/uljm05800-v102/overlay-sets/run-1` and `run-2`, each with
355 payloads and its canonical manifest. Both bundled manifests and both
external reports are byte-identical, 588075 bytes, SHA-256
`b57f0a00489860f9bc9fc7282324098f23988f64f664bc53d02141cffcfeda22`.
The frozen recovery profile SHA-256 is
`e5f9c9ba4ce99ace0d433b68e33299383976a26b88b047dc27749ea615a17544`.
Commands and publication boundaries are in `OVERLAY_SET_RECOVERY.md`.

The frozen3R inventory is reproduced before decoding; full ISO/catalogue,
ELF/table, metadata and preserved draft identities pass again before publishing.
The movie pilot's complete encoded/decoded identities reproduce exactly.
All reservation candidate lists and their169 value ambiguities remain intact.

All 355 raw-address spans are bounded:52 empty and303 nonempty, containing340
aligned values inside the corresponding declared code regions. No constructor,
entry-point, callability or function-boundary semantics follow from this alone.
Their actual loader use is a separate bounded static-analysis question.

## Validation and limits

All **329 tooling tests pass, zero skips**, including nine new recovery and
publication controls. Review found and closed final staged-directory/manifest
link acceptance before any real recovery. Injected stage-link substitution is
rejected without traversal/publication; standard cleanup may leave that injected
link for explicit removal. The actual two successful runs leave no stage residue.

The validation helper independently reimplemented full decoding from the ISO
for every image and verified all 710 payload copies, code/data hashes and raw
observations. The other helper independently checked all files/manifests and
inverse-transformed each image to reproduce every encoded hash. Both final
pre-recovery approvals preceded the status-only freeze and actual recoveries.
Source/profile/test bytes remain frozen; all parked drafts are preserved.

Reviews are `OVERLAY_SET_RECOVERY_REVIEW.md` and
`BUCKET_03S_VALIDATION_NOTES.md`; freeze, reports, test log, observed totals and
verification summary are under `evidence/bucket-03s/`.

Known recovered images now total 355; this is not a proven complete inventory
of every possible code module/library in the image. The initializer remains
PARKED with one commented shape, zero pins/empty asm, and zero game-match or
linked-source credit. The toolchain remains unlocked; the full-game gate and
its eighteen negative checks remain unimplemented. Runtime and port work remain
deferred.

Next useful investigation under the remaining timed approval: statically trace
the original loader's treatment of the raw address words, with bounded function
boundaries/call evidence and no source rewrite or runtime execution.
