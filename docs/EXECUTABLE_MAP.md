> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# ULJM05800 v1.02 executable map

Bucket 1 metadata inventory, 2026-10-30. This map covers the accepted decrypted
main executable. It is not a reconstruction, function-count audit or runtime
test. Overlay names and addresses are metadata declarations; no overlay payload
has been extracted in this bucket.

## Reproduce

From `<project-root>`, after preparing the pinned reference:

```powershell
python scripts/map_executable.py --out evidence/bucket-01/executable-map-v1.json
python scripts/map_executable.py --out evidence/bucket-01/executable-map-v1-repeat.json
```

The default report is `evidence/bucket-01/executable-map-v1.json`; a bare
`python scripts/map_executable.py` uses that path. The default input is
`reference/uljm05800-v102/EBOOT.ELF`; `--elf` can select
another prepared copy, but it must match the active reference lock's size and
SHA-256. `--lock` selects a lock file for independent test fixtures. The command
fails before publishing on a rejected/inactive reference, size/hash mismatch or
malformed ELF. A byte-identical existing report is accepted unchanged; a differing
report is preserved and the command requests a fresh output path.

The two reports above were generated independently and compared byte for byte:

- Each report: 819,425 bytes.
- SHA-256: `451fa59db4cb04b14b462d1fecb0f7edef56265d30cfc861c0f6add28db90a96`.
- The JSON contains no current time or machine-specific source/output paths.
- Older exploratory reports without `-v1` remain local ignored evidence; they
  use an earlier schema. The command will not overwrite them with this map.

## Pinned source

| Field | Verified value |
| --- | --- |
| Image | Original PSP release ULJM05800, disc version 1.02 |
| Decrypted executable size | 2,247,320 bytes |
| Decrypted executable SHA-256 | `755e5d84262c3bb30635b32deffab11a66de118f501e4ac105f503308be8b950` |
| ELF | ELF32, little endian, MIPS, ET_EXEC |
| Entry | `0x088214C8` |
| ELF flags, unchanged | `0x10A23001` |
| Section headers | 734 |
| Program headers | 356: one PT_LOAD and 355 PT_NULL |

The machine/flags are retained as observed. A generic tool's ISA label does not
settle the complete PSP instruction set or identify a compiler configuration.

## Main executable regions

Ranges use an exclusive end address. Section indices refer to the original ELF,
not a list reordered by name. Section names are not inferred source-file names.

| Section index / name | Declared address | File offset | Size | Interpretation limit |
| --- | --- | --- | --- | --- |
| 2 `.text` | `0x08804000` | `0x2CB4` | `0x15C9E8` | Main code section; game/library borders unclassified |
| 4 `.sceStub.text` | `0x089609E8` | `0x15F69C` | `0x948` | Import-stub section; individual APIs not resolved here |
| 14 `.rodata.sceModuleInfo` | `0x08961620` | `0x1602D4` | `0x34` | Module metadata |
| 20 `.data` | `0x0896265C` | `0x161310` | `0xB9874` | Initialized data; internal object boundaries unknown |
| 22 `.bss` | `0x08A1BED0` | `0x21AB84` | `0` | Empty named section, not a complete BSS map |
| 733 `.comment` | `0` | `0x224A74` | `0x22` | Nonloaded compiler/platform strings |

The full JSON retains the import/export metadata sections, empty relocation
sections, section alignment, original link/info fields and every program-header
field. The map does not repair unusual or stripped metadata.

Program header 0 is the only PT_LOAD:

| Range or field | Value |
| --- | --- |
| File range | `[0x2CB4, 0x21AB84)`; size `0x217ED0` |
| File-backed virtual range | `[0x08804000, 0x08A1BED0)` |
| Declared virtual memory range | `[0x08804000, 0x09E7DD80)`; size `0x1679D80` |
| Non-file/zero-fill range | `[0x08A1BED0, 0x09E7DD80)`; size `0x1461EB0` |
| Original p_paddr | `0x001602D4`, preserved without interpreting it as runtime physical memory |

