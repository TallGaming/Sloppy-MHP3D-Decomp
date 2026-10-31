> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Parked archive-key initializer

Status: **PARKED**. Label: `archive_key_initialize` (analysis name).
Reference: original PSP ULJM05800 v1.02 EBOOT.ELF,
`0x0886233C..0x08862380`, complete 68-byte SHA-256
`7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57`.

This is a visible diagnostic parking decision, not integration into a build or
an SDK/library reassignment. Original assembly is retained locally at
`asm/nonmatching/archive_key_initialize.s`; the machine-readable record is
`config/assembly-manifest.json`. Assembly from the reference grants no source
coverage or matching credit.

| Retained draft | Category | Result under unchanged MW219/C++/O2 |
| --- | --- | --- |
| `bench/archive_key_initializer.cpp` | Plain attempt 1, original flat fields | 100 bytes, NONEXACT |
| `bench/archive_key_grouped.cpp` | Plain attempt 2, grouped key state | Identical 100 bytes, NONEXACT |
| `bench/archive_key_pointer.cpp` | Plain attempt 3, one named record pointer | 72 bytes, NONEXACT; best retained draft |
| `bench/archive_key_field_references.cpp` | Matching-shape attempt 1 after plain budget | 84 bytes, NONEXACT |

Fresh repeat outputs and historical whole-object controls agree. The target
retains a high-part receiver base and signed field displacements. The best
pointer draft retains a complete subobject address instead; its low/high seed
operation order and register assignment also differ. The field-reference shape
materializes two full field addresses and makes the result larger. Full target
bytes were compared without shortening or masking instructions.

The latter source explicitly comments its matching-only field bindings. Totals
for this routine are three plain attempts, one matching-shape attempt, one
function with a commented shape, zero register pins and zero empty-asm lines.
Original class identity, nesting, full object extent and volatile qualifications
remain hypotheses. The partial declarations are not a recovered complete class.

Revisit when new independent evidence resolves the original compiler/global
profile or surrounding class/source-unit context, or when an already-matching
routine supplies a verified shared-base pattern. Do not reopen merely to try
more expression permutations or change per-function flags. Preserve this record,
all drafts and prior reports even after a future match.

No game runtime was tested, no source linked, and no full-game gate passed.
The all-module build gate and eighteen negative checks remain unimplemented.
