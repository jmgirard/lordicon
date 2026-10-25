# graphics-aria-1-0: the graphics role list and the `graphics-symbol img` fallback

**Provenance.** Ingested 2026-10-25 by M008 from https://www.w3.org/TR/graphics-aria-1.0/. The agent fetched it with `curl` and parsed each `<section class="role…">` heading and its characteristics rows.
Pagination: none. The anchors are the spec's section numbers and fragment ids.
Extraction: verified 2026-10-25 against the source by a parse of the fetched HTML, observed 2026-10-25.

**Citation.** WAI-ARIA Graphics Module. W3C Recommendation 02 October 2018. https://www.w3.org/TR/2018/REC-graphics-aria-1.0-20181002/

**Role.** This source settles which `graphics-` words count as roles for the nameless-role warning. It also shows why `graphics-symbol` warns like `img`.

## Extracted values

- Roles, 3, from §4.1 Definition of Roles (`#role_definitions`). None is abstract.

  ```
  graphics-document graphics-object graphics-symbol
  ```

- `graphics-symbol`, §4.1 `#graphics-symbol`: "Superclass Role: img" and "Accessible Name Required: True". The change log names `group` as a later superclass. The characteristics table, read here, says `img`.
- Fallback: the spec's examples write `role="graphics-symbol img"`. A browser that does not know `graphics-symbol` then uses `img`.

## Traces to

- `_extensions/lordicon/lordicon.lua`: the `KNOWN_ROLES` table takes the 3 names. The image-role set in `warn_nameless_role` takes `graphics-symbol`.

## Open questions

- None.
