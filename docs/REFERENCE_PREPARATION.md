> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Reproduce the accepted reference

Bucket 1, 2026-10-30. These tools prepare and inventory the accepted PSP
ULJM05800 v1.02 reference. They do not rebuild the game, extract overlay payloads,
select a compiler or execute gameplay.

## Normal commands

Run from `<project-root>`:

```powershell
$gameIso = '<game-image-directory>\Monster Hunter Portable 3rd (Japan) (v1.02)\Monster Hunter Portable 3rd (Japan) (v1.02).iso'
python scripts/prepare_reference.py --iso $gameIso
python scripts/map_executable.py
```

The first command verifies the active user-selected lock, complete ISO identity,
game metadata and encrypted executable. It checks the helper's pinned hash, runs
decryption in a fresh staging directory, then verifies both outputs and the ELF
structure before publishing. Existing correct files are preserved, but decryption
still runs again; existing different files cause failure instead of replacement.

Default products:

- `reference/uljm05800-v102/EBOOT.BIN` and `EBOOT.ELF` (local ignored game bytes).
- `evidence/bucket-01/reference-preparation.json` (identities and scope).
- `evidence/bucket-01/executable-map-v1.json` (deterministic metadata map).

Expected successful summaries are `REFERENCE_PREPARATION_PASS: ULJM05800 v1.02`
and `EXECUTABLE MAP WRITTEN` or `EXECUTABLE MAP UNCHANGED`. These are scoped tool
results; neither is a game-build gate result. Any failure returns nonzero.

Both tools preserve an existing identical report and reject a conflicting report.
Use a fresh `--report` or `--out` path when recording a changed implementation.
The image is always opened read-only; synthetic fixtures are used for mutations.

## Fresh-output repeatability

The following commands were run successfully on the accepted image:

```powershell
python scripts/prepare_reference.py --iso $gameIso --out-dir reference/bucket-01/final-run-1 --report evidence/bucket-01/final-preparation-run-1.json
python scripts/prepare_reference.py --iso $gameIso --out-dir reference/bucket-01/final-run-2 --report evidence/bucket-01/final-preparation-run-2.json
python scripts/map_executable.py --elf reference/bucket-01/final-run-1/EBOOT.ELF --out evidence/bucket-01/final-map-run-1.json
python scripts/map_executable.py --elf reference/bucket-01/final-run-2/EBOOT.ELF --out evidence/bucket-01/final-map-run-2.json
python -m unittest discover -s tests -v
```

The two encrypted executables, two decrypted executables, preparation reports
and map reports were directly byte-compared and found identical. See
`evidence/bucket-01/verification-summary.json` and the checkpoint report for hashes.
All 49 tooling tests passed; their log is `evidence/bucket-01/tooling-tests.log`.

## Prerequisites and limits

- Python 3.10 or newer; the Python code uses only the standard library.
- On Windows, the already prepared WSL Ubuntu environment and Linux helper at
  `toolchains/pspdecrypt/pspdecrypt`. Native Linux can run the helper directly,
  but that invocation was not independently exercised in this bucket.
- `config/reference.json` pins the selected image and output identities.
- `config/helper-tools.json` pins the locally built helper's SHA-256 and source
  commit. The helper executable remains ignored and is not distributed here.
- The pinned helper source is John-K/pspdecrypt at commit
  `c156627db7634d395c380c0a9589130f603307fc`, built locally with GCC/G++ and the
  OpenSSL/zlib development dependencies described in `docs/TOOLCHAIN.md`.

This command does not install WSL, download/build tools or promise a fresh-machine
installation. The helper binary was built in the existing environment; rebuilding
on another host can change its binary hash. Any helper replacement requires a
reviewed pin update and must still produce the independently pinned ELF bytes.
The exact game compiler and flags remain unselected.
