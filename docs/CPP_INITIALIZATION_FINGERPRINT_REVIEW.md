> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# C++ initialization fingerprints — Bucket 3V

Read-only comparison of primary compiler source, the pinned related-game build
and bounded original-code evidence. No compiler/game execution, new source
hypothesis or toolchain lock is part of this review. The parked archive-key
initializer remains untouched.

## Confirmed public GNU convention

The GCC mirror's `releases/gcc-3.3.3` tag resolves to commit
[`0cf7278b8ebcf154c6c9ee8977cdb1aafa599111`](https://github.com/gcc-mirror/gcc/tree/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111).
The reviewer fetched exact commit URLs and retained small line-numbered excerpts
with complete-source and excerpt hashes in
`evidence/bucket-03v/helper-map-public-sources.json`. These are upstream source
facts, not proof of PSP vendor modifications or a source-to-binary build.

[`gcc/cp/decl2.c:2232–2269`](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/cp/decl2.c#L2232)
defines a generated static initialization/destruction function taking two ints:
initialization selector and priority. Its generated conditional combines the
appropriate selector value with a priority equality test
([lines 2458–2473](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/cp/decl2.c#L2458)).
The constructor wrapper passes selector one and its priority
([lines 2681–2749](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/cp/decl2.c#L2681)).
This directly explains a two-stage wrapper/guard shape with arguments
`(1, 65535)` when default priority is used; it does not prescribe a particular
MIPS instruction schedule, prologue, optimization setting or exact output size.

[`gcc/tree.h:1617`](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/tree.h#L1617)
defines the default priority as 65535. The compiler's file-function naming
machinery uses the `_GLOBAL__%s_%s` form
([`gcc/tree.c:4400`](https://github.com/gcc-mirror/gcc/blob/0cf7278b8ebcf154c6c9ee8977cdb1aafa599111/gcc/tree.c#L4400));
the C++ frontend selects initialization/destruction letters I/D. This supplies
a source-backed interpretation of corresponding symbols if actually observed;
no stripped original symbol is recovered merely by giving a routine that name.

## Related Metrowerks evidence and discrimination limit

Pinned MHP2G commit
[`5b98acfd014090b07c81e6b17f376a5eba986083`](https://github.com/tclamb/mhp2g-decomp/tree/5b98acfd014090b07c81e6b17f376a5eba986083)
uses the MW219 pipeline. Its
[`configure.py:890`](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/configure.py#L890)
describes and conditionally patches `__sinit_` filename-symbol construction for
the raw executable fingerprint matching our unmodified MW219. Its
[`ctor.py`](https://github.com/tclamb/mhp2g-decomp/blob/5b98acfd014090b07c81e6b17f376a5eba986083/tools/splat_ext/ctor.py#L6)
labels the reconstructed pointer section as references to `__sinit_` routines;
the generated link layout brackets `.ctor` with header initialization bounds.

Those files establish related-project symbol/layout machinery, not the full
Metrowerks PSP runtime ABI or its internal initialization-wrapper arguments.
This review found no primary MW source establishing that `(1, 65535)` is either
required or impossible there. Thus the convention is positively documented for
GNU, while exclusivity across vendor frontends remains unproved. An ABI or
runtime convention can be shared, linked from another toolchain or implemented
explicitly; section names and initialization behavior alone cannot classify all
game translation units.

## Bounded original evidence

Bucket 3T already verified `P_v00.ovl` entry4590's initialization-table word
pointing to `[0x09E7D134, 0x09E7D144)`. That wrapper sets arguments one and
65535, then tail-jumps to `0x09E7D0E0`. Its full sixteen-byte SHA-256 is
`99c966228bfb1cd9b8917afea85e03e0d0820c1cb74f0bb6979e437e2663d0d4`.
The new static-dispatch body `[0x09E7D0E0, 0x09E7D134)` is 84 bytes, SHA-256
`758b0cf81404423292dff5887436a2b265ecd241254230fe5fe67f035b4474d5`.
The reviewer independently checked every selected instruction against the
verified 1,024-byte recovered payload. Selector one plus priority65535
tail-dispatches to `0x09E7D000`; selector zero plus that priority tail-dispatches
to `0x09E7D084`. Other inputs return. Both dispatched paths supply
`0x09E7D380` as the object pointer. The combined wrapper and selector/priority
guard agrees closely with the documented GNU frontend construction; it remains
a compatibility fingerprint rather than an exclusive identification.

The two further permitted bodies have tighter boundaries than the preliminary
windows retained by the primary:

| Exact body, exclusive end | Bytes | SHA-256 |
| --- | ---: | --- |
| Initialization target `0x09E7D000–0x09E7D038` | 56 | `5b8f5c4a2ac23cef2737578c93d3f8df0e67233b9995062c4a0ce6361bb64ade` |
| Zero-selector target `0x09E7D084–0x09E7D098` | 20 | `3174d0930588de9f6794c9cb32d44339e77f01a4b425685fbcc6ab8096cb5357` |

The initialization body saves the object pointer across a call to `0x09C344C0`,
then stores `0x09E7D208` into its first word and returns. The zero-selector body
stores the same pointer and tail-jumps to `0x09C34508`. Their last delay slots
are included. The external callees and adjacent bodies were not inspected.
The 132/92-byte preliminary extracts contain neighboring code; those larger
lengths must not be reported as these functions' boundaries.

The object address is exactly the declared BSS start. A bounded data observation
at `[0x09E7D200, 0x09E7D238)` has two zero words before the stored pointer's
address point, followed by twelve code-address words. Its first is the selected
zero-selector target, and its next points at an uninspected neighbor. This is
consistent with constructor/destructor updates of a virtual-table pointer;
zeros alone neither establish a no-RTTI option nor classify its producer.

## Embedded runtime names and attribution limits

The reviewer independently repeated the declared exact byte queries over the
main ELF and all355 verified recovered overlay payloads. The only three hits
are NUL-terminated names in the main ELF: `St9type_info`,
`N10__cxxabiv117__class_type_infoE`, and
`N10__cxxabiv120__si_class_type_infoE`. The declared prefixes, including
`__sinit`, `_GLOBAL__`, `__static_initialization`, `__cxa_` and `__gxx_`, have
no hits in this bounded image set. This establishes only the queried byte-string
inventory, not the absence of stripped routines, unqueried names, other code
modules or mixed-toolchain units.

The independent runtime provenance review locates all three exact names in an
available GNU `tinfo.o`. Consequently a linked runtime can account for these
strings without establishing the compiler for surrounding game code. Refer to
`BUCKET_03V_VALIDATION_NOTES.md` for that object's complete identity and archive
provenance. The existing MW219 directory contains no ABI manual, only the EXE
and its license DLL. Retained compiler help's GCC3.x compatibility statement
concerns dependency-file naming; it does not document the C++ runtime ABI.

The complete static evidence is
`evidence/bucket-03v/cpp-fingerprints.json`, 3,519 bytes, SHA-256
`91089e4d4e13ae79f6c08cdedaf9a22067ba240aa9f69e9e3ed4643fb85f5329`.
The reviewer checked the three exact bodies and delay slots, payload/table
hashes, BSS relationship and complete declared query inventory without running
the original game or any compiler. Together the evidence warrants investigating
GNU-compatible C++ initialization, not selecting GNU for all units or rejecting
MW/SNC. No historical compiler build, shared ABI exclusivity, runtime ownership
or fixed global profile is established, and no function receives match credit.
