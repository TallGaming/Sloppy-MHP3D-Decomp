> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Guarded host KL4E preparation review — Bucket 3AI

Both separately reviewed actual calls produce the same bounded 3,550-byte PSP
container. OPNSSMP preparation now succeeds; authentication, ownership and
execution remain unestablished. The source/build/control reviews below preserve
the order in which those claims became supported.

This reviews a native host data-preparation tool around an unchanged pinned
public decoder. It is not a rewrite or execution of game/SDK code, and no MIPS
interpreter or supplied module routine belongs to this preparation path.

## Decoder identity, ABI and format

The [pinned native source](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/kl4e.c)
is the same source already present in the original helper. Local CRLF bytes are
14,119 bytes, SHA256
`117befc155807a632120fbf743188a5b5ee9f924246042a67e2ea82f104af641`;
the public LF text is 13,773 bytes, SHA256
`10d433cbc03c43cb0bc5d7b7c40ba39d0c3863825aa050c74e87c9ee990b120a`.
They agree after newline normalization. Cache and immutable URL/commit metadata
are in `evidence/bucket-03ai/helper-map-native-source.json`.

The source describes a reverse-engineered firmware routine with simplifications;
that claim does not prove universal equivalence or safe handling of arbitrary
malformed inputs. It declares
`int decompress_kle(u8 *out, int capacity, u8 *stream, void **end, int isKl4e)`.
For this experiment, skip exactly the four observed KL4E magic bytes, preserve
all remaining bytes, and fix isKl4e=1. The decoder immediately accesses five
stream bytes and has no input-length parameter. Actual-input expected output
length 3550 comes from the existing declared PSP header and must be fixed before
any decode, not chosen after looking at an output.

