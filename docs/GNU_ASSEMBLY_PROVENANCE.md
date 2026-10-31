> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Retained GNU assembly and backend provenance

Bucket 3Y, 2026-10-31. The existing invented grouped-address fixture is compiled
under the unchanged GNU C++ O2 profile. Two fresh trials compare the established
ordinary pipeline with an equivalent native staging path that also retains the
emitted assembly verbatim. No game draft or target is compiled or compared.

Both helpers review the exact inputs before the freeze and all four invented
compilations. Every complete object is identical: 1,204 bytes, SHA-256
`22690e399773b59c25a0b3966312c5f6465c9d96690d5a91dba274b78ee80523`.
Both 995-byte assembly copies are identical, SHA-256
`9c1aabe61e5c0de8e02071f3759d294a1936833266514bd964d17281512a1078`,
matching the hashes from both ordinary pipeline invocations. Capturing this
file changes neither source, flags nor resulting object in this experiment.

## Compiler emission versus assembler behavior

The raw compiler output explicitly forms `0x18000` with a load-immediate of
65536, ORI `0x8000`, then ADDU. It explicitly accesses field displacements
8480/8484 (`0x2120/0x2124`), giving the invented offsets `0x1A120/0x1A124`.
Thus the compiler has already chosen this base/displacement decomposition
before the assembler processes the file. It is not solely a later assembler
choice between two equivalent address expansions.

The compiler also explicitly places default-value LI instructions immediately
after BNE under `.set noreorder`. Those branch delay-slot choices are already
present in emitted assembly. In contrast, the final `j $31` has no explicit
following NOP and is under reorder mode; the resulting final return-delay NOP
is supplied by this assembler pipeline. These distinctions prevent attributing
every instruction or every NOP to the same stage. This fixture has no move
pseudo-instruction, so it supplies no direct observation of move expansion.

## The upstream address algorithm changed

The pinned GCC 3.3.3 target header's
[`LEGITIMIZE_ADDRESS` macro](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/config/mips/mips.h#L3239)
splits large offsets using `high = offset & ~0x7fff` and
`low = offset & 0x7fff`. It predicts both the observed invented split
`0x18000 + 0x2120` and the earlier original-draft pipeline output
`0x28000 + 0x753C`. The SDK binary is a patched frontend, so upstream source
agreement alone is not a proof of source-to-binary equivalence; the retained
assembly independently establishes the actual tested fixture's emission.

The pinned GCC 3.4.6
[`mips_add_offset` implementation](https://github.com/gcc-mirror/gcc/blob/6018a82534694970fb27a6846b15d370b392085f/gcc/config/mips/mips.c#L1795)
uses signed high/low helpers. Its
[target-header definitions](https://github.com/gcc-mirror/gcc/blob/6018a82534694970fb27a6846b15d370b392085f/gcc/config/mips/mips.h#L1983)
calculate high as `(value + 0x8000) & ~0xffff` and low as value minus high.
For `0x2F53C`, those expressions give `0x30000` and `-2756`, the original
routine's observed address pattern. This is a concrete upstream algorithm
difference supporting investigation of later GNU backends, not an exact
version identification or a source/flag trick.

The review also finds later explicit sibling-call hooks and generic delay-slot
reorganization code. Their existence does not prove that a particular SDK
configuration executes those paths, which flags the game used, or why every
original slot is filled or empty. Precise source/version boundaries and a
citation-only correction for earlier line-number counting are in
`GNU_BACKEND_PROVENANCE_REVIEW.md`. Two directly required target headers were
added to the six initially selected implementation files after discovering
where the macros actually live; no compiler/capture inputs changed.

## A verified version lead, still not a historical lock

A community PSP recipe dated 2010-11-26 explicitly selects GCC4.3.5,
binutils2.18 and PSPSDK0.10.1
([pinned Minimalist PSPSDK build script](https://github.com/pmlopes/minpsp/blob/cfc3435509fefb0e05cb55acf2c2deb34b592399/toolchain.sh)).
This establishes a dated PSP toolchain recipe. It does not establish an
installed binary, complete patched source closure, publisher use or the game's
historical compiler. No new compiler archive is downloaded or built in 3Y.

## Reproduce and review

The fresh directories are `build/gnu-assembly-capture-cjxdcgvg` and
`build/gnu-assembly-capture-4nu26rfp`. Each retains `emitted.s`, ordinary/capture
objects, exact stage records and decoded object output. Reports, freeze, public
source caches and the fixed driver are under `evidence/bucket-03y/`.

The source is the unchanged `bench/address_reuse_grouped.cpp`; the profile is
`config/gnu-assembly-capture.json`. The 11,374-byte driver SHA-256 is
`043bf0c4caebc7b8c2d669afcae88f5ad4a7d2ba29f6769585829eb791f7a4b5`.
The 871-byte freeze SHA-256 is
`bb617549ec8d2172a94e86e19f6d7bf1afb306e0456cf01ccbae917f0f500e79`.
Independent reviews are `GNU_BACKEND_PROVENANCE_REVIEW.md` and
`BUCKET_03Y_VALIDATION_NOTES.md`. Source, native assembly, retained copy and all
object identities remain checked; failures retain partials without score.

No new production tool or test suite is added; the last full suite remains
340 WSL passes with zero skips from 3U. Matching/source-link credit stays zero,
the archive routine stays PARKED with unchanged drafts/counters, and global
historical compiler/profile and full-game gate remain unresolved. No game,
linked object or native port is executed or implemented.
