# Lessons

Durable repo lessons — build quirks, testing tricks, gotchas worth
remembering next time — captured at milestone end and surfaced at plan time.
Not status, not decisions: a lesson is a reusable "how this repo actually
behaves" note. Cross-cutting *choices* still go to `DECISIONS.md`.

One line per lesson: `- YYYY-MM-DD (M<NNN>): <lesson>`. Two caps: 50 lines
and 20,000 bytes; over either, retire or prune before adding. Corrected in
place when proven false (never append a correction).

- 2026-10-20 (M001): Quarto's HTML post-processing keeps only the first of two same-name attributes, so a rendered page hides a filter that writes an attribute twice. Read the raw shortcode output with `quarto pandoc lua` and a stubbed `quarto` table, as `_tests/raw_output.lua` does.
- 2026-10-20 (M002): `quarto render` at the repo root rewrites the `lastmod` date in `docs/sitemap.xml` even when no page changed. Run `git checkout -- docs/sitemap.xml` after a render that is only a check.
- 2026-10-20 (M002): Tags v0.3.1 and v0.5.1 carry an `_extension.yml` that still names the previous version, so read a tag's version from its tag name, not from the marker file.
