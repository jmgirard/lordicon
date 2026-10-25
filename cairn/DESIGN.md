# Design

_Seeded by cairn-init on 2026-10-20 and filled by `/design-interview` the same
day, with the maintainer's answers._

## Purpose & Scope

A Quarto extension that embeds animated Lordicon icons in HTML output.
Users install it with `quarto add jmgirard/lordicon`, which installs from
`main`, so every merge to `main` reaches users at once.

The users are Quarto authors who are not web developers. They should not need
to know HTML or the `<lord-icon>` element. Warnings say what to do in plain
words, and the docs explain the parts of the lordicon.com export UI that matter.

All formats where `quarto.doc.isFormat("html:js")` is true are commitments:
HTML documents, websites, books, and Reveal.js slides. A break in one of them
is a bug. Previewers such as the RStudio Viewer are best-effort. Other formats
get no output from a shortcode, by design.

The demo website (the root `*.qmd` files, rendered to the committed `docs/`
directory for GitHub Pages) is part of the deliverable. Each user-facing
feature gets an example there, and `docs/` is re-rendered in the same change.

### Contract boundary

The extension is a passthrough with guardrails. It forwards each shortcode
`key=value` to the `<lord-icon>` element, except the keys that Conventions
lists, and does not validate attribute values (corrected M003).
The element's documentation (lordicon.com/docs/web) owns their meaning.

The extension adds its own behavior in two cases only. A guardrail is added
where an icon fails with no visible error, for example the Minified-export
warning (825985a). A new shortcode argument or shortcode is added only for
behavior that passthrough cannot give, for example `label` to ARIA attributes.
Convenience shorthands do not qualify.

## Function Families

- `{{< li CODE ... >}}`: an icon from `https://cdn.lordicon.com/CODE.json`.
- `{{< lif FILE ... >}}`: an icon from a local Lottie file, with a render-time
  warning when a Minified export meets `colors`, `stroke`, or `state` in any
  letter case (corrected M004).

## Conventions

- Every shortcode `key=value` with a non-empty value goes to the `<lord-icon>`
  element as an attribute, except three kinds of key: `label` in lowercase; `src` in any
  letter case; and a key that is empty or holds whitespace, a control
  character, `"`, `'`, `>`, `/`, or `=`. For each call, the render gives one
  warning per kind for the last two kinds (D-003, corrected M003). Attributes
  are escaped and sorted for stable output.
- `label` gives `role="img"` and `aria-label`, each only when the user did not
  pass it. No label gives `aria-hidden="true"`, unless the user passes a
  non-empty `aria-hidden`, `aria-label`, `aria-labelledby`, or `role` (corrected M001).
  These four names match in any letter case (corrected M003).
- An icon whose kept `role` has `img`, `image`, or `graphics-symbol` as its
  first token that names a role in `KNOWN_ROLES` (WAI-ARIA 1.2, DPUB-ARIA 1.1,
  Graphics-ARIA 1.0, and `image`), with no `aria-label`, `aria-labelledby`,
  `title`, `hidden`, or `inert` and no `aria-hidden` of `true`, gets one render
  warning per call that it has no name (M005, corrected M008).
- Forwarded keys in one call that are equal after `pandoc.text.lower`, and a
  forwarded key such as `Label` that lowercases to `label`, still reach the
  element, and the render gives one warning per kind for each call (M004).
  The Minified check matches `colors`, `stroke`, and `state` in any ASCII
  letter case.
- The player reaches readers as a self-hosted bundle. webpack builds
  `@lordicon/element` into the committed `assets/js/bundle.js`, and the
  extension never loads a script from a third-party host. A `lif` icon needs no
  network access.
- `BUNDLE_VERSION` in `lordicon.lua` matches the `@lordicon/element` version in
  `package.json`. It is the cache-busting version of `assets/js/bundle.js`.
- The shortcode names, `label`, and the passthrough meaning are a stable surface.
  A breaking change ships only after one release that warns about it. D-003
  narrows this: the `src` and invalid-name skips shipped in 0.7.3 with no
  warning release first (corrected M003).
- The extension version is `version:` in `_extensions/lordicon/_extension.yml`.
- The extension version rises in each merge that ships a user-visible change
  (D-001). The changelog is `CHANGELOG.md` (D-002), with one `## <version>`
  section per version, newest first.

## Design Principles

Elicited by `/design-interview` on 2026-10-20. Numbers run within each type and
are never reused or renumbered; retiring one takes a D-entry.

### Inviolable

- IP1: (Passthrough) Every user attribute reaches `<lord-icon>` unchanged.
  The extension may warn about a value but never drops or rewrites one. A
  default the extension adds (such as `aria-hidden`) yields to a user-supplied
  attribute. The documented exceptions are the reserved keys (`label`, and
  `src` in any letter case) and keys that HTML does not allow as attribute
  names. The render warns about each such skipped key with a non-empty value,
  except `label` (D-003). A call whose first argument is empty makes no
  element, so its keys reach none, and the render warns (D-005).
