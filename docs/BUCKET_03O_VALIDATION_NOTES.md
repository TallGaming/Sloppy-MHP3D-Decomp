> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3O independent validation

This approved diagnostic compares two invented C++ fixtures: the unchanged
grouped form and one form naming a local `KeyState*`. It does not rewrite or
score a game function. The existing MW219/C++/O2 profile, scalar widths,
invented offsets/defaults and volatile access sequence stay fixed. No helper
invokes a real compiler for these checks.

## Before-compilation review

The helper approves the exact 1419-byte draft `config/pointer-reuse.json`,
SHA-256 `cd8c79beadab4b04b3c2192a0d9ba0bc1847d45b2bc15a6676170b01e27e3987`.
The new 1329-byte source has SHA-256
`54070496d2c38d71c3153025874637007acd6fa226d87849cca64c9749bde58b`.
The explicit pointer is a readable local expression; it introduces no register
pin, assembly, barrier, extra observable access or new game-source hypothesis.
The inherited Bucket 3J profile still rejects cached pointers and retains its
original source and checker. Its checker remains SHA-256
`5aefa4160aa2ad40aa114b1d696b085b98edd73a606bee56d983a88f4e7dcf99`.

The frozen profile is 1427 bytes, SHA-256
`eb33093dd8d47a019079738920a78a1ca41334b7b2b38b17746982500dd6c300`.
The helper reconstructs the exact approved draft hash by replacing only its
status value; no other profile byte changed during freezing.

Independent read-only input verification passes **208 local pin records and 11
native dependency records**. Counts are declarations, not distinct files. The
draft status is changed only in memory to exercise validation; the file remains
unmodified for the primary's explicit status-only freeze. The historical
baseline binds the complete prior 768-byte grouped object, SHA-256
`775c998a2213ab73a0458f44dc6357336afe8fea2d9b2e30f90d637e4fed101c`.
A baseline failure or any complete-object drift stops before the pointer case
and preserves an incomplete result without a comparison or claimed advantage.

## Meaningful controls

Seven new tests reuse the fully valid invented 3J/archive/language/family input
graph. Only compilation is mocked; inherited identity and scope validation
remain active. Existing ELF/classifier tests are not duplicated.

- Fixed pair and two fresh trials; complete bytes and interpreted static metrics
  remain separate, while the old no-pointer profile stays unchanged.
- New pair/order/flags/offset/default/trial constraints and the inherited strict
  no-pointer rule are enforced before compilation.
- Nonzero exit, warning, missing/invalid/member-mismatched/relocated output and
  timeout leave no false advantage. Valid but uninterpreted code retains its
  complete bytes while its address comparison stays unknown.
- A changed unused byte in the historical object is still a control mismatch,
  even when function bytes agree. Failed baseline compilation is not bypassed.
- Every retained output is rechecked, including a partial object written before
  a raised timeout. Later replacement prevents publication.
- Before/after source, historical, inherited game/reference/tool/native and
  profile mutations invalidate the outer result.
- Input/report aliases and existing report conflicts preserve prior files and
  fail before creating a new build or invoking compilation.

Review identified missing exception-partial output retention in the first runner
draft. The primary adds capture after the exception path, recording its hash
without adding an observation or changing the rejected outcome. Controls verify
both baseline and pointer timeout partials, and reject mutation during final
verification. The source, flags and old classifier are unchanged by this fix.

The helper runs **7 new tests successfully, zero skipped**, then the complete
suite: **303 passed, zero skipped**, preserving the prior 296 checks. These
tooling checks are separate from the unimplemented full-game gate and its
eighteen required negative tests.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `scripts/bench_pointer_reuse.py` | 8874 | `80cfcff737ee560ca10055fcc049b36f2a2bee6d8da58a10b278bfc11f4ba0af` |
| `tests/test_pointer_reuse.py` | 13586 | `6a4ed8e6da9f2e4dba6fe98bd7d2cdb6eaa03063bad89be6700862dd1e02c137` |

## Actual repeat audit

The helper independently reads all four objects and both retained reports from
`build/pointer-reuse-i74v_h8d` and `build/pointer-reuse-v_emq5h0`.
`evidence/bucket-03o/pointer-reuse-run-1.json` and `pointer-reuse-run-2.json`
are byte-identical: **12360 bytes**, SHA-256
`e629afabba70eac65081c662e8ecd38f671719c62f98632fcbbb939a05264f1a`.
Both cases validate in both trials; compiler logs are empty and corresponding
whole objects reproduce exactly.

| Case | Object bytes | Function bytes | Complete object SHA-256 |
| --- | ---: | ---: | --- |
| Grouped | 768 | 100 | `775c998a2213ab73a0458f44dc6357336afe8fea2d9b2e30f90d637e4fed101c` |
| Named local pointer | 736 | 72 | `178883c8ab0e521eb3d807f7d1da44b5f3fca441c607a7880966279ce2f65d96` |

The grouped output equals the entire historical object, not merely its function.
Its function hash remains
`5eec7bae467bb2a578f0aad3754d54ce6b8c7bb6875dea43b24150fce6d2c0fe`;
the pointer function hash is
`faaf79fe701ab7ea322b1ac1d71eac14b0eeae5af7c3deb6e0f9afcb87515c3c`.
All complete symbol extents and bytes are checked without masking, trimming or
substituting code. No unsupported code relocation is present.

The helper separately walks the actual bounded instruction words and both
forward branch alternatives, without executing guest code. All four possible
field-access traces agree between forms and match the report. Grouped memory
bases originate at five static ADDU sites, byte offsets **12, 24, 48, 60, 84**;
the pointer memory bases share the one ADDU at **8**. The pointer materializes
the full invented field offset with LUI/ORI before adding the receiver, whereas
the grouped form repeats LUI/ADDU address pairs. The complete body shrinks by
28 bytes, and the existing classifier reports four fewer static base sites.
Static site counts are not runtime execution counts or a proof of which
compiler optimization pass caused the change.

Final read-only verification again passes **208 local and 11 native pin
records**, including the unchanged game candidate and earlier profiles. No
original ISO was opened, game candidate revised or game target compared. The
result establishes this particular invented source-expression effect under the
fixed profile; it does not establish the original class layout, qualifiers,
source spelling, compiler revision or a game match. Source-linked/matched game
functions and counted matching tricks remain zero. Stop at the Bucket 3O
checkpoint under the user's advance-approval workflow.
