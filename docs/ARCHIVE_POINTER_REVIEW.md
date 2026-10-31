> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Archive record/pointer review — Bucket 3P

This is a bounded source-hypothesis comparison against the already selected
complete initializer, not integrated game source or a compiler search. The
original flat draft and its profile remain unchanged. The reviewer invokes no
compiler and permits no result-driven revision of these declared forms.

## Target, source budget and pre-compilation review

The target remains **[0x0886233C, 0x08862380)**, exactly 68 bytes, SHA-256
`7d089e6e2131eb950e3d72ee437c4aab2ec4a775e0baf8c4d45901cb227cee57`.
The existing caller/neighbor/return evidence is in
`ARCHIVE_KEY_PROBE_REVIEW.md`; the next routine at `0x08862380` is excluded.
Observed record accesses are word operations at lower `0x2F53C` and upper
`0x2F540`. The upper seed half is obtained logically and stored before the
masked low half. A zero low half receives `0x7F8D` without reloading lower;
upper is then reloaded and receives `0x2345` if that read is zero.

| Form | Source attempt | Pre-compilation source SHA-256 |
| --- | --- | --- |
| Original flat draft | 1, historical control | `6c4be341bcc3f113b56ccf7494a7b624a550b52f89c9c827eacbbce56e1f71d3` |
| Grouped `ArchiveKeyState` | 2 | `e1e8671b6a465df6b539a7d6d27f334b64865bc1ed15e6edf34223bdef865cbd` |
| Same grouping plus one local pointer | 3 | `f2e6439d81eace695d1027900503a3d3d368f3c6b506b6a5af203dbfe56be373` |

The flat source is 1,806 bytes and its unchanged profile is 1,902 bytes,
SHA-256 `30b5372dab0d1e2fb9dc0ec4436ca0e78af1922728c5a421499a66e2a4cc5188`.
The grouped and pointer copies are respectively 1,377 and 1,391 bytes. All are
preserved diagnostic files. Repeated compilation of the same source does not
create another source attempt; grouped/pointer consume the two remaining plain
forms if invoked. After attempt 3, further plain variants under this profile
require the stuck-rule decision, rather than silently extending the experiment.
This review does not authorize another form or a matching trick.

Independent comment/whitespace-insensitive body-token comparisons establish:

- Grouping changes flat member names into `key_state.lower/upper` only.
- The pointer form adds `ArchiveKeyState* state = &key_state` and substitutes
  `state->lower/upper`; all other body tokens agree with the grouped form.

Source declarations retain unsigned four-byte words, volatile fields and an
unchanged nonvirtual `ArchiveKeyContext::initialize_key(u32)` signature. The
unknown prefix is `0x2F53C` bytes, followed by the same two adjacent words in
an eight-byte subrecord, with partial extent `0x2F544`. Compile-time width and
extent guards generate no function code. A local pointer adds no owner member.
There is no assembly, register pin, barrier, helper, qualifier change, odd
expression order or added source alternative.

For a valid live receiver object, the three forms preserve the same ordered
volatile accesses and four optional-default-store paths. They define no null
receiver handling. Volatility, grouping, class identity and total original
object size remain hypotheses; the observed offsets and word widths do not
recover those source properties. Purpose comments make these boundaries
explicit. No foreign MHP2G field layout or SDK ownership is asserted.

## Profile and runner review before output

The reviewed draft `config/archive-pointer.json` is 1,723 bytes, SHA-256
`13fdbfe2fb5c429240941da7535235fdb9adb3a2bfe566610a0a5b50f1bace7c`.
The reviewed runner is 8,701 bytes, SHA-256
`aae87c43ecabd981199f4f395f2227bc85ce10761d775e9fff1330e4ed50e976`.
Both new sources, the three forms/order, target, defaults, attempt budget and
two trials are declared before compilation. The common flags remain
`-nostdinc -lang c++ -c`, with only the existing `-O2` optimization setting.
The exact expected symbol remains `initialize_key__17ArchiveKeyContextFUi`.

The original direct whole object, 768 bytes, SHA-256
`1d715acabd4cdec572d40c1905504881a396fa5e11296f1163533b30941d7796`,
must reproduce before alternatives are invoked. Its failure stops the trial
without spending uninvoked alternatives. Each declared result uses the
unchanged strict whole-function comparator against the same target and retains
the complete raw-word differences; there is no trimming, register renaming,
relocation masking or size-only acceptance. Separate bounded address analysis
uses the established checker with actual field offsets and retains unsupported
output as uninterpreted.

