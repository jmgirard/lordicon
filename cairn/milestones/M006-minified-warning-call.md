<!-- Section ownership + write-modes: see tracking-rules.md "Milestone-file
     section ownership". A phase skill never rewrites another phase's section.
     Per-section owners are tagged below. The one size check that can fail is
     cairn_validate's <150 over the plan-owned body. -->
# M006: Name the call in the Minified warning

- **Status:** planned   <!-- owner: transitioning skill · mirror-update; cairn/ROADMAP.md is the authority -->
- **Priority:** normal   <!-- owner: plan · create/amend-via-gate; high | normal | low -->
- **Depends on:** —   <!-- owner: plan · create/amend-via-gate; M<xx>, M<yy> or — -->
- **Driving RR:** —   <!-- owner: plan · create/amend-via-gate; RR<NN> whose Binding criteria bind this milestone's ACs (binding-criteria check), or — -->
- **Principles touched:** GP2   <!-- owner: plan · create/amend-via-gate; comma-separated IPn/GPn ids this milestone touches, or — -->
- **Resolves:** —   <!-- owner: plan · create/amend-via-gate; comma-separated GitHub issues the scope absorbs, each `#N closes` (the PR closes it at merge) or `#N partial` (the remainder gets a candidate row), or — ; skill conduct only — no validate check parses it -->
- **Surface tier:** user-facing — the warning text that users read in the render log   <!-- owner: plan · create/amend-via-gate; user-facing | internal — <one-clause reason>; skill conduct only — no validate check parses it -->
- **Branch/PR:** —   <!-- owner: implement (branch) / review (PR URL) · create; a companion checkout the milestone also works in is one further entry per checkout, `companion: <abs-path> <branch>` (implement), its PR URL appended by review — /milestone-review merges companions first, in listed order -->

## Goal
<!-- owner: plan · create; a wrong goal returns to plan, never edited in place -->

The Minified-export warning of `lif` names the shortcode call, such as `{{< lif minified.json >}}`, as the other render warnings do, where before it named only the file.

## Scope
<!-- owner: plan · create/amend-via-gate -->

**In:** `check_minified` in `_extensions/lordicon/lordicon.lua` takes the call string that `lif` builds and names it in the warning. The warning still names the file (inside the call), the keys, and the two fixes. The `minified-lif` expectation in `_tests/check_aria.py` checks the call. Version 0.7.6 and a `CHANGELOG.md` entry (D-001, D-002).

**Out:** The once-per-file rule stays as it is, and a test of it (including `./minified.json` warning again) stays in the candidate row "Add a render check with fixtures". No demo page changes, because the demo site shows no warning, so `docs/` gets no new content (GP4 needs an example only for new surface).

## Acceptance criteria
<!-- owner: plan · create/amend-via-gate; review reads, never reinterprets. -->

- [ ] AC1: Rendering `_tests/aria.qmd` gives exactly one lordicon warning line for the `minified-lif` call, and that line holds `{{< lif minified.json >}}`, `looks like a Minified Lottie export`, and `Colors, STROKE, sTaTe`, as a `python3 _tests/check_aria.py` run shows by exiting 0.
- [ ] AC2: `_extensions/lordicon/_extension.yml` has `version: 0.7.6`, and the first version section of `CHANGELOG.md` is `## 0.7.6`, with an entry saying that the Minified-export warning of `lif` now names the shortcode call.
- [ ] AC3: At the head of the milestone branch, `quarto render` at the repo root exits 0, and the only change it makes under `docs/` is the `lastmod` values in `docs/sitemap.xml`.

## Coverage
<!-- owner: plan · create/amend-via-gate -->

- AC1 → T1, T2
- AC2 → T3
- AC3 → T3

## Tasks
<!-- owner: plan (create) / implement (check-off, minor edits); substantive change is amend-via-gate. -->

- [ ] T1: In `_tests/check_aria.py` (`WARNED`, line 196), change the `minified-lif` expectation to `[CALL, "looks like a Minified Lottie export", "so Colors, STROKE, sTaTe will"]`. Run `python3 _tests/check_aria.py` against the current filter and make sure that it fails on the `minified-lif` case for the missing call text.
- [ ] T2: In `lif` (`lordicon.lua:410`), build the call string once and pass it to both `check_minified` and `build_element`. In `check_minified` (`lordicon.lua:368`), name the call as the subject of the warning, for example `lordicon: {{< lif FILE >}} uses a file that looks like a Minified Lottie export, so … will have no effect.`, and keep the rest of the text. Update the comment above `warned_minified`. Run `python3 _tests/check_aria.py`, which must exit 0.
- [ ] T3: Raise `version:` in `_extensions/lordicon/_extension.yml` to 0.7.6 and add a `## 0.7.6` section at the top of `CHANGELOG.md`. Run `quarto render` at the repo root, make sure that `git status -- docs` lists only `docs/sitemap.xml` with only `lastmod` lines changed, then run `git checkout -- docs/sitemap.xml`.

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

## Decisions
<!-- owner: implement / review · append-only; milestone-local. -->

## Review
<!-- owner: review · exclusive. -->
