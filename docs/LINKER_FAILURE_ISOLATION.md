> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# SNC linker failure isolation

Bucket 3F, 2026-10-30. This two-case experiment keeps the invented function,
SNC O0 compiler profile, unmodified linker and native Windows runner fixed.
It compares default placement with one minimal explicit script. It does not
link game code, recover overlays or establish a historical game toolchain.

## Review before new links

The source reviewer approved `config/linker-isolation.json` before any 3F link
output, draft SHA-256
`afc431a0bb038eeb5491abe8a7cbe653e9931b46059b0025694733c1817f75bb`.
It references the unchanged Bucket 3E configuration, SHA-256
`dc0017e2a922011fa51c59ab477baab74d805481d6ec56e53ff156b0da31094f`.
That configuration pins `compiler_family_smoke.c`, the existing family profiles,
SNC `pspld` 2.7.63.0, support files and declared Windows dependencies.
All 3E inputs and failed-link evidence remain preserved.

Both independent reviewers approved the draft. The primary then changed only
its status before linking, freezing SHA-256
`ddf78aa4d06d042e1a7f56765377e6e73b47c2931f6ed479536af280780e1f54`;
`evidence/bucket-03f/profile-freeze.json` records that sequence. Exactly one new SNC
object is compiled per trial, using the original source and unchanged
`-c -G0 -O0` profile. Both cases receive that identical object, with input bytes
checked before and after linking. Each case has a separate fresh output/map
directory; the complete two-case trial is repeated with another fresh object.

| Case | Layout policy | Entry/address requirement |
| --- | --- | --- |
| `default_layout` | No `-T` script option; let the linker choose its layout. | Entry must equal the sole complete function and have unambiguous executable section/load mapping; record its actual address. |
| `minimal_explicit_layout` | Supply the one reviewed minimal script. | The same mapping/entry checks, additionally requiring `0x08804000`. |

Both use `-comment -e family_smoke -Wall -Werror -t`, map/output arguments and
the same native Windows interop execution. There are no library/search-path,
strip, warning-suppression, binary-patching or licensing changes. Default-layout
requests for unavailable scripts, SDK libraries or startup objects remain
findings; the experiment does not obtain or supply replacements.

The explicit script, `bench/synthetic_link_minimal.ld`, is 306 bytes, SHA-256
`ff22d32c21f218aad04f04f78b8cfc355186c9ac62d9bfd6b420416e867a1f8d`.
It selects `family_smoke`, fixes `.text` at `0x08804000`, and accounts for the
SNC object's actual `.rodata`, `.data` and `.reginfo` sections. `.reginfo` is
metadata, not additional function code. It introduces no clauses for absent
GCC/Metrowerks sections and has no discard clause. Symbol/string tables remain
linker-managed rather than being removed from the input.

This is a deliberately limited layout comparison. The default case may choose
a different text address, and the explicit script differs from 3E's broader
script in several clauses. A difference in results cannot identify one specific
clause, address effect or internal exception's root cause without further
evidence. No case is revised after observing results.

## Results and audit

From `<project-root>`, the two-trial command sequence is:

```powershell
python scripts/bench_linker_isolation.py --report evidence/bucket-03f/isolation-run-1.json
python scripts/bench_linker_isolation.py --report evidence/bucket-03f/isolation-run-2.json
```

The reports are byte-identical, 3904 bytes, SHA-256
`bafda38fab6e86013a2c6e8f7f2ea18c0cc71ae49300b84ddddefbeca22ec81c`.
Artifacts remain under `build/linker-isolation-w8h8e0us` and
`build/linker-isolation-9stye3hw`. All four case executions returned 255 and
reported an internal linker exception; none produced an ELF.

| Case | Trial 1 | Trial 2 | Function placement in partial maps |
| --- | --- | --- | --- |
| Default layout | Link failed; no ELF | Link failed; no ELF | `0x00000000` |
| Minimal explicit layout | Link failed; no ELF | Link failed; no ELF | `0x08804000` |

