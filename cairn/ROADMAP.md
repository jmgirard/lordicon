# Roadmap

_The only authority on milestone status. Grouped by status, not ID._
_Last hygiene check: 2026-10-26 (review M013: archived, M010 row pruned; graduated 1 row, added 0; captured 0 lessons, marked 0 used; validate green)_

## Milestones

| ID | Title | Status | Depends on | Priority | File/Archive |
|---|---|---|---|---|---|
<!-- rows grouped by status, not sorted by ID; keep only the 3 most recent
     terminal (done or dropped) rows — older ones live in milestones/archive/ + git -->
| M013 | Name a missing first argument and Quarto's drops in IP1 | done | — | normal | milestones/archive/M013-ip1-missing-argument.md |
| M012 | Skip keys that hold a less-than or a noncharacter | done | — | normal | milestones/archive/M012-less-than-noncharacter-keys.md |
| M011 | Warn about an empty first argument | done | — | normal | milestones/archive/M011-empty-first-argument.md |

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
- [low] Match Quarto's case folding in warnings: the clash warning lowers with `pandoc.text.lower`, which folds Σ to σ, but Quarto's page folds it to ς, so `dataΣ dataσ` warns with no loss and `dataΣ dataς` loses a value with no warning — added 2026-10-24 — M004 review
- [low] Match each warning to its own call: `check_warnings` in `_tests/check_aria.py` counts the log lines for each warning text, so when two cases share a text, as `empty-li` and `empty-li-inline` do, one doubled and one missing warning still pass; match warnings to calls in document order — added 2026-10-25 — M011 review
- [low] Warn about a nested shortcode argument: the M011 diff-bug reviewer reported that `{{< li {{< meta empty >}} >}}` reaches the filter as a placeholder string and renders a wrong `src` with no warning; not reproduced in that session — added 2026-10-25 — M011 review
- [low] Say that an empty argument never shifts: `{{< li "" wlpxtupd >}}` shows no icon and warns, unlike `{{< li " x" wlpxtupd >}}` (see "Warn when Quarto shifts arguments left"), but README and CHANGELOG name only a lone empty argument, because `fixture_calls` accepts one positional argument — added 2026-10-25 — M011 review
- [parked] Know the WAI-ARIA 1.3 draft roles: the nameless-role warning's role list holds only published specs plus `image`, so `role="mark img"` warns though a current browser uses `mark`; promote when a user reports a false warning for a 1.3 role placed first — added 2026-10-25 — M008 plan
- [parked] Sort keys by byte, not by locale: `table.sort` in `build_element` and `warn_skipped` uses Lua's `<`, which follows the locale's collation, so under a non-C locale `role` can sort before `Role`, changing the attribute order and which duplicate the page keeps; a `quarto render` on Quarto 1.10.19 with `LC_ALL=en_US.UTF-8` kept the collation at `C` and sorted in byte order, observed 2026-10-26; `os.setlocale("en_US.UTF-8", "collate")` inside `quarto pandoc lua` does change the order, so a test can set it; promote when a Quarto render, or a filter in common use, is seen to set a non-C collation, or a user reports that attribute order changed — added 2026-10-24 — M004 review
- [parked] Warn when Quarto shifts arguments left: in `{{< li " x" wlpxtupd >}}` Quarto drops the leading-space `" x"` and `wlpxtupd` becomes the first argument, so the call renders that icon with no warning; found by the M010 claim audit; a probe filter got only `wlpxtupd` in both `args` and `raw_args` for that call on Quarto 1.10.19, so the filter cannot see the drop, observed 2026-10-26; promote when a Quarto release passes a dropped argument to the filter — added 2026-10-25 — M010
