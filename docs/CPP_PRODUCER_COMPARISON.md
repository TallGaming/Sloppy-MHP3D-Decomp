> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Invented C++ producer comparison

Bucket 3W, 2026-10-31. One natural C++98 fixture declares a polymorphic base,
derived type, constructors/destructors, an opaque external event hook, virtual
dispatch and a static derived instance. No game target is compared. Each family
uses its existing fixed O2 pipeline, changing only the declared C++ frontend or
language selection. No options are tuned to individual functions.

Both helpers reviewed exact source/profile/driver before the input freeze and
all six compilations. All three compilers produce objects without diagnostics;
each family's entire object repeats exactly in two fresh directories.

| Fixed C++ producer | Complete object bytes | SHA-256 |
| --- | ---: | --- |
| MW219 | 6528 | `406ea0e4105f271d4e6f81d142393d22e3b59b72542a0ed15ebe3bf6b85b004f` |
| GNU PSP1.7.1, GCC3.3.3 cc1plus | 6312 | `a8848c362e49c88129ef5373529cfbe9c86c6233d220bcd6d27928c7de3017d9` |
| SNC1.2.7503.0 | 2456 | `82075727f9e18b68f997b74ebd6e02172b319db60fc791474b4edb6242b8af59` |

## Observed producer conventions

MW219 emits a 64-byte `__sinit_` function, calls the derived constructor, then
references `__register_global_object` with its destructor/registration storage.
It uses classic `__ct__`/`__dt__` symbol names, `.vtables` and `.ctor` sections.
The fixture's value-method dispatch reads the function pointer at table+12.

GNU emits a 124-byte selector/priority helper, plus 32-byte initialization and
cleanup wrappers passing `(1, 65535)` and `(0, 65535)`. It emits Itanium-style
`C1/C2` and `D0/D1/D2` names, `.ctors/.dtors`, and type-name/typeinfo/table
sections. The two fixture table symbols each have a declared 20-byte extent;
their allocated sections are 24 bytes. Dispatch reads the value pointer at+8.
The default profile also emits exception-related data and unresolved runtime
references. Those defaults are observations, not inferred original-game flags.

SNC emits a 44-byte `__sti__` function, calls the derived constructor, then
references `__record_needed_destruction`. Its names use the `__0o`/`__0f`
convention. Each fixture table symbol is 24 bytes; dispatch reads an adjustment
and function address from its selected record, rather than a simple pointer-only
slot. There is no GNU-style selector/priority helper in this fixture output.

These facts use relocation records to identify calls and table entries.
Unrelocated `jal 0` labels and zero table words are placeholders, not resolved
call targets or proof that RTTI is disabled. No relocation is applied or masked.
No object is linked or executed.

## What this changes for the original sample

Among **these exact three tested default profiles**, GNU alone emits the
selector/priority convention found in the bounded original P_v00 unit. Together
with the original static-object/table observations, this justifies prioritizing
a GNU-compatible C++ producer investigation. It does not prove a particular
historical build, exclude every MW/SNC option/version or classify every game
unit. The original linked Metrowerks comment and the C++ runtime-only name
explanation remain valid separate evidence.

The invented GNU wrappers and selector are not byte-identical game reconstructions:
their bodies, sizes, scheduling and source context differ. The game source has
not been reconstructed here. We do not infer global exception, RTTI, scheduling,
small-data or inlining flags by forcing this fixture to resemble it.

## Integrity and retained outputs

Fresh directories are `build/cpp-producer-d93lhtl0` and
`build/cpp-producer-st8kopk6`. Reports and the fixed one-off driver are under
`evidence/bucket-03w/`. Each retains complete objects, compiler streams and
decoder output; report paths/logs need not match merely because objects do.

The natural source is 1,699 bytes, SHA-256
`fb88cb5c8f7be2b0f7a4cb83ac994789c3f88e3a2b49726e81d476a437426423`.
The profile is 4,052 bytes, SHA-256
`9f2616d9c2a2d19b1064448df671569cd07e94f49713982748fbe02204b2a339`.
The corrected fixed driver is 12,749 bytes, SHA-256
`7e0031c88b287f33b8ca5778d3b5fe99bb2fc7f4a284ad229a051401ee6dda74`.
The 867-byte freeze SHA-256 is
`43d5d003eabdb0aeacc8b45a67a5b61be00051006da50ee22f8757858caad7f2`.

All inherited tool/dependency, source/profile and parked draft identities are
rechecked. Earlier objects remain unchanged after later invocations and before
publication. Review closed output-link/drift, decoder-timeout and relocation/
extent validation gaps before the freeze. Independent invented-vector and
mocked-pipeline controls are documented in `BUCKET_03W_VALIDATION_NOTES.md`;
they are not new production tests or the full-game gate's negative checks.
The last full suite remains 340 WSL passes, zero skips, from 3U.

Both independent reviews are `CPP_PRODUCER_COMPARISON_REVIEW.md` and
`BUCKET_03W_VALIDATION_NOTES.md`. Matching/source-link credit remains zero,
the archive routine remains PARKED and no native-port work has begun.
