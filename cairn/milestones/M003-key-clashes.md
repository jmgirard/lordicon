# M003: Stop key clashes and bad attribute names

- **Status:** review
- **Priority:** normal
- **Depends on:** M002
- **Driving RR:** —
- **Principles touched:** IP1, IP2, IP3, IP5, GP2, GP4, GP5
- **Resolves:** —
- **Surface tier:** user-facing — changes the `<lord-icon>` markup that `li` and `lif` emit
- **Branch/PR:** m003-key-clashes

## Goal

A user `src` key, a mixed-case ARIA key, or a key that HTML does not allow as an attribute name no longer gives a second `src`, a kept `aria-hidden` default, or broken markup.

## Scope

**In:** In `build_element` (`lordicon.lua:73-121`), `src` in any letter case becomes a reserved key with one warning per call (D-003). The four ARIA override names match in any letter case. A key holding whitespace, a control character, `"`, `'`, `>`, `/`, or `=` is skipped with one warning per call (D-003). Fixture cases and harness changes in `_tests/`. The README forwarding section, the IP1 text, version 0.7.3, the changelog section, and the `docs/` re-render.

**Out:** Two keys in one call that differ only in letter case, and a mixed-case `label` → candidate row "Warn on keys that differ only in case". Other shortcode behavior checks → candidate row "Add a render check with fixtures". The GP5 wording and the nameless role icon → their candidate rows.

## Acceptance criteria

- [x] AC1: Fixture calls pass a `src` key to `li` and to `lif`, and an `SRC` key to `li`. Each gives a `<lord-icon>` with one `src` attribute, holding the first argument's source, in the raw filter output and the rendered page. The fixture render's log holds one warning per such call, naming its key. `python3 _tests/check_aria.py` reports each. (RB tripwire: ip-touching)
- [x] AC2: For each of `role`, `aria-hidden`, `aria-label`, and `aria-labelledby`, a fixture call passes the name in mixed or upper case with no `label`. Fixture calls also pass `Role` and `Aria-Label` with `label`. Each gives the ARIA attributes that the same call with all-lowercase keys gives, with names compared without regard to case. The raw filter output holds each key as the user wrote it. `python3 _tests/check_aria.py` reports each case in the raw filter output and the rendered page.
- [x] AC3: For each of a space, `"`, `'`, `>`, `/`, and `=`, a fixture call has a key that holds that character. Its `<lord-icon>` has no attribute from that key, and its other attributes match the same call without that key, in the raw filter output and the rendered page. The fixture render's log holds one warning per such call, naming the key. `python3 _tests/check_aria.py` reports each. (RB tripwire: ip-touching)
- [x] AC4: The 15 fixture cases that `_tests/check_aria.py` checks at 64116ad give the same ARIA attributes, and `python3 _tests/check_aria.py` exits 0 on the review head. `quarto render` at the repo root succeeds, and this milestone commits the re-rendered `docs/`.
- [x] AC5: The README section on forwarded `key=value` pairs states three facts that match the filter code. A `src` key in any letter case is not forwarded, and the render warns. The four ARIA names override the defaults in any letter case. A key holding whitespace, a control character, `"`, `'`, `>`, `/`, or `=` is skipped, and the render warns.
- [x] AC6: `version:` in `_extensions/lordicon/_extension.yml` reads `0.7.3`. `CHANGELOG.md` has a `## 0.7.3` section that names the changes of AC1, AC2, and AC3.

## Coverage

- AC1 → T1, T2, T3, T4
- AC2 → T2, T3, T4
- AC3 → T1, T2, T3, T4, T9
- AC4 → T3, T4, T5, T7
- AC5 → T5, T8, T9
- AC6 → T6

## Tasks

