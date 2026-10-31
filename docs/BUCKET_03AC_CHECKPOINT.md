> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3AC: supplemental container inventory — completed checkpoint

**Both fresh sets reproduce all eight payloads and deterministic manifests.**
The main EBOOT whole-byte control passes. BOOT is entirely zero-filled, not
merely zero at its prefix. OPNSSMP and the packaged updater have declared PSP
headers; four archive SCE candidates stay raw and uninterpreted. Exact archive
lengths exclude sector padding. See `SUPPLEMENTAL_MODULE_INVENTORY.md`.

Both reviews and the source/profile/test freeze precede real recovery. Every
ISO catalogue checksum, directory identity, archive index/length/prefix and
preserved source/toolchain/assembly input passes before/after checks. All sixteen
payload copies and both manifests/reports agree. Unknown wrapper offsets,
ownership and code extents remain unknown; complete code inventory is not claimed.

All **352 WSL tooling tests pass with zero skips**, including twelve new bounds/
identity/publication tests. No decryption/decompression, compiler call, game
execution, source rewrite, linker or native port occurs. The full matching gate
and18 negative checks remain unimplemented.

Parking/counters remain one PARKED routine, three plain attempts, one commented
shape, zero register pins/empty asm, zero credited matches/linked-source
functions. The clean PSP reference, privacy, fixed compiler flags and
matching-before-port requirements stay unchanged. Completed under timed
approval, pending output review.

Next bounded possibility: review the public loader's declared SCE wrapper-length
model against these retained bytes, and assess whether supported inner
containers can be prepared statically. It needs its own precise plan and freeze;
no universal wrapper offset or Sony-library attribution is assumed.
