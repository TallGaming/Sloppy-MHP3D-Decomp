> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Recover the single overlay pilot

Bucket 2 recovers `movie_task.ovl` from the accepted original PSP ULJM05800
v1.02 image. It does not compile game source, run the game or prove a build gate.
Only this one selected payload is supported by the command.

## Prerequisites and command

Use Python 3.10 or newer. First prepare the pinned decrypted executable using
[REFERENCE_PREPARATION.md](REFERENCE_PREPARATION.md). No new external executable
helper is needed for overlay decoding.

From `<project-root>`, run:

```powershell
python scripts/extract_overlay.py --iso "<game-image-directory>\Monster Hunter Portable 3rd (Japan) (v1.02)\Monster Hunter Portable 3rd (Japan) (v1.02).iso"
```

Outputs:

- `reference/uljm05800-v102/overlays/movie_task.ovl.mwo`: the exact 1,280-byte
  decoded archive entry, including its 64-byte MWo3 header. No padding or BSS
  is appended. SHA-256:
  `6a918f7af824103cfe5df0c4fb8d793c430a273b166a8eaf5ce1e5cd66951abb`.
- `evidence/bucket-02/overlay-recovery.json`: deterministic identity, extent,
  header and executable correspondence evidence.

Both directories are ignored by Git. Existing identical output is accepted;
different output or reports are refused. The original image and executable are
opened read-only. Full image and archive hashes are checked on every run;
fresh ISO9660 metadata locates the game archive, distinct from the updater's
unrelated `SYSDIR/UPDATE/DATA.BIN`.

## Repeatability and failure behavior

Use fresh directories and reports for independent runs:

```powershell
python scripts/extract_overlay.py --iso "D:\path\to\accepted.iso" --out-dir reference/bucket-02/check-1 --report evidence/bucket-02/check-1.json
python scripts/extract_overlay.py --iso "D:\path\to\accepted.iso" --out-dir reference/bucket-02/check-2 --report evidence/bucket-02/check-2.json
python -m unittest discover -s tests -v
```

The reports omit destination paths so equal inputs and pins produce directly
equal reports. Compare the two output files and reports as bytes, not just status
text. The checkpoint records the actual real-run comparisons performed.

Wrong image, archive, executable, table, directory, payload, header or descriptor
pins fail before publication. Index ranges are bounded before reading; the pilot
caps directory reads at 1 MiB and payload reads at 16 MiB. There is no decompression
in this payload's transformation. A conflicting existing report is checked before
publishing a new overlay. These checks exercise recovery tooling and do not
replace any of the future 18 build-gate negative checks.

## Evidence and limitations

[overlay-pilot.json](../config/overlay-pilot.json) contains the PSP-specific pins.
[ARCHIVE_FORMAT.md](ARCHIVE_FORMAT.md) explains the decoding, static-loader
evidence and selected descriptor relationship. The substitution table is read
from the pinned local ELF; game bytes are not embedded in tracked tooling.

The other overlay payloads remain unrecovered in this bucket. The meanings of
the two final header address words remain provisional; neither is treated as a
verified callable entry point. Coherent disassembly is a plausibility check,
not a behavior or runtime test. Compiler selection and matching remain later
buckets.
