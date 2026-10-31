> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3Z independent validation

## Isolation and provenance criteria

This bucket selects one later PSP GNU 4.3.5 candidate for invented-fixture
comparison. It does not change original sources, per-function flags, parking,
matching credit or the historical toolchain status. The existing static-object
and grouped-address C++ fixtures are the only planned inputs, with the exact
old GNU C++/O2/common/modern-assembler settings and mandatory old whole-object
controls in two fresh trials. Any unsupported dependency/option or failed build
stays explicit; another compiler or changed target profile is not a fallback.

Before any new compiler execution, the review requires the publisher archive or
published source/PSP-patch closure, isolated resolved extraction/build/output
paths, the frontend format/interpreter and complete runtime dependencies. Static
ELF reads precede execution; ldd is avoided for this initial inspection because
it can invoke a target loader. No system installation, maintainer script or
vendor-wide toolchain script is authorized by extraction. Existing toolchains
and host-library paths must not be overwritten or repaired with incompatible
soname links.

If the verified publisher binary is unusable, the approved fallback is one
frontend-only build from pinned published source/patches, with reviewed host
configuration and a fifty-minute bound within the remaining approval window.
No helper launches or downloads software. A new source build would be labeled
as such, not relabeled as an authentic historical publisher binary. Fixture
source/profile/driver freezing remains a second prerequisite after availability.

## Acquisition readback

The recorded SourceForge 0.10.0 Linux publisher archive is
`minpspw_0.10.0-1ubuntu0_amd64.deb`, with expected SHA-256
`0caefe824ace40687032c492acbcc6e894c5ed2acb881d20cab7294fea134055`.
The archive release must be called 0.10.0, distinct from the initial 0.10.1 lead;
actual GCC 4.3.5 identity still requires member/static evidence. The first three
recorded download attempts return HTTP 403 and acquisition.json records verified
false and no archive/candidate execution. No compiler availability or extraction
success is inferred from the publisher page alone.

## Concrete candidate review before execution

The primary subsequently downloads the exact publisher archive through WSL curl.
`acquisition-wsl.json` records 80,695,848 bytes and the expected SHA-256 above.
Independent read-only ar/tar parsing verifies Debian archive version 2.0 and the
complete archive hash, then compares both selected regular members with their
isolated extracted files. No archive/control script is executed or system file
installed. The only extracted compiler members are cc1plus and cc1 under the
private `toolchains/minpsp-0.10.0-amd64/opt/pspsdk/libexec/gcc/psp/4.3.5` tree.

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| cc1plus | 6,745,856 | `66324e6459dd5098606480fc5a442dd02afadbdba52a94d8372609a952c5baf3` |
| cc1 | 6,102,752 | `e29857596843952300e21f45728f5193189cd982badc824edb323ac89bd7de42` |

Both are independently parsed as little-endian ELF64 x86-64 executables, contain
static 4.3.5/psp strings and request `/lib64/ld-linux-x86-64.so.2`. Raw dynamic
records require libmpfr.so.4, libgmp.so.3 and libc.so.6. These are host dependencies,
not PSP target libraries. They must be resolved and pinned before the first
candidate execution; no incompatible modern-library soname alias is accepted.
No source-build fallback has been used at this point.

The private dependency closure is subsequently checked before first execution.
The downloaded official Ubuntu Maverick Packages.gz is 1,909,018 bytes,
SHA-256 `4ff91eab6a4e820fb8f90244e3830f4070590e5ec5151fb708dcc19987c7e2c5`.
Independent gzip/paragraph parsing verifies both selected package records, then
all .deb sizes and SHA-256/SHA-1/MD5 values against that index. Selected regular
ar/tar library members equal the private extracted files:

| Private library member | Bytes | SHA-256 |
| --- | ---: | --- |
| libgmp.so.3.5.2 | 393,088 | `f9144a4924e1ba0f16477769447a8d4b56a060e8353378cc11bced599fa3c27f` |
| libmpfr.so.4.0.0 | 352,600 | `54f3a045f2ebe74649bf4403a287a52722bbba139198674fe5a6597846aaa4ee` |

