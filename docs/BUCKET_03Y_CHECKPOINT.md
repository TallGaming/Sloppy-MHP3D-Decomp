> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3Y: GNU backend provenance — completed checkpoint

**The address decomposition and filled BNE slots are already present in the
tested compiler's emitted assembly.** Retaining that assembly is neutral in
both fresh invented-fixture trials: all four complete objects and both raw
assembly copies agree exactly with the ordinary pipeline's hashes.

Upstream GCC3.3.3's explicit 32KiB-window macro predicts the tested splits.
GCC3.4.6's different signed-high/low algorithm predicts the original routine's
`0x30000` plus negative-displacement pattern. This provides a concrete later-GNU
backend lead. A pinned 2010 PSP recipe also selects GCC4.3.5 and binutils2.18;
it is build metadata, not proof of a particular binary or the game's compiler.

`GNU_ASSEMBLY_PROVENANCE.md` records stage attribution, exact objects/assembly,
source changes across versions and limits. Reviews are
`GNU_BACKEND_PROVENANCE_REVIEW.md` and `BUCKET_03Y_VALIDATION_NOTES.md`; private
artifacts and source caches are under `evidence/bucket-03y/`.

Both exact reviews/freeze precede all four invented compiles. No compiler flags,
game source or old pipeline API change. The final return NOP is assembler-added
in this fixture, and move expansion is untested. No IR or historical profile
claim follows from final assembly alone.

Last full suite remains **340 WSL passes, zero skips** from 3U; one-off mock
controls and actual capture parity are separate. Source counters stay three
plain attempts/one commented shape, with one PARKED routine, zero pins/empty asm,
and zero credited matches/linked-source functions. Full-game gate/18 negative
checks and all matching-before-port requirements remain unchanged.

Completed under timed approval, pending user review. Next bounded proposal:
verify and provision one later PSP GNU candidate from a pinned public release
or complete published build recipe, then validate invented fixtures only under
a frozen uniform profile. No new candidate should be selected merely because
one function is four bytes short, and no parked source is retuned.
