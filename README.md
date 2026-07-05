b347.dev

## Maintenance

### TestFlight beta status

`rakrak.html` and `oh-shift.html` each wrap their TestFlight join button in:

```html
<div class="tf-slot" data-tf-state="open">
```

Flip `data-tf-state` between `open` and `closed` when a beta opens or fills up:
- CSS swaps the label above the button ("Open for testers" / "Beta closed") and greys the button out.
- A small script near the bottom of the file (next to the theme-toggle script) removes the link's `href` and marks it `aria-disabled` when closed, so it's actually non-interactive, not just faded.

No other edit is needed — one attribute drives both the look and the behavior.
