# M003: Stop key clashes and bad attribute names

- **Status:** in-progress
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

- [ ] AC1: Fixture calls pass a `src` key to `li` and to `lif`, and an `SRC` key to `li`. Each gives a `<lord-icon>` with one `src` attribute, holding the first argument's source, in the raw filter output and the rendered page. The fixture render's log holds one warning per such call, naming its key. `python3 _tests/check_aria.py` reports each. (RB tripwire: ip-touching)
- [ ] AC2: For each of `role`, `aria-hidden`, `aria-label`, and `aria-labelledby`, a fixture call passes the name in mixed or upper case with no `label`. Fixture calls also pass `Role` and `Aria-Label` with `label`. Each gives the ARIA attributes that the same call with all-lowercase keys gives, with names compared without regard to case. The raw filter output holds each key as the user wrote it. `python3 _tests/check_aria.py` reports each case in the raw filter output and the rendered page.
- [ ] AC3: For each of a space, `"`, `'`, `>`, `/`, and `=`, a fixture call has a key that holds that character. Its `<lord-icon>` has no attribute from that key, and its other attributes match the same call without that key, in the raw filter output and the rendered page. The fixture render's log holds one warning per such call, naming the key. `python3 _tests/check_aria.py` reports each. (RB tripwire: ip-touching)
- [ ] AC4: The 15 fixture cases that `_tests/check_aria.py` checks at 64116ad give the same ARIA attributes, and `python3 _tests/check_aria.py` exits 0 on the review head. `quarto render` at the repo root succeeds, and this milestone commits the re-rendered `docs/`.
- [ ] AC5: The README section on forwarded `key=value` pairs states three facts that match the filter code. A `src` key in any letter case is not forwarded, and the render warns. The four ARIA names override the defaults in any letter case. A key holding whitespace, a control character, `"`, `'`, `>`, `/`, or `=` is skipped, and the render warns.
- [ ] AC6: `version:` in `_extensions/lordicon/_extension.yml` reads `0.7.3`. `CHANGELOG.md` has a `## 0.7.3` section that names the changes of AC1, AC2, and AC3.

## Coverage

- AC1 → T1, T2, T3, T4
- AC2 → T2, T3, T4
- AC3 → T1, T2, T3, T4
- AC4 → T3, T4, T5
- AC5 → T5
- AC6 → T6

## Tasks

- [ ] T1: Change the DESIGN.md IP1 text and the forwarding Conventions bullet to name the `src` and invalid-name exceptions (D-003).
- [ ] T2: Extend the harness. `check_aria.py` keeps the fixture render's stderr and checks the warning lines. `fixture_calls()` keeps a quoted key that holds `=` whole. A raw-string check confirms that the filter output keeps each key's spelling.
- [ ] T3: Add the AC1 to AC3 cases to `_tests/aria.qmd` and their expected values to `CASES`. Run the check and see each new case fail on the current filter.
- [ ] T4: Change `build_element`: reserve `src` by `key:lower()` with a per-call warning, compare ARIA override names by `key:lower()`, and skip invalid names with a per-call warning. The check passes.
- [ ] T5: Update the README forwarding section. Run `quarto render` and commit `docs/`. Look at the changed demo pages in a browser, as the PROFILE `verify` slot asks.
- [ ] T6: Raise `version:` to 0.7.3 (D-001) and add the `## 0.7.3` section to `CHANGELOG.md`. `BUNDLE_VERSION` stays, because the player does not change.

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

## Decisions

## Review
