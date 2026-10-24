<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M005: Warn when a role icon has no name

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP5, GP2, IP1, IP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — a render warning that Quarto authors see   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m005-nameless-role-warning   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

An icon that the page gives `role="img"` with no accessible name gives a render warning, where before screen readers announced an unnamed image with no visible error.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** One warning per shortcode call from `build_element` in
`_extensions/lordicon/lordicon.lua`. It fires when the attributes the page
keeps give the icon a `role` whose first token (split at ASCII whitespace) is
`img` or `image` in any ASCII letter case, and none of these: an
`aria-hidden` whose value is `true` in any ASCII letter case; an
`aria-labelledby`, `aria-label`, or `title`; a `hidden` or `inert`. Key names
match in any ASCII letter case. For keys that differ only in letter case, the
check reads the value the page keeps: the first such key in the filter's byte
order. A quoted value that is empty, holds only spaces, or starts with a space
never reaches the filter (probe 2026-10-24), so a name key that is present
counts as a name. The warning names the call and says how to fix it. No
attribute changes (IP1). Fixture calls and expectations in `_tests/aria.qmd`
and `_tests/check_aria.py`. GP5 in `cairn/DESIGN.md` reworded to state user
ARIA precedence (D-004), plus DESIGN Conventions and Known issues text for the
warning. README and demo home page Accessibility text, `CHANGELOG.md` 0.7.5,
`version: 0.7.5`, and the re-rendered `docs/`.

**Out:** A check that an `aria-labelledby` id exists on the page (the filter
sees one call, not the page) → not planned. Warnings for other roles that need
a name, such as `button` → not planned. Values that start with a space →
candidate row "Keep values that start with a space". Attribute sorting and
non-HTML output checks → candidate row "Add a render check with fixtures".

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: Each of these calls in `_tests/aria.qmd` gets exactly one
      nameless-role warning, besides any warning it already gets, and that
      warning names the call, says the icon has an image role but no name, and
      says how to fix it: (a) `role=img` alone; (b) `ROLE=IMG`; (c)
      `role=image`; (d) `role="img presentation"`; (e) `role=img
      aria-hidden=false`; (f) `role=img aria-hidden=true ARIA-HIDDEN=false`,
      where the page keeps `false`; (g) the existing calls whose kept role is
      `img`: `clash-role`, `clash-two`, and `clash-empty`. Shown by
      `python3 _tests/check_aria.py` exiting 0, which matches each expected
      warning to exactly one line of the render log.
- [x] AC2: No call in `_tests/aria.qmd` other than the AC1 calls gets the
      nameless-role warning. The fixture holds `role=img` calls with
      `aria-label`, `ARIA-LABELLEDBY`, `title`, `Title`, `label`, `hidden`,
      `aria-hidden=true`, and `Aria-Hidden=TRUE`, plus
      `role="presentation img"` and `role=img Role=presentation`, where the
      page keeps `presentation`. Shown by `python3 _tests/check_aria.py`
      exiting 0; its log check counts every lordicon warning in the render.
- [x] AC3: The warning code adds no attribute and changes none: it only reads
      the call's keys and calls `quarto.log.warning`, and every case that
      `_tests/check_aria.py` holds on the default branch passes its page and
      filter checks with the expected values the default branch gives it.
- [x] AC4: GP5 in `cairn/DESIGN.md` states that a non-empty user
      `aria-hidden`, `aria-label`, `aria-labelledby`, or `role` in any letter
      case turns the `aria-hidden` default off, and that each attribute
      `label` adds yields to the user's own, marked with D-004, which
      `cairn/DECISIONS.md` holds. The DESIGN Conventions section names the
      new warning.
- [x] AC5: The README Accessibility section and the Accessibility section of
      `index.qmd` say when the render gives this warning; `CHANGELOG.md` has a
      `## 0.7.5` section with an entry for it; `_extension.yml` reads
      `version: 0.7.5`; `docs/` is re-rendered from the changed pages.
- [x] AC6: The `verify` slot of `cairn/PROFILE.md` is clean on the review
      head.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T3
- AC5 → T3
- AC6 → T2, T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [x] T1: Add a "Role img with no name" section to `_tests/aria.qmd` with the
      AC1 (a)-(f) calls and the AC2 calls, each with its own icon code, since
      a warning names only `{{< li CODE >}}`. In `_tests/check_aria.py`, add
      their `CASES` entries and the AC1 warnings to `WARNED`, (g) included.
      Give the new clash calls their letter-case warnings and `TWICE` counts.
      `dict(attrs)` keeps the last duplicate while the page keeps the first,
      so assert a kept clash value with a page-only expectation. Run the
      check and see it fail on the missing warnings only.
