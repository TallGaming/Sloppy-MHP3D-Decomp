> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AC independent validation

## Scope and required controls

Recover only the declared eight raw payloads into two fresh private sets: four
selected ISO files (the main EBOOT as a mandatory control, BOOT, OPNSSMP and
packaged updater EBOOT) and exact raw archive entries17-20. The latter are ~SCE
prefix candidates, not established executable extents or library ownership.
No decryption, deobfuscation, decompression or executable launch is authorized.

Require complete catalogue identity before and after, a fresh ISO directory
inventory with bounded path/extents and hashes, validated archive index/exact
lengths/prefix identities, and byte-exact comparison to the main EBOOT control.
Archive padding must not enter a payload. BOOT can be called zero-filled only
after every byte has been checked. Declared ~PSP metadata is separate from
actual recovered size and does not authenticate the file. Unknown headers and
inner structure remain uninterpreted.

Publication must preserve conflicting outputs/reports, guard linked or
nonregular staging paths, reject extra staged files and recheck complete staged
payload/manifest bytes and source identities before publishing a fresh bundle.
A manifest plus payload directory is the transaction unit; a later external
report copy is not an all-or-nothing transaction across directories.

## Exact pre-recovery review

The helper approves these exact inputs before real recovery and the primary's
separate freeze:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `scripts/inventory_supplemental_modules.py` | 13,670 | `f4029f998558603f420ac246809c46d52e53cafcbd5772a5dff0879b1bf33de9` |
| `config/supplemental-modules.json` | 3,060 | `96d8d9eb2f3904d8ce3f987aaaf92cf90f802c73fe845e482b553ca81ae1ed61` |
| `tests/test_supplemental_modules.py` | 12,607 | `05290ac085541bea89578d5c5a9f221bdb00a841ff6c1b8f546ced0ea307be8a` |

Actual nested input verification passes without recovering ISO bytes. Before
freeze, this helper finds that a stage directory could itself be replaced with
a symlink: payload link checks alone follow that directory. The primary adds an
explicit stage directory/link guard and rechecks stage/output-parent chains
adjacent to rename, plus the report-parent chain before writing. The corrected
source is the approved identity above.

Twelve meaningful new tooling tests pass under WSL, with no skips. Small invented
BytesIO/container fixtures exercise exact eight-item order and whole bytes,
archive padding exclusion, full EBOOT control, BOOT's final nonzero byte,
missing/duplicate ISO paths, hash mismatch, truncated/out-of-bounds reads,
archive index/length/extent/prefix guards, declared-only header metadata and
missing/extra/changed/linked staged products. Mocked inventory boundaries then
exercise fresh repeat bundles, existing output/report preservation, path escape
and input aliases, late whole-ISO mutation with size and mtime restored, fresh
inventory/directory mismatch, late pin drift and staged payload/extra-file/
manifest-symlink substitution. Actual POSIX symlink checks run in this suite.
The bounded extent reader runs directly and no decryption decoder is called.
The integration fixture mocks inherited discovery/verification because the
complete inherited reference pipeline has separate prior tests. A separate actual nested verify_inputs call
checks real project pins without recovering or executing anything.

These tests validate tooling, not the matching gate's 18 negatives. No helper
performs real recovery, launches a compiler/tool or changes source/profile/
parking inputs. Original actual outputs will be audited read-only after freeze.

## Actual output audit

The helper independently reads both completed private sets, `run-1` and
`run-2`, and compares all sixteen payload copies to direct bounded original ISO
reads. Each set has exactly eight payloads totaling 10,082,440 bytes; duplicates
do not increase inventory coverage. The source reads use the ISO directory LBA
and exact file length, or archive LBA plus indexed block and exact stored length.
The four raw SCE entries' prefixes and lengths agree with the frozen inventory;
sector padding is excluded. This audit does not execute the recovery routine.

| Payload | Bytes | SHA-256 |
| --- | ---: | --- |
| Main EBOOT control | 2,247,664 | `9a4142cbe12086f538046633f59cc9b2bbf024c91b16cbe9710078d1cef91fb5` |
| BOOT | 2,247,320 | `903a31545cbed615a8d520666805e7c8f6024eb85129f63d51ac0f32089319f1` |
| OPNSSMP | 3,264 | `1711d003bd744c28010e856f48c633a8b2a7a63cdae5f01d9ccd9f0ec3d49417` |
| Packaged updater EBOOT | 5,540,576 | `5ff66bc5cf2f1bfc658107737a6405b57fb969fe0641d64baca8039300d0a05f` |
| Archive entry17 | 20,688 | `4d0db777832973b8b40e6ed0206cdf68d0a52332d5f557dde60291dd6a6f0928` |
| Archive entry18 | 1,120 | `c077b56b6fe0ee5ca79fc30f7b0031c50ca161dcda037ff5b123f05411edb4f5` |
| Archive entry19 | 20,688 | `f0b2c5bb232938b6b21534405b840ca57da68ce6e528924028828c83a82805d4` |
| Archive entry20 | 1,120 | `c75cf1f32e70c4301f4c0a8cf3427a4bdcf5bd27c30d63d826d9b6ad2dc0f1b4` |

The main EBOOT is byte-exact to the existing encrypted reference control. Every
one of BOOT's 2,247,320 bytes is zero; this is a full-byte audit, not a prefix
inference. The three supported ~PSP headers yield exactly the recorded declared
metadata. The four raw ~SCE containers and zero-filled BOOT remain
UNINTERPRETED by this header reader; no presumed inner offset, decryption result
or executable size is inferred. The packaged updater stays distinct from
game-owned matching progress. Declared module names/tags do not establish owner
or authenticated contents.

Both bundle manifests and their external reports are byte-identical: 8,656 bytes,
SHA-256 `b88187266d7cffa99f5f82ea6902dffde4c3dded119e7f3ef62dd256fafb995a`.
The helper checks exact staged/published file sets and complete manifest bytes.
The 912-byte pre-recovery freeze has SHA-256
`8605d59d43036ec6c7b9bbf404d92836739b81adbea6f881487d77dbf5a347bd`;
all three frozen source/profile/test identities remain exact.

A fresh full ISO directory inventory agrees with all fourteen pinned directory
records. Complete ISO size, SHA-256, SHA-1, MD5 and CRC32 match the active lock
both before and after this independent read-only audit. Fresh nested input
verification also passes, including preserved parked assembly/source and
compiler profiles. No original input is modified. The primary's retained WSL
full-suite log reports 352 tests passing without skips; the helper separately
ran all twelve new tests successfully. These are tooling tests, distinct from
the still-unimplemented full-build matching gate and its eighteen negatives.

No decryption, deobfuscation, decompression, compiler/game execution, source
attempt, parking change or match credit occurs. This closes the declared
supplemental-container recovery gap, not the complete game-code inventory or
ownership denominator.
