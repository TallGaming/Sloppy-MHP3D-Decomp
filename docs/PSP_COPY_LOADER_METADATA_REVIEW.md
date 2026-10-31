> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# PSP copy-loader metadata review — Bucket 3AF

The new reader records bounded PSP load declarations without asserting ELF
paging congruence. It preserves the failed 3AE model and all 3AD preparation
outcomes; it does not repair bytes or change the frozen generic ELF reader.

## Source-backed model correction

At pinned PPSSPP commit `c0fd904feefedc66441d4d5d602e46d2fd8e4fd6`, the
[load-copy path](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/ELF/ElfReader.cpp#L704-L735)
gets its source from the file offset and its destination from base plus virtual
address. It bounds file bytes and rejects PT_LOAD filesz greater than memsz,
then performs a byte copy. It does not test file/virtual modulo congruence.
The [allocation path](https://github.com/hrydgard/ppsspp/blob/c0fd904feefedc66441d4d5d602e46d2fd8e4fd6/Core/ELF/ElfReader.cpp#L641-L677)
uses first-load alignment for allocation, or warns when a caller-specified base
does not meet it; non-power-of-two alignment falls back to ordinary allocation.
These observations warrant recording alignment shape and congruence, without
using them as rejection criteria or claiming paging validity. They do not prove
a module could execute successfully after relocation.

The source-backed module-info lookup, 52-byte structure and attribution limits
remain as documented in `PSP_MODULE_METADATA_REVIEW.md`. For a sectionless PRX,
record first-header raw p_paddr and its `0x7FFFFFFF` mask as a file offset; require
the full structure within the first file-backed PT_LOAD. Preserve 27 name bytes,
a separate terminal byte, version bytes and five raw pointer words. No pointer
is dereferenced. Named section selection remains a distinct provenance path.

## Exact independent pre-execution review

Approval covered reader `evidence/bucket-03af/read_psp_copy_loader_metadata.py`,
14,102 bytes, SHA256
`dabefc096a5f5bf5fe35a4a90d24451ec052a0fc4205d17f0a2b0e52922f4826`,
and profile `config/psp-copy-loader-metadata.json`, 7,427 bytes, SHA256
`a32c4f32522b0da1bc2261e90252724f50b797eb1799624a790ef51021ca558e`.

Full comparison against frozen 3AE confirms that the only format-model change
is replacing alignment rejection with explicit observations. File/table/string
bounds, PT_LOAD filesz/memsz and 32-bit extent checks, exact input byte pins,
whole main controls, unknown-type retention, source-backed module-info bounds,
parent-link guards and exclusive report publication remain. New config/freeze
paths and report/model names distinguish the new evidence. The new profile pins
the old source, profile, freeze and both failure reports without rewriting them.

Approval is limited to two five-case metadata reads of existing prepared bytes.
There is no decryptor, compiler, relocation, loader or module invocation. The
reader's bounded interpretation is not authentication, SDK ownership proof,
complete game-code inventory, compiler attribution or byte-match credit.

## Frozen actual outcome and independent raw audit

Both `evidence/bucket-03af/metadata-trial-{1,2}.json` reports are byte-identical,
422,021 bytes, SHA256
`c9490f6a2d0cee5214c5935aa6ac6b23dd8385dac6e773c922b498657d3c0514`.
The freeze records the two approved input identities before the actual reads.
The full main controls equal the pinned EBOOT ELF and preserve its 356 program
headers, 734 sections and named module-info selection. Its PT_LOAD offset
0x2CB4 and address 0x08804000 remain noncongruent under p_align 0x10; the report
records false congruence and no paging guarantee without changing these bytes.

| Case | Module-info file offset | Declared name | Attributes / version bytes |
| --- | --- | --- | --- |
| Main control | 1442516, exact named section | MonsterHunterPortable3rd | 0 / [1,1] |
| Archive 17 / 19 | 31184, first-header masked p_paddr | sceFont_Library | 6 / [1,1] |
| Archive 18 / 20 | 608, first-header masked p_paddr | sceBASE64_Library | 6 / [1,1] |

All four PRX files declare no section table. Each has two bounded PT_LOAD
entries plus PT_PSPREL2 bytes with memsz zero: 1968 bytes for 17/19 and 50 for 18/20.
Their full 52-byte module-info records are inside the first file-backed load;
terminal bytes are zero. Paired records agree, but all four complete prepared
files remain distinct. No relocation contents were decoded or applied, no
export/import entries were reconstructed, and raw pointer values were not
converted to runtime addresses.

Independent read-only Python struct/hash checks reconstructed all ten complete
input identities, 736 program-header instances, 1,468 section instances and ten
module-info records from the original bytes. They verified all reported field
widths, program file hashes, first-load bounds, name bytes, terminal bytes,
version bytes, raw pointer words, alignment observations and section-name data.
Both report bytes agree, and 23 inherited format/reference/preparation/preserved
pins were independently rehashed. No compiler, decryptor or module was invoked
for this audit.

The main's exact comment strings remain `MW MIPS C Compiler (2.4.1.01)` and
`PSP`. The sectionless candidates have no section-based comment observation;
this is no evidence of a particular producer or of their entire source language.
The bounded declared names do not authenticate library ownership. All cases
remain UNCLASSIFIED. OPNSSMP still has no prepared ELF after its retained 3AD
helper failure and was not retried or included as a successful metadata case.

The generic reader, 3AD preparation outcomes and both frozen 3AE failures remain
unchanged. This bucket establishes bounded metadata for the four retained PRX
images, not executable correctness, a complete game-code denominator, SDK
exclusion, toolchain lock, source integration or match credit.
