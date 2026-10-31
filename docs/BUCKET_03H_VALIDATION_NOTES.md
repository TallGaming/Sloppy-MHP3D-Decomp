> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3H independent validation

2026-10-30. The validation helper reviewed the naming evidence and complete
profile before C++ target scoring, added invented controls, and audited both
fresh final trials. **Both modes produce six exact diagnostic probes; thirteen
of fourteen function byte sequences are unchanged between C and C++.** These
results neither identify the original language nor select a historical build.

## Review and freeze before target results

The invented naming source mirrors each frozen probe's argument and result
categories: signed/unsigned byte pointers, constness, ordered scalar/pointer
arguments and named record-pointer types. Its record fields and function bodies
are artificial. No target bytes or reconstructed function bodies are used to
discover C++ spelling. The helper independently read the naming source,
signature-pair specification, both naming objects and their empty diagnostic logs.

The C naming object contains exactly fourteen unique undecorated function names;
the C++ object contains exactly fourteen unique observed decorated names. Each
observed suffix is transferred only to its paired canonical probe name. Named
record types retain their source names for this naming test; field layout is
not inferred from the spelling. The pinned naming artifacts are:

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `bench/language_mode_naming.c` | 2608 | `398818f95f948bcf4e40271329a96c93dd54a89f84af0f88aea0920039e36916` |
| `config/language-naming-fixture.json` | 3197 | `a28f748dccff244605bef825faa56acaee22f33f60fddb0158c2758949222f75` |
| C naming object | 4200 | `4b661828ab5e2a2c3e3adc5d760d69ffdf7bf47de7d3254bceac2360f0abef15` |
| C++ naming object | 4552 | `35fff2b05623e88398afa81e4a382a05dd813a1d9ea3ad4989348d6087bbff34` |
| `evidence/bucket-03h/naming-evidence.json` | 9360 | `c44419eca3863b92d50b2053b40aaae3249ae08c7ed84f5774c68e312dc3b7ba` |

The reviewed target-profile draft was 3847 bytes, SHA-256
`1413de4d00e9f2ce9cb3e7c0b2173e44afb932a3b6188cd9e8be34b7c215ec4a`.
The frozen `config/language-modes.json` is 3848 bytes, SHA-256
`d3c8b6b71710f390b545fec44f1d262d66814c4cec3841dc69057166dfab0a57`.
Reversing only the status-value change reproduces the reviewed draft hash.
`evidence/bucket-03h/profile-freeze.json` records both pre-score approvals.
The historical no-C++-scores declaration records that freeze, not current results.

The sole compiler is unmodified Metrowerks 219. Both configurations use the
unchanged fourteen-probe source at O2; only the `-lang` operand changes. Both
original source alternatives remain unused and frozen. The alias adapter derives
a manifest for the unchanged strict comparator, then restores canonical names
and records each exact `object_symbol`. It does not rewrite object bytes,
demangle heuristically, slice functions or relax relocation checks. Production
validation binds all fourteen associations to the reviewed naming pairs and
observed symbols; an arbitrary same-set permutation is rejected.

## Controls and one resolved review finding

The 17 tests in `tests/test_language_modes.py` use invented ELF bytes and mocked
compiler calls. They cover exact key/value bijections, absent/unexpected/duplicate
symbols, canonical reports, preservation of complete object identities,
wrong associations, complete function lengths, changed bytes, unsupported code
REL/RELA, malformed/undefined/overlapping/nonexecutable symbols and target pins.
The orchestration fixture uses all fourteen invented functions, not a reduced
stand-in for the complete-configuration requirement.

Runner controls cover fresh paths, repeatable reports, fixed commands and
signature bindings, warnings/nonzero exits/timeouts/missing or invalid objects,
and missing functions. Any invalid mode publishes no comparisons or score;
an independently complete other mode remains reportable. Cross-mode comparison
is unavailable if either configuration is rejected. Input/profile mutations
before or after work fail globally, and aliases/conflicting reports preserve
existing files.

One negative initially failed: the second compiler call could alter the first
mode's saved object after its score had been captured. The primary added a
post-pair exact-byte check for every emitted object, including partial objects
from failed compilations. Both variants of that control now invalidate the
outer report. The final trials were rerun fresh after this integrity fix.
No source, command flags, alias map, scoring policy or frozen configuration
changed in response to scores. Earlier trial reports remain local evidence.

The helper independently ran all 17 new tests and the full suite:
**226 passed, zero skips**. The primary's complete retained suite log is
`evidence/bucket-03h/tooling-tests.log`. These tooling controls are not the
future full-game gate's required 18 negative checks and confer no game match.

The helper also read the primary's real controls in
`evidence/bucket-03h/verification-summary.json`: report/input aliasing and a
swapped canonical mapping each return exit one, before a new build directory
or successful report. The alias control preserves the input. These commands
were performed by the primary, not independently rerun by this helper.

## Final repeat and byte audit

Both final reports `evidence/bucket-03h/final-language-run-{1,2}.json` are
byte-identical: 18,386 bytes, SHA-256
`83b655d51ebb314bda5bdd1534d1a4d76c9af8c1e007d282ff8fa81df7b323af`.
They retain every declared outcome and record zero game-match progress.
The fresh artifact directories are:

- `build/language-modes-ek4cadku`
- `build/language-modes-2578h52m`

Each directory contains two complete objects and two empty diagnostic logs.
Both C objects are 4344 bytes, SHA-256
`45d897dee18a5ddc6898a65d0963423dcb81ef2461d49808585c7b3a6f71473a`.
Both C++ objects are 4696 bytes, SHA-256
`0631c7b22afb9f53a5fc057e9e158f3765ba4c0e2623f5ed7f51b96993b0585e`.
Larger object size alone is not a change in function instructions.

The helper independently reparsed all four objects and recomputed all **56
complete-symbol target comparisons**, including sizes, hashes, equality and
first differing byte, plus **28 C-versus-C++ comparisons**. Each object contains
exactly the fourteen declared function symbols. Both modes reproduce six exact
tiny controls. The C object and all fourteen target comparisons also reproduce
the accepted Bucket 3D MW219/O2 control exactly after removing the new report's
explicit alias field.

The only changed function is `probe_08862434`: C emits 44 bytes, C++ 48, against
the 72-byte target; both fail complete equality. The other thirteen complete
function sequences are equal across modes. None of the six larger probes
becomes exact. The two networking leaves remain unmatched and unclassified.
The helper verified **194 declared local pin records and 11 native dependency
records** against current bytes. Duplicate declarations count as records, not
distinct files. This includes the naming objects, original source/manifest,
reference ELF and inherited tool/support configuration. No game ISO was opened
or modified for this audit.

## Final implementation identities and limits

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `scripts/bench_language_modes.py` | 13999 | `fa5b1c3b8a1138b5856bd525c44a609fe7d2d735713fb4da342a8ec7f203ccd2` |
| `tests/test_language_modes.py` | 24198 | `f5cd391a86b7319f385af59a9d5df135628b996f62ce1d6afb7bd51485dddfbe` |

The experiment concerns isolated C-compatible bodies under one reviewed tool
and profile. It cannot confirm or refute original C++ use, class/translation-unit
context, inlining, library ownership or historical flags. No original game
code was linked or executed, no new overlay or target function was selected,
and no compiler/library/runtime candidate was adopted. The toolchain stays
unlocked. Match credit, source-linked game functions, parked functions and
counted matching tricks stay zero; the full-game gate and native port remain
deferred. Stop at the Bucket 3H checkpoint.
