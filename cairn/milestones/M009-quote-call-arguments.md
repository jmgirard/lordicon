# M009: Quote spaced arguments in warning calls

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** GP2
- **Resolves:** —
- **Surface tier:** user-facing — it changes the render warnings that users read
- **Branch/PR:** m009-quote-call-arguments

## Goal

A render warning writes the call's argument in quotes when the argument holds a space, `"`, or `=`, so that Quarto reads the call that the warning shows back as the same argument.

## Scope

**In:** A helper in `_extensions/lordicon/lordicon.lua` that writes the first
argument of a call for a warning. It writes the argument bare by default. It
quotes an argument that Quarto cannot read bare: an empty one, one that starts
with `"`, `'`, `}`, or `>`, and one that holds a space, tab, newline, `"`, or
`=`. The bare-token rule is `sc_string` in Quarto's `lpegshortcode.lua`, and
probes on Quarto 1.10.19 add `"` and `=`. Quarto has no `\"` escape, so an
argument that holds `"` goes in single quotes, and any other argument goes in
double quotes. Inside quotes, `\` is written as `\\`, which Quarto reads back
as `\`. `li` (`lordicon.lua:394`) and `lif` (`lordicon.lua:465`) build their
`call` string with it. Fixture cases, version 0.7.8, and a changelog entry.

**Out:** an argument that holds both `"` and `'`, which no call can pass to
the filter, so the helper gives it no form of its own. A call with no first
argument, which now fails the render → M010. The docs note on values that
start with a space → M010.

## Acceptance criteria

- [ ] AC1: A render of `_tests/aria.qmd` gives one Minified warning for a `lif` call on `mini fied.json` with `colors`. That file is a copy of `_tests/minified.json`. The warning names the call as `{{< lif "mini fied.json" >}}`.
- [ ] AC2: The same render gives one skip warning for a `li` call with a `src` key and the code `a "b" c\d`. The fixture writes that code as `'a "b" c\d'`. The warning names the call as `{{< li 'a "b" c\\d' >}}`.
- [ ] AC3: The same render gives one skip warning for a `li` call with a `src` key and the code `x=y`. The fixture writes that code as `"x=y"`. The warning names the call as `{{< li "x=y" >}}`.
- [ ] AC4: The verify slot of `cairn/PROFILE.md` is clean. `python3 _tests/check_aria.py` exits 0, and `quarto render` at the repo root succeeds.
- [ ] AC5: `version:` in `_extensions/lordicon/_extension.yml` reads `0.7.8`. `CHANGELOG.md` has a `## 0.7.8` section. It says that warnings now quote an argument that holds a space, `"`, or `=`.

## Coverage

- AC1 → T1, T2
- AC2 → T1, T2
- AC3 → T1, T2
- AC4 → T1, T2, T3
- AC5 → T3

## Tasks

- [x] T1: Write the three fixture cases first and see them fail. In
      `_tests/aria.qmd`, add a `lif` call on `"mini fied.json"` with `colors`
      and the `li` calls `'a "b" c\d'` and `"x=y"`, each with a `src` key and
      its own `id`. In `check_aria.py`, copy `minified.json` to
      `mini fied.json` in `render()`. Let `QUOTED` and `unquote` read these
      arguments as Quarto does. Give each case a `CASES` entry and a `WARNED`
      entry whose call text is the literal string of AC1–AC3, stated apart
      from the fixture's argument. `check_warnings` uses that literal for
      these cases. Run the check and confirm that it fails on these three
      warnings only.
- [x] T2: Add the helper to `lordicon.lua` and use it in `li` and `lif`.
      Spell out the byte set (space, tab, newline) rather than `%s`, which
      follows the locale. Update the header comment if it names the call
      format. Run the check until it exits 0.
- [ ] T3: Raise `version:` to `0.7.8` and add the `## 0.7.8` CHANGELOG
      section. Run `quarto render` at the repo root, then
      `git checkout -- docs/sitemap.xml`, since no demo page changes.

## Work log

- 2026-10-25: created by /milestone-plan.
- 2026-10-25: tier check: milestone — both candidates change warning text or docs, and the request was split into two milestones.
- 2026-10-25: idea vet: no concern for quoting file names; the leading-space concern (the extension cannot keep or see such a value) was answered at the question set with a docs note, which M010 holds.
- 2026-10-25: lessons used: 2026-10-24 (M003) on `%s` following the locale; 2026-10-20 (M002) on the render rewriting `docs/sitemap.xml`.
- 2026-10-25: absorbed candidate "Quote file names that hold spaces" (M006 review); the archive shows M006 built the `call` string this milestone quotes.
- 2026-10-25: inbox sweep: 0 open issues and 0 open PRs.
- 2026-10-25: split: M009 covers the quoting; the leading-space docs note and the no-argument crash fix become M010 (planned now, depends on M009 for the version order and the shared CHANGELOG).
- 2026-10-25: plan chose to quote by Quarto's own read-back rule over quoting only on a space, because probes showed `x=y.json` and `a"b` also misread bare; falsified by a render that reads a call shown in a warning as a different argument.
- 2026-10-25: plan chose to quote `li` codes too over `lif` files only, because both build the call the same way; falsified by a `li` warning that misnames a call the user wrote.
- 2026-10-25: criteria audit (full mode, Opus reader): 4 findings, all fixed. Quarto has no `\"` escape, so AC2 uses single quotes; the quote rule adds `"` and `=`; the Goal no longer says "quoted argument", which reads two ways; AC3 adds an `=` case so one exemplar does not stand for the rule. AC4 and AC5 had none.
- 2026-10-25: changelog: one entry under 0.7.8 (D-001, D-002).
- 2026-10-25: priority normal, not the source row's low, because M010 depends on this milestone.
- 2026-10-25: implement: branch m009-quote-call-arguments cut from main at c876208; untracked `.DS_Store` left unstaged.
- 2026-10-25: T1 done: 3 fixture calls and literal `WARNED` calls; `QUOTED` and `unquote` needed no change, since no fixture argument uses an escape. The check fails on the 3 call texts only (85 cases, 45 warnings read).
- 2026-10-25: T2 done: `call_arg` in `lordicon.lua`, used by `li` and `lif`; named for what it writes, since the header comment names no call format. `check_aria.py` exits 0 (85 cases, 45 warnings).

## Decisions

## Review
