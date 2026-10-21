# Design

_Seeded by cairn-init on 2026-10-20 from the README and a read of the source.
Every section is a draft for the maintainer to refine; `/design-interview`
elicits what the code cannot show._

## Purpose & Scope

A Quarto extension that embeds animated Lordicon icons in HTML output,
Reveal.js slides included. Users install it with `quarto add jmgirard/lordicon`.
It ships two shortcodes and a bundled copy of the `<lord-icon>` web component.
Icons come from the Lordicon CDN by code or from local Lottie `.json` files.
Non-HTML formats, and HTML without JavaScript, get no output from a shortcode.
The repo also holds the demo website (`*.qmd` at the root, rendered to `docs/`
for GitHub Pages). _To refine: who the users are and what stays out of scope._

## Function Families

- `{{< li CODE ... >}}`: an icon from `https://cdn.lordicon.com/CODE.json`.
- `{{< lif FILE ... >}}`: an icon from a local Lottie file, with a render-time
  warning when a Minified export meets `colors`, `stroke`, or `state`.

## Conventions

Observed in the code, not yet confirmed by the maintainer:

- Every shortcode `key=value` except `label` goes to the `<lord-icon>` element
  as an attribute, so the extension follows the element API without listing it.
  Attributes are escaped and sorted for stable output.
- `label` gives `role="img"` and `aria-label`; no label gives `aria-hidden="true"`.
- `BUNDLE_VERSION` in `lordicon.lua` matches the `@lordicon/element` version in
  `package.json`. It is the cache-busting version of `assets/js/bundle.js`.
- The extension version is `version:` in `_extensions/lordicon/_extension.yml`.
  The repo keeps no changelog file. Commit subjects name the version (`(v0.7.1)`).

## Design Principles

_None elicited yet. Inviolable principles (IP<n>, hard constraints) come first,
then Guiding principles (GP<n>, tradeable with justification). Numbers are never
reused. Run `/design-interview` to elicit them._

## Architecture

- `_extensions/lordicon/lordicon.lua`: the shortcode filter. It adds the bundle
  as an HTML dependency and returns a raw `<lord-icon>` element.
- `_extensions/lordicon/assets/js/bundle.js`: the committed webpack build of
  `src/main.js`, which calls `defineElement()` from `@lordicon/element` v2.
  `npm run build` rebuilds it (`webpack.config.js`).
- Demo site: `_quarto.yml`, `index.qmd`, `css_styling.qmd`, `animations.qmd`,
  `target.qmd`, `custom.scss`, rendered to the committed `docs/` directory.

## Known issues

- lordicon.com no longer gives out CDN codes in its export UI, so `li` works for
  codes users already have but new codes are hard to find (README).
- RStudio Viewer shows icons only from version 2022.12.0+353 (README).
