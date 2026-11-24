b347.dev

## Files

| File | Loaded by | Content |
|------|-----------|---------|
| `site.css` | every page except `404.html` and `blank/` | fonts, colors, header, nav, footer, shared components |
| `home.css` | `index.html` | home layout, lead block, app table, principles, sidebar |
| `app.css` | app pages such as `rakrak.html` | spec plate, revision list, TestFlight slot, support links, and at the end one section per app for its signature element |
| `legal.css` | `<app>/privacy.html`, `<app>/support.html` | layout, section heads, questions |
| `site.js` | `index.html` and the app pages | back-to-top button, TestFlight slot behaviour |
| `_templates/` | nobody | starting points for new pages. Jekyll does not publish folders that start with `_` |

- Each page links `site.css` first, then its page-type sheet. Pages carry no inline `<style>` and no inline `<script>`.
- Exception: `404.html` and `blank/index.html` keep their own inline CSS. GitHub Pages serves `404.html` at any missing path, so a relative stylesheet link would break there.
- `site.css` loads the fonts with paths relative to itself. Pages in subfolders link it as `../site.css`.
- A signature element that only one app uses gets its own section at the end of `app.css`. If its rules could hit other app pages, scope them with a modifier class, for example `.instrument-panel.live` on ISSeeYou.

## Add an app

1. Copy the templates:
   - `_templates/app.html` → `<app>.html` at the root
   - `_templates/privacy.html` → `<app>/privacy.html`
   - `_templates/support.html` → `<app>/support.html`
2. Replace every `{{PLACEHOLDER}}` in the three files. Find leftovers with `grep -rn '{{' <app>.html <app>/`.
3. Put the app icon in `<app>/images/icon.png`, 256 px. Export it from Icon Composer at 1024 px, then run `sips -Z 256`. The app page shows it at 64 px, the app table in `index.html` at 24 px.
4. Optional: screenshots go in `<app>/images/`. The app page links them as `<app>/images/<file>.png`.
5. In `index.html`, add the app table row and the App Store line. Both snippets are in `_templates/index-snippets.html`.

The App Store Connect URLs are `https://b347.dev/<app>/privacy.html` and `https://b347.dev/<app>/support.html`.

## Change shared text

The header, nav, footer and `<head>` block are copied into every page. A change there means editing all pages:

```zsh
grep -rl 'Computer-System-Engineering' --include='*.html' .
```

### Site revision

`REV` in the footer is the site revision. All pages carry the same date. Update it on every page when you publish a change:

```zsh
sed -i '' -E 's/(footer-rev">)[0-9.]+/\12026.12.01/' $(grep -rl 'footer-rev' --include='*.html' .)
```

## Maintenance

### TestFlight beta status

`rakrak.html` and `oh-shift.html` each wrap their TestFlight join button in:

```html
<div class="tf-slot" data-tf-state="open">
```

Flip `data-tf-state` between `open` and `closed` when a beta opens or fills up:
- CSS swaps the label above the button ("Open for testers" / "Beta closed") and greys the button out.
- `site.js` removes the link's `href` and marks it `aria-disabled` when closed, so it's actually non-interactive, not just faded.

No other edit is needed. One attribute drives both the look and the behavior.
