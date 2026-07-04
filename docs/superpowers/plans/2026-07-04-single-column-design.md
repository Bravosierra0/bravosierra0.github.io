# Single-Column Design Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the homepage's two-column desktop layout into a single column at all widths, and apply the same alignment/layering/scale-contrast visual language to the three app detail pages, per `docs/superpowers/specs/2026-07-04-single-column-design.md`.

**Architecture:** This is a static HTML/CSS site with no build step, no shared stylesheet (every page embeds its own `<style>` block), and no test framework. Each of the 4 HTML files is edited independently — there are no cross-file code dependencies. "Tests" in this plan are manual browser-verification checklists, not automated assertions, since there is no test runner in this repo.

**Tech Stack:** Plain HTML5 + CSS (custom properties for theming), no JS framework, no build tooling.

## Global Constraints

- No build step exists — verification is manual, in a browser, per the spec's Verification section.
- Header, nav, footer, theme toggle, back-to-top button, and the outer 980px bordered page shell are untouched (spec §5, Out of scope).
- No new manual breakpoints are added — full-bleed bands and narrow columns must self-adjust via `max-width`/`auto-fit`/`margin-inline: auto` (spec §4).
- Every full-bleed "band" element must be a **direct child of an element whose content-box already spans the page's full centered width** (`.page-body` on the homepage, `.col-main` on detail pages after this plan removes its `max-width`). This is required for the `calc(50% - 50vw)` edge-to-edge technique to land on the true viewport edge — nesting it inside a narrower, non-centered wrapper (e.g. the old `.col-main { max-width: 720px }`) would offset the band incorrectly. See Task 2 for the full derivation; Tasks 3–4 reuse the same pattern.
- Where an existing element carries accessibility semantics (`<aside aria-label="...">`), preserve the element type when restyling it — do not silently downgrade to a bare `<div>`.

## File Structure

| File | Role in this change |
|---|---|
| `index.html` | Homepage. Two-column grid + `<aside>` removed; sidebar content folds into a new full-bleed `.meta-band`; Principles section narrows and centers. |
| `isseeyou.html` | Detail page. `.spec-plate` converted to `.meta-band`; body text narrows; `.readout-val` enlarged for scale contrast. |
| `rakrak.html` | Same treatment as `isseeyou.html`, adapted to its own content. |
| `oh-shift.html` | Same treatment, but its signature element is `.week-grid`/`.day-mark` (not `.readout-val`) — scale contrast applies to `.day-mark`. |

No new files are created. No files are deleted.

---

### Task 1: Homepage single-column layout (`index.html`)

**Files:**
- Modify: `index.html`

**Interfaces:**
- Consumes: none (this file has no dependency on the other tasks)
- Produces: none (no other task reads from this file)

- [ ] **Step 1: Edit the CSS — remove the two-column grid, add band/narrow-section rules**

In the `<style>` block of `index.html`, make these five edits:

1. Replace:
```css
  /* ── layout ── */
  .page-body {
    display: grid;
    grid-template-columns: 1fr 300px;
    flex: 1;
  }

  .col-main {
    border-right: 1px solid var(--border);
    padding: 18px 18px 28px;
  }

  .col-side {
    padding: 18px 16px 28px;
  }
```
with:
```css
  /* ── layout ── */
  .page-body {
    flex: 1;
  }

  .col-main {
    padding: 18px 18px 28px;
  }
```

2. Replace:
```css
  /* ── philosophy ── */
  .philosophy {
    border: 1px solid var(--border);
    background: var(--bg2);
  }
```
with:
```css
  /* ── narrow section (alignment contrast) ── */
  .narrow-section {
    max-width: 560px;
    margin-inline: auto;
  }

  /* ── philosophy ── */
  .philosophy {
    border: 1px solid var(--border);
    background: var(--bg2);
  }
```

3. Replace:
```css
  /* ── sidebar ── */
  .sidebar-block { margin-bottom: 22px; }
```
with:
```css
  /* ── meta band (replaces the old sidebar column) ── */
  .meta-band {
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    background: var(--bg2);
    border-top: 1px solid var(--border);
  }

  .meta-band-inner {
    max-width: 980px;
    margin-inline: auto;
    padding: 22px 18px 28px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 24px;
  }

  /* ── sidebar ── */
  .sidebar-block { margin-bottom: 0; }
```

