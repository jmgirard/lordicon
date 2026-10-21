# M001: Let user ARIA attributes beat defaults

**Status:** done (2026-10-20, PR #5 https://github.com/jmgirard/lordicon/pull/5)

**Goal:** The extension's ARIA defaults give way to ARIA attributes that the user passes.

**Outcome:** `build_element` in `lordicon.lua` keeps an `ARIA_OVERRIDES` set
(`aria-hidden`, `aria-label`, `aria-labelledby`, `role`) and a `passed` set of
non-empty user keys (lowercase match). With no `label`, a passed override key
turns off `aria-hidden="true"`. With `label`, `role="img"` and `aria-label` are
added only where the user passed none. `_tests/check_aria.py` (named in PROFILE
`verify`) checks 15 cases from `_tests/aria.qmd` in the rendered page and in raw
filter output from `_tests/raw_output.lua` (`quarto pandoc lua`, stubbed
`quarto`). `_quarto.yml` gained `render: ["*.qmd"]`, keeping `cairn/` out of
`docs/`. README and `index.qmd` document the rule. Version 0.7.1 → 0.7.2 (D-001).

**Decisions:** none promoted. The question set chose the four named attributes,
a silent user win over `label`, and a fixture check over checking by eye.

**Review:** four-lens fan-out, 22 findings: 7 fixed (8fe774b, among them the raw
filter stage), 4 follow-ups, 10 rejected, 1 noted. New candidate rows: "Reword
GP5 for user ARIA precedence", "Warn when a role icon has no name", "Guard
attribute names against bad markup". Hygiene graduated "Let user ARIA attributes
beat defaults" and narrowed "Add a render check with fixtures" to non-ARIA work.
