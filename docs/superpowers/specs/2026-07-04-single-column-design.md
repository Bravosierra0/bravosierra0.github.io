# Single-column design PoC

_rev: 20260704_

## Problem

The homepage (`index.html`) uses a two-column desktop layout (`.page-body` grid: `1fr 300px` main + sidebar) that only collapses to one column below 640px by naively stacking the sidebar under main — no redesign, just a breakpoint override. The detail pages (`isseeyou.html`, `rakrak.html`, `oh-shift.html`) are already single-column but flat: every section shares the same width and left alignment, with no visual variety.

Reference: [Single Column Web Design](https://anthonyhobday.com/books/singlecolumndesign/) (Anthony Hobday). Core principles applied here:

- Vary horizontal alignment/width per section instead of one uniform column — the main antidote to single-column monotony.
- Use background layering (color blocks) for depth.
- Use scale contrast — deliberately enlarge a few elements.

## Goal

Redesign the homepage as single-column at **all** viewport widths (not just mobile), and apply the same visual-variety language to the detail pages, so both page types read as one coherent single-column system instead of "desktop grid that happens to also work on phones."

## Scope

- `index.html` — remove the two-column grid, fold sidebar content into the single column.
- `isseeyou.html`, `rakrak.html`, `oh-shift.html` — apply the same visual-variety treatment (no structural sidebar to remove, since they're already single-column).
- Edits are made in place on the `single-column-design` branch (already checked out). No separate mockup files — `git diff`/`git checkout` against `main` is the before/after comparison mechanism.

## Design

### 1. Page shell (unchanged)

The outer 980px bordered container, colorbar, header, and nav are untouched on every page. Only content inside `.page-body` (homepage) and `.col-main` (detail pages) changes.

`.page-body`'s two-column grid and the `<aside class="col-side">` element are deleted from `index.html`. The homepage becomes one flowing column at all widths, not just below 640px.

### 2. Homepage section-by-section

| Section | Alignment/width | Purpose |
|---|---|---|
| Hero/About (`.lead-block`) | unchanged — left-aligned, accent border, full column width | baseline width; anchors the eye before variety starts |
| Apps table (`.app-table`) | unchanged — full column width | the "wide" element other sections contrast against |
| Principles (`.philosophy`) | **new**: centered, `max-width: ~560px`, `margin-inline: auto` | alternating-alignment break from the book's principle #2 |
| Meta band (replaces `.col-side` / `<aside>`) | **new**: full-bleed edge-to-edge section, `bg2` background, inset 3-up grid inside holding Stack / Source / App Store | layering (background) + scale contrast, placed after Principles and before the footer |
| Footer | unchanged | — |

The meta band's three former sidebar blocks (Stack, Source, App Store) keep their existing inner markup/classes (`kv-row`, `github-btn`) — only their outer wrapper and grid placement change.

### 3. Detail pages section-by-section

| Section | Change |
|---|---|
| Hero (`.detail-title`, `.detail-tagline`) | unchanged, left-aligned |
| `.spec-plate` | converted to the same full-bleed shaded band pattern as the homepage's meta band — visually ties detail pages back to the homepage |
| `.instrument-panel` readout values (`.readout-val`) | font-size increased to ~1.3rem and weight bumped to bold, for scale contrast (book principle #4) |
| Body text (`.detail-body`) | narrows to a centered `max-width: ~640px` reading column — contrasts against the full-width band above it |
| Revision history (`.revision-list`) + store button (`.store-btn`) | unchanged, left-aligned at normal column width |

### 4. Responsive mechanics

No new manual breakpoints are added for these changes:

- The full-bleed band uses the standard edge-to-edge break-out technique: `width: 100vw; margin-inline: calc(50% - 50vw)`. Works at any width without a media query.
- Its inner 3-up grid uses `grid-template-columns: repeat(auto-fit, minmax(200px, 1fr))`, which stacks naturally on narrow viewports.
- Centered narrow columns (Principles, detail body text) use `max-width` + `margin-inline: auto`, self-adjusting without a media query.
- The existing `@media (max-width: 640px) { .page-body { grid-template-columns: 1fr; } ... }` rule in `index.html` is deleted outright once `.page-body`'s grid and `.col-side` no longer exist — it becomes dead code, not something to repurpose.

### 5. Out of scope

- No changes to header, nav, footer, theme toggle, or back-to-top behavior.
- No changes to the 980px bordered page shell or colorbar.
- No new content — this reorganizes and restyles existing sections, it doesn't add copy, images, or features.

## Verification

No build step on this static site. Verification is manual, in a browser:

- Open `index.html` and `isseeyou.html` directly (file:// or local server).
- Toggle light/dark theme on each; confirm the meta band's `bg2` background and text contrast hold in both.
- Check three widths: ~375px, ~768px, ~1200px — confirm no horizontal scrollbar from the full-bleed band, and that the 3-up grid / centered columns reflow sensibly.
- Confirm internal links (Apps table rows → detail pages, breadcrumb back to `index.html#apps`) still work after markup changes.
