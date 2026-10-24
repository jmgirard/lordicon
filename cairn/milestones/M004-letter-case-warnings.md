<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section. -->
# M004: Warn about keys in another letter case

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP3, GP2
- **Resolves:** —
- **Surface tier:** user-facing — the warnings appear in users' renders
- **Branch/PR:** m004-letter-case-warnings

## Goal

A shortcode key whose effect depends on its letter case gives a render warning, where before it failed with no visible error.

## Scope

**In:** a warning for forwarded keys that differ only in letter case; a warning for `label` written in another letter case; the Minified warning for `colors`, `stroke`, and `state` in any ASCII letter case; fixture cases and a fixture file with no control layer; README, CHANGELOG 0.7.4, the version, and DESIGN Conventions and Known issues.

**Out:**
- Treating `Label` as `label`: the plan gate chose a warning, so the key keeps its passthrough meaning.
- Naming which key of a clash the page keeps: Quarto keeps the first for ASCII clashes and the last for non-ASCII ones (observed 2026-10-24), so the warning says only that one value is kept.
- Checks for attribute sorting and non-HTML output stay in the candidate row "Add a render check with fixtures".
- A warning for `role="img"` with no name, keys that hold `<`, and the GP5 wording stay in their candidate rows.
- A demo-site example: a warning shows in the render log, not on a page, so `docs/` changes only if a demo page changes.

## Acceptance criteria

- [ ] AC1: In one call, two or more forwarded keys with non-empty values can be equal after `pandoc.text.lower`, which lowercases letters inside and outside ASCII. Keys that equal `label` after this lowering are left to AC2. Such a call gives one case-clash warning, besides any `src`, invalid-name, or Minified warning. The warning names the call and each key of each group, and it says that the page keeps only one value of each group. Each key still appears in the raw filter output as written. `python3 _tests/check_aria.py` shows this for fixture calls with `role` and `Role`, with `class`, `Class`, and `CLASS`, with `aria-label` and `aria-Label`, with two groups in one call, and with `data-É` and `data-é`. It also shows that `role=""` beside `Role` gives no case-clash warning.
- [ ] AC2: A call can pass, with a non-empty value, a key that equals `label` after `pandoc.text.lower` but is not `label`, such as `Label`. Such a call gives one warning that names the call and each such key and says to use one lowercase `label`. Each such key still reaches the element as written. `check_aria.py` shows this for `Label="Bell"` alone, for `laBel` beside `label`, and for `Label` beside `LABEL`.
- [ ] AC3: The first `lif` call on a readable file with no `"nm":"control"` layer gives the Minified warning when it passes `colors`, `stroke`, or `state` in any ASCII letter case with a non-empty value. The warning names each such key as written. `check_aria.py` shows this for a call with `Colors`, `STROKE`, and `sTaTe` on a fixture file with no control layer. It also shows that the same keys on `gift_raw.json` give no Minified warning.
- [ ] AC4: The fixture calls that exist before this milestone give the same attributes and lordicon warnings as before. `python3 _tests/check_aria.py` exits 0 with their expected values unchanged, and `quarto render` at the repo root succeeds.
- [ ] AC5: README.md describes the warnings of AC1, AC2, and AC3. CHANGELOG.md has a `## 0.7.4` section that describes them. The `version:` line in `_extensions/lordicon/_extension.yml` is `0.7.4`.

## Coverage

- AC1 → T1, T2
- AC2 → T3
- AC3 → T4
- AC4 → T1, T6
- AC5 → T5

## Tasks

- [x] T1: Extend `_tests/check_aria.py` for the new cases before the code changes. Let a case expect more than one warning and match each warning by its own text, the Minified line included. Allow the expected duplicate names of AC1 cases in the raw-output duplicate check, and keep that check, the spelling check, and the exact warning count for every earlier case. Add the AC1 fixture calls to `_tests/aria.qmd` and see them fail on the current filter.
- [x] T2: In `build_element` (`lordicon.lua:117`), group the forwarded keys by `pandoc.text.lower` and give one case-clash warning per call for the groups with two or more keys, in the style of `warn_skipped`. Keys that lower to `label` are left out of the groups.
- [x] T3: Add the AC2 fixture calls and expectations, then the `label` warning in `build_element`, with advice to use one lowercase `label`.
- [x] T4: Add `_tests/minified.json`, a minimal Lottie file with no control layer and no icon art (IP6), and copy it in `render_page`. Add the AC3 calls. In `check_minified` (`lordicon.lua:217`), match `CONTROL_DEPENDENT` with `ascii_lower` over the call's keys and name each key as written.
- [x] T5: Update README.md (the passthrough and Minified sections), CHANGELOG.md `## 0.7.4`, `version:` in `_extension.yml`, the header comment of `lordicon.lua`, and DESIGN Conventions and Known issues (the Minified warning now has a check).
- [ ] T6: Run the verify slot: `python3 _tests/check_aria.py`, then `quarto render` at the repo root, then `git checkout -- docs/sitemap.xml` if no demo page changed. Open any changed demo page in a browser.

