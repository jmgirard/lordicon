<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M007: Check sorting, non-HTML output, and Minified spellings

- **Status:** in-progress   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** IP3   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** internal — tests and a code comment, with no change to what the extension does   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m007-render-check-fixtures   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

`_tests/check_aria.py` checks three behaviors that were checked by eye: the order of an icon's attributes, the empty output of a non-HTML render, and the Minified warning's once-per-path rule.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** A `sorted` case in `_tests/aria.qmd` and an order check in `_tests/check_aria.py` over the raw filter output and the page. A `gfm` render of `_tests/aria.qmd` inside `check_aria.py` that must give no icon and no lordicon warning. Two more `lif` calls on the Minified fixture, one with the same path and one as `./minified.json`, with their expected warnings. The comment above `warned_minified` states that the rule keys a file by its path as written. DESIGN.md's Known issues and Architecture lines for `_tests/` follow the new coverage.

**Out:** No change to the filter's behavior, so no version bump and no `CHANGELOG.md` entry (D-001, D-002). Warning once for every spelling of one file stays unbuilt (the user chose to test the rule as it is). Sorting the keys by byte under every locale stays in the candidate row "Sort keys by byte, not by locale". Other non-HTML formats run the same code path as `gfm` and get no render of their own. No demo page changes (GP4 needs an example only for new surface).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: `_tests/check_aria.py` compares the attribute names of the `sorted` case of `_tests/aria.qmd`, a `li` call whose keys are written out of order (`trigger=hover id=sorted Zeta=1 @click=2 class=big data-a=3`), in the order Python's HTML parser reads them from both the raw filter output and the rendered page, against the literal list `src`, `@click`, `zeta`, `class`, `data-a`, `id`, `trigger`, `aria-hidden`.
- [ ] AC2: `_tests/check_aria.py` also renders `_tests/aria.qmd` to `gfm`, and fails unless that render exits 0, its output file holds neither `lord-icon` nor `{{<`, and its log holds no line with `lordicon:`.
- [ ] AC3: `_tests/aria.qmd` gains a second `lif minified.json` call and a `lif ./minified.json` call, each with a `colors` key. `_tests/check_aria.py` expects no warning for the second `minified.json` call and one warning naming `{{< lif ./minified.json >}}` for the `./minified.json` call, inside its existing check that the log holds no other lordicon warning. The comment above `warned_minified` in `_extensions/lordicon/lordicon.lua` says that the rule keys a file by its path as written.
- [ ] AC4: At the head of the milestone branch, `python3 _tests/check_aria.py` exits 0, and `git diff origin/main...HEAD -- _extensions/` changes only Lua comment lines (lines whose text after leading spaces starts with `--`, or lines inside a `--[[ ]]` block). After `quarto render` at the repo root exits 0, `git status --porcelain docs/` lists only `docs/sitemap.xml`, and `git diff docs/sitemap.xml` changes only lines holding `<lastmod>`.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1
- AC2 → T2
- AC3 → T3
- AC4 → T3, T4

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [x] T1: Add `{{< li wlpxtupd trigger=hover id=sorted Zeta=1 @click=2 class=big data-a=3 >}}` to `_tests/aria.qmd` with a `CASES` entry, and an `ORDER` table in `_tests/check_aria.py` that `check()` compares, in order, against the names `IconParser` reads, for both the raw output and the page. Remove `table.sort(keys)` at `lordicon.lua:290` for one run and make sure that the check fails on `sorted`, then restore it.
- [ ] T2: Add a `gfm` render of `aria.qmd` to `check_aria.py`, in its own temporary directory with the same copied files and `LC_ALL=C.UTF-8` as `render_page()`. Fail on a nonzero exit, on `lord-icon` or `{{<` in the output, and on any `lordicon:` line in its log. For one run, make `build_element` (`lordicon.lua:267`) skip its format test and make sure that the check fails, then restore it.
- [ ] T3: Add `minified-again` (`lif minified.json`, `colors=primary:red`) and `minified-dotslash` (`lif ./minified.json`, `colors=primary:red`) to `aria.qmd`, with `CASES` entries and a `WARNED` entry for `minified-dotslash` only. Reword the comment at `lordicon.lua:364` to say that the rule keys a file by its path as written. For one run each, remove the `warned_minified[file]` return and strip a leading `./` from the key, and make sure that each run fails on its case, then restore the code.
- [ ] T4: Update the `check_aria.py` docstring, and DESIGN.md's Known issues and Architecture lines for `_tests/`, to name the new checks. Run `python3 _tests/check_aria.py` (exit 0), then `quarto render` at the repo root, check `git status --porcelain docs/` and `git diff docs/sitemap.xml`, and run `git checkout -- docs/sitemap.xml`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-25: created by /milestone-plan.
- 2026-10-25: tier check: not run — work named at the question set.
- 2026-10-25: question set: which candidate to plan — "Add a render check with fixtures" (absorbs that ROADMAP row in full).
- 2026-10-25: question set: the once-per-file Minified rule, which keys the path as written — test it as it is and state the rule in the code comment; no fix.
- 2026-10-25: idea vet: one concern, posed at the set: the row's `./minified.json` case is a behavior wart, not only a test gap; the user chose to pin it, not fix it. No other concern: sorting and the non-HTML branch are documented behavior (DESIGN Conventions, Purpose) with no test.
- 2026-10-25: lessons used: 2026-10-20 (M001) on reading the raw filter output beside the page; 2026-10-20 (M002) on `quarto render` rewriting `docs/sitemap.xml`; 2026-10-24 (M003) on setting `LC_ALL` for each subprocess; 2026-10-24 (M005) on the collation locale staying `C` under Quarto.
- 2026-10-25: collision check: absorbs the candidate row "Add a render check with fixtures"; M001 to M006 extended the same check and do not overlap; works under D-001 and D-002; no D-entry rejects it. Checker-regress shape: not hit, because `check_aria.py` tests the extension's output, not repo-internal records.
- 2026-10-25: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-25: criteria audit (reduced mode, fresh Opus reader): AC1 to AC3 none; AC4's `docs/` clause named no command listing the tree's changes, so new untracked files could pass. Fixed by naming `git status --porcelain docs/` and `git diff docs/sitemap.xml`.
- 2026-10-25: plan gate chose one `gfm` render over renders to several non-HTML formats, because all of them take the same `isFormat("html:js")` branch; falsified by a non-HTML format that gives output or a warning while `gfm` gives none.
- 2026-10-25: plan gate chose the uppercase `Zeta` key in the sort case over all-lowercase keys, because only a mixed-case key tells byte order from a case-folding sort; falsified by a sort change that keeps `Zeta` before `class` but breaks the order elsewhere.
- 2026-10-25: test scope: the new checks pass on the default branch; each is a documented claim with no test (DESIGN Known issues), and each task plants its defect once to see the check fail.
- 2026-10-25: implement started on branch m007-render-check-fixtures; `.DS_Store` at the repo root is untracked and left unstaged.
- 2026-10-25: T1 done: `sorted` case and `ORDER` table; check passes (63 cases); with `table.sort(keys)` removed the `sorted` case failed in both the page and the raw output, then the filter was restored.
