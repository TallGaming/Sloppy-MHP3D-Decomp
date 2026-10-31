> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Invented address-reuse review

Bucket 3J. This independent review invokes no compiler, linker or game. The
experiment concerns two invented C++ fixtures and does not change or add an
attempt to the frozen 3I game candidate. It supplies no game-byte matching
credit or historical language/class identification.

## Pre-output contrast

Only record grouping may differ: direct adjacent volatile word members versus
the same members within a named `KeyState` object. Both fixtures must retain the
same nonvirtual class/method signature, unsigned 32-bit seed, unknown byte
prefix of `0x1A120`, field offsets `0x1A120`/`0x1A124`, and defaults
`0x1357`/`0x2468`. These offsets/defaults are invented rather than game values.

The expected volatile access sequence is: upper store, lower store, optional
low-default store, upper reload, optional upper-default store. The low zero test
uses the masked seed local rather than rereading the lower field. Both use
ordinary unsigned split/default logic; the grouped version must refer directly
to `state.lower`/`state.upper`, with no cached pointer/reference, assembly,
register binding, helper function or changed compiler flags.

The exact sources were independently reviewed before compilation:

| Source | Bytes | SHA-256 |
| --- | --- | --- |
| `bench/address_reuse_direct.cpp` | 1058 | `9def28de2b740f255cc379e7468f54dcdbbe3be367efd442170d7ae84dcff3ae` |
| `bench/address_reuse_grouped.cpp` | 1200 | `04662faba3e8e68506928bb2d2623d25cf5e6a93f8f9fb1bde3e3dd223908094` |

Removing only `state.` from the grouped method yields the identical direct
method body. Both have the same nonvirtual `ArchiveKeyContext` owner and
`initialize_key(u32)` member signature. The inherited invented naming evidence
established raw name `initialize_key__17ArchiveKeyContextFUi`; differences in
these data members do not change that declared signature. The fixture names do
not claim the game's original class or reuse its field layout.

The prefix is divisible by four, the word-width checks require four bytes, and
the partial record extent is `0x1A128` in both cases. The grouped state extent
check requires eight bytes; no base/virtual member, cached address or callable
helper is added. This source/layout contrast is approved.

## Profile and interpretation preflight

Before any fixture compilation, review approved `config/address-reuse.json`,
1508 bytes, SHA-256
`5818d2a39d9c8fcd6917bcdb6ed5e071f7626f1f41b8c9576e766ceee0333bf4`,
and `scripts/bench_address_reuse.py`, 15748 bytes, SHA-256
`a718dc588c552f3f20172eb505795faa6d27bbca7079b3e52e6af02cb4c7f762`.
Still before compilation, checker refinements were reviewed at 15881 bytes,
SHA-256 `a5021b05e3ca1b1ef932910ee28a760733d31297a8d08f9781ed9fc8ab078254`:
an explicit return-address sentinel rejects clobbered return paths,
same-register branches have known outcomes, and the uncovered-instruction check
was simplified. Sources, configuration and compiler arguments did not change.
Both sources use the same pinned unmodified MW219, wibo, working directory and
compiler arguments:

```text
mwccpsp.exe -nostdinc -lang c++ -c -O2 -o {fresh-case-object} {frozen-case-source}
```

Only the declared source/output paths differ between cases. No new optimization,
alias, inline, RTTI, exception or assembler option is added. Exact object-symbol
validation requires one complete executable function and rejects unsupported
code relocations. Complete-function byte comparison is independent of the
static address observations. Inputs and emitted objects are rechecked before
report publication.

The static analyzer follows bounded forward branch paths with NOP delay slots
and a small instruction whitelist. It tracks constants/receiver-relative
addresses, counts the union of large-constant receiver ADDU instruction sites,
and checks declared word-access paths. It does not count dynamic visits or
prove stored values/behavior. Unsupported paths/instructions/addresses produce
`UNINTERPRETED` with null counts, never a partial count or assumed improvement.
Manual output audit must independently check complete instructions, offsets,
access order and constants.

No fixture output or prediction of which representation performs better was
available at preflight. The final 1509-byte profile has SHA-256
`614238f14ac02863dec2821e9b9ade3d002e6946a3116b494e9b758e1864f5f1`.
Replacing only its freeze-status value reconstructs the exact reviewed draft
digest above. Both independent reviews preceded the first fixture compilation.