4. Replace:
```css
  /* ── responsive ── */
  @media (max-width: 640px) {
    .page-body { grid-template-columns: 1fr; }
    .col-main { border-right: none; border-bottom: 1px solid var(--border); }
    .app-table th:nth-child(4),
    .app-table td:nth-child(4) { display: none; }
    .footer-left { font-size: 0.7rem; }
  }
```
with:
```css
  /* ── responsive ── */
  @media (max-width: 640px) {
    .app-table th:nth-child(4),
    .app-table td:nth-child(4) { display: none; }
    .footer-left { font-size: 0.7rem; }
  }
```

- [ ] **Step 2: Edit the HTML — wrap Principles, replace the sidebar `<aside>` with `.meta-band`**

Replace:
```html
    <hr class="sep">

    <h2 class="section-head">Principles</h2>
    <div class="dot-rule"></div>

    <ul class="philosophy">
      <li>Small tools outlast ambitious ones.</li>
      <li>No cloud. No account. No excuse.</li>
      <li>Platform conventions exist for a reason. Follow them.</li>
      <li>Boring is reliable.</li>
    </ul>

  </main>

  <aside class="col-side" aria-label="Details">

    <div class="sidebar-block">
      <h2 class="section-head">Stack</h2>
      <div class="dot-rule"></div>
      <div class="kv-row"><span class="kv-key">Language</span><span class="kv-val">Swift</span></div>
      <div class="kv-row"><span class="kv-key">UI</span><span class="kv-val">SwiftUI</span></div>
      <div class="kv-row"><span class="kv-key">IDE</span><span class="kv-val">Xcode</span></div>
      <div class="kv-row"><span class="kv-key">Distribution</span><span class="kv-val">App Store · Direct</span></div>
    </div>

    <div class="sidebar-block">
      <h2 class="section-head">Source</h2>
      <div class="dot-rule"></div>
      <p style="font-family:var(--sans); font-size:0.875rem; color:var(--muted); margin-bottom:4px;">Public repositories and activity.</p>
      <a href="https://github.com/Bravosierra0" class="github-btn" target="_blank" rel="noopener" aria-label="GitHub profile for Bravosierra0">github.com/Bravosierra0 ↗</a>
    </div>

    <div class="sidebar-block">
      <h2 class="section-head">App Store</h2>
      <div class="dot-rule"></div>
      <div class="kv-row"><span class="kv-key">ISSeeYou</span><span class="kv-val"><a href="#" aria-label="ISSeeYou on App Store">↗</a></span></div>
      <div class="kv-row"><span class="kv-key">RakRak</span><span class="kv-val" style="color:var(--muted)">TestFlight</span></div>
      <div class="kv-row"><span class="kv-key">Oh Shift!</span><span class="kv-val" style="color:var(--muted)">TestFlight</span></div>
    </div>

  </aside>

</div>
```
with:
```html
    <hr class="sep">

    <div class="narrow-section">
      <h2 class="section-head">Principles</h2>
      <div class="dot-rule"></div>

      <ul class="philosophy">
        <li>Small tools outlast ambitious ones.</li>
        <li>No cloud. No account. No excuse.</li>
        <li>Platform conventions exist for a reason. Follow them.</li>
        <li>Boring is reliable.</li>
      </ul>
    </div>

  </main>

  <aside class="meta-band" aria-label="Details">
    <div class="meta-band-inner">

      <div class="sidebar-block">
        <h2 class="section-head">Stack</h2>
        <div class="dot-rule"></div>
        <div class="kv-row"><span class="kv-key">Language</span><span class="kv-val">Swift</span></div>
        <div class="kv-row"><span class="kv-key">UI</span><span class="kv-val">SwiftUI</span></div>
        <div class="kv-row"><span class="kv-key">IDE</span><span class="kv-val">Xcode</span></div>
        <div class="kv-row"><span class="kv-key">Distribution</span><span class="kv-val">App Store · Direct</span></div>
      </div>

      <div class="sidebar-block">
        <h2 class="section-head">Source</h2>
        <div class="dot-rule"></div>
        <p style="font-family:var(--sans); font-size:0.875rem; color:var(--muted); margin-bottom:4px;">Public repositories and activity.</p>
        <a href="https://github.com/Bravosierra0" class="github-btn" target="_blank" rel="noopener" aria-label="GitHub profile for Bravosierra0">github.com/Bravosierra0 ↗</a>
      </div>

      <div class="sidebar-block">
        <h2 class="section-head">App Store</h2>
        <div class="dot-rule"></div>
        <div class="kv-row"><span class="kv-key">ISSeeYou</span><span class="kv-val"><a href="#" aria-label="ISSeeYou on App Store">↗</a></span></div>
        <div class="kv-row"><span class="kv-key">RakRak</span><span class="kv-val" style="color:var(--muted)">TestFlight</span></div>
        <div class="kv-row"><span class="kv-key">Oh Shift!</span><span class="kv-val" style="color:var(--muted)">TestFlight</span></div>
      </div>

    </div>
  </aside>

</div>
```

