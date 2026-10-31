> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AD: declared SCE wrapper lengths and static preparation feasibility

Use the remaining timed approval to test the concrete public-loader lead from
3AC. Stage A reads the four retained raw SCE candidates using only the pinned
loader's declared-length model: at least eight bytes, unsigned length at+4,
positive bounded length strictly inside the original payload. Never assume
0x40, scan for convenient magic, or repair the declared field. Record the
declared extent and exact inner identity. Only a complete `~PSP` header exactly
at that declared offset is eligible for a later PRX preparation attempt.
Unknown or unsupported inner formats remain uninterpreted, with no guessed
module/ownership or code extent. Do not decrypt during Stage A.

Both original supplemental sets must agree first. Pin the original raw inputs,
header/loader source, current parser/profile and preserved game/compiler/asm
inputs. Evaluate two fresh Stage A copies/reports and compare every byte and
metadata field. Also record OPNSSMP as an offset-zero PSP candidate, keeping it
distinct from the wrapped archive candidates. Main EBOOT remains a control only.

Only if supported by both Stage A audits, Stage B may receive its own exact
profile/reviews/freeze: the existing pinned decryption helper, one unchanged
invocation per eligible input per trial, two fresh trials,20-second time bounds,
and original EBOOT decryption/ELF identity as mandatory positive control before
any new candidate. Retain all failures/partial outputs/logs. Where the helper
returns an offset-zero gzip stream, permit one bounded standard-library gzip
decode with CRC/end-of-stream/unused-input checks and the declared ELF length;
preserve the original helper bytes. Other compression formats stay uninterpreted.
Decryption success,
complete ELF interpretation, module attribution and matching credit are separate
outcomes; do not infer authenticity or ownership from a return code/name.
If the remaining window cannot cover reviews and validation, leave Stage B
unstarted at the checkpoint rather than rush it.

Primary owns parser/profile/runners/integration. Helper1 owns
`SCE_WRAPPER_REVIEW.md`, exact loader-source/model and scope review. Helper2 owns
`BUCKET_03AD_VALIDATION_NOTES.md` and meaningful parser/boundary/integrity
controls. Both review/freeze each stage before actual execution. No original
module is ever executed. No source rewrite, compiler flag, linker, parked
initializer revisit, native port, library exclusion or match credit follows.