- [x] T2: Add `warn_nameless_role(call, ...)` to `lordicon.lua` and call it
      from `build_element` (`lordicon.lua:240`) after the attributes are
      known, reading user keys by `ascii_lower`. Spell ASCII whitespace as
      `[\t\n\f\r ]`, not `%s`. Update the header comment
      (`lordicon.lua:1-16`). Run the `verify` slot.
- [x] T3: Reword GP5 (D-004, written by the plan) and add the warning to
      Conventions and Known issues in `cairn/DESIGN.md`. Update README and
      `index.qmd` Accessibility text, add `CHANGELOG.md` 0.7.5, raise
      `_extension.yml` to 0.7.5, run `quarto render`, check the changed demo
      page in a browser, and commit `docs/` with its sitemap.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: tier check: not run — work named at the question set.
- 2026-10-24: idea vet: no concern; an element with an image role needs an accessible name, which `aria-labelledby`, `aria-label`, or `title` gives, a nameless image fails with no visible error (GP2), and a warning changes no attribute (IP1).
- 2026-10-24: question set: which candidate to plan — "Warn when a role icon has no name"; also reword GP5 in this milestone — yes.
- 2026-10-24: collision check: absorbed candidate rows "Warn when a role icon has no name" and "Reword GP5 for user ARIA precedence" (both from the M001 review); M001 (archived) shipped the ARIA precedence this warning builds on; no D-entry overlap.
- 2026-10-24: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-24: lessons used: 2026-10-20 (M001) Quarto keeps the first of two ASCII-equal attribute names; 2026-10-24 (M003) Lua `%s` follows the locale; 2026-10-20 (M002) `quarto render` rewrites `docs/sitemap.xml`.
- 2026-10-24: plan gate chose a warning over adding `aria-hidden` or dropping the role because IP1 forbids rewriting user attributes; falsified by a user decision that changes IP1.
- 2026-10-24: plan chose to count `title` as a name because the accessible-name computation falls back to it; falsified by a major screen reader that announces a `role="img"` element with only a `title` as unnamed.
- 2026-10-24: plan chose to read only the first role token over any token, a narrower warning; falsified by a browser that maps `role="x img"` to an image role and a user report of such a nameless icon.
- 2026-10-24: release-shaped tripwire: not hit; the 0.7.5 version rise at merge follows D-001 and is no release window.
- 2026-10-24: plan probe: a render keeps the first of `role`/`Role` in byte order; a quoted value that is all spaces or starts with a space reaches the filter as no key (`label=" Bell "` stays `aria-hidden`), so the blank-name cases left the plan and the candidate row "Keep values that start with a space" holds the rest.
- 2026-10-24: criteria audit (full mode, fresh Opus reader): 12 findings. Fixed: unreachable blank-value cases (1, 2) dropped; AC1 "exactly one" scoped to this warning (3); fix advice added (4); `WARNED` wording replaced by the log match (5); fixture traps moved into T1 (6); (f) reworded as the kept-role calls (7); letter-case, aria-hidden clash, and first-token probes added (8); AC3 narrowed to what the code does plus the fixture (9); GP5 "non-empty" added and D-004 written at plan (10). No finding on AC5 and proportionality; AC6's browser check stands as the profile's verify slot (12). Accepted its point that `hidden` and `inert` also remove an icon: the warning skips them.
- 2026-10-24: implement start: branch `m005-nameless-role-warning` cut from main at 576fa52; untracked `.DS_Store` left unstaged.
- 2026-10-24: T1 done: 17 fixture calls in two sections (one icon code each), a `named-inert` case beside the AC2 list to cover the `inert` branch, `PAGE_ONLY` expectations for kept clash values; the check fails only on the 9 missing nameless-role warnings (23 of 32 warnings, all attribute checks pass).
- 2026-10-24: warning text chosen: `gives the icon role="<kept value>" but no name, so a screen reader announces an image without saying what it shows. Add a label, such as label="Bell". If the icon is only decoration, pass aria-hidden="true" instead.`; the aria-hidden advice works even where a user `aria-hidden=false` would keep a role-less icon shown.
- 2026-10-24: T2 done: `warn_nameless_role` in `lordicon.lua`, called after `warn_label_case`; it returns early on a non-empty `label`, reads the first sorted key per `ascii_lower` name, and skips on `aria-label`, `aria-labelledby`, `title`, `hidden`, `inert` (table `NAMES_OR_HIDES`) or a trimmed `aria-hidden` of `true`. `check_aria.py`: 0 failures, 32 of 32 warnings. Planted defects turned it red: dropping `inert` (33 warnings), reading the last duplicate (clash-role, clash-two, nameless-hidden-clash lost). `quarto render` exit 0, no lordicon warning on the demo site, sitemap restored; no demo page changed, so no browser check.
- 2026-10-24: T3 done: GP5 reworded (D-004), Conventions, Known issues, and Architecture lines in DESIGN.md; README and `index.qmd` Accessibility paragraph; CHANGELOG 0.7.5; `version: 0.7.5`. `check_aria.py` 0 failures; `quarto render` exit 0 with no lordicon warning; `docs/` committed with its sitemap. Browser at http://localhost:8765/: `lord-icon` defined, 17 of 17 icons hold an SVG, the new paragraph shows.
- 2026-10-24: the simple-english lint hook flagged 25 older README sentences; fixed only the hits in the new paragraph (a long sentence, a trailing condition) and left the rest, which predate M005.
- 2026-10-24: claim audit: 14 claims read, 2 corrected — `_extensions/lordicon/lordicon.lua` (first-token comment now says `role="bogus img"` is not caught), `_tests/check_aria.py` (`dict(attrs)`, not the parser, keeps the last duplicate); the reader re-read both as true. `check_aria.py` 0 failures after the edits.
- 2026-10-24: implement complete; status set to review.
- 2026-10-24: step-7 approval: m005-nameless-role-warning approved for merge

