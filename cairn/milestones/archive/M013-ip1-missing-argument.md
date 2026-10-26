# M013: Name a missing first argument and Quarto's drops in IP1

**Status:** done (2026-10-26, PR #17 https://github.com/jmgirard/lordicon/pull/17)

**Goal:** IP1 names a call with no first argument as a call whose keys reach no element, and says that Quarto's own drops are outside the extension.

**Outcome:** Tracking-only, no version change. IP1 in `cairn/DESIGN.md` now lists every key of a call whose first argument is missing or empty as an exception: such a call makes no element and, in HTML output, warns once about the argument. Its per-key warning sentence now covers only the reserved and invalid-name kinds. A new sentence says that Quarto drops a quoted value that starts with a space or tab, with its key, and such a positional argument, before the extension runs, so neither is an IP1 exception, though a call left with no first argument is the missing case. The Conventions bullet gained the same call-level exception. IP5 is unchanged.

**Decisions:** D-007 (a call with no first argument gives no element, and Quarto's drops are not exceptions; narrows IP1, extends D-005). The user chose to name both cases at the plan gate.

**Review:** docs-only pair (diff-bug, ripple) after a reduced criteria audit (12 checks, 0 findings); 11 findings: 6 fixed on the branch (IP1's per-key warning claim, the Conventions gap found by both lenses, the dropped key, the HTML-only warning, the dropped-first-argument clause), 5 rejected (2 false, 2 planned, 1 style), 0 follow-ups. Graduated candidate row "Decide whether IP1 names Quarto's drops". No lesson captured; none marked used.
