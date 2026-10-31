> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Outside suggestions: review against current evidence

2026-10-30. The user supplied an outside review during approved Bucket 3I.
It is reference advice, not a replacement for the user's decisions or the
current experiment's frozen settings. No suggested tool, flag, wrapper or
runtime test was adopted from it.

## Useful ideas and current status

| Suggestion | Assessment for this project |
| --- | --- |
| Identify the compiler rather than assuming SNC | Compiler-family comparisons have already been performed; original attribution remains unresolved. Our current candidate is unmodified MW219. Eleven MW builds plus GCC/SNC profiles were compared; six of fourteen intervals match under the MW O2 control. The original full chain is still unproven. |
| Inspect comments, strings, sections and segments | Already recorded in the pinned ELF/map. The linked comment names MW MIPS/PSP; it does not identify every unit's compiler or the exact original compiler executable. Our raw MW219 also matches MHP2G's declared pre-patch fingerprint. |
| Read mangled symbols for definitive attribution | Our accepted ELF has no SYMTAB or DYNSYM. Runtime/demangler strings alone cannot establish which compiler produced particular game code. Even surviving names can describe library or mixed-toolchain inputs. |
| Give SNC's own linker an SNC-built minimal object | Already tested. Bucket 3E included an object from that exact SNC profile; 3F repeated the SNC case with default and minimal explicit layouts. Both failed. This establishes the bounded host/tool/input failure, not historical toolchain identity. |
| Treat the linker/finalizer as a separate variable | Useful and retained. MHP2G's declared MW linker/finalizer chain is relevant evidence; availability, complete identities and transformations remain incomplete. The object/linked-stage metadata gap remains explicit. |
| Compare section layout and relocations | Useful for eventual reconstruction. The current seed initializer has a bounded complete body with no external call/address target. Link-layout experiments are outside 3I; missing final-image relocations/symbols cannot reconstruct eliminated intermediate records by themselves. |
| Use richer probes and real data layout | This motivated 3I: one previously inspected archive routine, verified fields and one natural candidate. It does not authorize a broad probe search or importing another game's class offsets. |

The outside review repeatedly describes six probes or an assumed SNC compiler.
Those premises do not reflect the current fourteen-probe, multi-family evidence.
The detailed record is in `TOOLCHAIN.md` and the Bucket 3D–3H checkpoints.

## Ideas requiring different work or acceptance criteria

Assembly-injection wrappers can help reconstruct retained assembly, but injected
bytes cannot earn reviewed C/C++ source credit. Our current candidate has no
assembly, wrapper integration or fallback. A wrapper also does not establish
original compiler/linker attribution.

Flag optimization/search, GC-section layouts and alternative linkers would need
their own evidence and approved experiment. They are not adjustments to make
this function pass. The current MW219/C++/O2 settings stay fixed. Normalized
diffs may help diagnosis, but our acceptance still compares complete bytes after
only explicitly supported relocation handling, with no masking or trimming.

Differential execution could help validate interpreted behavior later; it does
not replace byte matching. Different register allocations alone are not proof
of an ABI violation. Runtime testing remains deferred by the user. Symbolic
execution and additional candidate sweeps are not part of the approved work.

