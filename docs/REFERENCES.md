> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Reference material and evidence boundaries

The user supplied these documents from a successful PS1 matching decompilation:

- `<ps1-reference-project>/docs/for-decompers/README.md`
- `<ps1-reference-project>/docs/for-decompers/PS1_DECOMP_PLAYBOOK.md`
- `<ps1-reference-project>/docs/for-decompers/WORKFLOW.md`
- `<ps1-reference-project>/docs/for-decompers/GATE_AND_NEG_TESTS.md`
- `<ps1-reference-project>/docs/for-decompers/MATCHING_PRACTICES.md`
- `<ps1-reference-project>/docs/for-decompers/MATCHING_TIPS.md`
- `<ps1-reference-project>/docs/for-decompers/STUCK.md`
- `<ps1-reference-project>/docs/for-decompers/TOOLCHAIN.md`
- `<ps1-reference-project>/docs/for-decompers/OTHER_PS1_DECOMPS.md`

Apply the methodology: readable source first, compare generated instructions,
reuse matched structures, investigate compiler behavior, document tricks,
declare retained assembly, and require a fresh full byte-identical build.

Do not transfer PS1 addresses, module boundaries, library classifications,
compiler versions, flags, assembler patches, existing progress counts, passing
tests, runtime claims, or project-specific instructions and approval history.
The user's explicit requirements and subsequent interview answers govern this
project; the reference documents are supporting material.

The reference project's 18 checks must be adapted to this game's actual build.
The essential checks include positive controls plus deliberate output mutation,
assembly mutation and failure, missing or undeclared inputs, source constant
mutation, source compile failure, stale objects, source participation in the
link, and independent module coverage. The exact executable/module layout and
the implementation of those checks are not established yet. Test counts alone
do not prove that the gate is sound.
