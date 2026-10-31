> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AL: first readable key-advance hypothesis tested

The single natural C++ method in `bench/archive_key_advance.cpp` compiles through
all four existing fixed C++/O2 pipelines. Both trials reproduce every complete
historical control object and every new candidate object. None of the four
complete candidate bodies equals the reviewed 140-byte target.

| Existing profile | Complete body | First differing byte | Result |
| --- | ---: | ---: | --- |
| Metrowerks 219 / C++ / O2 | 124 bytes | 5 | NONEXACT |
| PSP GCC3.3.3 package1.7.1 / C++ / O2 | 140 bytes | 0 | NONEXACT |
| SNC1.2.7503.0 / C++ / O2 | 116 bytes | 2 | NONEXACT |
| PSP GCC4.3.5 / C++ / O2, existing assembler profile | 100 bytes | 10 | NONEXACT |

Equal length is not a match. No register, scheduling, instruction, delay-slot or
padding difference is normalized away. GCC3.3.3 section padding outside its
function symbol remains outside the compared body; its entire symbol extent
still differs. All four candidates have complete validated extents and no code
relocations; no configuration is silently omitted from this result.

The draft has a purpose header, known field offsets and ordinary unsigned
multiply/modulus updates. It has no matching tricks. Ordinary fields are the
first explicit qualifier hypothesis, not recovered class information. Only this
one source form was tried, unchanged between profiles/repeats. This consumes
one plain-source hypothesis, not eight attempts for eight compilations.

Raw instructions distinguish the candidate pipelines: GCC3.3.3 emits reciprocal
multiply reductions, but its address formation, reduction/register/order details
and return delay slot differ. GCC4.3.5's retained compiler assembly itself uses
DIVU/check sequences; the assembler did not introduce those operations. The
Metrowerks O2 output also uses division and repeated address calculations.
These facts do not identify or exclude a whole original compiler family from
one unproved source context.

The compiler's already retained help distinguishes O2 from higher optimization
levels, including scheduling and strength reduction. That is a global-toolchain
investigation lead. No game-function flag was changed, no new configuration was
selected and the original toolchain remains unlocked. A separate capability
experiment can inspect invented code without changing any game diagnostic.

Before each candidate group, all four complete invented C++ producer objects
had to match both retained historical copies. Both independent reviews preceded
the source/profile/controller freeze. The exact-source Python loader bypasses
stale bytecode without rewriting old sources, binaries or caches. Twenty-seven
invented implementation controls cover source loading, sole-function metadata,
full-length comparison, control-first ordering, failures and preservation.

Independent reviewers read all sixteen ELF objects directly, without reusing
the controller's function selector, and verified 128 retained artifacts. They
confirmed symbol/section/relocation bounds, every complete comparison, all eight
whole-object repeat pairs and verbatim GNU assembly repeats. The only selected
function is the one complete declared global method, never a best-scoring byte
search. Raw mangled names and all object/log/assembly bytes are preserved.

Evidence is private under `evidence/bucket-03al/`: exact freeze, inherited
pipeline/control inventories, source-loader/extent/orchestration controls,
two final trials and both independent raw audits. The profile is
`config/archive-key-advance-experiment.json`. See
`ARCHIVE_KEY_ADVANCE_PIPELINE_REVIEW.md` and `BUCKET_03AL_VALIDATION_NOTES.md`.

The new routine remains explicitly DIAGNOSTIC_NONEXACT with one plain attempt;
it has not exhausted its source budget or been silently abandoned. Its next
action requires a separate bounded plan. The earlier initializer remains the
one parked routine with three plain attempts, one commented shape and four
retained drafts. Aggregate plain hypotheses now total four across two routines;
there are five retained game-source drafts, one commented matching-shape
function, zero register pins and zero empty-asm lines.

Credited matches and linked-source functions stay zero. The full-game build
gate and its18 negative tests remain unimplemented; the last full tooling suite
remains 352 WSL passes/no skips. No objects were linked or executed as game code.
The matching-before-port requirement and the deadline of16:21:44 UTC remain.
