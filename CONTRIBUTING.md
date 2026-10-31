# Contributing

This project is preparing a readable, byte-matching decompilation of Monster
Hunter Portable 3rd, Japanese PSP ULJM05800 v1.02. Start with
[current status](docs/CURRENT_STATUS.md) and [the help request](docs/HELP_WANTED.md).
The historical toolchain is unresolved; this is not a playable game or native port.

## Where to start

Read [the plan after compiler identification](docs/AFTER_TOOLCHAIN.md) for the
pipeline lock, linked baseline, gate and first matching-function checkpoints.
[The matching guide](docs/MATCHING_GUIDE.md) explains the contributor loop from
choosing a task to source review, comparison, integration and PR validation.
Use [the task record template](docs/MATCHING_TASK_TEMPLATE.md) to preserve scope,
attempt history, fixed inputs and results. GitHub PRs have a matching review
template. These guides describe future gate work explicitly; no complete game
build or general function-diff command is available in this snapshot yet.

## Source and matching rules

Write plain, natural source first, with a purpose header and useful comments.
Use C or C++ when evidence supports the source context; label uncertain types,
class layout, qualifiers, names and behavior as hypotheses. Preserve behavior,
including bugs. Prefer a proven matching pattern from a structurally similar
function when one exists.

Compiler, assembler, linker and global flags must be identified and frozen.
Never change flags to make an individual function match. Keep capability research
on invented fixtures separate from a game's fixed diagnostic profile. A public
suggestion is not permission to silently alter either.

After about three unsuccessful plain forms or thirty minutes of plain-source
work, move to documented known shapes. Comment every matching-only shape and
count it. If those fail, park original assembly visibly with the best draft and
an attempt log. The current initializer is parked; do not silently restart its
source budget. Register pins and empty asm are currently zero.

Positively identified Sony SDK and third-party implementations stay labeled
assembly. Classification requires evidence. Imported names/NIDs or library-like
strings do not establish ownership of an unknown implementation.

A function earns match credit only after the clean complete game/module build is
byte-identical and the required eighteen negative gate checks prove source
participation and reject stale objects, failed compilation, missing inputs and
undeclared assembly fallback. That gate does not exist yet. Exact isolated
objects, passing tooling tests and copied assembly earn no source match credit.

## Reviewable work

Keep changes in small declared buckets. Explain the problem, intended scope,
fixed inputs/settings, validation and unresolved assumptions before an experiment.
Freeze source/profiles and controls before results; retain failed outcomes and
complete function extents. Separate source review, binary equality, linked-source
coverage, library identification and runtime claims. Do not pool favorable results
from different configurations into a matching toolchain.

For compiler help, provide primary citations or a small invented fixture, full
version/hash and stage commands, complete symbols/relocations and reproducible
outputs. Include failures and uncertainty. The issue template asks for these facts;
it does not ask you to distribute proprietary tools or original game bytes.

## Public repository boundaries

Do not submit game images, assets, extracted game code/data, original disassembly,
SDK/compiler binaries, keys, private evidence/logs, machine paths, credentials or
personal saved-game data. Use your own lawful local inputs for research. Share
invented reproducers and descriptions without those materials. Third-party source
excerpts need their own provenance/license handling; link primary sources rather
than copying an unrelated project's documentation wholesale.

No game/module execution or native-port implementation is part of the current
matching work. The future Windows/Linux port follows complete original-game
matching; single-player comes first. An emulator, static recompiler, engine rewrite
or modern compiler does not substitute for the byte-matching requirement.
