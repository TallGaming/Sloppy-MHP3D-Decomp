> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# MHP3 and MHP2G: bounded structural comparison

Bucket 3G, 2026-10-30. **The existing MHP3 archive/overlay evidence has useful
structural counterparts in MHP2G; it does not establish a shared compiler,
original class layout or matched game function.** This review reads existing
MHP3 artifacts and public text at MHP2G commit
`5b98acfd014090b07c81e6b17f376a5eba986083`. It executes no public parser/build
script, performs no new disassembly or Ghidra analysis, and recovers no new game
payload. Public reconstruction declarations are evidence about that project's
implementation, not an independently rebuilt MHP2G original binary.

## Inputs and strength of claims

MHP3 evidence is the accepted PSP ULJM05800 v1.02 ELF, Bucket 1 map, Bucket 2
`movie_task.ovl` payload/report, unchanged fourteen-probe manifest/source, and
the previously completed Bucket 3B Ghidra export. Relevant existing explanations
are [EXECUTABLE_MAP.md](EXECUTABLE_MAP.md), [ARCHIVE_FORMAT.md](ARCHIVE_FORMAT.md)
and [PROBE_MISMATCH_DIAGNOSIS.md](PROBE_MISMATCH_DIAGNOSIS.md).

The ELF is 2,247,320 bytes, SHA-256
`755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950`.
The sole recovered overlay is 1280 bytes, SHA-256
`6a918f7af824103cfe5df0c4fb8d793c430a273b166a8eaf5ce1e5cd66951abb`.
The reviewed Ghidra export is 68,494 bytes, SHA-256
`a2957127574e6791345caee470056ca1a64a7fe218335492ee4f291e3db8a091`.
The helper reread these bytes/metadata, checked all fourteen target hashes
against existing ELF intervals, and read the existing exported hypotheses.
These operations are read-only; they add no function or behavior coverage.

The helper independently verified the 32 input pins and 22 public-text pins in
the primary's final manifests. `evidence/bucket-03g/comparison-inputs.json` is
11,723 bytes, SHA-256
`40d06cf5dbd324202b24a4126ce1924a782fc773c6f3ae0ba0bef2e2d53dc514`.
Its recorded ELF/header values, fourteen target hashes, identical prior Ghidra
exports and local MW219 identity agree with separate byte reads. The local
compiler's SHA-1 also equals the MHP2G script's pre-patch guard, which identifies
that tool input, not the compiler used for every original game unit. No patch
was applied. The last performed suite remains the retained Bucket 3F run.

## Overlay container: shared layout, different contents

MHP2G's pinned [header parser and linker declarations](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/configure.py)
describe the same 64-byte, little-endian MWo3 layout that Bucket 2 independently
observed in MHP3. Its generator also checks total stored size as header plus
text and data; BSS is absent from the stored payload.

| Field or relationship | Existing MHP3 pilot evidence | MHP2G comparison and limit |
| --- | --- | --- |
| Magic/name | MWo3; `movie_task.ovl` | Same format/name convention; not identical code |
| Header words through `0x14` | ID, load address, code/data/BSS lengths | Same declared order and widths |
| Stored size | `0x40 + 0x488 + 0x38 = 0x500` | Same size equation |
| Initial text padding | Bytes `[0x40,0x80)` are zero | Parser requires this padding; agreement on this one payload only |
| Reservation | `0x500 + 0x80 = 0x580` | BSS treatment agrees structurally |
| Pilot load | `0x09C57C80` | MHP2G task declaration uses `0x09A5A580`; do not transfer addresses |
| Task contents | Code reaches file offset `0x4C8`, then `0x38` data | MHP2G's movie configuration begins its data subsegment at `0x480`; internal boundaries differ |

The pinned [MHP2G movie configuration](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/config/task/movie_task.splat.yaml)
also ends stored bytes at `0x500` and declares BSS `0x80`. Equal total size,
name, padding and BSS do not establish byte equality or function correspondence.
No MHP2G game payload was obtained or compared here.

MHP3's header ID 158 agrees with program-header index 158, while the named
zero-sized descriptor is section 337. That selected association is supported
by load address and the uniquely corresponding `0x580` reservation. The public
MHP2G linker writes an overlay ID, but this does not prove the ID/index rule for
every MHP3 descriptor or establish runtime lifetimes.

## The two disputed words are still hypotheses

MHP2G names header words `0x18` and `0x1C` as the start/end of a static
initializer range. Its linker emits `.ctor` boundaries there. Its
[configuration generator](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/tools/generate.py)
uses a nonempty range to locate a pointer to initialization code, and its
[ctor extension](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/tools/splat_ext/ctor.py)
treats the region as function-address words. These are a specific, testable
alternative to treating either word as a single callable entry point.

Our recovered header has **both words equal `0x09C58180`**, exactly
`load_address + stored_length`. Under the MHP2G interpretation this is an empty
initializer interval at the stored-byte end. That is consistent, but provides
zero nonempty initializer entries to inspect and no observed loader invocation.
It cannot distinguish an initializer boundary from every other end-marker
interpretation. Existing parser labels `end_address`/`entry_address` remain
provisional; no production field rename or new call target is justified here.

## Archive routines: stronger bounded analogues

