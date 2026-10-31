> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Prefix-only overlay inventory review — Bucket 3R

This bucket inventories archive/header metadata, not additional recovered code.
It permits at most 64 decoded prefix bytes for each of the 5,955 pinned PSP
archive entries, plus the already established directory decode. The one fully
recovered `movie_task.ovl` remains the only recovered payload. No compiler,
initializer source, game execution or port work belongs to this inventory.

## Preconditions established before the real scan

The accepted PSP v1.02 executable/directory/archive pins and the existing
`extract_overlay.py` decoder remain unchanged. Per-entry decode starts at word
zero with the archive-relative block as seed, so a complete-word prefix can be
decoded without materializing the rest of its payload. Reads must stay inside
both the entry's stored length and padded archive extent; small/zero entries
need an explicit bounded policy rather than reading the next entry.

The existing full-payload `parse_overlay` cannot validate a 64-byte prefix by
itself because it checks header+code+data against its entire supplied buffer.
The inventory needs a header-only model that compares declared stored length
with the index length, without fabricating or decoding missing payload bytes.
Raw and decoded signatures are separate observations; `MWo3` alone does not
prove a valid complete header, while `~SCE` or `PSMF` identifies a signature
without assigning game/SDK ownership.

Header model checks must preserve ID, load address, code/data/BSS sizes, name
and the raw words at `0x18/0x1C`. The latter are not assumed entry points,
constructors or initializer bounds. A stored range is distinct from a memory
reservation including BSS. Header/index consistency is not proof that the
unread code/data bytes are valid or that loader behavior has been reproduced.

ELF correlation must retain original section/program indices. Name/address
agreement can associate a header with a zero-sized named descriptor without
treating that descriptor as embedded code. PT_NULL candidates use observed
address and full memory reservation; all duplicate candidates must remain
visible. Numeric header-ID/program-index agreement is corroborating metadata,
not an assumed indexing rule that may silently resolve ambiguity.

Shared start addresses do not define disjoint slot capacities, simultaneous
loads or lifetimes. Existing reservation overlaps and duplicate-sized entries
must remain explicit. The real-image source/model review and independent final
map audit are recorded below as their artifacts become available. No new archive
scan was performed by this reviewer when these preconditions were written.

## Exact source/model review before the real scan

The independently reviewed `scripts/inventory_overlays.py` is 14,673 bytes,
SHA-256 `84f18d2bc0e44b0f0bfd2a493603f946b65ad36bc44eef3c40027607c7613942`.
The draft `config/overlay-inventory.json` is 772 bytes, SHA-256
`b04bb23944d1f9149a622516383f8a97ce6302c8e3215410eff0221aeb76b8a3`.
Initial source/model approval preceded the first invocation, subject to the
other independent review and the declared status-only freeze. That invocation
later exposed the API mismatch recorded below before any entry-prefix decode;
the corrected source received a separate final approval before a new scan.

The implementation's bounded model agrees with the preconditions:

- For each validated index extent it reads exactly `min(64, stored_length)`
  bytes, with no read for zero length. Only the largest whole-word prefix is
  passed to the unchanged decoder; an unaligned short tail is not completed
  by reading padding or the next entry. Prefix-byte totals exclude whole-file
  integrity hashing, which necessarily reads more data without decoding it.
- Both raw and deobfuscated `MWo3` claims are inspected. Incomplete or invalid
  claims remain in the report and prevent the complete-inventory status, rather
  than silently disappearing. Header parsing checks code/data total against
  the directory's stored length, alignment, bounded memory range and terminated
  ASCII name. It does not invent payload bytes to reuse the full-payload parser.
- Header words `raw_0x18` and `raw_0x1c` are retained without semantic labels.
  The raw 64-byte valid header is retained only in ignored local evidence.
  Nonoverlay signature counts remain separate raw/decoded observations.
- Descriptor candidates require the original allocated, zero-sized named
  PROGBITS record's name/address. PT_NULL candidates require zero file size,
  matching address and memory size `stored_length + bss_size`. Every compatible
  program index is retained. Header-ID equality is a separate boolean, not a
  selector that hides otherwise identical candidates.
- Missing/multiply-covered descriptors, malformed claims and unresolved header
  associations remain explicit. Known-descriptor header coverage can complete
  while reservation-value ambiguity remains; it does not certify a unique
  descriptor/program pairing. Extending beyond the next distinct named start
  is geometry only, not a slot-capacity or lifetime inference.

The wrapper requires the active selected reference and frozen profile; checks
the full ISO/archive/ELF/directory/table pins; and reparses the established
directory with pinned counts. It repeats full ISO identity after scanning,
along with lock/profile/ELF checks, so restored timestamps alone cannot conceal
changed input. It rejects report/input aliases, existing reports and link paths.
The output explicitly reports zero full payload recoveries and no established
complete game-code inventory. Reference bytes, code/library ownership, source
coverage, binary reconstruction and runtime validation remain separate.

The final freeze identity and independent output-map audit follow below.
No archive scan or extraction was invoked by this reviewer during this source
review.

## Preserved pre-prefix failure and corrected-source review

The original frozen-source invocation passed the full catalogue identity check,
then stopped with `Fresh ISO inventory identity mismatch: sha1` before the
entry-prefix loop. `first-invocation-failure.json` under `evidence/bucket-03r`
records zero entry prefixes scanned and no published report. The original
14,673-byte source snapshot remains retained as
`inventory-overlays-preflight-v1.py`; the old source hash above is its identity,
not the corrected scanner's identity. The reviewer missed this API mismatch
during the initial source readback.

