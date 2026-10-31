> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 2 independent validation notes

Reviewed on 2026-10-30 by the validation helper. This checks reference recovery
tooling and one recovered overlay. It is not a game build, source match, runtime
test or the future matching gate's 18 negative checks. No commits were made.

## Automated checks

From `<project-root>`:

```powershell
python -m unittest discover -s tests -v
```

Result: **70 tests passed** (exit 0): all 49 existing checks and 21 new overlay
checks. The new fixtures contain invented ISO9660, archive, substitution-table,
MWo3 and MIPS ELF bytes. Failure tests mutate only temporary fixtures.

The new checks cover:

- Fixed decode vectors constrain byte substitution, little-endian words and
  advancing the modular state before the first word. Invalid seeds, incomplete
  words and non-permutation substitution tables fail.
- Directory lengths/counts, block-table bounds/ordering, exact-size pair bounds,
  duplicate indices and lengths exceeding padded extents fail clearly. An opaque
  tail is left uninterpreted. Exact stored length remains distinct from padding.
- MWo3 magic, stored size, ASCII terminated safe names and 32-bit memory bounds.
  BSS contributes reservation bytes but no stored bytes; raw address fields keep
  provisional meanings.
- A full synthetic pipeline freshly verifies the ISO/archive/ELF and pins, reads
  only the bounded directory and one exact selected extent for decoding, and
  publishes exactly one unpadded payload. A payload-limit failure happens before
  reading or decoding that payload.
- Wrong reference selection, changed input files, wrong table file/virtual
  location, directory/output hashes, selected index/extent, header, descriptor and
  reservation fail before publication. The ELF must be executable and the named
  zero-size descriptor must be allocated PROGBITS.
- Repeat runs decode again and produce identical payload/evidence. Conflicting
  existing payloads/reports and failed repeats preserve prior files. Report/input
  or report/payload aliasing and a bad staged identity are rejected.
- The CLI reports a failed input and creates neither payload nor report.

## Independent checks of real outputs

The validator independently streamed the entire original ISO and DATA.BIN for
SHA-256 verification, opened the image read-only, read the selected encoded
extent and reproduced its decode with a separate spelling of the documented
substitution/modular-XOR algorithm. No game code was executed.

- The ISO remains 1,207,140,352 bytes, SHA-256
  `20a3b77c76f3729843f4e945fe4f04085edd6f37aa6122399d296d7f2e9c3dd8`.
  Its size and modification timestamp were unchanged during validation.
- DATA.BIN at LBA 55968 remains 1,092,495,360 bytes, SHA-256
  `cb1229171c2a7bcc11716a2cd5a2bb3c40a242f0d614bb88aa50cbedfb60426e`.
- Entry 101's exact encoded extent is 1280 bytes at archive block 268538,
  SHA-256 `9a825ce43736d0869e67f9f56ea9ba3af4679fdd01748e806e11ce2bb2e982bb`.
  Its padded extent is 2048 bytes; padding is excluded from the recovered file.
- The independently decoded bytes equal both
  `reference/bucket-02/final-run-1/movie_task.ovl.mwo` and `final-run-2/`'s file:
  1280 bytes, SHA-256
  `6a918f7af824103cfe5df0c4fb8d793c430a273b166a8eaf5ce1e5cd66951abb`.
- `evidence/bucket-02/final-recovery-run-1.json` and `final-recovery-run-2.json`
  are byte-identical: 2037 bytes, SHA-256
  `65d5e42417609d16a99dfd9f185e8f5619d6b92d9f27093a3c6b38f69f1de9eb`.
- Header name/load address agree with allocated zero-size ELF descriptor 337.
  Header ID 158 agrees with PT_NULL index 158; load address `0x09C57C80` and
  reservation `0x580` agree with the 1280 stored bytes plus 128 BSS bytes.

The reviewed directory interpretation uses 5955 entries, 5956 block words and
1289 exact-size pairs. Entry zero starts at block 17, after the directory prefix;
the prefix is not itself an indexed entry. Its final 680 bytes remain opaque.

## Reviewed identities and findings

| File | SHA-256 |
| --- | --- |
| `scripts/extract_overlay.py` | `6f91572be1e5772129c39f17995c7d7b9f829df7133764f5816e6bb85c30c863` |
| `config/overlay-pilot.json` | `1f972b87c2d5a0187dff70b1b0494592f22f04a29d6e529ef9fde209a03eb7ab` |
| `tests/test_extract_overlay.py` | `992867fbe2a0f516db2fd7f08c262a9ef838b979437d3b63eab2b870affb2ba0` |

Review prompted explicit ET_EXEC/allocated-PROGBITS validation and checking the
decode table's virtual-address mapping against its pinned file range. These
checks are present and tested. An incorrect draft statement calling the
directory indexed entry zero was flagged for correction.

No material blocker remains in the reviewed extraction paths. Pins and static
value correspondence support this selected recovery; they do not establish
every overlay's index/reservation association, the meaning of both raw address
fields, complete code-module coverage, original compiler configuration, source
language or gameplay behavior. Exactly one complete overlay was recovered in
this bucket; no matching credit is implied.
