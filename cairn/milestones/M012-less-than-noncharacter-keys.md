# M012: Skip keys that hold a less-than or a noncharacter

- **Status:** in-progress
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

- [ ] AC1: In `_tests/aria.qmd`, 66 calls, one for each of the 66 noncharacters that whatwg-infra (§4.6 Code points) defines, and calls whose `<` key has `<` first, in the middle, last, and as the whole key, each give an element that lacks that key and keeps the call's other keys. The noncharacter's position in its key rotates among first, middle, last, and whole across the 66 calls. Each `<` form, and the U+FFFE and U+10FFFF calls, also appears inside a paragraph, and one `lif` call holds a `<` key and a noncharacter key. The raw filter output decides each case, and the rendered HTML page shows the same, as `python3 _tests/check_aria.py` checks.
- [ ] AC2: Each call of AC1 gives one lordicon warning in the render log that names its skipped keys in quotes, as the key is written. The warning's reason says in plain words that HTML forbids Unicode noncharacters, such as U+FFFE, in an attribute name and that HTML parsers flag `<` as an error, as `python3 _tests/check_aria.py` checks.
- [ ] AC3: Keys that hold one of these code points reach the element unchanged and give no invalid-name warning, as `python3 _tests/check_aria.py` checks: U+FDCF, U+FDF0, U+FFFD, U+1FFFD, U+10FFFD (next to a noncharacter range); U+FD90, U+FE10, U+FFBE, U+1EFFE, U+1FFBE, U+20FFE (one UTF-8 byte away from a noncharacter); U+4FFFD, U+EFFFD, U+10000.
- [ ] AC4: README's list of keys that do not reach the icon and a CHANGELOG `## 0.7.11` entry name `<` and noncharacters, and say that parsers flag `<` while HTML forbids noncharacters. `_extensions/lordicon/_extension.yml` reads `version: 0.7.11`.
- [ ] AC5: The profile's `verify` slot is clean on the review head: `python3 _tests/check_aria.py` exits 0, and `quarto render` at the repo root succeeds with the re-rendered `docs/` committed.

## Coverage

- AC1 → T2, T3
- AC2 → T2, T3
- AC3 → T2, T3
- AC4 → T4
- AC5 → T2, T3, T5

## Tasks

- [x] T1: Write source notes `cairn/references/whatwg-html.md` (§13.1.2.3 Attributes, the attribute-name rule that excludes noncharacters; §13.2.2 Parse errors, `unexpected-character-in-attribute-name` for `<`) and `cairn/references/whatwg-infra.md` (§4.6 Code points, the noncharacter definition), each with its `INDEX.md` line.
- [ ] T2: Tests first. Add the AC1 and AC3 cases to `_tests/aria.qmd`, each with a kept key beside the tested one. Write the non-ASCII keys with a short script and confirm the bytes with `od -c`. In `check_aria.py`, build the 66 code points from the §4.6 ranges, not from the filter's pattern, extend its `INVALID_NAME` model, split the render log on `"\n"` with `LC_ALL` set, and see the new checks fail before T3.
- [ ] T3: In `lordicon.lua`, extend `invalid_name` with `<` and byte patterns for the UTF-8 forms of the noncharacters (U+FDD0–U+FDEF, U+FFFE, U+FFFF, and U+nFFFE, U+nFFFF for planes 1–16), spelled as byte ranges, not `%` classes. Update the invalid-name warning's reason text and the comments above `INVALID_NAME`.
- [ ] T4: Raise the version to 0.7.11, add the CHANGELOG entry, and update README's skipped-key list. Update DESIGN.md Conventions, IP1, and IP5 to name `<` and noncharacters. Append a D-entry that records the user's decision and narrows IP1 and IP5. Its IP5 reason is its own, not D-003's: a `<` key such as `a<b` did give an attribute, but no `<lord-icon>` attribute has such a name. It also says the warning is IP1's warning for a skipped key, not a GP2 guardrail. (RB tripwire: ip-touching)
- [ ] T5: Run `quarto render` at the repo root and commit `docs/`, `sitemap.xml` included.

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

## Decisions

## Review
