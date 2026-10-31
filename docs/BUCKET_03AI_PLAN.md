> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AI: bounded host KL4E preparation

Continue within the renewed approval ending16:21:44UTC. Prepare the retained
OPNSSMP KL4E bytes using the existing pinned public native C decoder as an
offline data tool. This is not game source, a native SDK replacement or original
MIPS code execution. Keep the original decoder and every input unchanged;
never use JPCSP's optional MIPS-interpreter decompression path.

Stage A reviews the native decoder ABI, stream prefix, input/output/end-pointer
behavior and constraints. Build a small Linux/WSL host wrapper around that
unchanged source. The decoder has no input-length argument and uses absolute
output-address low bits for probabilities, so the wrapper must preserve8-byte
output alignment, bound input with a guard page, and guard/check output memory.
Use a declared rounded capacity above expected length, require the exact returned
length, and verify all bytes beyond that expected result remain sentinels.
Do not silently pad or repair compressed input. Record end-pointer observations
without assuming identical semantics for direct-copy and compressed streams.

Review/freeze source/build recipe before native compilation. Pin the binary and
runtime before execution; invented direct-copy and malformed/truncated/size/
existing-output controls must pass first. Any memory fault, timeout, decoder
error or bound violation is retained as failure, never a successful extraction.
No attempt to fix/reshape the decoder algorithm belongs here.

After both Stage A audits and a separate actual-input freeze, decode each retained
3AH raw payload once in fresh cases (two trials), with fixed wrapper parameters
derived from the unchanged declared ELF size3550. Require equal complete output
bytes, exact length, immutable inputs and bounded PSP metadata via the already
reviewed copy-loader reader. Missing/unsupported output remains uninterpreted;
this preparation is not signature authentication or independent gameplay proof.
If a second host implementation is needed, propose a separate bounded check.

Primary owns Python build/controller profiles, integration and checkpoint.
Helper1 owns `KL4E_HOST_PREPARATION_REVIEW.md`, exact decoder/source/ABI/bounds
review and independent output audit. Helper2 owns `tools/host/kl4e_guarded.c`
and `BUCKET_03AI_VALIDATION_NOTES.md`, the guarded native wrapper, meaningful
invented boundary controls and independent validation. One writer per file;
both reviews precede each frozen execution stage. No game compiler flags,
source attempts, ownership exclusions, linker/game runtime, port or match credit.
