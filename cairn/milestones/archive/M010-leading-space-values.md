# M010: Warn on a lost first argument and document leading spaces

**Status:** done (2026-10-25, PR #14 https://github.com/jmgirard/lordicon/pull/14)

**Goal:** A `li` or `lif` call with no first argument makes no element and warns instead of failing the render, and the docs say that Quarto drops a value or first argument that starts with a space or tab.

**Outcome:** Version 0.7.9. `li` and `lif` call `no_first_argument` when `args[1]` is nil: it warns in `html:js` formats only and returns `pandoc.Inlines({})`, where before `stringify(args[1])` stopped the render with "Cannot get Attr from TypeNil". README (Customizing) and `index.qmd` (Accessibility) say that Quarto drops a quoted value or first argument that starts with a space or tab, with its key, before the extension runs; that a following positional argument then becomes the first; and that removing the space fixes it. `_tests/aria.qmd` gained `lost-li`, `missing-lif`, `shift-li`, and four leading-space cases (`label=" Bell "`, `label=' Bell'`, a tab byte, `class=" x"`); `fixture_calls` models Quarto's drop, `NO_ICON` asserts no element, and `raw_output.lua` takes a null `arg`.

**Decisions:** none (implementation choices are work-log lines: empty `Inlines` over `pandoc.Null()`, one expectation for page and filter).

**Review:** four-lens fan-out plus an implement-side claim audit (32 claims, 0 false); 21 findings: 6 fixed on the branch (crash on a trailing empty line in `check_spelling`, silent extra positional words in `fixture_calls`, a docs sentence that ignored the argument shift, a stray `index.qmd` space), 2 to candidate row "Decide whether IP1 names Quarto's drops", 13 rejected with reasons. Candidate rows added: "Warn when Quarto shifts arguments left" and the IP1 row. Graduated candidate row "Keep values that start with a space" (the warning hint it raised was declined at the question set). Captured 1 lesson (`pandoc.Null` under `quarto pandoc lua`); extended the M005 lesson with the tab and the argument shift.
