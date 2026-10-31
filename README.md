# Monster Hunter Portable 3rd matching decompilation research

We are working toward readable source that rebuilds **Monster Hunter Portable
3rd, Japanese PSP release ULJM05800 v1.02**, byte for byte. We are currently
identifying the original build pipeline and asking other PSP decompilers for help.

Project repository: [TallGaming/Sloppy-MHP3D-Decomp](https://github.com/TallGaming/Sloppy-MHP3D-Decomp).

**Start with [HELP_WANTED](docs/HELP_WANTED.md)** for the compiler problem,
reviewed function ranges, source drafts, exact diagnostic results and questions.
[CURRENT_STATUS](docs/CURRENT_STATUS.md) separates verified results from open work.

The historical toolchain is **not locked**. There are **zero credited matched
or source-linked game functions**, and the full-game build gate and its 18
negative tests have not been implemented. One initializer is visibly parked;
a second routine has one readable, nonmatching diagnostic draft. Equal function
length or a compiler-banner hit does not count as a match.

This repository contains authored research, source hypotheses, invented fixtures
and Python tooling. Game images, extracted assets/code dumps, save data,
proprietary compilers/SDKs, keys and private execution evidence are excluded.
Use your own matching game image and separately obtained development tools.

## Reproduce the public tooling

Python 3.11 or newer is recommended. The tests use invented inputs and mocks;
they do not need a game image or proprietary compiler:

```sh
python -m unittest discover -s tests -v
```

[The minimal diagnostic guide](tools/repro/README.md) provides the fixed compiler
commands and a pure offline object/reference comparison tool. It never executes
PSP code and does not publish any original reference bytes.

[REPRODUCIBILITY](docs/REPRODUCIBILITY.md) explains the difference between that
public repro and the historical, machine-specific investigation records in
`config/`. Those records are not a complete build or a portable SDK installation.

## Working rules

- Start with natural, readable C/C++, with a purpose header and useful comments.
- Never tune compiler flags for individual functions. Investigate original
  project-wide toolchain settings explicitly before locking them.
- After about three plain attempts or 30 minutes, document/count any necessary
  matching tricks; visibly park a function if it remains unmatched.
- Keep Sony SDK and positively identified third-party library code labeled
  assembly. Only reconstruct the game's own code.
- Credit a rewrite only after a clean byte-identical build and the required
  checks prove source participation and reject stale objects/assembly fallback.

A native Windows/Linux port is a later objective, after all game code matches.
No playable native port is included in this snapshot. See [CONTRIBUTING](CONTRIBUTING.md)
before submitting findings or patches.

For what follows compiler identification, read [the matching roadmap](docs/AFTER_TOOLCHAIN.md).
For code contributions, follow [the matching guide](docs/MATCHING_GUIDE.md) and
[task template](docs/MATCHING_TASK_TEMPLATE.md).

## Documentation

[Documentation index](docs/INDEX.md) · [Current handoff](HANDOFF.md) ·
[Historical research](docs/history/README_2026-10-31.md) ·
[Publication contents](docs/publication/README.md) · [License status](LICENSE_STATUS.md)

[Publication checks](docs/publication/PUBLICATION_CHECK.md) record the clean-export
test results and remaining publication decisions.

Earlier checkpoint pages are preserved as dated research records. Their local
evidence paths and earlier privacy decisions are historical; the current public
status takes precedence. The local decomp.me instance described there is an
operator workbench, not a hosted public demo.