- [ ] **Step 3: Manual verification**

Run: `python3 -m http.server 8000` from the repo root, then open `http://localhost:8000/index.html`.

Check:
- No two-column grid remains — Stack/Source/App Store now render as a shaded full-width band below Principles, above the footer.
- The band's background extends edge-to-edge to the browser window (no gap, no horizontal scrollbar).
- Principles list is centered and narrower than the Apps table above it.
- Toggle the theme button — band background/text contrast holds in both light and dark mode.
- Resize to ~375px, ~768px, ~1200px — the 3-up band grid stacks to 1 column on narrow widths without any layout break; Apps table's 4th column still hides below 640px as before.
- Click the Apps table links — they still navigate to the detail pages.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Fold homepage sidebar into a single-column layout with a full-bleed meta band"
```

---

### Task 2: ISSeeYou detail page (`isseeyou.html`)

**Files:**
- Modify: `isseeyou.html`

**Interfaces:**
- Consumes: none
- Produces: none

- [ ] **Step 1: Edit the CSS**

1. Replace:
```css
  /* ── layout ── */
  .col-main {
    padding: 18px 18px 28px;
    max-width: 720px;
  }
```
with:
```css
  /* ── layout ── */
  .col-main {
    padding: 18px 18px 28px;
  }

  .detail-column {
    max-width: 720px;
  }

  .detail-narrow {
    max-width: 640px;
    margin-inline: auto;
  }
```

2. Replace:
```css
  /* ── spec plate ── */
  .spec-plate {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border: 1px solid var(--border);
    background: var(--bg2);
    margin-bottom: 20px;
  }

  .spec-cell {
    padding: 10px 14px;
    border-right: 1px dotted var(--border-d);
  }

  .spec-cell:last-child { border-right: none; }
```
with:
```css
  /* ── spec plate ── */
  .spec-plate {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 8px 24px;
  }

  .spec-cell {
    padding: 10px 0;
  }

  /* ── meta band (full-bleed wrapper for spec-plate) ── */
  .meta-band {
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    background: var(--bg2);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
  }

  .meta-band-inner {
    max-width: 980px;
    margin-inline: auto;
    padding: 16px 18px;
  }
```

3. Replace:
```css
  .readout-val {
    font-weight: 700;
    font-size: 0.95rem;
  }
```
with:
```css
  .readout-val {
    font-weight: 700;
    font-size: 1.3rem;
  }
```

4. Replace:
```css
  @media (max-width: 640px) {
    .spec-plate { grid-template-columns: 1fr; }
    .spec-cell { border-right: none; border-bottom: 1px dotted var(--border-d); }
    .spec-cell:last-child { border-bottom: none; }
    .readout-grid { grid-template-columns: 1fr; }
    .footer-left { font-size: 0.7rem; }
  }
```
with:
```css
  @media (max-width: 640px) {
    .readout-grid { grid-template-columns: 1fr; }
    .footer-left { font-size: 0.7rem; }
  }
