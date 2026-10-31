> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3N independent method review

The user approved a private local decomp.me instance. This review reads upstream
commit `cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7`; it starts no service, installs
nothing and invokes no compiler. Only invented fixture source/targets belong in
the deployment smoke. No original game source, object, assembly, asset, image,
flag selection or existing experiment is changed or submitted by this review.
Deployment and actual smoke results remain the primary agent's responsibility.

## Anonymous local API and object retrieval

The pinned backend exposes these routes without a trailing slash. GitHub login
is not required to create or compile a scratch. Anonymous read/list access is
part of the application; privacy is an instance/deployment property here.

| Route | Purpose and evidence to retain |
| --- | --- |
| `GET /api/platform/psp` | Confirm enabled PSP metadata, not merely a rendered homepage. |
| `GET /api/compiler/psp/mwccpsp_3.0.1_219` | Confirm the intended installed compiler is advertised. Directory presence alone does not prove it runs. |
| `POST /api/scratch` | Create an invented scratch with explicit compiler, platform, source, context, flags, diff label and empty libraries; omit presets. Supply invented target assembly or a multipart `target_obj`. Creation itself performs a compilation. |
| `POST /api/scratch/{slug}/compile` | Compile a complete explicit request with `include_objects: true`. Decode `right_object` as the full compiled object and `left_object` as the target. |
| `GET /api/scratch/{slug}/compile` | Also returns both objects, but updates the stored score. Prefer POST for a controlled smoke. |
| `GET /api/scratch/{slug}/export` | ZIP includes `target.o` and, if recompilation succeeds, `current.o`. Export performs another compile unless `target_only=1`. |
| `/scratch/{slug}` | Frontend editor for the API-created invented scratch. |

The internal Cromper service also exposes `POST /compile`: fields are
`compiler_id`, `compiler_flags`, `code`, `context`, `function` and `libraries`;
the result carries base64 `elf_object`, `success` and diagnostic text. This is
an internal endpoint, not the Django `/api/compile` route. Public metadata
routes are proxied to Cromper by the default development Nginx configuration.
[Backend routes](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/backend/coreapp/urls.py),
[scratch actions](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/backend/coreapp/views/scratch.py),
[Cromper compile handler](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/cromper/handlers/compile.py).

For persistent anonymous editing, keep a session cookie and use a normal,
nonbot user agent. Creation returns a claim token; the claim action can attach
the scratch to that anonymous session, after which normal saving is available.
Missing user agents and several automation user agents receive ephemeral
profiles, which cannot claim ownership. Compilation does not require claiming.
The smoke should not visit GitHub authentication merely to work around a local
session issue. [Profile middleware](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/backend/coreapp/middleware.py).

## Explicit settings and direct object parity

The reviewed flow compiles the chosen compiler and flags; it does not search
optimization settings. UI automatic recompilation resubmits edited inputs.
However, choosing a compiler resets draft flags, and a preset can supply
different flags/libraries. Use an explicit request and inspect the returned
scratch settings. Backend filtering removes options such as `-c` because the
compiler template already provides it; this is distinct from optimizer tuning.
[Draft behavior](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/frontend/src/app/%28navfooter%29/new/NewScratchForm.state.ts),
[flag filtering](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/backend/coreapp/compiler_utils.py).

Direct parity is possible because the API returns the entire object without
extracting the selected function. Its generated compiler input differs from
the editor text: Cromper normalizes CRLF to LF, combines context and source,
inserts `#line` directives naming `ctx.c` and `src.c`, and adds newlines. It also
creates the referenced files for Metrowerks diagnostics. For exact object
parity, retain and reproduce that generated input, language extension, command,
compiler/runner bytes and environment. Comparing an ordinary compile of the
original editor text alone would confound wrapper changes with compiler changes.
The PSP Metrowerks command supplies `-c`, the user flags and output/input paths;
it does not select O2 or `-nostdinc` automatically.
[Compiler wrapper](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/cromper/wrappers/compiler_wrapper.py),
[PSP compiler declarations](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/cromper/compilers.py).

Compare raw full-object size/SHA-256 first, then independently validate exact
function symbols, complete extents, bytes and relocations. If whole-object
parity fails, retain that failure and separately report any body equality;
do not normalize metadata or trim bytes to manufacture equality. A zero diff
score or successful invented self-comparison is not our byte-match gate,
source participation proof, compiler attribution or game-match credit.

## Meaningful deployment smoke and failure visibility

