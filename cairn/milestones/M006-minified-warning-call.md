<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M006: Name the call in the Minified warning

- **Status:** review   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the warning text that users read in the render log   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** m006-minified-warning-call   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The Minified-export warning of `lif` names the shortcode call, such as `{{< lif minified.json >}}`, as the other render warnings do, where before it named only the file.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `check_minified` in `_extensions/lordicon/lordicon.lua` takes the call string that `lif` builds and names it in the warning. The warning still names the file (inside the call), the keys, and the two fixes. The `minified-lif` expectation in `_tests/check_aria.py` checks the call. Version 0.7.6 and a `CHANGELOG.md` entry (D-001, D-002).

**Out:** The once-per-file rule stays as it is, and a test of it (including `./minified.json` warning again) stays in the candidate row "Add a render check with fixtures". No demo page changes, because the demo site shows no warning, so `docs/` gets no new content (GP4 needs an example only for new surface).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [x] AC1: Rendering `_tests/aria.qmd` gives exactly one lordicon warning line for the `minified-lif` call, and that line holds `{{< lif minified.json >}}`, `looks like a Minified Lottie export`, and `Colors, STROKE, sTaTe`, as a `python3 _tests/check_aria.py` run shows by exiting 0.
- [x] AC2: `_extensions/lordicon/_extension.yml` has `version: 0.7.6`, and the first version section of `CHANGELOG.md` is `## 0.7.6`, with an entry saying that the Minified-export warning of `lif` now names the shortcode call.
- [x] AC3: At the head of the milestone branch, `quarto render` at the repo root exits 0, and the only change it makes under `docs/` is the `lastmod` values in `docs/sitemap.xml`.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [x] T1: In `_tests/check_aria.py` (`WARNED`, line 196), change the `minified-lif` expectation to `[CALL, "looks like a Minified Lottie export", "so Colors, STROKE, sTaTe will"]`. Run `python3 _tests/check_aria.py` against the current filter and make sure that it fails on the `minified-lif` case for the missing call text.
- [x] T2: In `lif` (`lordicon.lua:410`), build the call string once and pass it to both `check_minified` and `build_element`. In `check_minified` (`lordicon.lua:368`), name the call as the subject of the warning, for example `lordicon: {{< lif FILE >}} uses a file that looks like a Minified Lottie export, so … will have no effect.`, and keep the rest of the text. Update the comment above `warned_minified`. Run `python3 _tests/check_aria.py`, which must exit 0.
- [x] T3: Raise `version:` in `_extensions/lordicon/_extension.yml` to 0.7.6 and add a `## 0.7.6` section at the top of `CHANGELOG.md`. Run `quarto render` at the repo root, make sure that `git status -- docs` lists only `docs/sitemap.xml` with only `lastmod` lines changed, then run `git checkout -- docs/sitemap.xml`.

## Work log
<!-- owner: any skill · append-only; one line per entry; absolute dates. -->

- 2026-10-24: created by /milestone-plan.
- 2026-10-24: tier check: not run — work named at the question set.
- 2026-10-24: question set: which candidate to plan — "Name the call in the Minified warning" (absorbs that ROADMAP row).
- 2026-10-24: idea vet: no concern. For `lif` the call adds only the shortcode name to the file name the warning already gives, so the gain is one warning format across the filter; the once-per-file rule names the first call, and every call on that file builds the same call string.
- 2026-10-24: lessons used: 2026-10-20 (M002) on `quarto render` rewriting `docs/sitemap.xml`.
- 2026-10-24: collision check: absorbs the candidate row "Name the call in the Minified warning"; M004 (Minified keys in any letter case) is distinct; works under D-001 and D-002; no D-entry rejects it.
- 2026-10-24: inbox sweep: 0 open issues, 0 open PRs.
- 2026-10-24: criteria audit (full mode, fresh Opus reader): AC1 none, AC2 none; AC3 named the verify slot (an instrument) and did not show the sitemap revert was the render's only change. Fixed by narrowing AC3 to the render exit code and its `docs/` diff, and dropping the `check_aria.py` clause that AC1 covers.
- 2026-10-24: plan gate chose the call as the warning's subject with the once-per-file rule kept, over one warning per call, because the fix is to the file and per-call warnings repeat it; falsified by a user report that a later call on the same Minified file went unwarned and confused them.
- 2026-10-24: test scope: only the `minified-lif` expectation changes; the `raw-lif` call and the total warning count in `check_warnings` keep the silent case covered.
- 2026-10-24: started on branch m006-minified-warning-call; `.DS_Store` (untracked, unrelated) left unstaged.
- 2026-10-24: T1 done: `minified-lif` expectation uses CALL; on the old filter `check_aria.py` fails only with "log minified-lif: 0 warnings hold ['{{< lif minified.json >}}', …]".
- 2026-10-24: T2 done: `lif` builds the call once and passes it to `check_minified`; the render logs "lordicon: {{< lif minified.json >}} uses a file that looks like a Minified Lottie export, so Colors, STROKE, sTaTe will have no effect. …"; `check_aria.py` exits 0 (62 cases, 32 warnings).
- 2026-10-24: T3 done: version 0.7.6 and CHANGELOG 0.7.6; `quarto render` exits 0, no lordicon warning, and changes only one `lastmod` line in `docs/sitemap.xml`, reverted. The changelog leaves out "still warns once per file", since no test checks that rule.
- 2026-10-24: claim audit: 7 claims read, 0 corrected — `CHANGELOG.md`, `_extensions/lordicon/lordicon.lua`, `_tests/check_aria.py`.
- 2026-10-24: implement complete; status review.
- 2026-10-24: step-7 approval: m006-minified-warning-call approved for merge

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->