```

- [ ] **Step 2: Edit the HTML**

Replace:
```html
<main class="col-main" id="main">

  <p class="breadcrumb"><a href="index.html#apps">← Apps</a></p>

  <h1 class="detail-title">ISSeeYou <span class="status-live">Live</span></h1>
  <p class="detail-tagline">Real-time ISS tracker. Know when and where to look up.</p>

  <div class="spec-plate">
    <div class="spec-cell">
      <div class="spec-key">Platforms</div>
      <div class="spec-val">macOS, iOS, iPadOS, tvOS</div>
    </div>
    <div class="spec-cell">
      <div class="spec-key">Category</div>
      <div class="spec-val">Utility</div>
    </div>
    <div class="spec-cell">
      <div class="spec-key">Distribution</div>
      <div class="spec-val">App Store</div>
    </div>
  </div>

  <div class="instrument-panel" aria-hidden="true">
    <div class="instrument-label">Sample readout</div>
    <div class="readout-grid">
      <div class="readout-row">
        <span class="readout-key">Altitude</span>
        <span class="readout-val">408 km</span>
      </div>
      <div class="readout-row">
        <span class="readout-key">Next pass</span>
        <span class="readout-val">00:04:12</span>
      </div>
      <div class="readout-row">
        <span class="readout-key">Velocity</span>
        <span class="readout-val">7.66 km/s</span>
      </div>
      <div class="readout-row">
        <span class="readout-key">Elevation</span>
        <span class="readout-val">62°</span>
      </div>
    </div>
  </div>
  <p class="instrument-note">Illustrative figures — not a live feed of this page. The app itself pulls current ISS position and pass predictions on device.</p>

  <hr class="sep">

  <p class="detail-body">ISSeeYou tells you when the International Space Station is overhead and worth stepping outside for. It tracks the station's current position and works out your next visible pass, so you get a heads-up instead of having to check a website.</p>
  <p class="detail-body">No account, no cloud sync, no ads. It runs the same whether you're on your Mac, phone, tablet, or TV.</p>

  <hr class="sep">

  <h2 class="section-head">Revision history</h2>
  <div class="dot-rule"></div>
  <ul class="revision-list">
    <li><span class="rev-num">1.2.0</span><span class="rev-note">Added tvOS pass predictions</span></li>
    <li><span class="rev-num">1.1.0</span><span class="rev-note">iPad multitasking support</span></li>
    <li><span class="rev-num">1.0.0</span><span class="rev-note">Initial release</span></li>
  </ul>

  <a href="#" class="store-btn" aria-label="ISSeeYou on the App Store">View on the App Store →</a>

</main>
```
with:
```html
<main class="col-main" id="main">

  <div class="detail-column">
    <p class="breadcrumb"><a href="index.html#apps">← Apps</a></p>

    <h1 class="detail-title">ISSeeYou <span class="status-live">Live</span></h1>
    <p class="detail-tagline">Real-time ISS tracker. Know when and where to look up.</p>
  </div>

  <aside class="meta-band" aria-label="Specifications">
    <div class="meta-band-inner">
      <div class="spec-plate">
        <div class="spec-cell">
          <div class="spec-key">Platforms</div>
          <div class="spec-val">macOS, iOS, iPadOS, tvOS</div>
        </div>
        <div class="spec-cell">
          <div class="spec-key">Category</div>
          <div class="spec-val">Utility</div>
        </div>
        <div class="spec-cell">
          <div class="spec-key">Distribution</div>
          <div class="spec-val">App Store</div>
        </div>
      </div>
    </div>
  </aside>

  <div class="detail-column">
    <div class="instrument-panel" aria-hidden="true">
      <div class="instrument-label">Sample readout</div>
      <div class="readout-grid">
        <div class="readout-row">
          <span class="readout-key">Altitude</span>
          <span class="readout-val">408 km</span>
        </div>
        <div class="readout-row">
          <span class="readout-key">Next pass</span>
          <span class="readout-val">00:04:12</span>
        </div>
        <div class="readout-row">
          <span class="readout-key">Velocity</span>
          <span class="readout-val">7.66 km/s</span>
        </div>
        <div class="readout-row">
          <span class="readout-key">Elevation</span>
          <span class="readout-val">62°</span>
        </div>
      </div>
    </div>
    <p class="instrument-note">Illustrative figures — not a live feed of this page. The app itself pulls current ISS position and pass predictions on device.</p>

    <hr class="sep">

    <div class="detail-narrow">
      <p class="detail-body">ISSeeYou tells you when the International Space Station is overhead and worth stepping outside for. It tracks the station's current position and works out your next visible pass, so you get a heads-up instead of having to check a website.</p>
      <p class="detail-body">No account, no cloud sync, no ads. It runs the same whether you're on your Mac, phone, tablet, or TV.</p>
    </div>

    <hr class="sep">

    <h2 class="section-head">Revision history</h2>
    <div class="dot-rule"></div>
    <ul class="revision-list">
      <li><span class="rev-num">1.2.0</span><span class="rev-note">Added tvOS pass predictions</span></li>
      <li><span class="rev-num">1.1.0</span><span class="rev-note">iPad multitasking support</span></li>
      <li><span class="rev-num">1.0.0</span><span class="rev-note">Initial release</span></li>
    </ul>

    <a href="#" class="store-btn" aria-label="ISSeeYou on the App Store">View on the App Store →</a>
  </div>

</main>
```

- [ ] **Step 3: Manual verification**

Run: `python3 -m http.server 8000` (if not already running), open `http://localhost:8000/isseeyou.html`.

