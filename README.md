# Lordicon Extension for Quarto

[![Release](https://img.shields.io/github/v/tag/jmgirard/lordicon?label=release&sort=semver)](https://github.com/jmgirard/lordicon/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Quarto](https://img.shields.io/badge/Quarto-%E2%89%A51.3-75AADB?logo=quarto&logoColor=white)](https://quarto.org)

This extension embeds animated [Lordicon](https://lordicon.com) icons in Quarto HTML documents, including Reveal.js presentations. Icons can be pulled directly from the official CDN or loaded from local `.json` files, and their appearance can be customized on the fly — no need to edit the `.json` files.

## Examples

[![Showcase of animated Lordicon icons](./showcase.gif)](https://jmgirard.github.io/lordicon/)

Explore the live demo site for runnable examples and previews:

- [**Home**](https://jmgirard.github.io/lordicon/) — codes, colors, stroke, and accessibility
- [**CSS Styling**](https://jmgirard.github.io/lordicon/css_styling.html) — resize, position, and style icons
- [**Animations**](https://jmgirard.github.io/lordicon/animations.html) — triggers, states, delay, speed, and sequences
- [**Targets**](https://jmgirard.github.io/lordicon/target.html) — trigger an icon from another element

## Installing

```
$ quarto add jmgirard/lordicon
```

This will install the extension under the `_extensions` subdirectory. If you're using version control, you will want to check in this directory.

## Using

To embed an icon from the CDN, use the `{{< li code >}}` shortcode. For example:

```
{{< li wlpxtupd >}}
{{< li rehjpyyh >}}
```

A `code` is the eight-character identifier in an icon's CDN URL (`https://cdn.lordicon.com/CODE.json`), which lordicon.com used to hand out under Export > Embed. That option is no longer part of the redesigned export UI, so codes you already have keep working but new ones may be hard to come by. Prefer `{{< lif file >}}` with a downloaded `.json` for new icons.

---

To embed an icon from a local .json file, use the `{{< lif file >}}` shortcode. For example:

```
{{< lif church.json >}}
{{< lif confetti.json >}}
```

Download an icon's .json file by browsing [lordicon.com](https://lordicon.com/icons), opening an icon, and clicking **Edit and download**. In the panel on the right, open the format menu (it starts on GIF), click the options icon next to **Lottie**, then **Select** and **Export**.

The format menu's options icon offers two Lottie flavors, and the choice depends on how you plan to use the icon:

- **Minified** (the default) bakes the editor's colors and stroke into the shapes and keeps only the animation you selected. The file is much smaller, so this is the better choice when you're happy with how the icon looks in the editor and won't be customizing it from the shortcode.
- **Raw** keeps every animation plus the control layer that `colors`, `stroke`, and `state` write into. Choose this when you want to set those arguments per use — configure the icon from the shortcode rather than in the editor.

> [!NOTE]
> The two don't mix: passing `colors`, `stroke`, or `state` to a minified file has no effect, because the values it would change were already baked in. Either re-export as Raw or drop the argument and set it in the editor instead. The extension warns at render time when it spots that combination.

---

## Customizing

Both shortcodes forward any `key=value` pairs directly to the underlying
[`<lord-icon>` element](https://lordicon.com/docs/web), so you can use the full
element API without the extension needing to know each option:

| Argument   | Description                                                                 |
|------------|-----------------------------------------------------------------------------|
| `colors`   | Recolor the icon, e.g. `colors=primary:gold,secondary:#ee66aa`.             |
| `stroke`   | Line thickness: `light`, `regular`, or `bold` (supported icons).           |
| `trigger`  | Animation trigger: `in`, `click`, `hover`, `loop`, `loop-on-hover`, `morph`, `boomerang`, `sequence`. |
| `state`    | A named animation state exported with the icon (e.g. `state=morph-open`).   |
| `target`   | CSS selector of an ancestor element that fires the trigger (see Targets).    |
| `delay`    | Milliseconds to wait between loops (with `trigger=loop`).                    |
| `speed`    | Playback speed multiplier (e.g. `speed=2`).                                  |
| `loading`  | Defer loading: `lazy` (when scrolled into view), `interaction` (first user action), or `delay` (paired with `loading-delay=MS`). |
| `class`    | CSS class(es) to apply for styling.                                         |
| `style`    | Inline CSS, e.g. `style=width:50px;height:50px;`.                            |
| `label`    | Accessible label (see below).                                               |

Any other attribute the element supports can be passed the same way.

### Accessibility

By default icons are treated as decorative and marked `aria-hidden="true"` so
screen readers skip them. If an icon conveys meaning, give it a `label` and it
will be exposed with `role="img"` and that label instead:

```
{{< li wlpxtupd label="Loading complete" >}}
```

ARIA attributes you pass yourself take precedence over these defaults. If you
pass `aria-hidden`, `aria-label`, `aria-labelledby`, or `role`, the icon is not
marked `aria-hidden="true"`. With `label`, your own `role` or `aria-label`
replaces the one `label` would add. When you set `aria-label` directly, also
pass `role="img"` so screen readers announce the icon:

```
{{< li wlpxtupd role="img" aria-label="Loading complete" >}}
```

## Note

In order for the icons to appear properly in your RStudio Viewer pane, you need to update to RStudio version 2022.12.0+353 or newer. You can still use older versions of RStudio, but to view your icons you will need to view the rendered HTML files in an external browser.