## Final repeated results

Independent read-only audit rehashed/reparsed all four objects under
`build/address-reuse-o2mm0k1m` and `build/address-reuse-8e3b12xv`, reproduced
their strict whole-function observations and bounded static reports, and checked
empty compiler logs. The complete objects are identical across both cases and
both trials: 768 bytes, SHA-256
`775c998a2213ab73a0458f44dc6357336afe8fea2d9b2e30f90d637e4fed101c`.
Each contains exactly one complete 100-byte function, SHA-256
`5eec7bae467bb2a578f0aad3754d54ce6b8c7bb6875dea43b24150fce6d2c0fe`.
Both retain flags `0x10970001`; no unsupported code relocation occurs.

The two `evidence/bucket-03j/address-reuse-run-*.json` reports are also identical:
12442 bytes, SHA-256
`40d44289975dc68110491b7c78512c230cc1ccfdf4b88922318be4c7a3f7cf0e`.
Both sources and the final reviewed runner retain their frozen hashes.

| Observation | Direct fields | Grouped fields |
| --- | --- | --- |
| Complete function size | 100 bytes | 100 bytes |
| Complete function bytes | Identical | Identical |
| Bounded static status | INTERPRETED | INTERPRETED |
| Large receiver-base ADDU sites | 5 | 5 |
| Declared access traces | All four | All four |
| Reduction from grouping | — | 0 static sites |

Manual disassembly with the already available GNU objdump independently confirms
the classifier. A LUI of `0x2` precedes each receiver ADDU at function offsets
`0x0C`, `0x18`, `0x30`, `0x3C` and `0x54`. Signed displacements `0xA120` and
`0xA124` resolve against that `0x20000` adjustment to the declared field offsets.
These are five static instruction sites, not five operations on every path.

| Function offset | Word access / control observation |
| --- | --- |
| `0x10` | Store logical high seed half to upper field. |
| `0x1C` | Store masked low seed half to lower field. |
| `0x20` / `0x34` | Low-half branch conditionally skips the lower default store of `0x1357`. |
| `0x40` | Reload upper field. |
| `0x44` / `0x58` | Upper-word branch conditionally skips its default store of `0x2468`. |
| `0x5C` / `0x60` | Complete JR return and NOP delay slot. |

All memory operations above are 32-bit LW/SW. Both internal forward branches
have NOP delay slots and preserve the declared ordered access paths. No runtime
execution or general source-semantic proof is implied by this bounded static
inspection.

## Post-trial checker hardening

Review found an abstract-analysis gap: a field address constructed solely by
small ADDIU steps could satisfy the access traces while receiving a misleading
zero large-ADDU count. After the trials, the checker was narrowed to the
characterized large-ADDU address model. Receiver expressions now carry immutable
origin-site provenance through supported moves/additions; loads or unsupported
value operations kill it. Every memory base must carry nonempty provenance, or
the result is `UNINTERPRETED` with null counts. Only origin sites contributing
to declared field accesses enter the union, excluding unused calculations.

The independently reviewed hardened runner is 16286 bytes, SHA-256
`5aefa4160aa2ad40aa114b1d696b085b98edd73a606bee56d983a88f4e7dcf99`.
The reviewer reapplied it to all four retained objects: every full observation
remains exactly equal to the original reports, including the same five sites
and four access traces. No fixture was recompiled and no bytes, source, flags,
frozen configuration or whole-function comparison criterion changed.

For the requested second inspection, full invented-fixture disassemblies are
retained in `evidence/bucket-03j/direct.disasm.txt` and
`evidence/bucket-03j/grouped.disasm.txt`. The differing file-name headings do not
represent a code difference; all complete instruction bytes remain identical.

## Interpretation limits

A difference would establish an effect of the declared record representation
under this one compiler/profile; equality would show that grouping alone did
not change these outputs. Neither outcome identifies a compiler backend pass,
an alias-kill mechanism, a unique source representation or the game's original
layout. Here, grouping alone was insufficient to change output or address reuse
under the fixed profile. Repeated large-offset calculations are observable
instructions, not a unique signature of why the compiler emitted them.
No cached-address variant, source search, flag search, runtime claim or
modification of the game candidate followed the result. The reviewer invoked
no compiler and did not read or rewrite the 3I candidate. Toolchain and game
matching status remain unchanged. Stop at the output checkpoint.
