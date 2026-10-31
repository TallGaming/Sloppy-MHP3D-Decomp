> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 2 checkpoint

2026-10-30. One-overlay recovery is implemented and validated. The user accepted
this output with "Continue"; Bucket 3 proceeds under its separately presented plan.

## Result

Recovered exactly one distinct overlay, `movie_task.ovl`, from the pinned
original PSP ULJM05800 v1.02 image. It is a 1,280-byte MWo3 entry, containing
64 header bytes, 1,160 code-region bytes and 56 data bytes. Its 128-byte BSS
has no stored bytes. No game functions have been rewritten or matched.

| Evidence | Result |
| --- | --- |
| Archive selection | Zero-based payload entry 101, archive-relative block 268538 |
| Original extent | ISO offset `0x279CD000`, padded 2,048 bytes; exact entry 1,280 bytes |
| Decoding | Local ELF substitution table, then modular halfword XOR sequence; no decompression |
| Load address | `0x09C57C80` |
| ELF association | Descriptor 337 has the same name/base; header ID and program-header index 158 agree |
| Reservation | `0x580` bytes, matching stored length plus BSS |
| Decoded SHA-256 | `6a918f7af824103cfe5df0c4fb8d793c430a273b166a8eaf5ce1e5cd66951abb` |

The loader statically confirms a 5,955-entry block table and 1,289 exact-size
records. Entry numbering excludes the directory prefix. The directory's remaining
680 bytes are kept opaque. HD project observations were used as research leads;
the PSP counts, table, addresses and selected payload were verified locally.

## Review locations

- [OVERLAY_RECOVERY.md](OVERLAY_RECOVERY.md): normal command and outputs.
- [ARCHIVE_FORMAT.md](ARCHIVE_FORMAT.md): transformation, loader evidence,
  source attribution, header and descriptor association.
- [extract_overlay.py](../scripts/extract_overlay.py) and
  [overlay-pilot.json](../config/overlay-pilot.json): bounded implementation/pins.
- [BUCKET_02_VALIDATION_NOTES.md](BUCKET_02_VALIDATION_NOTES.md) and
  [test_extract_overlay.py](../tests/test_extract_overlay.py): independent review
  and synthetic checks.

## Validation performed

- **70 tooling tests passed**: 49 existing and 21 overlay-recovery tests. These
  exercise independent fixed decode vectors, malformed indices/headers, extent
  bounds, identity failures, executable/descriptor requirements, staged-output
  failure, and preservation of conflicting files/reports.
- Two fresh real extractions produced directly byte-identical 1,280-byte files
  and directly byte-identical 2,037-byte reports. Report SHA-256:
  `65d5e42417609d16a99dfd9f185e8f5619d6b92d9f27093a3c6b38f69f1de9eb`.
- The documented default extraction command also succeeded.
- Real rejected-HD-image and missing-ELF controls returned exit 1, creating
  neither an output directory nor a success report.
- The validation helper independently hashed the original ISO/archive and
  separately decoded the selected entry; it agreed with both extracted files.
  The image's pinned identity, size and modification time remained unchanged.
- Static disassembly shows coherent MIPS function-shaped code and calls into
  the main executable. No runtime testing was performed.

Final local evidence is under ignored `evidence/bucket-02/`:
`final-recovery-run-1.json`, `final-recovery-run-2.json`,
`verification-summary.json`, `tooling-tests.log`, and `movie_task.disasm.txt`.
The fresh output copies are under `reference/bucket-02/final-run-1/` and
`final-run-2/`; the normal output is under
`reference/uljm05800-v102/overlays/`. All refer to the same single overlay.

## Decisions preserved and limits

The original PSP v1.02 target, readable-source-first policy, fixed-toolchain
requirement and all-game-code matching scope remain unchanged. Compiler build,
flags and original source language remain unproven. SDK/third-party assembly
policy remains unchanged. Matching precedes native-port implementation.

Recovery earns no matching credit: matched functions, source-linked functions,
parked functions, matching tricks and completed gate-negative checks remain
zero. The full byte-match gate is not implemented; the 70 tooling tests are
separate from its 18 required negative checks.

Only one of the 355 named overlay descriptors now has a recovered payload and
an individually checked reservation association. The full code-module inventory
and the other descriptor associations remain open. The two final header address
words have provisional parser names and are not proven callable entry points.
Runtime loading/lifetimes, SDK classification and original source behavior are
not established by recovery.

Review outcome: accept this bucket, request changes, or stop. If accepted,
present Bucket 3's concrete compiler-investigation plan before its work begins.
Minimum native hardware and right-stick camera behavior remain intentionally
undecided. No compiler lock, commit, verified tag or later bucket is approved
by this checkpoint alone.
