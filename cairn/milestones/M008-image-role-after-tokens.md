# M008: Catch image roles after other tokens

- **Status:** in-progress
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** IP1, IP3, GP2, GP4
- **Resolves:** —
- **Surface tier:** user-facing — it changes which shortcode calls give a render warning, and the README and demo text that describe it
- **Branch/PR:** m008-image-roles

## Goal

The nameless-role warning reads the first role word that the ARIA specs define, as a browser does, and warns when that role is `img`, `image`, or `graphics-symbol`.

## Scope

**In:** In `warn_nameless_role` (`_extensions/lordicon/lordicon.lua:213`),
split the kept `role` value on ASCII whitespace, skip each token that is not
in a known-role list (compared with ASCII case folding), and warn when the
first known token is `img`, `image`, or `graphics-symbol`, under the name and
hiding conditions that 0.7.5 set. The known-role list holds the non-abstract
roles of WAI-ARIA 1.2 (deprecated ones included), the roles of DPUB-ARIA 1.1,
the roles of Graphics-ARIA 1.0, and `image` from the WAI-ARIA 1.3 draft. One
source note per spec under `cairn/references/`. New fixtures in
`_tests/aria.qmd` and `_tests/check_aria.py`. README, `index.qmd`,
CHANGELOG 0.7.7, version 0.7.7, the DESIGN.md convention line, the Lua
comment, and a re-render of `docs/`.

**Out:**
- Other WAI-ARIA 1.3 draft roles, such as `mark`, `comment`, and
  `suggestion`: left out at the plan gate, so `role="mark img"` warns. The
  `[parked]` candidate row "Know the WAI-ARIA 1.3 draft roles" holds it.
- Other image-like roles that need no name, such as `doc-cover`: no warning,
  because the spec does not require a name.
- Role values with a tab, a newline, or a leading space: a render cannot
  carry them (Pandoc expands tabs, and Quarto drops a value that starts with
  a space), so no fixture tests them.
- Any change to an emitted attribute (IP1): the warning is the whole change.

## Acceptance criteria

- [ ] AC1: In a render of `_tests/aria.qmd`, `python3 _tests/check_aria.py`
      exits 0 with every case it had before this milestone unchanged, and
      with these new calls, each without `label` and without any name or
      hiding attribute unless one is named here. Each of these gives one
      nameless-role warning that quotes the role value as written:
      `role="bogus img"`, `role="landmark img"`, `role="BOGUS Img"`,
      `role="bogus  img"` (two spaces), `role="bogus image"`,
      `role="graphics-symbol"`, `role="graphics-symbol img"`,
      `role="bogus graphics-symbol"`, and `role="Graphics-Symbol img"`.
      Each of these gives none: `role="bogus presentation img"`,
      `role="button img"`, `role="doc-cover img"`,
      `role="graphics-document img"`, `role="bogus"`, `role` set to `bogus`,
      U+00A0, and `img`, `role="bogus graphics-symbol" aria-label="Bell"`,
      and `role="graphics-symbol" aria-hidden=true`.
- [ ] AC2: The filter's known-role list holds exactly the role names that
      four source notes under `cairn/references/` record: the non-abstract
      roles of WAI-ARIA 1.2, the roles of DPUB-ARIA 1.1, the roles of
      Graphics-ARIA 1.0, and `image` from the WAI-ARIA 1.3 draft. Each note
      names the spec's URL, the section it copied, the date it was read, and
      its role count.
- [ ] AC3: The README, the demo home page (`index.qmd`), and a CHANGELOG
      0.7.7 entry say that the render reads the first role that the ARIA
      specs define and warns for `img`, `image`, and `graphics-symbol`. The
      DESIGN.md convention line on the warning and the comment above the
      token scan in `lordicon.lua` say the same. `_extension.yml` reads
      `version: 0.7.7`, and `docs/` is re-rendered from the changed
      `index.qmd`.

## Coverage

- AC1 → T2, T3
- AC2 → T1, T3
- AC3 → T4

## Tasks

- [x] T1: Write the four source notes from `templates/source-note.md`
      (`wai-aria-1-2.md`, `dpub-aria-1-1.md`, `graphics-aria-1-0.md`,
      `wai-aria-1-3.md`, the last recording only `image`), each with its
      URL, section, read date, and role list with count, and add their
      `INDEX.md` lines.
- [ ] T2: Add the AC1 calls to `_tests/aria.qmd` and their expectations to
      `_tests/check_aria.py` (`CASES` and `WARNED`). Run the check and see
      the new warning cases fail before the filter changes.
- [ ] T3: In `lordicon.lua`, add the known-role table built from the T1
      notes and replace the first-token match (line 236) with a scan that
      splits on ASCII whitespace and takes the first known token. Run the
      check green. Compare the table with the notes' lists by a one-off
      script and record the result in the work log.
- [ ] T4: Update the README (line 125), `index.qmd` (line 61), the
      DESIGN.md convention line (line 57), the Lua comment, a CHANGELOG
      0.7.7 entry, and `_extension.yml` to 0.7.7. Run `quarto render`, keep
      the re-rendered `docs/`, and look at the home page in a browser.

## Work log

- 2026-10-25: created by /milestone-plan.
- 2026-10-25: tier check: milestone — it changes which calls give a render warning and needs a choice of role lists.
- 2026-10-25: idea vet: the row's first-known-token approach misses the Graphics-ARIA fallback `role="graphics-symbol img"`, whose role needs a name — the set chose to warn for `img`, `image`, and `graphics-symbol`; the list's source (published specs or the 1.3 draft) — the set chose published specs plus `image`.
- 2026-10-25: lessons used: 2026-10-24 (M003) on `%s` and the locale; 2026-10-24 (M005) on Quarto dropping values that start with a space; 2026-10-20 (M002) on `docs/sitemap.xml` after a render.
- 2026-10-25: collision check: absorbs candidate row "Catch image roles after other tokens"; extends M005 (done), consistent with D-004; no D-entry rejects it. Inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-25: plan gate chose warning for `img`, `image`, and `graphics-symbol` over `img` and `image` only, because Graphics-ARIA 1.0 requires a name for `graphics-symbol` and recommends `role="graphics-symbol img"`; falsified by a screen reader that does not announce `graphics-symbol` as an image.
- 2026-10-25: plan gate chose the published role lists plus `image` over adding the WAI-ARIA 1.3 draft roles, because the draft can change; falsified by a user report of a false warning for a 1.3 role placed first.
- 2026-10-25: criteria audit (full mode, fresh Opus reader): 6 findings, all fixed — docs claim narrowed from browsers to the ARIA specs; notes name URL, section, date, and count; deprecated roles kept and the 1.3 note records only `image`; six AC1 cases added (`bogus image`, U+00A0, a name and a hiding attribute with `graphics-symbol`, `Graphics-Symbol`, `button img`) and untestable separators moved to Out; DESIGN line and Lua comment added to AC3; the warning quotes the value as written. A committed comparison script was not added: the list is a fixed table checked once at T3 and at review.
- 2026-10-25: version and changelog: patch bump to 0.7.7 per D-001, as 0.7.5 did for the first version of this warning.
- 2026-10-25: implement started on branch m008-image-roles; the untracked `.DS_Store` stays unstaged.
- 2026-10-25: T1 done: four source notes and INDEX lines. A parse of the fetched specs gives 82 non-abstract WAI-ARIA 1.2 roles (12 abstract left out), 41 DPUB-ARIA 1.1 roles, 3 Graphics-ARIA 1.0 roles, and `image` from the 1.3 draft: 127 names.