[output_raw](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/kl4e.c#L126-L138)
uses the **absolute output address modulo 8**, not only an offset, when choosing
probabilities. The wrapper must therefore guarantee an 8-byte-aligned output
base. Page-end placement with an 8-byte-rounded declared capacity preserves
that property and permits a right guard immediately after capacity.

[Direct copy](https://github.com/John-K/pspdecrypt/blob/c156627db7634d395c380c0a9589130f603307fc/kl4e.c#L153-L170)
rejects count>=capacity and reports `end=inBuf-1` after copying, namely the last
copied source byte. The compressed terminator reports the current inBuf pointer.
The wrapper must bounds-check/report the raw pointer conservatively, rather
than normalize both cases into an unsupported “all input consumed” assertion.
Extra trailing input or a consumed-byte observation alone does not authenticate
or independently validate the stream.

The backreference code checks its source distance but its final copy loop lacks
a complete output-capacity check. Input-end protection, output guard pages and
sentinel checks across every unused output byte are mandatory. The decoder's
own error return is not a substitute. A memory signal, timeout, negative result,
wrong exact length, changed sentinels or invalid end pointer must retain failure
without publishing an output. Guard pages detect relevant memory violations;
they do not make this unchanged C implementation a generally safe decoder or
prove every undefined-behavior concern absent.

## Pre-execution review status

Exact wrapper source review passes for `tools/host/kl4e_guarded.c`, 11,209 bytes,
SHA256 `54924c9fb5dc705bc3b8147d6132c36fc18e67324261e73deac467932a1ed6ae`.
It requires KL4E magic and at least five stream bytes, maps the actual input end
adjacent to PROT_NONE, protects its usable mapping read-only, and passes exactly
input+4 without padding. Its declared output capacity is
round_up(expected+1,8), placed against a guard with at least 64 prefix sentinel
bytes. It checks all prefix/slack final bytes, exact return, conservative integer
endpoint bounds, fd/named-input identity and exclusive/no-follow output creation.
The decoder ABI and isKl4e=1 remain fixed. Parent-chain guards, timeout and full
file identities are controller obligations. A partial I/O output is never a
successful extraction. These guards do not replace independent codec evidence.

Pre-build approval covers `evidence/bucket-03ai/build_kl4e_host.py`, 10,168 bytes,
SHA256 `07c7fcc44d3e0f1bc31dce5e6d0f7d76763a7ae59b20c577072122b463f3d8ce`,
and `config/kl4e-host-build.json`, 1,516 bytes,
SHA256 `ffa9d26fe6ba0f3769eafbbe1d373bd649ec74c242d7a2948ff5f77d58c7a17b`.
The fixed host recipe uses GCC O2/c99/Wall/Wextra and no-undefined linking with
only PATH/LC_ALL supplied. The compiler header-dependency query uses the same
frontend flags, pins those inputs before compilation and rechecks them after
link/static inspection. Native compiler tools/runtime and resolved readelf are
pinned. Logs, source bytes, header inventory and binary snapshots are rechecked
before exclusive report publication; the binary identity is tied to its actual
retained snapshot. Spawn and timeout failures remain failures with evidence.
These host flags do not change a PSP game compiler setting.

Approval is only for two fresh host builds. Invented control/controller and
actual-payload execution each still require separate review/freeze. The actual
2,926-byte retained payload stage needs a separate freeze after these checks.
No decoder/helper/module was invoked by this reviewer. No input padding,
algorithm revision, new game-source attempt, flag tuning, ownership exclusion,
authentication or match credit is authorized by this format review.


## Future host-language comparison lead, not executed here

Pinned [JPCSP KL4E.java](https://github.com/jpcsp/jpcsp/blob/48f107aea7b021d51ebaf2fda4007ceb6f47bb03/src/jpcsp/format/KL4E.java)
contains a static byte-array decoder with standard Integer/Math imports and six
Utilities helpers, without Processor/Interpreter/TPointer dependencies. It is
15,685 bytes, SHA256
`85715945bf4e5fc57360930763a8bb37956d8150da384f472740e330d3fb23db`;
cache provenance is `helper-map-jpcsp-kl4e-source.json` in this bucket's evidence.
Its header explicitly calls it a direct Java port of this same native C source.
A later comparison could independently exercise host-language bounds and signed
arithmetic behavior, but must not be described as an independently derived
codec implementation. No Java implementation or decoder run occurred here.


## Actual host build audit, before decoder execution

Both frozen builds succeed with identical 21,384-byte native binaries, SHA256
`20d9ee7162765e3af8797f7bd8d9dfbffed6cbb14e37a4380e9a8d17fc2d25c9`.
Retained roots are `build/kl4e-host-build-2fxl2twz` and
`build/kl4e-host-build-uxaz36az`. Independent checks verified all 20 artifact
records and all 276 native header records; the two 138-record header inventories
are identical. ELF64/x86-64 dynamic parsing confirms only libc.so.6, with no
RPATH/RUNPATH. Static readelf records the default host loader.

Both builds retain the same original decoder signedness warning at line 219;
the wrapper has no warning. No source or option was changed to remove it.
Build success itself does not execute or validate a compressed stream. The
next invented-control review is separate from actual-payload preparation.


## Invented controls: independent pre-execution review

Controls-only approval covered `run_kl4e_host.py`, 17,119 bytes, SHA256
`0eaf39ea3c9b3ee91d2a4a93de7000f86379387860b80f611d03341c98658ca6`,
and `config/kl4e-host-experiment.json`, 2,484 bytes, SHA256
`73fca5a2b03c7bcc6206f85ea24d897f25770f54601d9ec1069fab15f9980ee7`.
The controller is frozen separately from the build. Actual-input invocation
requires another freeze plus both control-output audits; it is not enabled by
controls-only approval.

The fixed 17 cases contain 15 native invocations and two explicit controller
redirect rejections. Positive direct-copy lengths 1/3/7/8/4095/4096 exercise small
and page-adjacent output layouts. A trailing-data case records the direct-copy
last-byte endpoint without claiming full-stream consumption. Negative cases
cover magic/header, expected-size bounds, truncation hitting the input guard,
the direct-copy capacity boundary, wrong returned size and existing output.
These controls do not independently validate compressed arithmetic decoding or
every malformed backreference path; those limits remain explicit.

Review corrections before execution add structured spawn failure retention,
immediate input/output-state checks, complete stream/output identity bindings,
source/config/freeze guards and current-case snapshots after late metadata/pin
checks. Existing control artifacts are checked across calls and before report
publication. Success requires clean return/logs, exact expected output length,
complete bytes and all reported guards/sentinel observations. Faults/timeouts
and unsupported results remain failures with retained artifacts.


## Actual invented-control audit

All 17 declared cases agree: seven complete positive outputs, eight expected
native rejections and two controller redirects without native invocation. The
input-guard truncation exits by SIGSEGV and leaves no output/core file. Existing
output and redirect targets remain unchanged. The trailing-data fixture records
the direct-copy last-byte endpoint and does not claim full consumption.

Independent read-only auditing rehashed all 87 retained artifact identities and
checked every output, guard/size/endpoint report, native stage and case result.
WSL filesystem reads verified both retained symlinks and target bytes. These
are decoder/controller controls, not the 18 future game-build gate negatives.
Controls success does not grant actual-payload execution; a separate import-pin
adapter and actual freeze are still required before the two real-input calls.


## Separate actual-input approval and analysis import closure

Actual-stage approval covers adapter `run_actual_with_import_pins.py`, 5,449
bytes, SHA256
`c8ebd85ae4c3301c0beb48f66522c23807aaf6a12a7871bc12238db0ce3f3bc6`,
and `actual-imports.json`, 647 bytes, SHA256
`c36ed571ca08d5afc15d2ce33c312062dbc108ea6914a8be6424220bf726c8c9`.
Controls/controller/profile stay frozen. Approval permits exactly one decode
per retained raw input/fresh helper, expected length 3550, after both actual
freezes; no decoder/reader algorithm or option changes.

The metadata reader imports `elf32.py`, `prepare_reference.py` and
`inspect_input.py`. Independent hashes agree with their earlier frozen source
identities. The new manifest binds them explicitly, and the adapter checks them
before importing the frozen controller and at its existing pre-call and
post-metadata checkpoints. This adds provenance checks without changing the
parser or decoder. The adapter finally rechecks artifacts and unchanged report
bytes before publishing a separate acceptance witness. The controller report
alone is preliminary. Its stdout is retained through guarded exclusive writing,
even on failure. This distinguishes an accepted bounded preparation from an
unaccepted raw report if later integrity checks fail.

The actual inputs bind to their own 3AH decryption reports, exact 2,926-byte
identities, compression attribute 0x0201 and observed type 6. The expected output
length remains the original declared 3550 bytes. Native guard observations,
complete output equality, bounded PSP metadata and import integrity must all
hold; no signature authentication or module execution is implied.


## Actual preparation and independent final audit

Both actual-stage witnesses accept `PREPARED_BOUNDED_PSP_METADATA`. Complete
outputs are 3,550 bytes, SHA256
`2b4c5af91c7be885054e997bd05a51d8d5d7d544098b2395dc6d893e0e374599`,
with exact byte equality. Each unchanged input is 2,926 bytes. Both native calls
return cleanly with empty stderr, capacity 3552, output alignment 8, 544 prefix
sentinel bytes and 2 slack sentinel bytes unchanged. The compressed cursor is
observed at raw input offset 2926 (body offset 2922); the report still correctly
withholds a uniform input-consumption claim. No padding or algorithm change
was introduced.

Independent raw ELF32 decoding verifies sectionless PRX type 0xFFA0, three
program headers, two bounded PT_LOAD declarations and 206 bytes of unprocessed
PSPREL2 metadata. The second load declares 136 stored bytes and 144 memory bytes;
8 bytes remain declared memory excess, not additional recovered file bytes.
The first header's masked raw physical field selects offset 760, inside its
file-backed extent, for a full 52-byte module-info declaration. Its name bytes
declare `opnssmp`, attributes 0, version bytes [129,1] and a zero terminal byte.
The five pointer words remain raw, unreconstructed and unrelocated. No section
or compiler comment was fabricated and no ownership exclusion follows.

The retained cases are `build/kl4e-opnssmp-a_2x0kfu/opnssmp` and
`build/kl4e-opnssmp-suy2vdj4/opnssmp`. Independent read-only checks rehashed all
ten actual case artifacts, compared both full inputs/outputs, decoded all six
program headers and both module-info structures, and checked all three imported
source identities plus all four freeze sets. The two acceptance witnesses bind
their exact preliminary reports. Guard/size/log observations agree with the
retained files. No decoder or original module was invoked by this reviewer.

This establishes reproducible bounded offline preparation under the reviewed
native implementation. It does not provide signature authentication, a second
independently derived decoder, PSP execution proof, SDK/game ownership,
complete code inventory, compiler attribution or credited matching progress.
All previous failed stages and the parked initializer remain preserved.
