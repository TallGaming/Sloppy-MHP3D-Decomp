> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3O: named pointer diagnostic — completed checkpoint

**Naming the invented `KeyState` pointer reduces the complete function from
100 to 72 bytes and the characterized large-base sites from five to one.**
Both fresh trials agree, and the grouped control reproduces its historical
whole object exactly. This is a source-expression result under unchanged
MW219/C++/O2, not a game match or identification of an internal compiler pass.

| Observation | Grouped control | Named pointer |
| --- | ---: | ---: |
| Complete object | 768 bytes | 736 bytes |
| Complete function | 100 bytes | 72 bytes |
| Characterized large-base ADDU sites | 5 | 1 |
| Four declared volatile-access paths | Verified | Verified |

The baseline repeats five LUI/ADDU pairs. The pointer form constructs the full
invented subobject address once using LUI/ORI/ADDU, then uses offsets zero/four.
That removes seven instructions, **28 function bytes**. The 32-byte whole-object
size change also includes file-layout spacing; it is not a 32-byte code reduction.
Register assignments, instruction order and branch displacements change too.
The invented offsets/defaults differ from the game, so its size is not a game
comparison. The actual archive draft remains unchanged and uncompiled here.

## Evidence

- Sources: existing `bench/address_reuse_grouped.cpp` and new
  `bench/address_reuse_pointer.cpp`; independent token comparison found only
  the declared pointer initialization and access substitutions beyond comments.
- Frozen profile: `config/pointer-reuse.json`, 1427 bytes, SHA-256
  `eb33093dd8d47a019079738920a78a1ca41334b7b2b38b17746982500dd6c300`.
- Both 12360-byte reports have SHA-256
  `e629afabba70eac65081c662e8ecd38f671719c62f98632fcbbb939a05264f1a`;
  see `evidence/bucket-03o/pointer-reuse-run-1.json` and `-2.json`.
- Build roots: `build/pointer-reuse-i74v_h8d` and `build/pointer-reuse-v_emq5h0`.
  Pointer whole objects have SHA-256
  `178883c8ab0e521eb3d807f7d1da44b5f3fca441c607a7880966279ce2f65d96`;
  complete function SHA-256
  `faaf79fe701ab7ea322b1ac1d71eac14b0eeae5af7c3deb6e0f9afcb87515c3c`.
- Full disassemblies and provenance are under `evidence/bucket-03o/`.
  Independent reviews: `POINTER_REUSE_REVIEW.md` and
  `BUCKET_03O_VALIDATION_NOTES.md`.

All **303 tooling tests pass, zero skips**, including seven new integrity controls.
Before compilation, review fixed failed/timeout partial-output retention so those
bytes are also checked for drift without accepting the failed case. Historical
control drift stops before the pointer case; unsupported static analysis retains
complete bytes but withholds any numeric reuse advantage. Both helpers audited
all four objects and the unchanged inherited inputs.

## Decisions and next step

The result shows that this tested compiler/profile can retain a shared base for
this readable pointer form. It does not rule out compiler/source-context causes
for the remaining original-game difference. No flags, prior source/checker or
tool binary changed. Original game source attempts remain one; game matches,
linked source, parking and matching-trick counts remain zero. Full-game gate
and eighteen negative tests remain unimplemented; runtime/port work stays deferred.

The user's five-hour advance approval permits a separately documented next
bucket. The most direct follow-up is to test the same readable pattern with
the real archive offsets/defaults in retained diagnostic copies, while keeping
the historical direct draft as a full-object control. Declare the variants and
source-attempt budget before compiling them.
