# M009: Quote spaced arguments in warning calls

**Status:** done (2026-10-25, PR #13 https://github.com/jmgirard/lordicon/pull/13)

**Goal:** A render warning writes the call's argument in quotes when the argument holds a space, `"`, or `=`, so that Quarto reads the call that the warning shows back as the same argument.

**Outcome:** `call_arg` in `lordicon.lua` writes a call's first argument for
`li` and `lif` warnings. It writes the argument bare only when it holds
nothing but ASCII letters, digits, and `-._/:~+@`, and otherwise in double
quotes, or in single quotes when it holds `"`; `\` is doubled inside quotes.
The plan copied Quarto's Lua bare-token rule, but review found that Quarto's
check of a call on its own line also rejects a bare `'` or whitespace, so the
rule became that allowlist. `check_aria.py` adds 5 fixture calls (space, `"`,
`=`, `\`, `'`) with literal expected calls; `unquote` reads `\\` as `\`; 87
cases, 47 warnings. Version 0.7.8, CHANGELOG 0.7.8, DESIGN Known issues.

**Decisions:** none. The plan quoted `li` codes as well as `lif` files.

**Review:** one pass, four-lens fan-out, after a claim audit that added `\`
and `>}}`. 16 findings: 8 fixed (a bare `'` call failing on its own line, two
comments, the CHANGELOG list, DESIGN coverage), 8 rejected (1 edge: an HTML
entity in an argument; 4 planned; 3 false), 0 follow-ups. Hygiene graduated
"Quote file names that hold spaces"; captured 1 lesson; marked 3 lessons used.
