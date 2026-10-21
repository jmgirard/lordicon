# Toolchain profile: quarto-extension

<!-- A cairn *toolchain profile*: the language/toolchain-specific slots the
     operational skills read. cairn-init instantiates this into the repo's
     `cairn/PROFILE.md`. The oracle / Validation doctrine is UNIVERSAL and
     deliberately NOT a slot here — it is the orthogonal domain axis
     (D-024/D-025), stated once in skills/shared/validation-doctrine.md
     (referenced from tracking-rules). All seven `## <slot>` sections
     are defined; cairn_validate FAILs on a missing or empty slot. -->

The Quarto extension toolchain: a repo whose deliverable is a Quarto extension
under `_extensions/<name>/` (a filter, shortcode, format, or project type),
installed with `quarto add <owner>/<repo>`. Quarto 1.10 installs from the
branch named `main`, so in a repo whose default branch is `main` a merge
reaches users at once. A `v<version>` tag and a GitHub release mark the
version for `quarto add <owner>/<repo>@v<version>` and the releases page.
Selected by `cairn-init` when `_extensions/*/_extension.yml` (or `.yaml`) is
present and no language, plugin, or `Dockerfile` marker is. With a
`Dockerfile`, the disambiguation gate asks.

## verify
Run by `/milestone-implement` (per task) and `/hotfix` (gate-lite). Run
`python3 _tests/check_aria.py`, which renders `_tests/aria.qmd` and checks the
ARIA attributes of each icon. It must exit 0. Then run `quarto render` at the
repo root, which renders the demo site into `docs/`. Then open each changed demo page in a browser and make
sure that its icons load and animate. After a player change, run `npm run build` first.

## consistency-gate
Toolchain checks `/milestone-review` runs *in addition to* the universal
cairn-file checks (`cairn_validate`, coverage completeness, `cairn_impact`):
- Every version marker that `release-walk` names holds the same version.
- The verify render succeeds on the review head.
- The declared changelog (`## changelog` slot) has an entry for this
  milestone's user-visible changes, or the slot says "none".
  A milestone of a feature series (tracking-rules "Feature series") meets this with an edit to the series' existing entry.
  This holds where the series already has an entry. A milestone is in a series when its work log carries a `feature series:` line.
  A milestone before the series' last with no user-visible change needs no entry.

## test-doctrine
Test expectations layered on the universal "What gets a test" rules in
tracking-rules. An extension is checked by rendering, not by calling functions:
- A filter or shortcode change is tested by rendering a fixture document that
  uses it and checking the output (a string in the HTML, or a snapshot of it).
- A bug fix gets a fixture document that renders wrong before the fix.
- A change to a shipped asset (JavaScript, CSS) that browsers cache by path
  raises the version wherever the repo ties the asset path to it.

## release-walk
The release procedure `/cairn-release` follows. Here the version rises in each
shipping merge (D-001), so the tag-only arm is the usual one. The version marker is
`version:` in `_extensions/<name>/_extension.yml` (or `.yaml`). A repo that
keeps the same version in more files names each file here. One example is an
`add_html_dependency{ version = ... }` call in the extension's Lua filter.
Every named marker holds the same version. Before step 1 of `/cairn-release`,
run `git fetch --tags <base>` and read the remote default branch's tip:
`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cairn_versions.py" <marker file> --at <base>/<default-branch>`,
where `<marker file>` is the repo's `_extension.yml` or `_extension.yaml`. When
`CLAUDE_PLUGIN_ROOT` is unset, use the cairn plugin's install directory. The script refuses a shallow clone. It prints the tip's
version, the first commit of that version's unbroken run of first-parent
commits (`start`), and whether a `v<version>` tag exists.
- **Tag-only arm.** When the tag is absent, the tip's version is unreleased:
  merged work raised it, or it was never tagged. Raise nothing and make no
  prep commit. First check that every other named marker holds the version
  at `start` (`git show <start>:<file>`). With a declared changelog, find the
  section whose heading names the version (`## 1.2.9`, `## v1.2.9`, or
  `## [1.2.9]`, not `## 1.2.90`) in the file at the remote tip. Then step 1 asks the user to confirm the version and
  `start` (its subject) instead of choosing a bump. Step 2 makes no edit, but
  its claim-read runs on that section against the code at `start`. Tag the
  run's start: `git tag -a v<version> <start> -m "v<version>"`, pushed at the
  user's approval.
- **Stops.** A marker mismatch, a declared changelog with no section for the
  version, a false claim, or a declined confirmation ends the run with the
  reason and no tag. A missing section or a false claim clears with a merged
  changelog edit: retitle the development heading to the version, reword the
  claim, or move a later entry back under the development heading. Then run
  `/cairn-release` again. A marker mismatch
  at `start` cannot be fixed for this version: only a merge that raises the
  version again clears it, and this version then stays untagged.
- **Release-time arm.** When the tag exists, run the generic walk. Decide the
  bump (patch/minor/major) from the declared changelog. With changelog "none",
  decide it from git history and skip the consolidation. Raise every named
  marker and commit the release prep to the default branch. Tag that commit
  `v<version>`, pushed at the user's approval.
- **Release notes.** The notes are the changelog section for the version. With
  changelog "none", they are the commit subjects on the default branch since
  the previous `v*` tag:
  `git log --first-parent --format='- %s' <previous tag>..<tagged commit>`.
  The previous tag is
  `git describe --first-parent --tags --abbrev=0 --match 'v*' <tagged commit>^`.
  For a first release, with no previous `v*` tag, drop `<previous tag>..`.
  Where the `origin` remote is GitHub and `gh` is available, the handoff
  provides a `gh release create` command with these notes. cairn never runs
  it (the universal step 4). No registry step: the tag is the release.

## init-detection
Recognized by `cairn-init` from `_extensions/*/_extension.yml` or
`_extensions/*/_extension.yaml`. The repo must also have no `DESCRIPTION`, no
`pyproject.toml`/`setup.py`/`setup.cfg`, and no
`.claude-plugin/plugin.json`/`.claude-plugin/marketplace.json`. It ranks ahead
of docker-image and generic. A repo that also carries a language, plugin, or
`Dockerfile` marker is a hybrid: cairn-init runs the disambiguation gate.

## greenfield-openers
Openers `cairn-init` asks in a new or empty extension repo, on top of the
universal openers (distribution ambition and numeric-work oracles):
- **Extension type?** Filter, shortcode, format, or project type.
  - Lands in: DESIGN Purpose and the verify render's fixture document.
- **When does the version rise?** At release (reversible default), or at each
  merge that changes a shipped asset, when browsers cache that asset by a path
  that holds the version.
  - Consequence: at merge, the close hands over the tag commands (owner mode,
    `/milestone-review` step 10); the tag-only arm tags only the tip's version,
    so earlier untagged ones stay so. At release, the release-time arm raises it.
  - Lands in: CLAUDE.md conventions and the `release-walk` marker list.

## changelog
`CHANGELOG.md` (D-002). The file does not exist yet; a ROADMAP candidate
creates it. Until it exists, read this slot as "none".
