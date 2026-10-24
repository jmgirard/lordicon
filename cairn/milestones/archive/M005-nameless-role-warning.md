# M005: Warn when a role icon has no name

**Status:** done (2026-10-24, PR #9 https://github.com/jmgirard/lordicon/pull/9)

**Goal:** An icon that the page gives `role="img"` with no accessible name gives a render warning, where before screen readers announced an unnamed image with no visible error.

**Outcome:** `warn_nameless_role` in `lordicon.lua`, called from
`build_element`, gives one warning per call when the kept `role` (first
sorted key per `ascii_lower` name) starts with the token `img` or `image`, and
there is no `label`, no `aria-label`, `aria-labelledby`, `title`, `hidden`,
or `inert` (`NAMES_OR_HIDES`), and no `aria-hidden` equal to `true` in any
case. No attribute changes (IP1). `check_aria.py` adds 17 fixture calls and
`PAGE_ONLY` page-side expectations; 62 cases, 32 warnings. GP5 reworded
(D-004); README, demo home page, CHANGELOG 0.7.5.

**Decisions:** D-004 (GP5 states user ARIA precedence). The plan gate chose
a warning over changing defaults (IP1) and counted `title` as a name.

**Review:** one pass, four-lens fan-out; claim audit corrected 2 comments.
26 findings: 4 fixed (exact `aria-hidden` match, a test comment, two stale
texts), 2 follow-ups, 20 rejected (6 planned, 11 false, 3 edge). New row
"Catch image roles after other tokens"; "Keep values that start with a space"
added at plan and extended. Hygiene graduated "Reword GP5 for user ARIA
precedence" and "Warn when a role icon has no name"; captured 2 lessons.
