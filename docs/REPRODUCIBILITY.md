# Reproducing the public diagnostics

The public entry point is [tools/repro](../tools/repro/README.md). Its comparison
utility reads a separately compiled object and, optionally, your own exact
decrypted PSP reference. It requires complete function extents and compares
every byte. It does not execute a compiler or PSP code, embed original target
bytes, or grant game-match credit.

The [bench sources](../bench/) are authored source hypotheses and invented
fixtures. The five game-related drafts linked from HELP_WANTED are unchanged
from their reported diagnostic runs. Their hashes allow another researcher to
establish that they tested the same source.

Run the Python tooling tests with `python -m unittest discover -s tests -v`.
These use invented/temp/mock data. Some native-staging checks are host-specific;
the clean-export validation report records actual passes and skips. None of
these tests is the future 18-negative-test full-game gate.

## Historical records

Most JSON files in `config/` are frozen records from earlier local experiments.
They include hashes, original environment paths and references to private
`evidence/`, `build/`, `reference/` and `toolchains/` material. They document what
was tested; they are not a ready-to-run public game build. Personal path values
have been replaced where necessary. Do not treat a missing local artifact as a
passing check or bypass its expected hash.

The original experiment controllers and raw reports lived in ignored local
evidence directories. They are not silently reconstructed or claimed runnable
by this publication. The minimal public repro avoids that private graph and
documents the fixed baseline commands independently.

When proposing another global toolchain configuration, report the tool version
and hash, complete invocation, source hash, object hash and complete function
extent. Separate compiler output, assembler transformations and linker/runtime
metadata. Do not mix favorable flags between individual functions.

The native port, runtime validation, complete function inventory, original
toolchain lock and linked byte-identical game build remain future work.
