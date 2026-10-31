> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Archive key-advance pipeline review — Bucket 3AL

This bucket contains one plain-source hypothesis for the different key-advance
routine, not another attempt on the parked initializer. Whole invented controls
must reproduce under all four existing configurations before any new target
source is compiled. Exact isolated bytes do not grant game matching credit.

## Plain-source review before output

`bench/archive_key_advance.cpp` is 1,156 bytes, SHA256
`4bcd148007c42aa4a7e97fa01c99cd90ac9bafe986445a46ec91d72014e19f93`.
The method uses ordinary unsigned 32-bit state fields, straightforward constant
multiply/remainder updates and a packed return. These implement the 3AK arithmetic
for every 32-bit state, including wrapping products. The prefix is an explicitly
unknown byte region ending at the established lower-word offset 0x2F53C; upper
follows at 0x2F540. No preceding class members are invented or accessed.

The header identifies the unknown receiver/qualifiers and non-integrated status.
Ordinary fields are hypothesis 1, compatible with snapshot-like register dataflow;
the observed binary does not prove a compiler reordered a particular source
statement order. The public MHP2G volatile lower-first/reload shape is not copied
as a recovered qualifier contract. No assembly, pins, barriers, volatile shaping,
expression trick or conditional source fallback appears. No source revision after
results belongs to this bucket.

## Exact existing pipeline reuse

The smallest reuse path is the existing 3W producer `verify_inputs(config)` for
MW219/GCC171/SNC profiles and 3AA consistent-fixture `verify_freeze()` plus
`verify_inputs()` for its returned later GNU pipeline/runtime. These functions
verify original configs, tools and prior preparations; neither executes a compiler
merely by producing the profile.

| Profile | Fixed C++ compiler arguments before paths | Existing assembler |
| --- | --- | --- |
| MW219 | -nostdinc -lang c++ -c -O2 | Existing unmodified driver through wibo |
| GCC171 cc1plus | -quiet -nostdinc -G 0 -march=allegrex -mtune=allegrex -mel -mabi=eabi -O2 | -EL -march=allegrex -mabi=eabi -G0 -O0 |
| SNC1.2.7503.0 | -c -G0 -O2, preserving .cpp source | Existing unmodified driver through wibo |
| GCC435 cc1plus | Same declared backend flags as GCC171 | Same assembler flags plus preexisting -msingle-float |

MW/SNC reuse `producer.compile_profile`. GNU may use the existing
`capture.capture` API to preserve actual assembly while keeping native/tmp
staging, source basename, probe.s name and compiler/assembler argument order.
That retention path has already reproduced ordinary objects. GCC435 runs inside
the existing runtime context manager with only its declared private LD_LIBRARY_PATH
and LC_ALL overrides, restored afterward. Do not leak that environment into older
profiles. No SDK driver, linker, new frontend, binary patch or flag is introduced.
The modern GNU assembler is diagnostic machinery, not an original-SDK lock.

Full config/source/compiler/runner/assembler/native dependency records stay in
the inherited profiles. The exact reuse description and checked record hashes
are in `evidence/bucket-03al/helper-map-pipeline-reuse.json`; this inventory was
created by reading files, without invoking any compiler or native tool.

## Complete invented control objects

The unchanged control source `cpp_static_producer.cpp` is 1,699 bytes, SHA256
`fb88cb5c8f7be2b0f7a4cb83ac994789c3f88e3a2b49726e81d476a437426423`.
All eight retained objects were independently rehashed against both prior runs:

| Configuration | Whole object bytes | SHA256 |
| --- | --- | --- |
| MW219, 3W | 6528 | 406ea0e4105f271d4e6f81d142393d22e3b59b72542a0ed15ebe3bf6b85b004f |
| GCC171, 3W | 6312 | a8848c362e49c88129ef5373529cfbe9c86c6233d220bcd6d27928c7de3017d9 |
| SNC, 3W | 2456 | 82075727f9e18b68f997b74ebd6e02172b319db60fc791474b4edb6242b8af59 |
| GCC435/single-float-as, 3AA | 6056 | 890b3018129707bde119a706fc6540cd12d4dff683f32bf65aca6eee1f52e41d |

Exact report-derived paths for both copies are in
`helper-map-control-objects.json`. These are whole-object controls, including
metadata/relocations, not trimmed function hashes. Reusing them must preserve
source extension/basename and all existing stage settings. Control failure
prohibits every new target-source compilation in that trial.

## Independent pre-execution review

Final pre-compilation approval covered controller `compare_key_advance.py`,
23,866 bytes, SHA256
`c3b73b7034c654a6786df614638e57300f994d00055eebff1b3aaf30bf98df0d`,
and `config/archive-key-advance-experiment.json`, 86,547 bytes, SHA256
`39294276bc772ea9a42eb466b18a89fe7b96eea18c90960ff47b9ca4f2167c23`.
The source remains the approved 1,156-byte hypothesis above. Independent static
reconstruction of all four complete pipeline dictionaries agrees with the new
snapshot; 205 relative pin records and 12 distinct native tool/runtime files
were independently rehashed. No compiler/assembler/decoder was invoked by this
reviewer.

The inherited code closure has 11 pinned Python sources. Before repository
imports, the controller checks their bytes and installs a temporary verified-byte
source loader, clears applicable cached modules, and restores the loader afterward.
All controls precede every candidate. Partial logs/objects/assembly are retained;
accepted objects are associated with the same retained byte snapshot before
inspection. Final artifact identities and all source/config pins are rechecked.
The target binds the complete old ELF range, exact original-byte report and both
independent boundary assessments.

