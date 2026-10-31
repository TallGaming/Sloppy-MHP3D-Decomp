> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# OPNSSMP failure provenance — Bucket 3AG

The existing helper does not recognize OPNSSMP's declared tag. A pinned primary
JPCSP implementation does recognize it and associates it with an already
implemented decryption type. That is a concrete capability lead, not a proven
fix. No helper, module, compiler or game was executed during this research.

## Retained local facts

The unchanged 3AD input is 3264 bytes, SHA256
`1711d003bd744c28010e856f48c633a8b2a7a63cdae5f01d9ccd9f0ec3d49417`.
Its declared ~PSP header gives tag `0x457B8AF0`, decrypt_mode 4,
comp_attribute `0x0201`, compressed size 2926 and ELF size 3550. These remain
unauthenticated declarations. Both actual preparation trials retained exactly
`Decryption failed for tag 457B8AF0` plus newline, exit 0, empty stderr and an
empty output. The preparation gate correctly classified failure; there is no
prepared ELF or established SDK ownership.

## Exact helper's unsupported-tag path

The pinned [John-K/pspdecrypt source](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/PrxDecrypter.cpp#L357-L365)
uses exact tag lookup. `0x457B8AF0` occurs in neither of its two tag tables.
[Types 0/1](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/PrxDecrypter.cpp#L766-L832)
return -1 immediately if the first table has no entry;
[types 2/5/6](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/PrxDecrypter.cpp#L875-L885)
use the second table with the same early missing-entry return. The
[dispatcher](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/PrxDecrypter.cpp#L1077-L1127)
tries 0,1,2,5,6. Thus all five are blocked by missing tag metadata before
type-specific header/hash/cryptographic processing. Type 6 itself already exists.

This is a source-level explanation consistent with the retained run, not a new
live trace or proof that recognition is the only remaining obstacle. In
particular, neither a bad signature nor missing sign-check preprocessing was
established by the old generic failed message. “No available key anywhere” and
“missing type 6 implementation” would both overstate the evidence.

The [CLI](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/pspdecrypt.cpp#L203-L210)
writes the returned size without converting this failure to a process error;
main later returns 0. This explains why rc0 was insufficient. Public pinned LF
sources match the existing local CRLF checkout after newline normalization;
actual source-file and helper executable identities remain separately pinned.
No local source, table or executable was modified.

## Primary alternative and later format stage

Pinned [JPCSP PRX.java](https://github.com/jpcsp/jpcsp/blob/48f107aea7b021d51ebaf2fda4007ceb6f47bb03/src/jpcsp/crypto/PRX.java#L135-L146)
explicitly maps this exact tag to its `keys636_1` metadata and code 0x5B. Its
[mode/tag dispatch](https://github.com/jpcsp/jpcsp/blob/48f107aea7b021d51ebaf2fda4007ceb6f47bb03/src/jpcsp/crypto/PRX.java#L405-L425)
selects **type 6** for this tag in USER_MODULE mode, which the same source defines
as 4. It conditionally performs sign-check preprocessing only when its caller
sets `isSignChecked`. Our header and failure log do not establish that condition.
No key bytes were imported into the project helper or exposed in this report.

The separately pinned [PPSSPP decrypter](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/ELF/PrxDecrypter.cpp#L600-L610)
also lacks the exact tag in its tables. Its newer type dispatch alone therefore
does not justify expecting a successful tool swap.

JPCSP [defines 0x200 as KL4E compression](https://github.com/jpcsp/jpcsp/blob/48f107aea7b021d51ebaf2fda4007ceb6f47bb03/src/jpcsp/crypto/PRX.java#L46-L58)
and [routes nonzero compression-selector bits after successful decryption](https://github.com/jpcsp/jpcsp/blob/48f107aea7b021d51ebaf2fda4007ceb6f47bb03/src/jpcsp/crypto/PRX.java#L466-L556)
toward KL4E preparation. PPSSPP likewise
[decrypts before inspecting gzip/KL4E/KL3E payload magic](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/HLE/sceKernelModule.cpp#L1679-L1725).
Accordingly 0x0201 is a source-backed warning that gzip-only preparation may be
insufficient *after* successful decryption. It did not cause the existing
helper's absent-tag lookup. The actual inner compression magic remains unknown;
no decrypted payload exists to inspect. The reader must never relabel encrypted
bytes as KL4E output or infer a valid ELF from the declared length.

## Bounded future recommendation and remaining uncertainty

A future separately approved preparation experiment could review a minimal
helper capability addition against JPCSP's exact tag/type metadata, preserve the
original input and helper, and freeze a new helper identity before any run.
Require the known main and known type 2 preparation controls first; then process only
OPNSSMP twice with explicit per-stage statuses and full raw outputs retained.
Do not guess a different tag, force a type, skip hashes/signature checks, alter
the header or add a sign-check stage solely to make this input pass. If valid
decryption yields a non-gzip payload, stop with its raw identity; KL4E decoding
needs its own bounded source review and freeze before acceptance. JPCSP has
both a Java decompressor fallback and an optional path invoking a supplied MIPS
routine through its Interpreter; that module-execution path is outside our
static preparation scope and must not be adopted. An ELF claim
still requires complete declared-length and PSP metadata checks. This is a
proposal, with no acquisition/build/execution authorized by this research.

The public texts, immutable commits, URLs, sizes and SHA256 identities are in
`evidence/bucket-03ag/helper-map-sources.json`. The JPCSP source is 50,795 bytes,
SHA256 `3da0bc13170a97b0bd06f7e2dcd5edb841c8a10f7af0cb97a238c3b494f60ccd`.
No project bytes were uploaded. Research leaves OPNSSMP visibly unresolved,
ownership UNCLASSIFIED, compiler unlocked, initializer parked, and match credit
unchanged.
