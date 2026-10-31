> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AD independent validation

## Stage A contract

Use only the source-backed unsigned little-endian wrapper length at raw offset4,
after verifying at least eight raw bytes. The declared boundary must be positive,
strictly inside the complete retained payload and within the fixed bound. No
constant offset, alternate magic scan, repaired field or guessed executable
extent is permitted. Record the complete exact remainder identity. Only a
complete supported ~PSP header at that exact boundary is eligible; everything
else remains uninterpreted. OPNSSMP is a separate offset-zero candidate, not a
wrapped archive entry. Main EBOOT is only a later mandatory decryption control.

Both retained 3AC sets and their manifests must agree before new copies. Pins,
path guards, fresh staging and complete byte/manifest checks must prevent output
publication on source-set disagreement, input/output drift or conflicting
existing paths. Two independent Stage A copies/reports establish repeatability;
this stage performs no decryption or executable launch.

## Exact pre-execution review and controls

The helper approves these exact Stage A inputs before its freeze and both
actual copy/metadata runs:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `config/sce-wrapper-model.json` | 1,516 | `abc44e51d6f922ab55100b6b985b90c31cadbdab204a820aea2690b66413a841` |
| Fixed Stage A driver | 9,192 | `e0fcc53579404af4ea6f6b2f68683c76a69352e936aaadc59cac6b7739331b99` |

Three invented positive vectors validate offsets8,64,101. Seven rejected
raw declarations cover short headers, wrong magic, zero, boundary equal to
payload size, beyond-payload size and the fixed one-MiB maximum. Four supported
boundaries with truncated PSP, unknown/zero bytes, or a later decoy PSP magic
retain their full exact remainder and remain ineligible. No alternate offset is
searched. Seven mock-only run scenarios pass: full positive, existing report,
existing output, late pin drift, same-size source mutation during late
verification, staged payload mutation and extra staged file. Failures preserve
prior evidence and publish no successful normal report or new bundle.

Before freeze, this helper requests a snapshot recheck after late verification;
the primary adds it immediately before final staged/path audits and rename.
The other reviewer requests a report-parent-chain recheck beside exclusive report
creation; that is also present in the exact approved source. The helper reads
back both guards, reruns a pure boundary positive, and verifies actual prior
sixteen-payload/manifest/source pins without preparing any real inner payload.
No external compiler, decrypter or executable is launched by these controls.
These bounded review controls are separate from the unchanged352-test suite and
the unimplemented game matching gate.

Stage B requires separate source/profile/command/control review and freeze after
completed Stage A audits; Stage A success alone does not authorize decryption.

## Stage A actual output audit

Both actual Stage A sets contain the five eligible complete inner payloads.
The helper independently reads the four raw wrappers' little-endian declarations:
all four happen to be64 bytes. Each copied inner equals the complete remainder
at that exact declared boundary;64 is an observed value, not an assumed fallback.
OPNSSMP equals its entire unchanged offset-zero input. All ten copies across the
two sets are byte-exact, and their metadata recomputes exactly.

| Input | Complete inner bytes | SHA-256 |
| --- | ---: | --- |
| Archive17 | 20,624 | `61f19d0baa5bf2308e3ec3b8f93b4ba01b8af6d7db7fa788a5d0aa293884ab57` |
| Archive18 | 1,056 | `914f0b17d13219633c58dfa31d343ca136d7708c6a433be80f69d744b999babf` |
| Archive19 | 20,624 | `242cf2fa02c13e53c97453e300364d7a6418e21e745b43a6e57fe7237a383fd3` |
| Archive20 | 1,056 | `5078d29f52617811c574b836e8a5cb32748b99c9e2ca1da846bdfe85e061048a` |
| OPNSSMP | 3,264 | `1711d003bd744c28010e856f48c633a8b2a7a63cdae5f01d9ccd9f0ec3d49417` |

The four inner headers declare names sceFont_Library (17/19) and
sceBASE64_Library (18/20); these remain unauthenticated metadata, not SDK ownership
identification or a license to exclude code. The OPNSSMP declared name is one
space. The helper verifies complete supported headers precisely at the declared
boundaries, not magic discovered by scanning.

Both 9,016-byte reports and bundle manifests are byte-identical with SHA-256
`8405266c9100e45d0bab3c8c34600ee4e9575001abeae4a05cb52d463c17e105`.
The 702-byte pre-execution wrapper freeze has SHA-256
`906b03c3abe257cb9b66e3cc545dea3a459068de5d527c8761a308a7826317f2`.
Complete output sets, original sixteen payload/manifest snapshots, nested
preserved source/profile pins and exact freeze identities all pass after audit.
No decryption or executable launch is performed in Stage A.

## Stage B pre-execution review

After both Stage A audits, the helper approves the exact separate Stage B
profile and driver before its freeze and twelve declared helper invocations:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `config/module-static-preparation.json` | 5,078 | `64e74c98f2560e6e0eb49d79976198850b1e748066cd4145243cab724f240784` |
| Fixed Stage B driver | 14,310 | `75b928004528783e5c6ee3227b9ee5a9771a421b056f6d4322c204fc95fad162` |

The command uses the existing exact pinned helper and one unchanged invocation
per input, with20-second bounds, empty stdin, captured streams and LC_ALL=C.
The existing EBOOT must first produce its entire known ELF exactly before any
new candidate in each trial. The helper's zero exit alone is insufficient:
stdout must be the exact successful tag/type message, stderr empty, raw output
present and exactly the header's declared PRX-data length. A raw ELF or one
bounded complete gzip member may then be interpreted, with gzip CRC/end/trailing
checks and exact declared ELF size. Other formats stay uninterpreted. ELF type2
or0xFFA0 container parsing does not execute, relocate or authenticate the module.
The plan explicitly records the bounded gzip step before these real calls.

