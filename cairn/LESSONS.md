# Lessons

Durable repo lessons — build quirks, testing tricks, gotchas worth
remembering next time — captured at milestone end and surfaced at plan time.
Not status, not decisions: a lesson is a reusable "how this repo actually
behaves" note. Cross-cutting *choices* still go to `DECISIONS.md`.

One line per lesson: `- YYYY-MM-DD (M<NNN>): <lesson>`. Two caps: 50 lines
and 20,000 bytes; over either, retire or prune before adding. Corrected in
place when proven false (never append a correction).

- 2026-10-20 (M001): Quarto's HTML post-processing keeps only the first of two same-name attributes, so a rendered page hides a filter that writes an attribute twice. Read the raw shortcode output with `quarto pandoc lua` and a stubbed `quarto` table, as `_tests/raw_output.lua` does.
