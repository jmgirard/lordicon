# M008: Catch image roles after other tokens

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP3, GP2, GP4
- **Resolves:** —
- **Surface tier:** user-facing — it changes which shortcode calls give a render warning, and the README and demo text that describe it
- **Branch/PR:** m008-image-roles

## Goal

The nameless-role warning reads the first role word that the ARIA specs define, as a browser does, and warns when that role is `img`, `image`, or `graphics-symbol`.

## Scope

**In:** In `warn_nameless_role` (`_extensions/lordicon/lordicon.lua:213`),
split the kept `role` value on ASCII whitespace, skip each token that is not
in a known-role list (compared with ASCII case folding), and warn when the
first known token is `img`, `image`, or `graphics-symbol`, under the name and
hiding conditions that 0.7.5 set. The known-role list holds the non-abstract
roles of WAI-ARIA 1.2 (deprecated ones included), the roles of DPUB-ARIA 1.1,
the roles of Graphics-ARIA 1.0, and `image` from the WAI-ARIA 1.3 draft. One
source note per spec under `cairn/references/`. New fixtures in
`_tests/aria.qmd` and `_tests/check_aria.py`. README, `index.qmd`,
CHANGELOG 0.7.7, version 0.7.7, the DESIGN.md convention line, the Lua
comment, and a re-render of `docs/`.

**Out:**
- Other WAI-ARIA 1.3 draft roles, such as `mark`, `comment`, and
  `suggestion`: left out at the plan gate, so `role="mark img"` warns. The
  `[parked]` candidate row "Know the WAI-ARIA 1.3 draft roles" holds it.
- Other image-like roles that need no name, such as `doc-cover`: no warning,
  because the spec does not require a name.
- Role values with a tab, a newline, or a leading space: a render cannot
  carry them (Pandoc expands tabs, and Quarto drops a value that starts with
  a space), so no fixture tests them.
- Any change to an emitted attribute (IP1): the warning is the whole change.

## Acceptance criteria

- [x] AC1: In a render of `_tests/aria.qmd`, `python3 _tests/check_aria.py`
      exits 0 with every case it had before this milestone unchanged, and
      with these new calls, each without `label` and without any name or
      hiding attribute unless one is named here. Each of these gives one
      nameless-role warning that quotes the role value as written:
      `role="bogus img"`, `role="landmark img"`, `role="BOGUS Img"`,
      `role="bogus  img"` (two spaces), `role="bogus image"`,
      `role="graphics-symbol"`, `role="graphics-symbol img"`,
      `role="bogus graphics-symbol"`, and `role="Graphics-Symbol img"`.
      Each of these gives none: `role="bogus presentation img"`,
      `role="button img"`, `role="doc-cover img"`,
      `role="graphics-document img"`, `role="bogus"`, `role` set to `bogus`,
      U+00A0, and `img`, `role="bogus graphics-symbol" aria-label="Bell"`,
      and `role="graphics-symbol" aria-hidden=true`.
- [x] AC2: The filter's known-role list holds exactly the role names that
      four source notes under `cairn/references/` record: the non-abstract
      roles of WAI-ARIA 1.2, the roles of DPUB-ARIA 1.1, the roles of
      Graphics-ARIA 1.0, and `image` from the WAI-ARIA 1.3 draft. Each note
      names the spec's URL, the section it copied, the date it was read, and
      its role count.
- [x] AC3: The README, the demo home page (`index.qmd`), and a CHANGELOG
      0.7.7 entry say that the render reads the first role that the ARIA
      specs define and warns for `img`, `image`, and `graphics-symbol`. The
      DESIGN.md convention line on the warning and the comment above the
      token scan in `lordicon.lua` say the same. `_extension.yml` reads
      `version: 0.7.7`, and `docs/` is re-rendered from the changed
      `index.qmd`.

## Coverage

- AC1 → T2, T3
- AC2 → T1, T3, T5
- AC3 → T4

## Tasks