Before claiming an end-to-end result, retain these actual observations:

1. The deployed commit and local configuration/patch identities, container image
   identities, health response bodies and all listening/published addresses.
2. One declared invented fixture request, exact source/context/settings and
   target identity; a returned scratch that opens in the local editor.
3. An explicit successful compile with nonempty valid decoded object bytes,
   expected complete symbol, diagnostics and repeated object/body comparisons.
4. A deliberate syntax-error version of only that invented fixture returning
   visible failure and diagnostics, without reusing the prior successful object.
5. The direct parity result or its specific limitation, preserving both raw
   objects and commands. No game bytes should be mounted or submitted.

Creation returning HTTP 201 is insufficient: initial compile/score errors can
leave a created scratch. Compile responses can be HTTP 200 with `success: false`;
warnings can accompany an object. Inspect success, diagnostics and object
validity explicitly. Upstream also filters some driver diagnostic lines, so API
messages are not necessarily a complete raw process log.

The development proxy can convert upstream 502/503/504 responses into HTTP 200
with `{}` and `X-Backend-Down: true`. Health/smoke checks must validate expected
JSON and this header, rather than treating HTTP status alone as availability.
[Development proxy](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/nginx/development/default.conf).

## Privacy boundary to verify in the actual deployment

The supplied Compose file publishes ports 80, 5432, 8000, 5678, 8080 and 8888
without loopback addresses. Override every necessary publication to loopback
and remove unnecessary publications; internal service DNS does not require a
host port. The application's own notes about browsing localhost are not proof
of localhost-only binding. [Upstream Compose](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/docker-compose.yaml).

