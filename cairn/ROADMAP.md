# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-10-20 (design interview added four candidates)_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 3 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->
| M001 | Let user ARIA attributes beat defaults | in-progress | — | high | milestones/M001-user-aria-beats-defaults.md |

## Candidates
<!-- unnumbered ideas; one line each, ordered high → normal → low → parked:
     - [high] short title: detail — added YYYY-MM-DD — links
     - short title: detail — added YYYY-MM-DD — links
     - [parked] short title: detail; promote when <condition> — added YYYY-MM-DD — links
     the opening token is `[high]`/`[low]`/`[parked]` or absent (`normal`); `[parked]` marks a row whose
     promotion condition has not held — tracking-rules "Candidate priority token";
     open each row with its short title, the words the cairn pane shows, then `: `;
     the title is one sentence with no ending period, at least 5 words and at most 40 characters,
     ending with `(#N)` for a row written for GitHub issue N, such as
     `Fix SE of skewness calculation (#100)`; `/cairn-triage` offers a new title for one
     with fewer than 5 words or more than 40 characters; tracking-rules "Candidate short title" has the whole rule -->
- [high] Let user ARIA attributes beat defaults: with no `label`, `lordicon.lua` adds `aria-hidden="true"` even when the user passes `aria-label`, `aria-hidden`, or `role`; skip the default then (IP1, GP5) — added 2026-10-20 — DESIGN Known issues — started M001
- Start a CHANGELOG.md for releases: create the file with past versions from the `v*` tags and commit subjects (D-002) — added 2026-10-20 — PROFILE changelog slot
- Add a render check with fixtures: a fixture `.qmd` and a script that renders it and checks the `<lord-icon>` output, so verify is not only by eye — added 2026-10-20 — DESIGN Known issues — started M001
- Stop duplicate src and ARIA attributes: a user `src` key gives a second `src` beside the extension's own (IP1), and a mixed-case `Role` or `ARIA-LABEL` is not matched against the ARIA defaults — added 2026-10-20 — M001 criteria audit
- Close out the element API todo (#4): `loading` already passes through; an `icon` argument needs a GP3 case or a no — added 2026-10-20 — https://github.com/jmgirard/lordicon/issues/4
