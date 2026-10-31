> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Known-overlay set recovery review — Bucket 3S

This bucket may recover only the 355 overlay images identified by the frozen
Bucket 3R header inventory, into two fresh private output sets. It does not
establish a complete all-module inventory, rewrite functions or revisit the
parked initializer. The independent reviewer does not invoke a compiler or
recover additional payloads outside the primary's declared runs.

## Pre-recovery constraints

The selected inventory report is 3,380,121 bytes, SHA-256
`a7a3b1e7b88aefd342a4fdc4924200570496cd62abb241bd093165f5d383991f`.
Its known images declare 15,092,864 stored bytes in total, with maximum individual
length 1,525,632. All selection is frozen before payload recovery. The original
PSP v1.02 reference, directory/table pins and decoder remain authoritative;
neither an HD list nor a signature search may add more images to this set.

The recovery implementation must revalidate the frozen report through a fresh
bounded prefix inventory before using its image list. Each complete read must
stay within the index-declared stored length and archive extent, remain within
the new two-MiB per-image bound, decode complete words from the entry seed and
agree with the exact frozen header. The already recovered movie pilot must
agree in encoded/decoded bytes and identities, not just name or length.

For every selected image, report encoded/decoded identities plus separate
header/code/data identities and BSS metadata. Hashing decoded reference bytes
is not source matching or validation of code behavior. Stored bytes and BSS
remain separate; reservation candidates and all 169 prior value ambiguities
must not be collapsed after full recovery.

All selected files must validate in a private staging directory before a fresh
output directory is published. Destination/report/input aliases and links,
existing outputs, path escapes and filename collisions must be rejected.
Archive-indexed filenames preserve identity even if names repeat. Staging
cleanup must remain within its verified intended directory and must not delete
or replace an earlier output set or reference input.

Optional inspection of raw `0x18/0x1C` spans is limited to the declared bounded
range (at most 128 bytes) and records raw words/alignment/range observations.
Being aligned or pointing within declared code does not prove a function,
constructor, entry point or initializer table. No initializer-source work is
part of this bucket.

Two sets of 355 files are copies of the same known images. The earlier movie
pilot is already one of those images, so a successful recovery changes the
unique recovered-image total from one to 355, not 356 or 711. No full-game gate,
library ownership, historical toolchain selection or source-link credit follows.
The exact implementation/profile review and final output audit follow below.
No recovery was performed by this reviewer while establishing these constraints.

## Exact pre-recovery source/profile approval

The final reviewed `scripts/recover_overlay_set.py` is 14,354 bytes, SHA-256
`b37a3f6fc0bf4d73040894c3386a392aa1f9d1d9636afcddf19aceed2ab49a10`.
The draft `config/overlay-set-recovery.json` is 2,244 bytes, SHA-256
`c8fc8d74be3703755acf508755b7c13a611f97aca8fc5c0dd36a14688014fbc7`.
Explicit final approval of these exact artifacts was sent before real recovery,
after the other helper reported all nine new controls and 329 full-suite tests
passing. The reviewer did not invoke those controls or a real recovery.

The source verifies the frozen report/profile and preserved scanner/decoder,
all four initializer drafts, its parked assembly and assembly manifest. It
reproduces the entire fresh prefix inventory and requires equality with the
frozen report, then reads only the selected entries at their exact stored
lengths. Each image is bounded to two MiB and complete-word decoding. Decoded
header bytes must equal the frozen 64 bytes exactly; parsed fields and every
descriptor/reservation candidate list must agree as well. The movie pilot's
complete encoded and decoded identities must reproduce their original pins.
Code/data slices have separate identities; BSS remains metadata without new
zero-filled file content.

The only permitted output is a fresh named direct child of the private
`reference/uljm05800-v102/overlay-sets` area. Archive-indexed filenames are
checked for collision. One same-parent private staging directory contains all
payloads and canonical `manifest.json`. Before rename, the source rechecks
locks/profile/ELF/full ISO, every staged payload, exact manifest bytes and the
complete filename set. The atomic published unit is **the directory including
its manifest**. An optional external evidence report is copied afterward; that
separate copy is not part of a cross-directory atomic transaction.

