# M003: Stop key clashes and bad attribute names

**Status:** done (2026-10-24, PR #7 https://github.com/jmgirard/lordicon/pull/7)

**Goal:** A user `src` key, a mixed-case ARIA key, or a key that HTML does not allow as an attribute name no longer gives a second `src`, a kept `aria-hidden` default, or broken markup.

**Outcome:** `build_element` in `lordicon.lua` skips `src` in any case and
invalid names (empty, `INVALID_NAME` `[\0-\32\127"'>/=]`, `C1_CONTROL`
`\194[\128-\159]`) with one warning per kind per call, naming the call
(`{{< li CODE >}}`) and each key. Byte ranges replace `%s%c`, and
`ascii_lower` replaces `string.lower`, so neither follows the locale. `passed`
holds lowercase names, so the four ARIA overrides match in any case.
`check_aria.py` checks 34 cases (exact attributes, kept keys, key spelling,
warnings) with the page under `C.UTF-8` and the raw output under `C`. DESIGN
IP1 and IP5 name the D-003 narrowing; README, `index.qmd`, CHANGELOG 0.7.3.

**Decisions:** none promoted (D-003 was made at plan). The user declined the
tripwire escalation for AC1 and AC3.

**Review:** three passes, four-lens fan-out each. Return 1: no `docs/` commit
(AC4). Return 2: C1 controls forwarded (AC5); its fix found `%s%c` skipping
`data-straße` under UTF-8. 50 findings: 20 fixed, 9 follow-ups, 21 rejected.
New rows "Match Minified-check keys in any case" and "Decide on keys that hold
a less-than". Hygiene graduated "Stop duplicate src and ARIA attributes" and
"Guard attribute names against bad markup".
