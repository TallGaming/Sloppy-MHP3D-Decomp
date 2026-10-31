> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3W independent validation

## Exact pre-compilation review

The one invented header-free C++ fixture uses ordinary base/derived classes,
virtual destructors/methods, an opaque external event hook and one global static-
lifetime object. Purpose comments explain observable construction, cleanup and
virtual dispatch. It contains no game-derived offsets, source iteration, matching
trick or target score. Undefined external hooks/delete/runtime references are
allowed in an unlinked object; they must remain explicit relocations.

The helper approves the exact inputs before any of the six real compilations:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `bench/cpp_static_producer.cpp` | 1,699 | `fb88cb5c8f7be2b0f7a4cb83ac994789c3f88e3a2b49726e81d476a437426423` |
| `config/cpp-producer-comparison.json` | 4,052 | `9f2616d9c2a2d19b1064448df671569cd07e94f49713982748fbe02204b2a339` |
| Fixed evidence driver | 12,749 | `7e0031c88b287f33b8ca5778d3b5fe99bb2fc7f4a284ad229a051401ee6dda74` |

Actual nested input verification passes all three declared existing pipelines,
their support/native files, parser/decoder dependencies and preserved parked
source/assembly inputs. MW changes only its already supported C++ mode; GNU
selects the existing pinned cc1plus frontend through the same native staging and
fixed modern diagnostic assembler; SNC retains its flags and uses .cpp input.
O2 is fixed per family. No new fallback, flags, libraries or linking is introduced.

The raw inspector preserves all sections, symbol tables and aliases, REL/RELA
records and function extents. It does not apply relocations or normalize raw code.
Zero-sized/non-executable declared extents and unknown relocation types remain
explicitly uninterpreted. Whole-object repeatability is distinct from symbolic
role or raw per-function similarity, and no old source-match comparator is reused
to silently discard valid call relocations.

## Pre-freeze defects and invented controls

Both reviewers identify the missing end-to-end emitted-object drift checks and
linked-output rejection. This helper also identifies unbounded relocation places
and decoder exceptions that would abort without a declared outcome. Before
freezing, the primary fixes those controls. All captured outputs, including
failed partial objects, are checked after decoders, before subsequent compiles
and before report publication. Linked/nonregular objects are rejected; decoder
failures/timeouts retain raw objects and explicit uninterpreted diagnostics.

Without launching any real compiler or decoder, the helper runs invented parser
vectors for valid REL and RELA with a negative explicit addend, raw alias/body
preservation, five malformed symbol/relocation layouts or places, unknown types
and non-executable/zero-sized extents. REL/RELA metadata remains unapplied and
unchanged function bytes verify independently.

Six mock-only driver scenarios also pass: complete positive capture; later
compiler mutation of a prior object; mutation of a timeout-partial object;
linked output; decoder timeout with all three outcomes retained; and decoder
mutation of its current object. Invalid bytes cannot produce a success report.
These are bounded one-off review controls, not a new production API or unittest
module. The last broad tooling suite remains 340 WSL passes from 3U, separate
from this diagnostic and the future full-game gate.

## Actual repeated-object audit

Both fresh trials complete all three declared fixed profiles. The 867-byte
freeze record verifies SHA-256
`43d5d003eabdb0aeacc8b45a67a5b61be00051006da50ee22f8757858caad7f2`
and records both exact pre-compilation approvals. All frozen, inherited pipeline,
compiler/support/host/decoder and preserved parked-input pins reproduce after
the trials. Source/profile/driver bytes remain unchanged.

Reports are retained under `evidence/bucket-03w/`: trial 1 is 151,742 bytes,
SHA-256 `8de502ddf10831f1e5e3bd7f4ab437f689c630002bc82ac2826fa952b8f7902c`;
trial 2 is 151,742 bytes, SHA-256
`c77d626849e26c6983f5823d6d5077f7d02995984fa583b607404f714c7ac446`.
Builds are `build/cpp-producer-d93lhtl0` and `build/cpp-producer-st8kopk6`.

| Family | Complete object bytes | Repeat SHA-256 | Function / symbol / relocation records per object |
| --- | ---: | --- | --- |
| MW219 | 6,528 | `406ea0e4105f271d4e6f81d142393d22e3b59b72542a0ed15ebe3bf6b85b004f` | 8 / 37 / 51 |
| GNU1.7.1 C++ | 6,312 | `a8848c362e49c88129ef5373529cfbe9c86c6233d220bcd6d27928c7de3017d9` | 16 / 50 / 108 |
| SNC1.2.7503.0 | 2,456 | `82075727f9e18b68f997b74ebd6e02172b319db60fc791474b4edb6242b8af59` | 8 / 24 / 29 |

All three pairs equal in every object byte. Independent ELF record parsing checks
all six objects against every reported raw section identity, 222 symbol records,
376 REL records and 64 declared function extents. Symbol aliases remain distinct
records; their shared bytes are preserved. All actual relocations are recorded
without application/masking, with target/symbol/word extents checked. Actual
relocation types are 2/4/5/6 in all families, plus type7 in MW. Code and metadata
remain in their original section-indexed object form. The mock RELA test remains
a format control rather than a claim that these actual six objects contain RELA.

All six compiler exits and all six static decoder exits are zero; stdout/stderr
from compilation are empty and decoder stderr is empty. Every retained decoder
log hash reproduces its individual record. Different output paths appear in the
logs and outer reports, so those files are not claimed byte-identical. Whole-
object per-family identity is the repeatability result; no pathname/code
normalization is used to obtain it.

Independent inspection of the retained symbolic relocations and raw instruction
words confirms three different mechanisms in this fixture:

- GNU emits the static-initialization/destruction selector and initialization/
  destruction wrappers passing 1 or 0 with priority65535, with .ctors/.dtors.
- MW emits __sinit machinery in .init/.ctor, calling the derived constructor then
  __register_global_object with object/destructor bookkeeping.
- SNC emits __sti machinery with __cplinit, calling the derived constructor then
  __record_needed_destruction.

These call identities come from relocation symbol records. Printed jal0 targets
in the unlinked decoder output are not runtime addresses or evidence of calls
through zero. The GNU mechanism agrees with the earlier documented flag/priority
convention; this diagnoses a structural difference among these three fixed
producer configurations. It does not exclude every mode/version of MW/SNC, prove
an original compiler/global profile, or score any original target bytes. Current
source/default RTTI/exception/inlining context and the GNU modern-assembler
pipeline differ from unknown historical context and remain limitations.

No helper launches a real compiler or decoder for the actual audit, links or
executes an object, runs the game or changes an original draft/profile. The parked
initializer and all four retained drafts stay unchanged. Source-match/link/runtime
credit remains zero, and the last full tooling suite remains 340 WSL passes from
3U. A further diagnostic needs its own bounded reviewed plan; these observations
alone do not reopen matching or native-port implementation.
