> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# PSP GCC 4.3.5 candidate: verified provisioning, failed fixture validation

The publisher's MinPSP 0.10.0 AMD64 archive supplies a working PSP GCC 4.3.5
C++ frontend. Its exact archive SHA-256 is
`0caefe824ace40687032c492acbcc6e894c5ed2acb881d20cab7294fea134055`.
This is a dated community candidate, not attribution to Capcom's original build.

Only the C/C++ frontends and two genuine legacy support libraries were extracted
into the project's private toolchain directory. No installer or package script
ran, and no system library was replaced. The private SONAME files contain the
same bytes as the corresponding verified legacy libraries. Version and target
help calls pass under the pinned WSL loader/libc and private library path.
`config/psp-gcc435-candidate.json` pins these inputs; the independent review
records publisher provenance and package-member verification.

The frozen two-fixture comparison does **not** pass. Both fresh trials first
reproduce the old GCC static-object and grouped-address whole-object controls.
The new frontend then compiles the invented static-object fixture with exit0
and empty diagnostics, but the assembler warns:

```
.gnu_attribute 4,2 requires `singlefloat'
```

The existing strict pipeline rejects this warning even though the assembler
exits0. Both trials therefore abort unscored; neither runs the new grouped-
address case. Six compiler calls occurred out of eight planned. The two partial
new assembly files and objects repeat byte for byte; no comparison result is
published as successful. Raw stages, outputs and failure records remain local.

The target help already declares `-msingle-float` enabled and `-mdouble-float`
disabled. The retained assembly declares the corresponding GNU attribute. This
supports a separately reviewed assembler ABI consistency investigation. It
does not authorize compiler flag tuning or erasing this failed experiment.

Reviews: `PSP_GCC435_CANDIDATE_REVIEW.md` and
`BUCKET_03Z_VALIDATION_NOTES.md`. Private evidence: `evidence/bucket-03z/`.
The compiler/toolchain remains unlocked. No game draft, source form, original
target, linker, game runtime or credited match is involved in this bucket.