Independent diff against that preserved snapshot confirms the correction is
only the `inspect_iso` expected-field selection and its explanatory comment.
`inspect_iso` reports size/SHA-256; `check_identity` also requires SHA-1/MD5/CRC32
whenever the supplied lock contains them. The corrected call checks the fields
actually returned by that API, matching the existing one-overlay extractor.
Both full `file_identity` checks still receive the complete reference lock
before and after scanning, so none of the catalogue identity checks is waived.
No header/association/bounds/decoder rule was changed after viewing prefix data.

The corrected source is 14,869 bytes, SHA-256
`628643e527cdd88e5c266047e744534ce446713e97fdd37d041d6b48db13d24e`.
The unchanged frozen profile is 772 bytes, SHA-256
`bddd4163726e3b303a05fb2b0fa725e3f3d2ba016657288c0c11f6c2e6cd796f`.
Explicit corrected-source approval was sent before a new prefix scan, subject
to the other helper's regression review and the corrected-source pre-scan
record. No image scan was performed by this reviewer. The retained
`corrected-source-freeze.json` records both final approvals received at
`2026-10-31T06:02:33.281201Z`, before any entry-prefix decode, and declares two
successful repeat trials. The corrected scanner/profile hashes still agree
after those trials.

## Independent retained-map audit

Both `overlay-inventory-run-1.json` and `overlay-inventory-run-2.json` under
`evidence/bucket-03r` are byte-identical: 3,380,121 bytes, SHA-256
`a7a3b1e7b88aefd342a4fdc4924200570496cd62abb241bd093165f5d383991f`.
The reviewer independently checked all 5,955 entry rows and all 355 header records
against the pinned ELF without reading additional archive prefixes. This audit
recomputes recorded prefix-length bounds/totals and magic counts, unpacks every
raw 64-byte header, rehashes it, checks its declared length/name/fields, and
reconstructs every descriptor and PT_NULL candidate list from original ELF
metadata. Independent byte-decoder/reference-read validation is separately
recorded by the second helper in `BUCKET_03R_VALIDATION_NOTES.md`.

Observed results:

- There are 5,952 nonempty prefixes of exactly 64 bytes and three empty entries
  (indices 3980–3982): 380,928 raw/decoded prefix bytes in each successful scan.
  No actual nonempty short-tail case occurs here; its bounded policy remains
  covered by synthetic controls rather than an invented real-data observation.
- There are zero raw `MWo3` claims and 355 valid deobfuscated headers, with no
  malformed claim. Names and header IDs are each unique; observed IDs span
  1–355. Every named zero-sized descriptor is covered exactly once by header
  name/address, with no missing, duplicate or unresolved descriptor/header.
- All 355 header IDs equal one observed reservation candidate index. This
  corroborates an association in this reference without making the independent
  address/size relation unique or proving a universal loader rule.
- The earlier movie pilot still maps archive entry 101 / header ID 158 to
  descriptor 337 and reservation 158. There is no new payload extraction.

## Reservation ambiguity and overlapping ranges

Every value-compatible reservation candidate remains in the reports. There
are **169 headers with multiple candidates**; header coverage does not erase
that ambiguity:

| Address/size-compatible PT_NULL candidates | Header count |
| ---: | ---: |
| 1 | 186 |
| 2 | 16 |
| 3 | 6 |
| 4 | 12 |
| 5 | 5 |
| 6 | 6 |
| 8 | 8 |
| 26 | 26 |
| 90 | 90 |

All twelve original shared starts and their counts reproduce independently.
Two declared memory ranges extend beyond the next distinct named start:

| Header | Start | Stored + BSS length | Exclusive memory end | Next named start |
| --- | --- | ---: | --- | --- |
| `download_task.ovl` | `0x09C57C80` | 1,821,440 | `0x09E14780` | `0x09DB3D80` |
| `lobby_task.ovl` | `0x09C57C80` | 2,199,936 | `0x09E70E00` | `0x09DB3D80` |

These are independently checked address-range facts, not proof of disjoint
slots, available capacity, simultaneous residency or mutual-exclusion rules.
The BSS portions are declared memory without stored bytes. Summing those ranges
does not establish a runtime memory requirement.

## Other metadata and interpretation limits

Header-declared totals are 15,092,864 stored bytes, including 22,720 header
bytes, 8,284,380 code bytes and 6,785,764 data bytes. Declared BSS totals
6,558,848 bytes across these potentially overlapping/lifetime-dependent images.
The largest stored image is `lobby_task.ovl`, 1,525,632 bytes. These are sums
of validated header/index declarations; the unread code/data is not recovered
or byte-validated by this scan, and these values are not an all-game-code
coverage denominator.

Raw `~SCE` signatures occur at entries 17–20, and raw `PSMF` signatures at
81–92. These are signature observations requiring their own future inventory
if needed, not SDK ownership or full executable/media validation. HD indices
from public projects do not replace these original PSP indices.

The raw-address-word observations also reproduce:

| `raw_0x1c - raw_0x18` in bytes | Header count |
| ---: | ---: |
| 0 | 52 |
| 4 | 298 |
| 8 | 2 |
| 20 | 1 |
| 32 | 1 |
| 100 | 1 |

`raw_0x18` equals the declared stored-image end in 52 headers and that end minus
128 in 303. No bytes at those addresses were inspected as tables by this bucket.
The patterns alone do not establish constructors, entry points, initializer
bounds, callable targets or function counts; both fields remain uninterpreted.

The inventory establishes complete **header coverage of the existing 355 named
descriptors**, with structural reservation ambiguities retained. It establishes
neither a complete all-module code inventory nor library ownership, function
boundaries, loader execution or source reconstruction. This bucket recovers
zero complete payloads; the earlier single movie payload remains the project
total. Game matching and linked-source credit remain zero, the archive
initializer stays visibly parked, and no compiler/game execution or native-port
work was performed by this reviewer.
