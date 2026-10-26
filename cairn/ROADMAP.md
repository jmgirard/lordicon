# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-10-25 (review M011: archived, M008 row pruned; graduated 1 row, added 3; captured 1 lesson; validate green)_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 3 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->
| M012 | Skip keys that hold a less-than or a noncharacter | planned | — | normal | milestones/M012-less-than-noncharacter-keys.md |
| M011 | Warn about an empty first argument | done | — | normal | milestones/archive/M011-empty-first-argument.md |
| M010 | Warn on a lost first argument and document leading spaces | done | M009 | normal | milestones/archive/M010-leading-space-values.md |
| M009 | Quote spaced arguments in warning calls | done | — | normal | milestones/archive/M009-quote-call-arguments.md |

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
- Decide on keys that hold a less-than: `"a<b"=1` is forwarded as `a<b="1"`, which HTML parsers flag as an error but still read; D-003's skip set leaves `<` out; noncharacter keys such as U+FFFE or U+FDD0 pass through the same way — added 2026-10-24 — M003 review — started M012
- Sort keys by byte, not by locale: `table.sort` in `build_element` and `warn_skipped` uses Lua's `<`, which follows the locale's collation, so under a non-C locale `role` can sort before `Role`, changing the attribute order and which duplicate the page keeps; a `quarto render` on Quarto 1.10.19 with `LC_ALL=en_US.UTF-8` kept the collation at `C` and sorted in byte order, observed 2026-10-26 — added 2026-10-24 — M004 review
- Decide whether IP1 names Quarto's drops: IP1 lists only reserved keys, invalid names, and an empty first argument (D-005, corrected M011) as exceptions to passthrough, but Quarto drops a value or first argument that starts with a space or tab before the extension runs, and a call with no first argument now makes no element; changing IP1 takes the user's decision and a D-entry (D-003) — added 2026-10-25 — M010 review
- [low] Warn when Quarto shifts arguments left: in `{{< li " x" wlpxtupd >}}` Quarto drops the leading-space `" x"` and `wlpxtupd` becomes the first argument, so the call renders that icon with no warning; found by the M010 claim audit — added 2026-10-25 — M010
- [low] Match Quarto's case folding in warnings: the clash warning lowers with `pandoc.text.lower`, which folds Σ to σ, but Quarto's page folds it to ς, so `dataΣ dataσ` warns with no loss and `dataΣ dataς` loses a value with no warning — added 2026-10-24 — M004 review
- [low] Match each warning to its own call: `check_warnings` in `_tests/check_aria.py` counts the log lines for each warning text, so when two cases share a text, as `empty-li` and `empty-li-inline` do, one doubled and one missing warning still pass; match warnings to calls in document order — added 2026-10-25 — M011 review
- [low] Warn about a nested shortcode argument: the M011 diff-bug reviewer reported that `{{< li {{< meta empty >}} >}}` reaches the filter as a placeholder string and renders a wrong `src` with no warning; not reproduced in that session — added 2026-10-25 — M011 review
- [low] Say that an empty argument never shifts: `{{< li "" wlpxtupd >}}` shows no icon and warns, unlike `{{< li " x" wlpxtupd >}}` (see "Warn when Quarto shifts arguments left"), but README and CHANGELOG name only a lone empty argument, because `fixture_calls` accepts one positional argument — added 2026-10-25 — M011 review
- [parked] Know the WAI-ARIA 1.3 draft roles: the nameless-role warning's role list holds only published specs plus `image`, so `role="mark img"` warns though a current browser uses `mark`; promote when a user reports a false warning for a 1.3 role placed first — added 2026-10-25 — M008 plan
