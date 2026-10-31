> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Archive field-reference shape review — Bucket 3Q

The three declared plain-source forms were exhausted in Bucket 3P. This bucket
permits one explicitly commented matching-only shape: bind references to the
two existing volatile fields before stores and use those aliases. It is source
hypothesis four, matching-shape attempt one, not another plain attempt. If its
complete comparison remains NONEXACT, retain the drafts and park the routine
visibly; no second shape is included. The reviewer invokes no compiler.

## Exact source review before compilation

`bench/archive_key_field_references.cpp` is 1,304 bytes, SHA-256
`20c14d1b6e848a6de1ebd3505584aa5850eaaaa34766e2378ebbdb78a4bc4c4b`.
The source preserves the original flat partial class: prefix `0x2F53C`, lower
then upper volatile unsigned word fields at `0x2F53C/0x2F540`, nonvirtual member
signature and partial extent `0x2F544`. Class identity, complete object layout
and volatility remain hypotheses, as in the prior draft.

Independent body-token comparison against the preserved flat draft reconstructs
the new body exactly by adding
`volatile u32& lower = key_lower; volatile u32& upper = key_upper;` and replacing
the existing field uses with their aliases. No other body token changes.
Binding these references takes existing subobject addresses without reading
either volatile value. Subsequent accesses retain the same upper-then-lower
stores, optional lower-default store from the masked seed local, upper reload
and optional upper-default store. Defaults remain `0x7F8D/0x2345`; widths,
unsigned extraction, conditions and access ordering remain unchanged.
This reasoning assumes a valid live receiver, and introduces no null handling.

The purpose comment explicitly labels the shape and explains the code-generation
question without claiming original-source recovery or a proven backend cause.
There is no assembly, register pin, empty-asm barrier, grouping change, helper,
qualifier revision or added alternative. `HANDOFF.md` records one function with
a commented matching shape in a retained unintegrated draft, zero pins and zero
empty-asm lines. Those counts are distinct from source integration, match credit
and whether the shape was actually invoked in a particular trial.

## Protocol pre-review and final driver readback

The reviewed draft `evidence/bucket-03q/protocol.json` is 1,420 bytes, SHA-256
`21c6f7c25075701d987231d6cdbbb7cb9e4588438b2c1ac7d57ee5af17670459`.
The final reviewed fixed evidence driver is 6,291 bytes, SHA-256
`80b26d9f1b0b956bffa08bb5f72131077f8a6e63341f58e6c90acdc165f58ec2`.
It accepts only trial identifiers 1 and 2, requires protocol freeze before
compilation and reuses the unchanged 3P input verifier, strict complete-function
comparator and fail-closed address checker. Expected symbol remains
`initialize_key__17ArchiveKeyContextFUi`; flags remain
`-nostdinc -lang c++ -c -O2` under the existing unmodified MW219/runner profile.

The complete target remains [0x0886233C, 0x08862380), 68 bytes, SHA-256
`7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57`.
The original flat source remains unchanged. Before invoking the shape, each
trial must reproduce its historical complete 768-byte object, SHA-256
`1d715acabd4cdec572d40c1905504881a396fa5e11296f1163533b30941d7796`.
Failure of that control stops before the shape. Word differences retain all
bytes and length differences; no normalization or partial-match acceptance
is introduced. Unsupported address analysis retains no numeric conclusion.

Two independent pre-compilation findings were corrected before output:

- Report bookkeeping now separates four retained source hypotheses from actual
  shape invocation. It begins with zero matching-shape attempts and sets the
  invocation flag/count only immediately before calling the compiler helper
  for that shape. A failed control cannot be reported as a tested NONEXACT
  shape or justify parking on that basis.
- Evidence/protocol/report paths are checked for links and the resolved
  evidence directory must remain beneath the project before reading inputs or
  creating build output. Existing reports cannot be overwritten.

The driver refuses Python assertion optimization explicitly, so its assertions
cannot silently disappear under `-O`. It retains partial failure outputs without
accepting them, rechecks all inherited input/profile pins and verifies emitted
objects against their captured bytes before report publication. Source/protocol
approval preceded the declared status-only freeze. Final corrected-driver
acknowledgment timing is qualified below; no output conclusion or shape-output
inspection informed that acknowledgment.

## Freeze and review chronology

The frozen protocol is 1,420 bytes, SHA-256
`e9cdf8ebfefda2a783f0af7a7e42d8fb015962707b2bc550833df81f22f37fe3`.
Replacing only its status reconstructs the exact reviewed draft hash above.
The final guard changes were already present in the recorded 6,291-byte driver
before freeze at `2026-10-31T05:41:19.294824Z`; its hash still equals the reviewed
`80b26d9f...` value. Source, flags, target and driver did not change after freeze.

