> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Language-mode review

Bucket 3H. This independent review invokes no compiler or linker. It inspects
the primary agent's files and existing generated objects, and separates naming
evidence, pre-target freeze review and later target results.

## Invented naming evidence

Before any C++ target compilation, the invented fixture
`bench/language_mode_naming.c` was reviewed against all fourteen signatures in
the unchanged `bench/compiler_probes.c`. Return types, argument order, pointer
const qualification, signed/unsigned bytes and scalars, and named record tags
agree. This includes `probe_08826448`'s pointer result. The artificial record
fields and bodies are unrelated to target code; record layouts are not inferred
from mangled names. `ProbeNode` need not have its target-like members to exercise
the same named pointer category.

The reviewed fixture is 2608 bytes, SHA-256
`398818f95f948bcf4e40271329a96c93dd54a89f84af0f88aea0920039e36916`.
The 3197-byte naming specification has SHA-256
`a28f748dccff244605bef825faa56acaee22f33f60fddb0158c2758949222f75`.
Its prefix/suffix rule was declared before naming compilation. It does not use
byte similarity or target scores to discover names.

The primary's two invented objects were independently rehashed and parsed:

| Mode | Object SHA-256 | Naming observation |
| --- | --- | --- |
| C | `4b661828ab5e2a2c3e3adc5d760d69ffdf7bf47de7d3254bceac2360f0abef15` | Fourteen unique bare fixture names. |
| C++ | `35fff2b05623e88398afa81e4a382a05dd813a1d9ea3ad4989348d6087bbff34` | Fourteen unique fixture names followed by the recorded `__...` signature suffixes. |

Every explicit mapping in `evidence/bucket-03h/naming-evidence.json` agrees with
the corresponding object and signature category. The report is 9360 bytes,
SHA-256 `c44419eca3863b92d50b2053b40aaae3249ae08c7ed84f5774c68e312dc3b7ba`.
Only each paired prefix is replaced to declare the expected target object's
raw symbol name. The future comparator must demand that exact frozen name;
ambiguity, fallback aliases or a missing function must make its complete
configuration unscored.

This establishes the compiler's naming convention for these fixture signatures.
It supplies no historical symbol names, target-body evidence, original source
language or SDK ownership.

## Pre-target profile review

Before any C++ target compilation, the 3847-byte draft
`config/language-modes.json`, SHA-256
`1413de4d00e9f2ce9cb3e7c0b2173e44afb932a3b6188cd9e8be34b7c215ec4a`,
and `scripts/bench_language_modes.py`, SHA-256
`aa0a97ec1ac11f08119ebbe681fb3a744b5434092a897c574da756779698ffa3`,
were reviewed and approved for status-only freeze. Read-only schema validation
also passed. The exact compiler arguments are:

```text
mwccpsp.exe -nostdinc -lang c   -c -O2 -o {fresh-c-object}   {unchanged-source}
mwccpsp.exe -nostdinc -lang c++ -c -O2 -o {fresh-cpp-object} {unchanged-source}
```

Both use the same pinned wibo/MW219 and inherited bounded execution mechanism,
compiler working directory and source pathname. Apart from separate fresh output
paths, only the language operand differs. No added exception, RTTI, inline or
optimization switch occurs. The compiler remains unmodified; no source/assembly
adapter, assembler or linker enters this experiment.

The configuration binds original source, probe manifest, selected reference,
family profile, fixture/specification/evidence and both naming objects by hash.
The runner checks those objects' actual symbols, then uses exact frozen lookup
names in a copied manifest. It neither modifies ELF records nor discovers aliases
from target results. The unchanged strict comparator requires exactly fourteen
unique complete functions, nonoverlapping intervals and no unresolved code
relocations. A rejected function prevents scoring its complete configuration.
Whole-input verification also occurs after execution and before reporting.

The original source SHA-256 remains
`d5d588c184c7c95a86bb3772e760f9251d33e3e4aabf92dfc0449c6ddc7c7a95`.
The inherited comparator SHA-256 remains
`ab6b3c441c762180f3e0269cc4ea07c4d5e3c4801136907cc93ac1495db94d5c`.
The final 3848-byte profile has SHA-256
`d3c8b6b71710f390b545fec44f1d262d66814c4cec3841dc69057166dfab0a57`.
Its sole change from the reviewed draft is the freeze-status value, recorded in
`evidence/bucket-03h/profile-freeze.json` before C++ target compilation.

Validation subsequently identified an output-integrity gap: a later compiler
invocation could replace a previous mode's already-scored object. The runner now
retains every emitted object, including failed partial outputs, and checks exact
bytes again after both modes before publishing. A detected change fails the
trial. This changes no source, flags, symbol mappings, comparator or scoring
criteria. Initial `language-run-*` artifacts are preparation evidence; final
fresh trials after this hardening are the checkpoint evidence.
The hardened runner SHA-256 is
`fa5b1c3b8a1138b5856bd525c44a609fe7d2d735713fb4da342a8ec7f203ccd2`.

## Final repeated results

Independent read-only review rehashed and reparsed all four objects under
`build/language-modes-ek4cadku` and `build/language-modes-2578h52m`. For each,
the exact frozen raw symbol mapping was applied, every complete function was
compared again with the pinned reference, and recorded object/function hashes,
metadata and comparisons agreed. All four compiler diagnostic logs are empty.

Both `evidence/bucket-03h/final-language-run-1.json` and
`evidence/bucket-03h/final-language-run-2.json` are 18386 bytes, SHA-256
`83b655d51ebb314bda5bdd1534d1a4d76c9af8c1e007d282ff8fa81df7b323af`.
They are byte-identical. Both complete configurations are reported in each;
none was rejected or partially scored.

| Mode | Object bytes | Object SHA-256, identical across repeats | Exact probes |
| --- | --- | --- | --- |
| C O2 | 4344 | `45d897dee18a5ddc6898a65d0963423dcb81ef2461d49808585c7b3a6f71473a` | 6/14 |
| C++ O2 | 4696 | `0631c7b22afb9f53a5fc057e9e158f3765ba4c0e2623f5ed7f51b96993b0585e` | 6/14 |

The C object's complete hash also equals the earlier frozen MW219 O2 control in
`evidence/bucket-03d/final-reviewed-family-run-1.json`. Both new modes retain
flags `0x10970001` and comment `MW MIPS C Compiler (3.0.0)`.
The same six intervals match in both modes: `0883C4F8`, `0883C508`, `0885691C`,
`08856A14`, `0885BBFC` and `08860C9C`. These are diagnostic probe results,
not integrated game-source matches.

Thirteen complete function bodies are byte-identical between modes after only
the frozen name association. `probe_08862434` is the sole differing body: C is
44 bytes; C++ is 48 bytes. The latter adds instruction word `0x304200ff`
(`andi v0,v0,0xff`) before the return. This is an observed mode effect, not a
change to the source or a better target match; neither body matches its target.
No bytes were removed to compare them. Whole objects differ as expected from
their distinct symbols and this code difference; identical object metadata
does not imply identical bodies.

No compiler, linker or game was executed by this reviewer. Final tooling/failure
test counts and primary integration are recorded separately at the checkpoint.

## Inference limits

The unchanged probes describe C-compatible isolated bodies with hypothesized
types. A language switch does not reconstruct class methods, overload context,
inlining, neighboring definitions or original translation units. Equal output
would make this bench non-discriminating between these invocations; differing
output would show a controlled language-mode effect. Neither outcome proves or
refutes MHP3's original language or selects its historical toolchain. Complete
game reconstruction, source integration, matching credit and runtime validation
remain separate unmet milestones.
