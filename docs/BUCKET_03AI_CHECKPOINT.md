> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AI: guarded offline KL4E preparation

Both retained OPNSSMP raw copies now produce the same complete3,550-byte ELF,
SHA256 `2b4c5af91c7be885054e997bd05a51d8d5d7d544098b2395dc6d893e0e374599`.
This resolves the extraction/format-preparation blocker. It is not a game build,
signature authentication, library ownership decision or credited decompilation.

The unchanged public native `kl4e.c` was linked only into an offline Linux host
utility. No original module instructions or MIPS interpreter were executed.
The decoder has no input-length parameter and depends on absolute output-address
low bits. The reviewed wrapper therefore puts the real input end directly beside
an inaccessible page, makes input read-only, guarantees eight-byte output
alignment, and checks an output end guard plus every prefix/slack sentinel byte.
Input was neither padded nor repaired. The decoder algorithm was not modified.

Two reviewed/frozen fresh host builds agree in all21,384 binary bytes, SHA256
`20d9ee7162765e3af8797f7bd8d9dfbffed6cbb14e37a4380e9a8d17fc2d25c9`.
The fixed host recipe records138 header inputs before object generation. Static
inspection finds only libc and the default loader, without RPATH/RUNPATH. Both
logs retain the same existing decoder signedness warning; the wrapper is clean.
These host build flags do not select or change any game compiler configuration.

Separate execution review/freeze preceded17 invented controls: seven complete
copy outputs, eight expected native failures, and two controller path rejections.
There were15 native calls. The deliberately truncated copy faults with SIGSEGV
without an output or core file. Existing output and redirect targets remain
unchanged. A trailing-data case is accepted as a copy but explicitly makes no
full-consumption claim. These are extraction-tool checks, not the required18
future full-game build-gate negative tests or a general compressed-codec proof.

Only after the control audits and separate actual-stage freezes were the two
retained2,926-byte raw copies decoded, once per fresh binary. Both return3550,
with capacity3552,544 prefix sentinel bytes and two slack bytes intact, clean
stderr and a reported compressed cursor at raw offset2926. This endpoint is an
observation, not a uniform stream-authentication rule. The direct-copy branch
instead reports its last source byte.

The unchanged Bucket3AF PSP metadata reader finds a sectionless ET_PRX image,
two bounded PT_LOAD declarations and206 relocation2 bytes retained without
interpretation/application. Module-info at file offset760 declares `opnssmp`,
attributes0 and version bytes[129,1]. The load-memory excess is eight bytes.
Exports/imports remain raw pointers. No compiler comments or ownership proof
follow from this preparation, and the module has not been loaded or executed.

The reader's three imports are pinned separately. A narrow host-stage adapter
checks them before import, at existing controller boundaries, and after reading
metadata. Raw actual-trial reports are preliminary: acceptance requires their
matching `actual-stage-N.json` witness after final artifact/dependency checks.
The already completed controls driver/profile were preserved unchanged.

Evidence is private under `evidence/bucket-03ai/`: two build reports, controls,
four distinct freeze records, actual dependency manifest/adapter, two preliminary
actual reports and two final witnesses. The complete case files stay under the
reported fresh `build/` directories. Public/source/bounds review is
`KL4E_HOST_PREPARATION_REVIEW.md`; independent validation is
`BUCKET_03AI_VALIDATION_NOTES.md`. Final independent closeout is recorded in the
verification summary; both owned reviews and independent audits have passed.

The native decoder and the cached JPCSP Java implementation share algorithm
ancestry; a future Java comparison would check host-language behavior, not an
independently derived codec. No second implementation was run in this bucket.
The earlier helper failure, KL4E-uninterpreted result and all frozen earlier
artifacts remain retained.

The game toolchain and complete code inventory remain unresolved. Counts stay
zero credited matches/linked-source functions, one visibly parked initializer,
three plain attempts plus one commented shape, zero register pins/empty asm.
The last full tooling suite remains352 WSL passes with no skips from3AC; the
new native controls are reported separately. No native port begins before all
game code matches. Continue only through another documented reviewed bucket
inside the existing advance approval ending16:21:44UTC.