There is a review-timing qualification. The primary reports that this helper's
final driver acknowledgment arrived during the first trial tool cell. Retained
file timestamps are consistent with that sequence: first control object
`05:41:23.569085Z`, this review's initial saved note `05:41:23.588085Z`, and
first shape object `05:41:23.790111Z`. These timestamps establish artifact order,
not compiler invocation boundaries or when a message was read. Source/protocol
approval preceded scoring, and the other helper's final approval preceded the
trial; this helper's final guard readback/acknowledgment must not be described
as certainly preceding first control emission. The freeze record's broad
`both_helpers_precompile_approved` flag should not conceal that qualification.
The reviewer had not inspected new trial outputs when acknowledging the guards.

## Independent repeated-output audit

Both `field-reference-run-1.json` and `field-reference-run-2.json` under
`evidence/bucket-03q` are identical: 20,164 bytes, SHA-256
`98d90b125a0d0a726871d0c80a3150c8c21b43d5d81c65bc7aa34b3c733412a7`.
The reviewer rehashed/reparsed all four objects in
`build/archive-field-reference-e54d2drc` and
`build/archive-field-reference-ym9pnvvp`, reproduced the complete strict target
comparisons and every raw-word difference, and checked all four empty logs.
Both historical controls reproduce the expected whole object. Both shape
objects are identical, 752 bytes, SHA-256
`e28c296ec53eb2c54e08eba6457e7ca7f707a3cd2854e67cd829064abffcdb7a`.

| Observation | Historical flat control | Field-reference shape |
| --- | --- | --- |
| Complete function size | 100 bytes | 84 bytes |
| Complete target size | 68 bytes | 68 bytes |
| Strict result | NONEXACT | NONEXACT |
| First difference | Byte 0 | Byte 0 |
| Static large-base ADDU sites | 5 | 2 |
| Ordered access paths | All four | All four |

The shape's complete-function SHA-256 is
`6dd695b97d4b7cf3f61e246bb0b5c33fc557aa6ceed7bb00992dbc77bab37b30`.
Its two bases are full addresses for lower and upper respectively: two
`LUI 2 / ORI / ADDU` triples, with ADDU sites at offsets `0x08/0x14`.
All later 32-bit accesses use zero displacement from those two registers.
It preserves upper-then-lower stores, the low local condition, upper reload,
defaults and four paths. Two forward conditional branches and the final
JR all have NOP delay slots. No call or stack frame is introduced.

The original target instead shares a high-part receiver base with signed
displacements. The shape reduces repeated bases relative to the 100-byte flat
draft but adds 12 bytes relative to the earlier 72-byte pointer draft. It does
not recover the target's address construction, seed-operation order or register
assignments. Twenty positional words differ or are extra against the complete
target; that raw count is not a count of semantically incorrect instructions.
The matching-only source shape was actually invoked once as a hypothesis and
repeated in both trials, preserving three plain attempts and one shape attempt.

## Visible parking audit

`config/assembly-manifest.json` labels this exact 68-byte interval **PARKED**,
keeps original-name/ownership uncertainty explicit, marks source unlinked and
game-match credit false, and pins all four retained drafts. The selected best
draft remains `bench/archive_key_pointer.cpp`, 72 bytes and NONEXACT; the 84-byte
shape does not replace it. All manifest source and assembly pins independently
match their files. `docs/ARCHIVE_KEY_PARKING.md` records the attempts, failure,
best draft and evidence-based revisit conditions without reopening expression
or per-function flag searches.

The complete original assembly is retained at
`asm/nonmatching/archive_key_initialize.s`, 1,026 bytes, SHA-256
`ad4d4ea2fd5873df111ad552517035fcae3d5aab4af5b4fbe54cdae42db68058`.
Read-only reinspection of the already generated assembly-verification object
reproduces its observation and exact 68-byte function hash, equal to the full
locked reference interval. The diagnostic GNU assembler's object flags and
metadata are distinct from the game ELF; this proves retained instruction
bytes only, not a linked rebuild or selection of that assembler for the game.
The reviewer did not reassemble it. Assembly, reference and evidence paths are
git-ignored, keeping original bytes outside version control.

Totals are one parked routine, three plain source attempts, one matching-shape
attempt, four retained hypotheses, one retained function with a commented
shape, zero register pins and zero empty-asm lines. No additional shape was
tried, no SDK/library reassignment was made, and no game execution, linked
source, full gate, negative-gate suite or matching credit follows. The parked
record is the explicit stopping point for this routine until independent new
evidence justifies a separately documented revisit.
