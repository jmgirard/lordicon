# Lessons

Durable repo lessons — build quirks, testing tricks, gotchas worth
remembering next time — captured at milestone end and surfaced at plan time.
Not status, not decisions: a lesson is a reusable "how this repo actually
behaves" note. Cross-cutting *choices* still go to `DECISIONS.md`.

One line per lesson: `- YYYY-MM-DD (M<NNN>): <lesson>`. Two caps: 50 lines
and 20,000 bytes; over either, retire or prune before adding. Corrected in
place when proven false (never append a correction).

- 2026-10-20 (M001, used M007): Quarto's HTML post-processing lowercases attribute names, letters outside ASCII included, and keeps only one of two names equal after that: the first for an ASCII clash, the last for a non-ASCII one (corrected M004). So a rendered page hides a filter that writes an attribute twice. Read the raw shortcode output with `quarto pandoc lua` and a stubbed `quarto` table, as `_tests/raw_output.lua` does.
- 2026-10-20 (M002, used M010): `quarto render` at the repo root rewrites the `lastmod` date in `docs/sitemap.xml` even when no page changed. Run `git checkout -- docs/sitemap.xml` after a render that is only a check; when a criterion asks for the re-rendered `docs/`, commit it, sitemap included (corrected M003).
- 2026-10-24 (M003, used M009): Lua's `%s`, `%c`, and `string.lower` follow the process locale. Under a UTF-8 locale on macOS, `%c` matches bytes 128-159 and 173 and `%s` matches 160, which occur inside UTF-8 letters such as ß. Spell out byte ranges and ASCII case folding in filter patterns.
- 2026-10-24 (M003, used M007): Python's `splitlines()` also breaks at U+0085, and Python gives child processes a UTF-8 `LC_CTYPE` when it starts under the C locale, so a probe run from the shell and one run from Python can disagree. Split tool output on `"\n"` and set `LC_ALL` for each subprocess.
- 2026-10-24 (M003, used M010): Quarto's HTML post-processing drops a namespaced attribute such as `x:y` from the page, and Pandoc expands a tab in a shortcode argument to spaces. Check such keys in the raw filter output, not the page.
- 2026-10-20 (M002): Tags v0.3.1 and v0.5.1 carry an `_extension.yml` that still names the previous version, so read a tag's version from its tag name, not from the marker file.
- 2026-10-24 (M005, used M010): Quarto drops a quoted shortcode value or positional argument that is all spaces or starts with a space or tab, with no log line: the key never reaches the filter, the next positional argument takes a dropped one's place, and a trailing space survives. `_tests/raw_output.lua` passes such values through as written, so test them with a render, not the raw output.
- 2026-10-24 (M005, used M007): Under `quarto pandoc lua`, the collation locale stays `C` even with `LC_ALL=en_US.UTF-8`, so `table.sort` on strings gives byte order. Check `os.setlocale(nil, "collate")` before blaming the locale for a sort order.
- 2026-10-25 (M007, used M010): A render whose extension did not load leaves each shortcode in the output as literal `{{< … >}}` text and gives no error. A check that a format gets no icon must also fail on `{{<`, or it passes with the extension missing. The repo has no CI workflows, so a PR reports no checks and merges on the local check.
- 2026-10-25 (M008, used M010): The Edit tool writes U+00A0 as a plain space. Put a no-break space or other non-ASCII whitespace into `_tests/aria.qmd` with a short script, and confirm the bytes `302 240` with `od -c`. Quarto keeps U+00A0 and a run of two spaces inside a quoted shortcode value.
- 2026-10-25 (M009): Quarto reads a shortcode twice. Its Lua reader misreads a bare argument with `"`, `\\`, `>}}`, or `=` (as a key), and its check of a call alone on a line rejects a bare argument with a quote or whitespace. In quotes there is no `\"` escape, so use single quotes for a `"`, and `\\` reads as `\`. Test a call both inside a paragraph and on its own line.
- 2026-10-25 (M010): `pandoc.Null` is nil under `quarto pandoc lua` but defined in a Quarto render, so a filter path that returns it breaks `_tests/raw_output.lua`; return `pandoc.Inlines({})` there. A case with no output prints an empty line, so split that output with `removesuffix("\n")`, not `rstrip`.