Fresh output directories, source/profile/inherited-input checks, report alias
and existing-report rejection, failed partial-output capture and final emitted
byte checks protect this diagnostic. The explicit source-attempt count is
separate from repeat count and game-match progress, which remains zero.
Pre-compilation source/profile/runner review approved these exact artifacts,
subject to independent controls and the declared status-only freeze. No output
conclusion was available at that review. The frozen profile is 1,730 bytes,
SHA-256 `280c8dd72be9847bc6bd043e8211bf5cc045dc8496a37f3e748c9d060b7d23cf`.
Replacing only its status with the reviewed draft status reconstructs the exact
draft size/hash above. `evidence/bucket-03p/profile-freeze.json` records both
pre-compilation approvals, the three source-attempt identities and no fourth
plain form. Source/profile/runner hashes still agree after the trials.

## Independent repeated-output audit

The reviewer read all six retained objects in `build/archive-pointer-3ifya77m`
and `build/archive-pointer-nu4biryj`, rehashed the locked reference ELF, extracted
the complete target interval and reproduced each strict comparison, complete
ELF/function observation and every raw-word difference. All six compiler logs
are empty. The two reports under `evidence/bucket-03p` are identical: 30,076
bytes, SHA-256
`a2b909b6f17c3022337dc795159dc8c2c0558c66b08f73faae8bda37c1650cc1`.
Both trials complete all three declared forms, report attempted-source count 3
and mark the plain-source budget exhausted.

| Observation | Flat attempt 1 | Grouped attempt 2 | Pointer attempt 3 |
| --- | --- | --- | --- |
| Complete object size | 768 bytes | 768 bytes | 736 bytes |
| Complete function size | 100 bytes | 100 bytes | 72 bytes |
| Complete 68-byte target comparison | NONEXACT | NONEXACT | NONEXACT |
| First differing byte | 0 | 0 | 0 |
| Static large receiver-base ADDU sites | 5 | 5 | 1 |
| Declared ordered access paths | All four | All four | All four |

The grouped and flat objects are byte-identical to one another and to the
historical control. Their complete function SHA-256 remains
`193c361fab07498ef61aa22bfa4c417f10bfbfcd0cdb8bd50a591f7838aad2da`.
Both pointer objects are byte-identical, SHA-256
`5ee9111363a6205e76bd0c3f12dccd4bf174fdeef574229b7bf561c49298bd42`.
Their complete 72-byte function SHA-256 is
`ba2cd810be0758f8ba2a416a28d7bb30c9f1b5857e6596c4bdbd876e934a5331`.
The validated objects retain flags `0x10970001`, the expected raw member symbol
and the original compiler metadata; unsupported code relocations are not
accepted. The full target hash still equals the predeclared 68-byte hash.

## Manual remaining-difference review

Read-only GNU objdump inspection independently agrees with the bounded checker.
Flat/grouped retain five base ADDU sites at function offsets `0x0C`, `0x18`,
`0x30`, `0x3C` and `0x54`. The pointer form instead constructs
`receiver + 0x2F53C` once using `LUI at,2; ORI at,at,0xF53C; ADDU a2,a0,at`
at offsets `0x00/0x04/0x08`. All subsequent field operations use offsets 0/4
from that base, preserving the declared defaults, upper reload and word-access
sequence. Its two forward branches have NOP delay slots and its complete
JR/NOP return occupies `0x40/0x44`. There is no source register pin, call or
stack-frame change.

The target uses a different address construction and allocation:

| Detail | Original target | Pointer output |
| --- | --- | --- |
| Shared base | `LUI v0,3; ADDU a0,a0,v0` | Three-instruction full-offset base in `a2` |
| Field displacements | signed `0xF53C/0xF540` | `0/4` |
| Seed-operation order | SRL then ANDI | ANDI then SRL |
| Low-half register | `a1` | `a0` |
| Default/reloaded-upper register | `v0` | `v1` |
| Function length | 17 words | 18 words |

The extra base-construction instruction accounts for the length difference,
but deleting that word would not reproduce the target: address displacements,
register fields and instruction ordering also differ. Raw same-offset word
comparison reports 25 differing/extra words for flat/grouped and 18 for the
pointer form, including its final extra word. These are unnormalized positional
differences, not counts of semantically wrong instructions. No removal,
register renaming, masked comparison or partial-match percentage was applied.

## Outcome and stuck-rule boundary

The ordinary pointer pattern's shared-address effect carries over to the real
offsets/defaults under this diagnostic compiler/profile; grouping alone still
does not change output. **None of the three full functions matches.** These
results do not recover original class/qualifier/ownership information or
identify the compiler pass responsible. Bounded access traces are distinct
from execution or a general semantic proof.

The three plain-source forms are now spent. Preserve these drafts and their
attempt notes; do not add another plain variant under this profile. Any next
step must explicitly enter the documented-trick path or visibly park the
function, with its own recorded scope. This bucket implements neither a trick
nor parking and changes no earlier source/profile. No compiler or game was run
by the reviewer, and no full-game gate, negative-gate suite, toolchain lock or
game-match credit follows from this diagnostic.
