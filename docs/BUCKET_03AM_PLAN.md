> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AM: invented-only Metrowerks capability matrix

Continue within the approval ending 16:21:44 UTC. The game toolchain is still
unlocked; all existing game diagnostic profiles and source files stay frozen.
This experiment has no original game function, target bytes or match score.

The retained compiler help says level 3 adds instruction scheduling and strength
reduction. The previous four O2 diagnostics differed materially in arithmetic
lowering. Test what the existing MW219 binary can generate from invented code,
before drawing a compiler-family conclusion from those results.

Use exactly the eight project-wide investigation settings already declared in
`config/compiler-candidates.json`: default, O0, O1, O2, O3, O4, O4-p and O4-s.
Keep the already validated C++ language/common flags, binary and runner unchanged.
Apply each setting uniformly to both complete invented translation units:
the unchanged `address_reuse_grouped.cpp` fixture and a new small unsigned
arithmetic fixture. This is compiler-capability research, not a change to any
game-function flag or selection of an original project configuration.

Review/freeze the sources, complete matrix, compiler help/pipeline/control pins,
symbol-extent rules and opcode-analysis limits before compilation. Each of two
fresh trials starts by reproducing the complete historical MW C++ producer
control. Reuse exact staged execution/retention behavior. Every declared matrix
cell must run or remain explicitly unscored; no favorable-cell selection.

Retain whole objects, logs and disassembly. Compare complete repeat objects.
Report raw static DIVU, multiply/high-result and Allegrex MSUB encoding sites
within complete declared function extents, with the original words/offsets.
These are static encoding observations, not runtime execution counts. Unsupported
metadata/decoding stays uninterpreted; do not infer dataflow or normalize bytes.
Any address-reuse result must use the existing fail-closed checker or remain
uninterpreted, never an assumed count.

Primary owns the new invented source, profile, integration/checkpoint and
independent code/output review. Helper1 owns documented setting/control/ISA
provenance and independent review. Helper2 owns controller/static observations
and implementation validation. Primary and helper1 approve before the freeze,
then audit results independently of the implementation writer.

No game source is compiled, no original module executes, no source attempt or
trick count changes and no game toolchain is locked. A later whole-project
profile proposal must be separate, apply uniformly across a representative
frozen corpus and preserve the user's prohibition on per-function flag tuning.
Do not use this capability matrix as permission to alter a game function's flags.
