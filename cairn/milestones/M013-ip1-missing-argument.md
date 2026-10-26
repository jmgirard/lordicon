# M013: Name a missing first argument and Quarto's drops in IP1

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1
- **Resolves:** —
- **Surface tier:** internal — the diff changes only design and decision records under `cairn/`
- **Branch/PR:** m013-ip1-missing-argument

## Goal

IP1 names a call with no first argument as a call whose keys reach no element, and says that Quarto's own drops are outside the extension.

## Scope

**In:** A D-007 entry in `cairn/DECISIONS.md` that records the user's choice at the M013 plan gate and extends D-005. The IP1 text in `cairn/DESIGN.md`: a call whose first argument is missing joins a call whose first argument is empty, and one new sentence says that a value or positional argument that Quarto drops before the extension runs never reaches the extension and is not an IP1 exception.

**Out:** Code, README, `index.qmd`, CHANGELOG, and version changes: the behavior shipped in 0.7.9, and README already documents Quarto's drops. IP5 does not change (D-007 gives the reason). A warning for an argument that Quarto shifts left stays the candidate row "Warn when Quarto shifts arguments left".

## Acceptance criteria

- [x] AC1: IP1 in `cairn/DESIGN.md` names a call whose first argument is missing, beside a call whose first argument is empty, as a call that makes no element so that its keys reach none, and cites D-007.
- [x] AC2: IP1 in `cairn/DESIGN.md` states that a value or positional argument that Quarto drops before the extension runs, one that starts with a space or tab, never reaches the extension and is not one of IP1's exceptions.
- [x] AC3: `cairn/DECISIONS.md` ends with D-007, which records the user's choice at the M013 plan gate, names both IP1 changes, and states that IP5 does not change and why.
- [x] AC4: `git diff --name-only origin/main...HEAD` on the milestone branch lists only paths under `cairn/`.

## Coverage

- AC1 → T2
- AC2 → T2
- AC3 → T1
- AC4 → T1, T2, T3

## Tasks