Check:
- Hero (breadcrumb/title/tagline) still left-aligned at its original width.
- Spec plate now renders as a shaded full-bleed band, edge-to-edge to the browser window, no horizontal scrollbar.
- Readout values (`408 km`, `00:04:12`, etc.) are visibly larger/bolder than the labels next to them.
- The two `.detail-body` paragraphs form a centered, narrower block than the hero/instrument-panel above.
- Toggle theme — band contrast holds in both modes.
- Resize to ~375px, ~768px, ~1200px — band and spec cells reflow without breaking; revision history and store button remain left-aligned at the bottom.
- Breadcrumb link back to `index.html#apps` still works.

- [ ] **Step 4: Commit**

```bash
git add isseeyou.html
git commit -m "Apply single-column visual variety to the ISSeeYou detail page"
```

---

### Task 3: RakRak detail page (`rakrak.html`)

**Files:**
- Modify: `rakrak.html`

**Interfaces:**
- Consumes: none
- Produces: none

- [ ] **Step 1: Edit the CSS**

1. Replace:
```css
  /* ── layout ── */
  .col-main {
    padding: 18px 18px 28px;
    max-width: 720px;
  }
```
with:
```css
  /* ── layout ── */
  .col-main {
    padding: 18px 18px 28px;
  }

  .detail-column {
    max-width: 720px;
  }

  .detail-narrow {
    max-width: 640px;
    margin-inline: auto;
  }
```

2. Replace:
```css
  /* ── spec plate ── */
  .spec-plate {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border: 1px solid var(--border);
    background: var(--bg2);
    margin-bottom: 20px;
  }

  .spec-cell {
    padding: 10px 14px;
    border-right: 1px dotted var(--border-d);
  }

  .spec-cell:last-child { border-right: none; }
```
with:
```css
  /* ── spec plate ── */
  .spec-plate {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 8px 24px;
  }

  .spec-cell {
    padding: 10px 0;
  }

  /* ── meta band (full-bleed wrapper for spec-plate) ── */
  .meta-band {
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    background: var(--bg2);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
  }

  .meta-band-inner {
    max-width: 980px;
    margin-inline: auto;
    padding: 16px 18px;
  }
```

3. Replace:
```css
  .readout-val {
    font-weight: 700;
    font-size: 0.95rem;
  }
```
with:
```css
  .readout-val {
    font-weight: 700;
    font-size: 1.3rem;
  }
```

4. Replace:
```css
  @media (max-width: 640px) {
    .spec-plate { grid-template-columns: 1fr; }
    .spec-cell { border-right: none; border-bottom: 1px dotted var(--border-d); }
    .spec-cell:last-child { border-bottom: none; }
    .readout-grid { grid-template-columns: 1fr; }
    .readout-row:nth-last-child(-n+2) { border-bottom: 1px dotted var(--border-d); }
    .readout-row:last-child { border-bottom: none; }
    .footer-left { font-size: 0.7rem; }
  }
```
with:
```css
  @media (max-width: 640px) {
    .readout-grid { grid-template-columns: 1fr; }
    .readout-row:nth-last-child(-n+2) { border-bottom: 1px dotted var(--border-d); }
    .readout-row:last-child { border-bottom: none; }
    .footer-left { font-size: 0.7rem; }
  }
```

- [ ] **Step 2: Edit the HTML**

