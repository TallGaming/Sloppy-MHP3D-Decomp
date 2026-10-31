> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3S independent validation

## Pre-recovery review

This bucket recovers exactly the images in the frozen complete known-overlay
header inventory. It reproduces that inventory through the original ISO/table/
directory/ELF chain before complete decoding, bounds each image at 2 MiB and
requires the earlier movie pilot's full identities. It creates no source match,
compiler identification, game execution or new all-code inventory claim.

The approved 2,244-byte draft recovery profile has SHA-256
`c8fc8d74be3703755acf508755b7c13a611f97aca8fc5c0dd36a14688014fbc7`.
The reviewed final script is 14,354 bytes, SHA-256
`b37a3f6fc0bf4d73040894c3386a392aa1f9d1d9636afcddf19aceed2ab49a10`.
Only protocol status is expected to change before the real recovery.

Archive-indexed filenames avoid collisions from repeated header names. Full
stored image, code and data bytes are hashed separately; BSS remains metadata.
The directory's payload files and canonical manifest are staged and checked
before one same-parent rename. Existing output directories and input/report
aliases are refused. An optional report in a separate evidence directory is
copied after publication: the bundle plus its own manifest is the atomic unit,
not both independent directories.

Both reviewers find that final staged-directory and manifest link checks were
missing. The primary adds explicit link/type rejection before publication while
source/profile are still unexecuted drafts. Invented identical-byte manifest
symlink and same-parent stage-redirection controls confirm that no link can be
published. TemporaryDirectory cleanup may refuse an injected staging-directory
symlink and raise OSError; it does not traverse/delete its sibling target. The
control verifies no final output/report and removes only its injected artifacts.
This is failure residue rather than successful publication or silent recovery.

## Meaningful controls

Nine new tests use the genuine nested invented ISO/ELF/reference/pilot/inventory
chain. The decoder, directory parser and header parser are not mocked. These cover:

- Exact full payload, encoded/code/data identities and metadata-only BSS, two
  fresh bundles with byte-identical manifests and preserved original inputs.
- Two overlays with the same filename at different indexes and bases, without
  overwriting either original image.
- Frozen-set equality, duplicate indexes, invalid length/scope, altered
  header/prefix records and the mandatory pilot's full-body identity.
- Valid bounded raw-address words, empty spans, misalignment/reversal/overflow
  and unsupported spans that stay UNINTERPRETED without discarding a valid image.
- Existing output/evidence, output placement and input/report aliases, rejected
  before recovery or publication.
- Late mutations of all inherited inputs and preserved drafts, including ISO
  mutations with a restored timestamp, preventing bundle publication.
- Staged payload/manifest bytes, extra files and link substitutions preventing
  publication; external evidence failure preserving an already complete bundle
  whose own manifest still verifies.

Independent execution passes **9 new tests and all 329 tooling tests, zero
skipped**, preserving the preceding 320. These do not implement or pass the future
full-game gate or its eighteen negative tests. The test file is 16,065 bytes,
SHA-256 `2b9232d1ff86270f64c08407feaa58a6f2fe648781a38796b4851278eec3d924`.
No helper invokes a compiler or recovers real payloads before profile freezing.

## Actual complete-image audit

Both fresh complete sets pass independent verification. The deterministic reports
and both bundled manifests are byte-identical: 588,075 bytes, SHA-256
`b57f0a00489860f9bc9fc7282324098f23988f64f664bc53d02141cffcfeda22`.
Sets are retained at `reference/uljm05800-v102/overlay-sets/run-1` and `run-2`.
The frozen 2,244-byte profile has SHA-256
`e5f9c9ba4ce99ace0d433b68e33299383976a26b88b047dc27749ea615a17544`;
replacing only the frozen status reconstructs the approved draft hash.

Read-only independent audit checks the complete current ISO catalogue digest set,
ELF/decode table, inventory profile/report and all preserved draft/assembly pins.
Using an independent implementation of byte substitution and the modular XOR
sequence, the helper reads and decodes every complete selected image directly
from the original archive. No recovery-script decoder or header parser is used
for these actual full-byte comparisons. All 355 images equal both private output
copies in every byte, so all 710 output files reproduce their original decoded
source images. Every encoded/decoded/code/data hash, complete length, descriptor/
reservation association and mandatory pilot identity agrees with the report.

| Per recovered set | Bytes |
| --- | ---: |
| All 355 stored images | 15,092,864 |
| Headers | 22,720 |
| Declared code ranges | 8,284,380 |
| Declared data ranges | 6,785,764 |
| BSS, metadata only | 6,558,848 |
| Largest stored image | 1,525,632 |

Each output set contains exactly its 355 archive-indexed images and manifest;
no extra file, link or staging directory is present. BSS is excluded from stored
payloads. ISO metadata remains unchanged after the independent readback. The
stored images remain local private reference material, outside source control.

All 355 raw-address spans fit the bounded model. Fifty-two are empty; the other
303 contain 340 raw words in total. The independent observer recomputes every
word value, alignment and code-range compatibility flag. All words in those
nonempty spans meet the declared code-range/alignment test. This does not identify
constructors, entry points, functions or original C++ class/language boundaries;
no word is executed and the two address fields retain raw names. Unsupported
span handling remains covered by invented controls, even though no actual span
requires UNINTERPRETED here.

Full recovery now covers the frozen known 355 images. It does not establish that
all possible code modules/libraries have been identified, decode other archive
assets, reconstruct sources or justify native-port work. The initializer remains
PARKED, matching/linking/runtime credit stays zero and the toolchain remains
unlocked. All 329 tooling tests remain separate from the full-game build gate.
