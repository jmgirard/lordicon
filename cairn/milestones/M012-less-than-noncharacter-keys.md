# M012: Skip keys that hold a less-than or a noncharacter

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP5, GP2
- **Resolves:** —
- **Surface tier:** user-facing — it changes which shortcode keys reach the `<lord-icon>` element in users' pages
- **Branch/PR:** m012-less-than-noncharacter-keys

## Goal

A shortcode key that holds `<` or a Unicode noncharacter is left out of the `<lord-icon>` element with the invalid-name warning, instead of being forwarded as an attribute name that HTML flags or forbids.

## Scope

**In:** `<` and the 66 noncharacters that whatwg-infra (§4.6 Code points) defines join the characters that make a key invalid in `invalid_name` (`_extensions/lordicon/lordicon.lua:97`), so such a key is skipped with the existing invalid-name warning. The warning's reason and README say in plain words that HTML forbids noncharacters in a name (whatwg-html §13.1.2.3) and that parsers flag `<` as an error (whatwg-html §13.2.2). Fixture cases in `_tests/aria.qmd` and checks in `_tests/check_aria.py`. README, CHANGELOG 0.7.11, the version, DESIGN.md (Conventions, IP1, IP5), a D-entry, two source notes, and the re-rendered `docs/`.

**Out:** Other characters that HTML parsers accept but flag, such as a lone surrogate or invalid UTF-8 in a key: no row, since none was reported, and a reader can add one. Byte-order sorting of keys stays the candidate row "Sort keys by byte, not by locale". A separate warning kind for these keys: not planned, because the user's fix is the same rename.

## Acceptance criteria

- [x] AC1: In `_tests/aria.qmd`, 66 calls, one for each of the 66 noncharacters that whatwg-infra (§4.6 Code points) defines, and calls whose `<` key has `<` first, in the middle, last, and as the whole key, each give an element that lacks that key and keeps the call's other keys. The noncharacter's position in its key rotates among first, middle, last, and whole across the 66 calls. Each `<` form, and the U+FFFE and U+10FFFF calls, also appears inside a paragraph, and one `lif` call holds a `<` key and a noncharacter key. The raw filter output decides each case, and the rendered HTML page shows the same, as `python3 _tests/check_aria.py` checks.
- [x] AC2: Each call of AC1 gives one lordicon warning in the render log that names its skipped keys in quotes, as the key is written. The warning's reason says in plain words that HTML forbids Unicode noncharacters, such as U+FFFE, in an attribute name and that HTML parsers flag `<` as an error, as `python3 _tests/check_aria.py` checks.
- [x] AC3: Keys that hold one of these code points reach the element unchanged and give no invalid-name warning, as `python3 _tests/check_aria.py` checks: U+FDCF, U+FDF0, U+FFFD, U+1FFFD, U+10FFFD (next to a noncharacter range); U+FD90, U+FE10, U+FFBE, U+1EFFE, U+1FFBE, U+20FFE (one UTF-8 byte away from a noncharacter); U+4FFFD, U+EFFFD, U+10000.
- [x] AC4: README's list of keys that do not reach the icon and a CHANGELOG `## 0.7.11` entry name `<` and noncharacters, and say that parsers flag `<` while HTML forbids noncharacters. `_extensions/lordicon/_extension.yml` reads `version: 0.7.11`.
- [x] AC5: The profile's `verify` slot is clean on the review head: `python3 _tests/check_aria.py` exits 0, and `quarto render` at the repo root succeeds with the re-rendered `docs/` committed.

## Coverage

- AC1 → T2, T3
- AC2 → T2, T3
- AC3 → T2, T3
- AC4 → T4
- AC5 → T2, T3, T5

## Tasks

