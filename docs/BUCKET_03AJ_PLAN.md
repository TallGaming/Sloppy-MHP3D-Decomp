> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AJ proposal: bounded PSP import-table inventory

Begin only after3AI closes, under the same advance approval ending16:21:44UTC.
The new offline preparation makes the small OPNSSMP container available, while
the main executable provides our known absolute-address control. Use only these
two existing inputs. Do not expand to other modules inside this bucket.

First pin/review primary PSP import-table structures and stub definitions from
the already selected public PSPSDK/PPSSPP source versions. Distinguish the main
ET_EXEC image's declared virtual addresses from a PRX's unrelocated raw fields.
Map a pointer only through one unambiguous file-backed PT_LOAD interval; reject
ambiguous/unmapped/truncated tables and unsupported record forms as uninterpreted.
Do not apply relocations or infer a loaded runtime address.

Implement a small read-only parser with meaningful invented bounds/record/string/
aliasing tests. Bound counts, table lengths, file-backed strings, NID arrays and
function-stub bytes. Preserve raw record words, names, NIDs and mapping evidence.
Record exact stub instruction words rather than assuming their shape. A library
name/NID is a declared binding, not authentication or proof of that library's
implementation ownership. Unsupported variable imports or record extensions
must remain explicit; never silently skip them or manufacture a decoded total.

Review/freeze parser, source references, tests and the two exact input records
before actual parsing. Run twice into fresh reports; compare complete semantic
reports and independently map sampled original bytes. Existing inputs/readers,
compiler flags, parked source and all completed evidence stay unchanged.

Primary owns controller/profile/checkpoint and independent parser/test/output
review. Helper1 owns format-source and pointer/record semantics review. Helper2
owns parser/tests and implementation validation. Primary and helper1 review
exact source/tests before freeze, then audit original bytes/output independently
of the implementation writer. One writer per file. No module code executes; no
Ghidra relabeling, assembly generation, SDK ownership exclusion, original C/C++
rewrite, compiler selection or port implementation belongs here.

This advances the code inventory and gives later library-label work a bounded
basis. It does not finish the all-module inventory or the18-test build gate.
After review, explicitly choose a next bucket; do not treat a recognizable
library name as permission to rewrite SDK code or change the toolchain.
