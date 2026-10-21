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
- AC2 → T1, T2, T4
- AC3 → T2

## Tasks

- [x] T1: For each tag, newest first, read its range with `git log --format='%h %s' <previous>..<tag>` and `git diff --stat <previous>..<tag>`. Draft the user-visible changes from the subjects and diffs, or "No user-visible changes."
- [x] T2: Write `CHANGELOG.md` with plain `## <version>` headings and no Unreleased heading. Add the README link. Update the PROFILE `## changelog` slot and the DESIGN Conventions bullet.
- [x] T3: Compare the file's `## ` headings with the `git tag -l 'v*'` list by a one-line script, and record the result in the work log.
- [x] T4: Review return 1: add the missing 0.3.0, 0.5.1, and 0.7.1 README entries, narrow the 0.6.0 forwarding wording, and drop the 0.3.0 sentence that names no change.

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
- 2026-10-20: review return 1: AC2 fails as written. 0.3.0 omits the README RStudio version note (4ea39f2). 0.7.1 omits the README CDN-code text (825985a) and the `loading` values (4cf5d0a). 0.5.1 omits the CSS Styling page and the removed README sizing text. Also fix the too-broad 0.6.0 "every pair" wording and drop the 0.3.0 no-change sentence. The 0.7.2 rewording is already on disk.
- 2026-10-20: T4 added for review return 1 (minor amendment) and done. Added the 0.3.0 RStudio note, the 0.5.1 CSS Styling page, and the 0.7.1 CDN-code and `loading` entries, each checked with `git show` at its commit or tag. The 0.6.0 wording now excludes `label` and empty values, and the 0.3.0 size sentence is gone. Verify: 19 headings match the tags, `check_aria.py` 0 failures, render ok.
- 2026-10-20: claim audit: not re-run for T4. Each added claim was read against its commit in this session, and review return 1's reviewers read the same ranges.

## Decisions

## Review

- 2026-10-20 sync: branch cut from origin/main c61003d, which has not moved; no PR exists yet (route d); the Copilot round is off.
- AC1: `diff` of `grep '^## ' CHANGELOG.md` against `git tag -l 'v*' | sort -rV` with the `v` removed is empty: 19 sections, 19 tags, same order, no other `## ` section. T3's planted missing heading made the same diff exit 1.
- AC3: `README.md:28` holds `[CHANGELOG.md](CHANGELOG.md) lists the changes in each version.`
- gate: `cairn_validate.py` all checks passed. No principle changed, so `cairn_impact` was skipped. Toolchain: the one version marker (`_extension.yml`) reads 0.7.2, unchanged. `python3 _tests/check_aria.py` 0 failures, and `quarto render` succeeded (its `docs/sitemap.xml` date change was dropped). The changelog check needs no entry, because M002 changes nothing that `quarto add` installs.
- spawned: diff-bug, blame-history, prior-review, ripple
- AC2: not ticked. The diff-bug lens's 19-section ledger finds every entry true and in range, but three sections miss README changes users act on (diff-bug #1, #2, #5), so the criterion fails as written. This is a floor return.
- diff-bug #1: 0.3.0 omits the README RStudio note change in 4ea39f2 (update to RStudio 2022.12.0+353) — fix now (floor return 1)
- diff-bug #2: 0.7.1 omits the README CDN-code explanation (825985a) and the corrected `loading` values with `delay` (4cf5d0a) — fix now (floor return 1)
- diff-bug #3: 0.6.0 "forward every `key=value` pair" is too broad: `label` is reserved and empty values are dropped (verified in `git show v0.6.0:…/lordicon.lua` lines 19-20 and 69) — fix now (return 1)
- diff-bug #4: the 0.7.2 opening sentence is too broad — fix now, same edit as prior-review #1
- diff-bug #5: 0.5.1 omits the new CSS Styling demo page and the README's removed CSS sizing text — fix now (floor return 1)
- diff-bug #6: 0.1.0 has no Babel transpile entry — reject, planned change: the work log's build-tool-only rule, and the bundle stayed in effect the same (claim audit item 1)
- diff-bug #7: the 0.3.0 sentence about the 128-pixel size names no change — fix now (return 1)
- diff-bug #8: 0.6.0's removal of Babel and core-js has no entry — reject, planned change: build-tool-only rule
- diff-bug #9: D-002 Consequences still says the file does not exist — reject, false as a defect: DECISIONS.md is append-only history (IP4), and its consequence came true
- diff-bug #10: the PROFILE release-walk "retitle the development heading" text — reject, false: it is one remedy that applies only when such a heading exists, and the tag-only arm needs none
- diff-bug #11: old player version strings in `lordicon.lua` HTML dependencies get no entry — reject, false as a defect: the reviewer agrees that no entry is correct
- prior-review #1: the 0.7.2 entry said any passed ARIA attribute turns off `aria-hidden="true"`, which the M001 review fixed (8fe774b) — fix now, entry reworded to the README's wording
- prior-review #2: the 0.7.2 entry left out "non-empty" — fix now, same edit
- blame-history #1: the branch does not raise the version — reject, planned change: M002 changes nothing `quarto add` installs (D-001; plan Out)
- blame-history #2: the ROADMAP row moves to review — reject, false as a defect: a normal status step
- ripple #1: the "Start a CHANGELOG.md for releases" candidate row still reads open — reject, planned change: post-merge hygiene graduates a `started M002` row