MHP2G's [FileSys source](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/src/eboot/file_sys.cpp)
contains concrete seed, key-update and buffer-decode bodies. They split a
32-bit seed, substitute nonzero defaults `0x7F8D`/`0x2345`, update the low/high
states modulo `0xFFF1`/`0xFFD9`, substitute bytes and XOR each word with the
combined state. These steps agree with the **already reviewed** MHP3 loader
observations at `0x0886233C`, `0x08862700` and `0x08862808`–`0x08862888`.
The [standalone archive reader](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/tools/data-extractor.cpp)
implements the same family of transformation and adjacent-block size fallback.

This is a bounded algorithmic analogue with public source bodies, not merely
similar function names. It still establishes neither byte identity nor original
language, compiler flags, class receiver, ownership or source translation unit
for the MHP3 routines. The public code has not been compiled as MHP3 source.

| Directory property | MHP3 existing loader evidence | MHP2G source declarations |
| --- | ---: | ---: |
| Payload entries | 5955 | 6602 |
| Block-start words, including end sentinel | 5956 (`0x5D10` bytes) | 6603 (`0x672C` bytes) |
| Exact-size pairs | 1289 (`0x2848` bytes) | 812 (`0x1960` bytes) |

The count differences alone prohibit copying the foreign index layout. MHP3's
680-byte uninterpreted directory tail remains unknown. Neither the public
decoder nor agreement on this one overlay proves that every archive entry uses
the same content format or requires no decompression.

## Module groups, language and ABI

MHP2G's build organizes task/sub/enemy/stage overlay families and emits group
addresses. MHP3's map instead observes 355 zero-sized overlay descriptors at
12 shared starts; some reservation ranges overlap. Names such as `_task` and
`_sub` are useful organization clues, but MHP2G's four declared families cannot
become twelve proven MHP3 runtime slots, allocation rules or concurrency claims.
Source/assembly/library manifests should preserve unknown ownership and exact
module identities rather than importing directory-based labels.

MHP2G explicitly selects C++ and exposes virtual classes in its
[FileSysBase declaration](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/include/file_sys_base.hpp),
with virtual overrides and state in
[FileSys](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/include/file_sys.hpp).
That makes C++ engine structures a sensible MHP3 hypothesis. It does not
recover an MHP3 vtable, inheritance graph or field offsets. MHP3's stripped
ELF has neither SYMTAB nor DYNSYM; its runtime/demangler strings concerning
vtables, type information and exceptions support C++-related library presence,
not proof that a particular game unit used classes or the same ABI.

MHP3 is ELF32 little-endian MIPS, ET_EXEC, entry `0x088214C8`, flags
`0x10A23001`. The existing export uses `Allegrex:LE:32:default`; its compiler
specification is an analysis setting, not historical attribution. The ELF's
`.comment` identifies `MW MIPS C Compiler (2.4.1.01)` and `PSP`; neither string
settles language or the compiler of every unit. Existing object/link-stage
metadata differences remain unresolved rather than being normalized away. Observed
`a0` pointer arguments, `v0` results, four-byte list links and six-byte address
fields fit the previously reviewed PSP peer-list interface. They do not
distinguish free functions from compatible methods or establish exception,
RTTI, varargs, structure-return or floating-point ABI details. The MHP2G
project's type/header choices must not silently supply those missing answers.

## What the existing probes and export cannot establish

The fourteen frozen probes total only 444 target bytes; all remain ownership
unclassified and earn no full-game match credit. Existing larger probes remain
unmatched under the tested configurations. Tiny clear/copy/constant controls
can be emitted by unrelated compilers and are weak attribution evidence.

The existing export covers 34 selected functions, not the whole program. Its
six-byte reduction at `0x08830550` and list count at `0x08830654` have useful
networking context: 34 reduction call sites in 26 callers, one list-count
caller, and a neighboring copy of a six-byte field at node offset 132. The
existing SDK import identification supports that context without identifying
the local wrappers as SDK code. Auto-generated names, omitted pseudocode
arguments and inferred `int *` types remain hypotheses.

The inspected MHP2G [Net](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/include/net.hpp)
and [LobbyNet](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/include/lobby_net.hpp)
headers provide networking class names but no bounded equivalent bodies for
those two MHP3 routines. This review therefore records
**no source-level correspondence for either leaf** and does not rename them
to MHP2G methods, attribute them to an engine/library or spend another source
attempt on guessed foreign declarations.

## One proposed next experiment, not performed

The same-series C++ declarations support testing **one fixed language-mode
pair**: the unchanged fourteen-probe source and unmodified Metrowerks 219 at
fixed O2, differing only in C versus C++ mode. A separately approved plan must
freeze the pair before outputs and first validate C++ symbol mapping using an
invented naming fixture. Compare complete function symbols for all fourteen
targets or leave the entire configuration unscored; use fresh repeat builds,
with no source edits or pooling of favorable functions.

The existing probe bodies are C-compatible isolated hypotheses. This experiment
could reveal a language-mode effect on those bodies, but cannot confirm or
refute original C++ language, class layout, inlining, translation-unit context,
ownership or historical flags. It cannot resolve the overlay initializer words
or the object-versus-linked-stage gap. No naming fixture or compiler invocation
is performed or authorized by this comparison. Existing sources, settings,
library policy and matching requirements stay unchanged; the toolchain remains
unlocked. The last performed tooling suite remains 209 passing tests from
Bucket 3F; this documentation-only bucket does not claim a new test run.
