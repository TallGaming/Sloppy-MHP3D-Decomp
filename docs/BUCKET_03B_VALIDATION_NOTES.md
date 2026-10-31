> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3B independent validation notes

Reviewed on 2026-10-30 by the validation helper. This validates a narrow
invented-call diagnostic and reviews static analysis evidence. It does not link
an object, reconstruct game source, run the game, select a toolchain or implement
the matching gate's 18 negative checks. No commits were made.

## Automated checks

From `<project-root>`:

```powershell
python -m unittest discover -s tests -v
```

Result: **130 tests passed** (exit 0): all 95 existing checks and 35 new checks
(19 relocation controls, 11 fixture-runner checks and five Ghidra-export
validation checks). New fixtures contain invented ELF/instruction/tool bytes;
negative tests mutate only in-memory objects or temporary files.

The new checks cover:

- Known JAL address words, zero/positive/negative signed 28-bit implicit addends,
  and preservation of opcode, delay slot and all other selected function bytes.
- The region comes from `P + 4`, including a call at `0x0FFFFFFC` into the next
  256 MiB region. Wrong-region calls, bad alignment, invalid scalar/address
  ranges, addend underflow/overflow and the unsupported 32-bit wrap case fail.
- A defined global function and a unique, default-visibility, undefined global
  external symbol are required. Local, weak, section, hidden, defined, ambiguous
  and malformed external forms fail. Both NOTYPE and FUNC externals are covered.
- Call plans require the exact relocation offset, external name and addend;
  missing, extra, duplicate, unaligned and mismatching plans fail. Section-relative
  relocation offsets are correctly translated to a nonzero function offset.
- Only REL `R_MIPS_26` on JAL code is applied. RELA, other code relocation types,
  non-JAL words and a call without an in-function delay-slot word fail.
- Duplicate relocation locations within or across relocation sections fail.
  Truncated records, bad links/indices, out-of-bounds or unaligned places,
  malformed functions and overflowing assigned function ranges fail.
- The observed non-executable `R_MIPS_32` metadata form is validated and reported
  explicitly as unapplied. Other non-code forms are rejected. Returning selected
  function bytes makes no claim about a completely linked object.
- The fixture runner uses one fixed flag set for every candidate, checks source,
  compiler, runner, support-file and configuration pins, recompiles into fresh
  paths and produces identical path-free reports on repeat. Compile failures,
  warnings, timeout, missing/stale/invalid objects, unsupported relocations,
  an incorrect independently declared word or changed inputs prevent report
  publication. A late candidate failure emits no partial score report; existing
  reports and inputs remain preserved on failure or alias/conflict attempts.
- Synthetic Ghidra-export checks require the processor, ELF identity, image base,
  main-text mapping, target hashes, exact target bodies and completed target
  decompilation. Missing/duplicate/extra call references fail against a raw JAL
  scan. A caller must be exported, cover its call site and have completed
  decompilation; an unrelated existing function cannot substitute for it.