Pinned development settings allow all CORS origins with credentials and disable
CSRF checks. Verify a documented local override or proxy origin policy that
allows only the intended local UI origins; loopback binding alone does not
provide that browser-origin restriction. Confirm frontend public/internal API
bases point only to the local/container services, leave GitHub credentials
unused, and disable Sentry DSNs across services. Preserve logs locally and mount
only the fixture/tool inputs required for this smoke, not the game directory.
[Backend settings](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/backend/decompme/settings.py),
[frontend request routing](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/frontend/src/lib/api/request.ts),
[Cromper telemetry configuration](https://github.com/decompme/decomp.me/blob/cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7/cromper/cromper/config.py).

At the initial source-review stage no deployment, privacy, fixture-compilation
or object-parity check had been performed. The later retained evidence is
reviewed separately below; the method itself does not establish those results.

## Fixed local smoke client prepared during advance approval

`scripts/check_decompme_local.py` implements the declared smoke without starting
services or invoking Docker or a compiler directly. Run it only against the
approved ready local service:

```text
python scripts/check_decompme_local.py
```

The default is `http://127.0.0.1:8787`; the optional base URL must use that
literal loopback host, HTTP and an explicit port, without userinfo, path or
query. The client ignores proxy environment settings, sends no cookies or
authentication, rejects redirects outside its exact origin and rejects all POST
redirects. It has no argument accepting source files, compiler flags, presets,
libraries, game objects or target bytes. Its fixed natural C function returns
the unsigned sum of two arguments. The invented assembly uses the pinned PSP
`glabel`/`endlabel` prelude interface and a complete `addu`/`jr`/NOP body.

Each run creates a fresh `trial-*` directory below
`evidence/bucket-03n/workbench-smoke`. It retains sanitized requests/responses,
page responses, both returned objects from each compile, exact wrapper files
`code.c`, `ctx.c` and `src.c`, the plain fixture and target assembly, and a
success or failure report. Claim tokens and cookie/credential fields are
redacted; response cookies are not retained. The report explicitly leaves
direct compiler parity unperformed for the primary's separate comparison.

The client requires actual new-page SSR with PSP metadata, concrete platform
and compiler responses, a local default/connect CSP, hostile Origin and Host
403 controls, the created anonymous scratch/editor, and two explicit successful
compilations under `-nostdinc -lang c -O2`. It checks complete ELF/function
metadata using the existing strict fixture inspector, rejects code relocations
or extra/missing functions, validates the entire invented assembled body and
requires repeated whole-object identity. Displayed diff scores are recorded
separately from exact function bytes. The deliberate syntax error must show
compiler diagnostics and no retained compiled object; an unavailable service
or timeout is not accepted as the syntax-error control.

The helper verified Python syntax/help and pure URL, redirect, redaction and
CSP guards without network requests. No local service, compiler or game was
accessed by those checks. Actual end-to-end results remain pending the primary's
run against the ready services; these method checks add no full-game gate or
matching credit.

## Primary preliminary runs and canonical fixture boundary

The primary retained two preliminary failed runs. `trial-s1hwg3nj` cannot
connect because the WSL-hosted service has stopped; its report correctly records
connection refusal. After the primary keeps that runtime alive,
`trial-f_002ht0` passes SSR, metadata, CSP and hostile Origin/Host controls and
receives HTTP 201 from scratch creation. It then correctly fails the exact
source-echo check. No later compile/repeat/syntax-error checks are credited to
either preliminary run.

Read-only comparison of `06-create.body.json` identifies the precise boundary:
the returned source equals the original fixed fixture without its last LF;
compiler, flags, context, libraries and preset are otherwise unchanged. At the
pinned application commit, `ScratchCreateSerializer.source_code` uses the
ordinary DRF `CharField` whitespace behavior, whereas the explicit compilation
serializer and saved-scratch serializer set `trim_whitespace=False`. Creation
and subsequent explicit compilation therefore have different text boundaries.

Before successful end-to-end validation, the smoke's fixed invented `SOURCE`
literal was changed once to that exact canonical 146-byte value, with no final
LF. The strict equality check remains unchanged: no generic stripping,
normalization or masking of returned source was introduced. The arithmetic,
flags, target and all game source/profiles remain unchanged. Retained failed
trials are preserved. The wrapper files for the next run are computed directly
from the same exact source submitted for explicit compilation:

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Fixed source literal | 146 | `9967dea7001c51f79549bbb15e58eb81f2058f2be21d842805139fb8d45e9820` |
| `code.c` | 180 | `bd1c2c6efcb680c7a156c61467027c75b333c5945f5fa3e2bc9c50ab93507953` |
| `src.c` | 147 | `6c02f3a36728be1f0722331fbf87eb4b6a386a0e3ed31eea3ef699b043c5eaa1` |
| `ctx.c` | 1 | `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b` |

The helper verifies the canonical source against the retained response and
recomputes those wrapper bytes without contacting the service or compiling the
fixture. The subsequent successful run and direct-parity artifacts supply the
separate evidence reviewed below.

## Successful local smoke and independent artifact audit

The primary's `trial-ptzag59n/report.json` records
`LOCAL_WORKBENCH_SMOKE_COMPLETE`. It is 9316 bytes, SHA-256
`17b55a4183985404ec9b05fb3105d3b1c9af0fd07c1253ef2a6c87cfe1761c4d`.
The helper independently reads all ten sanitized request/response pairs, both
successful API compilation payloads and all six retained ELF files, without
making a service request, running Docker or recompiling anything.

The evidence verifies new-scratch and editor SSR, PSP/compiler response shapes,
the exact canonical source and explicit flags, no preset/libraries, local CSP,
and both hostile Origin/Host 403 responses. The report's `connect-src` and
`default-src` are `'self'`. Development script policy still permits inline/eval
and wasm evaluation; this is recorded configuration, not a production-hardening
claim. Requests stay on `http://127.0.0.1:8787`; response cookie headers are not
retained and the creation token is redacted. The retained JSON bodies are
formatted/sanitized evidence: their original-wire digest fields cannot all be
recomputed from those transformed files and are not represented as independently
verified raw HTTP streams.

Both successful compile responses contain actual complete ELF objects. Decoded
base64 bytes equal the retained object files, and the strict inspector's full
metadata reproduces the report. Target objects are 968 bytes, SHA-256
`5c08484ddee8c71bb89cd3284cff88ceddda5309990c4e7e4945c1a346fc36b1`.
Compiler objects are 624 bytes, SHA-256
`e623ca821a5ee6baed036c5d820cebdf43340950e659026ec0da0bffc1d93edc`.
Each corresponding whole object repeats exactly. Target and compiler objects
have different metadata and are not claimed byte-identical to one another.

Each has exactly one complete `workbench_sum` function, sized **12 bytes**, with
bytes `211085000800e00300000000` (the complete invented `addu`/`jr`/NOP body),
SHA-256 `6f03fb02b642d008fb614cf7b3091b03ee67edd4883bd23b1d5fe4a0ed5bfa69`.
The symbol extent and complete executable section are checked; no prefix or
padding was trimmed. Neither object contains an unresolved code relocation.
The application's displayed score zero agrees with the independently compared
function bytes, but does not supply the proof by itself.

The negative response is an actual Metrowerks diagnostic naming `src.c` and
`code.c`, showing the malformed addition and **"expression syntax error"**.
It is not a sandbox, timeout or unavailable-service error. `success` is false
and `right_object` is empty; the unchanged `left_object` is the invented target,
not a stale compiled result. The client's negative check therefore tests a real
source failure after the successful compiles.

## Direct parity and its limits

The helper independently reads `direct-compiler-parity.json` and both fresh
direct directories, `build/decompme-parity-cr53zwi_` and
`build/decompme-parity-25d0e80o`. Their `code.c`, `src.c` and `ctx.c` match the
saved service-wrapper files exactly. Both commands use the unchanged standalone
MW219 compiler and original pinned runner with
`-c -nostdinc -lang c -O2 -o object.o code.c`; both have empty stdout/stderr and
recorded return code zero. Both complete 624-byte outputs equal both service
compiler outputs byte for byte. Thus **all four compiled whole objects agree**
for this single invented fixture, including metadata.

`service-tool-identities.json` records a service wibo of 7256696 bytes, SHA-256
`02dac824064f86d03a869e3137071addd708c9342b618d241f4a76e2c0cb8f42`.
The original standalone runner remains 7256672 bytes, SHA-256
`13f86a2d618f0dbe67179d349625345eabf9b46450295cb4c904e49f6aff85af`.
The service compiler hash equals the original compiler hash. The helper checks
the original tools directly and reads the primary's service identity capture;
it does not query the running container. Different runner binaries mean the
observed parity is limited to this fixture. It is not general runner neutrality
or proof that the service reproduces every original project experiment.

Read-only hash checks also confirm the original fourteen-probe source, archive
initializer candidate and compiler-family/archive experiment profiles remain
unchanged. No game code or image was submitted, linked or executed. This result
validates a local workbench workflow; matching progress stays zero. Browser
cookie/profile persistence, interactive editing and lifecycle/storage validation
are separate checks for the primary and are not inferred from SSR or API smoke.

For that browser check, use its ordinary user agent and retain its session
cookie: create an invented scratch, claim its token through
`POST /api/scratch/{slug}/claim`, then verify a stable profile from
`GET /api/user`, matching scratch owner and a saved edit across reload. A
cookie-free `/api/user` deliberately returns an ephemeral profile. Actual
SameSite/Secure attributes must permit the local HTTP origin; source defaults
alone do not establish that browser cookies persist. Do not retain the cookie
or claim token in the review report.

## Session persistence and lifecycle integration audit

The primary subsequently records `PERSISTENCE_VERIFIED` in
`evidence/bucket-03n/session-persistence.json`. It claims an invented scratch,
checks its persistent owner/profile, performs an actual service down/up and
checks that the edited name, source and owner and the same cookie profile
survive. Cookie metadata is HttpOnly, SameSite=Lax and Secure=false for the
local HTTP origin; no cookie value or claim token is retained. Its earlier
probe incorrectly compared the initial cookie-free ephemeral profile with the
post-create persistent profile and stopped. That discarded assertion does not
establish application state loss; the corrected baseline is recorded explicitly.

The helper independently reads that summary and the retained lifecycle logs.
The stop log removes all four containers and both networks; the start log
recreates the runtime, with Cromper healthy before the backend and gateway start.
The helper also opens only the persistent SQLite file in read-only mode and
confirms the reported invented scratch currently has an owner and its canonical
source SHA-256 remains
`9967dea7001c51f79549bbb15e58eb81f2058f2be21d842805139fb8d45e9820`.
The same-session before/after observation is attributed to the primary's test;
the helper does not recover or replay private cookies to repeat it.

Read-only lifecycle review confirms identity validation precedes every action
in `scripts/decompme_local.py`. The retained controls reject four deliberately
wrong expected hashes for Compose, the WSL keeper, Nginx configuration and
backend startup configuration, while the positive validation passes. No live
configuration was changed for those negative controls. The helper recomputes
all four current file hashes, checks the configured internal default network,
confirms only Nginx joins the publishing network and verifies that only Nginx
publishes `127.0.0.1:8787:80`. No lifecycle command or HTTP request is issued by
this independent readback.

The browser-control tool refused interaction because its URL policy enforcement
does not support the active Firefox. No further browser automation was attempted.
The retained evidence therefore verifies API/session persistence and returned
SSR, **not visual browser QA or interactive editor behavior**. Source matching,
IR capture, compiler attribution and game/runtime validation remain unchanged.
