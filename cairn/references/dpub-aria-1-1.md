# dpub-aria-1-1: the digital publishing role list

**Provenance.** Ingested 2026-10-25 by M008 from https://www.w3.org/TR/dpub-aria-1.1/. The agent fetched it with `curl` and parsed each `<section class="role…">` heading.
Pagination: none. The anchors are the spec's section numbers and fragment ids.
Extraction: verified 2026-10-25 against the source by a parse of the fetched HTML, observed 2026-10-25.

**Citation.** Digital Publishing WAI-ARIA Module 1.1. W3C Recommendation 12 June 2025. https://www.w3.org/TR/dpub-aria-1.1/

**Role.** This source settles which `doc-` words count as roles for the nameless-role warning. It also shows that `doc-cover` needs no warning.

## Extracted values

- Roles, 41, from §3.1 Definition of Roles (`#role_definitions`). None is abstract. The deprecated `doc-biblioentry` and `doc-endnote` are in the list.

  ```
  doc-abstract doc-acknowledgments doc-afterword doc-appendix doc-backlink
  doc-biblioentry doc-bibliography doc-biblioref doc-chapter doc-colophon
  doc-conclusion doc-cover doc-credit doc-credits doc-dedication doc-endnote
  doc-endnotes doc-epigraph doc-epilogue doc-errata doc-example doc-footnote
  doc-foreword doc-glossary doc-glossref doc-index doc-introduction
  doc-noteref doc-notice doc-pagebreak doc-pagefooter doc-pageheader
  doc-pagelist doc-part doc-preface doc-prologue doc-pullquote doc-qna
  doc-subtitle doc-tip doc-toc
  ```

- `doc-cover`, §3.1 `#doc-cover`: "Superclass Role: img" and "Accessible Name Required: False".

## Traces to

- `_extensions/lordicon/lordicon.lua`: the `KNOWN_ROLES` table takes the 41 names. The filter knows `doc-cover` but gives it no warning.

## Open questions

- None.