Pass 1, 2026-10-24, at 610e7eb.

- AC1: `python3 _tests/check_aria.py` exits 0: 62 cases, 32 of 32 lordicon warnings, 0 failures. Its `minified-lif` check needs exactly one log line holding `{{< lif minified.json >}}`, `looks like a Minified Lottie export`, and `so Colors, STROKE, sTaTe will`. A render of the fixture logs that line as "lordicon: {{< lif minified.json >}} uses a file that looks like a Minified Lottie export, so Colors, STROKE, sTaTe will have no effect. …".
- AC2: `_extension.yml` line 3 reads `version: 0.7.6`. The first version heading of `CHANGELOG.md` is `## 0.7.6` (line 5, before `## 0.7.5` at line 9), and its entry reads "The Minified-export warning of `lif` now names the shortcode call, such as `{{< lif icon.json >}}`, …".
- AC3: at 610e7eb, `quarto render` at the repo root exits 0. `git status -- docs` then lists only `docs/sitemap.xml`, and its diff is one `<lastmod>` line. The file was restored with `git checkout`.
- gate: `cairn_validate.py` exit 0, all checks passed. No principle text changed, so `cairn_impact` was skipped.
- gate (profile): `_extension.yml` is the one version marker that the release-walk names, and `cairn_versions.py` reads 0.7.6 with the tag absent. The verify render passes (AC1, AC3). `CHANGELOG.md` has the `## 0.7.6` entry.
- spawned: diff-bug, blame-history, prior-review, ripple
- diff-bug #1: the comment "names the first such call" suggests later calls differ, but every call on a file builds the same call string — fix now, fixed ac03d3d (`check_aria.py` exit 0 after).
- diff-bug #2: the test does not pin "uses a file that" — reject, planned change: T1 named the three fragments, which are what AC1 promises.
- diff-bug #3: line 402 is 81 characters — reject, style.
- diff-bug #4: the changelog omits once-per-file — reject, planned change: left out on purpose because no test checks that rule (work log, T3).
- blame-history #1: the warning names one call where the old text named the file for all calls — reject, false: the call string is `{{< lif FILE >}}` for every call on that file, so the text is the same.
- blame-history #2: a quoted name such as `"my file.json"` shows as `{{< lif my file.json >}}`, as in every other warning since M003 — follow-up, new row "Quote file names that hold spaces".
- prior-review #1: the 0.7.6 entry lacks the once-per-file qualifier that the M002 review asked of the 0.7.1 entry — reject, false: the 0.7.6 entry makes no claim about when the warning fires, and the 0.7.1 entry still states once per file.
- prior-review #2: a second call on the same Minified file gets no warning — reject, planned change: Scope Out keeps the once-per-file rule.
- prior-review #3: naming the first call is untested — reject, false: no call-specific text exists to test, since every call on a file gives the same call string.
- prior-review #4: the Minified warning lists keys without quotes, unlike the M003 warnings — reject, style (M004 rejected it the same way).
- prior-review #5: `./minified.json` still warns again — follow-up, already in the row "Add a render check with fixtures".
- ripple #1: the ROADMAP row "Name the call in the Minified warning" still says the warning names the file — reject, planned change: merge hygiene removes the row.
