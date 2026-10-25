# M011: Warn about an empty first argument

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP3, IP5, GP2, GP4
- **Resolves:** —
- **Surface tier:** user-facing — it changes what a shortcode call renders and warns
- **Branch/PR:** m011-empty-first-argument

## Goal

A `li` or `lif` call whose first argument is empty, such as `{{< li "" >}}`, makes no element and gives a render warning, instead of an icon that cannot load.

## Scope

**In:** `li` and `lif` in `_extensions/lordicon/lordicon.lua` treat a first argument that stringifies to `""` like a missing one: they return no element, and in `html:js` formats they warn with text for an empty argument. Four fixture cases in `_tests/aria.qmd` and their checks in `_tests/check_aria.py`. A README sentence, a `## 0.7.10` changelog section, and the version raise (D-001). D-005 and the IP1 and IP5 text that it narrows.

**Out:** Whether IP1 names Quarto's drops and the no-element result of a call with no first argument stays with the candidate row "Decide whether IP1 names Quarto's drops"; D-005 covers the empty argument only. A warning when Quarto shifts arguments left stays with the candidate row "Warn when Quarto shifts arguments left". A call with an empty first argument and a second positional argument, such as `{{< li "" wlpxtupd >}}`, takes the same code path but gets no test, because `fixture_calls` accepts one positional argument (`_tests/check_aria.py:380`). No demo page changes, because a warning shows nothing on a page (GP4: re-render only).

## Acceptance criteria

- [x] AC1: A `li` or `lif` call whose first argument is empty gives no `<lord-icon>` element in an HTML render, as `python3 _tests/check_aria.py` shows in the page and in the raw filter output for four new `_tests/aria.qmd` cases: `{{< li "" >}}` on its own line, `{{< li '' >}}` inside a paragraph, `{{< lif '' >}}` on its own line, and `{{< lif "" >}}` inside a paragraph (RB tripwire: ip-touching).
- [x] AC2: In the same run, the HTML render's log holds exactly one lordicon warning for each of those four calls, holding the call as `{{< li "" >}}` or `{{< lif "" >}}`, the text `has an empty first argument, so it shows no icon.`, and the example call `{{< li wlpxtupd >}}` or `{{< lif icon.json >}}`; the run's `gfm` render of the fixture gives no icon and no lordicon warning.
- [x] AC3: README.md's Customizing section says that a call whose only positional argument is empty, such as `{{< li "" >}}`, shows no icon and that the render warns; CHANGELOG.md's first version section is `## 0.7.10` and holds that change; `_extensions/lordicon/_extension.yml` reads `version: 0.7.10`.
- [x] AC4: `python3 _tests/check_aria.py` exits 0, and `quarto render` at the repo root succeeds.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T3
- AC4 → T1, T2, T3

## Tasks

- [x] T1: Add the four AC1 calls to `_tests/aria.qmd` under "A first argument that Quarto drops, or none" (`_tests/aria.qmd:138`), with ids `empty-li`, `empty-li-inline`, `empty-lif`, and `empty-lif-inline`. In `_tests/check_aria.py`, add the ids to `NO_ICON` (`:210`) and give each a `WARNED` entry with the literal call string, because `check_warnings` builds `{{< li  >}}` from an empty `arg` (`:423-424`). Make `check_spelling` skip an empty `arg` as it skips `None` (`:405`). Run the check against the unchanged filter and confirm that each new case fails for an emitted icon and a missing warning, and for no other reason.
- [x] T2: In `_extensions/lordicon/lordicon.lua`, make `li` (`:427`) and `lif` (`:504`) return `pandoc.Inlines({})` when the stringified first argument is `""`, and in `html:js` formats warn: `lordicon: {{< li "" >}} has an empty first argument, so it shows no icon. Put the icon code first, such as {{< li wlpxtupd >}}.` (and the `lif` form with the path of the icon file and `icon.json`). Share the format gate of `no_first_argument` (`:409`). Update the header comment (`:17`). Run `python3 _tests/check_aria.py`.
- [x] T3: Add the README sentence after the first-argument paragraph (`README.md:103-110`), a `## 0.7.10` section in `CHANGELOG.md`, and `version: 0.7.10` in `_extensions/lordicon/_extension.yml`. Run `quarto render` at the repo root, and run `git checkout -- docs/sitemap.xml` if only the sitemap changed.
- [x] T4: Append D-005 to `cairn/DECISIONS.md`: an empty first argument gives no element (narrows IP1 and IP5); the user chose it at the M011 question set; no warning release first, because such a call never loaded an icon; keeping the element with a warning was rejected. Update IP1, IP5, and the `_tests/` and Known issues text in `cairn/DESIGN.md` to match.

## Work log

