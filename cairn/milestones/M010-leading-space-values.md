# M010: Warn on a lost first argument and document leading spaces

- **Status:** review
- **Priority:** normal
- **Depends on:** M009
- **Driving RR:** —
- **Principles touched:** IP3, GP2, GP4
- **Resolves:** —
- **Surface tier:** user-facing — it changes render behavior, a render warning, and the user docs
- **Branch/PR:** m010-leading-space-values

## Goal

A `li` or `lif` call with no first argument makes no element and warns instead of failing the render, and the docs say that Quarto drops a value or first argument that starts with a space or tab.

## Scope

**In:** Probes on Quarto 1.10.19 show the cause. Quarto's shortcode reader
writes each value into a Pandoc span attribute, and Pandoc's attribute parser
rejects a quoted value that starts with a space or tab, in `"` or `'` quotes.
The key, or the positional argument, then never reaches the filter, in
`kwargs` or in `raw_args`, and Quarto logs nothing. A trailing space survives.
So `label=" Bell "` labels nothing and the icon stays `aria-hidden`. A call
whose first argument is lost, or that has none, stops the render at
`lordicon.lua:390` (`li`) or `lordicon.lua:464` (`lif`), in HTML and in `gfm`,
because `stringify(args[1])` runs before the format check. This milestone
makes such a call return no element and, in `html:js` formats only, give one
warning. It adds the docs note to `README.md` and `index.qmd`, fixture cases,
version 0.7.9, and a changelog entry.

**Out:** an empty first argument (`{{< li "" >}}`), which reaches the filter
and renders a broken `src` with no warning → candidate row "Warn about an
empty first argument". A hint about leading spaces in the nameless-image
warning, which the user declined at the question set. A report to Quarto,
which the user declined at the question set.

## Acceptance criteria

- [x] AC1: A render of `_tests/aria.qmd` to HTML succeeds with a `li` call whose first argument is `" ibydboev"` and a `lif` call with no first argument. Each of these calls gives no `<lord-icon>` and one lordicon warning. The warning names the call as `{{< li >}}` or `{{< lif >}}`. It says that the call has no first argument, and that Quarto drops a first argument that starts with a space or tab.
- [x] AC2: A render of `_tests/aria.qmd` to `gfm` with the same calls succeeds and gives no lordicon warning.
- [x] AC3: In `README.md`, the Customizing text above `### Accessibility` says that Quarto drops a `key="value"` whose value starts with a space or tab, in `"` or `'` quotes, together with its key. It says that this happens before the extension runs, so no warning names the dropped value. It says that removing the leading space fixes it. It also says that Quarto drops a first argument that starts with a space or tab, and that the render then warns that the call has no first argument.
- [x] AC4: The Accessibility section of `index.qmd` says that Quarto drops a `label` value that starts with a space or tab in the same way. An icon with no other ARIA key then stays hidden from screen readers. `docs/` holds the re-rendered home page.
- [x] AC5: A render of `_tests/aria.qmd` shows each of these `li` calls, with no other ARIA key, as an icon with `aria-hidden="true"`, no `aria-label`, and no `role`: `label=" Bell "`, `label=' Bell'`, and `label="<TAB>Bell"` with a tab byte. A `li` call with `class=" x"` shows an icon with no `class` attribute. The render gives no lordicon warning for these four calls. These cases are in the fixture, so `python3 _tests/check_aria.py` fails if a Quarto version stops dropping such values.
- [x] AC6: The verify slot of `cairn/PROFILE.md` is clean. `python3 _tests/check_aria.py` exits 0, and `quarto render` at the repo root succeeds. The icons of the changed home page load and animate in a browser.
- [x] AC7: `version:` in `_extensions/lordicon/_extension.yml` reads `0.7.9`. `CHANGELOG.md` has a `## 0.7.9` section. It says that a `li` or `lif` call with no first argument now warns and shows no icon, where before it stopped the render.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T3
- AC4 → T3
- AC5 → T1
- AC6 → T1, T2, T3
- AC7 → T4

## Tasks

