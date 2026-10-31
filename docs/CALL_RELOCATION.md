> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Controlled external-call relocation

Bucket 3B adds a separate invented diagnostic. It does not change the frozen
fourteen-probe bench, relocate original game functions or construct a linked
game object.

## Fixture and command

[direct_call_fixture.c](../bench/direct_call_fixture.c) calls one declared
external function and adds one to the result. This prevents a tail jump while
keeping the source ordinary C. Its compiler flags are fixed at
`-nostdinc -lang c -c -O2` for every one of the eleven candidates. This diagnostic
setting is not a game compiler selection.

From `<project-root>`:

```powershell
python scripts/bench_direct_call.py --report evidence/bucket-03b/my-call-review.json
```

The runner uses fresh objects, pinned compiler/DLL/runner/source/configuration
identities, bounded execution and diagnostic checks. It checks pins again before
publishing a complete report and preserves existing conflicting reports. All
objects, logs and resolved synthetic function bytes stay under ignored `build/`.
The report records their hashes and every changed call word.

## Observed form and supported calculation

The real fixture objects contain a 36-byte global function. A REL record at
section-relative offset 8 names the undefined global `fixture_external` symbol
with relocation type 4 (`R_MIPS_26`). Its original JAL word is `0x0C000000`, so
the implicit addend is zero. The symbol is global, undefined and NOTYPE, with
zero value/size and default visibility.

[direct-call-fixture.json](../config/direct-call-fixture.json) explicitly assigns
invented addresses: function `0x08810000`, external symbol `0x08840000`. The
expected resolved instruction is independently declared as `0x0E210000`.
These addresses do not identify or link any game function.

[call_relocation.py](../scripts/call_relocation.py) supports only this external
REL/JAL form. The external-symbol addend is the signed 28-bit value from
`imm26 << 2`; the resolved target is `S + A`. Its upper address bits must agree
with the JAL delay-slot address, `P + 4`. Only the instruction's 26-bit target
field is replaced. This external-symbol rule follows Figure 4-11 of the
[MIPS ABI supplement](https://www.uclibc.org/docs/psABI-mips.pdf); the modern
[LLVM linker implementation](https://github.com/llvm/llvm-project/blob/main/lld/ELF/Arch/Mips.cpp)
also decodes the implicit MIPS26 addend with signed 28-bit extension. The delay
slot and every other function byte are preserved.
Section-relative relocation places are translated using the function's actual
section offset. The explicit plan must match the symbol, offset and addend.

Signed nonzero addends and the `P + 4` region boundary are covered by invented
known-address test vectors. The actual compiled fixture exercises addend zero.
Local/section/weak symbols, undefined address assignments, non-JAL code, unsupported
code relocations, RELA, duplicates, malformed tables, unaligned or overflowing
addresses, out-of-region targets and missing/extra call plans are rejected.
Address-space wrap at `P + 4` is outside this diagnostic's supported model.

## Explicitly unlinked metadata

The compiler also emits a non-executable `.mwcats` section, using Metrowerks
section type `0xCA2A82C2`, with an `R_MIPS_32` record pointing at the function.
That record is bounded/validated and reported **unapplied**, outside the selected
function-byte scope. It is not masked or counted as resolved. The output is a
resolved synthetic function byte string; it is not a linked ELF or a promise
that other relocation forms are implemented. The original game bench continues
to reject all unresolved code relocations.