- 2026-10-25: created by /milestone-plan.
- 2026-10-25: tier check: not run — work named at the question set.
- 2026-10-25: idea vet: no concern found; a probe render with Quarto 1.10.19 confirmed that `""` and `''` reach the filter as an empty first argument, both on a line of their own and inside a paragraph, and render `src="https://cdn.lordicon.com/.json"` or `src=""` with no warning.
- 2026-10-25: lessons used: 2026-10-24 (M005) Quarto's leading-space drop, 2026-10-25 (M009) test a call inside a paragraph and on its own line, 2026-10-25 (M010) return `pandoc.Inlines({})`, 2026-10-25 (M007) the `gfm` check, 2026-10-20 (M002) the sitemap date.
- 2026-10-25: question set: work to plan — "Warn about an empty first argument" (over the IP1 row, the less-than row, and the byte-sort row); what an empty call makes — no icon and one warning.
- 2026-10-25: plan gate chose no element plus a warning over keeping the element with a warning, because the element can never load an icon and the missing-argument path already does this since 0.7.9; falsified by a user report of a page script that sets `src` on an empty `lif` element.
- 2026-10-25: collision check: absorbed the candidate row "Warn about an empty first argument"; the IP1 row overlaps on the no-element result and stays for the missing argument and Quarto's drops; no D-entry or archived milestone covers an empty argument; inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-25: criteria audit (full mode, fresh Opus reader): 10 findings. Fixed: two cases varied shortcode, quote, and place together (now four cases); IP1/IP5 conflict (T4 writes D-005, AC1 tagged); `check_warnings` cannot build an empty call name (T1 uses literal strings); AC2 paraphrased the warning (exact text); README overclaimed for `{{< li "" x >}}` (narrowed to an only positional argument); `docs/` re-render unstated (Scope); `check_spelling` and `NO_ICON` edits unnamed (T1). Answered: `''` premise (probe render passes it through); a dropped argument could pass AC1 on the page (AC2's empty-argument text tells the two paths apart); `lif ''` warns as `""` (intended, `call_arg` writes double quotes).
- 2026-10-25: byte-sort row vet: a probe render under `LC_ALL=en_US.UTF-8` gave collation `C`, so that row's premise did not hold in a render; the row stays as it is.
- 2026-10-25: implement started on branch m011-empty-first-argument; the untracked `.DS_Store` at the repo root is not milestone work and stays unstaged.
- 2026-10-25: escalation offer for AC1's ip-touching tag: the user chose to go on and record the choice as D-005 (T4), with no review brief.
- 2026-10-25: T1 done: four `empty-*` cases in `_tests/aria.qmd` (two on their own lines, two in one paragraph); `check_aria.py` adds them to `NO_ICON` with literal-call `WARNED` entries and skips an empty `arg` in `check_spelling`. Against the unchanged filter the check gives 13 failures, all of them the new cases' emitted icons (page and filter), their missing warnings, and the warning count.
- 2026-10-25: T2 done: `no_first_argument` takes the argument (nil or "") and gives the empty-argument text for ""; `li` and `lif` call it when the stringified first argument is missing or empty. `check_aria.py` exits 0.
- 2026-10-25: minor amendment to T2: `check_warnings` now requires that a warning text shared by several cases appear once per case, because the two `li` cases (and the two `lif` cases) warn with the same text; a planted second warning for empty `lif` calls failed the check with 4 lines for 2 cases.
- 2026-10-25: T3 done: README sentence, `## 0.7.10` changelog entry, `version: 0.7.10`. `quarto render` at the root exited 0 and changed only `docs/sitemap.xml`, which was reverted. `curl` gave 404 for `https://cdn.lordicon.com/.json`, the source of the changelog's claim. The simple-english hook flags README lines that this milestone did not write; they stay as they are.
- 2026-10-25: T4 done: D-005 appended to `cairn/DECISIONS.md`; DESIGN.md's IP1 and IP5 name the empty first argument, and the `_tests/` and Known issues text names the empty-argument check.
- 2026-10-25: claim audit: 18 claims read, 0 corrected — CHANGELOG.md, README.md, _extensions/lordicon/lordicon.lua, _extensions/lordicon/_extension.yml, _tests/check_aria.py, _tests/aria.qmd. The reader noted that `{{< li "" wlpxtupd >}}` also shows no icon; the README keeps the narrower claim, because `fixture_calls` cannot test that call (Scope Out).
- 2026-10-25: catch-up minor amendment to T1: the four cases went under a new `## An empty first argument` heading (`_tests/aria.qmd:144`), not under "A first argument that Quarto drops, or none", because Quarto does not drop an empty argument.
- 2026-10-25: implement complete; `python3 _tests/check_aria.py` exits 0 and `quarto render` at the root exits 0; status set to review.

## Decisions

- 2026-10-25 (review): Before 0.7.10, `{{< li "" label="Bell" >}}` made an element with `role="img"` and `aria-label="Bell"`, so a screen reader could announce an image that the page never showed. D-005's reason, that such a call never loaded an icon, covers this output too: it named an image that was not there, so no warning release comes first. Raised by the blame-history reviewer.

## Review

Evidence gathered 2026-10-25 on branch m011-empty-first-argument at b2f7c83, level with origin/main 1bb7a2b.

