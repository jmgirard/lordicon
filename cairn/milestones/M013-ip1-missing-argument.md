# M013: Name a missing first argument and Quarto's drops in IP1

- **Status:** planned
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Resolves:** —
- **Surface tier:** internal — the diff changes only design and decision records under `cairn/`
- **Branch/PR:** —

## Goal

IP1 names a call with no first argument as a call whose keys reach no element, and says that Quarto's own drops are outside the extension.

## Scope

**In:** A D-007 entry in `cairn/DECISIONS.md` that records the user's choice at the M013 plan gate and extends D-005. The IP1 text in `cairn/DESIGN.md`: a call whose first argument is missing joins a call whose first argument is empty, and one new sentence says that a value or positional argument that Quarto drops before the extension runs never reaches the extension and is not an IP1 exception.

**Out:** Code, README, `index.qmd`, CHANGELOG, and version changes: the behavior shipped in 0.7.9, and README already documents Quarto's drops. IP5 does not change (D-007 gives the reason). A warning for an argument that Quarto shifts left stays the candidate row "Warn when Quarto shifts arguments left".

## Acceptance criteria

- [ ] AC1: IP1 in `cairn/DESIGN.md` names a call whose first argument is missing, beside a call whose first argument is empty, as a call that makes no element so that its keys reach none, and cites D-007.
- [ ] AC2: IP1 in `cairn/DESIGN.md` states that a value or positional argument that Quarto drops before the extension runs, one that starts with a space or tab, never reaches the extension and is not one of IP1's exceptions.
- [ ] AC3: `cairn/DECISIONS.md` ends with D-007, which records the user's choice at the M013 plan gate, names both IP1 changes, and states that IP5 does not change and why.
- [ ] AC4: `git diff --name-only origin/main...HEAD` on the milestone branch lists only paths under `cairn/`.

## Coverage

- AC1 → T2
- AC2 → T2
- AC3 → T1
- AC4 → T1, T2, T3

## Tasks

- [ ] T1: Append D-007 to `cairn/DECISIONS.md`: context (a call with no first argument makes no element since 0.7.9, and D-005's Consequences left it to the candidate row), the user's choice of both changes, and that IP5 does not change because such a call stopped the render before 0.7.9, so no working output broke.
- [ ] T2: Edit IP1 in `cairn/DESIGN.md` (line 91): "first argument is empty" becomes "first argument is missing or empty" in both places, the closing citation becomes "(D-005, D-007)", and add the sentence for AC2 with a D-007 citation.
- [ ] T3: Run `python3 /Users/jmgirard/.claude/skills/cairn/scripts/cairn_validate.py` and `git diff --name-only origin/main...HEAD`, and confirm that the second lists only `cairn/` paths.

## Work log

- 2026-10-26: created by /milestone-plan.
- 2026-10-26: tier check: not run — work named at the question set.
- 2026-10-26: idea vet: found no concern; the new IP1 text describes behavior the filter has had since 0.7.9, and D-005 left the question to the candidate row.
- 2026-10-26: lessons used: none.
- 2026-10-26: collision check: absorbs candidate row "Decide whether IP1 names Quarto's drops"; extends D-005, whose Consequences hand this question to that row; D-003 and D-006 are unaffected. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-26: question set: which candidate to plan — "Decide whether IP1 names Quarto's drops"; how IP1 treats the two cases — name both.
- 2026-10-26: plan gate chose naming both cases over naming only the missing argument, because IP1 otherwise reads as if the extension passes on values that Quarto drops; falsified by a Quarto version that hands such values to the filter.
- 2026-10-26: plan chose to leave IP5 unchanged over adding a D-007 narrowing, because a call with no first argument stopped the render before 0.7.9 and broke no working output; falsified by a release before 0.7.9 in which such a call rendered an element.
- 2026-10-26: criteria audit (reduced mode, fresh Opus reader): 12 checks over AC1–AC4, 0 findings.
- 2026-10-26: no changelog entry and no version change, because nothing user-visible changes (D-001, D-002).

## Decisions

## Review
