> Historical research snapshot. See [current public status](CURRENT_STATUS.md). Local evidence, game files and proprietary tools mentioned below are not distributed. Earlier privacy/approval decisions are historical; the current public-release request supersedes them.

# Local decomp.me workbench

Open **http://127.0.0.1:8787/new**. This is the private local installation,
separate from the public decomp.me website. It currently exposes the existing
Metrowerks PSP build 219 as a diagnostic compiler, not a selected game toolchain.

Run these from `<project-root>` in PowerShell:

```powershell
python scripts/decompme_local.py start
python scripts/decompme_local.py status
python scripts/decompme_local.py logs
python scripts/decompme_local.py stop
```

`start` checks the source revision, tracked source changes, compose configuration,
reverse-proxy configuration, backend startup script and WSL keeper hashes. It
starts existing images and a single scoped helper that keeps WSL active.
`stop` removes this application's containers/network and stops its keeper;
it preserves saved scratches and installed tools. It does not shut down WSL
globally or remove other applications.

The source checkout lives inside Ubuntu WSL at
`/home/<user>/mhp3rd-tools/decompme-local`, pinned to
`cddb46d53a0405f35be42c1c45aaa5b59dfa1ad7`. Deployment files and persistent
SQLite data live at `/home/<user>/mhp3rd-tools/decompme-instance`;
the database is `state/decompme.sqlite3`. Scratch media is in the checkout's
`backend/media`. These directories are local private state, not repository files.
Machine configuration is recorded in `config/decompme-local.json`.

## Using a scratch

Select **PlayStation Portable** and **mwccpsp 3.0.1 build 219**. The invented
validation fixture used the fixed diagnostic flags `-nostdinc -lang c -O2` and
no preset or libraries. Actual game experiments must retain their own reviewed
language/settings; this C fixture does not replace the existing C++/O2 profile.
Supporting declarations belong in Context, readable function source in Source,
and the complete target function in Target Assembly. Use the assembly diff view.

The normal local UI can create an anonymous persistent profile without GitHub.
An initial read-only user request is intentionally ephemeral; creating/claiming
a scratch establishes the session. Keep browser cookies to retain edit ownership.
The installation's scratch list is shared among its local users; this is not a
per-scratch access-control system. The reverse proxy accepts only the local
Host/Origin and publishes only `127.0.0.1:8787`.

The external objdiff iframe is replaced with a local explanatory page. Browser
CSP permits local connections, telemetry DSNs are empty, and the application
services use an internal Docker network. Only nginx also joins the network
needed for loopback publication. No game images or project directories are
mounted into the application. No project data was sent to public decomp.me.

## Verified behavior and limits

The fixed invented `workbench_sum` fixture compiled repeatedly. Both complete
624-byte objects equal two fresh objects from the existing standalone compiler
and runner, SHA-256
`e623ca821a5ee6baed036c5d820cebdf43340950e659026ec0da0bffc1d93edc`.
The complete twelve-byte function also equals the independently assembled
invented target. Syntax errors fail visibly without returning a stale object.
Actual session claim/edit and full stop/start persistence passed.

The container's wibo binary differs from the standalone runner; parity was
proved for this fixture only. Compiler identity, global code-generation
equivalence and original game-toolchain attribution do not follow from it.
The workbench's instruction score cannot replace our complete-byte gate,
source-participation evidence or eighteen required negative checks.

Server-rendered pages, served editor assets, APIs and actual compilation were
checked. Visual browser interaction remains unverified: the computer-use tool
stopped because URL policy enforcement was unsupported for the current Firefox
session. No further browser automation was attempted. See
`BUCKET_03N_CHECKPOINT.md`, `DECOMPME_LOCAL_REVIEW.md` and
`BUCKET_03N_VALIDATION_NOTES.md` for evidence and preserved setup failures.
