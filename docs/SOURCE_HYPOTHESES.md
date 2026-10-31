> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Two fixed source hypotheses

Bucket 3C, 2026-10-30. This experiment tests two ordinary C interpretations of
the loop differences diagnosed in `PROBE_MISMATCH_DIAGNOSIS.md`. It changes no
compiler flags or original bench input. An exact emitted sequence would support
a source/configuration combination; it would not establish original source,
library ownership, source language or a unique historical compiler.

## Sources prepared before compilation

The baseline is `bench/compiler_probes.c`, SHA-256
`d5d588c184c7c95a86bb3772e760f9251d33e3e4aabf92dfc0449c6ddc7c7a95`.
Each alternative is a complete fourteen-probe copy. Only the declared function
body differs: every byte before its opening brace and after its closing brace
is identical to baseline, including purpose comments, signatures, typedefs and
all other functions. Rationale is recorded here so those comments stay unchanged.

| Full-bench copy | Only changed body | Size | SHA-256 |
| --- | --- | ---: | --- |
| `bench/hypotheses/compiler_probes_guarded_list.c` | `probe_08830654` | 4460 | `ed2c865775d70d857cec9f8f825ecb5a5925bf4d09379c10465f886602c7b1d1` |
| `bench/hypotheses/compiler_probes_pointer_bytes.c` | `probe_08830550` | 4425 | `2cd8899bd3ad3060e77cb0131c990f6f14ae4fd86879689a560b42f20dfb6ddf` |

Exactly one alternative per function is prepared. No assembly, register pins,
barriers, `volatile`, intrinsics or unusual expression orders are introduced.
Source files are not to be revised after observing compiler results. Independent
source review is required before the primary agent freezes or compiles them.

## Guarded list traversal

The original body uses a `while` loop. In all previous O1/O2 objects, its only
instruction difference from the target is the loop-entry branch at offset four.
The alternative expresses the target's initial null guard and subsequent
bottom-tested traversal directly, with ordinary structured C:

```c
{
    u32 count = 0;

    if (node != 0) {
        do {
            node = node->next;
            ++count;
        } while (node != 0);
    }
    return count;
}
```

The signature, `const ProbeNode *node` parameter, node type, unsigned count and
body order of next-pointer load then increment are retained. Null returns zero
without a node read. For a valid finite chain, both versions read the same
offset-zero links and return its length. Unsigned count overflow wraps modulo
2^32 on the target in both versions; no new signed overflow is introduced.
Cyclic chains do not terminate, and invalid/dangling links are outside the
ordinary-input model. This experiment adds no cycle detection or error behavior.

Prediction: an explicit guard plus a `do` loop may explain the target's guarded
entry without a different compiler setting. This is a source hypothesis, not a
claim that the original programmer wrote this exact spelling.

## Pointer-walking byte reduction

The original body indexes `values[index]`. The target instead advances its byte
pointer. The alternative keeps the same counted `for` loop, signed byte type,
local variable types, conditional assignment and result, while walking the
pointer explicitly:

```c
{
    int found = 0;
    int index;

    for (index = 0; index < 6; ++index) {
        if (*values != 0) {
            found = 1;
        }
        ++values;
    }
    return found;
}
```

For an input pointing to six valid readable `s8` elements, both versions test
the same elements in order and return zero or one. Neither exits early or writes
memory. A nonzero negative byte also sets the result. Pointer advancement ends
at the valid one-past position after the sixth element; it is never dereferenced
there. Null/short/invalid ranges are outside this ordinary-input model. The
six-iteration `int` counter cannot overflow; its original `< 6` test is retained.

Prediction: explicit pointer walking may explain address induction independently
of compiler selection. It does not request `movn`, change the limit comparison
to an equality test, or force delay-slot scheduling. Those previous mismatches
may remain, and that is a valid outcome of the fixed experiment.

## Review and comparison status

