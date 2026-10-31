> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AF: source-backed PSP copy-loader metadata

Preserve failed3AE and the original generic ELF reader. Use the same two retained
sets and the same primary sources in a new version/profile. Pinned PPSSPP
ElfReader.cpp704–735 bounds file bytes and copies PT_LOAD payloads; it does not
require file/virtual offset congruence. Its allocation path also treats alignment
as an input with fallbacks. Therefore record alignment shape/congruence as
observations, without claiming paging validity or rejecting metadata solely for
those declarations. Do not repair a header, move bytes or map/execute a module.

Keep all file/table/string bounds, PT_LOAD file-size/memory and32-bit range
checks, source-backed sectionless module-info selection and both known main
controls. Unknown non-load contents and all pointer fields remain uninterpreted.
Freeze the new reader/profile only after both exact reviews and meaningful
controls, then run the same five-case metadata suite twice. Compare complete
input bytes and all metadata; no original preparation rerun or ownership claim.

Primary owns new version/profile/integration/checkpoint. Helper1 owns
`PSP_COPY_LOADER_METADATA_REVIEW.md`; helper2 owns
`BUCKET_03AF_VALIDATION_NOTES.md`, targeted malformed/observation/identity tests
and final independent audit. Preserve all older negative outcomes. No compiler,
source form, flags, relocation application, SDK exclusion, game execution,
credited match or port. Finish the reviewable checkpoint before09:52UTC.
