> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Bucket 3N: local matching workbench — completed checkpoint

The user approved the local instance, then granted advance approval to continue
project work for five hours. The workbench is running at
**http://127.0.0.1:8787/new**. Startup, shutdown and persistence instructions are
in `DECOMPME_LOCAL.md`. This checkpoint records completed work; the active
five-hour window permits the next documented diagnostic without waiting here.

## Outputs and validation

- Pinned upstream source `cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7`, Docker Engine
  29.9.2 and Compose 5.6.1 in Ubuntu WSL. Application dependencies were installed
  from locked files before starting the isolated runtime.
- Four local services, only nginx publishing `127.0.0.1:8787`. Backend, frontend
  and compiler service have no published ports and use only the internal network.
  The application has a copied hash-verified MW219 executable; no project/game
  directory is mounted. All earlier project tools and game inputs remain intact.
- Default remote objdiff object transfer is disabled; the served editor bundle
  points to a local inert page. Telemetry is disabled. Local CSP and Host/Origin
  rejection were checked, including actual foreign-request HTTP 403 responses.
- Real `/new`, `/platform`, scratch editor server rendering and PSP metadata
  passed. Repeated local compiles returned valid complete ELF objects with the
  full invented twelve-byte function. Two service objects and two fresh existing
  standalone-runner objects are identical in all 624 bytes, SHA-256
  `e623ca821a5ee6baed036c5d820cebdf43340950e659026ec0da0bffc1d93edc`.
- A genuine syntax error returns failure and no previous compiled object.
  Session claim/edit and an actual controller stop/start preserve scratch name,
  exact source, owner and profile. Local HTTP cookies are HttpOnly/SameSite Lax.
- Lifecycle controls verify source revision and tracked changes plus compose,
  keeper, nginx and backend-start hashes. Four deliberately wrong expected pins
  are rejected before any lifecycle action; positive validation passes.
- All **296 existing tooling tests pass**, with the complete log retained at
  `evidence/bucket-03n/tooling-tests.log`. Integration checks above are reported
  separately; they are not the future full-game gate's eighteen negative checks.

The two helpers independently audited deployment/source boundaries, served local
assets, retained API evidence, complete objects and session/restart evidence.
Their reports are `DECOMPME_LOCAL_REVIEW.md` and
`BUCKET_03N_VALIDATION_NOTES.md`. The final summary and identities are under
`evidence/bucket-03n/`.

## Preserved failures and limits

The internal-only initial network did not create a published host port; only
nginx now also joins a publishing network. WSL would stop between commands;
a scoped single-instance keeper handles this without globally shutting down WSL.
The first smoke retained a connection failure. The second caught the create API
trimming a final newline; the invented source was made canonical before the
successful run, while strict equality remained enforced. An initial session
probe compared the intentionally ephemeral pre-cookie profile to the later
persistent one; the corrected test follows the actual session lifecycle.

Visual browser QA is incomplete. The computer-use tool stopped because it cannot
enforce URL policy for the current Firefox session; no further UI automation
occurred. HTML/asset/API validation does not substitute for a visual browser run.
Sanitized JSON response records retain semantics and object bytes; recorded wire
hashes cannot be recomputed from reformatted/redacted JSON alone.

Container wibo is not byte-identical to the existing standalone runner. The
observed complete-object equality is limited to the invented fixture; it does
not establish historical attribution or equality for every compilation.
Source commit and lockfiles do not make container base tags/apt packages
intrinsically reproducible; resolved identities are recorded.

No game function was compiled or changed in this bucket. Game-match, linked-source,
parking and matching-trick totals remain zero. Toolchain attribution, the all-module
byte gate and its eighteen negative checks remain unresolved or unimplemented.
Readable source first, fixed per-function settings, private scope and matching
all original game code before native-port work remain unchanged.