## Decisions
<!-- owner: implement / review · append-only; milestone-local -->

## Review
<!-- owner: review · exclusive -->

Evidence, 2026-10-24, on `1f4facb` (branch level with main at 576fa52):

- AC1: `python3 _tests/check_aria.py` exit 0 (62 of 62 cases on page and filter, 32 of 32 warnings, 0 failures); its log check matches each expected warning to exactly one log line. A separate render of the fixture gives the nameless-role warning once each for `nrimg` (`role="img"`), `nrupper` (`IMG`), `nrimage` (`image`), `nrfirst` (`img presentation`), `nrshown`, `nrhidclash`, `clashrole`, `clashtwo`, `clashempty`; each text holds the call, "but no name", and the fix `Add a label, such as label="Bell".`
- AC2: the same render's log holds the nameless-role warning for those 9 calls and no other; `check_aria.py` exit 0 with its total-count check (32 read, 32 expected). `_tests/aria.qmd` holds all 10 AC2 calls (`named-arialabel`, `-labelledby` with `ARIA-LABELLEDBY`, `-title`, `-title-upper`, `-label`, `-hidden-attr`, `-aria-hidden`, `-aria-hidden-upper` with `Aria-Hidden=TRUE`, `-first-presentation`, `-role-clash`); the page keeps `role="presentation"` for `named-role-clash` (`PAGE_ONLY` check passes).
- AC3: `warn_nameless_role` reads `keys` and `kwargs` and calls only `quarto.log.warning` (no `attrs` use, no write to `kwargs`). `git diff main -- _tests/check_aria.py` removes one line, the `for name, want in CASES[case].items()` loop head now reading the merged `expected`; no `CASES` entry of a main case is removed or changed, and all 62 cases pass on page and filter.
- AC4: `cairn/DESIGN.md:127` GP5 names a non-empty user `aria-hidden`, `aria-label`, `aria-labelledby`, or `role` in any letter case and says each `label` attribute yields to the user's own, marked `(corrected M005, D-004)`; `cairn/DECISIONS.md:24` holds D-004; Conventions line ending `name (M005).` names the warning.
- AC5: README.md:125 and index.qmd:61 describe when the render warns; `CHANGELOG.md` has `## 0.7.5` with the entry; `_extension.yml` reads `version: 0.7.5`; `quarto render` on the review head leaves `docs/` unchanged and `docs/index.html:290` holds the paragraph.
- AC6: verify slot on `1f4facb`: `check_aria.py` exit 0; `quarto render` exit 0 with no lordicon warning; browser at http://localhost:8765/: `lord-icon` defined, 17 of 17 icons hold an SVG.
- Gate: `cairn_validate.py` all checks passed; `cairn_impact.py --changed` lists GP5 and IP1 references, all history records or this milestone's, except ROADMAP row "Reword GP5 for user ARIA precedence", which hygiene graduates; one version marker (`_extension.yml` 0.7.5); verify render green; CHANGELOG 0.7.5 entry present.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the `aria-hidden` check trims whitespace beyond the scope, so `aria-hidden="true "` (kept as written on the page) silences the warning though Chromium is believed to compare the exact value — fix now (trim dropped), fixed 74defa8.
- diff-bug #2: `named-title-upper` repeats the key case-folding path that `named-labelledby` and `nameless-upper` already run — reject: planned change (AC2 names `Title`).
- diff-bug #3: `clash-role`, `clash-two`, `nameless-hidden-clash`, and `named-role-clash` each test the first-sorted-key rule — reject: planned change (AC1 (f)-(g) and AC2 name them).
- diff-bug #4: the comment above `SHOWN` in `check_aria.py` repeats what the case names show — fix now (comment removed), fixed 74defa8.
- diff-bug #5: the five `named-*` name and hide cases run one loop over `NAMES_OR_HIDES` — reject: planned change (AC2 names each; each guards its own table entry, as the planted `inert` defect showed).
- diff-bug #6: `named-role-clash` asserts the kept `role` on the page only — reject: false; `dict(attrs)` keeps the last duplicate, so the filter side cannot show the kept value, which is what `PAGE_ONLY` is for.
- diff-bug #7: `Label` with `role=img` fires both warnings, untested — reject: false; the probe shows the right output and the path is plain `role=img`.
- diff-bug #8: the warning prints the kept role raw, so `role="img "` shows a trailing space — reject: edge; a quoted role ending in a space is outside documented and common use, and the effect is warning text only.
- diff-bug #9: README, `index.qmd`, and CHANGELOG name only `role="img"` or `role="image"`, though `IMG` and `"img presentation"` also warn — reject: false; the statements are true, and the `"x img"` gap is in the code comment.
- diff-bug #10: `ascii_lower` here against `pandoc.text.lower` in the clash warning — reject: false; no non-ASCII letter lowercases into the six names read.
- diff-bug #11: `table.sort` follows the collation locale — reject: false; the check reads the same sorted `keys` the element is written from, so it matches the page in any locale.
- ripple #1: ROADMAP row "Warn when a role icon has no name" still open — reject: planned change (post-merge hygiene graduates it).
- ripple #2: ROADMAP row "Reword GP5 for user ARIA precedence" still open — reject: planned change (post-merge hygiene graduates it).
- ripple #3: ROADMAP row "Add a render check with fixtures" lists what `check_aria.py` covers without the new warning — fix now, fixed 74defa8.
- ripple #4: with `role=img label=" Bell "` the label is lost and the warning tells the user to add a label — follow-up, absorbed into "Keep values that start with a space".
- ripple #5: DESIGN Conventions line on the `aria-hidden` default omits "non-empty", which GP5 and README state — fix now, fixed 74defa8.
- blame-history #1: the check reads only the first role token, but ARIA has browsers use the first role they know, so `role="bogus img"` gives an unnamed image with no warning — follow-up, new row "Catch image roles after other tokens".
- blame-history #2: browsers ignore `role="image"`, so the warning is false for it — reject: false; ARIA 1.3 makes `image` the primary role with `img` its synonym (Mozilla bug 1829269, fixed in Firefox 116; WebKit bug 224615 fixed).
- blame-history #3: `table.sort` follows the locale, so the first sorted key may not be the page's — reject: false; `quarto pandoc lua` reports the collation locale `C` under `LC_ALL=en_US.UTF-8` (plan probe), and the check reads the same order the element is written in.
- blame-history #4: `ascii_lower` misses a key such as `İnert` that Quarto folds to `inert` — reject: edge; a non-ASCII letter in an ARIA or HTML attribute name is outside documented and common use, and the effect is a spurious warning.
- blame-history #5: the header comment omits the `aria-label`, `aria-labelledby`, and `title` exemptions — reject: false; "no name" covers them.
- blame-history #6: the render changed `docs/sitemap.xml` — reject: planned change (the M002 lesson commits the sitemap with a re-render).
- prior-review #1: the "byte order" claim fails under a non-C locale (M004 review) — reject: false; same probe as blame-history #3.
- prior-review #2: grouping by `ascii_lower` reverses M004's choice of `pandoc.text.lower` — reject: edge; same input as blame-history #4, and M004's choice concerned the clash warning, not these six names.
- prior-review #3: with `Label="Bell" role=img` the advice says to add a label the user wrote — reject: false; the label-case warning fires beside it, and both point to the lowercase `label` the icon needs.
- prior-review #4: the header comment omits the name exemptions (M003 checked header accuracy) — reject: false; same as blame-history #5.
- Settled: 26 findings; 4 fix now (`74defa8`), 2 follow-up, 20 rejected (6 planned change, 11 false, 3 edge). Snapshot files changed: none.
- Re-verify after the fixes, on `d1674fd`: `check_aria.py` 0 failures; `quarto render` exit 0 and `docs/` unchanged.
