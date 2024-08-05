# Lordicon Extension for Quarto

This extension provides support for embedding animated icons from Lordicon into Quarto HTML files (including RevealJS presentations). The icons can be pulled directly from the official CDN or loaded via local .json files; they can also be customized in appearance on-the-fly (without needing to edit the .json files).

## Example

[![](https://i.imgur.com/4uC2Mqy.png)](https://jmgirard.github.io/lordicon/example.html)

[HTML Demo](https://jmgirard.github.io/lordicon/example.html) ([Source Code](https://github.com/jmgirard/lordicon/blob/main/example.qmd))

## Installing

```
$ quarto add jmgirard/lordicon
```

This will install the extension under the `_extensions` subdirectory. If you're using version control, you will want to check in this directory.

## Using

To embed an icon from the CDN, use the `{{< li code >}}` shortcode. For example:

```
{{< li wlpxtupd >}}
{{< li lupuorrc >}}
```

Look up an icon's `code` by browsing [lordicon.com](https://lordicon.com/icons), clicking on an icon and choosing Export > Embed HTML.

---

To embed an icon from a local .json file, use the `{{< lif file >}}` shortcode. For example:

```
{{< lif church.json >}}
{{< lif confetti.json >}}
```

Download an icon's .json file by browsing [lordicon.com](https://lordicon.com/icons), clicking on an icon, and choosing Export > JSON (Lottie).

---

You can also customize various aspects of the icon's appearance and animation (see the [HTML example](https://jmgirard.github.io/lordicon/example.html) to see these options in action). 

## Note

In order for the icons to appear properly in your RStudio Viewer pane, you need to update to RStudio version 2022.12.0+353 or newer. You can still use older versions of RStudio, but to view your icons you will need to view the rendered HTML files in an external browser.