The external-symbol addend convention follows the
[MIPS System V ABI, Figure 4-11, page 4-19](https://www.uclibc.org/docs/psABI-mips.pdf).
Its local/section-symbol convention differs and remains unsupported. The `P+4`
boundary vector follows the JAL definition in the MIPS Technologies
[MIPS32 Architecture for Programmers, Volume II](https://courses.cs.washington.edu/courses/cse378/documentation/MIPS32_Architecture_For_Programmers_Volume_II.pdf).
The actual compiler fixture has addend zero; nonzero-addend controls are synthetic
ABI tests, not evidence that the compiler emitted those cases. The independently
read [LLVM MIPS linker implementation](https://github.com/llvm/llvm-project/blob/main/lld/ELF/Arch/Mips.cpp)
also sign-extends the shifted implicit field to 28 bits; it is supporting
algorithm evidence, not a selected game linker or a Metrowerks-linker experiment.

Review found that duplicate metadata locations split across separate REL
sections initially lacked a global duplicate check. The primary added that check;
the final tests reject duplicates in both code and metadata sections. Review
also prompted explicit caller-body/completed-decompilation validation in the
Ghidra checker. Both fresh real exports pass the updated checker.

## Independent static diagnosis checks

The validator independently compared the frozen list-count interval against
all 22 existing O1/O2 objects: each is 36 bytes and differs from the target in
exactly one instruction, at offset four. Equal sizes and substantial instruction
agreement still fail exact whole-function equality. This supports the diagnosis
of a loop-entry layout difference; it establishes no historical source shape.

The validator also independently parsed the main ELF's `.lib.stub` and NID
arrays. Library `sceWlanDrv`, NID `0x0C622081` maps to stub `0x089610D0`;
`sceNetAdhocctl`, NID `0xE162CB14` maps to `0x08961110`. The community PSPSDK
[WLAN declarations](https://github.com/pspdev/pspsdk/blob/master/src/wlan/sceWlanDrv.S)
and [adhoc-control declarations](https://github.com/pspdev/pspsdk/blob/master/src/net/sceNetAdhocctl.S)
agree with the EtherAddr/GetPeerList names. Its
[peer-list header](https://github.com/pspdev/pspsdk/blob/master/src/net/pspnet_adhocctl.h)
places a six-byte address after a pointer and 128-byte nickname, consistent with
the observed offset 132 on PSP. This identifies imported interfaces; it does
not identify the local wrappers or either probe as Sony SDK code, nor establish
the original game language or exact historical SDK structure.

## Real direct-call fixture audit

The validator independently read both complete fixture reports, all 22 retained
compiler objects and all 22 selected-function outputs. Both reports are
byte-identical: 9867 bytes, SHA-256
`5e99ad0c3ab2eef48313f9b8f0420a6eaedf769f53b05307a208a20de129c463`.

Reports are `evidence/bucket-03b/final-call-run-1.json` and `final-call-run-2.json`;
their raw artifacts are in `build/direct-call-0o6xi3p5/` and
`build/direct-call-p_kh2hcy/`. Configuration/source hashes agree with report
provenance. Every object and output hash agrees with the actual bytes.

All eleven candidates emitted an ordinary REL `R_MIPS_26` at function offset
eight, referring to a default-visibility undefined global NOTYPE symbol,
`fixture_external`, with implicit addend zero. The function is 36 bytes. Each
selected output differs only at that JAL word: `0x0C000000` becomes
`0x0E210000` for invented place `0x08810008` and assigned symbol `0x08840000`.
An independent instruction-target calculation recovers `0x08840000` from every
output. Delay-slot and remaining bytes are preserved. Each object also has one
non-code `.mwcats` `R_MIPS_32`, reported as unapplied. No original game-function
address or bytes participated in this diagnostic; `matched_progress` stays zero.

## Pinned Ghidra import/export audit

The validator independently checked all 5751 installed manifest entries,
including 205 symbolic links, through WSL's native filesystem semantics. Every
file/link, all three downloaded archives, the manifest itself and the Java
export script agree with their pins in `config/analysis-tools.json`.

Two fresh projects produced byte-identical exports:
`evidence/bucket-03b/ghidra-final-run-1.json` and `ghidra-final-run-2.json`,
68494 bytes, SHA-256
`a2957127574e6791345caee470056ca1a64a7fe218335492ee4f291e3db8a091`.
Both summary reports agree with their export/configuration hashes and with an
independent rerun of the current export validator.

The PSP ELF loader uses `Allegrex:LE:32:default`, compiler specification
`default` and image base `0x08804000`. Its main `.text` block agrees with the
original ELF's start and size `0x15C9E8`. Both target memory hashes agree with
the reference and frozen manifest; Ghidra's target bodies cover exactly 52 and
36 bytes. All 34 selected function/caller decompilations completed, including
the intervening six-byte-copy helper at `0x088305DC`.

The export contains 34 direct calls to the six-byte reduction in 26 distinct
callers, and one direct call to the list counter. The validator independently
decoded every reported call word from the pinned ELF and confirmed its target.
The raw whole-text JAL scan agrees with both exports; every reported caller is
present and its body covers the call site. The pseudocode supports the basic
loop observations, but generic `int *`, `undefined4`, signatures and automatic
names remain hypotheses. Missing or inferred arguments must be checked against
the instructions before source or ownership claims.

The imported workspace omits runtime memory/overlay reservations and gives some
data blocks executable permissions. Those properties are not whole-memory
reconstruction or code classification. The ELF map remains the reservation
evidence, and Ghidra's automatic labels do not identify local code as a library.

## Reviewed source identities and conclusion

| File | SHA-256 |
| --- | --- |
| `scripts/call_relocation.py` | `fd68e1a9db44d3ed159938c10c85e3a1735a3f3e815e8a372f2b75f3ebf8d860` |
| `scripts/bench_direct_call.py` | `93cab70e418b81cacfd8ade89b02883aedbd7e2228ce8440ebd995baa4fc77db` |
| `scripts/analyze_reference.py` | `ee2ac39a0861340c0283f54dfa8b2f1505804498f20a61787a0af26d5895485b` |
| `scripts/ghidra/ExportProbeAnalysis.java` | `3eba0650f66a14245628b9cc4172a7335c2c114e23245ebccf121b1a7929773a` |
| `tests/test_call_relocation.py` | `cdebe8d2a38966259536d1161c345225d1417569986a3b5fe9259436447d0d0a` |
| `config/direct-call-fixture.json` | `382fa252cfa2e1f38bd34292d57d84b76b8bb60c29a0501e1c5388a2ea96b2f9` |
| `config/analysis-tools.json` | `5aa6760392c96d152b3f8524b809b29e2324aeedda0255de5b484cedfc465eb7` |

No material blocker remains in the reviewed paths. The invented fixture proves
this narrow direct-call calculation and repeatability, not full linking or game
matching. Static analysis supports the documented networking context and loop
diagnosis; original ownership, source language, compiler flags and a complete
build chain remain unresolved. The frozen game probes and flags were not
changed, and no game function receives match credit.