- [x] T1: Write the fixture cases first and see the check fail. In
      `_tests/aria.qmd`, add the two calls of AC1 and the four calls of AC5,
      each with its own `id`. Write the tab of AC5 with a short script and
      confirm the byte with `od -c` (LESSONS, M008). Make `fixture_calls`
      and `check_warnings` model Quarto's drop: a positional argument or
      value that starts with a space or tab reaches the filter as absent, so
      the expected call is `{{< li >}}` or `{{< lif >}}`. Make
      `raw_output.lua` call the shortcode with no argument for such a case.
      `raw_output.lua` passes a leading-space value through as written
      (LESSONS, M005), so give the AC5 cases page-side expectations. Give the
      AC1 cases a way to expect no `<lord-icon>`. Confirm that the HTML and
      `gfm` renders now stop at `lordicon.lua:390`.
- [x] T2: In `li` and `lif`, return no element when `args[1]` is nil, and in
      `html:js` formats give the warning of AC1 before returning. Name the
      call as `{{< li >}}` or `{{< lif >}}`, and say what to write instead,
      such as `{{< li wlpxtupd >}}`. Run the check until it exits 0.
- [x] T3: Add the README text of AC3 and the `index.qmd` text of AC4. Run
      `quarto render` at the repo root, commit `docs/` with the sitemap
      (LESSONS, M002), and open the home page in a browser to see its icons
      load and animate.
- [x] T4: Raise `version:` to `0.7.9` and add the `## 0.7.9` CHANGELOG
      section. Update the `_tests/` line of DESIGN.md Architecture and its
      Known issues entry to name the no-argument and leading-space cases.

## Work log

- 2026-10-25: created by /milestone-plan.
- 2026-10-25: tier check: milestone — the leading-space candidate changes docs and, with the folded crash fix, render behavior.
- 2026-10-25: idea vet: concern that the extension cannot keep or see a value that starts with a space, so the candidate's title "Keep values" cannot be met; the question set chose a docs note with a fixture that pins Quarto's behavior.
- 2026-10-25: lessons used: 2026-10-24 (M005) on Quarto dropping leading-space values and on testing them with a render; 2026-10-25 (M008) on writing whitespace bytes into `_tests/aria.qmd` with a script; 2026-10-20 (M002) on committing `docs/` with the sitemap.
- 2026-10-25: absorbed candidate "Keep values that start with a space" (M005 plan probe); the M005 archive holds the nameless-image warning this milestone leaves as it is.
- 2026-10-25: inbox sweep: 0 open issues and 0 open PRs.
- 2026-10-25: question set: leading-space work — docs note, with a fixture that pins the behavior (the warning hint was declined).
- 2026-10-25: question set: crash on a lost or missing first argument — fold the fix into this milestone.
- 2026-10-25: question set: report to Quarto — no report; nothing is posted outside this repo.
- 2026-10-25: plan gate chose a docs note over a hint in the nameless-image warning because every reader of that warning would see it for a rare case; falsified by user reports of labels lost to a leading space that the docs did not prevent.
- 2026-10-25: plan chose to warn only in `html:js` formats over warning in every format, because the render check holds that other formats give no lordicon warning; falsified by a non-HTML format where a lost first argument hides a failure.
- 2026-10-25: plan chose Depends on M009 because both raise the version and edit CHANGELOG; M009 takes 0.7.8 and this milestone 0.7.9.
- 2026-10-25: criteria audit (full mode, Opus reader) of the criteria the question set changed: 7 findings. Fixed: "space or tab" in AC1; "no warning names the dropped value" in AC3, since `role=img` still gives the nameless-image warning; AC5 now varies the quote style, a tab, and a non-label key, and its last sentence states what the fixture gives; Depends on M009 for AC7. Answered: an empty first argument becomes a candidate row, toward the narrower promise; the call name `{{< li >}}` is what the filter can know; the browser look in AC6 is the profile's own verify step. AC2 and AC4 had none.
- 2026-10-25: changelog: one entry under 0.7.9 (D-001, D-002).
- 2026-10-25: implement started on branch m010-leading-space-values; unrelated untracked `.DS_Store` left unstaged.
- 2026-10-25: T1 done: six fixture cases; `fixture_calls` drops a positional argument or value that starts with a space or tab, so `raw_output.lua` gets what a render gives the filter and the AC5 cases share one expectation for page and filter (chosen over page-only expectations); before T2 the HTML and `gfm` renders stopped at `lordicon.lua:406` (`li`) and `:480` (`lif`) with "Cannot get Attr from TypeNil" (the scope's 390 and 464 predate M009's added lines); two planted defects (no drop in `fixture_calls`; a `lif` with no argument that returns an icon) turned the check red.
- 2026-10-25: T2 done: `li` and `lif` call `no_first_argument` when `args[1]` is nil, which warns in `html:js` formats only and returns `pandoc.Inlines({})` (chosen over `pandoc.Null()`, which `quarto pandoc lua` lacks); check exits 0 (91 cases, 49 warnings, 0 in `gfm`) and `quarto render` succeeds.
- 2026-10-25: T3 done: README paragraph above `### Accessibility` and `index.qmd` Accessibility paragraph, written against renders this session (a tab-led and a single-quoted leading-space first argument also give the warning); `docs/` re-rendered with the sitemap; in the browser all 17 home-page icons were ready and advanced from frame 0 to 24; the simple-english hook's 27 README hits all predate this paragraph (27 before and after) and stay out of scope.
- 2026-10-25: T4 done: `version: 0.7.9` (the only extension version marker), `## 0.7.9` CHANGELOG entry, DESIGN `_tests/` line and Known issues entry name the no-argument and leading-space cases; check exits 0 and `quarto render` succeeds (no page changed, sitemap restored).
- 2026-10-25: claim audit: 32 claims read, 0 corrected — CHANGELOG.md, README.md, index.qmd, docs/index.html, lordicon.lua, _tests/check_aria.py, _tests/raw_output.lua, _tests/aria.qmd
- 2026-10-25: claim audit caveat: a leading-space first argument followed by another positional lets Quarto promote the second, with no warning; recorded as candidate row "Warn when Quarto shifts arguments left" rather than widening the criteria.
- 2026-10-25: implement complete; status review; handing off to /milestone-review.

