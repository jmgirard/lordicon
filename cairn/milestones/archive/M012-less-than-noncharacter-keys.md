# M012: Skip keys that hold a less-than or a noncharacter

**Status:** done (2026-10-26, PR #16 https://github.com/jmgirard/lordicon/pull/16)

**Goal:** A shortcode key that holds `<` or a Unicode noncharacter is left out of the `<lord-icon>` element with the invalid-name warning, instead of being forwarded as an attribute name that HTML flags or forbids.

**Outcome:** Version 0.7.11. `invalid_name` in `lordicon.lua` adds `<` to `INVALID_NAME` and checks a new `NONCHARACTERS` table of three UTF-8 byte patterns (U+FDD0–U+FDEF; U+FFFE, U+FFFF; U+nFFFE, U+nFFFF for planes 1–16). The invalid-name warning's reason now names noncharacters and says HTML parsers report a `<` in a name as an error. Before, `a<b=1` gave `a<b="1"`. `_tests/aria.qmd` gained 66 noncharacter calls (key position rotating), the four `<` forms on their own line and inline (inline under `li ltinline`, so warnings differ), a `lif` call, and `kept-neighbors` with 16 code points next to or one byte from a noncharacter. `check_aria.py` builds the 66 from Infra §4.6 and models `invalid_name`. README, CHANGELOG 0.7.11, DESIGN Conventions, IP1, IP5. Source notes `whatwg-html.md` and `whatwg-infra.md`.

**Decisions:** D-006 (skip keys with `<` or a noncharacter; narrows IP1 and IP5; extends D-003). The user chose skipping both at the plan gate and declined a Fable review at the escalation offer.

**Review:** four-lens fan-out after a criteria audit (9 items) and a claim audit (23 claims, 0 false); 23 findings: 12 fixed (inline `<` twins shared warning text, a lead-byte neighbor gap, stale comments in `lordicon.lua`, two test comments restating code, the DESIGN stable-surface bullet, the CHANGELOG format limit, the README noncharacter definition), 11 rejected (5 false, 3 planned, 3 style), 0 follow-ups. Graduated candidate row "Decide on keys that hold a less-than". Captured 1 lesson; marked 9 lessons used.
