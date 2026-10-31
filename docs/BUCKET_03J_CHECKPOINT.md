> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3J checkpoint

2026-10-30. The approved grouping-only fixture experiment is complete.
**Direct fields and grouped `KeyState` fields produce identical complete objects
and identical 100-byte functions in both fresh trials. Both retain five static
large receiver-base ADDU sites. Grouping alone provides no reduction here.**

## Scope and result

The two invented readable C++ fixtures were independently reviewed and frozen
before compilation. They share their owner/method signature, volatile 32-bit
fields, offsets `0x1A120`/`0x1A124`, extent `0x1A128`, defaults `0x1357`/`0x2468`
and access order. The grouped form uses `state.member` directly, with no local
pointer, reference, helper, register pin or assembly. Existing unmodified
MW219/C++/O2 and `-nostdinc -lang c++ -c -O2` remain unchanged.

| Observation, reproduced in both trials | Direct | Grouped |
| --- | --- | --- |
| Complete object | 768 bytes | Identical 768 bytes |
| Complete function | 100 bytes | Identical 100 bytes |
| Static address analysis | INTERPRETED | INTERPRETED |
| Large-base ADDU sites | 5 | 5 |
| Static-site reduction from grouping | — | 0 |

The sites occur at function byte offsets `0x0C`, `0x18`, `0x30`, `0x3C` and
`0x54`. These are static instruction positions, not operations executed on every
path. Complete byte equality also establishes that no register, scheduling or
branch-displacement difference exists between these particular outputs.
This does not prove that grouping never helps, identify an internal compiler
pass or establish the game's original type layout. No game target was scored.

## Full outputs and provenance

- Direct/flat full disassembly (local-only artifact: `evidence/bucket-03j/direct.disasm.txt`)
- Grouped full disassembly (local-only artifact: `evidence/bucket-03j/grouped.disasm.txt`)
- Objdump and object provenance (local-only artifact: `evidence/bucket-03j/disassembly-provenance.json`)
- [Direct source](../bench/address_reuse_direct.cpp) and
  [grouped source](../bench/address_reuse_grouped.cpp)
- [Frozen profile](../config/address-reuse.json) and
  pre-compilation freeze record (local-only artifact: `evidence/bucket-03j/profile-freeze.json`)
- Trial 1 (local-only artifact: `evidence/bucket-03j/address-reuse-run-1.json`) and
  trial 2 (local-only artifact: `evidence/bucket-03j/address-reuse-run-2.json`)
- [Independent source/output review](ADDRESS_REUSE_REVIEW.md) and
  [validation notes](BUCKET_03J_VALIDATION_NOTES.md)

The disassembly headings name different files; the full function bytes agree.
Fresh build roots are `build/address-reuse-o2mm0k1m` and
`build/address-reuse-8e3b12xv`. All four complete objects have SHA-256
`775c998a2213ab73a0458f44dc6357336afe8fea2d9b2e30f90d637e4fed101c`.
Every complete function has SHA-256
`5eec7bae467bb2a578f0aad3754d54ce6b8c7bb6875dea43b24150fce6d2c0fe`.
Both 12442-byte reports have SHA-256
`40d44289975dc68110491b7c78512c230cc1ccfdf4b88922318be4c7a3f7cf0e`.

## Checker validation

The static checker follows a bounded whitelist of instructions and forward
branches, tracking constants, receiver-relative offsets and address origins.
Unsupported instructions, branches, addressing or limits return
`UNINTERPRETED`, withholding counts and traces. Complete bytes remain available
independently. This is static address inspection, not guest execution or a proof
of stored values, source semantics or runtime behavior.

After the trials, review found that a chain of small ADDIU steps could reach
the fields and misleadingly yield zero large-base sites. The checker was
hardened to require characterized large-ADDU lineage for every memory base;
only origin sites used by memory accesses are counted. Dedicated controls cover
that unsupported construction and unused large-address arithmetic. Independent
and primary reinspection of all four retained objects reproduces every original
observation exactly. No fixture was recompiled or source/profile changed.
The historical freeze records the original runner; the final hardened runner is
SHA-256 `5aefa4160aa2ad40aa114b1d696b085b98edd73a606bee56d983a88f4e7dcf99`.

All **258 tooling tests pass under WSL, zero skips**: 239 prior and 19 new
address-reuse controls. Two real failure controls reject a report/input alias
and an unapproved cached-pointer scope before any new compilation directory or
success report, preserving the profile. Both helpers independently audited the
outputs; the validation audit checked 204 local and 11 native pin records.
See verification summary (local-only artifact: `evidence/bucket-03j/verification-summary.json`) and
test log (local-only artifact: `evidence/bucket-03j/tooling-tests.log`).

From the project root, reproduce tests or request new fresh fixture trials with:

```powershell
wsl -d Ubuntu -- python3 -m unittest discover -s tests -v
python scripts/bench_address_reuse.py --report evidence/bucket-03j/new-trial-1.json
python scripts/bench_address_reuse.py --report evidence/bucket-03j/new-trial-2.json
```

## Decisions preserved; stop for review

The Bucket 3I game candidate remains unchanged and NONEXACT. This experiment
adds no game-source attempt, parked function, matching trick or match credit.
Toolchain attribution remains unresolved. The full-game byte gate and required
18 negative checks remain unimplemented; these 258 tooling tests do not replace
them. Runtime testing, linking, full reconstruction and native-port work remain
deferred. No cached-address variant or next bucket is authorized.
