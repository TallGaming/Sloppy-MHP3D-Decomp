> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Supplemental containers from the PSP reference

Two fresh recoveries preserve the same eight exact payloads,10,082,440 bytes
per set. Both manifests/reports are8,656 bytes, SHA-256
`b88187266d7cffa99f5f82ea6902dffde4c3dded119e7f3ef62dd256fafb995a`.
All sixteen payload copies agree with their declared identities and source
extents. The original fourteen-file ISO directory is reproduced unchanged.

| Source | Exact bytes | Observed status |
| --- | --- | --- |
| Main EBOOT | 2,247,664 | Byte-exact existing encrypted reference control |
| BOOT | 2,247,320 | Entire file zero-filled; no executable content inferred |
| OPNSSMP | 3,264 | Declared PSP header; module name is one space, tag457B8AF0 |
| Packaged updater EBOOT | 5,540,576 | Declared PSP header, name updater, tag02000000 |
| Archive17 | 20,688 | Raw SCE candidate, uninterpreted |
| Archive18 | 1,120 | Raw SCE candidate, uninterpreted |
| Archive19 | 20,688 | Raw SCE candidate, uninterpreted |
| Archive20 | 1,120 | Raw SCE candidate, uninterpreted |

The four archive payloads exclude5,536 bytes of surrounding sector padding.
They are copied raw, without the archive deobfuscation transform. Their exact
lengths, original blocks and64-byte prefix hashes agree with the reproduced
validated index/inventory. Both recoveries verify every catalogue checksum and
the original source/toolchain/assembly locks before and after publication.

PSP fields are declarations from complete offset-zero headers, using the pinned
public helper's0x150-byte structure. Module names, tags, ELF sizes, entry values
and compression fields are not authenticated metadata, decoded code extents,
SDK ownership proofs or successful decryption. All ownership stays unclassified.
The four SCE wrappers have no invented inner offset. Public loader code provides
a future declared-length lead, not a universal0x40 wrapper size.

Private outputs are `reference/uljm05800-v102/supplemental-sets/run-1` and
`run-2`; reports/freezes/tests are under `evidence/bucket-03ac/`.
Reproduce into a **fresh** set and evidence name:

```powershell
python scripts/inventory_supplemental_modules.py "D:\path\to\clean.iso" reference/uljm05800-v102/supplemental-sets/fresh-name --out evidence/fresh-supplemental.json
```

The tool rejects conflicting output, redirected staging directories, incomplete
sets, extent/control/prefix drift and changed inputs. Bundle publication and the
separate evidence report are successive operations, not one atomic transaction;
a late report conflict preserves the verified bundle and existing evidence.

All352 tooling tests pass under WSL with zero skips, including twelve new tests
covering bounds, exact lengths, full controls, BOOT tails, input drift and staged
publication integrity. These are not the outstanding full-game18 negative tests.
No original code was executed, decrypted, decompressed, rewritten or matched.
This improves container coverage; complete game-code inventory remains unproven.
