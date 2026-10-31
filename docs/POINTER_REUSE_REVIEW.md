> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Named-pointer fixture review — Bucket 3O

This diagnostic compares the unchanged grouped fixture with one ordinary local
pointer to its existing `KeyState` subobject. It does not revise the game
candidate, choose compiler flags or claim a game match. The independent reviewer
does not invoke the compiler.

## Preconditions recorded before compilation

The existing grouped source is `bench/address_reuse_grouped.cpp`, 1,200 bytes,
SHA-256 `04662faba3e8e68506928bb2d2623d25cf5e6a93f8f9fb1bde3e3dd223908094`.
Its historical complete object is 768 bytes, SHA-256
`775c998a2213ab73a0458f44dc6357336afe8fea2d9b2e30f90d637e4fed101c`.
The complete 100-byte function has SHA-256
`5eec7bae467bb2a578f0aad3754d54ce6b8c7bb6875dea43b24150fce6d2c0fe`.
Fresh grouped controls must reproduce these bytes, not merely their length.

Both forms retain the exact raw symbol
`initialize_key__17ArchiveKeyContextFUi`, unsigned 32-bit seed/fields, eight-byte
`KeyState`, nonvirtual owner and invented field offsets `0x1A120/0x1A124`.
Record extent remains `0x1A128`; defaults remain `0x1357/0x2468`.
The proposed new body adds only `KeyState* key_state = &state` and replaces
member accesses with `key_state->member`. It changes no qualifier, field,
constant, condition, store ordering or call interface. A local pointer adds no
member to the owner record.

For a valid live owner object, both source forms perform these volatile word
accesses in the same order: store the high seed half to upper; store the low
half to lower; optionally store lower's default when the masked low half is
zero; reload upper; optionally store upper's default when that read is zero.
The four declared optional-store paths remain the relevant access traces.
This source reasoning does not define behavior for an invalid/null receiver or
prove runtime equivalence for every external execution environment.

Only the existing unmodified MW219/C++/O2 profile is allowed. Both fixtures run
in two fresh trials; entire objects and complete functions are inspected, with
the established strict symbol/section/relocation checks. Existing fail-closed
static analysis must retain unsupported output as `UNINTERPRETED` with no
materialization count. A shorter function alone does not establish address
reuse or identify the internal compiler pass responsible.

No fixture output or preferred result was available when these preconditions
were written. Neither a change nor equality can identify the historical game's
original source representation.

## Exact pre-compilation source and profile review

The pointer source is 1,329 bytes, SHA-256
`54070496d2c38d71c3153025874637007acd6fa226d87849cca64c9749bde58b`.
An independent token comparison, excluding comments and whitespace, reconstructs
it exactly from the grouped source by adding the declared local pointer and
replacing `state.lower/upper` with `key_state->lower/upper`. All remaining code
tokens agree. Purpose comments identify the experiment and its invented values;
there is no assembly, register pin, barrier, additional volatile qualifier or
extra source alternative.

The reviewed draft `config/pointer-reuse.json` is 1,419 bytes, SHA-256
`cd8c79beadab4b04b3c2192a0d9ba0bc1847d45b2bc15a6676170b01e27e3987`.
It declares the two case IDs in order, unchanged compiler flags/symbol/field
offsets/defaults, two trials and the full historical grouped object. The runner
requires frozen status before invocation, checks inherited frozen inputs,
rejects report aliases/existing output reports, and uses a fresh build directory.
Grouped compilation must reproduce the historical whole object before the
pointer case is invoked. Complete ELF/function validation and bounded static
analysis remain separate; unsupported analysis receives no numeric improvement.

Before compilation, independent review also flagged that a compiler exception
could leave a partial object outside the emitted-output drift checks. The
primary corrected this failure-evidence path before any fixture was compiled:
post-exception handling rejects links/nonregular files, records any retained
partial output's identity and includes it in final byte rechecks without
accepting the failed case. The reviewer read back that correction. Successful
case bytes are also checked against their earlier snapshot before report
publication, catching cross-invocation output changes.

Pre-compilation source/profile approval applies only to these exact artifacts
and the declared status-only freeze. The final runner is 8,874 bytes, SHA-256
`80cfcff737ee560ca10055fcc049b36f2a2bee6d8da58a10b278bfc11f4ba0af`.
The frozen profile is 1,427 bytes, SHA-256
`eb33093dd8d47a019079738920a78a1ca41334b7b2b38b17746982500dd6c300`.
Replacing only its status with the reviewed draft status reproduces the exact
draft size/hash above. The freeze record at
`evidence/bucket-03o/profile-freeze.json` records both independent pre-compilation
reviews and no prior pointer-fixture compilation. No source, flags, symbol or
checker changed after these trials.

