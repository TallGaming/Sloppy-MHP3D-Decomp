> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3E independent validation notes

The synthetic link-stage experiment is independently reviewed. **All six real
link attempts failed and produced no linked ELF.** The completed investigation
does not validate linked metadata propagation or establish a working game
toolchain. No game code was linked or executed; no match credit is claimed.
No commits were made.

## Pre-link review and freeze

Before any actual link output, the validator approved draft profile SHA-256
`1c8fa7ec74b6e19a7fa5dba0d2bc228ebfb6b1e6bc8f3c6d574452dfab349a85`.
It uses one existing unmodified SNC `pspld` binary, one shared script, explicit
`family_smoke` entry and `.text` address `0x08804000`, O0 for every existing
compiler profile, and the same comment/trace/map/warning options for all inputs.
No library arguments, discard clauses, stripping, family-specific changes or
input ELF repairs were approved.

The final profile is 3423 bytes, SHA-256
`dc0017e2a922011fa51c59ab477baab74d805481d6ec56e53ff156b0da31094f`.
Literal restoration of its previous status exactly reproduces the approved
draft hash: no other profile byte changed. Source SHA-256 is
`4fae81ae773148d74eb76914f823cd3f4946ff498e76eabb5c2b21db39d63702`;
layout SHA-256 is
`d4a7a44addfd7f70d88b09fe9d6058e21058d700b1bafcebd10cd373eba1ab55`.
Both remain unchanged. The historical `no_link_outputs_observed` field describes
the freeze point; it does not deny that trials subsequently ran.

The validator independently checked all seven local linker/input/evidence pins
and five declared native Windows DLL pins before linking. Native Windows interop
was explicitly selected; unreliable wibo help cleanup was not treated as a
successful link. The recorded Windows imports describe a limited dependency
scope, not a complete OS installation snapshot. Actual link success requires
exit zero; help's exit-one convention does not relax that rule.

## Automated checks

From `<project-root>`:

```powershell
wsl -d Ubuntu -- python3 -m unittest discover -s tests -v
```

Result: **196 tests passed** (exit 0, no skips): all 174 existing checks and 22
new synthetic-link checks. The new tests use invented ELF/source/tool fixtures
and mocked compiler/linker subprocesses. Their positive ELF controls are not
evidence that any real tool successfully linked this experiment.

Coverage includes:

- Complete symbol extents, nonzero function offsets, raw comment bytes and ELF
  flags as separate observations. Changed code or extra bytes inside a function
  produce a code-change finding; no padding is trimmed to obtain equality.
- Missing, duplicate, empty, unaligned or out-of-bounds functions; wrong ELF
  type/machine/endianness; malformed tables, entries and address overflow.
- One unambiguous executable file-backed load mapping, with section/file offsets
  agreeing. Missing/short/nonexecutable mappings, duplicate segments and partial
  segment/allocated-section overlaps fail, including zero-fill overlap.
- Unsupported code relocations and malformed non-code relocation links, symbol
  indices, places and record bounds. Metadata is retained, not stripped to make
  an input acceptable.
- Three declared fresh synthetic inputs with identical linker options/layout;
  repeatable reports and immutable source/profile/tool/native dependency pins.
- Compile and link warnings, nonzero results, timeouts, missing objects/ELFs/maps,
  invalid outputs and input-object mutation cannot claim preservation. All
  declared outcomes remain visible. Valid ELF bytes left by a failed process
  are still not a successful link.
- Global pin changes prevent an outer report; conflicting evidence and input
  aliases preserve files. The native wrapper uses empty stdin, a bounded timeout,
  explicit command arguments and no shell, and rejects stale output/map paths.

Review prompted complete non-code relocation-record checks and rejection of
partial allocated-section/load overlaps. These protections are present and
tested. The matching gate and its eighteen negative checks remain separate
and unimplemented.

## Independent audit of the real repeat trials

Reports `evidence/bucket-03e/final-link-run-1.json` and `final-link-run-2.json`
are byte-identical: 13377 bytes, SHA-256
`fbe206a40ae6f4efcaf9e91c54faa7281c7648bc84d4931289e76945d4338af7`.
Fresh artifacts are in:

- `build/synthetic-link-4cs9z75u/`
- `build/synthetic-link-sepjo2c6/`

The validator independently read all six input objects, six compile logs, six
link logs and four partial maps. Object hashes, function hashes/bytes/extents,
section indices, metadata comments and flags agree with the reports. All four
non-code relocation records across the six objects have valid places/symbol
indices; there are no code relocations in these invented inputs. The objects
remain byte-identical across repeats and to their recorded pre-link identities.

| Input | Full function | Object flags | Link exit in both trials | Observed artifact |
| --- | ---: | --- | ---: | --- |
| GCC backend/explicit assembler | 44 bytes | `0x10843000` | 255 | Internal exception; partial map; no ELF |
| SNC | 24 bytes | `0x10A23001` | 255 | Internal exception; partial map; no ELF |
| Metrowerks 219 | 28 bytes | `0x10970001` | 1 | Internal zero-alignment error; no map or ELF |

The GCC `.text` section is 48 bytes while its complete symbol is 44. The four
outside-symbol bytes are section padding, not a shortened comparison of the
function. No linked function comparison was possible in any real row.

Both GCC/SNC partial maps mention the function at the intended address. That
does not prove an executable entry, segment/file mapping, preserved instructions
or output flags/comments. The Metrowerks diagnostic does not identify which
section caused the alignment error. The traces show the declared object input;
the command/layout passed no SDK/runtime libraries. Inputs were not patched and
no alternate options were tried to repair the failures.

The primary's real wrong-source-pin and report/input-alias controls both exited
one, preserved inputs and created no new build directory or successful report;
their records are in `evidence/bucket-03e/verification-summary.json`. The unit
tests independently exercise the same failure classes using disposable fixtures.

After the trials, the validator independently rechecked all 191 combined local
input/tool/evidence pin records and sixteen native dependency/tool records from
the synthetic and existing family profiles. All match. The original comparator,
unused Bucket 3C alternatives and prepared reference ELF also retain their
accepted hashes.

## Reviewed identities and limits

| File | SHA-256 |
| --- | --- |
| `scripts/bench_synthetic_link.py` | `a5b0c1872102ee8735888678f8eb5649abad7b3c2481b8057d863a9aa36d1cad` |
| `tests/test_synthetic_link.py` | `4c29e0762044d1a9aeecbdac638f1266f2d95b4f7646f87f54c5ead6c0962809` |
| `config/synthetic-link.json` | `dc0017e2a922011fa51c59ab477baab74d805481d6ec56e53ff156b0da31094f` |

No material blocker remains in the reviewed evidence/failure-handling paths.
The real linker experiment itself remains unsuccessful. It provides no basis
for claiming that a linked banner was reproduced, that flags/comments propagated
in a particular way, that a compiler family is generally incompatible, or that
the historical game linker was identified. The game comparator, frozen source
variants and compiler flags remain unchanged. No full game build, runtime test,
new relocation support or matched function is claimed. Further investigation
needs its separately reviewed bucket.