The predeclared extent rule accepts exactly one defined STT_FUNC, including a
count of any zero-size declarations when detecting ambiguity. It must be a
strong global, default visibility in the low two st_other bits, positive
word-aligned complete extent, and allocated executable PROGBITS. Raw high st_other
bits are retained without being normalized. Additional function declarations,
ambiguous/empty/invalid extents and every nonzero relocation targeting code leave
the row unscored. Non-code relocation facts remain explicit and unapplied.
No target-byte search or mangling alias guess selects a function.

Twenty-seven invented selection/orchestration/partial-output controls are
reported passing, including output snapshot association, empty decoder rejection
and stale-pyc source loading. These are tooling controls, not the 18 game gate
checks. Approval permits only the two declared control-first trials. No source
revision, different flag setting or extra compiler candidate is included.
Require one complete defined executable function; preserve raw symbols, every
code relocation and full bytes. An unsupported or ambiguous extent stays unscored;
no target-driven instruction trimming, padding removal, symbol relaxation or
relocation masking is allowed. Decoder failures remain explicit. Both fresh
trials must retain all four outcomes, with no best-family pooling or toolchain
attribution from an isolated exact interval. Source hypothesis 1 and parked/trick/
matching counters require visible accounting regardless of outcome.
## Final two-trial audit

Both frozen control-first trials completed in `archive-key-advance-u4o5ciqe`
and `archive-key-advance-xna8e9kj`. Their reports are each 279,148 bytes;
SHA256 values are respectively
`43e2350c4440cd4f75091bfcb19724b541ae4e805bf11f2449a4b12c5fc4b3d9`
and `7a5006a54789bff5b14d732ca72b0b128b1ef0fa5e983b91774db8be606703f1`.
Report bytes differ because they retain actual paths and stage provenance;
all eight corresponding whole control/candidate objects repeat byte for byte.

Independent read-only checks covered 207 relative input/freeze records, all 128
retained case artifacts and sixteen whole objects. Each of the eight new controls
was compared in full with both historical copies, sixteen byte comparisons.
Compiler/assembler stages report zero exit codes and empty diagnostic streams;
all sixteen retained decoder outputs are nonempty with empty error streams.
Independent `struct` decoding of the original ELF and candidate objects, without
using the controller's selector or repository ELF parser, confirmed every sole
strong/default-visible function extent, complete body, absence of nonzero code
relocations and first differing byte. All raw non-code relocations remain present.
The audit record is `evidence/bucket-03al/helper-map-final-audit.json`.

| Profile | Complete function bytes | First differing byte | Outcome in each trial |
| --- | ---: | ---: | --- |
| MW219 | 124 | 5 | NONEXACT |
| GCC171 | 140 | 0 | NONEXACT |
| SNC | 116 | 2 | NONEXACT |
| GCC435 | 100 | 10 | NONEXACT |

The complete target is 140 bytes, SHA256
`0ff874a4e619b6a6202257c13125a9ed1ed5dab4c45cbc0242eb9ad5f0a3261f`.
Equal function size under GCC171 does not establish byte identity. Its executable
section also contains a trailing four-byte NOP outside the declared 140-byte
function; the symbol extent, not target length or padding removal, selects the body.

## Observed instruction differences

These facts come from retained full objdump text, raw words and the two GNU
assembly files. They describe this source/configuration only.

- Original and GCC171 both load upper before lower and use the same reciprocal
  constants with two unsigned high-product operations. GCC171 forms the receiver
  window with LUI/ORI/ADDU at 0x28000 and positive field displacements; original
  uses LUI/ADDU at 0x30000 and signed negative displacements. Registers and schedules
  differ. Original uses MTLO/MSUB for the upper remainder; GCC171 multiplies the
  quotient and subtracts. Their lower quotient-product shift/add sequences differ.
  GCC171 puts the lower store in the return delay slot; original stores both words
  before JR and has a NOP delay. No one-for-one instruction normalization applies.
- MW219 loads/stores lower before upper, reloads lower for the return and emits
  five separate LUI/ADDU field-address constructions. Both remainders use DIVU;
  its return delay is NOP. These observations do not establish original qualifiers
  or an optimizer aliasing cause.
- SNC loads lower before upper, retains two field bases and uses two DIVU
  operations, with six actual zero words inside its 116-byte extent. Its packed
  addition occupies the return delay slot. Ellipses in objdump's zero-run display
  do not remove those bytes from comparison.
- GCC435 uses the original's two-instruction signed-displacement address window
  and upper-first snapshot loads, but both remainders use DIVU. Its compiler-emitted
  `.s` explicitly includes each divisor check, DIVU delay instruction and BREAK;
  those operations were not invented by assembler scheduling. The lower store is
  in the return delay. A shorter result does not identify the historical compiler.

No result establishes the original receiver class, field qualifiers, compiler
version, library ownership or full-program configuration. There was one plain
source hypothesis, reused across four profiles and two trials. It remains the
same source after output; this bucket consumes no additional form or flag attempt.
The different initializer remains PARKED with its prior three plain drafts and
one commented matching shape. The new advance routine is not parked merely because
hypothesis 1 differs. Linked source and credited matches remain zero, with no
linking, original MIPS execution, native port or full game gate in this bucket.
