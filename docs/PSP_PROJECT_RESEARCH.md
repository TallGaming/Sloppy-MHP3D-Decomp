> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# PSP project research

Read-only review, 2026-10-30. Four public matching projects were inspected at the
commits linked below. These are implementation evidence and investigation leads;
their reported progress was not independently rebuilt. No local experiments,
tool downloads, source changes, or toolchain decisions follow from this review.

## Closest comparison: Monster Hunter Portable 2nd G

[MHP2G configure.py, snapshot 5b98acfd](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/configure.py)
targets ULJM05500 and constructs EBOOT plus named overlays, with module checksums
and separate application/library progress categories. Its C/C++ rule selects
Metrowerks 219 and C++ compilation. That is useful same-series evidence, not
proof of MHP3's original language, compiler, flags, or library ownership.

The complete pipeline matters: mwccgap and pspas feed mwldpsp and elffixup. The
configuration also explicitly patches compiler static-initializer naming and a
linker section-size check. Its
[object conversion](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/tools/fixup_elf.py)
changes a PC16 implicit relocation value and selected section alignments. These
are declared intermediate transformations, not evidence that arbitrary ELF
header edits would fix our SNC crash. The project's pipeline is more than a
compiler executable with the right banner.

The build graph creates assembly and compiled objects for application C units,
then records their comparison pairing. Consequently, a successful module hash
alone cannot establish which bytes came from reviewed source. Its link rule's
failure-tolerant options also need independent gate scrutiny. We should borrow
its module organization and investigate its engine terminology while preserving
our source-participation checks and stricter failure policy. Directory labels
alone do not positively identify SDK code. MHP2G overlay field names and grouping
must remain hypotheses when compared with our differently structured MHP3 data.

## Castlevania: Symphony of the Night

