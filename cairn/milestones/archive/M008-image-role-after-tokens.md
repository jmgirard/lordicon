# M008: Catch image roles after other tokens

**Status:** done (2026-10-25, PR #12 https://github.com/jmgirard/lordicon/pull/12)

**Goal:** The nameless-role warning reads the first role word that the ARIA specs define, as a browser does, and warns when that role is `img`, `image`, or `graphics-symbol`.

**Outcome:** `warn_nameless_role` in `lordicon.lua` splits the kept `role`
on ASCII whitespace, folds case with `ascii_lower`, takes the first token in
`KNOWN_ROLES` (built from `ROLE_LISTS`: 82 non-abstract WAI-ARIA 1.2 roles,
41 DPUB-ARIA 1.1, 3 Graphics-ARIA 1.0, and `image`; 127 names), and warns
when it is in `IMAGE_ROLES` (`img`, `image`, `graphics-symbol`). Warning text
and attributes unchanged (IP1). Four source notes under `cairn/references/`.
`check_aria.py` adds `AFTER_TOKENS` and `OTHER_FIRST`: 82 cases, 42 warnings.
README, demo home page, DESIGN convention line, CHANGELOG 0.7.7, version 0.7.7.

**Decisions:** none. The plan gate chose `graphics-symbol` over `img` and
`image` only, and the published specs plus `image` over the 1.3 draft roles
(parked row "Know the WAI-ARIA 1.3 draft roles").

**Review:** one return (AC2: the 1.3 note had no role count), then a
four-lens fan-out. 25 findings: 7 fixed (test comment, `[a-z-]+` role split,
README wrap, 1.3 note wording, a planted-defect run), 0 follow-ups, 18
rejected (10 planned, 7 false, 1 style). Claim audit corrected 2 claims.
Hygiene graduated "Catch image roles after other tokens"; captured 1 lesson.
