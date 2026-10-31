> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Isolated OPNSSMP tag capability

The missing-tag lead is confirmed on the unchanged input. The isolated helper
naturally selects type6 and produces2,926 bytes beginning `KL4E`, SHA-256
`baa08abb7d5aef2fff636f0eecfd01f49a67f1fe887d6a55e1f14cc3a307dfe5`.
Both trials give the same bytes. There is no prepared ELF yet: the existing
raw-ELF/gzip preparation code correctly leaves this encoding uninterpreted.

The candidate is a separate source-built host tool. All34 baseline source files
match the original pinned commit and checkout exactly, including CRLF. Only two
insertions change one candidate file: the exact public16-octet JPCSP metadata
array and its457B8AF0/code5B table entry. The dispatcher, type selection,
cryptographic algorithms, headers and original helper are unchanged.

Four fresh builds reproduce complete products. Both baseline binaries equal the
old229,584-byte helper exactly. Both candidate binaries are229,632 bytes, SHA-256
`9101c7dfc5c4667b5a400b947b94ec3e5b584b7a877cc41ab0983b0571528920`.
The original host recipe and a minimal child environment were used; no PSP game
compiler profile or flags changed. An initial source-copy preflight stopped on
a one-sided newline comparison; its partial tree/failure remains preserved.
The corrected source copy uses exact raw-byte equality, not normalization.

Build diagnostics are retained unchanged across all four builds: nine OpenSSL
deprecations, one old-style definition and two preexisting signing-routine
overread warnings. The selected decryption path does not call that signing
routine. The helper's existing `g_checkEcdsa=0` and other preexisting behavior
remain unchanged: this result is **not signature authentication** and introduces
no new bypass. The existing type6 SHA comparison remains active.

After source/build audits and a separate execution freeze, each trial requires
the complete main output and all four known type2 raw/prepared outputs to equal
their3AD artifacts before OPNSSMP runs. All ten control cases reproduce exactly.
Twelve candidate-helper calls complete; both OPNSSMP outputs are identical, with
empty stderr and natural type6 agreement. All inputs,212 build artifacts,
runtime bindings, golden outputs and prior source/assembly/profile pins verify.

Profiles and private build/experiment reports are under `config/opnssmp-tag-*`
and `evidence/bucket-03ah/`. Reviews are `OPNSSMP_TAG_CAPABILITY_REVIEW.md` and
`BUCKET_03AH_VALIDATION_NOTES.md`. Original failed3AD and all older results remain
intact; the shared helper lock still selects the original helper.

Next requires a separate bounded host KL4E preparation model. No module code
executes, no library ownership is assigned, and no game source or match credit
follows. Last full suite remains352 WSL tooling passes/zero skips; source/build/
control-specific checks are separate from the outstanding full-game gate.