Replace:
```html
<main class="col-main" id="main">

  <p class="breadcrumb"><a href="index.html#apps">← Apps</a></p>

  <h1 class="detail-title">RakRak <span class="status-testflight">TestFlight</span></h1>
  <p class="detail-tagline">Relationship date tracker. Keep track of moments that matter.</p>

  <div class="spec-plate">
    <div class="spec-cell">
      <div class="spec-key">Platforms</div>
      <div class="spec-val">iOS, iPadOS</div>
    </div>
    <div class="spec-cell">
      <div class="spec-key">Category</div>
      <div class="spec-val">Personal</div>
    </div>
    <div class="spec-cell">
      <div class="spec-key">Distribution</div>
      <div class="spec-val">TestFlight</div>
    </div>
  </div>

  <div class="instrument-panel" aria-hidden="true">
    <div class="instrument-label">Sample tally</div>
    <div class="readout-grid">
      <div class="readout-row">
        <span class="readout-key">Days together</span>
        <span class="readout-val">1,842</span>
      </div>
      <div class="readout-row">
        <span class="readout-key">Next anniversary</span>
        <span class="readout-val">in 23 days</span>
      </div>
      <div class="readout-row">
        <span class="readout-key">Moments logged</span>
        <span class="readout-val">96</span>
      </div>
      <div class="readout-row">
        <span class="readout-key">Last entry</span>
        <span class="readout-val">4 days ago</span>
      </div>
    </div>
  </div>
  <p class="instrument-note">Illustrative figures — your own dates and entries populate this on device.</p>

  <hr class="sep">

  <p class="detail-body">RakRak keeps the dates that actually matter to you in one place — anniversaries, first meetings, small moments worth remembering — and counts down or up so you're never caught off guard.</p>
  <p class="detail-body">No account, no cloud sync, no ads. Everything stays on your device.</p>

  <hr class="sep">

  <h2 class="section-head">Revision history</h2>
  <div class="dot-rule"></div>
  <ul class="revision-list">
    <li><span class="rev-num">0.4.0</span><span class="rev-note">Home Screen widget added</span></li>
    <li><span class="rev-num">0.3.0</span><span class="rev-note">iPad layout refined</span></li>
    <li><span class="rev-num">0.2.0</span><span class="rev-note">Initial TestFlight build</span></li>
  </ul>

  <a href="#" class="store-btn" aria-label="Join the RakRak TestFlight beta">Join the TestFlight beta →</a>

</main>
```
with:
```html
<main class="col-main" id="main">

  <div class="detail-column">
    <p class="breadcrumb"><a href="index.html#apps">← Apps</a></p>

    <h1 class="detail-title">RakRak <span class="status-testflight">TestFlight</span></h1>
    <p class="detail-tagline">Relationship date tracker. Keep track of moments that matter.</p>
  </div>

  <aside class="meta-band" aria-label="Specifications">
    <div class="meta-band-inner">
      <div class="spec-plate">
        <div class="spec-cell">
          <div class="spec-key">Platforms</div>
          <div class="spec-val">iOS, iPadOS</div>
        </div>
        <div class="spec-cell">
          <div class="spec-key">Category</div>
          <div class="spec-val">Personal</div>
        </div>
        <div class="spec-cell">
          <div class="spec-key">Distribution</div>
          <div class="spec-val">TestFlight</div>
        </div>
      </div>
    </div>
  </aside>

  <div class="detail-column">
    <div class="instrument-panel" aria-hidden="true">
      <div class="instrument-label">Sample tally</div>
      <div class="readout-grid">
        <div class="readout-row">
          <span class="readout-key">Days together</span>
          <span class="readout-val">1,842</span>
        </div>
        <div class="readout-row">
          <span class="readout-key">Next anniversary</span>
          <span class="readout-val">in 23 days</span>
        </div>
        <div class="readout-row">
          <span class="readout-key">Moments logged</span>
          <span class="readout-val">96</span>
        </div>
        <div class="readout-row">
          <span class="readout-key">Last entry</span>
          <span class="readout-val">4 days ago</span>
        </div>
      </div>
    </div>
    <p class="instrument-note">Illustrative figures — your own dates and entries populate this on device.</p>

    <hr class="sep">

    <div class="detail-narrow">
      <p class="detail-body">RakRak keeps the dates that actually matter to you in one place — anniversaries, first meetings, small moments worth remembering — and counts down or up so you're never caught off guard.</p>
      <p class="detail-body">No account, no cloud sync, no ads. Everything stays on your device.</p>
    </div>

    <hr class="sep">

    <h2 class="section-head">Revision history</h2>
    <div class="dot-rule"></div>
    <ul class="revision-list">
      <li><span class="rev-num">0.4.0</span><span class="rev-note">Home Screen widget added</span></li>
      <li><span class="rev-num">0.3.0</span><span class="rev-note">iPad layout refined</span></li>
      <li><span class="rev-num">0.2.0</span><span class="rev-note">Initial TestFlight build</span></li>
    </ul>

    <a href="#" class="store-btn" aria-label="Join the RakRak TestFlight beta">Join the TestFlight beta →</a>
  </div>

</main>
```

- [ ] **Step 3: Manual verification**

Same checklist as Task 2, run against `http://localhost:8000/rakrak.html`. Additionally confirm the `readout-row:nth-last-child(-n+2)` border rule (2-row-grid bottom border removal) still renders correctly at narrow widths — this rule was left untouched by this task.

- [ ] **Step 4: Commit**

```bash
git add rakrak.html
git commit -m "Apply single-column visual variety to the RakRak detail page"
```

---

### Task 4: Oh Shift! detail page (`oh-shift.html`)

**Files:**
- Modify: `oh-shift.html`

**Interfaces:**
- Consumes: none
- Produces: none

