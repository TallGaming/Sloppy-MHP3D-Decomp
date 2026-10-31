> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3Y independent validation

## Exact pre-execution capture-path review

This bucket uses only the unchanged invented grouped address fixture and the
already reviewed GNU1.7.1 C++/O2 profile. Each of two fresh trials compares the
ordinary immutable pipeline with a native capture path that adds only a verbatim
copy of the compiler's emitted assembly before the same pinned assembler. No
game draft or target is compiled/compared, no flag changes and no source tuning.

The helper approves these exact inputs before any of the four real compilations:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Existing `bench/address_reuse_grouped.cpp` | 1,200 | `04662faba3e8e68506928bb2d2623d25cf5e6a93f8f9fb1bde3e3dd223908094` |
| `config/gnu-assembly-capture.json` | 1,011 | `0d0e70fe7629a9f76a7f51083270b5219a09533f9d656cdb092c4e11cc29a262` |
| Fixed evidence capture driver | 11,374 | `043bf0c4caebc7b8c2d669afcae88f5ad4a7d2ba29f6769585829eb791f7a4b5` |

Real inherited input verification reproduces the fixed source/profile/pipeline,
compiler/support/assembler/host dependencies and preserved parked files. The new
capture code matches ordinary compile_profile's native /tmp staging, exact
source basename and probe.s name, compiler/assembler argv and cwd, timeout-tool
20-second limit and outer 25-second subprocess limit. It copies all assembly
bytes, including directives, comments and file metadata, without rewriting them.
The existing production pipeline/API remains unchanged.

Both paths check original/staged source bytes. The capture path checks native
assembly after the assembler, retained-copy identity, earlier control outputs and
all captured bytes before publication. Linked/nonregular inputs/outputs fail.
Compiler/assembler exceptions retain partial assembly/object identities and stage
streams without success. Ordinary-pipeline exceptions retain partial object
identity and stop before attempting capture. Decoder failures remain explicit.

## Meaningful mock-only controls

Ten capture scenarios independently pass without executing a compiler, assembler
or decoder: positive; original source mutation; staged-source mutation; linked
native assembly; assembler modification of native assembly; retained-copy
modification; linked output; previous-object drift; compiler timeout with partial
assembly; and assembler timeout with partial object. Mock subprocess checks also
assert exact argv, source basename, probe.s, cwd and limits against the existing
profile. Invalid paths/bytes cannot become parity success.

A separate ordinary timeout-partial control checks its retained object hash and
verifies capture/publication are not attempted. These are fixed one-off review
controls, not new production tests. The last full WSL tooling suite remains 340
passes from 3U, separate from this experiment and the future full-game gate.

## Actual object/assembly repeat audit

Both fresh actual trials are complete. Their build directories are
`build/gnu-assembly-capture-cjxdcgvg` and `build/gnu-assembly-capture-4nu26rfp`.
The preceding 871-byte freeze, SHA-256
`bb617549ec8d2172a94e86e19f6d7bf1afb306e0456cf01ccbae917f0f500e79`,
records both exact final approvals and reproduces all source/profile/driver pins.
All inherited source/tool/pipeline/assembler/host and parked-input identities
reverify afterward; neither the old API nor any game draft changes.

| Artifact | Bytes | SHA-256 / repeated relationship |
| --- | ---: | --- |
| Complete ordinary and capture objects | 1,204 each | All four equal `22690e399773b59c25a0b3966312c5f6465c9d96690d5a91dba274b78ee80523` |
| Verbatim retained emitted assembly | 995 each | Both copies equal `9c1aabe61e5c0de8e02071f3759d294a1936833266514bd964d17281512a1078` |
| Complete sole function | 64 each | All equal `938610c5f086bf6422c724621a7955766f22fd3fc156e7fd68a2fadc7182be4e` |
| Trial 1 report | 3,451 | `21cddb1b1f29c6e485385eec99a2502d531ac896fe8d30e0723780c1a0389b84` |
| Trial 2 report | 3,451 | `3ade8a7bcd903fbe74a6f7b5afd07d4244aacf7082d559e53a56872cdf9d3a1f` |

Independent readback compares all four complete objects, both complete assembly
copies, the single complete symbol and all sixteen encoded instruction words.
Each ordinary pipeline's returned assembly SHA equals the retained capture
assembly SHA. Its temporary assembly is not separately retained, so that latter
comparison is explicitly hash parity; the two capture copies and all four
objects are compared byte for byte. No metadata, .file line, comment, instruction,
padding or pathname is removed to obtain object equality.

Both real capture stages use the exact reviewed compiler/assembler commands,
source basename, probe.s and shared native temporary cwd. Stage logs and the
ordinary records reproduce the report. Every compiler/assembler return is zero,
with empty diagnostics. Both static decoder returns are zero with empty stderr;
each decoder log matches its individual hash. Temporary paths in logs/reports
differ and those whole reports are not claimed byte-identical.

## What emitted assembly establishes, and what it does not

The raw compiler output already contains a load-immediate of 65536, ORI 0x8000 and
ADDU to form receiver+0x18000, followed by field displacements 8480/8484. That
arithmetic produces the invented offsets 0x1A120/0x1A124. The assembler encodes the
large immediate as LUI; the selected base and additional ORI are already present
before assembly. The assembler did not invent that address-splitting choice.

The compiler output also explicitly pairs each BNE with its default-value LI
under .set noreorder/.set nomacro. These branch-delay instructions are already
scheduled in the captured .s, rather than introduced later by this assembler.
The final `j $31` has no explicit following NOP in .s, while the object contains
JR RA plus NOP: that final delay-slot filler belongs to assembly in this observed
pipeline. The fixture has no move pseudo, so it supplies no direct observation
of move's assembler expansion; primary-source comparison is a separate lead.

This experiment validates capture parity for this one frozen fixture/profile.
It is final emitted assembly, not compiler IR, a trace of individual optimization
passes, proof of every input's neutrality or an original historical toolchain.
Upstream backend-version differences may motivate a separately reviewed candidate
investigation, but do not justify per-function flag tuning or source changes.
No actual compiler/assembler/decoder process is launched by this helper, no game
draft or target is compiled and no source-match/runtime/link/gate credit is added.
The initializer stays PARKED with all attempt/trick counters unchanged. The last
full WSL tooling suite remains 340 passes from 3U.