- [x] T1: Change the DESIGN.md IP1 text and the forwarding Conventions bullet to name the `src` and invalid-name exceptions (D-003).
- [x] T2: Extend the harness. `check_aria.py` keeps the fixture render's stderr and checks the warning lines. `fixture_calls()` keeps a quoted key that holds `=` whole. A raw-string check confirms that the filter output keeps each key's spelling.
- [x] T3: Add the AC1 to AC3 cases to `_tests/aria.qmd` and their expected values to `CASES`. Run the check and see each new case fail on the current filter.
- [x] T4: Change `build_element`: reserve `src` by `key:lower()` with a per-call warning, compare ARIA override names by `key:lower()`, and skip invalid names with a per-call warning. The check passes.
- [x] T5: Update the README forwarding section. Run `quarto render` and commit `docs/`. Look at the changed demo pages in a browser, as the PROFILE `verify` slot asks.
- [x] T6: Raise `version:` to 0.7.3 (D-001) and add the `## 0.7.3` section to `CHANGELOG.md`. `BUNDLE_VERSION` stays, because the player does not change.
- [x] T7: (review return 1) Run `quarto render` at the repo root on the final head and commit the re-rendered `docs/`, the `sitemap.xml` date included.
- [x] T8: (review return 2) Skip a key holding a C1 control (U+0080 to U+009F) with the invalid-name warning. Add a fixture case that fails first.
- [x] T9: (review pass 2 fix-now) Add a kept case for valid non-letter keys; remove `bad-tab`; fix the DESIGN wording (Contract boundary, per-kind warnings, IP1 non-empty, IP5 and stable surface per D-003, Architecture, Known issues), PROFILE `verify`, README "forward any", `index.qmd` letter case, and the "Add a render check" row. Re-render `docs/` and look at the home page in a browser.

