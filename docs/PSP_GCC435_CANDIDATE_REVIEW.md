> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# PSP GCC4.3.5 candidate review — Bucket 3Z

This bucket verifies one later PSP GNU candidate before execution and uses only
the existing invented fixtures after a separate review/freeze. It changes no
game draft, target, flag matrix, source-attempt counter or parking decision.
No historical compiler lock follows from candidate availability.

## Publisher archive lead

The reviewer independently read the publisher's
[SourceForge0.10.0 folder](https://sourceforge.net/projects/minpspw/files/SDK%20%2B%20devpak/pspsdk%200.10.0/).
It lists Linux amd64/i386 Debian packages, an i386 tarball and a Windows
installer. An initial provisional impression that this release was Windows-only
was corrected immediately after this folder inspection. The GitHub releases
API has no assets; that is not evidence that publisher binaries are unavailable.

The selected single candidate is
`minpspw_0.10.0-1ubuntu0_amd64.deb`, listed2010-11-17, approximately80.7MB.
Its [publisher download page](https://sourceforge.net/projects/minpspw/files/SDK%20%2B%20devpak/pspsdk%200.10.0/minpspw_0.10.0-1ubuntu0_amd64.deb/download)
displays SHA-256
`0caefe824ace40687032c492acbcc6e894c5ed2acb881d20cab7294fea134055`,
independently confirmed by this reviewer before local candidate execution.
The alternative i386 tarball's
[page](https://sourceforge.net/projects/minpspw/files/SDK%20%2B%20devpak/pspsdk%200.10.0/minpspw-0.10.0-linux_i386.tar.bz2/download)
displays `b43e3aed54bc4d9db2d4ccb5b8b68ab302a0984a7da43bf80c0c6e2ea27f597a`;
it is only an availability observation, not a second candidate to provision.

Publisher package identity is stronger than a product-label guess but does not
prove its cc1plus version, member identities, host dependencies or original-game
use. The primary must hash the downloaded archive, inspect member/control
metadata without installing/running package scripts, and freeze the isolated
compiler/dependencies before version/help or fixture execution. This helper
downloaded no compiler binary and executed no candidate.

## Dated source context and unused fallback

The separate dated recipe
[`pmlopes/minpsp@cfc3435509fefb0e05cb55acf2c2deb34b592399`](https://github.com/pmlopes/minpsp/blob/cfc3435509fefb0e05cb55acf2c2deb34b592399/toolchain.sh)
identifies PSPSDK0.10.1 and GCC4.3.5 on2010-11-26. This is adjacent release
context, not proof that its exact source/patch tree generated the selected0.10.0
binary. The recipe fetches official GNU GCC4.3.5 source and applies optional
PSP, checked-in MINPSPW and local in-source patches in that order. Its unpinned
SVN checkout prevents reproducing a unique complete historical checkout from
the script alone.

The checked-in
[`gcc-4.3.5-MINPSPW.patch`](https://github.com/pmlopes/minpsp/blob/cfc3435509fefb0e05cb55acf2c2deb34b592399/mingw/patches/gcc-4.3.5-MINPSPW.patch)
is6,652,385 bytes, SHA-256
`8e08692cc5479aac769519fecaf2cdf18f8a55d745b7b8e83b93bdba390bcfea`.
Its459 file diffs target pristine4.3.5.orig and include Allegrex/PSP target
recognition, backend/scheduling support and D-language additions. Added
`config.gcc` target settings select Allegrex, ISA2 and EABI; added `psp.h`
defines PSP preprocessor/startfile/assembler context. These describe the public
patch, not verified installed backend defaults or settings to copy into a
function experiment.

The dated
[`psptoolchain@00f2bb1e29018869070116969d89861b7c0a08a6`](https://github.com/pspdev/psptoolchain/tree/00f2bb1e29018869070116969d89861b7c0a08a6)
mirror contains `gcc-4.3.2-PSP.patch`, with no4.3.5 PSP patch. Therefore that
snapshot would skip the recipe's optional first4.3.5 patch; it cannot prove
what every contemporaneous SVN checkout contained. The cached public patch,
readme and tree metadata use only `helper-map-*` paths under
`evidence/bucket-03z/`. No whole vendor build script was run. Source-build
fallback remains unused while the publisher prebuilt is assessed.

Candidate member/dependency review, exact fixture approval and retained results
will be recorded separately after the primary supplies the pinned inventory.

## Independent static archive/member verification

The primary's successful acquisition retained one80,695,848-byte amd64 package
with the exact publisher SHA-256 above. Earlier direct mirror requests returned
403; their failure records remain beside `acquisition-wsl.json`. The successful
request followed the normal publisher-page redirects. This helper independently
rehashed the local archive and parsed its ar members and compressed data archive
without installation, extraction scripts or candidate execution.

Only two regular frontend members were selected into the private toolchain:

| Archive member, beneath `./opt/pspsdk/libexec/gcc/psp/4.3.5/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `cc1plus` | 6,745,856 | `66324e6459dd5098606480fc5a442dd02afadbdba52a94d8372609a952c5baf3` |
| `cc1` | 6,102,752 | `e29857596843952300e21f45728f5193189cd982badc824edb323ac89bd7de42` |

The reviewer compared each retained frontend directly with its complete regular
archive member and independently parsed its ELF class/machine. The C++ frontend
is an ELF64 little-endian x86-64 host executable with embedded GCC4.3.5 source
paths. Independent dynamic-tag parsing matches readelf: `libmpfr.so.4`,
`libgmp.so.3` and `libc.so.6` are required. Its interpreter is
`/lib64/ld-linux-x86-64.so.2`. Package control says `minpspw-pspsdk`, version0.10,
architectureamd64; that package version is distinct from frontend version.

The required GMP/MPFR SONAMEs differ from those currently installed. Exact
publisher legacy-library packages must be pinned/extracted privately and their
actual loader resolution reviewed before any candidate execution. Substituting
modern library symlinks would not preserve dependency identity. The source-build
fallback is unnecessary if this single publisher binary becomes usable; no
fallback build or second binary acquisition is approved by this review.

## Private runtime and first-execution approval

The exact legacy-library closure is supplied by the official
[Ubuntu Maverick amd64 package index](https://old-releases.ubuntu.com/ubuntu/dists/maverick/main/binary-amd64/Packages.gz),
1,909,018 bytes, SHA-256
`4ff91eab6a4e820fb8f90244e3830f4070590e5ec5151fb708dcc19987c7e2c5`.
The reviewer independently refetched that index and checked its records against
both local packages, their regular archive members and private copies:

| Package | Complete package SHA-256 | Extracted library SHA-256 |
| --- | --- | --- |
| `libgmp3c2_4.3.2+dfsg-1ubuntu1_amd64.deb` | `78bf52ac9364cff0c1f100659303ce9c39645c0c3f29f65baaa691aea8630ddd` | `f9144a4924e1ba0f16477769447a8d4b56a060e8353378cc11bced599fa3c27f` |
| `libmpfr4_3.0.0-2_amd64.deb` | `f7ac357c7a4ea2edc8f30ca97ae4519bace928d16af2eeb663932a027ecfcb0d` | `54f3a045f2ebe74649bf4403a287a52722bbba139198674fe5a6597846aaa4ee` |

The GMP/MPFR regular files are393,088/352,600 bytes. SONAME-named regular copies
contain the identical legacy bytes, not links to incompatible modern libraries.
Their static dependencies close over each other and the pinned host libc/loader.
No package scripts or system installation are involved. This pins the declared
runtime files, not the entire host OS or a reproducible original package build.

Before first execution the reviewer approved exactly two help-only invocations
from `config/psp-gcc435-candidate.json`,2,583 bytes, SHA-256
`78c15bdcec0a105fbc92698b7d81257f1bc990ca226fc985ceea9c9241cb22de`,
using ignored driver `check_candidate_help.py`,4,743 bytes, SHA-256
`fc385f83f9cb3f6b89b0e029d548af7d4bc7762130712009a9eaa9a35563d065`.
It checks exact archive/frontend/runtime pins and interpreter binding,
rejects LD_PRELOAD/LD_AUDIT, sets the private LD_LIBRARY_PATH and LC_ALL=C,
uses no source/stdin and imposes twenty-second process-group bounds. Both
review approvals and the help freeze must precede those calls. Fixture builds
remain subject to their separate pre-compilation review/freeze.

## Candidate help outcome

Both reviews preceded the help freeze at
`2026-10-31T08:02:48.843015+00:00`. Its732-byte record has SHA-256
`010fda353b1a869a541668d0cad2ceaf0b3a89efdd4d840d360305f9231ec04f`.
Both predeclared invocations complete with exit0 and no timeout. The185-byte
version text is written to stderr and identifies GNU C++4.3.5(psp), built by
GNU C4.4.5 with GMP4.3.2 and MPFR3.0.0-p3; this metadata is not a diagnostic
compilation error. Target help produces2,755 bytes on stdout and empty stderr.

The reviewer rehashed every raw help stream, matched observations to the report
and rechecked both frozen input records. The retained1,436-byte
`evidence/bucket-03z/candidate-help.json` has SHA-256
`180a9dc5e29c734a4bf3046bf6d0313e61b86605938d1ced340459db2704dd2b`.
Tool/runtime pins are recorded unchanged. This establishes a runnable identified
publisher frontend under the private runtime, not the game's original compiler,
source provenance of every vendor patch, or fixture/object neutrality. No source
was compiled at this help-only stage.

## Separate fixture-stage approval

The reviewer subsequently approved `config/gcc435-fixtures.json`,2,554 bytes,
SHA-256 `6081aff692157325ccbff159b6144162a359203e4b6b773e30ebf4ca43c0786d`,
and ignored driver `run_gcc435_fixtures.py`,8,747 bytes, SHA-256
`d2b54c55e317d2c0f4d126eeb550f6abb57b09d8a05eb0cf493f6a0c4b83433c`.
This approval covers exactly eight invented fixture compilations after both
reviews and a separate freeze: unchanged static-object/grouped-address sources,
old/new GNU frontends and two fresh trials. Both old whole-object controls must
reproduce before either new-frontend case in each trial.

The existing capture pipeline supplies the same native staging, complete raw
assembly and diagnostic assembler. Common target flags and O2 remain identical;
only frontend identity and the necessary private library environment differ.
The environment context restores values in finally and does not alter a user's
shell/system environment. Global snapshots cover all earlier objects and
assembly copies, with input/runtime pins rechecked per case. Symbol/section/
relocation inspection and decoder uncertainty remain separate from complete
byte preservation. This stage compares no original code and creates no new
source hypothesis or matching attempt.

## Fixture outcome: retained failure, comparison incomplete

The exact fixture freeze preceded execution at
`2026-10-31T08:10:40.342238+00:00`. Both fresh trials stop at the same reviewed
prerequisite; `fixture-trial-1-failure.json` and `fixture-trial-2-failure.json`
report **ABORTED_UNSCORED**. No successful full comparison report is published.

The reviewer independently checked both retained directories,
`build/gcc435-fixtures-1ngni_g5` and `build/gcc435-fixtures-4x_iby11`, their
complete objects/assembly, stage diagnostics and frozen inputs. Each contains
exactly the old static-object fixture, old grouped-address fixture and new
static-object fixture. Both old whole objects reproduce their historical
controls exactly. The new grouped-address case is never invoked because the
preceding new static-object case fails validation. Thus six of the eight
declared fixture compilations occurred; no absent case counts as completed.

The new compiler returns0 with empty stdout/stderr and emits16,510 bytes of
assembly, SHA-256
`aae4577da7c1b830e0baa52315325c257f05483097845a09075c8d253fca866d`.
The unchanged modern diagnostic assembler also returns0, but reports:
`.gnu_attribute 4,2 requires singlefloat`. Its raw input explicitly contains
that attribute. The previously captured target help already records single-
float enabled and double-float disabled for this compiler. Those observations
identify a compiler/assembler ABI-consistency issue; they do not authorize
ignoring the warning or changing a function's options.

The existing strict stage check treats that warning as failure, retains all
partial artifacts and stops. Both partial objects are6,056 bytes, SHA-256
`890b3018129707bde119a706fc6540cd12d4dff683f32bf65aca6eee1f52e41d`.
They and the raw assembly reproduce completely in the second fresh trial, but
remain **unscored/unvalidated comparison outputs**. Byte preservation does not
waive the failed prerequisite. No producer-convention or original-target
conclusion is drawn from those partial objects here.

Candidate provisioning and bounded version/help validation are complete. The
planned two-fixture comparison is incomplete and failed closed under the exact
frozen pipeline. No source or flag was revised, no fallback compiler/build was
substituted, and every earlier profile remains intact. Any assembler ABI
investigation needs a separately declared review/freeze; this document approves
no additional invocation. PARKED remains one, plain attempts three, retained
commented shapes one, register pins/empty asm zero, credited matches/linked
source zero. This helper performed static/public-text/artifact review only,
never candidate/compiler/game execution.
