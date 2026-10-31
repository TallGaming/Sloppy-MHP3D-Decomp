# Publication and future updates

The audited snapshot was committed and pushed on 2026-10-31 at the user's
explicit request. Initial publication is commit `5a80710`. The original working
project, game data and private evidence remain outside this public repository.

Read PUBLICATION_CHECK.md, README.md and docs/HELP_WANTED.md before publishing.
The configured `origin` is
`https://github.com/TallGaming/Sloppy-MHP3D-Decomp.git`, supplied by the user.
The initially empty repository was private. It was made public to carry out the
public-release request, and anonymous API access was verified. The authenticated
GitHub account was verified as TallGaming. Git is configured locally for this
repository as TallGaming with `340650866+TallGaming@users.noreply.github.com`;
no private email or global Git setting was used. A project-wide license remains
unselected, as recorded in LICENSE_STATUS.md.

For a future reviewed update, stage only audited public files, inspect the diff,
run the checks appropriate to the change, then commit and push:

```sh
git diff --cached
git commit -m "Describe the reviewed change"
git push
```

Fetch/reconcile any newer remote history before pushing. Do not force-push over
existing work. No access token belongs in a
remote URL, committed file or help request.

The prepared help request is docs/HELP_WANTED.md. The compiler-help issue form
is in .github/ISSUE_TEMPLATE/compiler-help.yml. These files are published in Git;
no issue, discussion, email or other outreach message has been posted.