## Independent repeated-output audit

Both retained reports, `pointer-reuse-run-1.json` and
`pointer-reuse-run-2.json` under `evidence/bucket-03o`, are identical: 12,360
bytes, SHA-256
`e629afabba70eac65081c662e8ecd38f671719c62f98632fcbbb939a05264f1a`.
The reviewer rehashed and strictly parsed all four objects in
`build/pointer-reuse-i74v_h8d` and `build/pointer-reuse-v_emq5h0` and reproduced
every complete-function observation and bounded address-analysis record.
All four compiler logs are empty. Both grouped controls reproduce the complete
historical object, and both pointer objects are byte-identical to one another.

| Observation | Grouped control | Named pointer |
| --- | --- | --- |
| Complete object size | 768 bytes | 736 bytes |
| Complete function size | 100 bytes / 25 words | 72 bytes / 18 words |
| Static receiver-base ADDU sites | 5 | 1 |
| Declared ordered access paths | All four | All four |
| Address analysis | INTERPRETED | INTERPRETED |
| Flags | `0x10970001` | `0x10970001` |

Pointer whole-object SHA-256:
`178883c8ab0e521eb3d807f7d1da44b5f3fca441c607a7880966279ce2f65d96`.
Pointer complete-function SHA-256:
`faaf79fe701ab7ea322b1ac1d71eac14b0eeae5af7c3deb6e0f9afcb87515c3c`.
Grouped hashes remain the historical values recorded above. The validated ELF
contains the expected single complete function without unsupported code
relocations. The original noncode `.mwcats` / `.rel.mwcats` metadata remains;
these objects have not been patched or normalized to compare them.

## Manual instruction and access-path review

Read-only GNU objdump inspection independently agrees with the checker. The
pointer function begins with `LUI at,1; ORI at,at,0xA120; ADDU a2,a0,at`,
forming the complete `receiver + 0x1A120` base once at function offset `0x08`.
All later field operations use `a2+0` or `a2+4`. The use of `at` is the
compiler's emitted register choice; the source contains no register pin.

| Pointer function offset | Complete access/control observation |
| --- | --- |
| `0x0C` / `0x10` | Mask low seed half and logically shift high half. |
| `0x14` / `0x18` | Store upper at base+4, then lower at base+0. |
| `0x1C` / `0x20` | Low-half conditional branch to `0x2C`, with NOP delay slot. |
| `0x24` / `0x28` | Materialize `0x1357` and optionally store lower. |
| `0x2C` | Reload upper at base+4. |
| `0x30` / `0x34` | Upper-word conditional branch to `0x40`, with NOP delay slot. |
| `0x38` / `0x3C` | Materialize `0x2468` and optionally store upper. |
| `0x40` / `0x44` | Complete JR return and NOP delay slot. |

Every memory operation is the expected 32-bit LW/SW. The two forward branches
yield the same four ordered access traces as the baseline. No call, spill or
stack adjustment is introduced. The grouped version retains large ADDU sites
at `0x0C`, `0x18`, `0x30`, `0x3C` and `0x54`, each preceded by `LUI 2` and used
with signed field displacements. Five two-instruction bases become one
three-instruction full-offset base: seven fewer instructions, hence **28 bytes**
of function reduction. Four removed bases do not mean a 32-byte reduction.
The separate 32-byte object-size reduction also includes file-layout spacing:
`.mwcats` moves from offset 416 to 384, while `.text` itself shrinks by 28.

## Bounded conclusion

Under this unchanged compiler/profile, naming the local subobject pointer
changes the complete synthetic output and permits one shared field-address
base. Grouping alone previously did not. This demonstrates a source-shape
effect for this invented record; it does not identify an alias mechanism,
optimization pass, original game record or historical source representation.
The checker validates a bounded access pattern, not all stored-value semantics
or dynamic execution counts. No game candidate was revised or scored, no game
ran and no matching-gate credit follows. The one existing game-source attempt,
original flags and unlocked toolchain status remain unchanged. The reviewer
invoked no compiler; further work needs its own recorded scope.
