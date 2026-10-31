> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# GCC 4.3.5 diagnostic assembler ABI

The new frontend declares single-precision hardware floating point in both its
preexisting target help and emitted `.gnu_attribute 4,2`. The modern assembler's
baseline profile instead reports an ABI compatibility warning. A separately
reviewed check assembles the **same retained invented assembly**, without
recompiling it or changing any source directive.

Both fresh Stage A trials reproduce the baseline warning exactly and reject
that case as a clean pipeline. Adding `-msingle-float` removes all diagnostics.
All four complete objects equal the pinned 6,056-byte retained artifact, SHA-256
`890b3018129707bde119a706fc6540cd12d4dff683f32bf65aca6eee1f52e41d`.
This equality covers code, data, symbols, relocations and metadata; no byte is
masked or sliced. The setting changes acceptance of the declared ABI without
changing these object bytes. No compiler ran in Stage A.

The two independent reviews and separate freezes govern Stage B: the existing
static-object and grouped-address fixtures, old/new GNU frontends, two fresh
trials. Both historical old whole-object controls must reproduce before new
compilation. The new frontend uses this single assembler setting uniformly;
the old profile and every compiler flag remain unchanged. Any stage diagnostic,
inspection failure, decoder uncertainty, missing output or identity drift stops
the new comparison and preserves partials without a success report.

Both Stage B trials pass. The complete object identities reproduce:

| Fixture | Old GNU object | GCC4.3.5 object |
| --- | --- | --- |
| Static C++ object | 6,312B, `a8848c36...` | 6,056B, `890b3018...` |
| Grouped address | 1,204B, `22690e39...` | 1,272B, `8f46afb5...` |

All eight compiler/assembler pairs have empty diagnostics, and all eight
decoders complete cleanly. The old objects equal their historical artifacts.
GCC4.3.5's grouped function is72B versus64B for the old compiler; its emitted
assembly uses the later signed-high/negative-displacement split. The unchanged
bounded address checker returns **UNINTERPRETED with no reuse count** for both
compilers' non-NOP branch slots. These observations do not compare a game target.

The new static fixture references `__cxa_atexit`, has an initialization wrapper
and lacks the old selector/priority dispatcher and separate cleanup wrapper.
It therefore differs from the convention observed in the original3V sample.
The old/new backends each explain some observations; neither is historically
established, and no flags are changed to reconcile the differing defaults.

See `BUCKET_03AA_CHECKPOINT.md` for the completed result. This diagnostic
profile is not a historical toolchain lock or a game match. The frozen failed3Z
experiment remains failed. Reviews are `GNU435_ASSEMBLER_ABI_REVIEW.md` and
`BUCKET_03AA_VALIDATION_NOTES.md`; private artifacts are under
`evidence/bucket-03aa/` and the referenced fresh build directories.
