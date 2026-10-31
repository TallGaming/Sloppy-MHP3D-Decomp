> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AE: separate PSP module metadata reader

Use the remaining timed approval to investigate the four retained ELF parser
rejections. Preserve every3AD result and the original generic `scripts/elf32.py`;
do not alter its validation or frozen compiler/matching profiles.

Review primary ELF/PSP loader definitions before interpretation. A bounded raw
header/program-table preflight may identify the actual rejected program types.
The new reader must distinguish PT_LOAD memory constraints from non-load
metadata, validate all file extents, retain unknown program types explicitly,
and never apply relocations, invent memory mappings or rewrite an input header.
Reuse existing bounded byte/string access where suitable, without normalizing
or patching a copy to make the old parser accept it.

After both reviews/freeze, read both retained preparation sets: exact known
main ELF controls plus four candidate prepared files per set. Compare all
original bytes, parsed metadata and repeat reports. Report bounded program and
section fields, named module-info metadata only where its structure/source and
section extent are proven, and exact compiler-comment strings if present.
The bounded preflight establishes that allfour candidates are sectionless PRX
files with a700000A1 non-load relocation segment. For these, permit a module-info
file offset only if primary loader source confirms the exact first-header
p_paddr rule and both reviewers approve its52-byte first-load bounds. Preserve
that raw field and any mask explicitly; never fabricate a named section.
Missing or unsupported metadata stays uninterpreted. Decrypted module names
alone do not grant SDK ownership or remove game-code obligations.

Primary owns the separate reader/profile/integration/checkpoint. Helper1 owns
`PSP_MODULE_METADATA_REVIEW.md`, primary format/source and attribution limits;
helper2 owns `BUCKET_03AE_VALIDATION_NOTES.md`, meaningful malformed/load/nonload/
unknown/bounds/identity controls and independent repeat audit. Review/freeze exact
inputs and reader before final metadata runs. No new decryptor calls, original
code execution, game source/flag change, parked initializer revisit, compiler
lock, library exclusion, match credit or native-port work.

Stop at a reviewable checkpoint by09:52UTC. Do not start a wider export/import
reconstruction or unsupported OPNSSMP recovery if reviews cannot finish in time.
