# From compiler identification to matching contributions

This is the forward plan for the Japanese PSP ULJM05800 v1.02 target.
It does not select a compiler, approve a build architecture or announce a working
game build. [Current status](CURRENT_STATUS.md) still applies: the toolchain is
unlocked, no game functions have match credit, and the full-game gate is absent.

Each stage below is a small work bucket: present its concrete plan, produce the
listed output, then stop at a review checkpoint before the next stage. Large
stages can be split further. Finding a promising compiler does not skip the
assembler, linker, source-context or validation work.

## 1. Establish and review the complete build pipeline

Record the compiler, assembler, linker, relevant driver/runtime components,
versions and executable hashes. Record exact project-wide commands, language
mode, ABI, include setup, environment requirements and host runner. Distinguish
compiler output from assembler transformations and linked runtime metadata.
Provide setup instructions for separately obtained tools, without bundling them.

Freeze a representative corpus and controls before comparing results. Include
more than leaf functions: calls/relocations, large member offsets, integer
arithmetic, C++ initialization and translation-unit effects where relevant.
Repeat clean trials and retain failures. Equal size, a banner or one small exact
body alone cannot settle the original pipeline. Identify remaining hypotheses.

Output: a provenance-backed toolchain-lock proposal, repeat results and a clean
setup recipe. Review must explicitly confirm which components/settings are
locked and which remain uncertain. Different module configurations need evidence
and declared scope; no flags may be chosen to suit an individual function.

## 2. Establish code scope and a reproducible linked baseline

Verify the selected image/reference identities and local preparation recipe.
Extend the inventory to every executable/code module and overlay, with module
identity, load context, reviewed boundaries, sections and ownership evidence.
The known 355-overlay set is not yet a complete all-code denominator. Shared
addresses and zero-sized descriptors must retain their ambiguities.

Reconstruct section layout, symbols, relocations, data placement and link order.
Keep original assets unchanged. Keep Sony SDK and positively identified third-party
implementations in explicitly declared assembly units. Unknown ownership remains
unclassified. Assembly/reference material is generated or supplied locally and
stays outside the public payload.

Output: a repeatable, byte-identical assembly-based baseline covering the agreed
targets, with manifests and link provenance. This baseline earns zero source
match credit. If the inventory is incomplete, label the scope incomplete rather
than presenting it as a complete game rebuild. Review the target list, module
ownership and source/layout organization before integrating reconstructed code.

## 3. Build the fail-closed gate before awarding matches

Implement a clean build that checks all expected targets against immutable local
references, compares every required byte and propagates every tool failure.
Inputs, generated objects, outputs and link participation must have explicit
provenance. Missing inputs/targets, stale outputs or undeclared assembly must fail.
Timestamps alone are insufficient proof that the submitted source was rebuilt.

Implement and review the required eighteen negative checks in disposable work
directories, together with an unchanged positive control. The checks must cover
output corruption, source/data changes reaching output, compilation/assembly/link
failure, missing inputs/outputs, stale-object reuse, undeclared assembly fallback
and module/overlay-specific failures. The precise eighteen-check mapping must be
documented for this PSP pipeline; the PS1 reference project's scripts and layout
are not drop-in PSP tools. Each injected fault must produce the expected failure
and a nonzero exit, without changing the real checkout or reference files.

Output: documented real gate commands, a positive baseline pass and all eighteen
negative checks passing their expected rejection assertions. Review the source-
participation proof and failure coverage. Python tooling tests are separate.
There are no working full-game gate commands to run in this snapshot yet.
When these checks actually work, update current status, reproduction instructions,
the matching guide and the PR template with the real commands/results. Remove
their unavailable warnings only after that validation, not when work merely starts.

## 4. Prove the contribution loop with one small game function

Choose a routine with reviewed boundaries and ownership/context, then follow the
[matching guide](MATCHING_GUIDE.md). Start with natural C/C++, a purpose header
and useful comments. Integrate it into the reviewed build layout and show that
the source object supplies its linked code instead of the original assembly.

Run the clean full-target gate and the eighteen negative checks. Record exact
source/object/output identities, the attempt log, any commented tricks and the
link evidence. A byte-identical isolated object remains diagnostic until this
integration proof passes.

Output: one reviewed pilot PR, updated coverage/attempt records and instructions
another contributor can actually reproduce. Review readability and binary/source
proof separately. If it remains unmatched, park it visibly with notes; no credit
is granted and no source attempt is silently discarded.

## 5. Grow through small, coordinated matching tasks

Publish available tasks with module/range identities and known context. Use the
[task template](MATCHING_TASK_TEMPLATE.md) and keep ownership visible so helpers
do not duplicate work. Expand group size after the pilot process works. Prefer
already proven source patterns for structurally similar functions.

Keep implementation sources, shared declarations, build metadata and generated
local assembly/reference material distinct. Organize game code by understood
module/system and original translation-unit evidence; do not invent an engine
architecture or split every routine into a file merely to force code generation.
Precise directories and build tools are a later reviewed implementation choice.

Output per bucket: readable source, reproducible validation, updated manifests/
status and a review checkpoint. Track reconstructed source, linked-source
coverage, binary identity, ownership, tricks and runtime checks separately.
Do not report a completion percentage without a proved code denominator.

## 6. Complete matching before starting the native port

Finish all game-owned code in scope and revalidate the complete clean build,
source participation, ownership exclusions, unchanged assets and negative checks.
Parked functions remain visible unfinished game-code work. An assembly baseline
or emulator is not completion of the decompilation.

Only after the matching milestone is accepted do native-port implementation
buckets begin. Hardware separation, platform replacements and behavior tests
then receive their own plans and checkpoints. Windows/Linux, original timing,
PSP saves, local downloaded quests and the first village/one-hunt milestone remain
the agreed goals; renderer/backend and other unresolved choices remain open.
Runtime validation is a separate requirement to plan, not a claim established by
the byte gate. Co-op, translation and HD support remain later work.