- [x] T1: Write source notes `cairn/references/whatwg-html.md` (§13.1.2.3 Attributes, the attribute-name rule that excludes noncharacters; §13.2.2 Parse errors, `unexpected-character-in-attribute-name` for `<`) and `cairn/references/whatwg-infra.md` (§4.6 Code points, the noncharacter definition), each with its `INDEX.md` line.
- [x] T2: Tests first. Add the AC1 and AC3 cases to `_tests/aria.qmd`, each with a kept key beside the tested one. Write the non-ASCII keys with a short script and confirm the bytes with `od -c`. In `check_aria.py`, build the 66 code points from the §4.6 ranges, not from the filter's pattern, extend its `INVALID_NAME` model, split the render log on `"\n"` with `LC_ALL` set, and see the new checks fail before T3.
- [x] T3: In `lordicon.lua`, extend `invalid_name` with `<` and byte patterns for the UTF-8 forms of the noncharacters (U+FDD0–U+FDEF, U+FFFE, U+FFFF, and U+nFFFE, U+nFFFF for planes 1–16), spelled as byte ranges, not `%` classes. Update the invalid-name warning's reason text and the comments above `INVALID_NAME`.
- [x] T4: Raise the version to 0.7.11, add the CHANGELOG entry, and update README's skipped-key list. Update DESIGN.md Conventions, IP1, and IP5 to name `<` and noncharacters. Append a D-entry that records the user's decision and narrows IP1 and IP5. Its IP5 reason is its own, not D-003's: a `<` key such as `a<b` did give an attribute, but no `<lord-icon>` attribute has such a name. It also says the warning is IP1's warning for a skipped key, not a GP2 guardrail. (RB tripwire: ip-touching)
- [x] T5: Run `quarto render` at the repo root and commit `docs/`, `sitemap.xml` included.

## Work log

- 2026-10-26: created by /milestone-plan.
- 2026-10-26: tier check: not run — work named at the question set.
- 2026-10-26: question set: which candidate to plan — "Decide on keys that hold a less-than"; what such a key should do — skip `<` and noncharacter keys with the invalid-name warning, starting in the next version with no warning release first.
- 2026-10-26: idea vet: one concern, that `<` is allowed by HTML's attribute-name rule (§13.1.2.3) and only flagged by parsers (§13.2.2); the question set posed it as the "skip noncharacters only" option, and the user chose to skip both.
- 2026-10-26: lessons used: 2026-10-24 (M003) byte ranges in Lua patterns; 2026-10-24 (M003) split tool output on "\n" with LC_ALL; 2026-10-25 (M008) write non-ASCII fixture keys with a script and `od -c`; 2026-10-25 (M009) test a call inline and on its own line; 2026-10-20 (M001) read raw filter output; 2026-10-20 (M002) commit the sitemap with `docs/`.
- 2026-10-26: collision check: absorbs candidate row "Decide on keys that hold a less-than" in full; extends D-003's skip set, so T4 adds a D-entry with its own reason; no planned or in-progress milestone overlaps; the archive (M003) shipped the current skip set.
- 2026-10-26: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-26: probes on Quarto 1.10.19: `<` keys (first, middle, last, whole) and keys holding U+FFFE, U+FDD0, U+FDEF, U+1FFFE, U+10FFFF reach the page unchanged; a warning that names a U+FFFE or U+10FFFF key keeps the key's bytes in the render log.
- 2026-10-26: criteria audit (full mode, fresh Opus reader): 9 items. Fixed: AC1 now counts 66 calls and varies the bad character's position, inline calls, and `lif`; AC2 states the reason in plain words and that the log keeps the key's bytes (probed); AC2 and AC4 separate `<` (flagged) from noncharacters (forbidden); AC3 adds neighbors one UTF-8 byte away and planes 4-15; AC1 names the raw filter output as the deciding check; T2 adds the "\n" and LC_ALL split. Answered: the DESIGN.md and D-entry edits stay in T4, not a criterion, because they are tracking records; T4 now names the D-entry's own IP5 reason and its GP2 note. No finding on AC5 or on task-lesson conflicts.
- 2026-10-26: plan gate chose skipping both `<` and noncharacter keys over skipping only noncharacters, because parsers report `<` in a name as an error and no `<lord-icon>` attribute needs it; falsified by a user report of a working attribute whose name holds `<`.
- 2026-10-26: plan chose reusing the invalid-name warning over a new warning kind, because the user's fix is the same rename; falsified by a user report that the shared warning text misleads.
- 2026-10-26: implement started on branch m012-less-than-noncharacter-keys, cut from main at 8e88928; `.DS_Store` stays untracked and unstaged.
- 2026-10-26: T1 done: source notes whatwg-html.md (§13.1.2.3, §13.2.2, §13.2.5.33) and whatwg-infra.md (§4.6) from pages fetched with curl, with INDEX lines; no code, so no verify run.
- 2026-10-26: T2 checkpoint, red by design until T3: 85 fixture calls added to `_tests/aria.qmd` by a script (bytes confirmed with `od -c`); `check_aria.py` builds the 66 code points from the §4.6 ranges and adds `invalid_name`; on the unchanged filter it gives 237 failures (154 kept `<` or noncharacter attributes, 83 missing warnings) and none for `kept-neighbors`. The render log was already split on "\n" under `LC_ALL=C.UTF-8`.
- 2026-10-26: correction to the T2 line: the 83 were log failures (82 case groups plus the total count), not 83 missing warnings.
- 2026-10-26: T2 and T3 done: `invalid_name` adds `<` to `INVALID_NAME` and checks three UTF-8 byte patterns in a new `NONCHARACTERS` table; the warning's reason names noncharacters and `<`. `check_aria.py` 0 failures (170 cases, 130 warnings). A planted second-byte range `[\143-\191]` gave 7 failures on `kept-neighbors` (U+1EFFE, U+20FFE) and was reverted. The `quarto render` of the verify slot runs at T5.
- 2026-10-26: implementation choice: noncharacter patterns kept in a table beside `INVALID_NAME`, rather than one pattern, because Lua patterns have no alternation.
- 2026-10-26: T4 escalation offer (ip-touching): the user chose to write the drafted text without a Fable review.
- 2026-10-26: T4 done: version 0.7.11, CHANGELOG 0.7.11 entry, README skipped-key list (noncharacters with the forbidden characters, `<` in its own item), DESIGN Conventions, IP1, IP5, and the Known issues milestone list, and D-006. `check_aria.py` 0 failures; `cairn_validate` passes. Pre-existing README lint hits from the simple-english hook are outside this change and left alone.
- 2026-10-26: T5 done: `quarto render` at the repo root exited 0 with no warning; only `docs/sitemap.xml` changed, so no demo page needed a browser look.
- 2026-10-26: claim audit: 23 claims read, 0 corrected — lordicon.lua, check_aria.py, aria.qmd, README.md, CHANGELOG.md, _extension.yml. The reader's Infra §4.6 claim rested on recall, and T1's source note verified it against the fetched spec.
- 2026-10-26: implement complete; status set to review.

