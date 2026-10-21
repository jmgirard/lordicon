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

The extension is a passthrough with guardrails. It forwards every shortcode
`key=value` to the `<lord-icon>` element and does not validate attribute values.
The element's documentation (lordicon.com/docs/web) owns their meaning.

The extension adds its own behavior in two cases only. A guardrail is added
where an icon fails with no visible error, for example the Minified-export
warning (825985a). A new shortcode argument or shortcode is added only for
behavior that passthrough cannot give, for example `label` to ARIA attributes.
Convenience shorthands do not qualify.

## Function Families

- `{{< li CODE ... >}}`: an icon from `https://cdn.lordicon.com/CODE.json`.
- `{{< lif FILE ... >}}`: an icon from a local Lottie file, with a render-time
  warning when a Minified export meets `colors`, `stroke`, or `state`.

## Conventions

- Every shortcode `key=value` except `label` goes to the `<lord-icon>` element
  as an attribute. Attributes are escaped and sorted for stable output.
- `label` gives `role="img"` and `aria-label`; no label gives `aria-hidden="true"`.
- The player reaches readers as a self-hosted bundle. webpack builds
  `@lordicon/element` into the committed `assets/js/bundle.js`, and the
  extension never loads a script from a third-party host. A `lif` icon needs no
  network access.
- `BUNDLE_VERSION` in `lordicon.lua` matches the `@lordicon/element` version in
  `package.json`. It is the cache-busting version of `assets/js/bundle.js`.
- The shortcode names, `label`, and the passthrough meaning are a stable surface.
  A breaking change ships only after one release that warns about it.
- The extension version is `version:` in `_extensions/lordicon/_extension.yml`.
- The extension version rises in each merge that ships a user-visible change
  (D-001). The changelog is `CHANGELOG.md` (D-002), not yet created.

## Design Principles

Elicited by `/design-interview` on 2026-10-20. Numbers run within each type and
are never reused or renumbered; retiring one takes a D-entry.

### Inviolable

- IP1: (Passthrough) Every user attribute reaches `<lord-icon>` unchanged.
  The extension may warn about a value but never drops or rewrites one. A
  default the extension adds (such as `aria-hidden`) yields to a user-supplied
  attribute. Reserved keys (`label`) are the documented exception.
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
  meaning is Lordicon's break, not the extension's.
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
- GP5: (Decorative by default) An icon without `label` is `aria-hidden`; a
  labeled icon gets `role="img"` and `aria-label`.

## Architecture

- `_extensions/lordicon/lordicon.lua`: the shortcode filter. It adds the bundle
  as an HTML dependency and returns a raw `<lord-icon>` element.
- `_extensions/lordicon/assets/js/bundle.js`: the committed webpack build of
  `src/main.js`, which calls `defineElement()` from `@lordicon/element` v2.
  `npm run build` rebuilds it (`webpack.config.js`).
- Demo site: `_quarto.yml`, `index.qmd`, `css_styling.qmd`, `animations.qmd`,
  `target.qmd`, `custom.scss`, rendered to the committed `docs/` directory.

## Known issues

- With no `label`, the extension adds `aria-hidden="true"` even when the user
  passes `aria-label`, `aria-hidden`, or `role` directly. This breaks IP1
  (ROADMAP candidate).

- The repo has no automated checks. Nothing renders a fixture or tests the Lua,
  so a change is checked by eye in a browser (as in 09a2e5f).
- lordicon.com no longer gives out CDN codes in its export UI, so `li` works for
  codes users already have but new codes are hard to find (README).
- RStudio Viewer shows icons only from version 2022.12.0+353 (README).
