# Lordicon Extension for Quarto

This extension provides support for embedding icons from Lordicon into Quarto HTML and Revealjs formats; they can also be customized in appearance. Loading icons from downloaded/edited JSON files is coming soon...

## Installing

```
$ quarto install extension jmgirard/lordicon
```

This will install the extension under the `_extensions` subdirectory. If you're using version control, you will want to check in this directory.

## Using

To embed an icon, use the `{{< li code >}}` shortcode. For example:

```
{{< li wxnxiano >}}
{{< li surjmvno >}}
{{< li jluicbpf >}}
```

Look up the `code` for an icon by browsing [lordicon.com](https://lordicon.com/icons), clicking on an icon you like, going to the sidebar, and clicking on the HTML button. The `code` is displayed at the bottom left of the modal and can be copied to the clipboard using the COPY HTML CODE button (see screenshot of the modal below).

<img src="docs/screenshot.png" />

You can also customize various aspects of the icon's appearance, such as their animation trigger, delay, speed, colors, stroke, scale, and position (see the [HTML example](https://jmgirard.github.io/lordicon/example.html) to see these options in action). 

Icons sizes are controlled by setting CSS for `lord-icon` HTML elements:

```
lord-icon {
  width: 128px;
  height: 128px;
}
```

To style groups of icons, you can pass each icon a CSS class via the shortcode's `class` argument (e.g., `{{< li lupuorrc class=small >}}`).

```
lord-icon.small {
  width: 48px;
  height: 48px;
}
```

## Example

Here is the source code for a minimal example: [example.qmd](https://github.com/jmgirard/lordicon/blob/main/example.qmd)

This is the output of `example.qmd` for [HTML](https://jmgirard.github.io/lordicon/example.html)

Note that there is currently a bug where the icons won't appear in the RStudio Viewer but will appear when the HTML file is opened in a modern browser.

