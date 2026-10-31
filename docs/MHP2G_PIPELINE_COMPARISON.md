> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# MHP2G pipeline comparison

Bucket 3G, 2026-10-30. This is a read-only comparison of public source at
`tclamb/mhp2g-decomp` commit `5b98acfd014090b07c81e6b17f376a5eba986083`
with existing local evidence. No candidate was provisioned or executed; no
compiler, linker, flags, source, reference bytes or prior results were changed.
External configuration describes a reconstruction project, not recovered original
Capcom build instructions. Its target is ULJM05500, whereas ours is ULJM05800 v1.02.

## Stage-by-stage evidence

Labels: **local** means observed in our pinned files/prior artifacts;
**external** means verified in the linked public source; **unknown** means not
established by either. Similarity is a hypothesis until supported for MHP3.

| Stage | Confirmed external pipeline | Comparison and limit |
| --- | --- | --- |
| Compiler | [configure.py](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/configure.py#L62) selects C++, O4,p, inline level 8, small-data threshold 0, RTTI/exceptions off, no loop unrolling and explicit zero data. Its scratch profile names build 219. | **Local:** our MW219 is unmodified and used as C in the frozen experiments. The public choice neither proves original MHP2G C++ nor selects MHP3's language/flags. |
| Compiler identity/patch | [patch_toolchain](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/configure.py#L890) recognizes compiler SHA-1 `3dc756594b1a46d27203c27a3c38e7c868eb3419` and changes static-initializer filename handling. | **Local:** that SHA-1 exactly matches our existing raw MW219 EXE. Its SHA-256 is `828f9b30b3ae33c7a0202c2baf48aab49884c60e48c5b3daa2436bc3237368df`; recorded help identifies 3.0.1 build 219. **Unknown:** external post-patch binary digest and runtime behavior. A conditional pre-patch guard is not a universal binary verifier. |
| mwccgap | Gitlink pins [459c02bb](https://github.com/mkst/mwccgap/blob/459c02bbca288b91cc84a7be4027022d654f6e4d/mwccgap/mwccgap.py#L21). It compiles source, handles unresolved INCLUDE_ASM through placeholders, assembles declared assembly and transplants its code/data/relocations. With no missing assembly it returns the raw compiler object. | **Local:** our probes compile directly and contain no assembly fallback. This wrapper is not a general assembler conversion of ordinary compiler output. Its reconstructed initializer symbol names and mixed-source provenance would require separate accounting. |
| pspas wrapper | The gitlink pins [SOTN a13e7cad](https://github.com/Xeeynamo/sotn-decomp/blob/a13e7cad31aa3f8bb7947f472ef8109207b28ae1/tools/pspas/src/main.rs). The [MHP2G patch](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/sotn-decomp-pspas.patch) extends VFPU recognition and changes the backing assembler to `mipsel-linux-gnu-as`. Annotated VFPU bytes become `.word` directives. | This is a source-built Rust adapter, not Sony's same-named assembler. The [mwccgap assembler](https://github.com/mkst/mwccgap/blob/459c02bbca288b91cc84a7be4027022d654f6e4d/mwccgap/assembler.py#L29) receives ABI 32; the separate retained-assembly rule requests EABI and disables section padding. Do not collapse these distinct paths into one assumed original ABI recipe. |
| Object conversion | The separate assembly rule invokes [fixup_elf.py](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/tools/fixup_elf.py): REL PC16 implicit `0xffff` becomes zero; selected section alignments become 4. | The ordinary `cc` rule does not universally invoke this fixup. **Local:** no such transformations were applied to our frozen objects or reference. It is not evidence for repairing the SNC access violation with header edits. |
| Linking/layout | [Generated LCF and arguments](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/configure.py#L580) specify main sections, constructor ranges and overlay outputs. The rule invokes `mwldpsp.exe` through wibo. | **Local:** 3E/3F used SNC `pspld`, a different executable. The common main text base is a layout agreement, not exact linker identification. MHP2G's overlay addresses/counts do not transfer. |
| Linker patch/finalization | The linker patch recognizes SHA-1 `40e4eb915d5ff9a719fe79542045a0bf9df3f819` and disables a section/symbol-size check for reporting symbols. EBOOT then passes through binary `elffixup.exe`. Module SHA-1 checks precede progress reporting. | **Unknown:** publicly verified linker version, complete binary identities, elffixup transformation details and historical-game provenance. The failure-tolerant link options and preliminary `touch` require scrutiny; module checks do not prove source participation. |

## Availability, metadata and contradictions

The public [archive checksum](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/bin/mwccpsp_219.tar.gz.sha256)
is `62ec4faa807ad5afaefa7c92de6423505072c321fad13c071c2f640e9820b5c8`.
Our archive SHA-256 is `81a2a8664d779901f6fa2f298b663b4b0feeb1d7f6613fd14531f51e66926d78`.
That container difference does not contradict the exact compiler-file SHA-1
agreement. It does mean that the archive itself must not be claimed identical.
The [dependency action](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/.github/actions/get-dependencies/action.yml)
uses a private repository/cache; its public script is not public availability or
an independently pinned supply of linker/elffixup binaries. Python requirements
also include ranges rather than a complete environment lock.

**Local evidence:** `config/compiler-candidates.json` and
`config/compiler-families.json` retain diagnostic C profiles, not a selected game
toolchain. GCC uses a pinned modern GNU assembler; SNC uses its bundled pipeline;
MW uses direct compiler output. `config/synthetic-link.json` pins SNC pspld
SHA-256 `46e6068518d96fd8b3d7ffe3e7ab0f1aa1c7e85f580a9f32de0aa65ac7daf534`.
Both frozen 3F layouts failed in both trials, without output ELFs. A different
project's successful MW pipeline supplies no diagnosis of that bounded failure.

Our accepted linked ELF has flags `0x10A23001` and comment strings
`MW MIPS C Compiler (2.4.1.01)` / `PSP`; MW219 O2 diagnostic output is relocatable,
flags `0x10970001`, comment `MW MIPS C Compiler (3.0.0)`.
These stage differences remain unresolved. No inspected public source proves
which tool writes our linked comment/flags. Compiler identity, wrapper behavior,
linker behavior, finalization and original-game attribution are separate claims.
See `COMPILER_ATTRIBUTION.md` and `LINKER_FAILURE_ISOLATION.md` for prior evidence.

The assembly/compiled comparison pairs and per-module checks are useful design
examples. They do not establish reviewed source integration, positive library
ownership, our required negative gate, runtime behavior or port readiness.
The MHP2G LCF's constructor-range names are hypotheses for our overlay's raw
fields `0x18`/`0x1C`; our field semantics remain unknown.

## One proposed future experiment — not executed

Isolate the language front end using the **existing unmodified MW219**, unchanged
fourteen-probe source and a single O2 pair: the existing C invocation versus the
same invocation with only `-lang c++` replacing `-lang c`. Do not import MHP2G's
optimization, inline, exception, RTTI, wrappers or patches.

Before execution, independently review and freeze the source/manifest/compiler/
runner hashes, exact commands, fresh-output policy, C++ symbol-to-probe mapping
and complete-function comparison rules. Establish the naming rule with an
invented naming fixture before examining target scores; do not discover aliases
from whichever target result looks favorable. Require all fourteen functions, unique
symbols and supported relocations; reject the entire configuration on compile
failure, missing/ambiguous functions, unexpected code relocations or stale output.
Preserve original evidence. Repeat both cases in fresh directories and audit
complete object/function hashes; report per-function differences without pooling
settings or changing source after results.

This tests whether the chosen language front end changes current diagnostic
code generation. Identical bytes would make these probes non-discriminating;
different bytes would establish a controlled mode effect. Neither extra exact
matches nor a failure confirms or refutes MHP3's original language/toolchain.
These C-compatible isolated bodies do not recreate class methods, inlining or
translation-unit context. No linking,
new candidate, match credit or port work belongs in this experiment. It requires
its own approved bucket; Bucket 3G ends with this proposal.