Independent review and the validator both found a final link-substitution gap
before any recovery: the initial implementation could accept a manifest link
to identical bytes or a same-parent stage redirect. The primary added explicit
stage/manifest link checks before manifest comparison and adjacent to rename,
plus final directory/regular-file checks. The reviewer read back that correction
before approving it. The validator reports both substitutions rejected before
publication and no traversal/deletion of their sibling targets. Failed staging
is not published and earlier output sets are preserved.

`observe_address_span` reads only already decoded stored bytes. Reversed,
unaligned, oversized or out-of-image spans remain UNINTERPRETED. A bounded span
records raw words and separate alignment/code-range flags; its aggregate flag
requires both properties. Empty spans have a null aggregate flag rather than
vacuous positive evidence. This model adds no constructor/entry-point semantics.

No new source form, compiler setting or initializer experiment is authorized by
this recovery approval. The final freeze and retained-set audit follow below.

## Frozen recovery and independent published-set audit

The frozen profile is 2,244 bytes, SHA-256
`e5f9c9ba4ce99ace0d433b68e33299383976a26b88b047dc27749ea615a17544`.
Replacing only its status reconstructs the exact reviewed draft identity above.
`evidence/bucket-03s/profile-freeze.json` records both final approvals received
before recovery at `2026-10-31T06:21:24.667247Z`. The reviewed recovery source
still has the same hash; all preserved draft/assembly/scanner pins agree after
the runs.

The two private sets are:

- `reference/uljm05800-v102/overlay-sets/run-1`
- `reference/uljm05800-v102/overlay-sets/run-2`

Each contains exactly 355 regular, archive-indexed payload files and its regular
`manifest.json`, with no links, extra files or remaining `.overlay-set-*` stage.
The reviewer independently read all **710** payload files, checked their
complete size/SHA-256, exact frozen header bytes, code/data slice identities,
BSS metadata, naming/bounds and every descriptor/reservation candidate list.
Every corresponding image agrees between sets. Both bundled manifests and the
two external `recovery-run-*.json` evidence reports are byte-identical: 588,075
bytes, SHA-256
`b57f0a00489860f9bc9fc7282324098f23988f64f664bc53d02141cffcfeda22`.

The reviewer also independently reconstructed the inverse substitution/XOR
transform and re-encoded every first-set decoded image in memory. All 355
complete encoded identities reproduce the manifest. This checks full algorithm/
identity consistency without another archive-body read; it is not described as
an independent new read of the original encoded images. The second helper's
separate original-archive read and independent decoder comparison are recorded
in `BUCKET_03S_VALIDATION_NOTES.md`.

The movie image at archive index 101 matches the earlier complete pilot file
in every byte, as well as its original encoded/decoded size/hash pins. It is
one member of this set, not an additional image. Known unique recovered images
are now **355**, an increase of 354 from the earlier single-payload recovery.
The two sets are reproducibility copies; they do not multiply that coverage.

| Per set | Verified bytes / status |
| --- | ---: |
| Complete stored images | 15,092,864 |
| Header bytes | 22,720 |
| Declared code slices | 8,284,380 |
| Declared data slices | 6,785,764 |
| BSS | 6,558,848, metadata only |
| Largest individual stored image | 1,525,632, below the two-MiB limit |

The file lengths exclude BSS; no zero-filled reservation was appended as if it
were stored payload. These code/data ranges are exact header-declared slices
with recovered byte identities, not proof of function boundaries, SDK/game
ownership, instruction reachability or a full-game coverage denominator. All
169 reservation-value ambiguities and shared-start overlap caveats survive
unchanged in the manifests through their original candidate lists.

## Raw-address-span audit and stopping boundary

Independent observation of the already recovered files reproduces every raw
span word and flag. All 355 spans fit the declared bounds: 52 empty spans with
null aggregate flags and 303 nonempty spans containing 340 raw words in total.
All those nonempty values are word-aligned and within their own image's
declared code range. This is range compatibility only. It does not identify
constructors, entries, complete functions, callable targets or original language
and class boundaries; no word or instruction was executed.

The recovered payloads and bundled manifests remain ignored local reference
material. The parked initializer, all four retained source drafts and the
original compiler settings are unchanged. This bucket recovers the frozen
known set; other raw module signatures and unknown archive forms still prevent
a claim that every code module has been identified. No game source was compiled
or linked, the full matching gate and eighteen negative checks remain absent,
runtime testing remains deferred, and native-port implementation has not begun.
No remaining payload/map/publication inconsistency was found in this bounded
independent audit.
