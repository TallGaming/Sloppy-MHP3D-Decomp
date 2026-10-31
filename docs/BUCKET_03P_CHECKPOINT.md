> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3P: real-offset archive copies — completed checkpoint

**The readable pointer pattern reduces the real-offset diagnostic to 72 bytes,
but it remains NONEXACT against the full 68-byte target.** Grouping alone produces
the same 100-byte function and whole object as the original flat draft. Both
fresh three-case trials agree, with the unchanged historical control reproduced.

| Source hypothesis | Attempt | Complete function | Exact target bytes | Static base sites |
| --- | ---: | ---: | --- | ---: |
| Preserved flat draft | 1 | 100 bytes | No | 5 |
| Grouped key record | 2 | 100 bytes | No | 5 |
| Named key-record pointer | 3 | 72 bytes | No | 1 |

All four declared volatile-access paths agree. The target itself remains
`0x0886233C..0x08862380`, SHA-256
`7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57`.
No byte is trimmed or normalized. All three first differ at byte zero.

The remaining difference includes more than function length: the target forms
`receiver + 0x30000` in a0 and uses signed field displacements F53C/F540. The
pointer form builds the exact `receiver + 0x2F53C` address using LUI/ORI/ADDU in
a2 and accesses offsets zero/four. Seed-operation order, assigned registers and
default-value registers differ too. Removing a word or renaming registers would
not establish equality. These observations do not identify the original class,
qualifiers, compiler build or global settings.

## Frozen evidence

The original `bench/archive_key_initializer.cpp`, original profile and target
manifest are unchanged. New preserved copies are `bench/archive_key_grouped.cpp`
and `bench/archive_key_pointer.cpp`. Helper review preceded compilation and the
only post-review profile change was its frozen status.

- `config/archive-pointer.json`: 1730 bytes, SHA-256
  `280c8dd72be9847bc6bd043e8211bf5cc045dc8496a37f3e748c9d060b7d23cf`.
- Both 30076-byte reports: SHA-256
  `a2b909b6f17c3022337dc795159dc8c2c0558c66b08f73faae8bda37c1650cc1`.
- Build roots: `build/archive-pointer-3ifya77m` and `build/archive-pointer-nu4biryj`.
- Pointer whole-object SHA-256
  `5ee9111363a6205e76bd0c3f12dccd4bf174fdeef574229b7bf561c49298bd42`;
  complete function SHA-256
  `ba2cd810be0758f8ba2a416a28d7bb30c9f1b5857e6596c4bdbd876e934a5331`.

Reports, complete disassemblies, freeze/provenance and final summary are under
`evidence/bucket-03p/`. Independent reviews are `ARCHIVE_POINTER_REVIEW.md` and
`BUCKET_03P_VALIDATION_NOTES.md`. Both helpers rechecked six objects, full target
comparisons, raw word differences and input preservation. All **309 tooling
tests pass, zero skips**, including six new integrity controls. This is separate
from the unimplemented full-game gate and its eighteen negative tests.

## Stuck-rule decision

The three plain-source attempts for this routine under the current diagnostic
profile are exhausted. Preserve them; repeats do not create new attempts.
Do not introduce a fourth plain form or change per-function flags. Under the
active advance approval, the next bounded plan may try one explicitly commented
field-binding shape, with its matching-only trick counted in HANDOFF.md. If it
also fails, park the routine visibly with its original assembly, best draft,
attempt log and a concrete revisit condition, then move to other useful work.

No game function has passed the full byte gate, source is not linked, the
toolchain remains unlocked, and no runtime or native-port work occurred.
Register pins/empty-asm/matching-only shape counts remain zero at this checkpoint.
