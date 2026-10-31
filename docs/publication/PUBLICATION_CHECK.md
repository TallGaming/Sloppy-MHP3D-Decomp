# Publication preparation check — 2026-10-31

This records the preparation review and subsequent user-authorized GitHub
publication on 2026-10-31. The audited snapshot was pushed as initial commit
`5a80710`, and anonymous access to the public repository was verified. No issue
or other outreach message has been posted. The private working project was
preserved. The user-supplied GitHub destination is configured as `origin`.

## Included and excluded

Included: authored documentation and historical checkpoints, five game-source
hypotheses, invented compiler fixtures, Python tools/tests, a minimal offline
comparison guide, a compiler-help issue form and a Windows/Linux CI workflow.
Start with [the help request](../HELP_WANTED.md) and
[current status](../CURRENT_STATUS.md).

Excluded: original game images, extracted assets/code dumps, saves, proprietary
toolchains/SDKs, keys, local service databases, external source caches and private
execution evidence. User-supplied reference documents from other projects are
referenced rather than redistributed. Two machine-specific service operator
scripts were omitted. There is no copied private Git history.

[SOURCE_EXPORT.json](SOURCE_EXPORT.json) records the original identities of 287
authored files and the identities of their adapted public copies. Historical
source hashes remain historical; anonymization does not manufacture new evidence.
All 21 exported bench sources retain their exact original bytes. Git attributes
disable newline conversion to preserve source hashes across platforms.

## Completed checks

- Clean public-directory tests on Windows: **362 run, 360 passed, 2 platform
  skips**; exit status 0.
- Clean public-directory tests under Ubuntu/WSL: **362 passed, no skips**;
  exit status 0. Tests use invented inputs/mocks, with no game data or compiler.
- The new offline comparison tool contributes ten tests included in those totals.
- Independent documentation review: local links, factual status, source hashes,
  current versus historical instructions and matching-attempt counts checked.
  See [DOCUMENT_AUDIT.md](DOCUMENT_AUDIT.md).
- Independent content review: text payload, secrets/private paths, excluded
  material, source identities and Git byte preservation checked. See
  [CONTENT_AUDIT.md](CONTENT_AUDIT.md).
- Case-sensitive ignore checks reject upper/mixed-case game/tool extensions,
  private directories and cookie JSON as well as the usual lowercase names.
- CI and issue-form YAML parse successfully. CI actions are pinned to verified
  upstream commit identities. Preparation results above are local tests;
  live GitHub execution is reported separately on the repository's Actions page.

Tooling tests do not establish a game match. The historical toolchain remains
unlocked, there are zero credited or linked-source functions, and the full-game
byte gate plus its eighteen negative checks remain unimplemented.

## Git-tree and archive verification

The initial prepared Git tree contained 313 text files. A Git-generated ZIP was extracted
into a new directory with no private inputs. Every archive entry matched the
indexed working file byte for byte; no absolute/traversing entry or symlink was
present. The extracted snapshot passed **362 tests under Ubuntu/WSL, no skips**.
That audit checked 186 Markdown documents: **577 local links, zero broken links**.
The final publication ZIP is checked against the final staged tree separately;
its tree identity, file hashes and ZIP hash are recorded in the local receipt.

Four historical extra-blank-line-at-EOF warnings remain in the staged whitespace
check: the 3AH, 3AI and 3AJ validation-note pages and
`tests/test_language_modes.py`. They are retained to avoid incidental changes to
the research snapshot. CRLF is recognized explicitly while newline conversion
remains disabled. No new public-file whitespace defect was reported.

The contributor-documentation follow-up added three current guides and a PR
template, with links from README, CONTRIBUTING, HANDOFF and the documentation
index. They explain the post-toolchain checkpoints, the matching contribution
loop and the task/review record. These are instructions for future work, not a
claim that the compiler or build gate was implemented.

The revised public payload contains **317 text files**, including **190 Markdown
documents with 599 local links and zero broken links**. The full test suite was
not repeated for that documentation-only change. Implementation/fixture bytes
were unchanged by the documentation revision; source-export pins, links,
whitespace exceptions and final archive bytes were checked again. The external
release receipt records updated payload hashes and later validation separately.

## GitHub Windows test-fixture portability follow-up

The initial Linux CI job passed. Windows CI exposed temporary-directory 8.3
aliases: tools canonicalized the root, while fixture expectations retained its
short spelling. This produced path-comparison failures despite referring to the
same directory. Temporary roots in eleven test modules now use `Path.resolve()`
before fixture paths are constructed (twelve setup-line changes). Assertions and
rejection controls remain enabled; production tools, compiler profiles and all
bench/game-source bytes are unchanged. SOURCE_EXPORT preserves historical source
hashes and records updated public-copy hashes for the adapted tests.

For this fix the complete suite passed again: **362 passed on Linux, no skips**;
under an actual Windows short-alias temporary root, **360 passed and 2 platform
checks skipped** (362 run, zero failures/errors). These remain tooling checks,
separate from the unimplemented game gate. The release receipt records this
validation; GitHub results are visible on the repository's Actions page.

The initial audited snapshot is committed on `main`, with `origin` set to
`https://github.com/TallGaming/Sloppy-MHP3D-Decomp.git`. The ZIP contains the public payload
without Git metadata; the separately preserved private project is not packaged.

## Decisions still needed for publication

The initially empty repository was made public after the explicit push request;
anonymous API access confirms visibility. The authenticated account was verified
as TallGaming. Its ID-based GitHub noreply address is configured only in this
repository, rather than exposing a private email or changing global settings.
A project-wide license remains unselected; see
[LICENSE_STATUS.md](../../LICENSE_STATUS.md). This is a
public research snapshot, not a claim that it is already licensed open source.

[PUBLISH.md](PUBLISH.md) records publication and future update steps. The help
request is available in Git; no separate issue or outreach message was posted.
