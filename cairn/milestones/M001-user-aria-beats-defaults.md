# M001: Let user ARIA attributes beat defaults

- **Status:** review
- **Priority:** high
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP2, GP4, GP5
- **Resolves:** —
- **Surface tier:** user-facing — it changes the HTML that every `li` and `lif` shortcode gives
- **Branch/PR:** m001-user-aria-beats-defaults

## Goal

The extension's ARIA defaults give way to ARIA attributes that the user passes.

## Scope

**In:** `build_element` in `_extensions/lordicon/lordicon.lua` skips `aria-hidden="true"` when the user passes `aria-hidden`, `aria-label`, `aria-labelledby`, or `role`. With `label`, the filter adds only the `role` and `aria-label` that the user did not pass. A test document and a check script cover these cases. README, `index.qmd`, and `docs/` show the new rule. The version rises one patch (D-001).

**Out:** A user `src` that gives a second `src`, and mixed-case names such as `Role`, go to the candidate row "Stop duplicate src and ARIA attributes". A render check for other shortcode behavior stays in the candidate row "Add a render check with fixtures". The changelog entry waits for the candidate row "Start a CHANGELOG.md for releases", because the PROFILE `changelog` slot reads as none until that file exists. The `v0.7.2` tag is handed over in the close after the merge.

## Acceptance criteria

- [x] AC1: A `li` or `lif` shortcode with no non-empty `label` can pass a non-empty `aria-hidden`, `aria-label`, `aria-labelledby`, or `role`. Its `<lord-icon>` then has that attribute with the escaped value and no other `aria-hidden` attribute.
- [x] AC2: A shortcode with no non-empty `label`, and with none of those four attributes at a non-empty value, still gets `aria-hidden="true"`.
- [x] AC3: A shortcode with a non-empty `label` gets `role="img"` and an `aria-label` that holds the escaped label. If the user passes a non-empty `role` or `aria-label`, the element keeps the user's value and the extension adds no second attribute with that name.
- [x] AC4: The README "Accessibility" section and the `index.qmd` "Accessibility" section say that a user `aria-hidden`, `aria-label`, `aria-labelledby`, or `role` replaces the `aria-hidden` default. They also say that with `label`, a user `role` or `aria-label` takes the place of the one that `label` adds.
- [x] AC5: `docs/index.html` holds the new Accessibility text and a demo row whose `<lord-icon>` has a user `role="img"` and `aria-label`.
- [x] AC6: `version:` in `_extensions/lordicon/_extension.yml` is one patch above the version on `main` at merge (`0.7.2` at planning, D-001).

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T3
- AC5 → T3
- AC6 → T4

## Tasks

- [x] T1: Add a test `.qmd` and a check script that renders it and reads the attributes of each `<lord-icon>`. Keep the test document out of the demo site, and make sure that `docs/` gets no page for it. Cases: each of the four attributes through `li`, and one through `lif`. A value with `&` and `"`. `aria-label=""` alone and `label=""` alone, which expect the default. A bare icon. An icon with only `class` and `aria-describedby`. `label` alone, `label` with `role`, `label` with `aria-label`, `label` with both, and a label with `&` and `"`. Run the script on the unchanged filter and log which cases fail.
- [x] T2: Change `build_element` (`lordicon.lua:86-93`) so that the `aria-hidden` default yields to the four attributes, and `label` adds only the `role` and `aria-label` that the user did not pass. Run the check script until every case passes.
- [x] T3: Update the README and `index.qmd` Accessibility text. Add a demo row with `role="img"` and `aria-label`, and advise `role="img"` with a user `aria-label`. Run `quarto render` and look at the page in a browser.
- [x] T4: Name the check script in the `verify` slot of `cairn/PROFILE.md`. Raise `version:` one patch, then run the check script and `quarto render` again.

