> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3 independent validation notes

Reviewed on 2026-10-30 by the validation helper. This is compiler-investigation
tooling review. No game code was executed or reconstructed; no source-match,
full-build or matching-gate credit is implied. No commits were made.

## Automated checks

From `<project-root>`:

```powershell
python -m unittest discover -s tests -v
```

Result: **95 tests passed** (exit 0): all 70 existing tests and 25 new bench
tests. Fixtures contain invented ELF/probe/compiler/runner/support-file bytes.
Integration tests mock compilation; they do not execute a proprietary compiler.

The new checks cover:

- Section-indexed function extraction with repeated `.text` names; exact versus
  partial bytes, unequal lengths and the first differing byte. A matching prefix
  is not counted as exact.
- ET_REL/MIPS requirements; missing, unexpected, duplicate, overlapping,
  nonexecutable, empty, unaligned and out-of-bounds functions.
- REL and RELA in probe code are rejected. Invalid relocation record layout,
  linked symbol table, target section, symbol index or offset are rejected.
  This bench performs no relocation resolution.
- Empty manifests, duplicate names, overlapping/unaligned targets, wrong target
  hashes and unsupported manifest relocation declarations fail closed.
- A complete two-candidate/two-setting synthetic matrix uses the same fixed
  source and whole-bench flags. Repeats use distinct fresh object paths and
  produce identical reports without temporary paths or timestamps.
- Candidate/setting identifiers must be unique and the matrix must be nonempty.
  Source, manifest, reference, runner, compiler and support-file pins are checked;
  input or metadata changes during compilation invalidate the matrix.
- A compile failure, diagnostic warning, timeout, missing object or invalid
  object emits no successful matrix report. A stale object elsewhere cannot
  substitute for new output. A failure remains a failure even with a valid object.
- Conflicting reports and report/input aliases preserve existing files. Failed
  compilation retains diagnostics in its local log.
- The real invocation wrapper passes empty stdin and a bounded timeout without
  invoking a shell. Only this subprocess call is mocked in that wrapper test.

## Independent probe and metadata review

The validator separately checked all 14 manifest intervals against the pinned
PSP ELF: 444 target bytes total, all target hashes correct, word-aligned
boundaries including each final `jr ra` and its delay slot. No JAL instruction
occurs inside the intervals. The manifest declares no relocations and retains
unclassified game/SDK/third-party ownership for every probe.

The source uses ordinary C and records uncertain field meanings, signatures and
behavior. Code-generation agreement cannot validate those hypotheses or prove
the original source language. In particular, the six larger additions still
exercise leaf code: calls, global-address relocations, floating point, C++ object
layout, exceptions, assembler behavior and final linking are not covered.

The target's linked `.comment` contains `MW MIPS C Compiler (2.4.1.01)` and `PSP`,
and its ELF flags are `0x10A23001`. The tested compiler objects contain
`MW MIPS C Compiler (3.0.0)` with flags `0x10970001`. These are real metadata
differences, but linked executable and relocatable-object metadata have different
provenance possibilities. They neither prove an original compiler version nor
disqualify all tested candidates by themselves.

C++ runtime/demangler strings in the linked executable support the presence of
C++-related library code; they do not establish that the game's own code was
written in C++. The bench deliberately selects C as a probe language, not as a
historical-source conclusion. Installed GNU MIPS assembler/linker tools are not
an established PSP reconstruction toolchain.

## Independent readback of the final matrices

The validator read both complete reports and all retained object files without
rerunning a compiler. Both reports contain 88 rows with 14 comparisons per row,
and `matched_progress` is zero. The reports are byte-identical: 552555 bytes,
SHA-256 `9e36e6753a49730eb90fa66cfc31f19bef726e541a853eb85cb9504abbecb046`.

Reports:

- `evidence/bucket-03/final-bench-run-1.json`
- `evidence/bucket-03/final-bench-run-2.json`

Retained object sets:

- `build/bench-bucket03-6dfxf3bd/`
- `build/bench-bucket03-_ge5pqk7/`

All **176 objects and 2464 comparison records** were read back. For each row,
candidate/setting IDs and whole-bench flags agree with the current configuration;
the object hash agrees with the actual file; and every function's reported
length, compiled hash, target hash, exact boolean and first differing offset
agree with the actual section-indexed bytes and pinned reference. Each internal
build report equals the named final report.

The current source, manifest, candidate configuration and reference-lock hashes
agree with report provenance. The pinned reference ELF also agrees. All 23
runner/compiler/support-file pins, 11 downloaded archive hashes and 11 persisted
help-file hashes were independently verified.

All builds score 6/14 exact probes at levels 1 and 2, and 1/14 at the other
settings. None of the six larger probes is exact anywhere in this matrix. Equal
scores conceal different generated bodies: there are four observed body groups
at default/level 0, two at levels 1 and 2, and three at the higher settings.
Consequently these results identify neither a unique compiler nor justified
project flags. They also do not disprove the source hypotheses on their own.

## Reviewed source identities

| File | SHA-256 |
| --- | --- |
| `scripts/bench_compiler.py` | `ab6b3c441c762180f3e0269cc4ea07c4d5e3c4801136907cc93ac1495db94d5c` |
| `tests/test_bench_compiler.py` | `6fb5c852b3db6701bb284524f257ca53b6ba8bbab586fe90f2e7cc6706d4a7b0` |
| `config/compiler-candidates.json` | `9ba0d75472c7a1ceb45ffdbc46c50d3ffa119c3315be0e93c2f9f8ada4099147` |
| `bench/compiler_probes.c` | `d5d588c184c7c95a86bb3772e760f9251d33e3e4aabf92dfc0449c6ddc7c7a95` |
| `config/compiler-probes.json` | `2a3a7783a11704c870311470cf851434ec1e0a660af29787db48178b2c58ffbc` |

## Review findings and limits

The independent artifact audit caught help-output hashes computed from
newline-normalized text instead of persisted Windows CRLF bytes. All 11 help
pins were corrected to the saved bytes before the final matrix runs. Compiler,
support-file, source and setting bytes were unchanged by that correction.

No material blocker was found in the reviewed bench paths. Timeouts prevent
success reports but propagate before per-row log creation; that is a diagnostic
limitation, not a stale-output fallback. A complete successful bench still
cannot establish historical source, exact flags, a full compiler/assembler/linker
lock, linked reconstruction or gameplay behavior. Any toolchain proposal needs
the separate user checkpoint required by the bucket plan.
