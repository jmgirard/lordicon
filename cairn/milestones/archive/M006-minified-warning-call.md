# M006: Name the call in the Minified warning

**Status:** done (2026-10-24, PR #10 https://github.com/jmgirard/lordicon/pull/10)

**Goal:** The Minified-export warning of `lif` names the shortcode call, such as `{{< lif minified.json >}}`, as the other render warnings do, where before it named only the file.

**Outcome:** `lif` in `lordicon.lua` builds the call string once and
passes it to `check_minified` and `build_element`. The warning now reads
"lordicon: {{< lif FILE >}} uses a file that looks like a Minified Lottie
export, so … will have no effect." The once-per-file rule (`warned_minified`
keyed by the path as written) is unchanged. The `minified-lif` expectation in
`check_aria.py` uses the `CALL` marker (62 cases, 32 warnings). Version
0.7.6 and CHANGELOG 0.7.6; no demo page change.

**Decisions:** none. The plan kept one warning per file over one per call,
because the fix is to the file.

**Review:** one pass, four-lens fan-out. 12 findings: 1 fixed (a comment
implied that calls on one file differ), 2 follow-ups (new row "Quote file
names that hold spaces"; `./minified.json` is already in "Add a render check
with fixtures"), 9 rejected (3 false, 4 planned, 2 style). Hygiene graduated
"Name the call in the Minified warning"; no lesson captured.
