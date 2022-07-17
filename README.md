# Lordicon Extension for Quarto

This extension provides support including free icons provided by Lordicon. Icons can be used in HTML and Revealjs formats. Icon customization and loading icons (including premium icons) from JSON files is coming soon...

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

You can also customize various aspects of the icon's appearance, such as their animation trigger, delay, speed, colors, stroke, scale, and position (see the [HTML example](https://jmgirard.github.io/lordicon/example.html) to see these options in action). Icon sizing and background color are controlled by setting CSS for `lord-icon` HTML elements:

```
lord-icon {
  width: 128px;
  height: 128px;
}
```

## Example

Here is the source code for a minimal example: [example.qmd](https://github.com/jmgirard/lordicon/blob/main/example.qmd)

This is the output of `example.qmd` for [HTML](https://jmgirard.github.io/lordicon/example.html)