Independent pre-compilation review approved the exact hashes above: body-only
byte differences, preserved signatures/types/comments and thirteen controls,
ordinary-input equivalence, and absence of matching tricks. Both alternatives
were frozen before compilation; measured results are recorded separately below.
No compiler was invoked by the source author or independent source reviewer.
The primary agent owns the cohort runner and
repeat runs; the independent helper owns review and controls. The comparison
must use baseline and both alternatives
with the same eleven builds and eight existing whole-bench settings. All thirteen
unchanged probe functions in each alternative remain controls. Compare complete
symbols with the existing relocation checks; do not trim, mask or pad results.
`config/source-hypotheses.json` records the reviewed source/body/prefix/suffix
pins; its SHA-256 is
`a6d2ffde2156713897932638f8422947c7752276243926aaf8beb772c4dd4745`.
Report each full-bench copy separately rather than pooling favorable functions
or settings into an uncompiled combined score.

Any result-driven third source form, flag change, additional function or wider
experiment needs a later reviewed bucket. These two alternatives plus the
original drafts remain within the agreed plain-source attempt budget. No game
source is integrated, no function earns matched credit, and no game runtime test,
library classification, further overlay recovery or reconstruction is performed.

## Results after the freeze

The primary ran baseline and both full-bench alternatives across the same eleven
builds and eight settings, then repeated in a fresh directory: 264 objects and
3696 function comparisons per run. The reports are
`evidence/bucket-03c/final-experiment-run-1.json` and
`evidence/bucket-03c/final-experiment-run-2.json`. They are byte-identical,
2034441 bytes, SHA-256
`5fceb84ce537f189ea827ac4006b165547cd8a0e7c3dff89d04ae1c027999b35`.
The baseline cohort is identical to the accepted Bucket 3 baseline report.

| Full-bench copy | Changed function exact rows | Best complete-bench score | Unchanged controls per run |
| --- | ---: | ---: | --- |
| Baseline | Neither target exact in any of 88 rows | 6/14 | Original frozen reference |
| Guarded list | 0/88 | 6/14 | All 1144 comparisons agree with baseline |
| Pointer bytes | 0/88 | 6/14 | All 1144 comparisons agree with baseline |

The guarded-list function's bytes changed in 77 rows; the pointer-byte function's
bytes changed in all 88. These counts show that the alternatives affected code
generation without improving exact whole-symbol agreement. Scores and byte
counts are observations, not coverage or matched-game-function credit.

The source author inspected representative existing objects with system objdump
after checking their object hashes against the reports. In local run directory
`build/source-hypotheses-baxmplm9`, the guarded-list cohort is
`bench-bucket03-s0l0k9j9` and the pointer-byte cohort is
`bench-bucket03-7py844l7`. Checked examples were build 121/O1 and O3 and build
180/O3 and O4; no new compilation or source edit was used for this inspection.

The guarded-list prediction is partly confirmed: O1/O2 now produce an initial
null guard followed by a bottom-tested traversal. However, the 40-byte result
contains an additional nop at offset `0x14` between the count increment and
loop back-edge. This shifts the branch/return positions and displacements from
the 36-byte target. Higher settings emit 28-byte sequences with initialization
or counting scheduled into branch delay slots. No nop is removed or ignored
in the comparison, and the reason for that scheduling choice is not established.

The pointer-walking prediction is also confirmed at the instruction level:
the alternatives load through the advancing pointer rather than recomputing
base-plus-index. O1/O2 remain 60 bytes, O3 becomes 48, and O4/O4-p/O4-s become
52, compared with the 52-byte target. The target's `movn` assignment and fixed
counter-equality back-edge are still absent in the inspected optimized shapes;
they retain conditional branches and a signed less-than-six test. Some schedule
the pointer increment into the loop-branch delay slot. Equal size at O4 does
not close those differences.

These results explain two source-dependent structural effects but do not resolve
the complete mismatches or distinguish a unique build/configuration. They do
not establish the original types, C versus C++, ownership of the networking
helpers, or whether a separately compiled library used different tools/settings.
The toolchain stays unlocked. Both alternatives remain exactly as prereviewed;
no third form, compiler option, combined-source cohort or further experiment
has been introduced. The next step requires a separate reviewed plan.
