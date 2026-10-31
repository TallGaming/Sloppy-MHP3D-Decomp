# Standalone compiler reproduction

This directory provides an offline inspector for an independently compiled,
single-function object. It never launches a compiler, game or emulator. Game
images, decrypted executables, target bytes, SDKs and compiler binaries are not
included. Supply your own tools and, optionally, your own reference executable.
The repository's license has not been selected; do not infer a license for any
third-party compiler or dependency from this help pack.

From the repository root, with Python 3.10 or newer:

```sh
python tools/repro/compare_function.py --object candidate.o --case key-advance
```

Without a reference it reports the complete declared function's size and SHA-256,
and makes no matching decision. To compare every byte and the complete length:

```sh
python tools/repro/compare_function.py --object candidate.o --case key-advance \
  --reference /path/to/your/decrypted/EBOOT.ELF
```

Use `--case initializer` for the separate parked initializer. Only the exact
2,247,320-byte decrypted PSP Japanese v1.02 reference is accepted (SHA-256
`755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950`).
The reviewed intervals are 68 bytes at `0x0886233C` and 140 bytes at `0x08862700`.
The tool does not decrypt an image or print original target bytes. JSON contains
sizes, hashes, the first differing byte offset and an isolated exactness flag.

Selection requires exactly one positive, aligned, strong global function extent
in executable file-backed code. Extra/zero/weak/ambiguous functions, malformed
metadata and all nonzero code relocations are rejected. No relocation is applied,
no bytes are trimmed or masked, and no best-looking function or interval is chosen.
Unapplied non-code relocation counts are reported separately.

An exact diagnostic body would not prove source participation, historical compiler
identity or a credited game match. The clean complete-game build and eighteen
negative gate checks have not been implemented. Synthetic public tests are tooling
checks; they do not replace that gate.

## Fixed diagnostic commands

The following are the existing investigation profiles, not a selected historical
game build. Keep them unchanged when reproducing these particular diagnostics.
Do not tune flags for individual functions. All tool paths below are paths to
your own existing installations; no tool download or installation is performed.

| Producer | Frontend/common flags, then optimization | Assembly stage |
| --- | --- | --- |
| MW PSP 3.0.1 build 219 | `-nostdinc -lang c++ -c -O2` | Compiler's existing pipeline |
| Sony SNC 1.2.7503.0, `.cpp` input | `-c -G0 -O2` | Compiler's existing pipeline |
| PSP GCC 1.7.1, bundled `cc1plus` 3.3.3 | `-quiet -nostdinc -G 0 -march=allegrex -mtune=allegrex -mel -mabi=eabi -O2` | `-EL -march=allegrex -mabi=eabi -G0 -O0` |
| MinPSP GCC 4.3.5, bundled `cc1plus` | Same frontend flags above | Same assembly flags plus existing `-msingle-float` |

The GNU profiles use the reviewed modern GNU MIPS assembler with Allegrex support;
they are diagnostic pipelines, not reconstructed historical SDK driver builds.
GCC 4.3.5 also requires its separate legacy runtime libraries. The assembler ABI
option above was validated for that frontend and applies uniformly to its profile.

For example, on Linux/WSL, provide absolute `WIBO` and `MWCCPSP` paths:

```sh
repro_root="$PWD"
(cd "$(dirname "$MWCCPSP")" &&
  "$WIBO" "$MWCCPSP" -nostdinc -lang c++ -c -O2 \
    -o "$repro_root/candidate.o" "$repro_root/bench/archive_key_advance.cpp")
python tools/repro/compare_function.py --object candidate.o --case key-advance
```

For SNC, use the same existing wibo runner, the `PSPSNC` compiler path, flags
`-c -G0 -O2`, and a `.cpp` source. Retain its required support files beside the
compiler. Replace `archive_key_advance.cpp` with `archive_key_initializer.cpp` and
select `initializer` only when reproducing that separate first hypothesis.

The old GCC frontend cannot reliably stat some Windows-mounted inode numbers.
Its existing pipeline stages a byte-identical source copy under native `/tmp`,
preserving the source basename and using `probe.s`. For GCC 1.7.1:

```sh
repro_root="$PWD"
repro_scratch=$(mktemp -d /tmp/mhp3rd-repro.XXXXXX)
cp "$repro_root/bench/archive_key_advance.cpp" "$repro_scratch/archive_key_advance.cpp"
(cd "$repro_scratch" &&
  "$CC1PLUS" -quiet -nostdinc -G 0 -march=allegrex -mtune=allegrex \
    -mel -mabi=eabi -O2 -o probe.s archive_key_advance.cpp &&
  "$MIPS_AS" -EL -march=allegrex -mabi=eabi -G0 -O0 \
    -o "$repro_root/candidate.o" probe.s)
```

Keep the emitted assembly and complete object when reporting differences. For
4.3.5, use its own `CC1PLUS`, the previously described private runtime environment
(`LC_ALL=C` and its legacy-library directory), and add `-msingle-float` to that
profile's assembler invocation. Do not substitute similarly named modern runtime
libraries. No compiler or object execution is part of the inspection tool.

## Public tests

```sh
python -m unittest tests.test_public_repro -v
```

These tests build invented ELF bytes in temporary directories and test metadata,
complete comparisons and rejection paths. They need no private evidence, game
data, compiler, SDK, emulator or network service.
