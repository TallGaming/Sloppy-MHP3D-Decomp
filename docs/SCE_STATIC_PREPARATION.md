> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Declared SCE boundaries and static preparation

The public loader model uses an unsigned length at offset4; it does not imply a
universal wrapper size. All four retained candidates actually declare64 bytes.
Both fresh Stage A copies preserve the exact remainder at that boundary and
find complete PSP headers. The names declare two sceFont_Library and two
sceBASE64_Library candidates. OPNSSMP remains a separate offset-zero candidate.
Names alone establish no ownership or authenticity.

Both Stage A manifests/reports are9,016B, SHA-256
`8405266c9100e45d0bab3c8c34600ee4e9575001abeae4a05cb52d463c17e105`.
After both audits and a separate frozen profile, the existing pinned helper ran
twelve times: known EBOOT control first, then five candidates, in each trial.
The helper, native libraries, bindings and loader cache are pinned. No original
module is executed and no input is edited.

| Input | Repeated result |
| --- | --- |
| Main EBOOT control | Exact original2,247,320B ELF in both trials |
| Archive17/19 | Helper type2 success; gzip CRC/length checks pass;35,232B prepared bytes each |
| Archive18/20 | Helper type2 success; gzip CRC/length checks pass;1,138B prepared bytes each |
| OPNSSMP | Failed-tag457B8AF0 message, exit0, empty output; correctly rejected |

All four archive prepared files start with ELF and satisfy their declared exact
lengths, but the frozen generic `Elf32` parser rejects them with
`ELF segment file size exceeds memory size`. They remain **uninterpreted**.
No original header is repaired, field normalized or old parser relaxed. The two
font and two Base64 prepared files have four distinct full hashes and are not
silently deduplicated. All raw gzip/helper output, prepared bytes, stage logs and
failed OPNSSMP artifacts remain private and reproduce across trials.

The feasibility report distinguishes helper success, bounded gzip decoding,
ELF-container interpretation and ownership. Standard gzip support accepts one
CRC-valid complete member, no trailing input and at most16MiB, with exact
declared ELF size. Other formats stay uninterpreted. A zero process exit alone
never validates output, as the OPNSSMP failure demonstrates.

Reviews: `SCE_WRAPPER_REVIEW.md`, `BUCKET_03AD_VALIDATION_NOTES.md`. Private
Stage A bundles are under `reference/uljm05800-v102/sce-wrapper-sets/`; Stage B
build directories and both report pairs are recorded in `evidence/bucket-03ad/`.
Last full suite remains352WSL passes/zero skips; targeted pure/mocked controls
are separate. No game-code inventory completion, library exclusion, historical
toolchain, source progress, matching gate or runtime validation is claimed.