## Decisions

## Review

Evidence gathered 2026-10-25 at 63bfd7e with Quarto 1.10.19.

- AC1: an HTML render of `_tests/aria.qmd` (scratchpad script, temp dir) exited 0; no `<lord-icon>` holds `id="lost-li"` or `id="missing-lif"`; the log holds exactly one warning naming `{{< li >}}` and one naming `{{< lif >}}`, each saying "has no first argument, so it shows no icon. Quarto drops a first argument that starts with a space or tab."
- AC2: the same fixture rendered to `gfm` exited 0 with 0 lordicon warnings; the output holds no `lord-icon` and no `{{<`.
- AC3: `README.md`, in the Customizing text above `### Accessibility`, says Quarto drops a `key="value"` whose value starts with a space or tab, in `"` or `'` quotes, with its key; that this happens before the extension runs, so no warning names the dropped value; that removing the leading space fixes it; and that Quarto drops a first argument that starts with a space or tab, after which the render warns that the call has no first argument (read with awk this session).
- AC4: the Accessibility section of `index.qmd` says Quarto drops a `label` value that starts with a space or tab, with its key, and that an icon with no other ARIA key then stays hidden from screen readers; `docs/index.html` holds that paragraph once (grep), re-rendered and committed in T3 (d6b3c5d); a fresh `quarto render` changed no page.
- AC5: in the AC1 HTML render, `space-label` (`label=" Bell "`), `space-squote` (`label=' Bell'`), `space-tab` (tab byte, `od -c` in T1) and `space-class` (`class=" x"`) each render as `<lord-icon>` with only `src`, `id`, and `aria-hidden="true"`: no `aria-label`, `role`, or `class`; none of the log's 49 lordicon warnings comes from them (the 12 that name `{{< li wlpxtupd >}}` are the 11 `src` and invalid-key cases and the example in the `{{< li >}}` warning); the four cases are in `CASES` and `EXACT` of `check_aria.py`, and T1's planted keep-the-value defect turned those cases red.
- AC6: `python3 _tests/check_aria.py` exited 0 (page and filter 91 icons and 91 cases, 49 of 49 warnings, `gfm` 0 warnings, 0 failures); `quarto render` at the root exited 0 (sitemap restored); in the browser pane at the `docs` preview, all 17 home-page icons were ready and all 17 advanced from frame 0 after `playFromStart()`.
- AC7: `_extension.yml` reads `version: 0.7.9`; `CHANGELOG.md` has `## 0.7.9`, whose entry says a `li` or `lif` call with no first argument now shows no icon and warns in HTML, where before it stopped the render.
- gate: `cairn_validate.py` exit 0 (all checks passed); no IP/GP line changed in DESIGN.md, so `cairn_impact` skipped; version markers agree (`_extension.yml` is the only one the release-walk names, 0.7.9); verify render green at 63bfd7e (AC6); `CHANGELOG.md` has a `## 0.7.9` entry for the user-visible change.