## Decisions

## Review

- Review pass 1, 2026-10-26, on branch head 1d2944e, level with origin/main 8e88928; no PR yet (route d); Copilot round off.
- AC1 evidence: `python3 _tests/check_aria.py` exit 0 (170 cases on the page and in the raw filter output, 0 failures; `EXACT` fails a kept `<` or noncharacter attribute). Fixture count: 66 own-line `nc-` calls hold 66 distinct noncharacters equal to the §4.6 set, in forms first 17, middle 17, last 16, whole 16; `lt-first`, `lt-middle`, `lt-last`, `lt-whole` each once on their own line and once inline; `nc-fffe-inline`, `nc-10ffff-inline`, and `lt-nc-lif` once each. T2's red run on the unchanged filter showed 154 kept-attribute failures for these cases.
- AC2 evidence: the same run reads 130 lordicon warnings, 130 expected. Each `BAD` case and `lt-nc-lif` must match one log line holding its call, `skips the`, its quoted key as written, "or Unicode noncharacters such as U+FFFE.", and "HTML parsers also report a < in a name as an error."; the total count fails any extra warning.
- AC3 evidence: the same run passes `kept-neighbors`, an `EXACT` case whose 14 `data-<hex><code point>` keys for U+FDCF, U+FDF0, U+FFFD, U+1FFFD, U+10FFFD, U+FD90, U+FE10, U+FFBE, U+1EFFE, U+1FFBE, U+20FFE, U+4FFFD, U+EFFFD, U+10000 each hold their value on the page and in the filter output, with no warning for the call. T3's planted range `[\143-\191]` made this case fail (U+1EFFE, U+20FFE).
- AC4 evidence: README.md:91-96 lists "a Unicode noncharacter such as U+FFFE" with the forbidden characters ("HTML does not allow such an attribute name") and `<` in its own item ("HTML parsers report a `<` in an attribute name as an error"); CHANGELOG.md:5-7 has `## 0.7.11` naming `<` and noncharacters, that HTML does not allow a noncharacter, and that parsers report `<` as an error; `_extensions/lordicon/_extension.yml:3` reads `version: 0.7.11`.
- AC5 evidence: on head 1d2944e, `python3 _tests/check_aria.py` exit 0, and `quarto render` at the repo root exit 0 leaving `git status` with no change under `docs/` (cbd20b0 committed the re-render); no demo page changed, so no browser look was owed.
- Gate: `cairn_validate.py` exit 0, all checks passed. `cairn_impact.py --changed` compares against HEAD and reported none, so `cairn_impact.py IP1 IP5` ran instead: outside this milestone and history, DESIGN.md:90 and :107 are the edited principles, DESIGN.md:139 (GP5 citing IP1) is unaffected, and ROADMAP.md:31's list of IP1 exceptions was reconciled to name keys with `<` (corrected M012). Toolchain: the one version marker, `_extension.yml`, reads 0.7.11; the verify render succeeds (AC5); CHANGELOG has the 0.7.11 entry.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: each own-line `<` case and its inline twin share a call and a key, so `check_warnings` cannot tell a doubled warning from a missing one — fix now: the inline `<` cases call `li ltinline`, so their warnings name another call.
- diff-bug #2: no kept neighbor differs from a noncharacter only in the lead byte, so `[\238\239]\183` would pass — fix now: `kept-neighbors` adds U+EDD0 and U+EFFE; a planted `[\238\239]` made it fail (4 failures) and was reverted.
- diff-bug #3: the four-byte pattern also matches the invalid runs F0 8F and F4 9F/AF/BF — reject (false): Pandoc reads a file that is not valid UTF-8 as Latin-1 (probed with byte FF), so no such run reaches the filter.
- diff-bug #4: the comment above `INVALID_NAME` still says every listed symbol makes the name invalid, though `<` does not — fix now.
- diff-bug #5: the `build_element` comment says an invalid name gives a broken or stray attribute, which a `<` key does not — fix now: "broken, stray, or flagged".
- diff-bug #6: "also" in "HTML parsers also report a < in a name as an error" can read as covering the earlier characters — reject (style): the sentence names only `<`, and AC2 fixes the reason's content.
- diff-bug #7: the candidate row "Decide on keys that hold a less-than" is still listed — reject (planned change): its ` — started M012` token marks it for removal at post-merge hygiene.
- diff-bug #8: the `EXACT` line is about 120 characters — reject (style); wrapped anyway with the #2 fix.
- diff-bug test rule: the 30 interior `U+FDD1`–`U+FDEE` calls, the noncharacter position rotation, and the `lif` call repeat a code path — reject (planned change): AC1 names each of them.
- diff-bug test rule: two `check_aria.py` comments restate the code below them ("The fixture cycles…", "A lif call skips both kinds of key") — fix now: both removed.
- ripple #1: ROADMAP.md:29 still says `<` and noncharacter keys pass through — reject (planned change): same row as diff-bug #7, removed at hygiene.
- ripple #2: DESIGN.md Conventions says only "D-003 narrows this" for the stable surface — fix now: names D-005 and D-006 (corrected M012).
- ripple #3: the comment over `invalid_name` says "a key that HTML does not allow" — fix now: adds "or that holds a `<`".
- ripple #4: the `INVALID_NAME` comment says the set ends a tag early — fix now, same edit as diff-bug #4.
- ripple #5: the file header names one class, "keys that are not valid attribute names" — fix now: adds "or hold a `<`".
- prior-review #1: the `<` twins share warning text (echoes M011's row "Match each warning to its own call") — fix now, same as diff-bug #1.
- prior-review #2: the CHANGELOG 0.7.11 entry says "the render warns" with no format limit, though only HTML output warns (echoes M011's changelog overclaim fix) — fix now: "In HTML output, the render warns."
- prior-review #3: README names "a Unicode noncharacter such as U+FFFE" without saying which code points — fix now: README names U+FDD0 to U+FDEF and the last two code points of each plane.
- prior-review #4: the `lt-nc-lif` expectation relies on the key sort order — reject (false): the keys differ in their first byte (`a` against `x`), and Quarto's collation is `C` (observed 2026-10-26), so the order cannot change.
- blame-history #1: D-006's reason that no `<lord-icon>` attribute has such a name was not checked — reject (false): the bundle's `observedAttributes` list is colors, src, state, trigger, loading, target, stroke, speed.
- blame-history #2: the candidate row is still listed — reject (planned change), same as diff-bug #7.
- blame-history #3: a tool that strips noncharacters from `aria.qmd` would change the keys under test — reject (false): stripped keys would be valid, so `EXACT` and the warning count fail, and the review's count found all 66.
- blame-history #4: odd line wrapping in the DESIGN IP1 and IP5 hunks — reject (style).
- After the fixes: `python3 _tests/check_aria.py` 0 failures (170 cases, 130 warnings).
