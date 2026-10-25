# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-10-25 (review M009: archived, M006 row pruned; graduated 1 row, added 0; captured 1 lesson; validate green)_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 3 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->
| M010 | Warn on a lost first argument and document leading spaces | in-progress | M009 | normal | milestones/M010-leading-space-values.md |
| M009 | Quote spaced arguments in warning calls | done | — | normal | milestones/archive/M009-quote-call-arguments.md |
| M008 | Catch image roles after other tokens | done | — | normal | milestones/archive/M008-image-role-after-tokens.md |
| M007 | Check sorting, non-HTML output, and Minified spellings | done | — | normal | milestones/archive/M007-render-check-fixtures.md |

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
- Decide on keys that hold a less-than: `"a<b"=1` is forwarded as `a<b="1"`, which HTML parsers flag as an error but still read; D-003's skip set leaves `<` out; noncharacter keys such as U+FFFE or U+FDD0 pass through the same way — added 2026-10-24 — M003 review
- Sort keys by byte, not by locale: `table.sort` in `build_element` and `warn_skipped` uses Lua's `<`, which follows the locale's collation, so under a non-C locale `role` can sort before `Role`, changing the attribute order and which duplicate the page keeps — added 2026-10-24 — M004 review
- Keep values that start with a space: in a render, `label=" Bell "` and `aria-label=" . "` reach the filter empty, so the icon stays `aria-hidden`; find whether Quarto's shortcode parser or `value_of` drops them, and whether the docs or a warning should say so; with `role=img label=" Bell "` the nameless-role warning tells the user to add the label they wrote (M005 review) — added 2026-10-24 — M005 plan probe — started M010
- Warn about an empty first argument: `{{< li "" >}}` reaches the filter with an empty argument and renders `src="https://cdn.lordicon.com/.json"`, and `{{< lif "" >}}` renders `src=""`, with no warning — added 2026-10-25 — M010 plan audit
- [low] Match Quarto's case folding in warnings: the clash warning lowers with `pandoc.text.lower`, which folds Σ to σ, but Quarto's page folds it to ς, so `dataΣ dataσ` warns with no loss and `dataΣ dataς` loses a value with no warning — added 2026-10-24 — M004 review
- [parked] Know the WAI-ARIA 1.3 draft roles: the nameless-role warning's role list holds only published specs plus `image`, so `role="mark img"` warns though a current browser uses `mark`; promote when a user reports a false warning for a 1.3 role placed first — added 2026-10-25 — M008 plan
