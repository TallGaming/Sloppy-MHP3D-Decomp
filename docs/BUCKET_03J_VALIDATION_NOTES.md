> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3J independent validation

2026-10-30. **Grouping the two invented fields changes neither complete object
bytes nor function bytes in either trial.** Both layouts produce the same
100-byte function with five statically identified large-base sites. The measured
static-site reduction is zero. This is a bounded result for these two fixtures,
not proof of a compiler pass, aliasing mechanism or the original game's layout.

## Before either fixture was compiled

The helper reviewed both readable C++ sources and their exact pins before any
fixture output. Direct fields and `KeyState` subobject fields have the same
owner/method signature, four-byte scalar widths, volatile qualifications,
invented offsets `0x1A120`/`0x1A124`, record extent `0x1A128`, and defaults
`0x1357`/`0x2468`. Both write upper then lower, optionally write the lower
default, read upper and optionally write its default. The grouped form uses
`state.member` directly: no cached pointer/reference, helper, virtual member,
assembly or register constraint was introduced. These are invented records,
not a second game-source candidate.

| Reviewed source | Bytes | SHA-256 |
| --- | ---: | --- |
| `bench/address_reuse_direct.cpp` | 1058 | `9def28de2b740f255cc379e7468f54dcdbbe3be367efd442170d7ae84dcff3ae` |
| `bench/address_reuse_grouped.cpp` | 1200 | `04662faba3e8e68506928bb2d2623d25cf5e6a93f8f9fb1bde3e3dd223908094` |

The reviewed profile draft was 1508 bytes, SHA-256
`5818d2a39d9c8fcd6917bcdb6ed5e071f7626f1f41b8c9576e766ceee0333bf4`.
The frozen `config/address-reuse.json` is 1509 bytes, SHA-256
`614238f14ac02863dec2821e9b9ade3d002e6946a3116b494e9b758e1864f5f1`.
Reversing only the status-value change reproduces the reviewed draft hash.
The historical pre-compilation declaration records the freeze point; it is not
a statement that later trials have not run.

The command stays the existing unmodified MW219 pipeline with
`-nostdinc -lang c++ -c -O2`. The exact method symbol remains the previously
validated `initialize_key__17ArchiveKeyContextFUi`. Neither source, layout,
flag set nor scoring policy was adjusted after outputs. The Bucket 3I game
candidate and all original fourteen-probe inputs remain untouched.

## Static-analysis review and invented controls

The helper reviewed the classifier before compilation and exercised nine pure
ELF/instruction controls before approving the experiment. The analysis first
requires a complete valid ET_REL function and rejects unsupported code
relocations. The abstract CFG walker tracks constants and receiver-relative
offsets through an explicit whitelist, explores both unknown forward-branch
outcomes, and requires NOP delay slots and the expected access paths.

Loads kill destination provenance, `$zero` remains immutable, and return-address
provenance must survive. Unresolved addresses, unsupported instructions/calls/
loops, invalid targets/delay slots, uncovered nonpadding instructions and state/
path limits leave the analysis `UNINTERPRETED`, with **null counts and traces**.
A valid object with uninterpreted addresses still retains its complete bytes.
It receives no manufactured zero count or reuse advantage.

The site metric counts the union of static large-constant receiver-ADDU
instruction positions that contribute to actual memory bases across validated
paths. Unused address arithmetic is excluded. It is neither dynamic execution
count nor total arithmetic cost. The access traces concern offsets/order, not
stored values, concurrency, source semantics or a runtime performance result.
No guest code is executed by this abstract analysis.

`tests/test_address_reuse.py` contains 19 tests. Independently constructed
17-word shared-base and 25-word repeated-base vectors validate the same four
access traces and yield one versus five sites, with the shared position counted
once. Other pure controls cover branch-skipped definitions, loaded/masked/
clobbered bases, `$zero` writes/loads, return-address overwrite/load, unknown
instructions, calls, loops, delay slots, wrong offsets/order and budgets. ELF
lengths, symbols, executable bounds and relocation rejection remain mandatory.

Runner fixtures preserve the real nested Bucket 3I/3H validation using invented
inputs; only compiler calls are mocked. Controls retain both case outcomes,
keep an independently valid case after another fails, prevent unknown analysis
from becoming an advantage, and compare complete function bytes including
padding. They reject additional/reordered/cached-address cases, changed scope,
input/profile mutations, altered earlier objects and report/input aliases or
conflicting evidence. The helper independently ran the full suite:
**258 passed, zero skips**, including these 19 new tests. These are tooling
checks, not the full-game gate's required 18 negatives or any source-match proof.

One final classifier limitation was identified during primary review: a series
of small ADDIU operations could reach the same fields without a large-constant
ADDU and previously receive an interpreted zero count. The primary tightened
the model to require large-ADDU lineage for every memory base and collect only
lineage sites actually used by memory accesses. New controls confirm that the
small-addition chain is uninterpreted, while unrelated unused large-address
arithmetic does not inflate the count. This narrows interpretation; it changes
neither source, compiler flags, complete byte comparison nor actual trial data.
The helper reanalyzed all four retained objects with the hardened classifier;
their complete observations exactly reproduce the existing reports. No fixture
was recompiled for that check.

## Independent final artifact audit

The reports `evidence/bucket-03j/address-reuse-run-{1,2}.json` are byte-identical:
12,442 bytes, SHA-256
`40d44289975dc68110491b7c78512c230cc1ccfdf4b88922318be4c7a3f7cf0e`.
The two fresh roots are:

- `build/address-reuse-o2mm0k1m`
- `build/address-reuse-8e3b12xv`

Each contains one direct and one grouped object with empty diagnostic logs and
exit zero. All four objects are 768 bytes with identical SHA-256
`775c998a2213ab73a0458f44dc6357336afe8fea2d9b2e30f90d637e4fed101c`.
Each has exactly one complete 100-byte function, SHA-256
`5eec7bae467bb2a578f0aad3754d54ce6b8c7bb6875dea43b24150fce6d2c0fe`.
The helper independently reparsed every object's function identity, full bytes,
metadata, source identity and diagnostics against the reports.

Separately from the production classifier, the helper tracked the actual
invented outputs' receiver-relative addresses across both branch choices from
their existing instruction words. All four objects have the expected four
static access traces at the declared fields and the same five large-base ADDU
sites at byte offsets **12, 24, 48, 60 and 84**. This verifies the recorded
static metric without executing either fixture or validating game behavior.
The report correctly separates complete byte identity from its interpreted
address comparison with zero static-site reduction. No byte was masked,
trimmed, patched or substituted.

The helper recomputed **204 local pin records and 11 native dependency records**;
all match current bytes. Duplicate declarations count as records, not distinct
files. This includes both fixtures, the inherited tools, analysis inputs and
the unchanged Bucket 3I candidate. No original ISO was opened or modified.

## Final implementation identities and limits

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `scripts/bench_address_reuse.py` | 16286 | `5aefa4160aa2ad40aa114b1d696b085b98edd73a606bee56d983a88f4e7dcf99` |
| `tests/test_address_reuse.py` | 21316 | `7aa8c54a471f5c15d91415215fb9fa1272c0c5c0337ee23ed76474419f292af6` |

The measured equality does not prove that grouping never affects code generation
or identify why this compiler repeats the address calculation. No third fixture,
cached-address form, compiler option, tool candidate or game-source revision was
tried. No game target was scored, linked or executed; there is no new source
attempt against the Bucket 3I function. Toolchain attribution remains unresolved;
game-match/source-link credit, parked functions and counted matching tricks
remain zero. Stop at the Bucket 3J review checkpoint.