The non-file range includes the overlay-address groups below. Its entirety must
not be called BSS: this ELF's `.bss` size is zero, and the real divisions between
persistent state, work memory and overlay storage remain unknown.

## Overlay shared-start groups

The inventory finds **355 allocated PROGBITS sections named `*.ovl`**, excluding
relocation sections. All have size zero. Their names and declared addresses group
into **12 shared starts**, not 12 proven disjoint runtime slots.

For structural program candidates, the mapper requires matching virtual start,
file offset and file size, and excludes PT_LOAD. In this ELF those candidates are
PT_NULL entries with zero file size. Every group has more than one candidate;
all 355 descriptor-to-program pairings are therefore marked ambiguous. Matching
counts and order do not prove which reservation size belongs to a particular name.

The largest candidate reservation below is a group-level observation, not an
assigned size for each overlay or a sum of live memory requirements.

| Declared shared start | Descriptors | Largest candidate reservation | Candidate end | First / last name in original section order |
| --- | --- | --- | --- | --- |
| `0x09BFAE00` | 2 | `0x54700` | `0x09C4F500` | `demo_sub.ovl` / `game_sub.ovl` |
| `0x09C4F500` | 154 | `0x8780` | `0x09C57C80` | `P_m01a00d.ovl` / `P_v00a04d.ovl` |
| `0x09C57C80` | 11 | `0x219180` | `0x09E70E00` | `demo_task.ovl` / `edit_task.ovl` |
| `0x09DB3D80` | 44 | `0x34E80` | `0x09DE8C00` | `em001m0.ovl` / `result.ovl` |
| `0x09DE8C00` | 43 | `0x34E80` | `0x09E1DA80` | `em001m1.ovl` / `em069m1.ovl` |
| `0x09E1DA80` | 18 | `0x14A80` | `0x09E32500` | `em010m2.ovl` / `em069m2.ovl` |
| `0x09E32500` | 18 | `0x14A80` | `0x09E46F80` | `em010m3.ovl` / `em069m3.ovl` |
| `0x09E46F80` | 11 | `0xD800` | `0x09E54780` | `we00player00.ovl` / `we10player00.ovl` |
| `0x09E54780` | 11 | `0xD800` | `0x09E61F80` | `we00player01.ovl` / `we10player01.ovl` |
| `0x09E61F80` | 11 | `0xD800` | `0x09E6F780` | `we00player02.ovl` / `we04player02.ovl` |
| `0x09E6F780` | 12 | `0xD800` | `0x09E7CF80` | `tutorialm1.ovl` / `we03player03.ovl` |
| `0x09E7CF80` | 20 | `0xE00` | `0x09E7DD80` | `P_m01.ovl` / `P_v00.ovl` |

The `0x09C57C80` group's largest candidate reservation reaches `0x09E70E00`,
overlapping later groups. Consequently these starts alone cannot establish
concurrent lifetimes or a safe native-port allocation plan. The archive and
loader must supply the missing evidence in later buckets.

## Observations and open questions

The `.comment` strings are `MW MIPS C Compiler (2.4.1.01)` and `PSP`. They support
investigating Metrowerks PSP tooling, but do not prove the exact compiler build,
flags or whether the original source was C or C++.

Still unresolved:

- Archive extents, compression, actual overlay payload sizes and their hashes.
- Descriptor-to-reservation pairing and runtime loading/state lifetimes.
- Real BSS/work-memory boundaries and internal initialized-data structure.
- Function boundaries/counts and game versus SDK/third-party classifications.
- Import API names and the complete required platform-service inventory.

The Bucket 1 map report credits **zero recovered overlay payloads and zero
matched game functions**. Subsequent [Bucket 2 evidence](BUCKET_02_CHECKPOINT.md)
recovers `movie_task.ovl` and checks its individual reservation association;
the structural mapper alone still cannot resolve the other pairings. No game
functions are matched. The full matching gate and its 18 negative checks are
later work.
