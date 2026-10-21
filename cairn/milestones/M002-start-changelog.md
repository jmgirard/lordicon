# M002: Start CHANGELOG.md for past releases

- **Status:** review
- **Priority:** normal
- **Depends on:** —
- **Driving RR:** —
- **Principles touched:** —
- **Resolves:** —
- **Surface tier:** user-facing — users read the changelog to see what each version changed
- **Branch/PR:** m002-start-changelog

## Goal

The repo has a CHANGELOG.md that lists each tagged version with its user-visible changes (D-002).

## Scope

**In:** `CHANGELOG.md` at the repo root, written from the 19 `v*` tags and the commits in each tag's range. A README link to it. The PROFILE `changelog` slot and the DESIGN Conventions bullet stop saying that the file does not exist.

**Out:** The `## 0.7.3` section for the key-clash fixes → M003. No version raise, because the file is outside `_extensions/` and `quarto add` installs nothing new (D-001).

## Acceptance criteria

- [x] AC1: At M002's review head, `CHANGELOG.md` at the repo root has one `## <version>` section for each tag that `git tag -l 'v*'` lists, newest first, and no other `## ` section. The version is the tag name without its `v`.
- [ ] AC2: Each section lists the user-visible changes in its range, `git log <previous v* tag>..<tag>`, or says "No user-visible changes." The first tag's range is all history up to it. Each entry names a change that a commit in its range makes.
- [x] AC3: README links to `CHANGELOG.md`.

## Coverage

- AC1 → T2, T3
- AC2 → T1, T2
- AC3 → T2

## Tasks

- [x] T1: For each tag, newest first, read its range with `git log --format='%h %s' <previous>..<tag>` and `git diff --stat <previous>..<tag>`. Draft the user-visible changes from the subjects and diffs, or "No user-visible changes."
- [x] T2: Write `CHANGELOG.md` with plain `## <version>` headings and no Unreleased heading. Add the README link. Update the PROFILE `## changelog` slot and the DESIGN Conventions bullet.
- [x] T3: Compare the file's `## ` headings with the `git tag -l 'v*'` list by a one-line script, and record the result in the work log.

## Work log

- 2026-10-20: created by /milestone-plan.
- 2026-10-20: tier check: not run — work named at the question set.
- 2026-10-20: question set: what to work on — the key-clash fixes (M003), with CHANGELOG.md in its own milestone first (this file).
- 2026-10-20: criteria audit (full, fresh Opus reader): 2 findings, both fixed. AC1 clashed with M003's 0.7.3 section, so it now holds at M002's review head. AC2 checked only that entries were true and bound the review's recording act, so it now asks each section to list its changes or say none, and the recording sentence is gone.
- 2026-10-20: plan gate chose a separate changelog milestone over folding it into M003 because the user chose it and it keeps M003's review on code; falsified by M002's review needing M003's code to judge an entry.
- 2026-10-20: decided: plain `## <version>` headings and no Unreleased heading, because the version rises at each shipping merge (D-001) and the release-walk reads `## <version>`.
- 2026-10-20: implement started on branch m002-start-changelog, cut from main at c61003d. `.DS_Store` stays untracked and unstaged.
- 2026-10-20: T1 done: read all 19 tag ranges (`git log`, filter and package.json diffs, full messages of the big commits). The 0.3.1 and 0.5.1 tags carry an `_extension.yml` that still names the previous version.
- 2026-10-20: decided: entries cover the extension's behavior, the bundled player version, and README or demo changes users act on. Build-tool-only and internal refactor changes get no entry.
- 2026-10-20: T2 done: CHANGELOG.md with 19 sections, README link under Installing, PROFILE `changelog` slot and DESIGN Conventions bullet updated. The 0.7.0 entry says the bundle is smaller from `git cat-file -s` on bundle.js at v0.6.0 and v0.7.0. The README's older text keeps its plain-English linter hits, which this task does not touch.
- 2026-10-20: T3 done: `diff` of the `## ` headings against `git tag -l 'v*' | sort -rV` matched 19 sections. A planted missing 0.5.2 heading made it exit 1. Verify: `check_aria.py` 0 failures, `quarto render` ok; the render's `docs/sitemap.xml` date change was dropped.
- 2026-10-20: claim audit: 57 claims read, 5 corrected — CHANGELOG.md (0.1.0 Babel claim dropped and the RStudio note moved there from 0.2.0, 0.3.1 player versions split with 0.3.0, 0.5.0 screenshot is static, 0.3.0 cause tied to the #2 issue title). Five omissions added after a check against the tags: 0.3.0 player versions, 0.5.0 default size removed, 0.5.2 version-number fix, 0.6.0 Quarto 1.3.0 minimum, 0.5.4 README export steps.

## Decisions

## Review

- 2026-10-20 sync: branch cut from origin/main c61003d, which has not moved; no PR exists yet (route d); the Copilot round is off.
- AC1: `diff` of `grep '^## ' CHANGELOG.md` against `git tag -l 'v*' | sort -rV` with the `v` removed is empty: 19 sections, 19 tags, same order, no other `## ` section. T3's planted missing heading made the same diff exit 1.
- AC3: `README.md:28` holds `[CHANGELOG.md](CHANGELOG.md) lists the changes in each version.`
- gate: `cairn_validate.py` all checks passed. No principle changed, so `cairn_impact` was skipped. Toolchain: the one version marker (`_extension.yml`) reads 0.7.2, unchanged. `python3 _tests/check_aria.py` 0 failures, and `quarto render` succeeded (its `docs/sitemap.xml` date change was dropped). The changelog check needs no entry, because M002 changes nothing that `quarto add` installs.