The unversioned private SONAME filenames are byte-identical regular copies of
these original members, not symlinks to a modern substitute. Raw dynamic-table
inspection confirms internal SONAMEs libgmp.so.3 and libmpfr.so.4, no private
RPATH/RUNPATH, GMP requiring libc and MPFR requiring GMP/libc. The current pinned
host libc requires only the pinned loader; that loader has no further DT_NEEDED
entry. The original interpreter path resolves to that exact host-loader pin.
Neither dpkg/apt nor package maintainer scripts are used.

The helper approves the exact first-execution config, 2,583 bytes, SHA-256
`78c15bdcec0a105fbc92698b7d81257f1bc990ca226fc985ceea9c9241cb22de`,
and the 4,743-byte help driver, SHA-256
`fc385f83f9cb3f6b89b0e029d548af7d4bc7762130712009a9eaa9a35563d065`.
Only --version and --help=target are permitted at this stage, with 20-second
process-group limits, private LD_LIBRARY_PATH, LC_ALL=C, loader-injection
variables rejected, and complete before/after pins. A separate fixture freeze
is still required. No helper downloads or launches the new binaries.

This is the verified publisher binary release 0.10.0, not a source build or proof
that its exact patch revision equals the later dated recipe snapshot. Neither
publication timing nor version identity establishes Capcom's historical tools.

The first-execution help freeze is 732 bytes, SHA-256
`010fda353b1a869a541668d0cad2ceaf0b3a89efdd4d840d360305f9231ec04f`.
Both final approvals and exact two input pins precede the two commands. Read-only
independent readback verifies their complete streams, commands, normal exits,
no timeouts and unchanged candidate/private/host/frozen identities.

The 1,436-byte help result has SHA-256
`180a9dc5e29c734a4bf3046bf6d0313e61b86605938d1ced340459db2704dd2b`.
The 185-byte informational version stderr states GNU C++ 4.3.5 (psp), compiled by
host GNU C 4.4.5, with GMP 4.3.2 and MPFR 3.0.0-p3. The host compiler build version
is separate from the PSP frontend version. Target-help emits 2,755 stdout bytes
and empty stderr. No source file/object is involved and no candidate is executed
by the helper. Availability/version/target help is verified, not a historical
compiler lock. No fallback source build is needed.

## Frozen fixture and output audit

The helper separately approves the exact fixture stage before any of its eight
compilations:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| `config/gcc435-fixtures.json` | 2,554 | `6081aff692157325ccbff159b6144162a359203e4b6b773e30ebf4ca43c0786d` |
| Fixed fixture driver | 8,747 | `d2b54c55e317d2c0f4d126eeb550f6abb57b09d8a05eb0cf493f6a0c4b83433c` |
| Existing static C++ source | 1,699 | `fb88cb5c8f7be2b0f7a4cb83ac994789c3f88e3a2b49726e81d476a437426423` |
| Existing grouped-address source | 1,200 | `04662faba3e8e68506928bb2d2623d25cf5e6a93f8f9fb1bde3e3dd223908094` |

Actual nested verification proves the later pipeline differs only in the selected
frontend/support identity; common target flags, O2, assembler/flags, source
basenames and the reviewed native capture API remain unchanged. Both historical
old-GNU whole objects must reproduce before the new frontend is called in each
trial. The new private library/locale context covers both capture children and
is restored before decoding or the next case; this is recorded explicitly.

Pure/mocked controls verify the environment allowlist and finally-restoration,
injected frontend-byte drift rejection, four-case old-before-new order, old
control mismatch blocking all new cases, a new capture exception restoring the
environment with no success report, and later output drift preventing publication.
No actual frontend/assembler/decoder is launched for these controls. The existing
capture snapshot checks protect all prior objects and assembly copies across
cases, and unsupported parse/decoder outcomes remain explicit.

### Preserved initial warning-gate abort

