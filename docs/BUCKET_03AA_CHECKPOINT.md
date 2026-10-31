> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AA: assembler ABI consistency — output checkpoint

**The new GNU candidate now has a clean, repeatable invented-fixture pipeline.**
Stage A uses the exact retained invented assembly: both baseline warning
controls remain rejected, both single-float cases are clean, and all four
complete objects are byte-identical. No compiler runs in Stage A.

After both output audits and a separate Stage B freeze, eight invented compiles
complete cleanly across two fresh trials. All complete objects and raw assembly
repeat; historical old-GNU controls match exactly. See
`GNU435_ASSEMBLER_ABI.md`, both independent reviews, and private3AA reports.

The new grouped function uses the later signed-offset split but is72B versus
old64B. Its bounded checker remains UNINTERPRETED without a reuse count.
The new static fixture uses `__cxa_atexit`, unlike the selector/priority pattern
in the original sample. Thus the candidate is usable for diagnostics but does
not establish the game's compiler. No game target was compared in this bucket.

The single assembler ABI setting applies uniformly to the new frontend's
fixtures, based on its preexisting help/attribute; compiler flags and historical
profiles remain unchanged. Failed3Z stays failed. Last full suite remains
340WSL passes/zero skips; targeted pure/mocked failure controls pass separately.

One routine remains PARKED, with three plain attempts and one commented shape;
zero pins/empty asm, credited matches or linked-source functions. The full gate
and18 negative checks are pending. PSP reference/privacy/matching-before-port
requirements remain unchanged. Completed under timed approval, pending review.

Next separately reviewed diagnostic: the entire existing fourteen-probe suite
under fixed old/new GNU C++ profiles, with a prior invented naming fixture and
mandatory whole-object controls. Choose the language before seeing scores and
keep the archive routine parked. No new source or per-function flags.
