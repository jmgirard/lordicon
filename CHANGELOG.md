# Changelog

This file lists the changes in each version of the extension, newest first.

## 0.7.2

- ARIA attributes that you pass now take precedence over the extension's defaults. If you pass a non-empty `aria-hidden`, `aria-label`, `aria-labelledby`, or `role`, the extension does not add `aria-hidden="true"`. With `label`, your own `role` or `aria-label` replaces the one that `label` adds.
- If you set `aria-label` or `aria-labelledby` yourself, the README and the demo home page now advise you to also pass `role="img"`.

## 0.7.1

- If a Minified Lottie export gets `colors`, `stroke`, or `state`, `lif` warns once per file at render time in HTML output. These arguments have no effect on that export. The warning names the two fixes. A file that the extension cannot open gets no warning.
- The README explains the Raw and Minified Lottie exports and the new download path on lordicon.com.
- The README says what a CDN code is and that the export UI on lordicon.com no longer offers codes. It recommends `lif` with a downloaded `.json` file for new icons.
- The README lists the `delay` value of `loading`, used with `loading-delay=MS`.
- The demo site is now a themed Quarto website with Speed, Sequence, and accessibility examples. Its home page moved from `example.html` to the site root, so old links to `example.html` no longer work.

## 0.7.0

- The bundled player is now `@lordicon/element` 2.3.1, which no longer needs `lottie-web`. The bundle is smaller. The shortcode arguments do not change.

## 0.6.0

- The extension now requires Quarto 1.3.0 or later.
- Both shortcodes forward each `key=value` pair with a non-empty value, except `label`, to the `<lord-icon>` element as an attribute. Options such as `speed`, `loading`, and `id` work with no extension update.
- Attribute values are HTML-escaped.
- New `label` argument. It gives the icon `role="img"` and `aria-label`. An icon without `label` gets `aria-hidden="true"`.

## 0.5.4

- The bundled player is updated to `@lordicon/element` 1.11.0 and `lottie-web` 5.13.0.
- The README's lordicon.com steps follow the site's new export menu.

## 0.5.3

- The bundled player is updated to `@lordicon/element` 1.10.1.

## 0.5.2

- The bundled player is updated to `@lordicon/element` 1.9.0.
- `_extension.yml` now reads 0.5.2. In the 0.5.1 release it still read 0.5.0.

## 0.5.1

- New `target` argument: a CSS selector of an ancestor element that fires the icon's trigger.
- New demo pages for animations, targets, and CSS styling, linked from the README. The README's CSS sizing text moved to the CSS Styling page.
- Every example icon is a free icon.

## 0.5.0

- New `state` and `style` arguments.
- The `speed`, `scale`, `x`, and `y` arguments are removed.
- The extension no longer gives icons a default size of 128 by 128 pixels. Set the size with `class` or `style`.
- The README's lordicon.com steps change to Export > Embed HTML for a code and Export > JSON (Lottie) for a file.
## 0.4.2

- The bundled player is updated to `@lordicon/element` 1.8.0.

## 0.4.1

- The bundled player is updated to `@lordicon/element` 1.5.1.

## 0.4.0

- The bundled player now comes from the `@lordicon/element` package (1.4.2), which replaces `lord-icon-element`.

## 0.3.2

- `_extension.yml` now reads 0.3.2. In the 0.3.1 release it still read 0.3.0.

## 0.3.1

- The bundled player is rebuilt with `lottie-web` 5.12.2.
- The README install command is now `quarto add jmgirard/lordicon`.

## 0.3.0

- The extension no longer sets the text color and background of the page `body`, which broke the dark mode toggle (#2).
- The bundled player is updated to `lord-icon-element` 3.4.4 and `lottie-web` 5.10.2.
- The README says that the RStudio Viewer shows icons from RStudio 2022.12.0+353.

## 0.2.0

- New `lif` shortcode: an icon from a local Lottie `.json` file, with the same arguments as `li`.
- The README's RStudio Viewer note says which RStudio release fixes the bug.
- The README explains how to find an icon's code and how to download its `.json` file on lordicon.com.

## 0.1.0

- The README notes a bug: icons do not appear in the RStudio Viewer.

## 0.0.2

- New arguments: `trigger`, `speed`, `delay`, `colors`, `stroke`, `scale`, `x`, `y`, and `class`. The `x` and `y` arguments set `axis-x` and `axis-y`.
- `li` no longer sets `trigger="loop"` by default.
- The README explains how to size icons with CSS and how to style groups of icons with `class`.

## 0.0.1

- First release. The `li` shortcode embeds the icon at `https://cdn.lordicon.com/CODE.json` with `trigger="loop"` in HTML output. Other formats get no output. The extension's CSS sets the page `body` colors and a 128 by 128 pixel icon size. The bundled player is `lord-icon-element` 3.4.2 with `lottie-web` 5.9.6.
