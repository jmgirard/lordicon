# whatwg-infra: the 66 Unicode noncharacters

**Provenance.** Ingested 2026-10-26 by M012 from https://infra.spec.whatwg.org/, the Living Standard last updated 19 October 2026. The agent fetched it with `curl` and read §4.6 at `#noncharacter` in the fetched HTML.
Pagination: none. The anchors are fragment ids.
Extraction: verified 2026-10-26 against the source by a read of the fetched HTML, observed 2026-10-26.

**Citation.** Infra Living Standard. WHATWG, last updated 19 October 2026. https://infra.spec.whatwg.org/

**Role.** This source defines the noncharacters that whatwg-html (§13.1.2.3) forbids in an attribute name.

## Extracted values

- §4.6 Code points, `#noncharacter`: a noncharacter is a code point in the range U+FDD0 to U+FDEF inclusive, or one of the last two code points of a plane. These are U+FFFE, U+FFFF, U+1FFFE, U+1FFFF, and so on through U+10FFFE, U+10FFFF, for all 17 planes.
- Count: 32 in U+FDD0 to U+FDEF, plus 2 × 17 = 34 plane ends, 66 in all.

## Traces to

- `_extensions/lordicon/lordicon.lua`: `invalid_name` (M012).
- `_tests/check_aria.py`: builds the 66 code points from these ranges (M012).

## Open questions

- None.
