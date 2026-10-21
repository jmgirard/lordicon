# Design

_Seeded by cairn-init on 2026-10-20 and filled by `/design-interview` the same
day. The maintainer confirmed Purpose & Scope, the contract boundary, and the
conventions below._

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
  It rises in each merge that ships a user-visible change.
- The repo keeps no changelog file yet. The maintainer chose to start
  `CHANGELOG.md` (ROADMAP candidate).

## Design Principles

_Not yet formalized. Inviolable principles (IP<n>, hard constraints) come first,
then Guiding principles (GP<n>, tradeable with justification). Numbers are never
reused._

### Banked candidates (interview in progress)

Banked during the facts phase on 2026-10-20, for the principles phase:

- Forward attributes, do not curate them (contract boundary answer).
- Guardrails only where an icon fails with no visible error.
- Self-hosted player: no runtime script from a third-party host.
- Stable shortcode surface; deprecate with a warning before a break.
- New arguments only for behavior passthrough cannot give.
- The demo site ships with each user-facing feature.
- Plain, actionable warnings for authors who are not web developers.

Choices to record at write-out: the version rises at each shipping merge
(D-entry and the PROFILE `release-walk` slot); start `CHANGELOG.md` (PROFILE
`changelog` slot and a candidate row); the PROFILE `verify` slot is a render of
the demo site, because the repo has no automated checks.

## Architecture

- `_extensions/lordicon/lordicon.lua`: the shortcode filter. It adds the bundle
  as an HTML dependency and returns a raw `<lord-icon>` element.
- `_extensions/lordicon/assets/js/bundle.js`: the committed webpack build of
  `src/main.js`, which calls `defineElement()` from `@lordicon/element` v2.
  `npm run build` rebuilds it (`webpack.config.js`).
- Demo site: `_quarto.yml`, `index.qmd`, `css_styling.qmd`, `animations.qmd`,
  `target.qmd`, `custom.scss`, rendered to the committed `docs/` directory.

## Known issues

- The repo has no automated checks. Nothing renders a fixture or tests the Lua,
  so a change is checked by eye in a browser (as in 09a2e5f).
- lordicon.com no longer gives out CDN codes in its export UI, so `li` works for
  codes users already have but new codes are hard to find (README).
- RStudio Viewer shows icons only from version 2022.12.0+353 (README).
