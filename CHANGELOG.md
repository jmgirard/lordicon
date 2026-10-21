# Changelog

This file lists the user-visible changes in each version of the extension, newest first.

## 0.7.2

- An ARIA attribute that you pass now replaces the default that the extension adds. The attributes are `aria-hidden`, `aria-label`, `aria-labelledby`, and `role`. Without `label`, any of these attributes turns off `aria-hidden="true"`. With `label`, a `role` or `aria-label` that you pass replaces `role="img"` or the label text.

## 0.7.1

- If a Minified Lottie export gets `colors`, `stroke`, or `state`, `lif` warns at render time. These arguments have no effect on that export. The warning names the two fixes.
- The README explains the Raw and Minified Lottie exports and the new download path on lordicon.com.
- The demo site is now a themed Quarto website with Speed, Sequence, and accessibility examples.

## 0.7.0

- The bundled player is now `@lordicon/element` 2.3.1, which no longer needs `lottie-web`. The bundle is smaller. The shortcode arguments do not change.

## 0.6.0

- Both shortcodes forward every `key=value` pair to the `<lord-icon>` element as an attribute. Options such as `speed`, `loading`, and `id` work with no extension update.
- Attribute values are HTML-escaped.
- New `label` argument. It gives the icon `role="img"` and `aria-label`. An icon without `label` gets `aria-hidden="true"`.

## 0.5.4

- The bundled player is updated to `@lordicon/element` 1.11.0 and `lottie-web` 5.13.0.

## 0.5.3

- The bundled player is updated to `@lordicon/element` 1.10.1.

## 0.5.2

- The bundled player is updated to `@lordicon/element` 1.9.0.

## 0.5.1

- New `target` argument: a CSS selector of an ancestor element that fires the icon's trigger.
- The README and demo pages add animation and target examples, and every example icon is a free icon.

## 0.5.0

- New `state` and `style` arguments.
- The `speed`, `scale`, `x`, and `y` arguments are removed.
- The README has new usage instructions and an animated screenshot.

## 0.4.2

- The bundled player is updated to `@lordicon/element` 1.8.0.

## 0.4.1

- The bundled player is updated to `@lordicon/element` 1.5.1.

## 0.4.0

- The bundled player now comes from the `@lordicon/element` package (1.4.2), which replaces `lord-icon-element`.

## 0.3.2

- `_extension.yml` now reads 0.3.2. In the 0.3.1 release it still read 0.3.0.

## 0.3.1

- The bundled player is rebuilt with `lord-icon-element` 3.4.4 and `lottie-web` 5.12.2.
- The README install command is now `quarto add jmgirard/lordicon`.

## 0.3.0

- The extension no longer sets the text color and background of the page `body`, which broke dark mode (#2). Icons keep their default size of 128 by 128 pixels.

## 0.2.0

- New `lif` shortcode: an icon from a local Lottie `.json` file, with the same arguments as `li`.
- The README describes a bug in the RStudio Viewer.

## 0.1.0

- The bundled player is built with Babel and core-js for older browsers.

## 0.0.2

- New arguments: `trigger`, `speed`, `delay`, `colors`, `stroke`, `scale`, `x`, `y`, and `class`. The `x` and `y` arguments set `axis-x` and `axis-y`.
- `li` no longer sets `trigger="loop"` by default.

## 0.0.1

- First release. The `li` shortcode embeds the icon at `https://cdn.lordicon.com/CODE.json` with `trigger="loop"` in HTML output. Other formats get no output. The extension's CSS sets the page `body` colors and a 128 by 128 pixel icon size.
