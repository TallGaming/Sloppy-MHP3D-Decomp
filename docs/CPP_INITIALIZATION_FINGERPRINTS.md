> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Original C++ initialization fingerprints

Bucket 3V, 2026-10-31. The sampled `P_v00.ovl` contains a concrete static-object
initialization/cleanup pattern. This supports readable C++ for this sampled
unit; it does not establish one compiler, version or profile for all game code.
No compiler or game was executed and no source draft was changed.

## Three selected original bodies

The earlier callback at `0x09E7D134` passes `(1, 65535)` to the 84-byte selector
`[0x09E7D0E0, 0x09E7D134)`. That selector dispatches only when its second
argument equals 65535. A first argument of one selects `0x09E7D000`; zero
selects `0x09E7D084`; other values return. Both dispatches replace the first
argument with the same address, `0x09E7D380`.

The initialization target is **56 bytes**, `[0x09E7D000, 0x09E7D038)`: it calls
`0x09C344C0`, then stores `0x09E7D208` into object offset zero. The cleanup target
is **20 bytes**, `[0x09E7D084, 0x09E7D098)`: it stores the same value then
tail-jumps to `0x09C34508`. The external callees were not inspected. The static
object address equals the selected image's exact stored end and declared BSS
start; its declared BSS has 128 bytes. No complete object size or original
class/name declaration follows from that region size.

Two preliminary disassembly windows were initially 132 and 92 bytes, extending
up to the next requested range. Return/tail-jump inspection reveals neighboring
methods inside them. Those windows remain retained as preliminary evidence;
the selected target extracts and semantic analysis use only the corrected 56
and 20 bytes. Neighboring bodies are not assigned to the targets or analyzed
further. This boundary correction is recorded rather than hidden.

The stored value points into declared data, where twelve code addresses follow
two zero words. The first address is the selected cleanup target. This is
compatible with a C++ vtable address point preceded by metadata words, as
described by the [Itanium C++ ABI](https://itanium-cxx-abi.github.io/cxx-abi/abi.html#vtable-components).
The zero words do not prove their source-level role, disabled RTTI, particular
compiler switches or exclusive ABI ownership. Other table entries remain
uninterpreted addresses, not newly analyzed methods.

## Producer evidence and alternatives

Pinned GCC 3.3.3 source generates initialization/destruction selectors and
wrappers using a constructor flag plus priority; its default priority is 65535.
Both the wrapper arguments and the original selector's comparisons agree with
that documented convention. Precise source excerpts, commit identities and
the related Metrowerks comparison are in
`CPP_INITIALIZATION_FINGERPRINT_REVIEW.md`.

The related MHP2G reconstruction uses MW219 and `__sinit_` symbol machinery.
Those facts do not prove that Metrowerks PSP cannot emit the observed argument
convention, nor that another compatible frontend cannot. The retained vendor
help supplies no decisive ABI rule. Thus this is **GNU-compatible producer
evidence, not exclusive GNU identification**. The main executable's Metrowerks
metadata remains separate link/runtime evidence; mixed producers are possible
but not demonstrated by these observations alone.

Exact name queries over the pinned main ELF and all 355 known recovered images
find three terminated runtime names only in the main ELF: `St9type_info`,
`N10__cxxabiv117__class_type_infoE` and
`N10__cxxabiv120__si_class_type_infoE`. No declared `__sinit`, `_GLOBAL__`,
`__cxa_` or `__gxx_` prefix query matches. This is an inventory of those literal
queries, not proof that every possible ABI/source marker is absent.

All three names also occur in `tinfo.o` inside the already pinned GNU PSP
`libsupc++.a`. A standard C++ runtime can therefore explain them without
attributing the game's translation units to that compiler. The available
`cc1plus`, CRT objects and runtime archive identities are independently checked
in `BUCKET_03V_VALIDATION_NOTES.md`. Their generic `.ctors/.dtors` sentinel
sections must not be conflated with our bounded forward-call header consumer,
which has no observed sentinel handling.

## Retained evidence and next decision

Private extracts, the exact query inventory, the bounded data window and
`cpp-fingerprints.json` are under `evidence/bucket-03v/`. The report is
3,519 bytes, SHA-256
`91089e4d4e13ae79f6c08cdedaf9a22067ba240aa9f69e9e3ed4643fb85f5329`.
Both helpers independently verify the selected bodies and keep attribution
limits explicit. No production tool or new test is added; the last full suite
remains 340 passing WSL tests with no skips from 3U.

A useful next diagnostic is one invented static-polymorphic-object C++ fixture
under the already installed compiler families, with one fixed O2 profile per
family and no flag search. Comparing emitted selectors, symbol conventions and
table layouts can test whether these fingerprints discriminate the available
producers. It needs its own reviewed/frozen plan. The archive initializer stays
PARKED, and no source-match credit or global toolchain lock is granted.