## Work log

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: not run — work named at the question set.
- 2026-10-20: question set: what to work on — the key-clash fixes, absorbing "Stop duplicate src and ARIA attributes" and "Guard attribute names against bad markup".
- 2026-10-20: question set: src key — reserved in any case, the first argument's source stays, one warning per call (D-003).
- 2026-10-20: question set: bad keys — skipped with a warning from 0.7.3, with no warning release first (D-003).
- 2026-10-20: question set: changelog — its own milestone first (M002), so this milestone depends on it.
- 2026-10-20: probe (Quarto 1.10.19): quoted keys reach the filter with a space, `"`, `'`, `/`, or `=`, and `a>b` reaches it unquoted. Today `a>b=1` breaks the element, and `Role=img` keeps `aria-hidden="true"`.
- 2026-10-20: criteria audit (full, fresh Opus reader): 9 findings, all fixed. The goal is narrowed to three key kinds. AC1 adds an `SRC` probe and one warning per call. AC2 compares names without regard to case and checks spelling in raw output only. AC3 names the exact set and binds its promise to six probed characters. IP5 joins D-003. T2 covers the `=` fixture parse and the render's stderr. AC4 binds the 15 cases at 64116ad and adds the `docs/` re-render. AC5 names the same set and the case rule.
- 2026-10-20: plan gate chose reserving `src` over letting a user `src` win because the first argument would then be ignored; falsified by users who pass `src` on purpose to replace the first argument.
- 2026-10-20: plan gate chose skipping bad keys now over a warning release first because these keys never gave one valid attribute; falsified by a document whose output relies on such a key's stray attributes, such as `"a b"=1` giving `a` and `b`.
- 2026-10-20: plan gate chose comparing `key:lower()` over writing lowercase names because IP1 forbids rewriting a user attribute; falsified by an output format where attribute-name case changes meaning.
- 2026-10-20: decided: new cases go into `_tests/aria.qmd` and `check_aria.py`, because the PROFILE `verify` slot already names them. A wider check stays with its candidate row.
- 2026-10-20: implement started on branch m003-key-clashes, cut from main at 0c6e04b. The untracked `.DS_Store` stays unstaged.
- 2026-10-24: resumed; merged main (a72e0d7, hygiene stamp only) into the branch, and `check_aria.py` passed 15 of 15 cases.
- 2026-10-24: T1 done: IP1 names `src` and invalid names as exceptions with a warning; the forwarding bullet lists the three skipped key kinds, and the ARIA bullet says the four names match in any case.
- 2026-10-24: decided: each warning names the call as `{{< li CODE >}}` or `{{< lif FILE >}}` and the key in double quotes, one warning per kind per call, so the check can match a warning to its call and users can find it.
- 2026-10-24: T2 done: `check_aria.py` parses quoted keys (a quoted key may hold `=`), checks the render's stderr against `WARNED`, checks `EXACT` cases for extra attributes, and reads the raw output for each forwarded key's spelling. 15 of 15 cases still pass. A planted lowercase `role` made the spelling check fail.
- 2026-10-24: T3 done: 15 new cases (6 mixed-case ARIA, 3 `src`, 6 invalid names). On the unchanged filter each new case fails (42 failures: kept `aria-hidden`, a second `src`/`role`/`aria-label`, stray attributes, `a>b` breaking its element, no warnings), and the 15 old cases pass. This commit leaves the check red until T4.
- 2026-10-24: decided: a `src` or invalid key with an empty value is dropped with no warning, as empty values already were; `build_element` takes a third argument naming the call for warnings.
- 2026-10-24: T4 done: `build_element` skips `src` (by `key:lower()`) and invalid names (`[%s%c"'>/=]`) with one warning per kind per call, and records passed names in lowercase for the ARIA checks. `check_aria.py`: 30 of 30 cases, 9 of 9 warnings, 0 failures.
- 2026-10-24: T5 done: the README Customizing section lists the three skipped key kinds and says the four ARIA names count in any case. `quarto render` succeeded and changed no page in `docs/`, only the `sitemap.xml` date, which was reverted (LESSONS M002), so `docs/` as committed is the re-render. No demo page changed, so the browser look had no page to open. The simple-english hook flags older README text outside this milestone's scope; the added lines carry no hits.
- 2026-10-24: added a sub-task: fixture cases `bad-tab` and `bad-control`, so the changelog's whitespace and control-character claims have a test. Each fails on the pre-T4 filter. Quarto's log shows a tab as a space, so the warning check matches keys with whitespace as spaces. The control byte went in with `perl`, because the Edit tool drops it.
- 2026-10-24: T6 done: `version:` is 0.7.3, and `CHANGELOG.md` has a `## 0.7.3` section for the `src`, mixed-case ARIA, and invalid-name changes. `BUNDLE_VERSION` stays 2.3.1. `check_aria.py`: 32 of 32 cases, 11 of 11 warnings.
- 2026-10-24: claim audit: 37 claims read, 4 corrected — lordicon.lua (two comments on what an invalid name did), CHANGELOG.md (the "Before" sentence), check_aria.py (`INVALID_NAME` now ASCII-only to match Lua `%s%c`; the tab comment now says Pandoc expands the tab, and the warning check compares whitespace runs). The reader's re-read found all four hold.
- 2026-10-24: noted for review: Lua `%c` covers ASCII controls only, so a key with a C1 control (U+0080 to U+009F) is still forwarded; the README and changelog say "a control character".
- 2026-10-24: implement complete: `check_aria.py` 0 failures and `quarto render` succeeded (no page changed; `sitemap.xml` date reverted). Status set to review.
- 2026-10-24: review return 1: AC4 — the branch has no `docs/` commit; the root `quarto render` changes only `docs/sitemap.xml`, which implement reverted. Commit the re-rendered `docs/`.
- 2026-10-24: review noted: AC1 and AC3 carry `(RB tripwire: ip-touching)`, and implement step 3's escalation offer for them was not posed; the return poses it.
- 2026-10-24: resumed for review return 1; added T7 for it and mapped AC4 to it (minor amendment). Status in-progress; the branch still contains origin/main.
- 2026-10-24: T7 done: `check_aria.py` 0 failures, root `quarto render` exit 0; the re-render changes `docs/sitemap.xml` only (the `index.html` lastmod), committed here.
- 2026-10-24: escalation offer for the AC1 and AC3 tripwire tags: the user chose to continue to review without a review brief.
- 2026-10-24: T7 added no prose; the earlier claim audit covers every added claim. Status set to review.
- 2026-10-24: review return 2: AC5 — the README says a key with a control character is skipped, but `INVALID_NAME`'s `%c` is ASCII-only, so a C1 control (U+0080 to U+009F) is forwarded with no warning. Skip C1 controls too, with a fixture case. The pass-2 fix-now findings in the Review section ride with this return.
- 2026-10-24: resumed for review return 2; added T8 (the return) and T9 (the pass-2 fix-now findings), mapped AC5 to T8 and T9 and AC3 to T9 (minor amendment).
- 2026-10-24: found at T8: Lua `%s` and `%c` follow the C locale, and under a UTF-8 locale they match bytes 128 to 160 and 173, so a valid key such as `data-straße` (ß is bytes 195 159) was skipped with a warning, while under the C locale a C1 control was forwarded. The pattern now spells out its byte ranges (`[\0-\32\127"'>/=]` plus `\194[\128-\159]` for C1), so it does not depend on the locale.
- 2026-10-24: T8 done: new cases `bad-c1` (U+0085) and `kept-names` (`@click`, `data.k`, `data-straße`, `data-datà`; `x:y` left out because Quarto's HTML post-processing drops it from the page while the raw output keeps it). `bad-tab` removed (diff-bug #3). The raw filter output now runs under `LC_ALL=C` while the page renders under UTF-8, and output is split on `\n` alone, since `splitlines()` breaks at U+0085. `check_aria.py`: 33 cases, 11 warnings, 0 failures. The old pattern fails 4 checks (ß and à skipped on the page, C1 forwarded in the raw output, an extra warning), and `[^%w%-]` fails `kept-names`.
- 2026-10-24: T9 done: DESIGN Contract boundary, per-kind warnings, IP1 (non-empty values), IP5 and the stable-surface convention (D-003 narrowing), Architecture, and Known issues; PROFILE `verify`; README "forward your pairs" with a pointer to the exceptions; `index.qmd` letter-case sentence; the "Add a render check" row narrowed; new rows "Match Minified-check keys in any case" and "Decide on keys that hold a less-than". `check_aria.py` 0 failures; `quarto render` changed `docs/index.html`, `search.json`, `sitemap.xml`. Served `docs/` locally: 17 icons drew their SVG, no console errors, and the new sentence shows.
- 2026-10-24: claim audit: 16 claims read, 4 corrected — lordicon.lua and check_aria.py (`%s`/`%c` follow the current locale, not "the C locale"), check_aria.py (the page render now sets `LC_ALL=C.UTF-8` itself, so both locales are covered whatever the caller's locale), README (an empty-value key is not passed on either). `check_aria.py` 0 failures under the caller's locale and under `LC_ALL=C`; the old `%s%c` pattern still fails 4 checks under `LC_ALL=C`.
- 2026-10-24: the reader's re-read found all four corrected claims hold. Implement complete for return 2: T8 and T9 done, `check_aria.py` 0 failures, `quarto render` clean. Status set to review.

## Decisions

## Review

Pass 1 (2026-10-24, head 83e1bae, branch contains origin/main a72e0d7).

- AC1: `python3 _tests/check_aria.py` exits 0 (32 cases on page and filter, 11 of 11 warnings). `src-li`, `src-lif`, `src-upper` each have one `src`: `https://cdn.lordicon.com/wlpxtupd.json`, `gift_raw.json`, `https://cdn.lordicon.com/wlpxtupd.json`, in the raw output and the page. The log has one warning each, naming `"src"`, `"src"`, `"SRC"`.
- AC2: the six mixed-case cases match their lowercase twins in `CASES`; the check passes them on page and filter. Raw output keeps `Aria-Hidden`, `ARIA-LABEL`, `Aria-LabelledBy`, `ROLE`, `Role`, `Aria-Label` as written.
- AC3: the six probed characters plus tab and a control byte: each `<lord-icon>` holds only `src`, `class="big"`, `id`, `aria-hidden="true"` (the call without the key), on page and filter; one warning per call naming the key.
- AC4: FAIL. The 15 cases at 64116ad have the same expected values in the current `CASES`, no fixture line of theirs changed, the check exits 0, and `quarto render` exits 0. But the branch has no `docs/` commit: the re-render changes `docs/sitemap.xml` only, and implement reverted it.
- AC5: README "Customizing" lists `src` in any case (warns, keeps the source) and the invalid-character set (warns, leaves the key out); "Accessibility" says the four ARIA names count in any case. Each matches `build_element` and `INVALID_NAME` (`[%s%c"'>/=]`).
- AC6: `_extension.yml` reads `version: 0.7.3`; `CHANGELOG.md:5` is `## 0.7.3`, with entries for the `src`, ARIA-case, and invalid-name changes.
- Gate: `cairn_validate` all checks passed. IP1 changed: `cairn_impact IP1` lists 11 references; DECISIONS lines are history, ROADMAP line 29 graduates at hygiene, line 31 still holds. Toolchain: the one version marker reads 0.7.3, the render succeeds, the changelog has the entry.

Pass 2 (2026-10-24, head 98f4c0e, branch contains origin/main a72e0d7). Code unchanged since pass 1 (T7 touched `docs/sitemap.xml` and `cairn/` only); `check_aria.py` re-run: 32 cases on page and filter, 11 of 11 warnings, 0 failures, so the pass-1 lines for AC1-AC3, AC5, AC6 stand.

- AC4: the 15 cases at 64116ad keep their expected values (pass 1), `check_aria.py` exits 0 on 98f4c0e, root `quarto render` exits 0 and leaves the tree clean, and the branch commits the re-rendered `docs/` (f38f9b3, `docs/sitemap.xml`).
- Gate: `cairn_validate` all checks passed on 98f4c0e; toolchain checks as in pass 1.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: README, CHANGELOG, and `INVALID_NAME` say a key with "a control character" is skipped, but `%c` is ASCII-only, so `"a\u0085b"=1` gives `a<U+0085>b="1"` with no warning — fix now; shows AC5 failing (README fact does not match the code), so floor return 2; AC5 unticked.
- diff-bug #2: no fixture shows a valid non-letter key (`x:y`, `@click`, `data.k`) still forwarded, so an over-broad pattern (`[^%w%-]`) passes the check — fix now (add a kept case).
- diff-bug #3: `bad-tab` adds nothing: in the raw path a tab hits `%c`, and in the render Pandoc turns it into spaces like `bad-space` — fix now (remove the case and the whitespace-run matching it needed).
- diff-bug #4: DESIGN Conventions says the render warns "once per call about the last two kinds"; the code warns once per kind per call — fix now (wording).
- diff-bug #5: no test for the plural "keys" wording or two kinds in one call — reject, false: only warning text differs, and "What gets a test" excludes cosmetic output.
- diff-bug #6: the six mixed-case ARIA twins run one code path — reject, planned change: AC2 names each case.
- diff-bug #7: `"a<b"=1` is forwarded as `a<b="1"`, an HTML parse error that browsers still read; D-003's set leaves `<` out — follow-up, new row "Decide on keys that hold a less-than".
- diff-bug #8: the warning says names cannot hold "spaces, control characters", and the log shows a key's raw control bytes — reject, false for the wording (tab and newline are control characters) and edge for the raw bytes (a key holding control bytes is outside documented and common use; the effect is odd warning text).
- diff-bug #9: `Label=` is forwarded and two keys differing only in case still clash — reject, planned change: Scope Out sends both to "Warn on keys that differ only in case".
- blame-history #1: IP5 and the stable-surface convention still require a warning release first, though D-003 narrows IP5 for these skips; the branch changed IP1 only — fix now (name the D-003 exception in IP5 and the convention).
- blame-history #2: `check_minified` looks up `colors`, `stroke`, `state` by exact case, so `Colors=` takes effect and the Minified warning stays silent — follow-up, new row "Match Minified-check keys in any case" (pre-existing, 825985a).
- blame-history #3: only exact-case `label` is reserved, unlike `src` — follow-up, absorbed by "Warn on keys that differ only in case" (it names `label` and `Label`).
- blame-history #4: IP1 says the render warns about each skipped key, but `src=""` or `"a b"=""` drop with no warning — fix now (IP1 wording: keys with a non-empty value).
- prior-review #1: `index.qmd` Accessibility text lists the four ARIA names with no letter-case rule — fix now (one sentence, re-render `docs/`).
- prior-review #2: GP5 still says an icon without `label` is `aria-hidden` — follow-up, the existing row "Reword GP5 for user ARIA precedence".
- prior-review #3: skipping invalid keys contradicts IP1's "never drops" — reject, false: the branch's IP1 text names the exception (D-003).
- prior-review #4: "Warn when a role icon has no name" is untouched — reject, false: nothing reintroduced; the row stays.
- ripple #1: DESIGN Contract boundary says the extension forwards every `key=value` — fix now.
- ripple #2: README "Both shortcodes forward any `key=value` pairs" — fix now.
- ripple #3: `lordicon.lua:8` "forwarded verbatim" — reject, false: the same comment names the exceptions four lines down.
- ripple #4: the stable-surface convention vs. skipping in 0.7.3 — fix now, with blame-history #1.
- ripple #5: DESIGN Architecture and Known issues say `check_aria.py` covers ARIA only and other behavior is checked by eye — fix now.
- ripple #6: PROFILE `verify` says `check_aria.py` "checks the ARIA attributes" — fix now.
- ripple #7: candidate "Add a render check with fixtures" still asks for `src` for `li` and `lif` and says M001 covers ARIA only — fix now (narrow the row).
- ripple #8: candidate rows "Stop duplicate src and ARIA attributes" and "Guard attribute names against bad markup" read as open — reject, planned change: step 9 hygiene graduates them.
- ripple #9: `index.qmd` ARIA text silent on letter case — fix now, with prior-review #1.
- Pass-2 fix-now lines: diff-bug #1 fixed 3ceeeda; diff-bug #2 fixed 3ceeeda; diff-bug #3 fixed 3ceeeda; diff-bug #4, blame-history #1, blame-history #4, prior-review #1, ripple #1, #2, #4, #5, #6, #7, #9 fixed 9e097db. Follow-up rows "Decide on keys that hold a less-than" and "Match Minified-check keys in any case" written 9e097db.

Pass 3 (2026-10-24, head 41f9c81, branch contains origin/main a72e0d7).

- AC1: `check_aria.py` exits 0 under the caller's locale and under `LC_ALL=C` (33 cases on page and filter, 11 of 11 warnings). Raw output: `src-li` and `src-upper` have one `src`, `https://cdn.lordicon.com/wlpxtupd.json`, and `src-lif` has `gift_raw.json`; the page matches; the log names `"src"`, `"src"`, `"SRC"` once each.
- AC2: the six mixed-case cases pass on page and filter against their lowercase twins; raw output keeps each key's spelling (spelling check, 0 failures).
- AC3: the six probed characters plus `bad-c1` (U+0085) and `bad-control` (U+0001): each icon holds only `src`, `class`, `id`, `aria-hidden` on page and filter, with one warning per call naming the key. `kept-names` keeps `@click`, `data.k`, `data-straße`, `data-datà`.
- AC4: the 15 cases at 64116ad keep their expected values and no fixture line of theirs was removed; `check_aria.py` exits 0 on 41f9c81; root `quarto render` exits 0 and leaves the tree clean; the branch commits the re-rendered `docs/` (f38f9b3, 9e097db).
- AC5: README "Customizing" lists `src` in any case (warns, keeps the source) and a key holding whitespace, a control character, `"`, `'`, `>`, `/`, or `=` (warns, leaves it out); "Accessibility" says the four ARIA names count in any case. `INVALID_NAME` (`[\0-\32\127"'>/=]`) and `C1_CONTROL` (`\194[\128-\159]`) cover ASCII whitespace and all C0 and C1 controls; `bad-c1` and `bad-control` pass.
- AC6: `version: 0.7.3`; `CHANGELOG.md` `## 0.7.3` names the three changes.
- Gate: `cairn_validate` all checks passed; `cairn_impact IP1 IP5` references reconciled (DESIGN now names the D-003 narrowing in both); the one version marker reads 0.7.3; the render succeeds; the changelog has the entry.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: an empty key, `""=1`, is written as ` ="1"`, so the page holds an attribute named `="1"`, with no warning — fix now: D-003 skips any key HTML does not allow as a name, and a name cannot be empty.
- diff-bug #2: the README bullet saying `label` is not passed on has no test; removing `label` from `RESERVED` passes — fix now (the `label` case becomes exact).
- diff-bug #3: no fixture has two skipped keys of one kind, or both kinds, in one call — reject, false: only warning count and text differ, and "What gets a test" excludes cosmetic output (as pass-2 diff-bug #5).
- diff-bug #4: DEL (U+007F) and other C0 members are untested — reject, false: one `find` over one class is one code path, and `bad-control` and `bad-space` run it.
- diff-bug #5: four mixed-case ARIA cases run one path — reject, planned change: AC2 names each case.
- diff-bug #6: `key:lower()` follows the locale; under glibc's tr_TR.ISO-8859-9, `I` lowers to 0xFD, so `ARIA-LABEL` would not match — fix now (an ASCII-only lowercase helper).
- diff-bug #7: the UTF-8 half of the locale check catches the old `%s%c` pattern only where the C library classifies bytes 128 and up (macOS, not glibc) — fix now (the comment says so).
- diff-bug #8: noncharacter keys such as U+FFFE pass through with no warning — follow-up, absorbed by "Decide on keys that hold a less-than".
- diff-bug #9: `"a<b"=1` is forwarded — follow-up, the row "Decide on keys that hold a less-than".
- diff-bug #10: no test that an empty-value `src` or invalid key stays silent — reject, false: only warning output differs (cosmetic).
- diff-bug #11: DESIGN's forwarding bullet leaves out empty-value keys, which README lists — fix now.
- diff-bug #12: a test comment names `INVALID_NAME` and `C1_CONTROL` — reject, style.
- blame-history #1: `Label` is not reserved in any case — follow-up, absorbed by "Warn on keys that differ only in case".
- blame-history #2: `check_minified` matches by exact case — follow-up, the row "Match Minified-check keys in any case".
- blame-history #3: IP1 now drops keys, and D-003's rationale is loose for `src` — reject, false: D-003 records the narrowing, and the warning is the change for `src`.
- blame-history #4: `"a<b"=1` is forwarded — follow-up, the row "Decide on keys that hold a less-than".
- prior-review #1: the ROADMAP row "Stop duplicate src and ARIA attributes" reads as open — reject, planned change: step 9 hygiene graduates it.
- prior-review #2: `lordicon.lua:8` "forwarded verbatim" — reject, false: the same comment names the exceptions.
- ripple #1, #2: the rows "Stop duplicate src and ARIA attributes" and "Guard attribute names against bad markup" read as open — reject, planned change: step 9 hygiene graduates them.
- ripple #3: `lordicon.lua:8` "verbatim" — reject, false (as prior-review #2).
- ripple #4: `check_aria.py` docstring "Exits 1 when a case fails" — fix now (any check).
- ripple #5: the `RESERVED` comment does not cover the `src` and invalid-name skips — reject, false: it describes `label`, which is handled specially, and claims nothing about other skips.
- ripple #6: DESIGN Contract boundary allows behavior "in two cases only" — reject, false: both skips are guardrails for silent failures (a second `src` that is ignored, a broken element).
