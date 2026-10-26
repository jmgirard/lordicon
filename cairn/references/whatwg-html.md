# whatwg-html: which characters an HTML attribute name can hold

**Provenance.** Ingested 2026-10-26 by M012 from https://html.spec.whatwg.org/multipage/syntax.html and https://html.spec.whatwg.org/multipage/parsing.html, the Living Standard last updated 26 October 2026. The agent fetched both pages with `curl` and read the sections below in the fetched HTML.
Pagination: none. The anchors are fragment ids.
Extraction: verified 2026-10-26 against the source by a read of the fetched HTML, observed 2026-10-26.

**Citation.** HTML Living Standard. WHATWG, last updated 26 October 2026. https://html.spec.whatwg.org/

**Role.** This source settles which shortcode keys the filter treats as invalid attribute names: the characters that the authoring rule forbids, and `<`, which the parser accepts but reports as an error.

## Extracted values

- §13.1.2.3 Attributes, `syntax.html#attributes-2`: attribute names consist of one or more characters other than controls, U+0020 SPACE, `"`, `'`, `>`, `/`, `=`, and noncharacters. `<` is not in that list. "Noncharacter" is defined in whatwg-infra (§4.6).
- §13.2.2 Parse errors, `parsing.html#parse-error-unexpected-character-in-attribute-name`: when the parser meets `"`, `'`, or `<` in an attribute name, it reports the parse error `unexpected-character-in-attribute-name`. The parser keeps such code points in the name.
- §13.2.5.33 Attribute name state, `parsing.html#attribute-name-state`: `"`, `'`, and `<` give that parse error and are then appended to the name like any other character. Tab, LF, FF, space, `/`, and `>` end the name, and `=` starts the value.

## Traces to

- `_extensions/lordicon/lordicon.lua`: `invalid_name` and the invalid-name warning's reason (M012). D-003 set the earlier skip set.

## Open questions

- None.
