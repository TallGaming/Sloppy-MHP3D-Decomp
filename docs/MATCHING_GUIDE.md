# How to contribute matching code

Read [CONTRIBUTING](../CONTRIBUTING.md), [current status](CURRENT_STATUS.md) and
[the roadmap](AFTER_TOOLCHAIN.md) first. This guide describes the contribution
loop we will use after the pipeline and gate are ready. Today you can contribute
compiler evidence, invented reproducers, tooling fixes and source/context
analysis. Game-source drafts remain diagnostic; there is no complete build or
game-match credit yet. Do not invent a gate command or treat CI as that gate.

## 1. Agree on a small task

Use an issue/task record to identify the proposed routine and check whether
someone is already working on it. Record the reference version/hash, module or
overlay identity, address with exclusive end, local file mapping, original
interval size/hash and boundary evidence. An address alone cannot distinguish
overlays sharing a load range. Record ownership evidence and unresolved types,
callee names, class layout or translation-unit assumptions.

Use the [task template](MATCHING_TASK_TEMPLATE.md). Have the maintainer confirm
the task and its intended scope before a matching bucket starts. Do not rewrite
Sony SDK or positively identified third-party implementations. Unclassified code
needs investigation; an import name is not ownership proof. The parked archive
initializer already has a spent attempt history: coordinate any evidence-backed
revisit rather than resetting its budget.

## 2. Prepare the exact local inputs

Use the agreed PSP v1.02 reference and the reviewed setup/profile once available.
Keep game material and proprietary tools outside the public submission. Verify
their identities locally. Work on a branch with only the task's related changes.
Do not alter compiler flags, frozen toolchain headers, ABI options or linker
settings to help a particular function. Changes to game declarations need
source-context evidence and review. Report a global pipeline problem separately.

The current [public diagnostic tool](../tools/repro/README.md) supports only the
two named archive cases. Its commands reproduce investigation profiles, not a
selected game build or a general matching gate. It rejects code relocations;
do not remove relocations or select a favorable subrange to get past it.
General relocatable-function work will require the reviewed linker-aware build.

## 3. Understand behavior and write natural source

Review the complete routine and its context locally, including callees, data
references, delay slots, signedness, widths, access order and return behavior.
Keep uncertain declarations clearly labeled. Choose C or C++ from evidence,
preserving original translation-unit relationships where known. A decompiler
can supply an initial hypothesis; its output is not proof of types or intent.

Give each function a purpose header: what it does, inputs/outputs, important
side effects and any uncertainty. Comment meaningful behavior, layout assumptions
and constraints. Choose understandable analysis names when original names are
unknown. Preserve behavior, including apparent bugs; improvements belong later.
Avoid speculative refactors of neighboring functions or shared types.

Start with the source a person would naturally write. An address-bearing local
variable or unusual order chosen only to influence matching is a source-shape
hypothesis and must be described honestly. Do not add pins, barriers or expression
permutations preemptively. Reuse a proven matching pattern when the structure and
semantics support it, explaining any non-obvious shape.

## 4. Compare, explain and record each attempt

Compile through the unchanged reviewed profile. Compare the complete candidate
extent and exact bytes, including registers, scheduling and delay slots. Keep
compiler output, assembler output and linked results distinct. Review any size,
address construction, access order or branch difference; equal length is not a
match. Never trim, mask, patch target bytes or normalize registers to claim one.

Keep an attempt log: source identity, hypothesis, fixed profile/tool identities,
commands, complete extent/hash, outcome, time spent and next interpretation.
Retain unsuccessful drafts/notes locally and share source hypotheses and safe
summaries. Running the same source under another diagnostic compiler does not
erase prior source attempts. A fixed-profile repeat is not a new source form.

After about three unsuccessful plain forms or thirty minutes, stop the plain-C
loop. Review known matching shapes. Comment every non-obvious matching choice
with its reason and update HANDOFF totals for register pins, empty-asm lines and
functions with commented shapes. If documented shapes fail, park the routine:
retain the best draft and log, mark its status and explicit local assembly
fallback, and continue with a reviewed task. Parking earns no match credit and
must never silently route a failed compilation to original assembly.

## 5. Integrate and prove source participation

Once the real build exists, add the source to its explicit module/translation-unit
configuration and remove the corresponding original-code fallback for that
interval. Preserve other declared assembly/library units and data/layout.
Show from the fresh object/link map that the submitted source supplies the
intended function and contributes to the correct target. A source file in Git,
a matching unused object or a timestamp is insufficient.

Run the documented clean full-target gate and all eighteen negative checks on
the proposed tree. The positive build must match all expected executables/code
modules byte for byte and preserve assets. The negative tests must demonstrate
rejection of failed compilation, stale objects and undeclared fallback, as well
as the other reviewed failure cases. Report exact commands/results, affected
targets and omissions. If the pipeline or gate is unavailable, mark this proof
unavailable and keep the contribution diagnostic.

Run appropriate Python tooling tests if your patch changes those tools. They
are not the game gate. Byte equality, runtime behavior and review quality are
distinct checks; do not claim a playtest or native-port result from a match.

## 6. Submit a reviewable PR

Use the repository PR template. Include the task/range, behavior and uncertainties,
source and tool/profile identities, complete comparison result, attempt history,
trick-counter changes, integration evidence and validation. Keep raw game bytes,
disassembly, compiler distributions, secrets and personal paths out of the PR.
Use hashes and safe summaries; public requests must not require uploading those
materials. Source drafts and invented fixtures can be reviewed publicly.

Update the task status and HANDOFF, without granting yourself match credit from
an isolated comparison. Keep diagnostic, parked, linked-source and gate-verified
states distinguishable. The maintainer reviews readability, justified declarations,
source participation and full-build evidence before awarding credit. Stop at the
bucket checkpoint; do not merge another bucket or begin port work automatically.

The project-wide license is still unselected; see
[LICENSE_STATUS](../LICENSE_STATUS.md). No PR template invents a license grant,
CLA or permission to redistribute third-party material.