## Work log

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: milestone — the set of user attributes that turn off the default is a design choice, and the README and demo text change with it.
- 2026-10-20: collision check: absorbs candidate "Let user ARIA attributes beat defaults" in full and "Add a render check with fixtures" in part (test document and script for the ARIA cases only). DECISIONS has no overlap. LESSONS.md is empty.
- 2026-10-20: inbox sweep: 0 open issues and 0 open PRs on jmgirard/lordicon.
- 2026-10-20: criteria audit (full mode, fresh Opus reader): 12 findings, all applied. Empty values count as not passed, escape and `lif` probes moved to T1, fixture and check wording moved out of the criteria, the duplicate promise narrowed to `role` and `aria-label`, AC4 covers the `label` case, AC5 states the `docs/` result, the demo row uses `role="img"`, AC6 is relative to `main`, T4 adds the PROFILE `verify` line, T1 keeps the fixture out of `docs/`.
- 2026-10-20: audit finding on duplicate `src` and mixed-case names decided toward the narrower promise: lowercase names only, and the rest became candidate row "Stop duplicate src and ARIA attributes".
- 2026-10-20: question set: which attributes turn off the default — the four named ones. Label clash — the user value wins with no warning. Testing — test document and check script.
- 2026-10-20: plan gate chose the four named attributes over any `aria-*` or `role` because `aria-describedby` alone would unhide an icon with no name; falsified by ARIA guidance or a user report that another attribute must unhide an icon.
- 2026-10-20: plan gate chose a silent user win over a warning because the icon does not fail (GP2); falsified by user reports that `label` had no visible effect.
- 2026-10-20: plan gate chose a test document and check script over checking by eye because the repo has no regression guard; falsified by the script being unable to run where `quarto render` runs.
- 2026-10-20: `cairn_validate` failed "principles slot valid" because DESIGN.md wrote principles as `- IP1 (Name):` and the check reads `- IP1:`. Moved the colon on all 11 principle lines, with no change to their text.
- 2026-10-20: implement started on branch m001-user-aria-beats-defaults. Untracked `.DS_Store` left unstaged.
- 2026-10-20: T1 chose `_tests/aria.qmd` (Quarto skips `_` paths in a project render) and `_tests/check_aria.py` (Python standard library only, no new dependency). The script renders the fixture in a temporary directory with a copy of `_extensions/` and `gift_raw.json`, and identifies each case by its `id`.
- 2026-10-20: T1 run on the unchanged filter: 5 of 15 cases fail (arialabel-li, labelledby-li, role-li, arialabel-lif, arialabel-escaped), each with `aria-hidden` 'true' where none is expected.
- 2026-10-20: T1 finding: Quarto 1.10.19's HTML post-processing keeps only the first of two same-name attributes, so the old filter's duplicates never reach the page and hidden-li and the label-clash cases pass on the unchanged filter. T2 plants a defect to show those cases can fail.
- 2026-10-20: minor amendment: `quarto inspect` listed the `cairn/*.md` files as site inputs, so a root render would publish them to `docs/`. Added `render: ["*.qmd"]` to `_quarto.yml`; `quarto inspect` now lists only the four root pages.
- 2026-10-20: T2 added `ARIA_OVERRIDES` and a `passed` set in `build_element`. The check script reports 15 icons, 15 cases, 0 failures.
- 2026-10-20: T2 planted defect (extension ARIA attributes inserted before the user's): the check reported 10 failures, among them hidden-li, label-role, label-arialabel, and label-both, so those cases can fail. Plant removed, and the check is back to 0 failures.
- 2026-10-20: T3 updated the README and `index.qmd` Accessibility text and added the `role="img" aria-label="Money bag"` demo row. `quarto render` passed. The other pages' diffs in `docs/` come from Quarto 1.10.18 → 1.10.19 (generator tag, syntax CSS hash). On a local server, all three Accessibility icons were defined and ready, and each had an SVG.
- 2026-10-20: T4 named `python3 _tests/check_aria.py` in the PROFILE `verify` slot and raised `version:` to 0.7.2. The check reported 0 failures, and `quarto render` left `docs/` unchanged. DESIGN.md Conventions and Known issues were updated to match the code (corrected M001).
- 2026-10-20: claim audit: 13 claims read, 1 corrected — README.md, index.qmd (the four attributes count only with a non-empty value). The reader re-read the corrected wording and found it TRUE. `docs/` was re-rendered.
- 2026-10-20: implement complete: all four tasks done, the check reports 0 failures, and `quarto render` passes. Status set to review.

## Decisions

## Review

Review pass 1, 2026-10-20, branch head 774fd4b, synced with origin/main d201f39.

- AC1 evidence: `python3 _tests/check_aria.py` exit 0, "15 icons read, 15 cases, 0 failures". The cases hidden-li (`aria-hidden` 'false'), arialabel-li, labelledby-li, role-li, arialabel-lif, and arialabel-escaped (value `Tom & "Jerry"` read back unchanged) have the user attribute and no `aria-hidden` 'true'. The script fails on any attribute name that appears twice on one element.
- AC2 evidence: same run. The cases bare, empty-arialabel, empty-label, and describedby (`class` + `aria-describedby`) have `aria-hidden` 'true'.
- AC3 evidence: same run. The case label has `role` 'img' and `aria-label` 'Bell'. label-role keeps 'presentation', label-arialabel keeps 'Other', and label-both keeps both user values. label-escaped has `aria-label` `Tom & "Jerry"`. No attribute name appears twice. The T2 planted defect made these cases fail (work log).
- AC4 evidence: the README Accessibility section (lines 12 to 15 of the section) and `index.qmd:59` name the four attributes as replacing the `aria-hidden` default when non-empty. Both also say that with `label`, a user `role` or `aria-label` "replaces the one `label` would add".
- AC5 evidence: `docs/index.html` holds "Passing a non-empty" once and the element `<lord-icon src="https://cdn.lordicon.com/ibydboev.json" aria-label="Money bag" role="img">`, which has no `aria-hidden`.
- AC6 evidence: `git show origin/main:_extensions/lordicon/_extension.yml` reads `version: 0.7.1`, and the branch reads `version: 0.7.2`.
- Gate: `cairn_validate` passed all checks. `cairn_impact --changed` listed 5 IP1 references. IP1's text is unchanged on the branch (the plan commit only moved its colon), and the references agree with it. `quarto render` exit 0 left `docs/` unchanged. `version:` is the only marker that release-walk names. Changelog slot reads as none (`CHANGELOG.md` absent).
- spawned: diff-bug, blame-history, prior-review, ripple