- [x] T1: Append D-007 to `cairn/DECISIONS.md`: context (a call with no first argument makes no element since 0.7.9, and D-005's Consequences left it to the candidate row), the user's choice of both changes, and that IP5 does not change because such a call stopped the render before 0.7.9, so no working output broke.
- [x] T2: Edit IP1 in `cairn/DESIGN.md` (line 91): "first argument is empty" becomes "first argument is missing or empty" in both places, the closing citation becomes "(D-005, D-007)", and add the sentence for AC2 with a D-007 citation.
- [x] T3: Run `python3 /Users/jmgirard/.claude/skills/cairn/scripts/cairn_validate.py` and `git diff --name-only origin/main...HEAD`, and confirm that the second lists only `cairn/` paths.

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
- 2026-10-26: implement started on branch `m013-ip1-missing-argument`, cut from `origin/main` at 0566f1c; untracked `.DS_Store` left unstaged.
- 2026-10-26: T1 done: D-007 appended to `cairn/DECISIONS.md` (with a shell heredoc, not the Edit tool); its 0.7.9 facts read from `CHANGELOG.md` and `no_first_argument` in `lordicon.lua`.
- 2026-10-26: T2 done: IP1 now says "missing or empty" in both places, cites D-005 and D-007, and ends with the Quarto-drop sentence; the skipped-key sentence was rewrapped, its words unchanged.
- 2026-10-26: T3 done: `cairn_validate` all checks passed; `git diff --name-only origin/main...HEAD` lists 4 paths, all under `cairn/`.
- 2026-10-26: verify: `python3 _tests/check_aria.py` printed "0 failures" (130 of 130 lordicon warnings); `quarto render` and the browser look skipped, because the diff changes no file the demo site renders.
- 2026-10-26: claim audit: not owed — internal tier.
- 2026-10-26: implement done; status set to review.

## Decisions

## Review

- 2026-10-26 AC1: `cairn/DESIGN.md` IP1 (lines 97-101, read at a9006d3) says "every key of a call whose first argument is missing or empty" and "A call whose first argument is missing or empty makes no element, so its keys reach none, and the render warns about the argument (D-005, D-007)". Pass.
- 2026-10-26 AC2: IP1 (lines 101-103) says "Quarto drops a value or positional argument that starts with a space or tab before the extension runs, so it never reaches the extension and is not one of these exceptions (D-007)". Pass.
- 2026-10-26 AC3: the last `### D-` heading in `cairn/DECISIONS.md` is D-007; its Decision names the M013 plan gate choice, the missing-argument change, and the Quarto-drop sentence, and says "IP5 does not change, because a call with no first argument stopped the render before 0.7.9". Pass.
- 2026-10-26 AC4: `git diff --name-only origin/main...HEAD` (origin/main 0566f1c, HEAD a9006d3) lists `cairn/DECISIONS.md`, `cairn/DESIGN.md`, `cairn/ROADMAP.md`, `cairn/milestones/M013-ip1-missing-argument.md`. Pass.
- 2026-10-26 gate: `cairn_validate` all checks passed; `cairn_impact IP1` live references are DESIGN.md:144 (GP5's "(IP1)", still true), the ROADMAP M013 row, and the candidate row this milestone graduates; `--changed` reports none because it reads the working tree. Version marker `_extension.yml` 0.7.11, unchanged; `check_aria.py` 0 failures on a tree whose only later change is under `cairn/`; changelog entry not needed, no user-visible change.
- spawned: diff-bug, ripple (internal tier, docs-only diff).
- diff-bug #1: IP1's "each such skipped key" sentence claimed a per-key warning for the keys of a missing- or empty-argument call, which `no_first_argument` never gives — fix now, fixed 7f91a3c (the sentence now covers the first two kinds only).
- diff-bug #2: the Conventions bullet names no call-level exception, so it contradicts IP1 — fix now, fixed 7f91a3c (one sentence citing D-005 and D-007).
- diff-bug #3: "positional argument" says more than README shows, which names only a first argument — reject, false: the 2026-10-24 (M005) lesson records Quarto dropping a quoted positional argument that starts with a space or tab.
- diff-bug #4: IP1 said only the value is dropped, but README says a quoted value goes with its key — fix now, fixed 7f91a3c.
- diff-bug #5: the drop sentence could read as contradicting the missing-argument exception — fix now, fixed 7f91a3c (a clause names the call a dropped first argument leaves).
- diff-bug #6: IP1 did not say that the warning comes only in HTML output — fix now, fixed 7f91a3c.
- diff-bug (unranked note): D-007's heading says "no first argument" where IP1 says "missing" — reject, style: both name the nil case, and D-007's Context says which.
- ripple #1: the ROADMAP candidate row "Decide whether IP1 names Quarto's drops" is stale — reject, planned change: this milestone absorbs it and post-merge hygiene graduates it.
- ripple #2: the Conventions bullet names no call-level exception — same as diff-bug #2, fixed 7f91a3c.
- ripple #3: IP5 does not mention a missing first argument — reject, planned change: D-007 keeps IP5 unchanged and says why; the diff-bug lens confirmed that every version before 0.7.9 stopped the render on such a call.
- ripple #4: README's list of keys the extension does not pass on has no entry for a missing or empty first argument — reject, false: the list names kinds of key, and README lines 110-116 cover both calls.
- 2026-10-26 AC1 (re-read after 7f91a3c): IP1 lines 98-101 say "every key of a call whose first argument is missing or empty" and "A call whose first argument is missing or empty makes no element, so its keys reach none, and in HTML output the render warns once about the argument (D-005, D-007)". Pass.
- 2026-10-26 AC2 (re-read after 7f91a3c): IP1 lines 101-106 say Quarto drops a quoted value or a positional argument that starts with a space or tab before the extension runs, and "Such a value or argument never reaches the extension and is not one of these exceptions". Pass.
- 2026-10-26 AC4 (re-run after 7f91a3c): `git diff --name-only origin/main...HEAD` lists the same 4 paths, all under `cairn/`; `cairn_validate` all checks passed. Pass.
