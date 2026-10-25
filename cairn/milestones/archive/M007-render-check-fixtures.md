# M007: Check sorting, non-HTML output, and Minified spellings

**Status:** done (2026-10-25, PR #11 https://github.com/jmgirard/lordicon/pull/11)

**Goal:** `_tests/check_aria.py` checks three behaviors that were checked by eye: the order of an icon's attributes, the empty output of a non-HTML render, and the Minified warning's once-per-path rule.

**Outcome:** `check_aria.py` adds an `ORDER` table compared in `check()` for
the page and the raw output (`sorted` case, mixed-case `Zeta` to tell byte
order from case folding); `render(to, output)` replaces `render_page()`, and
`check_non_html()` renders `aria.qmd` to `gfm` and fails on `lord-icon`,
`{{<`, or a lordicon warning; `minified-again` and `minified-dotslash` pin
one Minified warning per path as written. 65 cases, 33 warnings. The comment
above `warned_minified` states the rule; no behavior change, no version
bump. DESIGN Known issues names what still has no test.

**Decisions:** none. The plan gate pinned the once-per-path rule over a fix
(user's choice) and chose one `gfm` render over several formats.

**Review:** one pass, four-lens fan-out; reduced criteria audit fixed AC4's
`docs/` clause. 14 findings: 6 fixed (comment, docstring, three DESIGN
lines), 0 follow-ups, 8 rejected (5 planned, 2 false, 1 edge). Hygiene
graduated "Add a render check with fixtures"; captured 1 lesson.
