# Lessons

Durable repo lessons — build quirks, testing tricks, gotchas worth
remembering next time — captured at milestone end and surfaced at plan time.
Not status, not decisions: a lesson is a reusable "how this repo actually
behaves" note. Cross-cutting *choices* still go to `DECISIONS.md`.

One line per lesson: `- YYYY-MM-DD (M<NNN>): <lesson>`. Two caps: 50 lines
and 20,000 bytes; over either, retire or prune before adding. Corrected in
place when proven false (never append a correction).

- 2026-10-20 (M001): Quarto's HTML post-processing keeps only the first of two same-name attributes, so a rendered page hides a filter that writes an attribute twice. Read the raw shortcode output with `quarto pandoc lua` and a stubbed `quarto` table, as `_tests/raw_output.lua` does.
- 2026-10-20 (M002): `quarto render` at the repo root rewrites the `lastmod` date in `docs/sitemap.xml` even when no page changed. Run `git checkout -- docs/sitemap.xml` after a render that is only a check; when a criterion asks for the re-rendered `docs/`, commit it, sitemap included (corrected M003).
- 2026-10-24 (M003): Lua's `%s`, `%c`, and `string.lower` follow the process locale. Under a UTF-8 locale on macOS, `%c` matches bytes 128-159 and 173 and `%s` matches 160, which occur inside UTF-8 letters such as ß. Spell out byte ranges and ASCII case folding in filter patterns.
- 2026-10-24 (M003): Python's `splitlines()` also breaks at U+0085, and Python gives child processes a UTF-8 `LC_CTYPE` when it starts under the C locale, so a probe run from the shell and one run from Python can disagree. Split tool output on `"\n"` and set `LC_ALL` for each subprocess.
- 2026-10-24 (M003): Quarto's HTML post-processing drops a namespaced attribute such as `x:y` from the page, and Pandoc expands a tab in a shortcode argument to spaces. Check such keys in the raw filter output, not the page.
- 2026-10-20 (M002): Tags v0.3.1 and v0.5.1 carry an `_extension.yml` that still names the previous version, so read a tag's version from its tag name, not from the marker file.
