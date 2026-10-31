> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Local decomp.me source review — Bucket 3N

Reviewed upstream source commit
[`cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7`](https://github.com/decompme/decomp.me/tree/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7).
This combines read-only source/configuration review with the final bounded
running-instance audit below. The reviewer did not install dependencies, start
services or invoke a compiler. Primary-owned installation and invented-fixture
results belong in the bucket checkpoint. No game source or target bytes are
required for setup; browser visual QA and a full browser network trace were
not performed by this reviewer.

## Bindings and data flow

The upstream development compose publishes PostgreSQL 5432, cromper proxy 8888,
backend 8000 and debugger 5678, frontend 8080 and nginx 80 without host-IP
restrictions. These are not localhost-only declarations. A local configuration
should publish only the required browser entry on an explicit loopback address
and leave dependencies internal. Inspect the fully merged compose configuration:
adding a new published binding must not retain an original unrestricted entry.
Container-internal servers listening on all container interfaces are distinct
from ports published on the host.
[Development compose](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/docker-compose.yaml).

Browser egress is a separate concern. Root `.env` defaults `OBJDIFF_BASE` to
`https://diff.decomp.me/`. `ObjdiffPanel` loads that URL in an iframe and transfers
both target and compiled object ArrayBuffers, compiler output and the diff
label to it using `postMessage`. Therefore an otherwise local instance can send
private object bytes to an external page. Before private use, configure a
verified local objdiff endpoint or an explicitly unavailable local route; do not
retain the remote default or use an empty value that resolves unpredictably.
This bucket needs only an invented fixture and does not require hosting objdiff.
[Environment](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/.env),
[iframe and object transfer](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/frontend/src/components/Diff/ObjdiffPanel.tsx#L113-L199).

Keep backend/cromper `SENTRY_DSN` and frontend `NEXT_PUBLIC_SENTRY_DSN` empty.
Cromper and frontend Sentry initialization are conditional, but the frontend
production Dockerfile supplies a nonempty default DSN and remote objdiff URL at
build time. A production build needs explicit empty/local build arguments,
not only runtime overrides. The frontend package disables Next telemetry in
`postinstall`; an explicit local telemetry setting is still reviewable. Blank
GitHub credentials avoid accidentally configuring an external login service.
Package/image downloads during installation are not uploads of game data, and
are not evidence that later browser egress is absent.
[Frontend build defaults](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/frontend/Dockerfile#L27-L40),
[frontend Sentry](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/frontend/sentry.server.config.ts),
[cromper Sentry](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/cromper/main.py#L27-L41).

Use local browser/API URLs consistently. Compose supplies `/api` to the browser
and internal service URLs to server-side requests. If using a nonstandard
browser port, review absolute media URLs as well. `ALLOWED_HOSTS` is not a
firewall or authentication control: the development backend enables broad CORS
and disables its normal CSRF middleware. This strengthens the reason to avoid
exposing the development services beyond the approved local boundary.
[Backend settings](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/backend/decompme/settings.py).

## Current compiler service and minimal PSP provisioning

The compiler service is **cromper**, accessed through `cromper-proxy`; the
backend persists scratches and calls it. Old instructions in `docs/COMPILER.md`
still name `backend/compilers` and `backend/coreapp/compilers.py`. The actual
definitions, compiler storage and downloader are under `cromper/` at this pin.
Backend-only `ENABLE_PSP_SUPPORT` does not install a compiler there.
[Compiler definitions](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/cromper/compilers.py),
[historical instructions](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/docs/COMPILER.md).

The downloader supports `--platforms` and `--compilers` filters. Without an
explicit platform filter, platforms default enabled unless their
`ENABLE_<PLATFORM>_SUPPORT` value is `NO`. Those variables select downloads;
runtime compiler availability instead checks installed directories. For this
bounded setup, an explicit selection of `psp / mwccpsp_3.0.1_219` plus
`common / wibo_dlls` is preferable to downloading every compiler. Existing
verified local tool files can be provisioned separately if their required
layout and identity are preserved. A visible compiler entry is not proof that
its executable, DLLs or command work.
[Downloader selection](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/compilers/download.py#L277-L355),
[Linux inventory](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/compilers/compilers.linux.yaml),
[directory availability](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/cromper/compilers.py#L35-L90).

`CompilerWrapper` supplies `WIBO_PATH` from
`<compiler-base>/common/wibo_dlls`. The PSP MW command uses wibo and adds `-c`;
it does not itself impose our frozen `-nostdinc -lang c++ -O2` diagnostic flags.
The invented fixture must record the actual selected compiler, submitted flags,
effective command, complete output and tool identities. This does not change
the earlier source/profile experiments. PSP assembly/diff uses patched
`mips-ps2-decompals` tools with its own platform flags, so UI assembly output
is not automatically our selected assembler or matching authority.
[Compiler wrapper](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/cromper/wrappers/compiler_wrapper.py#L148-L163),
[PSP platform tools](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/cromper/platforms.py#L149-L159).

## Dependency and host traps

- Cromper's development entrypoint directly executes
  `/cromper/.venv/bin/python`; its development image does not create that
  environment. A fresh checkout requires a separate dependency bootstrap.
  Backend starts with `uv sync`; frontend installs its frozen yarn lock on
  startup. Record the actual lockfiles/dependency outcomes rather than assuming
  the pinned source alone fixes every installed artifact.
  [Cromper entrypoint](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/docker_entrypoint.sh).
- Compose requests `/dev/kvm` unconditionally. If that device is absent, it can
  prevent service creation even though PSP219's declared command uses wibo.
  Keep any local configuration adjustment explicit. Nsjail is enabled by
  default; a working Docker daemon does not prove its namespace/mount operations
  work under this WSL host. A jail failure must be reported, not silently
  replaced by unjailed compilation.
  [Sandbox implementation](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/cromper/sandbox.py).
- Images use Ubuntu 26.04/Python 3.14, Node 24, PostgreSQL 17 and downloaded
  binutils/wibo/daze/nsjail components. Some artifacts have hashes; base image
  tags, package indexes and registry compiler tags are separate provenance
  inputs. Record resolved image digests and tool hashes. Source commit pinning
  does not imply byte-reproducible containers or equivalence to our standalone
  wibo executable.
  [Cromper image](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/Dockerfile).

## Persistence, stopping and checkpoint

Upstream compose bind-mounts `./postgres`, `./pgdump`, backend media/static,
compiler/library folders and development source trees. PostgreSQL holds scratch
state; media can hold uploaded objects. Treat both as private persistent data.
Stopping containers does not erase these host directories. Use the exact
recorded project name and compose files with `docker compose ... down` to stop
the instance; avoid deleting data or requesting volume removal as routine
shutdown. Ctrl+C stops foreground compose, while Ctrl+C during `logs -f` only
ends log-following for a detached stack.
[Storage declarations](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/docker-compose.yaml),
[upstream shutdown instructions](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/docs/DOCKER.md#L13-L30).

The checkpoint should distinguish installation, effective loopback bindings,
browser/network observations, compiler availability and one successful invented
compile. None establishes historical attribution, original-language recovery,
full-byte reconstruction or the mandatory source-participation/negative gate.
The private PSP v1.02 reference and all earlier compiler profiles remain fixed.

## Generated instance: independent pre-start review

Reviewed `/home/<user>/mhp3rd-tools/decompme-instance/compose.json`,
`nginx.conf` and `backend-start.sh` read-only before service startup. The
secret environment file was neither opened nor printed. This local deployment
uses four services and SQLite, so the upstream PostgreSQL storage description
above is a source reference rather than its actual database layout.

The generated configuration publishes only `127.0.0.1:8787` on nginx and marks
the Docker service network internal. Its mounts contain the workbench copy and
instance state, not the decompilation project or game image. The browser objdiff
URL is a local inert page. Nginx applies a same-origin CSP and rejects foreign
Host/Origin values; the visible DSN settings are empty and production build
arguments override the upstream public defaults. These declarations address
the identified exposure/egress paths; effective socket and browser behavior
still require the primary's running-instance validation.

One upstream build limitation remains explicit: `frontend/Dockerfile` does not
declare `ARG INTERNAL_CROMPER_BASE`, so passing that build argument does not
set it inside the builder. The generated runtime environment does supply
`http://cromper:8888`. Pinned `frontend/src/lib/api/request.ts` uses that private
environment variable for server-side compiler/platform/library requests; browser
requests fall back to the built `/api` URL. `/new` and `/platform` are declared
force-dynamic. Runtime SSR checks on those pages are therefore necessary in
addition to directly testing `/api/platform`. This source review found no
confirmed routing defect when the declared runtime variable is present, and
does not certify build/runtime environment behavior without those checks.

At the time of review, neither backend nor cromper had a `.venv` directory,
and `common/wibo_dlls` was absent. The state directory was uid/gid 1000 with
mode 0755. The Python environments need an explicit dependency-bootstrap phase
before the isolated runtime starts: backend `uv sync --locked` cannot fetch
missing dependencies over an internal-only network, and cromper does not sync
in its entrypoint. Whether this PSP compiler requires the common fallback DLL
directory must be established by the invented fixture rather than a catalogue
entry alone.

Finally, visible backend settings use `DEBUG=on` without a cookie override.
Upstream selects `SameSite=None` in that branch and defaults secure cookies
on. Verify actual local HTTP session behavior; setting only Secure=false while
retaining SameSite=None is not an adequate correction. If changed for this HTTP
instance, `DEBUG=off` plus `SESSION_COOKIE_SECURE=false` selects the source's
Lax branch. This is a deployment/session choice, not a compiler flag change.
No configuration was mutated and no service or compiler was run by the reviewer.

## Final generated configuration and observed runtime

The primary corrected startup and session configuration after the pre-start
review. Backend startup now uses the prebootstrapped environment directly,
migrates SQLite, collects static files and starts without dependency downloads.
`DEBUG=off` and `SESSION_COOKIE_SECURE=false` select the upstream Lax branch
for this HTTP instance. The initially internal-only network failed to create
a usable host publication; the retained negative observation is
`evidence/bucket-03n/internal-only-port-observation.json`. The final deployment
adds a noninternal gateway network **only to nginx**. The earlier statement
that every service has only an internal network is superseded by this explicit
layout, not silently treated as the successful configuration.

Independent read-only Docker inspection observed:

| Service | Published ports | Attached networks |
| --- | --- | --- |
| backend | none | internal default only |
| cromper | none | internal default only |
| frontend | none | internal default only |
| nginx | `127.0.0.1:8787` → TCP 80 | internal default and publishing gateway |

Docker reports the default network internal and the gateway noninternal.
Backend/frontend/cromper have no gateway in their inspected network settings;
nginx is deliberately dual-homed. This is effective network metadata, not a
claim that every container lacks an outbound route or a hostile-container
security proof. Effective mounts contain only the workbench source/state and
nginx configuration/static/media paths; no game or decompilation-project root
is mounted. The secret environment file was not opened or printed, and the
backend environment was never dumped wholesale.

Independent GET observations establish more than a health response:

- `/new` and `/platform` return 200 and their server-rendered HTML contains
  PlayStation Portable and the 219 compiler identifier. `/api/platform` also
  returns 200. The runtime `INTERNAL_CROMPER_BASE` works for those server routes
  despite the unused build argument documented above.
- The retained invented scratch's editor page returns 200. All 25 script URLs
  referenced by that response are local. Its served editor chunk
  `/_next/static/chunks/0r5lijlvvk851.js` contains `/objdiff-disabled/` and no
  `https://diff.decomp.me/` occurrence. The local disabled page returns inert
  explanatory HTML, and the observed responses include the reviewed CSP.
- Fresh GET requests carrying a foreign Origin or Host each return 403.
  Selected runtime fields confirm empty frontend/cromper Sentry DSNs, local
  objdiff, internal API routes, disabled frontend telemetry and the intended
  backend HTTP/session environment. These are response/asset/configuration
  observations, not a full browser egress capture or visual editor test.

The reviewer independently read both retained service objects from
`workbench-smoke/trial-ptzag59n` and both standalone comparison objects identified
by `direct-compiler-parity.json`. All four complete 624-byte files are identical,
SHA-256 `e623ca821a5ee6baed036c5d820cebdf43340950e659026ec0da0bffc1d93edc`.
No fixture was recompiled for this audit. The recorded container wibo differs
from the earlier standalone executable; this one complete-object parity result
does not prove universal runner equivalence or alter prior tool identities.

The initial lifecycle controller checked compose/keepalive but omitted the
contents of the privacy-critical mounted nginx/startup files. The primary added
`pinned_runtime_files` checks for both and `git diff --exit-code HEAD --` in
addition to the commit check. Independent readback confirms all four deployed
file hashes match `config/decompme-local.json` and tracked source has no diff.
This guards the reviewed files/tracked checkout; it is not an immutable
container-image or all-dependencies proof. The controller starts without builds
and its scoped keepalive uses a lock and stop marker rather than shutting down
the whole WSL distribution.

No remaining configuration defect was found in this bounded final review.
The later retained `evidence/bucket-03n/session-persistence.json` records
`PERSISTENCE_VERIFIED`: after scratch creation establishes a session cookie,
the invented scratch is claimable/editable, and its source and profile survive
the actual controller stop/start. Independent read-only review of that record
and `lifecycle-stop.log` / `lifecycle-start.log` confirms the reported sequence
includes container/network removal followed by recreation, rather than just
an HTTP reload. The cookie metadata is HttpOnly, SameSite=Lax and Secure=false,
consistent with the selected local HTTP settings. This is an audit of the
primary's retained API result, not a second session test by this reviewer.

The earlier failed assertion compared a pre-cookie ephemeral profile with the
post-create persistent profile. That comparison did not establish data loss or
an application defect; the successful post-cookie test is the relevant result.
Visual/browser automation remained unavailable because the browser-control
tool rejected the Firefox URL-policy operation. No visual QA, full browser
packet trace, matching-source upload, game execution, toolchain lock or
game-match credit belongs to these observations.
