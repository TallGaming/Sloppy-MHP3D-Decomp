> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3R: known-overlay prefix inventory — completed checkpoint

**All 355 named ELF overlay descriptors now have one validated archive header.**
Two fresh scans of all 5955 entries produce identical reports, with no malformed
MWo3 claims, missing descriptors or duplicate header associations. This covers
known headers; it recovers no additional complete payload and does not establish
the complete game-code inventory.

| Observation | Result |
| --- | ---: |
| Entry prefixes inventoried | 5955 |
| Nonempty prefixes / bytes read | 5952 / 380928 bytes |
| Largest entry prefix read or decoded | 64 bytes |
| Valid deobfuscated MWo3 headers | 355 |
| Named descriptors uniquely covered | 355 |
| Distinct named load starts | 12 |
| Headers with multiple address/size-compatible reservations | 169 |
| Header-ID values agreeing with compatible program-header indexes | 355 |

The reservations' candidate-list lengths range from one to ninety. Their numeric
ID agreements are independently reported, without discarding other structurally
compatible records. `download_task.ovl` and `lobby_task.ovl` have declared ranges
extending past the next distinct named start; those starts cannot be treated as
capacity boundaries or a proven lifetime model.

Headers declare 15092864 stored bytes and 8284380 code bytes across these images;
the largest stored image is 1525632 bytes. Those are declarations, not newly
decoded body coverage. Words 0x18/0x1C remain raw addresses. Their spacing/range
statistics do not by themselves prove constructor or entry-point semantics.
The archive also contains raw `~SCE` prefixes at entries 17–20 and `PSMF` prefixes
at 81–92; signatures alone do not classify library ownership or all code modules.

## Evidence and validation

Both 3380121-byte reports have SHA-256
`a7a3b1e7b88aefd342a4fdc4924200570496cd62abb241bd093165f5d383991f`.
They are `evidence/bucket-03r/overlay-inventory-run-1.json` and `-2.json`.
The frozen profile `config/overlay-inventory.json` has SHA-256
`bddd4163726e3b303a05fb2b0fa725e3f3d2ba016657288c0c11f6c2e6cd796f`.
The corrected frozen scanner's SHA-256 is
`628643e527cdd88e5c266047e744534ce446713e97fdd37d041d6b48db13d24e`.

The first invocation stopped before prefix decoding because it passed the full
multi-checksum lock to an inspector reporting only size/SHA-256. That failure,
original scanner and original freeze remain preserved. Both helpers reviewed
the narrow API correction before successful scans. Full catalogue checksums
still pass before and after scanning; nothing was loosened to fit archive data.

All **320 tooling tests pass, zero skips**: eleven new controls cover headers,
short/empty bounds, raw/deobfuscated claims, duplicate associations, source drift,
aliases and catalogue-checksum compatibility. The validation helper independently
read every actual prefix and reimplemented decoding to verify all header fields
and identities; the map reviewer independently checked all ELF associations.
See `OVERLAY_INVENTORY_REVIEW.md` and `BUCKET_03R_VALIDATION_NOTES.md`.

The initializer remains PARKED, with one counted commented shape and zero
register pins/empty asm. No compiler/profile/game source changed; no game code
ran and no native-port work occurred. Credited matches/linked source remain zero;
full-game gate and eighteen negative checks remain unimplemented.

Next useful bucket: recover the complete bytes of these frozen 355 images into
fresh private reference directories, verify complete headers/pilot equality,
compare two independent repeat manifests and retain every ambiguity. This is
reference preparation under the remaining timed approval, not a matching rewrite.
