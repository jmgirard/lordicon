# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-10-24 (review M005: archived; graduated 2 rows, added 1; captured 2 lessons; validate green)_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 3 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->
| M006 | Name the call in the Minified warning | review | — | normal | milestones/M006-minified-warning-call.md |
| M005 | Warn when a role icon has no name | done | — | normal | milestones/archive/M005-nameless-role-warning.md |
| M004 | Warn about keys in another letter case | done | — | normal | milestones/archive/M004-letter-case-warnings.md |
| M003 | Stop key clashes and bad attribute names | done | M002 | normal | milestones/archive/M003-key-clashes.md |

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
- Add a render check with fixtures: extend `_tests/` (ARIA, `src`, skipped and kept keys, letter-case warnings, and the Minified warning are covered since M004, the nameless-role warning since M005) to attribute sorting and non-HTML output; also the once-per-file Minified rule, which keys the path as written, so `./minified.json` warns again (M004 review) — added 2026-10-20, narrowed 2026-10-20 by M001, narrowed 2026-10-24 by M003, narrowed 2026-10-24 by M004 — DESIGN Known issues
- Decide on keys that hold a less-than: `"a<b"=1` is forwarded as `a<b="1"`, which HTML parsers flag as an error but still read; D-003's skip set leaves `<` out; noncharacter keys such as U+FFFE or U+FDD0 pass through the same way — added 2026-10-24 — M003 review
- Sort keys by byte, not by locale: `table.sort` in `build_element` and `warn_skipped` uses Lua's `<`, which follows the locale's collation, so under a non-C locale `role` can sort before `Role`, changing the attribute order and which duplicate the page keeps — added 2026-10-24 — M004 review
- Name the call in the Minified warning: it names the file (`minified.json looks like …`), while the other warnings name the call, such as `{{< lif FILE >}}` — added 2026-10-24 — M004 review — started M006
- Catch image roles after other tokens: the nameless-role warning reads only the first role token, but browsers use the first role they know, so `role="bogus img"` gives an unnamed image with no warning; reading the first known token needs a list of ARIA roles — added 2026-10-24 — M005 review
- Keep values that start with a space: in a render, `label=" Bell "` and `aria-label=" . "` reach the filter empty, so the icon stays `aria-hidden`; find whether Quarto's shortcode parser or `value_of` drops them, and whether the docs or a warning should say so; with `role=img label=" Bell "` the nameless-role warning tells the user to add the label they wrote (M005 review) — added 2026-10-24 — M005 plan probe
- [low] Match Quarto's case folding in warnings: the clash warning lowers with `pandoc.text.lower`, which folds Σ to σ, but Quarto's page folds it to ς, so `dataΣ dataσ` warns with no loss and `dataΣ dataς` loses a value with no warning — added 2026-10-24 — M004 review