Both fresh SNC object files have SHA-256
`c0b233c8c2049470ca92516735aa2e51cf02beaef95825fc62108f1b5ddaee1f`.
Each trial supplies that same immutable object to both cases. Independent
read-only review checked both complete object/function hashes, all four logs,
all four maps and the frozen input pins. The object contains one complete
24-byte function, raw flags `0x10A23001` and no `.comment` section.

Each trace names only its own object, twice. The partial maps identify that
object and linker-internal bookkeeping; no SDK, startup or archive-library
object was observed. This is a bounded trace observation, not a complete
file-access audit or a successful library-free link. Partial placement records
do not validate an executable entry point or load mapping. With no output ELF,
linked metadata and function-byte preservation remain unmeasured; zero preserved
cases does not mean that changed function bytes were observed.

The reported failure reproduces without 3E's broader explicit script, so that
script is not a necessary trigger for failure under this setup. This does not
isolate a particular script clause, address effect, input field, host dependency
or internal root cause. Identical printed exception messages do not establish
that all four executions faulted at the same instruction.

## Retained crash artifact

`evidence/bucket-03f/last-linker-crash.dmp` is a 26609-byte `MDMP` file, SHA-256
`667c38f5dc52565380b89ba95581beeb249b3406ceec5f6e16243fb68c8bd9d2`.
The linker writes every crash to the same temporary filename. The primary
retained the file after all four attempts; its association with a particular
case/trial is not independently proven. `crash-artifact.json` records that limit.

A bounded read using Microsoft's
[minidump directory](https://learn.microsoft.com/en-us/windows/win32/api/minidumpapiset/ns-minidumpapiset-minidump_directory),
[exception-stream](https://learn.microsoft.com/en-us/windows/win32/api/minidumpapiset/ns-minidumpapiset-minidump_exception_stream)
and [exception-record](https://learn.microsoft.com/en-us/windows/win32/api/minidumpapiset/ns-minidumpapiset-minidump_exception)
schemas gives the following independently checkable fields. All offsets below
are **file offsets** in this retained dump; integers are little endian.

| Field | File offset | Value |
| --- | --- | --- |
| Directory count / location | `0x08` / `0x0C` | 12 / `0x20` |
| Exception stream directory entry | `0x44` | Type 6, size `0xA8`, data at `0x63C` |
| Exception code | `0x644` | `0xC0000005` |
| Exception instruction address | `0x654` | `0x004104A2` |
| Exception parameter count | `0x65C` | 2 |
| Operation / inaccessible address | `0x664` / `0x66C` | 0 / `0x1C` |
| Module-list directory entry | `0x2C` | Type 4, size `0x9B8`, data at `0x7B4` |

Microsoft defines this exception/parameter combination as a
[read access violation at the second parameter's address](https://learn.microsoft.com/en-us/shows/inside/c0000005).
The first [module record](https://learn.microsoft.com/en-us/windows/win32/api/minidumpapiset/ns-minidumpapiset-minidump_module),
at file offset `0x7B8`, identifies `pspld.exe` with base `0x00400000` and image
size `0x62000`. Its UTF-16 module-name record starts at `0x13F6`. The instruction address
falls inside that module, at image-relative RVA `0x104A2`; this image RVA is
different from a dump-file offset.

This establishes a recorded read access violation at address `0x1C` inside the
linker module, not why the invalid access occurred. The dump lists 23 modules,
including CRT, demangler and debugging DLLs; that reinforces the declared host
dependency list's limited scope, without assigning fault to any dependency or
proving that every listed module participated in the failure. No further
disassembly, binary edits, new tools or extra link cases were performed.

The source reviewer performed no compilation or linking. The frozen cases and
3E evidence remain unchanged. Further isolation needs another reviewed plan;
game matching credit remains zero and the toolchain remains unlocked.