**Note:** This page's signature element is `.week-grid`/`.week-cell`/`.day-mark`, not `.readout-val` — there is no `.instrument-label` pulse/readout markup here to confuse with the other two pages. Scale contrast (book principle #4) applies to `.day-mark` instead.

- [ ] **Step 1: Edit the CSS**

1. Replace:
```css
  /* ── layout ── */
  .col-main {
    padding: 18px 18px 28px;
    max-width: 720px;
  }
```
with:
```css
  /* ── layout ── */
  .col-main {
    padding: 18px 18px 28px;
  }

  .detail-column {
    max-width: 720px;
  }

  .detail-narrow {
    max-width: 640px;
    margin-inline: auto;
  }
```

2. Replace:
```css
  /* ── spec plate ── */
  .spec-plate {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border: 1px solid var(--border);
    background: var(--bg2);
    margin-bottom: 20px;
  }

  .spec-cell {
    padding: 10px 14px;
    border-right: 1px dotted var(--border-d);
  }

  .spec-cell:last-child { border-right: none; }
```
with:
```css
  /* ── spec plate ── */
  .spec-plate {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 8px 24px;
  }

  .spec-cell {
    padding: 10px 0;
  }

  /* ── meta band (full-bleed wrapper for spec-plate) ── */
  .meta-band {
    width: 100vw;
    margin-left: calc(50% - 50vw);
    margin-right: calc(50% - 50vw);
    background: var(--bg2);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
  }

  .meta-band-inner {
    max-width: 980px;
    margin-inline: auto;
    padding: 16px 18px;
  }
```

3. Replace:
```css
  .week-cell .day-mark {
    font-size: 0.8rem;
    font-weight: 700;
  }
```
with:
```css
  .week-cell .day-mark {
    font-size: 1.1rem;
    font-weight: 700;
  }
```

4. Replace:
```css
  @media (max-width: 640px) {
    .spec-plate { grid-template-columns: 1fr; }
    .spec-cell { border-right: none; border-bottom: 1px dotted var(--border-d); }
    .spec-cell:last-child { border-bottom: none; }
    .week-grid { grid-template-columns: repeat(7, 1fr); gap: 4px; }
    .week-cell .day-label { font-size: 0.55rem; }
    .footer-left { font-size: 0.7rem; }
  }
```
with:
```css
  @media (max-width: 640px) {
    .week-grid { grid-template-columns: repeat(7, 1fr); gap: 4px; }
    .week-cell .day-label { font-size: 0.55rem; }
    .footer-left { font-size: 0.7rem; }
  }
```

- [ ] **Step 2: Edit the HTML**

