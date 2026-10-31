> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AG independent validation

## Bounded method and retained facts

The primary dispatch imposes the stricter09:40UTC research stop; this review
finishes research at09:33UTC. Only public source texts and existing private
inputs/logs are read. No helper, compiler, emulator or module is run; no keys,
options, game headers, source drafts or tool binaries are changed. No game bytes
are submitted to any public service. This is a source/claim audit, not a new
preparation trial.

Both retained3AD OPNSSMP cases have the same3,264-byte input SHA-256
`1711d003bd744c28010e856f48c633a8b2a7a63cdae5f01d9ccd9f0ec3d49417`.
The declared header has tag457B8AF0, decrypt_mode4, compression attribute0x0201,
compressed size2,926 and ELF size3,550. Both actual streams contain the exact
failed-tag message, zero process exit, empty stderr and empty output. Neither has
a prepared ELF. The helper independently reads these artifacts and checks the
failure classifications; declarations remain unauthenticated metadata.

## Independent source/claim findings

1. **Unsupported lookup is established in the exact helper source.** The pinned
   [pspdecrypt PRX implementation](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/PrxDecrypter.cpp)
   contains no457B8AF0 entry in either exact-match tag table. Types0/1 look up
   the first table; types2/5/6 look up the second. Every path returns an error
   immediately when its lookup fails, before its type-specific header/hash/
   cryptographic processing. The dispatcher tries those five paths. This source
   flow explains the retained failed message; it is not a new binary trace or
   proof that recognizing the tag would be sufficient for success.
2. **A globally unavailable key or missing type6 implementation is not proved.**
   Type6 already exists in the exact helper. The independently pinned
   [PPSSPP implementation](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/ELF/PrxDecrypter.cpp)
   also lacks this exact tag, so merely substituting that source is not a
   supported fix. However, pinned
   [JPCSP PRX.java](https://github.com/jpcsp/jpcsp/blob/48f107aea7b021d51ebaf2fda4007ceb6f47bb03/src/jpcsp/crypto/PRX.java)
   explicitly recognizes it, references keys636_1 metadata/code0x5B and selects
   type6 in its USER_MODULE path, whose source constant is4. This is a concrete
   alternative capability lead. No key bytes are copied or printed here.
3. **Sign-check applicability remains unknown.** JPCSP conditionally invokes
   preprocessing when its external isSignChecked argument is true. Our retained
   header/failure does not establish that caller condition. The selected helper
   fails earlier at absent lookup; the evidence therefore cannot identify a bad
   signature or missing preprocessing as its observed cryptographic failure.
   No guessed sign-check flag, forced type or skipped verification is justified.
4. **Compression is a later, separately unresolved stage.** JPCSP defines the
   0x200 selector as KL4E and routes compressed nonzero-selector input through
   non-gzip processing after decryption. For the declared0x0201 value, a future
   successful decryption could require more than the existing gzip-only
   preparation. The actual decrypted magic is unknown: no such bytes exist yet.
   This declaration did not cause the current missing-tag lookup, and encrypted
   bytes must not be relabeled as decoded KL4E or a valid ELF.
5. **Process exit is not a decryption result.** The pinned
   [CLI](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/pspdecrypt.cpp)
   passes the decryptor's returned size to its file writer without propagating
   that error to main's final exit status. The retained zero exit therefore
   cannot override failed stdout or an empty output. The3AD gate correctly
   rejects the case.

## Source and artifact identity audit

All five cached texts in `helper-map-sources.json` match their recorded sizes and
SHA-256 identities. The combined manifest is1,919 bytes, SHA-256
`ec3c5bddb69fd63151138bfdc5426160f9f5d3c30deb5bff49fcc093f8f0dce4`.
It binds immutable commits for the exact helper, PPSSPP, JPCSP and the previously
inspected loader source. The JPCSP text is50,795 bytes, SHA-256
`3da0bc13170a97b0bd06f7e2dcd5edb841c8a10f7af0cb97a238c3b494f60ccd`.

The public exact-helper PRX/CLI text matches the local source after LF/CRLF
normalization only; actual local bytes retain their separate pinned identities.
The helper executable remains229,584 bytes, SHA-256
`05d323b28b3ceed86a42d019767ddcdae3e40f85dacebe25a5fe7d86f2b02c98`.
Local PRX source remains55,124 bytes, SHA-256
`aceeb545e8b9d8ccfb6e24b22b2be4123a33a97bb927193c1e537b1b3458a2e3`;
CLI source remains10,507 bytes, SHA-256
`7f7acb398084b895f20cca9cc09d197c690cf6acec70b82bdc48f178c3181206`.
No local normalization or source rewrite is performed. Source consistency is
reported separately from the observed binary run.

## Recommendation audit and limits

The sibling's bounded proposal is supported as a future review target, not an
implemented fix: investigate the source-backed recognition/type gap with a new
separately pinned capability version, keep the original helper/input unchanged,
require known whole main and successful type2 preparation controls first, and
retain two exact OPNSSMP trial outputs with explicit stage statuses. Recognition
alone must never count as decryption success. Unknown sign-check requirements,
crypto verification, decrypted format and complete ELF validation remain open.
No execution, build, acquisition, key import or header change is performed here.

If raw decryption later succeeds with non-gzip output, stop that phase at its
full raw identity. Any offline KL4E decoder needs its own source review, bounds
and freeze. JPCSP offers a Java fallback but also an optional path that invokes a
supplied MIPS decompressor through its Interpreter. That module-execution path
falls outside our static-preparation scope and must not be adopted implicitly.
No export/import reconstruction or original-code runtime test is authorized.

Final claim audit agrees with the sibling's substantive conclusions. The review
requests replacing the phrase "known type2 library controls" with preparation
controls, because library-like names alone do not establish SDK ownership. All
modules remain UNCLASSIFIED; no original game-code obligation is excluded.
OPNSSMP remains visibly unresolved, prior failures remain unchanged, the
historical compiler remains unlocked and the initializer stays PARKED with its
existing attempts/shapes. No game-match credit, library exclusion or native-port
progress follows. The352-test tooling result is unchanged; no new tests or
full-build/18-negative gate are claimed. Research stops here before09:40UTC.
