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
| `_tools/gen_a2.py` | Generator. Writes every page except `blank/` from the data in the file |
| `404.html`, `blank/` | Error page and a separate page |

- All paths are absolute (`/site.css`), so every page works at any folder depth, the 404 page included.
- No JavaScript. The blinking cursor is CSS and stops when the visitor has reduced motion turned on.
- Fonts are hosted on the site itself. Nothing loads from other servers.

## Never rename

The URLs `/<app>/support.html` and `/<app>/privacy.html` are registered in App Store Connect. Renaming one breaks the App Store listing.

## The generator writes the pages

`_tools/gen_a2.py` writes every page except `blank/`. It overwrites them on each run. Put each change into `gen_a2.py`, or the next run removes it.

```zsh
python3 _tools/gen_a2.py .
```

## Add an app

1. In `_tools/gen_a2.py`, add an entry to `APPS` (slug, name, tag, devices, state, store).
2. Add its texts to `CONTENT` under the same slug: the privacy sections and the FAQ.
3. Put the icon in `<app>/images/icon.png`, 256 px: `sips -Z 256`.
4. Run the generator. Then run `./check.zsh`.
5. In App Store Connect, enter `https://b347.dev/<app>/support.html` and `https://b347.dev/<app>/privacy.html`.

## Every privacy page has these sections

Apple guideline 5.1.1 and the Swiss data protection act (revFADP) require them.

- `Your data`
- `Network requests` (if any)
- `Third parties`
- `Data on your device`
- `Delete your data`
- `Changes`
- `Controller and contact`

The `rev:` date goes under the title.

## Change the status of an app

In `_tools/gen_a2.py`, set `state` and `store` in the app's entry in `APPS`. Then run the generator.
- `live`: "● live" and `[ App Store ]`. `store` is the App Store URL.
- `open`: "○ testflight" and `[ TestFlight ]`. `store` is the TestFlight link.
- `closed`: "○ testflight" and `[ beta full ]`.
- `dev`: "○ in dev" and no store link.

## Revision

`rev:` in the footer and under each privacy title shows the date of the last change, as `YYYYMMDD`. The generator writes one date for all pages. To change it, set `REV` in `_tools/gen_a2.py`. Then run the generator.

## Before a push

```zsh
./check.zsh
```

FAIL blocks the push: broken internal link, missing page or stub, missing privacy section, missing rev date, missing mailto, third-party resource. WARN does not block: `{{...}}` placeholders, different rev dates.
