# Help wanted: original PSP build pipeline

We need source-backed help identifying the historical build pipeline for
Monster Hunter Portable 3rd, Japanese PSP **ULJM05800 v1.02**, and understanding
two small nonmatching source drafts. [Current status](CURRENT_STATUS.md) records
what was actually tested. There are zero credited matches, no linked reconstructed
source, no passing full-game gate and no historical toolchain lock.

Please focus on documented compiler/linker/ABI evidence and readable source
context. We will not retune flags separately for a function. Original game bytes,
SDK/compiler binaries, keys and assets are not included or requested.

## Evidence and limits

The linked ELF reports `MW MIPS C Compiler (2.4.1.01)` in `.comment`. Relocatable
objects from the tested MW219 compiler report a different internal string.
Different pipeline stages can contribute metadata; the linked string does not
prove the exact frontend executable or every function's producer. A sampled C++
initialization unit has GNU-compatible conventions, with linked-runtime/shared-ABI
explanations still possible. Neither observation locks the original build.

Two fresh trials of four existing fixed C++/O2 pipelines reproduced all complete
invented producer controls before the new advance diagnostic. All candidate
bodies remained NONEXACT. Results and raw body identities below summarize local
records; private objects/logs/target disassembly are not public evidence downloads.

| Advance pipeline | Function size | First differing byte | Function SHA256 |
| --- | ---: | ---: | --- |
| MW219 | 124 | 5 | 9294f268f6cf5032c15fe750f97d64417e8a7d50cd4551891405b3edddc01b64 |
| PSP GCC 3.3.3, package 1.7.1 | 140 | 0 | 23b0eb7215e3f61d1f18858ee583125e4bab8826790474f4c8857dc05bafb164 |
| SNC 1.2.7503.0 | 116 | 2 | e33c245c03fb3931a0807fba13a67eee8d47a72809e55b61d4c45b069750d39f |
| PSP GCC 4.3.5 | 100 | 10 | cc5dce400b7d381e4eb4e7c0d4b1fbe2b007e159a3aa565d8a58a40336c2ef06 |

The original advance is [0x08862700, 0x0886278C), 140 bytes, SHA256
`0ff874a4e619b6a6202257c13125a9ed1ed5dab4c45cbc0242eb9ad5f0a3261f`.
Its [plain draft](../bench/archive_key_advance.cpp) is 1,156 bytes, SHA256
`4bcd148007c42aa4a7e97fa01c99cd90ac9bafe986445a46ec91d72014e19f93`.
Known unsigned modular arithmetic and offsets are represented naturally;
receiver class, translation-unit context and memory qualifiers remain hypotheses.
This different routine has consumed one plain source hypothesis, with no trick.

## Parked initializer

Original interval [0x0886233C, 0x08862380) is 68 bytes, SHA256
`7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57`.
It remains visibly parked after the allowed plain budget and one commented shape.

| Public diagnostic draft | Category | MW219 C++/O2 complete body |
| --- | --- | ---: |
| [archive_key_initializer.cpp](../bench/archive_key_initializer.cpp) | Plain 1, flat fields | 100, NONEXACT |
| [archive_key_grouped.cpp](../bench/archive_key_grouped.cpp) | Plain 2, grouped state | 100, NONEXACT |
| [archive_key_pointer.cpp](../bench/archive_key_pointer.cpp) | Plain 3, named state pointer | 72, NONEXACT |
| [archive_key_field_references.cpp](../bench/archive_key_field_references.cpp) | One commented matching shape | 84, NONEXACT |

The best retained source is the 1,391-byte pointer draft, SHA256
`f2e6439d81eace695d1027900503a3d3d368f3c6b506b6a5af203dbfe56be373`.
Other retained source identities are:

| Source | Bytes | SHA256 |
| --- | ---: | --- |
| bench/archive_key_initializer.cpp | 1806 | 6c4be341bcc3f113b56ccf7494a7b624a550b52f89c9c827eacbbce56e1f71d3 |
| bench/archive_key_grouped.cpp | 1377 | e1e8671b6a465df6b539a7d6d27f334b64865bc1ed15e6edf34223bdef865cbd |
| bench/archive_key_field_references.cpp | 1304 | 20c14d1b6e848a6de1ebd3505584aa5850eaaaa34766e2378ebbdb78a4bc4c4b |

A separately reviewed GNU C++/O2 diagnostic produced 64-byte flat/pointer bodies,
also NONEXACT. Size proximity does not establish correct code generation.
No expression permutation or additional source form is authorized just by this
help request; independent context could justify a later reviewed revisit.

## Questions that could move this forward

1. Which documented PSP compiler/linker release or construction stage emits the
   linked `2.4.1.01` string? Can you cite vendor documentation, a public source
   rule or an invented-object/link experiment distinguishing retained input
   comments from linker-written metadata?
2. Do primary sources establish how the relevant PSP C++ ABIs, static initializer
   conventions and mixed-toolchain runtime linkage relate? Separate ABI
   compatibility from exclusive compiler/version attribution.
3. Can readable class/subobject/translation-unit context explain retained versus
   repeated large field addresses, access order and snapshot results under one
   global configuration? Qualifier claims need access semantics; a missing reload
   alone does not prove the original declaration.
4. Are there documented, provenance-bearing SDK/library signatures applicable to
   these units? A library-like name, imported NID or runtime string is not enough
   to classify unknown implementation code or exclude it from game-source work.

Useful contributions include a precise public source citation, an explanation
with uncertainty, or a minimal invented reproducer with complete tool identities,
commands, symbols/relocations and repeat outputs. Do not upload a game image or
proprietary tool distribution in an issue. Use the compiler-help issue template.

## Public leads, with limits

- [Pinned MHP2G pipeline](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/configure.py)
  documents a same-series compiler/assembly/fixup/link chain. Its target and source
  choices do not transfer automatically to MHP3.
- [MHP2G ELF conversion](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/tools/fixup_elf.py)
  shows why intermediate layout/relocations need full stage provenance, rather
  than an unexplained patch to reference bytes.
- [GNU MIPS ELF definitions](https://github.com/pspdev/binutils-gdb/blob/febbfd5154af3d28d5e0f39fd0b9b6895f78c25a/include/elf/mips.h)
  are a decoding reference, not a translation of raw bits into original flags.
- [DiE's pinned ELF MWCC rule](https://github.com/horsicq/Detect-It-Easy/blob/adc0617abd4d35e7449c767f62cf6ae276c67762/db/ELF/compiler_MWCC.4.sg)
  searches `.comment` for the banner and sets a language label. Source review is
  complete for that rule; no scanner ran. It adds no independent MIPS-code
  fingerprint, and its C label does not prove source language. Wider database
  coverage was not established by the interrupted review.

These tools/projects are references, not endorsements of flags, architecture or
claims that this repository has a matching build or playable port.
