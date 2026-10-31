# Public payload content audit

Reviewed 2026-10-31. This audit covers the authored-text public export, not the
excluded private repository, third-party distributions or a game build. The
primary prepares the export; this reviewer independently scans its contents and
checks the public reproduction tool. No external publication was performed.

## Content and privacy

The complete payload present during the scan is UTF-8 text, without embedded
NULs, PE/ELF/archive signatures or file/directory redirects. No credential/private
key patterns, long contiguous byte-hex dumps or large octet tables were found.
Excluded private directories and vendor binaries/source caches are absent.
Generated Python caches and Git's internal metadata are not publication payload.

Both complete original diagnostic intervals (68-byte initializer and 140-byte
key advance) were checked read-only against the export as raw bytes, hexadecimal
and Base64 encodings. Neither occurs. The scan emits no original target bytes.
This does not claim that every short instruction fragment is absent: authored
research includes addresses, hashes, isolated instruction observations and
reconstructed C/C++ hypotheses, clearly distinct from original binary dumps.

The initially reported remaining machine-root paths were replaced with
`<project-root>`. A subsequent whole-payload scan finds no real personal username,
home or game-folder paths. Remaining examples use explicit `/home/<user>` or
generic `path/to` placeholders; Windows-path cases in tests are invented fixtures.
The local-service state, cookies, databases, credentials and two machine-specific
operator scripts are not included. Historical service documentation is not a
claim that the public snapshot deploys that service.

## Export provenance and checkout bytes

All 287 `SOURCE_EXPORT.json` public-copy identities verify. All 21 bench files
are byte-identical to their private authored sources. Historical-source hashes
are preserved separately from adapted public-copy hashes; sanitization does not
manufacture a new historical test result. The private AGENTS instruction journal
changed after the export snapshot, so its recorded original hash is historical,
not a claim about the current private journal. Other compared original-source
identities agree at readback.

`.gitattributes` disables text newline conversion with `-text`, leaving ordinary
text diffs enabled. Filtered and unfiltered Git object hashes agreed for every
payload file checked. This protects the exact source bytes used by historical
SHA-256 records across Windows/Linux checkout. The added `cr-at-eol` whitespace
attribute recognizes preserved CRLF; it does not rewrite bytes. The primary
retains four pre-existing extra-blank-at-EOF findings rather than silently editing
historical files. These are formatting observations, not failing tooling tests.

The corrected ignore rules were checked with `core.ignorecase=false` and
NUL-delimited paths. All fourteen probes are ignored, including upper/mixed-case
game/SDK extensions, private roots, saves, environment files, credentials,
licenses, cookie JSON/text and shared libraries. Authored Python, C++ and test
paths remain eligible. The initial case-sensitivity/cookie gaps are resolved.

## Public reproduction tool

`tools/repro/compare_function.py` is offline and launches no compiler, decoder,
game or emulator. It requires one complete, unique, positive, aligned, strong
global function in allocated executable PROGBITS, validates symbol/relocation
metadata and rejects all nonzero code relocations. It never selects by matching
bytes, trims padding from a declared function or masks/applies relocations.

Without a reference it reports inspection with `comparison: null`. Comparison
requires the complete pinned decrypted reference identity and the complete
reviewed interval hash. Output contains sizes/hashes/first difference and an
isolated exactness boolean, not target bytes. Source participation is unproved
and game-match credit remains false even for an isolated exact result.

The tool and its ten invented tests pass on Windows and WSL with no private
evidence, game image, SDK, compiler or network input. The tests cover malformed
metadata, multiple/zero/weak/hidden/unaligned functions, REL/RELA code relocations,
unapplied non-code relocations, full-length mismatches, pinned-reference rejection
and CLI failure without a success report. The primary's separate clean-export
suite result is 362 tests: Windows 360 passed/two native-staging tests skipped;
WSL 362 passed/zero skipped. These are tooling tests, not the absent eighteen
full-game negative gate checks. Fresh Git-archive verification is recorded
centrally after this audit.

## CI and publication limits

The workflow has read-only contents permission, disables persisted checkout
credentials and runs the public tooling tests on Linux/Windows. Both actions
are pinned by full commit ID. The official package metadata at the selected
commits identifies [checkout 7.0.1](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/package.json)
and [setup-python 7.1.0](https://github.com/actions/setup-python/blob/6d4fd22b20465ccc0f7354476588e8df7c9ca0e0/package.json).
Only public source metadata was read to verify those identities; no GitHub
workflow or remote publication was launched by this audit.

No project-wide license has been selected, as `LICENSE_STATUS.md` states.
External references do not confer redistribution rights over third-party tools
or game materials. Historical configuration graphs remain explicitly archival;
omitted private evidence and toolchains are not advertised as portable native
reproduction dependencies already present in a clone.

The content/ignore/byte-preservation findings identified in this review are
resolved. The export is ready for the primary's final staged-tree/archive review.
This is not a game release, source-match credit, historical toolchain lock,
ownership determination or completed full-build gate.