The [project scope](https://github.com/Xeeynamo/sotn-decomp/blob/a6c3ef9d0189a0cc67b23d93b7b4f3abc91c5fa2/README.md)
includes a matching PSP target alongside PSX and Saturn versions. Its
[build generator](https://github.com/Xeeynamo/sotn-decomp/blob/a6c3ef9d0189a0cc67b23d93b7b4f3abc91c5fa2/tools/builds/gen.py)
uses Metrowerks C through a wrapper, an Allegrex assembler and GNU linking.
It makes overlays depend on symbol exports generated from the main executable;
this prevents stale main/overlay address assumptions. Shared source, platform
defines, and distinct module outputs offer practical organization patterns.

Important differences: source-specific optimization selection is allowed there;
our fixed-flags requirement remains unchanged. Its
[pspas adapter](https://github.com/Xeeynamo/sotn-decomp/blob/a6c3ef9d0189a0cc67b23d93b7b4f3abc91c5fa2/tools/pspas/src/main.rs)
re-emits selected VFPU instructions from annotated assembly bytes before invoking
the assembler. That supports assembly reconstruction, not C-source credit.
Neither its multiple platform targets nor its adapters establish a suitable
MHP3 renderer or native-port design.

## Hot Shots Tennis

[HST's completion contract](https://github.com/Jstar269/hst-decomp/blob/78bf721233fb2f2fb56d1e8e8420a0e280cce4c5/docs/COMPLETION.md)
distinguishes isolated function matches, whole-module source participation,
relocatable builds, and human review. This separation directly supports our
coverage reporting: a binary match, readable source and proven integration are
different claims. Its documented shifted-build runtime requirement is stronger
than static relocation checking; neither substitutes for runtime evidence.

The [MW build driver](https://github.com/Jstar269/hst-decomp/blob/78bf721233fb2f2fb56d1e8e8420a0e280cce4c5/toolchain/drivers/mwcc_wibo_link.py)
hash-checks tools, rejects unresolved symbols and unplaced data, links with
psp-ld, and validates the complete function symbol's address and size before
extracting bytes. These are useful failure-control examples, not proof that our
required 18 negative checks are already covered.

Differences matter: its contract includes reconstructing Sony modules and permits
a narrowly declared inline-VFPU exception. Our library-assembly policy does not
change. Its associated Nakagawa hybrid port fills unmatched functions through
static recompilation and a host runtime. That is distinct from the all-source
port we have chosen to begin only after matching. Separating host system calls
from game code is useful later; adopting that runtime is not decided here.

## Yu-Gi-Oh! Tag Force 5

The [module-focused project](https://github.com/angelof-exe/ygo-tf-5-decomp/blob/712c18b3078f0fd4d969bd992ddabea6debe78ca/README.md)
offers another small PSP-module workflow. Its
[relocation-aware diff](https://github.com/angelof-exe/ygo-tf-5-decomp/blob/712c18b3078f0fd4d969bd992ddabea6debe78ca/scripts/mwcc_diff.py)
accepts matching relocation symbols/kinds without comparing the full instruction
word on that path, and separately handles known baked addresses. Such a diff can
help diagnose object output; its MATCH result does not prove final linked bytes
or even unchanged non-relocation instruction bits. We should retain our complete
byte comparison after explicit supported relocation resolution. Its small-module
scope is a useful pilot pattern, not evidence for our executable-wide gate.

## Bounded next investigation ideas

1. Prioritize a read-only MHP2G/MHP3 pipeline and structural comparison: overlay
   descriptors, initializer hypotheses, ABI conventions and same-shaped routines.
   Record contradictions as carefully as similarities; do not import flags or
   infer exact compiler attribution from a small match.
2. When a reconstruction bucket is approved, review a per-module source/assembly/
   library manifest and main-export dependency graph, with deliberate gate
   failures. Preserve unknown ownership and deferred runtime status explicitly.
3. Treat alternative documented linker pipelines as provenance leads for a future
   approved synthetic experiment. None of these inspected implementations provides
   a verified fix for our SNC access violation. Targeted public searches for its
   exact exception/alignment messages produced no usable primary-source diagnosis.
   Do not patch inputs or substitute linkers under the frozen 3E/3F profiles.

This research grants no matching credit or toolchain lock and authorizes no wider
overlay recovery, hardware replacement or port implementation. Subsequent
approved investigations are recorded in `BUCKET_PLAN.md`.

## Yakumo: user-requested same-game reference

Reviewed snapshot: [TeamGDB/Yakumo, b61852ae](https://github.com/TeamGDB/Yakumo/tree/b61852aef10870400320b96d92a14136ac17b051).
Seven public text files and their hashes are retained in
`evidence/yakumo-review/source-manifest.json`. No Yakumo code was run or installed.
Repository instructions and reported results are reference material.

Yakumo translates PSP machine instructions into host C++ and supplies a PSP
runtime. Its [input profile](https://github.com/TeamGDB/Yakumo/blob/b61852aef10870400320b96d92a14136ac17b051/profiles/mhp3rd/config/mhp3rd_npjb40001.toml)
pins HD NPJB40001, decrypted ELF SHA-256
`55c0598436c0753b04331f8e95d406f832d9217806e3a896fed0e88b33637d8c`.
Our PSP v1.02 reference is different. Generated host C++ does not recover the
original source or identify its compiler; the reviewed sources provide no new
original compiler executable or reproducible original-toolchain build.

The user's observation that HD is largely the PSP game with enhanced graphics
is consistent with this profile: the PS3 release embeds a PSP image, and Yakumo
recompiles that PSP executable. This makes it a close same-game reference, not
an unrelated native PS3 engine. The caution here concerns exact release bytes,
addresses, expanded memory layout and archive contents. It does not imply that
all gameplay code or data formats were rewritten. Measuring corresponding
functions across verified clean releases would distinguish shared code from
release-specific changes; that comparison has not yet been performed.

| Finding | How it can help us | Limit |
| --- | --- | --- |
| [Archive documentation](https://github.com/TeamGDB/Yakumo/blob/b61852aef10870400320b96d92a14136ac17b051/docs/DATA_BIN.md) describes the two seed defaults and the 64-byte MWo3 header. | Independent same-game corroboration of archive/key semantics and header fields; useful cross-check before broader recovery. | HD uses 6043 entries, block-table end `0x5E70` and a 328-byte trailer; our PSP evidence has 5955, `0x5D10` and 680 bytes. Its last two address fields also remain described provisionally. |
| [Overlay loader](https://github.com/TeamGDB/Yakumo/blob/b61852aef10870400320b96d92a14136ac17b051/profiles/mhp3rd/host/overlays.cpp) distinguishes image starts from capacities and handles images extending across another listed start. | Supports keeping our twelve shared starts separate from unproven disjoint slot bounds; suggests cases for later loader validation. | HD addresses and observed overlay coverage are not PSP measurements. |
| The loader hashes header/code identity and unregisters replaced functions. | A concrete stale-overlay failure case to address when runtime work is approved. | Its FNV identity check is neither our full-byte comparison nor proof of source participation. |
| [Architecture](https://github.com/TeamGDB/Yakumo/blob/b61852aef10870400320b96d92a14136ac17b051/docs/ARCHITECTURE.md) separates reusable execution services from title-specific layout, graphics, audio and input. | A useful boundary for later separating hardware dependencies from recovered game code. | It is a machine-code execution framework, not an architecture already selected for our source port. |
| The architecture reports interpreted addresses and offers `PSPRECOMP_NO_INTERPRETER=1`. | Explicit fallback detection is a useful future coverage lesson. | Even a successful strict run covers only exercised paths and cannot establish all-module byte equality. |

The [overlay conversion tools](https://github.com/TeamGDB/Yakumo/blob/b61852aef10870400320b96d92a14136ac17b051/profiles/mhp3rd/tools/add_overlay.py)
check the load address and calculate stored image length from header, code and
data. The [ELF wrapper](https://github.com/TeamGDB/Yakumo/blob/b61852aef10870400320b96d92a14136ac17b051/profiles/mhp3rd/tools/wrap_overlay.py)
then marks the whole supplied blob executable and inserts ELF flags `0x10A23001`.
That is an analysis container, not recovery of original section boundaries or
new compiler-attribution evidence.

Its [README](https://github.com/TeamGDB/Yakumo/blob/b61852aef10870400320b96d92a14136ac17b051/README.md)
reports PSP saves, downloaded quests, right-stick controls and Windows/Steam Deck
support. These provide later implementation leads for requirements we already
settled; they were not independently tested here. Renderer, input library,
analog camera behavior, interpolation and other enhancements remain unselected.
Finish matching all original game code before port implementation remains the
user's decision. The next useful action from this review is a separately planned
PSP archive/overlay cross-check, not adopting HD addresses or beginning a port.