Replace:
```html
<main class="col-main" id="main">

  <p class="breadcrumb"><a href="index.html#apps">← Apps</a></p>

  <h1 class="detail-title">Oh Shift! <span class="status-testflight">TestFlight</span></h1>
  <p class="detail-tagline">Simple roster-calendar wrapper for general purpose shift planning.</p>

  <div class="spec-plate">
    <div class="spec-cell">
      <div class="spec-key">Platforms</div>
      <div class="spec-val">macOS, iOS, iPadOS</div>
    </div>
    <div class="spec-cell">
      <div class="spec-key">Category</div>
      <div class="spec-val">Productivity</div>
    </div>
    <div class="spec-cell">
      <div class="spec-key">Distribution</div>
      <div class="spec-val">TestFlight</div>
    </div>
  </div>

  <div class="instrument-panel" aria-hidden="true">
    <div class="instrument-label">Sample roster</div>
    <div class="week-grid">
      <div class="week-cell filled"><span class="day-label">Mon</span><span class="day-mark">●</span></div>
      <div class="week-cell filled"><span class="day-label">Tue</span><span class="day-mark">●</span></div>
      <div class="week-cell"><span class="day-label">Wed</span><span class="day-mark">—</span></div>
      <div class="week-cell filled"><span class="day-label">Thu</span><span class="day-mark">●</span></div>
      <div class="week-cell filled"><span class="day-label">Fri</span><span class="day-mark">●</span></div>
      <div class="week-cell"><span class="day-label">Sat</span><span class="day-mark">—</span></div>
      <div class="week-cell"><span class="day-label">Sun</span><span class="day-mark">—</span></div>
    </div>
  </div>
  <p class="instrument-note">Illustrative week — your own roster and shift pattern populate this on device.</p>

  <hr class="sep">

  <p class="detail-body">Oh Shift! wraps your work roster in a plain calendar view, so shifts show up alongside everything else you've got on. No separate app to check, no manual copying dates across.</p>
  <p class="detail-body">No account, no cloud sync, no ads. Your roster stays on your device.</p>

  <hr class="sep">

  <h2 class="section-head">Revision history</h2>
  <div class="dot-rule"></div>
  <ul class="revision-list">
    <li><span class="rev-num">0.3.0</span><span class="rev-note">Recurring shift patterns added</span></li>
    <li><span class="rev-num">0.2.0</span><span class="rev-note">macOS build added</span></li>
    <li><span class="rev-num">0.1.0</span><span class="rev-note">Initial TestFlight build</span></li>
  </ul>

  <a href="#" class="store-btn" aria-label="Join the Oh Shift! TestFlight beta">Join the TestFlight beta →</a>

</main>
```
with:
```html
<main class="col-main" id="main">

  <div class="detail-column">
    <p class="breadcrumb"><a href="index.html#apps">← Apps</a></p>

    <h1 class="detail-title">Oh Shift! <span class="status-testflight">TestFlight</span></h1>
    <p class="detail-tagline">Simple roster-calendar wrapper for general purpose shift planning.</p>
  </div>

  <aside class="meta-band" aria-label="Specifications">
    <div class="meta-band-inner">
      <div class="spec-plate">
        <div class="spec-cell">
          <div class="spec-key">Platforms</div>
          <div class="spec-val">macOS, iOS, iPadOS</div>
        </div>
        <div class="spec-cell">
          <div class="spec-key">Category</div>
          <div class="spec-val">Productivity</div>
        </div>
        <div class="spec-cell">
          <div class="spec-key">Distribution</div>
          <div class="spec-val">TestFlight</div>
        </div>
      </div>
    </div>
  </aside>

  <div class="detail-column">
    <div class="instrument-panel" aria-hidden="true">
      <div class="instrument-label">Sample roster</div>
      <div class="week-grid">
        <div class="week-cell filled"><span class="day-label">Mon</span><span class="day-mark">●</span></div>
        <div class="week-cell filled"><span class="day-label">Tue</span><span class="day-mark">●</span></div>
        <div class="week-cell"><span class="day-label">Wed</span><span class="day-mark">—</span></div>
        <div class="week-cell filled"><span class="day-label">Thu</span><span class="day-mark">●</span></div>
        <div class="week-cell filled"><span class="day-label">Fri</span><span class="day-mark">●</span></div>
        <div class="week-cell"><span class="day-label">Sat</span><span class="day-mark">—</span></div>
        <div class="week-cell"><span class="day-label">Sun</span><span class="day-mark">—</span></div>
      </div>
    </div>
    <p class="instrument-note">Illustrative week — your own roster and shift pattern populate this on device.</p>

    <hr class="sep">

    <div class="detail-narrow">
      <p class="detail-body">Oh Shift! wraps your work roster in a plain calendar view, so shifts show up alongside everything else you've got on. No separate app to check, no manual copying dates across.</p>
      <p class="detail-body">No account, no cloud sync, no ads. Your roster stays on your device.</p>
    </div>

    <hr class="sep">

    <h2 class="section-head">Revision history</h2>
    <div class="dot-rule"></div>
    <ul class="revision-list">
      <li><span class="rev-num">0.3.0</span><span class="rev-note">Recurring shift patterns added</span></li>
      <li><span class="rev-num">0.2.0</span><span class="rev-note">macOS build added</span></li>
      <li><span class="rev-num">0.1.0</span><span class="rev-note">Initial TestFlight build</span></li>
    </ul>

    <a href="#" class="store-btn" aria-label="Join the Oh Shift! TestFlight beta">Join the TestFlight beta →</a>
  </div>

</main>
```

- [ ] **Step 3: Manual verification**

Same checklist as Task 2, run against `http://localhost:8000/oh-shift.html`. Additionally confirm the week-grid's 7 day cells still render in one row at desktop widths and that filled/unfilled cell coloring (`.week-cell.filled`) is unaffected by the `.day-mark` size bump.

- [ ] **Step 4: Commit**

```bash
git add oh-shift.html
git commit -m "Apply single-column visual variety to the Oh Shift! detail page"
```

---

## Final check (after all 4 tasks)

- [ ] Open all four pages once more and click through every internal link (homepage → each detail page → breadcrumb back to homepage) to confirm nothing broke across the set.
- [ ] Confirm `git log --oneline -5` on `single-column-design` shows 4 new commits (one per file) plus the earlier spec commit.
