# wai-aria-1-2: the core ARIA role list and how a browser picks a role

**Provenance.** Ingested 2026-10-25 by M008 from https://www.w3.org/TR/wai-aria-1.2/. The agent fetched it with `curl` and parsed each `<section class="role…">` heading and its "Is Abstract" row.
Pagination: none. The anchors are the spec's section numbers and fragment ids.
Extraction: verified 2026-10-25 against the source by a parse of the fetched HTML, observed 2026-10-25.

**Citation.** Accessible Rich Internet Applications (WAI-ARIA) 1.2. W3C Recommendation 06 June 2023. Editors: James Nurthen, Peter Krautzberger, Scott O'Hara. https://www.w3.org/TR/wai-aria-1.2/

**Role.** This source settles which words count as roles for the nameless-role warning. It also gives the rule that a browser uses the first role token it knows.

## Extracted values

- Role choice, §7.1 Role Attribute (`#host_general_role`): user agents "MUST use the first token" that names a non-abstract role.
- Abstract roles, 12, each with "Is Abstract: True" in §5.4:

  ```
  command composite input landmark range roletype section sectionhead
  select structure widget window
  ```

- Non-abstract roles, 82, from §5.4 Definition of Roles (`#role_definitions`). The deprecated `directory` is in the list.

  ```
  alert alertdialog application article banner blockquote button caption
  cell checkbox code columnheader combobox complementary contentinfo
  definition deletion dialog directory document emphasis feed figure form
  generic grid gridcell group heading img insertion link list listbox
  listitem log main marquee math meter menu menubar menuitem
  menuitemcheckbox menuitemradio navigation none note option paragraph
  presentation progressbar radio radiogroup region row rowgroup rowheader
  scrollbar search searchbox separator slider spinbutton status strong
  subscript superscript switch tab table tablist tabpanel term textbox time
  timer toolbar tooltip tree treegrid treeitem
  ```

- `img`, §5.4 `#img`: "Accessible Name Required: True".

## Traces to

- `_extensions/lordicon/lordicon.lua`: the `KNOWN_ROLES` table takes the 82 names, and the token scan in `warn_nameless_role` takes the first-known-token rule.

## Open questions

- None.
