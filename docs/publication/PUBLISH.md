# Publishing this prepared snapshot

The release contents are staged in this separate public repository. The original
working project, game data and private evidence remain outside it. Nothing has
been uploaded by the preparation process.

Read PUBLICATION_CHECK.md, README.md and docs/HELP_WANTED.md before publishing.
The configured `origin` is
`https://github.com/TallGaming/Sloppy-MHP3D-Decomp.git`, supplied by the user.
Authenticated Git access advertised no refs when checked on 2026-10-31.
Anonymous Git access failed and the anonymous GitHub API returned 404; public
visibility is not verified. Check repository visibility before public outreach.
The repository currently has no configured commit author.
Choose the public identity you want attached to the initial commit; a GitHub
noreply address can be used if appropriate. A project-wide license is also
unselected, as recorded in LICENSE_STATUS.md.

From the prepared repository, after supplying the public author identity:

```sh
git config user.name "YOUR PUBLIC COMMIT NAME"
git config user.email "YOUR PUBLIC COMMIT EMAIL"
git commit -m "Prepare public MHP3 matching-decomp research snapshot"
git push -u origin main
```

Use an empty GitHub repository or reconcile any existing remote history before
pushing. Do not force-push over existing work. No access token belongs in a
remote URL, committed file or help request.

The prepared help request is docs/HELP_WANTED.md. The compiler-help issue form
is in .github/ISSUE_TEMPLATE/compiler-help.yml. They are drafts for publication;
no issue, discussion, email or other outreach message has been posted.
