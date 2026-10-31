> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# PSP copy-loader metadata

Both new metadata reports repeat exactly:422,021B, SHA-256
`c9490f6a2d0cee5214c5935aa6ac6b23dd8385dac6e773c922b498657d3c0514`.
The known main executable remains byte-exact. The separate reader records its
noncongruent file/virtual offsets without claiming paging alignment or changing
the original file. Pinned PPSSPP source bounds and copies segment bytes; this
is the applicable metadata model, unlike the failed generic assumption in3AE.

| Retained input | File bytes | Program metadata | Module-info declaration |
| --- | --- | --- | --- |
| Main control | 2,247,320 | Original356 program headers/734 sections retained | MonsterHunterPortable3rd, exact named section |
| Archive17/19 | 35,232 each | Two bounded PT_LOAD records and one PSP relocation2 record; no sections | sceFont_Library, file offset31,184 |
| Archive18/20 | 1,138 each | Two bounded PT_LOAD records and one PSP relocation2 record; no sections | sceBASE64_Library, file offset608 |

The relocation program type is0x700000A1. Its file bytes are bounded, with zero
declared memory size; no relocation stream is interpreted or applied. PT_LOAD
file-size/memory/range constraints remain strict. Every file/table/string extent
is bounded independently, including section records where present. Unknown
non-load types remain explicitly uninterpreted.

Sectionless PRX module-info selection follows pinned loader code's first-header
p_paddr file-offset rule with mask0x7FFFFFFF, narrowed here to the first PT_LOAD
and its full52-byte file-backed extent. The raw field, mask and selection method
are recorded. The27-byte name and separate terminal are preserved; version,
attributes and five pointer words are declarations. No pointer is dereferenced
and no export/import table is reconstructed.

Paired font/Base64 module-info bytes agree, but their full files and first load
segments differ. Keep all four original containers; metadata similarity is not
deduplication or compiler/source matching evidence. Names alone grant no SDK
exclusion or ownership classification. OPNSSMP still has no prepared ELF after
the failed3AD attempt.

Reviews are `PSP_COPY_LOADER_METADATA_REVIEW.md` and
`BUCKET_03AF_VALIDATION_NOTES.md`. Exact profiles, primary-source caches, freezes,
paired comparisons and reports are private under `evidence/bucket-03ae/` and
`evidence/bucket-03af/`. All3AD/3AE outcomes and the generic `Elf32` source remain
unchanged. Last full suite remains352WSL passes/no skips; targeted model/identity
controls pass separately. No code is executed, relocated, rewritten or credited.