The cited PPSSPP option is real in the inspected upstream
[command-line implementation](https://github.com/hrydgard/ppsspp/blob/master/Core/CmdLine.cpp):
`--re-module` loads a PRX standalone to write a reverse-engineering report, with
related report/filter options. That verifies the option's existence, not that
its annotations constitute dynamic differential execution or prove every
claimed analysis result. No PPSSPP build was installed or run. The report's
specific MetroWrap PSP-integration claim was not independently established in
this bounded review and supplies no reason to introduce assembly injection.

## Current decision

Continue only Bucket 3I as approved: verify the seed initializer's accesses,
declare uncertain types before compilation, freeze one readable candidate and
compare it twice under unchanged diagnostic settings. The full game gate,
source-participation proof, eighteen negative checks and toolchain lock remain
separate unmet milestones. No broader change follows automatically from the
outside advice.

## Third opinion received after the 3I result

The user supplied a second outside text after the completed 3I experiment. It
is also a reference, not authorization to change source, flags or tools.

- **Small matches do not prove a compiler family.** Our Bucket 3D byte-copy
  control matched under both GCC O2 and MW O3. Common instruction sequences can
  coincide, and tiny functions do not uniquely identify a family or revision.
  The MW comment and same-series compiler fingerprint are separate evidence.
- **Build-context explanations are hypotheses.** Inlining, alias rules, source
  types, register lifetimes and scheduling can be useful investigation axes;
  a difference category does not uniquely determine which caused it. No project-
  specific evidence was supplied for unity builds, exact minor-build changes,
  structure-passing thresholds or the proposed environment-variable requirements.
- **Classifying actual differences is useful and already paid off.** The 3I
  mismatch includes four extra LUI/ADDU pairs for repeated receiver-base
  calculation, rather than merely renamed registers. The source stays frozen;
  this observation does not itself select an alias, qualifier or compiler flag.
- **Relocation masking is insufficient for match credit.** We compare complete
  function bytes, explicitly resolve only supported relocations, and reject
  unsupported code relocations. A normalized diagnostic must remain separate
  from exact acceptance and source-participation checks.
- **The crash explanations remain untested alternatives.** Missing module
  metadata, scripts, environment or compatibility issues could be investigated
  in a separately approved synthetic experiment. None was demonstrated as the
  cause of our retained access violation. Our final pspld trials used native
  Windows interop, not wibo, and included an object from the exact bundled SNC
  compiler. A suggestion to switch from wibo to Wine does not describe those
  existing trials.
- **Runtime helpers and padding are clues, not linker identity proofs.** A
  runtime helper can identify linked library code without identifying the tool
  that linked every unit. MIPS zero words can encode NOPs, so zero-versus-NOP
  wording alone is not a distinct padding fingerprint. Section ordering also
  depends on scripts and inputs; our stripped symbol tables and incomplete unit
  map limit conclusions about per-object ordering or data sorting.

Medium switch/float probes, more tools, partial linking and broader flag
experiments are not part of completed 3I. They need their own evidence-led plan
before execution. The immediate retained finding is the natural candidate's
100-byte body versus the complete 68-byte target, with unchanged source/settings
and no exact-match gain. Bucket 3I remains at its review checkpoint.

## Later receiver-base explanation supplied during 3J

The later pasted text proposes late displacement splitting, array-base handling
and store-induced alias invalidation as explanations for the repeated base
calculations. Those are possible investigation hypotheses; the supplied text
does not establish this particular Metrowerks backend's internal pass order or
uniquely identify a cause from the output pattern.

The already retained 3I candidate has five `lui` immediates of `0x0003`, but only
two accessed field offsets: lower `0x2F53C` repeats twice and upper `0x2F540`
repeats three times. The source writes only those two typed volatile fields;
there is no extra character/output-buffer pointer store. Repeated identical or
different displacements can coexist in more than one lowering/optimization
scenario, so the proposed binary decision rule is insufficient to prove alias
invalidation or late splitting. The actual mechanism remains unknown.

Likewise, removing four pairs would make the lengths equal, not necessarily
the complete bytes. Register choices, scheduling and branch displacements still
need exact validation. Native Windows trials establish that wibo was not the
runner for those crashes; they do not exclude every host compatibility problem.

The user approved 3J independently: two invented grouping-only layouts under
unchanged MW219/C++/O2. That tests an observable representation contrast rather
than adopting the claimed explanation. The grouped fixture adds no cached
pointer, reference, array variant, inline helper or flag. The actual 3I game
candidate remains unchanged. This supplied text authorizes no extra experiment.

Completed 3J produces identical whole objects and identical 100-byte functions
for both layouts in two fresh trials, each with five static large-base sites.
Grouping alone does not affect these outputs. This bounded negative result
neither proves a backend mechanism nor rules out every grouped representation.
The user's later clarification agrees that shared upper immediates and repeated
offsets do not uniquely separate aliasing from constant folding, and that a
32-byte length reconciliation does not establish complete byte identity. Full
fixture disassemblies are provided at `BUCKET_03J_CHECKPOINT.md` for a second
inspection. Unsupported static analysis withholds counts; no extra source shape
or broader experiment follows without a separate approved bucket.
