# wai-aria-1-3: the `image` role, a synonym of `img`

**Provenance.** Ingested 2026-10-25 by M008 from https://w3c.github.io/aria/, the Editor's Draft of 21 October 2026. The agent fetched it with `curl` and read it at `#image` and `#img`.
Pagination: none. The anchors are fragment ids.
Extraction: verified 2026-10-25 against the source by a read of the fetched HTML, observed 2026-10-25.

**Citation.** Accessible Rich Internet Applications (WAI-ARIA) 1.3. W3C Editor's Draft 21 October 2026. https://w3c.github.io/aria/

**Role.** This source settles only that `image` is a role with the same meaning as `img`. The draft's other roles stay out of the filter's list. The M008 plan gate chose this, and the parked ROADMAP row "Know the WAI-ARIA 1.3 draft roles" holds the rest.

## Extracted values

- `image`, `#image`: "A container for a collection of elements that form an image. See synonym `img`."
- `img`, `#img`: the same text, with "See synonym `image`."

## Traces to

- `_extensions/lordicon/lordicon.lua`: the `KNOWN_ROLES` table and the image-role set in `warn_nameless_role` take `image`. The warning covers it since 0.7.5.

## Open questions

- The draft can change before it becomes a Recommendation, observed 2026-10-25.
