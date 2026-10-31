> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# PSP v1.02 DATA.BIN: one-overlay recovery

Bucket 2, 2026-10-30. The selected payload is `movie_task.ovl`; broader recovery
is outside this bucket. These are static observations from the accepted original
PSP ULJM05800 v1.02 reference, not compiler selection, matching credit or a runtime
test. Game bytes and disassembly remain in ignored local directories.

## Reproduce the selected payload

From `<project-root>`, with the prepared reference ELF:

```powershell
python scripts/extract_overlay.py --iso "<game-image-directory>\Monster Hunter Portable 3rd (Japan) (v1.02)\Monster Hunter Portable 3rd (Japan) (v1.02).iso"
```

The command selects only the payload pinned in `config/overlay-pilot.json` and
writes `reference/uljm05800-v102/overlays/movie_task.ovl.mwo`. It verifies the
active reference, whole ISO/archive, ELF, substitution table, directory and
selected encoded/decoded identities before publication. Existing differing
outputs/reports are rejected; use a fresh output/report path for repeatability.
The primary agent owns test and repeat-run results in the bucket checkpoint.

## Evidence and source limits

The public [MHTools decoder](https://github.com/codestation/mhtools/blob/d71d174a27074a518c1df55e576744a8028a6c84/src/crypt/DecryptUtils.java)
and [archive constants](https://github.com/codestation/mhtools/blob/d71d174a27074a518c1df55e576744a8028a6c84/src/keys/DataKeys.java)
provided the substitution/XOR algorithm. The local checkout is pinned to that
commit. [Yakumo's format notes](https://github.com/TeamGDB/Yakumo/blob/b61852aef10870400320b96d92a14136ac17b051/docs/DATA_BIN.md)
and [parser](https://github.com/TeamGDB/Yakumo/blob/b61852aef10870400320b96d92a14136ac17b051/profiles/mhp3rd/tools/databin.py)
provided index/header leads. Yakumo targets an HD executable through static
recompilation; its entry counts, addresses, loader claims and compiler choices
are not evidence for our PSP binary. The PSP values below were checked directly.

`/PSP_GAME/USRDIR/DATA.BIN` begins at ISO LBA 55968, occupies 1,092,495,360
bytes (533445 blocks of 2048), and has SHA-256
`cb1229171c2a7bcc11716a2cd5a2bb3c40a242f0d614bb88aa50cbedfb60426e`.
The local ELF is pinned separately by `config/reference.json`. Its static
disassembly is `evidence/eboot-v102.disasm.txt`; addresses below are virtual
addresses in that ELF.

## Decode transformation

For an entry starting at archive-relative block `b`, initialize high state to
`(b >> 16) or 0x2345`, and low state to `(b & 0xffff) or 0x7f8d`. Substitute
each encoded byte through the **decode** table directly. Before each little-endian
32-bit word, update `high = high * 0x2345 % 0xffd9` and
`low = low * 0x7f8d % 0xfff1`; XOR the substituted word with
`(high << 16) | low`. Reset state for each entry. The directory starts at block
zero. Bounds and word alignment must be checked before decoding.

The 256-byte table is read from ELF file offset `0x1A86FC`, virtual address
`0x089A9A48`, after ELF identity verification; it is not copied into source.
Its SHA-256 is
`442d20ebfcc0fbba34b20a28e20fbd72c8a8f330a3342b0122f9e405f4822cc2`.
PSP static evidence independently confirms this algorithm:

| ELF address | Observation |
| --- | --- |
| `0x0886233C` | Splits the seed and substitutes the two default nonzero seeds. |
| `0x08862700` | Updates the two states with the multipliers and modular reductions. |
| `0x08862808`–`0x08862888` | Forms the table address, substitutes four bytes, calls the state update and XORs/stores one word. |

No decompression is needed for this selected overlay. This does not classify
every archive entry or establish whether other payloads use compression.

## Directory layout and loader correspondence

The first decoded word is 17: the directory occupies 17 blocks, 34816 bytes.
The table contains 5956 little-endian block-start words: 5955 entries and the
final archive-end sentinel 533445. Entry `n` spans
`[blocks[n], blocks[n + 1]) * 2048`. Entry zero starts at block 17, after the
directory prefix; the directory is not a payload entry in this numbering.
Starts must be monotonic and remain inside the archive. MHTools' extraction
loop counts the directory as file zero, so its numeric filenames are one
higher than the zero-based payload indices used here.

After the sentinel, exactly 1289 `(entry_index, exact_byte_length)` pairs occupy
10312 bytes. A pair overrides the padded block extent; its length must fit that
extent. Entries without a pair retain their block extent. The pairs here are
strictly ordered and end at entry 5652. Their end is directory offset `0x8558`;
the remaining 680 bytes are uninterpreted and are not a zero-terminated pair
list. The extractor pins counts rather than scanning until a plausible failure.

| ELF address | Independent PSP evidence |
| --- | --- |
| `0x08862F98` | Archive-entry loop bound is 5955. |
| `0x088631C4`, `0x08863204` | Reads then decodes `0x5D10` (23824) block-table bytes. |
| `0x08863240`, `0x08863270` | Reads then decodes `0x2848` (10312) pair bytes, continuing the directory decode state. |
| `0x08863C78`–`0x08863CA8` | Exact-size lookup scans 1289 eight-byte pairs and returns the second word on an index match. |
| `0x08863CB8`–`0x08863CCC` | Missing-pair fallback subtracts adjacent block starts and shifts left eleven. |

Thus the observed loader consumes the first 34136 directory bytes through these
two reads; the remaining tail's content and purpose are unresolved. The SHA-256
of all 34816 directory bytes after decoding is
`64c10d7e2fbba5a1a6ad860790396dac5d0e4fedd4fedfed83a609745cb92a1f`.

## Selected overlay and ELF link

The primary selected `movie_task.ovl` because its name identifies an existing ELF
descriptor and its complete payload is small. Candidate discovery inspected
only 64-byte prefixes; only this payload is recovered in full.

| Property | PSP observation |
| --- | --- |
| Archive entry (zero-based) | 101 |
| Archive block / byte offset | 268538 / `0x20C7D000` |
| ISO LBA / byte offset | 324506 / `0x279CD000` |
| Padded extent / exact stored length | 2048 / 1280 bytes |
| Decoded magic / name | `MWo3` / `movie_task.ovl` |
| Header ID / load address | 158 / `0x09C57C80` |
| Code / data / BSS length | `0x488` / `0x38` / `0x80` |
| Raw fields at `0x18`, `0x1C` | Both `0x09C58180` |
| ELF descriptor index | 337, zero-sized allocated PROGBITS, same name and load address |
| ELF program-header index | 158, PT_NULL, same load address, reservation `0x580` |

The 64-byte header has little-endian ID at `0x04`, load address at `0x08`, code
length at `0x0C`, data length at `0x10`, BSS length at `0x14`, two raw address
fields at `0x18`/`0x1C`, and a 32-byte name field at `0x20`. The exact payload
length is `64 + 0x488 + 0x38 = 0x500`; BSS contributes no stored bytes. With BSS
the reservation is `0x580`, uniquely matching program header 158 at this base.
The header ID also equals that program-header index. These independent value
agreements support this selected association without assuming descriptor/program
order. They do not establish the association for every overlay.

The two raw address fields equal the stored-byte end for this payload. Their
precise semantics are unresolved; the current parser's `entry_address` label
must not be treated as a proven callable entry point. Code follows the header at
`0x09C57CC0`; data begins at `0x09C58148`. Static disassembly contains coherent
function-shaped code at `0x09C57D00`, `0x09C57E18` and `0x09C57F30`, with calls
back into main-executable addresses. This supports code plausibility, not names,
behavior, successful execution or historical source reconstruction.

The selected encoded 1280 bytes have SHA-256
`9a825ce43736d0869e67f9f56ea9ba3af4679fdd01748e806e11ce2bb2e982bb`;
the decoded 1280 bytes have SHA-256
`6a918f7af824103cfe5df0c4fb8d793c430a273b166a8eaf5ce1e5cd66951abb`.
The 768 remaining bytes in its archive extent are padding, excluded from the
overlay output. The ELF's 355 zero-sized descriptors still do not represent
355 recovered binaries; Bucket 2 recovers one. SDK/game boundaries, source
language, relocation/loader behavior for all overlays, and complete code-module
coverage remain open.
