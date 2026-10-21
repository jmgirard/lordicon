# M002: Start CHANGELOG.md for past releases

**Status:** done (2026-10-20, PR #6 https://github.com/jmgirard/lordicon/pull/6)

**Goal:** The repo has a CHANGELOG.md that lists each tagged version with its user-visible changes (D-002).

**Outcome:** `CHANGELOG.md` at the repo root has one `## <version>` section per `v*` tag, 0.0.1 to 0.7.2, newest first, with no Unreleased heading. Entries cover shortcode arguments and output, render warnings, the required Quarto version, the extension's CSS, and bundled player versions from `package-lock.json`, plus README and demo changes as best effort. README links to it under Installing. The PROFILE `changelog` slot and the DESIGN Conventions bullet name the file. No version raise, because `_extensions/` did not change (D-001).

**Decisions:** none promoted. AC2 was amended at the user's choice: completeness is promised only for changes that `git diff` shows in `_extensions/lordicon/`, `src/`, `package.json`, and `package-lock.json`. README and demo entries are best effort, a deliberate difference from D-002's wording.

**Review:** four-lens fan-out over three passes. There was one defect return, for missing README entries, and one amendment return on AC2, after each pass found more README edits. 18 findings fixed, 17 rejected (build-tool-only changes, internal renames, history-record wording), 5 noted, none to candidates. The claim audit before review corrected 5 claims and added 5 missing changes. Hygiene graduated "Start a CHANGELOG.md for releases".
