# M011: Warn about an empty first argument

**Status:** done (2026-10-25, PR #15 https://github.com/jmgirard/lordicon/pull/15)

**Goal:** A `li` or `lif` call whose first argument is empty, such as `{{< li "" >}}`, makes no element and gives a render warning, instead of an icon that cannot load.

**Outcome:** Version 0.7.10. `li` and `lif` pass a missing (nil) or empty ("") first argument to `no_first_argument`, which returns `pandoc.Inlines({})` and, in `html:js` formats only, warns `{{< li "" >}} has an empty first argument, so it shows no icon.` with an example call; the missing-argument text is unchanged. Before, `li` wrote `src="https://cdn.lordicon.com/.json"` (CDN 404) and `lif` wrote `src=""`. `_tests/aria.qmd` gained four `empty-*` cases (`""` and `''`, own line and inside a paragraph); `check_aria.py` adds them to `NO_ICON`, matches literal call strings, skips an empty `arg` in `check_spelling`, and `check_warnings` now matches a warning text shared by several cases once per case. README (Customizing) and CHANGELOG 0.7.10 name a call whose only positional argument is empty. DESIGN IP1 and IP5 name the exception (D-005).

**Decisions:** D-005 (an empty first argument gives no element; narrows IP1 and IP5). Milestone-local: a labeled empty call named an image the page never showed, which D-005's reason covers.

**Review:** four-lens fan-out after a claim audit (18 claims, 0 false); 22 findings: 7 fixed (changelog overclaims, IP1 list, a test comment, the D-005 labeled-call note, a missing work-log line), 4 follow-ups to 3 new rows ("Match each warning to its own call", "Warn about a nested shortcode argument", "Say that an empty argument never shifts"), 11 rejected (3 style, 4 false, 4 planned). Corrected the IP1 row's list of exceptions. Graduated candidate row "Warn about an empty first argument". Captured 1 lesson; marked 5 lessons used.
