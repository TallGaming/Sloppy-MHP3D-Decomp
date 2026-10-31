> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Recovering the known PSP overlay set

The verified sets are local at
`reference/uljm05800-v102/overlay-sets/run-1` and `run-2`. Each contains the same
355 original MWo3 images and a deterministic `manifest.json`. The earlier movie
pilot is among these images, so total unique recovered images are355, not 356.
Game bytes remain outside version control.

To create another fresh set from the locked original PSP image:

```powershell
python scripts/recover_overlay_set.py --iso "<game-image-directory>\Monster Hunter Portable 3rd (Japan) (v1.02)\Monster Hunter Portable 3rd (Japan) (v1.02).iso" --out-dir reference/uljm05800-v102/overlay-sets/review-copy --report evidence/bucket-03s/review-copy.json
```

The destination must be a new direct child of the reviewed private output area.
Existing directories/reports are refused. The tool reproduces the complete
prefix inventory before decoding bodies, then checks every complete header,
association list and the movie pilot's full known bytes. Each image is bounded
to2MiB. Archive-indexed filenames keep distinct images separate even if names
repeat. The original archive and all other assets are opened read-only.

Every image records encoded/decoded hashes, separate header-declared code/data
hashes and BSS size. BSS is not written into the stored image. A private staging
directory contains all 355 files and the canonical manifest; final identity,
link/type and exact-file-set checks precede a same-parent rename. The bundle
with its manifest is the publication unit. An optional external report copy
can fail after a valid bundle has been published; its internal manifest remains
the authoritative record.

The two final header words are preserved as raw addresses. When their proposed
span is within the image, word aligned and at most 128 bytes, the manifest records
its raw words and whether their values are aligned/inside the declared code
region. Invalid spans remain UNINTERPRETED without invalidating recovered
bytes. This observation is not a constructor/entry-point interpretation or
proof of function boundaries.

Each set contains 15092864 stored bytes: 22720 header bytes, 8284380 code bytes and
6785764 data bytes. Declared BSS totals 6558848 bytes. Both 588075-byte manifests
have SHA-256 `b57f0a00489860f9bc9fc7282324098f23988f64f664bc53d02141cffcfeda22`.
Every complete output was independently decoded from the original ISO; an
independent inverse transform also reproduces the encoded identities.

This is reference preparation, not source reconstruction or a matching build.
The complete all-code-module inventory, locked compiler/global profile, source
participation gate and eighteen negative build checks remain separate work.
See `BUCKET_03S_CHECKPOINT.md` and the two independent review documents.
