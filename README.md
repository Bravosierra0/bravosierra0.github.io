b347.dev

Support and privacy landing pages for the b347 apps. Plain HTML and one stylesheet, served by GitHub Pages.

## Files

| Path | Content |
|------|---------|
| `index.html` | Start page: one row per app with status, store link, support and privacy |
| `privacy.html` | Privacy policy for the website itself |
| `<app>/support.html` | Support page per app. URL registered in App Store Connect |
| `<app>/privacy.html` | Privacy policy per app. URL registered in App Store Connect |
| `<app>/images/icon.png` | App icon, 256 px |
| `<app>.html` | Redirect to `/#<app>`. Old app pages, kept so old links work |
| `site.css` | The only stylesheet. Dark by default, light from the system setting |
| `avatar.svg` | Logo in the header |
| `favicon.svg`, `favicon.ico`, `apple-touch-icon.png`, `icon-512.png` | Browser and Home Screen icons |
| `_templates/` | Starting points for new pages. Jekyll does not publish folders that start with `_` |
| `404.html`, `blank/` | Error page and a separate page |

- All paths are absolute (`/site.css`), so every page works at any folder depth, the 404 page included.
- No JavaScript. The blinking cursor is CSS and stops when the visitor has reduced motion turned on.
- Fonts are hosted on the site itself. Nothing loads from other servers.

## Never rename

The URLs `/<app>/support.html` and `/<app>/privacy.html` are registered in App Store Connect. Renaming one breaks the App Store listing.

## Add an app

1. Copy the templates:
   - `_templates/support.html` → `<app>/support.html`
   - `_templates/privacy.html` → `<app>/privacy.html`
2. Add the row from `_templates/index-row.html` to `index.html`, inside `<div class="apps">`.
3. Replace every `{{PLACEHOLDER}}`. Find leftovers with `grep -rn '{{' --include='*.html' .`
4. Put the icon in `<app>/images/icon.png`, 256 px: `sips -Z 256`.
5. In App Store Connect, enter `https://b347.dev/<app>/support.html` and `https://b347.dev/<app>/privacy.html`.

## Every privacy page has these sections

Apple guideline 5.1.1 and the Swiss data protection act (revFADP) require them.

`Your data` · `Network requests` (if any) · `Third parties` · `Data on your device` · `Delete your data` · `Changes` · `Controller and contact`, plus the `rev:` date under the title.

## Change the status of an app

In `index.html`, in the app's row:
- live: `<span class="status live">● live</span>` and `<a class="store" href="…">[ App Store ]</a>`
- open beta: `<span class="status beta">○ testflight</span>` and `<a class="store" href="…">[ TestFlight ]</a>`
- full beta: `<span class="status beta">○ testflight</span>` and `<span class="store muted">[ beta full ]</span>`

## Revision

`rev` in the footer is the site revision. A privacy policy has its own `rev:` under its title. Update it when the policy changes:

```zsh
sed -i '' -E 's/rev [0-9-]+/rev 2026-12-01/' $(grep -rl 'class="bar"' --include='*.html' .)
```
