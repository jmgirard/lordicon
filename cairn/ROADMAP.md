# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-10-24 (M003 done: two rows graduated, two rows added)_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 3 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->
| M003 | Stop key clashes and bad attribute names | done | M002 | normal | milestones/archive/M003-key-clashes.md |
| M002 | Start CHANGELOG.md for past releases | done | — | normal | milestones/archive/M002-start-changelog.md |
| M001 | Let user ARIA attributes beat defaults | done | — | high | milestones/archive/M001-user-aria-beats-defaults.md |

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
- Add a render check with fixtures: extend `_tests/` (ARIA, `src`, and skipped and kept keys are covered since M003) to attribute sorting, the Minified warning, and non-HTML output — added 2026-10-20, narrowed 2026-10-20 by M001, narrowed 2026-10-24 by M003 — DESIGN Known issues
- Warn on keys that differ only in case: two keys in one call that differ only in letter case, such as `role=x Role=y` or `label` and `Label`, both reach `<lord-icon>`, and HTML keeps one, because attribute names ignore case — added 2026-10-20 — M003 criteria audit
- Reword GP5 for user ARIA precedence: GP5 says an icon without `label` is `aria-hidden`, but since M001 a user `aria-hidden`, `aria-label`, `aria-labelledby`, or `role` turns the default off (IP1); a principle change takes the user's decision and a D-entry — added 2026-10-20 — M001 review
- Warn when a role icon has no name: `role="img"` with no `label`, `aria-label`, or `aria-labelledby` (or a blank `aria-label`) now gives an unhidden icon with no accessible name; decide whether this earns a GP2 warning — added 2026-10-20 — M001 review
- Close out the element API todo (#4): `loading` already passes through; an `icon` argument needs a GP3 case or a no — added 2026-10-20 — https://github.com/jmgirard/lordicon/issues/4
- Match Minified-check keys in any case: `check_minified` (`lordicon.lua`) looks up `colors`, `stroke`, and `state` by exact case, so `Colors=` reaches the element and works, but the Minified warning does not fire (GP2); since 825985a — added 2026-10-24 — M003 review
- Decide on keys that hold a less-than: `"a<b"=1` is forwarded as `a<b="1"`, which HTML parsers flag as an error but still read; D-003's skip set leaves `<` out; noncharacter keys such as U+FFFE or U+FDD0 pass through the same way — added 2026-10-24 — M003 review
