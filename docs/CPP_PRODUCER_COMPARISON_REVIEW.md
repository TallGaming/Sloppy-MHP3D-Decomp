> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Invented C++ producer comparison — Bucket 3W

This compares compiler conventions using one invented translation unit. It
compares no original function bytes and grants no source-match credit. It does
not revise the parked initializer, select an original compiler or establish a
historical C++ ABI from resemblance alone.

## Source and fixed-profile review before compilation

`bench/cpp_static_producer.cpp` is natural C++98-compatible code with purpose
comments: a polymorphic base and derived class, out-of-line constructors and
destructors, distinguishable virtual value methods, an externally visible
static-lifetime derived instance, and a C-linkage function that dispatches
through a caller-supplied base pointer. An opaque C-linkage event hook makes
construction/cleanup observable without SDK headers or a runtime harness.
Its source is 1,699 bytes, SHA-256
`fb88cb5c8f7be2b0f7a4cb83ac994789c3f88e3a2b49726e81d476a437426423`.
No original code or target-specific offset/default occurs in the fixture.

The declared profiles retain their installed tool/dependency identities and
existing O2 pipelines. MW219 changes only the existing `-lang c` selection to
`-lang c++`; GNU1.7.1 selects its already pinned cc1plus; SNC retains its driver
flags and uses the `.cpp` source extension. The GNU backend continues to bypass
the SDK driver and uses the same explicitly pinned modern diagnostic assembler.
This is not a recreation of three complete historical SDK builds. No RTTI,
exception, destructor-registration, inlining or ABI option is normalized across
families, and no per-function flag selection occurs.

The profile is `config/cpp-producer-comparison.json`, 4,052 bytes, SHA-256
`9f2616d9c2a2d19b1064448df671569cd07e94f49713982748fbe02204b2a339`.
It pins the source, inherited profiles/pipeline/dependencies, ELF parser,
read-only decoder and six parked-source/assembly records. Two fresh trials
compile all three declared families without linking or executing outputs.

The source naturally requests initialization, cleanup, virtual-table and
symbol machinery, but optimization may inline, combine or omit particular
helpers. Absence of a named helper is not a compilation failure. Unresolved
external/runtime relocations are recorded without masking or applying them;
they are expected in relocatable fixture objects and are distinct from the
strict original-function byte comparator's requirements.

Pre-compilation review requested stronger output integrity: snapshot complete
objects, reject output links/nonregular files and recheck every emitted object
after later invocations and before publication, including partial failures.
The primary implemented those checks before any compilation, added explicit
uninterpreted decoder failures/timeouts, conservative relocation-place bounds
and code-only declared function-extent status. The reviewer read back and
approved the corrected fixed driver, 12,749 bytes, SHA-256
`7e0031c88b287f33b8ca5778d3b5fe99bb2fc7f4a284ad229a051401ee6dda74`.
The source and profile remained unchanged. Retained outcomes follow separately.

## Retained outcomes and independent audit

Both approvals preceded the freeze at `2026-10-31T07:11:51.621659+00:00`.
`evidence/bucket-03w/profile-freeze.json` is 867 bytes, SHA-256
`43d5d003eabdb0aeacc8b45a67a5b61be00051006da50ee22f8757858caad7f2`.
Its source/profile/driver identities still match the approved bytes.

Both fresh directories, `build/cpp-producer-d93lhtl0` and
`build/cpp-producer-st8kopk6`, contain complete successful objects for all three
profiles. The reviewer independently compared all six objects byte for byte
within each family, rechecked section metadata and declared function extents,
and matched retained decoder streams to their report hashes. All decoders exit
zero without stderr. No relocation was applied or hidden.

| Fixed profile | Complete object bytes | SHA-256, identical in both trials |
| --- | ---: | --- |
| MW219 C++ O2 | 6,528 | `406ea0e4105f271d4e6f81d142393d22e3b59b72542a0ed15ebe3bf6b85b004f` |
| GNU1.7.1 cc1plus O2 | 6,312 | `a8848c362e49c88129ef5373529cfbe9c86c6233d220bcd6d27928c7de3017d9` |
| SNC1.2.7503.0 C++ O2 | 2,456 | `82075727f9e18b68f997b74ebd6e02172b319db60fc791474b4edb6242b8af59` |

The two reports are 151,742 bytes each. Their SHA-256 values are
`8de502ddf10831f1e5e3bd7f4ab437f689c630002bc82ac2826fa952b8f7902c`
for `evidence/bucket-03w/trial-1.json` and
`c77d626849e26c6983f5823d6d5077f7d02995984fa583b607404f714c7ac446`
for trial2. Build-directory paths differ; per-family object bytes and captured
producer conventions reproduce exactly.

## Observed producer conventions

MW219 emits classic `__ct__`/`__dt__` class symbols, `.vtables`, `.ctor`,
`.init`, `.mwcats` and exception metadata. Its 64-byte `__sinit_` function
directly calls the derived constructor, then references
`__register_global_object` with object/destructor/record arguments. The initializer
symbol retains filename-dependent padding from the unmodified compiler. Each
fixture vtable symbol is sixteen bytes; relocations identify RTTI at offset0,
the destructor at8 and value method at12. Duplicate `.text` and `.vtables`
section names are preserved with their distinct indexes.

GNU emits Itanium-style `_ZN...` class symbols, C1/C2 constructor aliases and
D0/D1/D2 destructor forms, RTTI/name symbols, `.ctors` and `.dtors`. A
124-byte `_Z41__static_initialization_and_destruction_0ii` implements the
selector/priority dispatch. Its 32-byte initialization and cleanup wrappers
pass `(1,65535)` and `(0,65535)`, respectively. The body reaches constructor or
destructor through relocations; local section-relative jumps remain unresolved
object facts. Each `_ZTV` symbol has a declared twenty-byte extent in a
24-byte allocated section, with RTTI/destructor-pair/value relocations at
offsets4/8/12/16. Section allocation is not silently substituted for symbol size.

SNC emits `__0o...` constructor/destructor names, `__0f...` virtual method names,
24-byte `__vtbl` symbols and `__cplinit`. Its 44-byte `__sti__` directly calls
the derived constructor, then references `__record_needed_destruction`.
Its two table relocations are at offsets12 and20. No GNU-like two-int
selector/priority wrapper is present in this fixture's captured symbols/code.

These observations use raw symbols, instruction sequences and relocation
targets together. Zero-valued words in relocatable tables are placeholders;
they do not establish a missing RTTI pointer or a no-RTTI compiler option.
Object size differences include metadata, alignment and different conventions;
they are not quality rankings or original matching scores.

## What this changes, and what it leaves open

Among these three installed producers under their exact declared defaults, the
GNU frontend alone emits the wrapper/selector/priority convention already
observed in the bounded original 3V unit. MW and SNC produce different
initialization/destructor-registration machinery on this common fixture. This
is stronger evidence for prioritizing GNU-compatible C++ initialization than
the isolated argument pair was, while remaining a bounded family comparison.

No original bytes were compared in 3W, and no neighboring original constructor
bodies were added to the 3V scope. The fixture differs from that original unit
in event side effects, source context, class members and options that remain
unidentified. Other compiler versions, vendor modifications, shared ABIs,
mixed producers and runtime/library units are not excluded. Names/sections may
also be stripped or combined during a real link. The diagnostic GNU assembler
contributes metadata and is not a historical PSP pipeline lock. No new flags,
compiler selection, source integration, runtime validation or match credit
follows automatically. The parked routine and its preserved drafts remain
unchanged; this helper invoked no compiler or executable fixture.
