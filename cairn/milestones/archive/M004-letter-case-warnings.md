# M004: Warn about keys in another letter case

**Status:** done (2026-10-24, PR #8 https://github.com/jmgirard/lordicon/pull/8)

**Goal:** A shortcode key whose effect depends on its letter case gives a render warning, where before it failed with no visible error.

**Outcome:** `build_element` in `lordicon.lua` gives one warning per call
from `warn_case_clashes`, which groups forwarded keys by `pandoc.text.lower`
(the page keeps one value per group), and one from `warn_label_case` for keys
such as `Label`. `check_minified` matches `colors`, `stroke`, and `state` with
`ascii_lower` and names each key as written. All keys still pass through
(IP1). `check_aria.py` lists several warnings per case (`WARNED` text sets),
allows exact duplicate counts (`TWICE`), and adds `_tests/minified.json`; 45
cases, 21 warnings. README, CHANGELOG 0.7.4, DESIGN Conventions.

**Decisions:** none. The plan gate chose a warning for `Label` over treating
it as `label`, and `pandoc.text.lower` over ASCII-only folding, because the
page also drops non-ASCII clashes.

**Review:** one pass, four-lens fan-out; claim audit corrected 2 claims. 24
findings: 8 fixed, 9 rejected (2 edge), 3 follow-ups, 4 split. New rows "Sort
keys by byte, not by locale", "Name the call in the Minified warning", and
"Match Quarto's case folding in warnings". Hygiene graduated "Warn on keys
that differ only in case" and "Match Minified-check keys in any case",
narrowed "Add a render check with fixtures", and corrected the M001 lesson.
