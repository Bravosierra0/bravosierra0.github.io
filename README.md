b347.dev

## Stylesheets

| File | Loaded by | Content |
|------|-----------|---------|
| `site.css` | every page except `404.html` and `blank/` | fonts, colors, header, nav, footer, shared components |
| `app.css` | app pages such as `rakrak.html` | spec plate, revision list, TestFlight slot, support links |
| `legal.css` | `<app>/privacy.html`, `<app>/support.html` | layout, section heads, questions |

- Each page links `site.css` first, then its page-type sheet, then its own inline `<style>`. Inline rules win.
- An app page keeps only its signature element inline, for example the week grid in `oh-shift.html`.
- `site.css` loads the fonts with paths relative to itself. Pages in subfolders link it as `../site.css`.
- `404.html` and `blank/index.html` keep their own inline CSS. GitHub Pages serves `404.html` at any missing path, so a relative stylesheet link would break there.

## Add an app

1. Create `<app>.html` at the root. Copy `almanora.html`, which links `site.css` and `app.css`.
2. Create the folder `<app>/` with `privacy.html` and `support.html`. Copy them from `almanora/`. They link `../site.css` and `../legal.css`.
3. Point the breadcrumb on both pages to `../<app>.html`.
4. Put screenshots in `<app>/images/`. The app page links them as `<app>/images/<file>.png`.
5. Add the `detail-links` line on the app page. It links `<app>/support.html` and `<app>/privacy.html`.
6. Add a row to the app table and to the App Store block in `index.html`.

The App Store Connect URLs are `https://b347.dev/<app>/privacy.html` and `https://b347.dev/<app>/support.html`.

## Maintenance

### TestFlight beta status

`rakrak.html` and `oh-shift.html` each wrap their TestFlight join button in:

```html
<div class="tf-slot" data-tf-state="open">
```

Flip `data-tf-state` between `open` and `closed` when a beta opens or fills up:
- CSS swaps the label above the button ("Open for testers" / "Beta closed") and greys the button out.
- The last script in the file removes the link's `href` and marks it `aria-disabled` when closed, so it's actually non-interactive, not just faded.

No other edit is needed. One attribute drives both the look and the behavior.
