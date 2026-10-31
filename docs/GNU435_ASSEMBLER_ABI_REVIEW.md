> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# GNU4.3.5 assembler ABI review — Bucket 3AA

This is a staged pipeline-consistency investigation using invented fixtures.
Stage A reassembles one exact retained assembly file; it invokes no compiler
and uses no game source/target. Stage B requires independent Stage A audits and
its own prior review/freeze. Failed3Z remains preserved without reinterpretation.

## ABI rationale assessed before Stage A

The already pinned4.3.5 target help records single-float enabled and double-float
disabled. Its retained invented static-object assembly declares
`.gnu_attribute 4, 2`; the unchanged diagnostic assembler warned that this
requires singlefloat. These observations preceded this bucket's option choice.

GNU's primary assembler manual identifies MIPS attribute tag4 as the FP ABI and
value2 as hardware single-precision ABI
([object attributes](https://sourceware.org/binutils/docs/as/GNU-Object-Attributes.html#MIPS-Attributes)).
It documents `-msingle-float` as disabling double-precision floating-point
operations ([MIPS options](https://sourceware.org/binutils/docs/as/MIPS-Options.html)).
This aligns the assembler's declared ABI with the compiler's existing output;
it is not a game-byte-driven compiler-option change. Current public manuals
provide semantic context, while exact local help/assembly/tool hashes and the
bounded test establish this installed diagnostic pipeline's behavior. Neither
manual establishes the retail game's original assembler or historical flags.

## Exact Stage A prior review

The reviewer approved `config/gcc435-assembler-abi.json`,1,229 bytes, SHA-256
`021db27faefe42bbe98c0066c89b75832b5c7b982a9ebc12e6550a4d59ccfe61`,
and final ignored driver `evidence/bucket-03aa/check_assembler_abi.py`,6,355 bytes,
SHA-256 `d7af12444b900dac6ea8a25215d9174fc4109d40261202b53b75ddfd07ba2472`.
Before execution the validator strengthened exact target-help line binding and
linked-build-root rejection; this reviewer read back and reapproved that final
driver. Cases, options, classification and the profile remained unchanged.
The input is the unchanged16,510-byte invented static assembly from3Z, SHA-256
`aae4577da7c1b830e0baa52315325c257f05483097845a09075c8d253fca866d`.
Its retained partial object is6,056 bytes, SHA-256
`890b3018129707bde119a706fc6540cd12d4dff683f32bf65aca6eee1f52e41d`.

The baseline flags remain `-EL -march=allegrex -mabi=eabi -G0 -O0`.
The corrected case adds exactly `-msingle-float`, uniformly for the declared
assembler case. Two fresh trials mean four assembler calls and no compiler
calls. Inputs, inherited tools/profiles, retained assembly and earlier outputs
are checked throughout.

The baseline must reproduce the full exact known warning, with no additional
diagnostic, and remain rejected by the original clean-stage validator. It is
an expected-warning negative control, never an accepted clean pipeline. The
corrected case must exit0 with empty stdout/stderr. Both additionally require
complete object identity to the pinned partial artifact, preserving code,
data, symbol/relocation tables and all metadata. A differing object or any new
diagnostic fails this declared experiment rather than causing masked comparison
or an in-place option change. Informational decoder uncertainty remains explicit.

Stage A outcomes and later Stage B review, if authorized by its prerequisite,
will be appended separately. This helper has run no compiler or assembler.

## Stage A output audit and separate Stage B review

Both Stage A repeats satisfy the predeclared contract in
`build/gcc435-abi-b_lhjtqb` and `build/gcc435-abi-atopefmt`. The reviewer
independently compared all four whole objects directly with the pinned6,056-byte
partial artifact: every byte, including metadata and relocations, is identical.
Both baseline logs contain the exact known warning; both corrected logs have
exit0 and empty diagnostics. The baseline remains rejected as a clean pipeline.
No compiler was invoked, and the final Stage A freeze inputs remain unchanged.

The retained reports are2,782 bytes each:

- `abi-trial-1.json`: SHA-256
  `97a0992d5ba0bd9841bb1a4385f54da80f7e546c9770ac41c382366d5dd7c7ae`.
- `abi-trial-2.json`: SHA-256
  `1620b964a2d793dc4c67e4bc1431e795889319abe657d3818fa0c5b6f28230d7`.

After completing that audit, this reviewer separately approved Stage B profile
`config/gcc435-consistent-fixtures.json`,1,840 bytes, SHA-256
`bf5908a7a78e0a885df72358ed5f137eb333d52c635c63493b8e7f25553ba838`,
and final ignored driver `run_consistent_fixtures.py`,8,007 bytes, SHA-256
`3d5129b5fbcf56112f67b05bd68037f09d8d95872fc48e025fd96079c43a8ce1`.
The final pre-freeze delta requires the exact ordered pair of Stage A reports;
it does not permit duplicate prerequisite evidence. This reviewer read back and
reapproved it before any Stage B compilation.

A further validator finding before freeze showed that structured-inspection or
decoder uncertainty could still allow a successful pipeline status. The primary
made both fatal after retaining a per-case result, and required exactly two
capture stages with exit0 and empty diagnostics. This reviewer read back and
reapproved the final hash above. Partial artifacts remain unscored if those
prerequisites fail; neither case selection nor source/options changed.

Stage B retains both unchanged invented fixtures and exact old/new GNU compiler
flags. Both old historical whole-object controls precede any new-frontend case
in each trial. All new cases uniformly use the separately validated single-float
assembler ABI setting; old controls retain their original flags. Global source/
assembly/object snapshots and inherited input/runtime checks remain enforced.
Both output audits and final reviews must be recorded in a separate freeze
before eight declared invented compilations. No original target is selected to
choose this setting, and no failed3Z artifact is relabeled as a clean result.

## Stage B output audit

Both fresh trials complete the declared four cases in
`build/gcc435-consistent-xoa0qmy_` and `build/gcc435-consistent-j89k5stw`.
The reviewer independently compared all eight whole objects and raw assembly
copies within each profile/fixture, checked reported function extents/hashes,
and rehashed the final freeze inputs. Both old historical controls reproduce
exactly before new cases. Every compiler/assembler stage exits0 with empty
diagnostics; structured inspection and decoding complete. The full objects and
assembly reproduce byte for byte across fresh trials.

| Profile / invented fixture | Object bytes | Complete object SHA-256 |
| --- | ---: | --- |
| Old GNU / static C++ | 6,312 | `a8848c362e49c88129ef5373529cfbe9c86c6233d220bcd6d27928c7de3017d9` |
| Old GNU / grouped address | 1,204 | `22690e399773b59c25a0b3966312c5f6465c9d96690d5a91dba274b78ee80523` |
| GNU4.3.5 / static C++ | 6,056 | `890b3018129707bde119a706fc6540cd12d4dff683f32bf65aca6eee1f52e41d` |
| GNU4.3.5 / grouped address | 1,272 | `8f46afb5c5c9afb6533193ae8e0771d0bc28540dd87282fb3f41f1f9774a04a8` |

The new static assembly is the same16,510 bytes seen in3Z, SHA-256
`aae4577da7c1b830e0baa52315325c257f05483097845a09075c8d253fca866d`.
The new grouped assembly is973 bytes, SHA-256
`66c5cb879346e5d424bf3c3b1dfc3254ca8b05225acbe6ad068603e78b882a93`.
Their object bytes repeat, including the new static object's identity to the
earlier partial3Z output, while the new assembler invocation now satisfies the
separately declared clean ABI contract. The old failed invocation remains failed.

Reports `fixture-trial-1.json` and `fixture-trial-2.json` are166,216 bytes each,
SHA-256 values
`3328a074c46aff62873c2e44dc702801d5c1434b196a59085b59d8dd6310b648`
and `725f408b56667dbf24d38c02521e059c540ebec183d67bcc63770bc218b30817`.
Paths differ between reports; complete per-case object/assembly bytes agree.

## Conventions observed without a match implication

The new static-object fixture has a60-byte `_GLOBAL__I_` initializer and no
old two-int selector helper or `_GLOBAL__D_` wrapper. Actual raw assembly and
R_MIPS_26 relocation identify a tail jump to `__cxa_atexit`; HI16/LO16
relocations identify `__dso_handle`. This is direct destructor-registration
evidence in this invented unit, not an inference from a symbol-like string.
The old GNU fixture retains its selector/priority helper and separate I/D
wrappers. Thus this4.3.5 default configuration does not reproduce the3V
initialization convention simply because its address decomposition is newer.
Other source context, options and vendor versions remain unresolved.

The new grouped-address function is72 bytes versus the old64. Its emitted
assembly uses a`0x20000` high base with negative signed field displacements,
matching the newer upstream high/low algorithm's prediction for the invented
offset. It also contains two explicit ADDU base calculations. The first BNE's
delay slot rematerializes the high constant; the low default value is loaded
afterward on its conditional path. The second BNE's delay slot loads the upper
default. An explicit return NOP is present in the raw assembly. These are manual
instruction observations; no unsupported static checker result is promoted into
a proven optimization-pass explanation or normalized matching score.

Stage A established one assembler ABI consistency correction with unchanged
whole objects. Stage B validates a diagnostic old/new fixture pipeline under
the separately frozen uniform new assembler profile. Neither establishes a
historical game toolchain, globally correct game flags or original behavior.
No game source/target was compiled, no new source shape was attempted, and no
object was linked or executed. PARKED remains one, plain attempts three,
commented shapes one, register pins/empty asm zero, credited matches/linked
source zero. This helper performed static/public-document/artifact review only;
the primary performed the declared assembler/compiler invocations.