## Work log

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: tier check: not run — work named at the question set.
- 2026-10-24: idea vet: two concerns. A lone `Label` gives a hidden icon with no name, which the candidate's clash warning misses; the set chose a warning that keeps passthrough. The page keeps only one value of a clash, and which one depends on ASCII or non-ASCII letters; decided toward the narrower warning that names no kept key. The test-only fixture row tests unchanged behavior; noted at the set, not chosen.
- 2026-10-24: question set: which work — letter-case warnings; `Label` handling — warn, keep passthrough.
- 2026-10-24: collision check: absorbs the candidate rows "Warn on keys that differ only in case" and "Match Minified-check keys in any case" in full and the Minified-warning part of "Add a render check with fixtures"; D-003 and IP1 allow a warning that drops nothing; no open issues or PRs (0 and 0).
- 2026-10-24: criteria audit (full mode, fresh Opus reader): 8 findings. Fixed: non-ASCII clash collapses on the page (AC1 now lowers with `pandoc.text.lower` and drops the no-warning probe); "one warning" ambiguous (AC1 names the other warnings); AC4 could pass by loosening the checker (AC4 keeps earlier expectations, T1 keeps the checks); missing probes (empty value, interior letter, `laBel`); `Label=""` and wrong advice (AC2 non-empty, "use one lowercase label"); Minified once-per-file and unreadable files (AC3 first call, readable file); verify browser step (T6); DESIGN updates (T5). Answered: `id` clashes are warned but not probed, because the harness finds cases by `id`.
- 2026-10-24: plan gate chose a warning for `Label` over treating it as `label` because it keeps IP1 with no decision entry; falsified by users who keep writing `Label` after the warning.
- 2026-10-24: plan chose `pandoc.text.lower` over ASCII-only folding for clashes because the page also drops non-ASCII clashes (observed); falsified by a supported Quarto whose Pandoc has no `pandoc.text`.
- 2026-10-24: plan chose a synthetic fixture with no icon art over a real Minified export because the filter reads only the control layer and IP6 then holds; falsified by a Minified check that reads more of the file.
- 2026-10-24: no demo-site change planned: GP4 asks for an example per feature, and a render-log warning has no page to show.
- 2026-10-24: implement started on branch m004-letter-case-warnings; `.DS_Store` untracked at the root, left unstaged.
- 2026-10-24: T1 done: `WARNED` now lists several warnings per case, each a set of texts one log line must hold; `TWICE` allows the clash names twice in the filter output only. New clash calls use their own icon codes so each call name is unique. The 5 clash warnings failed on the old filter (12 of 17 warnings read).
- 2026-10-24: T2 done: `warn_case_clashes` groups the sorted forwarded keys by `pandoc.text.lower`, groups in order of their first key, joined by "; ". check_aria 0 failures (17 warnings), root render exit 0, sitemap reverted.
- 2026-10-24: T3 done: `warn_label_case` warns once per call for forwarded keys that lowercase to `label`. The 3 label warnings failed first (17 of 20); then check_aria 0 failures (20 warnings), root render exit 0, sitemap reverted.
- 2026-10-24: T4 done: `_tests/minified.json` is an empty Lottie file with no layers; `check_minified` loops over the call's keys with `ascii_lower`. The Minified case failed first (20 of 21); then check_aria 0 failures (21 warnings, none for `raw-lif`), root render exit 0, sitemap reverted.
- 2026-10-24: T5 done: README (a letter-case paragraph after the skipped-keys list, and the Minified note), CHANGELOG `## 0.7.4`, `_extension.yml` 0.7.4, the `lordicon.lua` header comment, DESIGN Conventions, Architecture, and Known issues. The simple-english lint hook flags 23 hits in README text this change did not write; left as is, out of scope. Root render changed only `docs/sitemap.xml`, reverted.

## Decisions

## Review