- AC1: `python3 _tests/check_aria.py` exit 0, 0 failures, 92 icons for 92 cases in the page and in the filter output. `NO_ICON` holds `empty-li`, `empty-lif` (own lines, `""` and `''`) and `empty-li-inline`, `empty-lif-inline` (one paragraph, `''` and `""`), so any `<lord-icon>` from them would fail. A separate HTML render of the fixture's "An empty first argument" section gave 0 `<lord-icon>`. T1's run against the unchanged filter failed on all four cases in both places.
- AC2: same run: log 53 of 53 lordicon warnings, 0 failures, with each `WARNED` text tuple matched once per case. The separate render printed 4 warnings: twice `lordicon: {{< li "" >}} has an empty first argument, so it shows no icon. Put the icon code first, such as {{< li wlpxtupd >}}.` and twice the `lif` form ending `such as {{< lif icon.json >}}.` The check's `gfm` render: 0 lordicon warnings, no `lord-icon` or `{{<` in 776 characters; the separate `gfm` render matched (0 and 0).
- AC3: README.md:111-113, in `## Customizing` (README.md:62, next heading 115), says a call whose only positional argument is empty, such as `{{< li "" >}}`, shows no icon and the render warns. CHANGELOG.md's first version heading is `## 0.7.10` (line 5), and its entry (line 7) names the empty first argument. `_extensions/lordicon/_extension.yml:3` reads `version: 0.7.10`.
- AC4: `python3 _tests/check_aria.py` exit 0 (AC1 run); `quarto render` at the repo root exit 0, which changed only `docs/sitemap.xml`, reverted.
- Gate: `cairn_validate.py` all checks passed. `cairn_impact.py --changed` reported no changed principles, because it reads uncommitted edits and the IP1/IP5 edit is in T4's commit; `cairn_impact.py IP1 IP5` listed the references. Live ones outside history: DESIGN.md:134 (GP5 cites IP1, still true) and the ROADMAP row "Decide whether IP1 names Quarto's drops", whose list of IP1 exceptions was corrected in place to add the empty first argument. Version markers: `_extension.yml` and CHANGELOG.md both say 0.7.10. Changelog entry present. The verify render ran on the review head.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: `check_warnings` grouping lets a 2+0 split between two cases that share a warning text pass — follow-up, row "Match each warning to its own call" (the separate AC2 render printed the four warnings in call order)
- diff-bug #2: CHANGELOG "The render gave no warning" is false for an empty call with other keys, which got skipped-key or nameless-role warnings — fix now, fixed 9b5a5a4
- diff-bug #3: "in HTML output" does not hold for epub — reject, style: the repo's docs use "HTML output" for `html:js` formats, as the 0.7.9 entry does
- diff-bug #4: the empty-argument text writes `""` instead of calling `call_arg("")` — reject, planned change: the plan named that text, and `call_arg("")` returns `""`
- diff-bug #5: `{{< li {{< meta empty >}} >}}` reaches the filter as a placeholder and gives a wrong `src` with no warning — follow-up, row "Warn about a nested shortcode argument" (not introduced by this diff)
- diff-bug #6: T1's change of fixture heading has no work-log line — fix now, fixed 9b5a5a4
- diff-bug #7: IP1's "the render warns" leaves out the `html:js` condition — reject, style: IP3 states the format rule for every warning
- diff-bug #8: the `""` and `''` cases repeat one filter path — reject, planned change: the criteria audit asked for both quote forms to pin the `''` premise
- blame-history #1: D-005's reason contradicts the work log's "falsified by a user report" — reject, false: that line names the evidence class that would falsify the choice, not a report received
- blame-history #2: D-005 does not address that `{{< li "" label="Bell" >}}` gave an element with a name — fix now, milestone-local Decisions entry 2026-10-25 (review)
- blame-history #3: same as diff-bug #1 — follow-up, row "Match each warning to its own call"
- blame-history #4: `check_aria.py:209` comment omits the empty cases — fix now, fixed 9b5a5a4
- blame-history #5: CHANGELOG says any empty first argument, README a lone one — fix now, CHANGELOG narrowed to "only positional argument"
- blame-history #6: the candidate row "Warn about an empty first argument" is still listed — reject, planned change: post-merge hygiene graduates it
- prior-review #1: `{{< li "" wlpxtupd >}}` is neither documented nor tested, as M010 fixed for the shift case — follow-up, row "Say that an empty argument never shifts"
- prior-review #2: lines over 100 columns — reject, style (as M010 diff-bug #8)
- ripple #1: IP1's exception list omits the empty first argument — fix now, fixed 9b5a5a4
- ripple #2: `lordicon.lua:12-13` exception list omits the empty argument — reject, false: lines 17-18 of the same comment state it
- ripple #3: ROADMAP row "Warn about an empty first argument" stays in the present tense — reject, planned change: hygiene graduates it
- ripple #4: `check_aria.py:209` comment — fix now, fixed 9b5a5a4 (same as blame-history #4)
- ripple #5: `fixture_calls` docstring says `arg` is None only with no first argument — reject, false: that stays true, and an empty argument is ""
- ripple #6: `aria.qmd:138` heading does not name the empty case — reject, false: the empty cases have their own heading at line 144
- Return floor: no finding shows a criterion failing or a load-bearing defect; no return. Fix-now: 7, follow-up: 4 (3 new rows), rejected: 11.
