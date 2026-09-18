b347.dev

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
