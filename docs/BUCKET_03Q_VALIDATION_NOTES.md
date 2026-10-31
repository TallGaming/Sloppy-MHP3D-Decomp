> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3Q independent validation

## Before-compilation review

After three unsuccessful plain-source attempts, this bucket permits exactly one
explicitly commented matching-only shape: bind volatile word references to both
existing flat fields before the first store. It retains the original field
widths, offsets, default values, member symbol and volatile access order. Binding
a reference itself adds no volatile read. This is source hypothesis 4 and matching
shape attempt 1; it is not a fourth plain attempt or a register pin.

The reviewed 1,304-byte source `bench/archive_key_field_references.cpp` has SHA-256
`20c14d1b6e848a6de1ebd3505584aa5850eaaaa34766e2378ebbdb78a4bc4c4b`.
The 1,420-byte draft protocol has SHA-256
`21c6f7c25075701d987231d6cdbbb7cb9e4588438b2c1ac7d57ee5af17670459`.

Read-only import and pure verification, with only the draft status changed in
memory, passes the unchanged inherited source/tool/reference/control validation
chain. The complete target remains 68 bytes, SHA-256
`7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57`.
No helper invokes a compiler or changes an earlier source/profile.

The fixed evidence driver allows only trials 1 and 2 and no arbitrary source,
flags or report path. Historical complete-object equality must succeed before
compiling the shape. It uses the original strict complete-function comparator,
then separately records bounded static address observations and full word
differences. Compiler errors/warnings or malformed objects receive no accepted
comparison. Partial exception outputs are retained and all emitted bytes are
rechecked at the end. An explicit `__debug__` guard prevents assertion-based
validation from disappearing under optimized Python. The helper requested
protocol/report link rejection before compilation as a small preflight safeguard.
The final pre-compilation driver implements those guards, checks the evidence
directory remains beneath the project, and separates declared/retained shapes
from actual invocation: a failed control leaves shape attempts zero and its
invocation flag false. The approved driver is 6,291 bytes, SHA-256
`80b26d9f1b0b956bffa08bb5f72131077f8a6e63341f58e6c90acdc165f58ec2`.

No new reusable production runner or unit-test module is warranted for this
fixed one-off diagnostic. The preceding 309 regression tests remain separate
from actual repeated-trial validation and from the unimplemented full-game gate.

## Actual trials and parking

Both fresh trials complete and repeat exactly. The two reports are 20,164 bytes,
SHA-256 `98d90b125a0d0a726871d0c80a3150c8c21b43d5d81c65bc7aa34b3c733412a7`.
Objects are retained in `build/archive-field-reference-e54d2drc` and
`build/archive-field-reference-ym9pnvvp`. The frozen 1,420-byte protocol has SHA-256
`e9cdf8ebfefda2a783f0af7a7e42d8fb015962707b2bc550833df81f22f37fe3`;
only its status differs from the reviewed draft. Source and driver hashes remain
unchanged.

Independent readback recomputes the four full symbol extents, object/body hashes,
complete 68-byte target comparisons and all recorded word differences: 92 aligned
word positions across both trials. No code relocation is left unapplied. All
compiler return codes are zero and all four diagnostic logs are empty. Every
comparison is NONEXACT, first differing at byte 0. No instruction or tail word is
trimmed or normalized.

| Form | Complete object bytes | Complete body bytes | Different aligned words versus full target | Static large-base sites |
| --- | ---: | ---: | ---: | --- |
| Historical control | 768 | 100 | 25 | 5 |
| Field references | 752 | 84 | 20 | 2 |

Both controls reproduce the entire historical object, SHA-256
`1d715acabd4cdec572d40c1905504881a396fa5e11296f1163533b30941d7796`.
Both shape objects repeat SHA-256
`e28c296ec53eb2c54e08eba6457e7ca7f707a3cd2854e67cd829064abffcdb7a`;
the complete 84-byte body repeats SHA-256
`6dd695b97d4b7cf3f61e246bb0b5c33fc557aa6ceed7bb00992dbc77bab37b30`.
The unchanged bounded checker is independently rerun on all four objects and
reproduces the complete stored observations. Shape base sites are at byte offsets
8 and 20. These static findings do not establish runtime equivalence or original
source representation, and the 72-byte pointer draft remains shorter.

Both reports correctly distinguish three plain attempts, one actually invoked
matching shape, four retained source hypotheses and zero matching progress.
Match/link/runtime credit remains zero; register pins and empty-assembly counts
remain zero. The preceding 309 tooling-test result is not a new gate result.

Visible parking is now audited. `config/assembly-manifest.json` is 4,007 bytes,
SHA-256 `391290964bfc33eb4713fe83460d71b885b34810f360d7db84799e48ce0da37a`.
Its sole routine is labeled PARKED, not source linked, not positively identified
as SDK/third-party code, and has no game-match credit. Reference, original
assembly, all four source pins, body extents/hashes and best-draft selection
match the actual files and reports. The attempt log retains differences and an
evidence-based revisit condition, rather than authorizing further permutations.

The 1,026-byte retained assembly source has SHA-256
`ad4d4ea2fd5873df111ad552517035fcae3d5aab4af5b4fbe54cdae42db68058`
and an explicit PARKED header. The primary independently assembled this original
assembly using the existing pinned native GNU assembler as a preservation check,
not a matching C build. Read-only helper inspection of the retained 884-byte
object, SHA-256
`f5333ac2ecf07fe7fbcc446471cb3024b6328d4a94708ca8b493884c37ea10c3`,
confirms its sole complete 68-byte function equals every reference byte. The
assembler's current identity matches the retained verification record; stdout and
stderr are empty. The helper did not assemble or execute the function. Original
assembly equality is not C-source progress or selection of a PSP build toolchain.

One process caveat is recorded explicitly: both helpers reviewed source/protocol
before compilation, and this validation helper acknowledged the exact final
guarded driver before freezing. The source-review helper's final acknowledgment
of the additional driver guards arrived during the first trial, after control
object emission and before shape emission, according to the primary's retained
chronology. Therefore this review does not claim both final-driver acknowledgments
preceded every compilation. No source/protocol/flags changed after freeze and no
code-generation result motivated a change.

Current retained-draft totals are one PARKED routine, three plain attempts, one
commented matching-shape function/attempt, zero register pins and zero empty-asm
lines. All four source hypotheses and repeated failure evidence remain visible.
The 72-byte plain pointer draft remains best; no additional source form was tried.
Full-game matching, linked source, runtime validation and a toolchain lock remain
unachieved.