The initial fixture freeze is 1,088 bytes, SHA-256
`4a3b34211562f9c1e1f3a3ec3445e6fbfea758c3cf77a2c33cf90fe535535851`.
In `build/gcc435-fixtures-4x_iby11`, both old whole-object controls reproduce:
static C++ 6,312 bytes and grouped address 1,204 bytes (complete identities below).
Their compiler/assembler returns and diagnostics are clean.

The new static-C++ frontend then exits 0 without diagnostics and emits 16,510
assembly bytes, SHA-256
`aae4577da7c1b830e0baa52315325c257f05483097845a09075c8d253fca866d`.
The unchanged assembler exits 0 but warns that .gnu_attribute 4,2 requires
singlefloat. It creates a retained 6,056-byte object, SHA-256
`890b3018129707bde119a706fc6540cd12d4dff683f32bf65aca6eee1f52e41d`.
The frozen strict warning gate correctly rejects this artifact and publishes
ABORTED_UNSCORED rather than a successful comparison. The fourth case was not
attempted in that initial invocation and no normal fixture-trial-1 report exists.
Independent readback verifies all those raw files and stage records.

The predeclared target help already reports hard/single float enabled and double
float disabled. That supports recording an assembler/profile ABI metadata
compatibility issue, not calling the frontend unavailable or altering the source.
No flag or .gnu_attribute directive is removed/changed and the warning is not
ignored. The second frozen trial repeats the same fail-closed outcome in
`build/gcc435-fixtures-1ngni_g5`; the first root is retained unchanged. Each
198-byte failure report has SHA-256
`85b1ae47db9a27809ad3cb99e6c2cff5b4f53e0957793f42e11ea35331c29237`.
No continuation, criterion change or warning suppression occurs within 3Z.

Independent final readback verifies all six actual frontend compilations: four
old controls and two new static-C++ attempts. The two new grouped-address cases
are **NOT RUN** because each trial stops at its earlier assembler-warning gate.
Thus the planned eight-case fixture validation is not complete or successful.
The exact counts are reported instead of crediting uninvoked cases.

| Repeated case | Complete raw object bytes / SHA-256 | Verbatim assembly bytes / SHA-256 |
| --- | --- | --- |
| Old static C++ control | 6,312 / `a8848c362e49c88129ef5373529cfbe9c86c6233d220bcd6d27928c7de3017d9` | 21,103 / `5aebeb1ab5a4a2bcd5aafa6b014002eb618b8371cf27b2c0467e9ffc9bd70482` |
| Old grouped control | 1,204 / `22690e399773b59c25a0b3966312c5f6465c9d96690d5a91dba274b78ee80523` | 995 / `9c1aabe61e5c0de8e02071f3759d294a1936833266514bd964d17281512a1078` |
| New static C++, REJECTED | 6,056 / `890b3018129707bde119a706fc6540cd12d4dff683f32bf65aca6eee1f52e41d` | 16,510 / `aae4577da7c1b830e0baa52315325c257f05483097845a09075c8d253fca866d` |

Each raw object and assembly pair is byte-identical across the two roots. Both
old objects also equal their entire historical controls. Every stage's exact
compiler/assembler argv, output hashes, returns and diagnostics reproduce.
Independent bounded symbol/relocation inspection finds respectively 16/1/14
function records, 50/12/56 symbol records and 108/1/101 relocation records in
the three case types. This describes retained bytes, not acceptance of the
warning-bearing new configuration; no relocation is applied or masked.

Final source/frontend/archive/private-library/host-loader/producer/parked pins
all verify, including the original fixture freeze. No normal fixture-trial report
or new grouped output directory appears. No helper executes a compiler, assembler,
loader, object or game; all new-software invocations are the separately approved
primary help/fixture commands.

Provisioning and version/target-help availability succeeded, but the fixed
fixture pipeline **failed validation and remains unscored**. No global or
per-function option is silently added, no assembly attribute changed, no warning
ignored, and no replacement compiler/source build is attempted. Any assembler
ABI investigation belongs to a new reviewed bucket. The last full WSL tooling
suite remains 340 passes from 3U. The initializer remains PARKED and all source,
trick, linking, runtime and match-credit counters stay unchanged.