- IP2: (Escaping) Every user value in emitted HTML is escaped: attribute
  values, the label, and the `li` code inside `src`.
- IP3: (A shortcode never fails a render) Non-HTML formats get no output, and
  problems become warnings, not errors. Whether a given problem earns a warning
  is a GP2 matter.
- IP4: (Self-hosted player) The extension never loads a script from a
  third-party host at read time. The icon JSON that `li` fetches from
  cdn.lordicon.com is the author's choice per icon, not the player.
- IP5: (Stable surface) `li`, `lif`, `label`, and the passthrough meaning do
  not break without one release that warns first. This covers removal of `li`
  too: no silent break, not "forever". An upstream change to an attribute's
  meaning is Lordicon's break, not the extension's. D-003 narrows this rule:
  skipping `src` and invalid attribute names started in 0.7.3 with no warning
  release first, because such keys never gave one valid attribute. D-005
  narrows it too: an empty first argument has made no element since 0.7.10
  with no warning release first, because such a call never loaded an icon.
- IP6: (Free-license icons only) Every icon in the repo (demo pages, `docs/`,
  README examples, sample `.json` files) is one that Lordicon's free license
  lets anyone redistribute.

### Guiding

- GP1: (Containment) The extension adds only the player bundle and
  `<lord-icon>` elements to a page, with no page-level CSS or script (issue #2,
  fixed in 4dd3edc). Page styling is the author's job through `class` or `style`.
- GP2: (Guardrails for silent failures) A check is added only where an icon
  fails with no visible error, and its warning says in plain words what to do.
  The Minified-export warning (825985a) is the model.
- GP3: (New surface only where passthrough cannot reach) A new argument or
  shortcode is added only for extension-side behavior, such as `label` to ARIA.
  Convenience shorthands do not qualify.
- GP4: (The demo site ships with the feature) Each user-facing feature gets an
  example on the demo site, and `docs/` is re-rendered in the same change. A
  hotfix with no new surface needs only the re-render.
- GP5: (Decorative by default) An icon without `label` is `aria-hidden`,
  unless the user passes a non-empty `aria-hidden`, `aria-label`,
  `aria-labelledby`, or `role` in any letter case. A labeled icon gets
  `role="img"` and `aria-label`, and each yields to the user's own (IP1)
  (corrected M005, D-004).

## Architecture

- `_extensions/lordicon/lordicon.lua`: the shortcode filter. It adds the bundle
  as an HTML dependency and returns a raw `<lord-icon>` element.
- `_extensions/lordicon/assets/js/bundle.js`: the committed webpack build of
  `src/main.js`, which calls `defineElement()` from `@lordicon/element` v2.
  `npm run build` rebuilds it (`webpack.config.js`).
- Demo site: `_quarto.yml`, `index.qmd`, `css_styling.qmd`, `animations.qmd`,
  `target.qmd`, `custom.scss`, rendered to the committed `docs/` directory.
  The `render: ["*.qmd"]` list in `_quarto.yml` limits the site to root `.qmd`
  pages, so a new page in another format must be added to that list.
- `_tests/`: `check_aria.py` checks the attributes of `aria.qmd` icons (ARIA,
  `src`, skipped and kept keys, key spelling, letter-case clashes, image
  roles with no name, attribute order, values that start with a space or
  tab) in the rendered page and in the raw filter output from
  `raw_output.lua`, that calls with a missing or empty first argument give no
  icon (M011), and the
  lordicon warnings in the render's log. `check_aria.py` models Quarto's drop
  of a value or first argument that starts with a space or tab before it
  hands the calls to `raw_output.lua` (M010). It also renders `aria.qmd` to `gfm` and checks that the
  output holds no icon and no unexpanded shortcode, and the log no lordicon
  warning (M007).

## Known issues

- The only automated check is `_tests/check_aria.py` (M001, extended M003,
  M004, M005, M007, M009, M010, and M011), which covers ARIA attributes, `src`, skipped and kept
  keys, letter-case warnings, the nameless-role warning, the Minified warning
  and its once-per-path rule, the quoted first argument in a warning's call,
  attribute order under the C locale, `gfm` output, the warning for a call
  with no first argument or an empty one, and values and first arguments that Quarto drops
  because they start with a space or tab. The bundle dependency, the lookup of a `lif` file next to the
  document, a missing `lif` file, and formats other than HTML and `gfm` have
  no test, and the demo site's icons are checked by eye (corrected M007).
- lordicon.com no longer gives out CDN codes in its export UI, so `li` works for
  codes users already have but new codes are hard to find (README).
- RStudio Viewer shows icons only from version 2022.12.0+353 (README).