Two raw-ELF/gzip positives and ten malformed/size/CRC/truncated/concatenated/
trailing/unknown-format negatives pass. Eleven mocked per-case controls cover a
positive, false success stdout, unsupported reported type, stderr, nonzero exit,
timeout with retained partial output, missing output, wrong output length,
malformed ELF, redirected output and staged-input mutation. Six mocked trial
controls cover full positive, false/wrong-known-ELF control stopping before any
candidate, a separately retained failed candidate, earlier-output mutation and
late helper-pin drift. A failed candidate never becomes an all-candidates-pass
result, while an independently supported peer may still be recorded.

Before freeze, this helper identifies that oversized partial helper output was
retained without an identity/end check. The primary adds streamed size/SHA-256
tracking for every over-bound regular output, with immutable end checks and no
acceptance. It also retains spawn exceptions and snapshots stdout/stderr/stage/
case-result files. Final positive/spawn-partial/over-bound tests pass, including
same-size mutation of an over-bound output. Actual read-only verification checks
all helper/source/runtime/interpreter/library/cache bindings and prerequisite
sets. No helper invocation is performed by the reviewer. These inline mocked
controls do not add to the352-test tooling suite or matching gate.

## Stage B actual output audit

The helper independently audits both actual roots,
`module-static-prep-hxse0az7` and `module-static-prep-8z373w8d`. Both trials first
reproduce the entire 2,247,320-byte known EBOOT ELF (SHA-256
`755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950`)
before any candidate. All twelve input bindings, raw helper outputs, stdout/
stderr/stage records and exact helper commands agree with frozen inputs; complete
raw and prepared bytes and outcomes reproduce across trials. No module is run.

The four archive helpers report the exact successful tag457B06F0/type2 message,
zero exit and empty stderr. Each raw gzip size equals the declared PRX-data
size. Independent standard-library checks verify one complete member, CRC,
end-of-stream and absence of trailing/unconsumed bytes; exact decoded lengths
match the declared ELF sizes. All eight decoded candidate copies are preserved.

| Candidate | Raw helper bytes / SHA-256 | Prepared bytes / SHA-256 |
| --- | --- | --- |
| Archive17 | 20,276 / `8366e2240642bb1d68ce6f84c87f36614c5ba1edd8b231bbf2992b861aaa4d0c` | 35,232 / `9d6c771861b8dec4ed74284809e6853d5e738f794a7c5d3052ac288a23dc71cb` |
| Archive18 | 707 / `3913b6048345ff76e5ec53a0546ee950a0433b2af8a2edfd9917fa4f23ce3713` | 1,138 / `7e49891b16f453c09433249953f9a1330555525e6a51201f63e4b3a6abbd3807` |
| Archive19 | 20,275 / `6d13505bcd9a1c0c9337edb81a2fbbe885a1cfbc35f2153a35ea7e5d5bdc4e06` | 35,232 / `3eb3b7f83442370533647b46365be49463256931196610175119959729b4e466` |
| Archive20 | 706 / `bf01b70cef4fde463dc9f9cb241c92e47c90ba7eaecf84cf98b5b424c178e624` | 1,138 / `129e8e7a5231a81ba919d751c2ff0b1f03f95996a27d766732bf4f5bf61085bc` |

However, the unchanged existing Elf32 reader rejects all four decoded candidates:
`ELF segment file size exceeds memory size`. The helper independently reproduces
that error. Every archive outcome therefore remains
`HELPER_SUCCESS_OUTPUT_UNINTERPRETED`; none receives an elf_container record or
new parsed-module claim. Prepared byte identity is not complete ELF validation.
The frozen parser is not relaxed to turn this into a success.

OPNSSMP returns zero but prints `Decryption failed for tag 457B8AF0` and leaves
an empty raw output (SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
Both outcomes correctly remain `HELPER_FAILED_OR_UNINTERPRETED`, with no prepared
ELF file. The aggregate all-candidates-prepared flag is false. No retry, source
repair or alternative helper invocation is performed in this bucket.

The 839-byte pre-execution preparation freeze has SHA-256
`88b66e21a05a665f1d07f70cf462f2e4456faa5c706c5e29721ac1d70cde779c`.
The two 289,755-byte reports have SHA-256
`60f6d7ec4a68f9e0e7856c6873e4bebbca8162b4bbe391b19061288e1a035517`
and `8ef61c9c85e67ec2869dce7f2724b3aac8a03d034095fc86b4838ab9c4bac40d`.
Trial/build paths differ; complete per-case bytes/streams and outcomes are the
repeat controls. Final nested verification and exact freeze checks pass,
including original source/profile/parking, helper and all pinned host-runtime
bindings. The helper performs only read-only verification, never another helper
invocation.

Declared boundary eligibility, helper decryption, gzip decoding, complete ELF
interpretation, module ownership/authentication and matching credit remain
separate. This bucket identifies a retained parser-model boundary and one
unsupported-helper case; it does not establish new executable modules, SDK
exclusions, original compiler, source matches or a completed game-code inventory.
The initializer remains PARKED with unchanged attempts/shape counters. No linking,
game/runtime execution or native-port implementation occurs. The last352-test
WSL suite is unchanged; inline controls do not replace the full-build gate or its
eighteen required negatives.
