# M011: Warn about an empty first argument

- **Status:** in-progress
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

- [ ] AC1: A `li` or `lif` call whose first argument is empty gives no `<lord-icon>` element in an HTML render, as `python3 _tests/check_aria.py` shows in the page and in the raw filter output for four new `_tests/aria.qmd` cases: `{{< li "" >}}` on its own line, `{{< li '' >}}` inside a paragraph, `{{< lif '' >}}` on its own line, and `{{< lif "" >}}` inside a paragraph (RB tripwire: ip-touching).
- [ ] AC2: In the same run, the HTML render's log holds exactly one lordicon warning for each of those four calls, holding the call as `{{< li "" >}}` or `{{< lif "" >}}`, the text `has an empty first argument, so it shows no icon.`, and the example call `{{< li wlpxtupd >}}` or `{{< lif icon.json >}}`; the run's `gfm` render of the fixture gives no icon and no lordicon warning.
- [ ] AC3: README.md's Customizing section says that a call whose only positional argument is empty, such as `{{< li "" >}}`, shows no icon and that the render warns; CHANGELOG.md's first version section is `## 0.7.10` and holds that change; `_extensions/lordicon/_extension.yml` reads `version: 0.7.10`.
- [ ] AC4: `python3 _tests/check_aria.py` exits 0, and `quarto render` at the repo root succeeds.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T3
- AC4 → T1, T2, T3

## Tasks

- [x] T1: Add the four AC1 calls to `_tests/aria.qmd` under "A first argument that Quarto drops, or none" (`_tests/aria.qmd:138`), with ids `empty-li`, `empty-li-inline`, `empty-lif`, and `empty-lif-inline`. In `_tests/check_aria.py`, add the ids to `NO_ICON` (`:210`) and give each a `WARNED` entry with the literal call string, because `check_warnings` builds `{{< li  >}}` from an empty `arg` (`:423-424`). Make `check_spelling` skip an empty `arg` as it skips `None` (`:405`). Run the check against the unchanged filter and confirm that each new case fails for an emitted icon and a missing warning, and for no other reason.
- [ ] T2: In `_extensions/lordicon/lordicon.lua`, make `li` (`:427`) and `lif` (`:504`) return `pandoc.Inlines({})` when the stringified first argument is `""`, and in `html:js` formats warn: `lordicon: {{< li "" >}} has an empty first argument, so it shows no icon. Put the icon code first, such as {{< li wlpxtupd >}}.` (and the `lif` form with the path of the icon file and `icon.json`). Share the format gate of `no_first_argument` (`:409`). Update the header comment (`:17`). Run `python3 _tests/check_aria.py`.
- [ ] T3: Add the README sentence after the first-argument paragraph (`README.md:103-110`), a `## 0.7.10` section in `CHANGELOG.md`, and `version: 0.7.10` in `_extensions/lordicon/_extension.yml`. Run `quarto render` at the repo root, and run `git checkout -- docs/sitemap.xml` if only the sitemap changed.
- [ ] T4: Append D-005 to `cairn/DECISIONS.md`: an empty first argument gives no element (narrows IP1 and IP5); the user chose it at the M011 question set; no warning release first, because such a call never loaded an icon; keeping the element with a warning was rejected. Update IP1, IP5, and the `_tests/` and Known issues text in `cairn/DESIGN.md` to match.

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

## Decisions

## Review