- [x] T1: Write the four source notes from `templates/source-note.md`
      (`wai-aria-1-2.md`, `dpub-aria-1-1.md`, `graphics-aria-1-0.md`,
      `wai-aria-1-3.md`, the last recording only `image`), each with its
      URL, section, read date, and role list with count, and add their
      `INDEX.md` lines.
- [x] T2: Add the AC1 calls to `_tests/aria.qmd` and their expectations to
      `_tests/check_aria.py` (`CASES` and `WARNED`). Run the check and see
      the new warning cases fail before the filter changes.
- [x] T3: In `lordicon.lua`, add the known-role table built from the T1
      notes and replace the first-token match (line 236) with a scan that
      splits on ASCII whitespace and takes the first known token. Run the
      check green. Compare the table with the notes' lists by a one-off
      script and record the result in the work log.
- [x] T4: Update the README (line 125), `index.qmd` (line 61), the
      DESIGN.md convention line (line 57), the Lua comment, a CHANGELOG
      0.7.7 entry, and `_extension.yml` to 0.7.7. Run `quarto render`, keep
      the re-rendered `docs/`, and look at the home page in a browser.
- [x] T5: State the role count on `cairn/references/wai-aria-1-3.md`
      (review return 1).

## Work log

- 2026-10-25: created by /milestone-plan.
- 2026-10-25: tier check: milestone — it changes which calls give a render warning and needs a choice of role lists.
- 2026-10-25: idea vet: the row's first-known-token approach misses the Graphics-ARIA fallback `role="graphics-symbol img"`, whose role needs a name — the set chose to warn for `img`, `image`, and `graphics-symbol`; the list's source (published specs or the 1.3 draft) — the set chose published specs plus `image`.
- 2026-10-25: lessons used: 2026-10-24 (M003) on `%s` and the locale; 2026-10-24 (M005) on Quarto dropping values that start with a space; 2026-10-20 (M002) on `docs/sitemap.xml` after a render.
- 2026-10-25: collision check: absorbs candidate row "Catch image roles after other tokens"; extends M005 (done), consistent with D-004; no D-entry rejects it. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-25: plan gate chose warning for `img`, `image`, and `graphics-symbol` over `img` and `image` only, because Graphics-ARIA 1.0 requires a name for `graphics-symbol` and recommends `role="graphics-symbol img"`; falsified by a screen reader that does not announce `graphics-symbol` as an image.
- 2026-10-25: plan gate chose the published role lists plus `image` over adding the WAI-ARIA 1.3 draft roles, because the draft can change; falsified by a user report of a false warning for a 1.3 role placed first.
- 2026-10-25: criteria audit (full mode, fresh Opus reader): 6 findings, all fixed — docs claim narrowed from browsers to the ARIA specs; notes name URL, section, date, and count; deprecated roles kept and the 1.3 note records only `image`; six AC1 cases added (`bogus image`, U+00A0, a name and a hiding attribute with `graphics-symbol`, `Graphics-Symbol`, `button img`) and untestable separators moved to Out; DESIGN line and Lua comment added to AC3; the warning quotes the value as written. A committed comparison script was not added: the list is a fixed table checked once at T3 and at review.
- 2026-10-25: version and changelog: patch bump to 0.7.7 per D-001, as 0.7.5 did for the first version of this warning.
- 2026-10-25: implement started on branch m008-image-roles; the untracked `.DS_Store` stays unstaged.
- 2026-10-25: T1 done: four source notes and INDEX lines. A parse of the fetched specs gives 82 non-abstract WAI-ARIA 1.2 roles (12 abstract left out), 41 DPUB-ARIA 1.1 roles, 3 Graphics-ARIA 1.0 roles, and `image` from the 1.3 draft: 127 names.
- 2026-10-25: T2 done: 17 fixture calls (9 warn, 8 do not). Before the filter change the check failed only on the 9 new warnings (33 of 42 read), and every attribute case passed, so two spaces and U+00A0 reach the page as written. The U+00A0 was written by a one-line Python replace, because the Edit tool turned it into a space.
- 2026-10-25: T3 done: `ROLE_LISTS`, `KNOWN_ROLES`, and `IMAGE_ROLES` in `lordicon.lua`, and a token scan replacing the first-token match. Check: 82 cases, 42 warnings, 0 failures. A one-off script found the Lua table, the notes, and a fresh parse of the saved specs equal at 127 names each. Choice: the lists are kept as one string per spec, so each can be compared with its note line for line.
- 2026-10-25: T4 done: README, `index.qmd`, CHANGELOG 0.7.7, DESIGN.md convention line (corrected M008), the Lua comment, `_extension.yml` 0.7.7. Check green (82 cases, 42 warnings); `quarto render` re-rendered `docs/`, sitemap kept per the M002 lesson. Served `docs/` at localhost: 17 of 17 home-page icons drew an SVG, no console errors. The style hook still flags older README lines this milestone does not touch.
- 2026-10-25: claim audit: 22 claims read, 2 corrected — CHANGELOG.md, README.md, index.qmd (the role rule now says non-abstract, and "announces an image" became "cannot say what the icon shows"), lordicon.lua (the IMAGE_ROLES comment cites the specs' name requirement, not screen readers). The same reader re-read both and found them true; `docs/index.html` re-rendered.
- 2026-10-25: all tasks done, check green; status set to review.
- 2026-10-25: review return 1: AC2 — `cairn/references/wai-aria-1-3.md` names no role count; status back to in-progress.
- 2026-10-25: minor amendment: T5 added for review return 1, Coverage AC2 → T1, T3, T5. T5 done: the 1.3 note now states "Roles recorded, 1: `image`"; validate green; no code changed, so the check result stands. Status set to review.

## Decisions

## Review

- AC1: `python3 _tests/check_aria.py` on the branch head exits 0: page and filter 82 of 82 cases, 42 of 42 warnings, gfm 0 warnings. `git diff main...HEAD -- _tests` removes no line (48 added), so every earlier case stands unchanged. The 9 warning calls are in `AFTER_TOKENS`, each matched to one warning quoting `role="<value>"`; the 8 silent calls are in `OTHER_FIRST` and the two `named-symbol-*` cases, and the log-count check (42 read, 42 expected) fails on any extra warning. The 9 warning cases failed on the filter before T3 (work log, T2).
- AC2 (pass 1, not ticked): a scratchpad script compared the Lua `ROLE_LISTS`, the four notes' lists, and a fresh parse of the saved specs: 127 names each, no difference. URL, section, and read date are on all four notes, and counts are on three (82, 41, 3). `wai-aria-1-3.md` states no role count, so AC2 fails as written.
- Pass 2: since pass 1 only `cairn/` files changed (`git diff 086a6dc..HEAD --name-only`), so the AC1 run stands for the code under review.
- AC2: the comparison script again finds the Lua table, the notes, and the specs at 127 names each with no difference. Each note names its URL, section (§5.4 and §7.1; §3.1; §4.1; `#image`), read date 2026-10-25, and count (82, 41, 3, and "Roles recorded, 1" on `wai-aria-1-3.md`).
- AC3: README.md:125-130, index.qmd:61, and CHANGELOG.md `## 0.7.7` (lines 7-8) say the render reads the first word of `role` that names a non-abstract role in the ARIA specs and warns for `img`, `image`, and `graphics-symbol`. DESIGN.md:57 names the three roles and `KNOWN_ROLES`. The comment above the token scan in `lordicon.lua` states the first-non-abstract-role rule and points to `IMAGE_ROLES`, whose comment names the three roles. `_extension.yml` line 3 reads `version: 0.7.7`. `docs/index.html` holds the new sentence once and was committed in 086a6dc, the same commit as the last `index.qmd` change.
- Gate: `cairn_validate.py` all checks passed (exit 0); `cairn_impact.py --changed` reports no changed principle. Version markers: the release-walk names only `_extension.yml`, which reads 0.7.7. Verify render: `check_aria.py` renders `aria.qmd` green on the code under review, and `quarto render` ran at 086a6dc with no later code change. Changelog: `CHANGELOG.md` has a `## 0.7.7` section for this change.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the warning text says a screen reader "announces an image", which the docs no longer claim for `graphics-symbol` — reject (false): Graphics-AAM 1.0 §7.2 maps `graphics-symbol` to the image role in MSAA, UIA, ATK, and AXAPI.
- diff-bug #2: `named-symbol-label` and `named-symbol-hidden` re-test the name and hiding branch — reject (planned change): AC1 names both calls.
- diff-bug #3: `graphics-symbol img` runs the same path as `graphics-symbol` — reject (planned change): AC1 names it as the spec's fallback form.
- diff-bug #4: `Graphics-Symbol img` repeats the case-folding path of `BOGUS Img` — reject (planned change): AC1 names it.
- diff-bug #5: `bogus image` repeats the path of `bogus img` — reject (planned change): AC1 names it.
- diff-bug #6: `bogus  img` adds no filter path — reject (planned change): AC1 names it.
- diff-bug #7: `button img` overlaps `bogus presentation img` — reject (planned change): AC1 names both.
- diff-bug #8: the test comment says the role is the one a browser "knows", not the filter's list — fix now, fixed d67fa89.
- diff-bug #9: README.md line 130 runs to 145 characters among lines wrapped near 80 — fix now, fixed d67fa89.
- diff-bug #10: the docs do not say that `image` comes from the WAI-ARIA 1.3 draft — reject (false): the text lists `image` apart from the three specs ("plus `image`") and states nothing wrong.
- diff-bug #11: `ROLE_LISTS` splits on `[^\n ]+`, so a later tab would join two names — fix now: the split now matches `[a-z-]+`, fixed d67fa89.
- diff-bug #12: the absorbed candidate row is still in the ROADMAP — reject (planned change): post-merge hygiene graduates a row marked `started M008`.
- blame-history #1: `role="doc-cover img"` gives no warning, though a browser without DPUB-ARIA uses `img` — reject (planned change): Scope Out names `doc-cover`, and the docs state the WAI-ARIA rule, not each browser's support.
- blame-history #2: the choice to leave out the 1.3 draft roles has no D-entry — reject (false): a deferral lives in the ROADMAP, here the parked row "Know the WAI-ARIA 1.3 draft roles", not in DECISIONS.md.
- blame-history #3: pages with a nameless `role="<other> img"` or `graphics-symbol` now warn — reject (planned change): the Goal calls for it and CHANGELOG 0.7.7 states it.
- blame-history #4: the new README and index.qmd prose is not wrapped like the M005 text — README fixed with diff-bug #9; index.qmd reject (style): its paragraphs are one line each throughout.
- blame-history #5: `wai-aria-1-3.md` says the warning covers `image` since 0.7.5, true only for a first-token `image` — fix now, fixed d67fa89.
- prior-review #1: no planted-defect run is recorded for the new scan — fix now: a plant that stops the scan at any `IMAGE_ROLES` token (skipping `KNOWN_ROLES`) turned the check red, 47 warnings against 42 expected, and the file was restored. After d67fa89 the check is green again (82 cases, 42 warnings) and the role comparison still finds 127 equal names.
- prior-review #2: the scan folds case with `ascii_lower`, while M004 chose `pandoc.text.lower` for clashes — reject (false): every role name is lowercase ASCII, and `pandoc.text.lower` would only add matches through non-ASCII letters such as U+212A KELVIN SIGN, which an ASCII role match does not accept.
- prior-review #3: README line 130 breaks the wrap — fixed with diff-bug #9.
- prior-review #4: `graphics-symbol` warnings rest on a spec whose change log names a `group` superclass — reject (planned change): the plan gate chose it, and Graphics-AAM maps the role to image.
- ripple #1-3: the notes say the table "takes the 82/41/3 names" though it holds 127 — reject (false): each note says the table takes that note's names, which it does.
- ripple #4: the ROADMAP candidate row still describes the bug as open — reject (planned change): hygiene graduates it.
