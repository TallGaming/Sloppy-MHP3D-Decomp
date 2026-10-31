> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AE: metadata model — failed-control checkpoint

**Both frozen trials stop at the known main executable before any PRX result.**
The new reader imposed a generic ELF alignment/congruence condition. The
unchanged main PT_LOAD has file offset0x2CB4, virtual address0x08804000 and
alignment16; these offsets differ modulo16. Both114-byte failure records repeat
the same rejection, and no normal metadata report exists.

The parser and its pure tests checked the declared condition, but did not prove
that condition applies to the actual PSP copy loader. The source review missed
this distinction. Pinned PPSSPP code copies bytes from file offsets to declared
virtual destinations without requiring that paging-style congruence. It also
has fallback allocation behavior for alignment shapes. This supports a new
metadata model that records these declarations without claiming paging validity.

All3AE inputs, source/profile/freeze, failures and prior generic reader remain
unchanged. See `PSP_MODULE_METADATA_REVIEW.md` and
`BUCKET_03AE_VALIDATION_NOTES.md`. No PRX is counted as parsed or identified.
Last full suite remains352WSL passes/no skips; source/trick/parking/match counters
and all user requirements remain unchanged.

Completed failed investigation under timed approval, pending review. A separately
reviewed3AF may apply the source-backed copy-loader metadata model, with all file
extent/PT_LOAD memory bounds retained and alignment observations kept explicit.
This does not alter the matching gate or any compiler/source configuration.
