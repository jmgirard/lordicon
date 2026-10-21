# Decisions

Append-only. Never renumber; supersede with a new entry. D-entries record
choices with rationale — never deferrals ("not now" is a ROADMAP fact).

### D-001 (2026-10-20): The extension version rises at each shipping merge

**Context:** `quarto add jmgirard/lordicon` installs from `main`, so every merge reaches users at once; history already raised `_extension.yml` with each change (09a2e5f, 825985a).
**Decision:** Each merge that ships a user-visible change raises `version:` in `_extension.yml`; the `v<version>` tag follows the merge.
**Consequences:** `/cairn-release` takes its tag-only arm for these versions; considered raising only at release time, rejected because users on `main` would get changes under an old number.

### D-002 (2026-10-20): Keep a CHANGELOG.md

**Context:** Users of `quarto add` see no commit log, and release notes so far came only from commit subjects.
**Decision:** The repo keeps `CHANGELOG.md`, with an entry for each user-visible change; the PROFILE `changelog` slot names it.
**Consequences:** The review consistency gate checks for an entry in each milestone; the file is created by a candidate milestone, and until it exists the slot reads as none.
