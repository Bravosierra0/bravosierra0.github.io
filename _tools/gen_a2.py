#!/usr/bin/env python3
"""Generator for the A2 design of b347.dev.

Writes all pages (start page, support, privacy, site privacy, redirect stubs, 404, templates)
into the repo given as argv[1]. Run from the repo root:  python3 _tools/gen_a2.py .

Warning: it overwrites the generated pages. Hand edits to those pages are lost on the next run.
Folders starting with "_" are not published by GitHub Pages.
"""
import sys, os, html

ROOT = sys.argv[1]
REV = "2026-11-26"
MAIL_TEXT = "sibe1024[at]gmx{dot}net"
MAIL_HREF = "mailto:sibe1024@gmx.net"
CONTROLLER = "Beat Sifrig<br>Altstetterstrasse 193<br>CH-Zurich"

def mail():
    return f'<a href="{MAIL_HREF}">{MAIL_TEXT}</a>'

def head(title, desc, canonical):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="dark light">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#181818">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#ffffff">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/Fonts/IBMPlexMono-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
'''

BRAND = '<a class="brand" href="/"><img src="/avatar.svg" alt="">b347.dev</a>'

def footer():
    return f'''<footer class="bar">
  <div class="bar-in">
    <span>nopr_b347</span>
    <span>rev {REV}</span>
    <a href="/privacy.html">[ site privacy ]</a>
    <span>Branch never.</span>
  </div>
</footer>
</body>
</html>
'''

APPS = [
    dict(slug="isseeyou", name="ISSeeYou", tag="Real-time ISS tracker.", devices="Mac, iPhone, iPad and Apple TV",
         state="live", store=None),  # D4: App Store URL follows
    dict(slug="rakrak", name="Rak Rak", tag="Relationship date tracker.", devices="iPhone and iPad",
         state="closed", store=None),
    dict(slug="oh-shift", name="Oh Shift!", tag="Roster calendar for shift work.", devices="iPhone and iPad",
         state="closed", store=None),
    dict(slug="almanora", name="Almanora", tag="History for any calendar date.", devices="iPhone, iPad and Mac",
         state="closed", store=None),
]

def store_link(a, cls=""):
    c = f' class="{cls}"' if cls else ""
    if a["state"] in ("live", "open") and not a["store"]:
        return f'<span{c}></span>' if cls else ""   # URL not known yet: no link
    if a["state"] == "live":
        return f'<a{c} href="{a["store"]}">[ App Store ]</a>'
    if a["state"] == "open":
        return f'<a{c} href="{a["store"]}">[ TestFlight ]</a>'
    return f'<span{c} class="muted">[ beta full ]</span>' if not cls else f'<span class="{cls} muted">[ beta full ]</span>'

# ---------------- home
def home():
    rows = []
    for a in APPS:
        live = a["state"] == "live"
        status = '<span class="status live">● live</span>' if live else '<span class="status beta">○ testflight</span>'
        rows.append(f'''      <div class="app" id="{a["slug"]}">
        <div class="app-id"><img src="/{a["slug"]}/images/icon.png" alt=""><span><span class="app-name">{a["name"]}</span><span class="app-tag"> · {a["tag"]}</span></span></div>
        <div class="links">{status}{store_link(a, "store")}<a href="/{a["slug"]}/support.html">[ support ]</a><a href="/{a["slug"]}/privacy.html">[ privacy ]</a></div>
      </div>''')
    return head("b347.dev", "Apps for Apple platforms. Support and privacy pages.", "https://b347.dev/") + f'''<main class="wrap" id="main">
  <header class="top">{BRAND}</header>

  <section>
    <div class="cmd">&gt; whoami</div>
    <h1>Apps for Apple platforms.</h1>
    <p class="muted">Independent developer, Zurich. Support and privacy pages for each app are below.</p>
  </section>

  <section>
    <div class="cmd">&gt; ls apps/</div>
    <div class="apps">
{chr(10).join(rows)}
    </div>
  </section>

  <section>
    <div class="cmd">&gt; mail</div>
    {mail()}
    <div style="margin-top: 14px"><span class="cmd">&gt;</span> <span class="cursor" aria-hidden="true"></span></div>
  </section>
</main>
''' + footer()

def legal_top(a, page):
    return f'''<main class="wrap" id="main">
  <header class="top">
    {BRAND}
    <nav class="crumb" aria-label="Breadcrumb"><a href="/">~</a>/{a["slug"]}/<span class="here">{page}</span> <span class="prompt">$</span></nav>
  </header>

  <div class="title"><img src="/{a["slug"]}/images/icon.png" alt=""><h1>{a["name"]} <span>[ {page.capitalize()} ]</span></h1></div>
'''

def legal_links(a, other):
    s = store_link(a)
    store = s if a["state"] != "closed" else ""
    return f'  <div class="links"><a href="{other}.html">[ {other} ]</a>{store}</div>\n</main>\n'

def support(a, faq):
    items = "\n".join(f'''    <section>
      <h3>--[ {html.escape(q, quote=False)} ]</h3>
      <p>{ans}</p>
    </section>''' for q, ans in faq)
    return head(f'{a["name"]} Support — b347.dev', f'Support for {a["name"]}: contact and common questions.', f'https://b347.dev/{a["slug"]}/support.html') + legal_top(a, "support") + f'''  <p class="sub">{a["name"]} for {a["devices"]}.</p>

  <section>
    <div class="cmd">&gt; mail</div>
    <p>Need help, or found a bug? {mail()}</p>
  </section>

  <div class="cmd" style="margin-bottom: 8px">&gt; cat faq</div>
  <div class="doc">
{items}
  </div>

''' + legal_links(a, "privacy") + footer()

def standard_tail(name):
    return [
        ("Delete your data", f"{name} collects no personal data, so I hold nothing to delete. For questions or requests about your data, write to {mail()}."),
        ("Changes", "Changes to this policy appear on this page, with a new rev date."),
        ("Controller and contact", f"{CONTROLLER}<br>{mail()}"),
    ]

def privacy(a, sections):
    secs = "\n".join(f'''    <section>
      <h2>--[ {t} ]</h2>
{"".join(f"      <p>{p}</p>{chr(10)}" for p in (body if isinstance(body, list) else [body]))}    </section>''' for t, body in sections + standard_tail(a["name"]))
    return head(f'{a["name"]} Privacy Policy — b347.dev', f'Privacy policy for {a["name"]}.', f'https://b347.dev/{a["slug"]}/privacy.html') + legal_top(a, "privacy") + f'''  <p class="sub">{a["name"]} for {a["devices"]}. rev: {REV}</p>

  <div class="doc">
{secs}
  </div>

''' + legal_links(a, "support") + footer()

# ---------------- content
CONTENT = {
"isseeyou": dict(
  privacy=[
    ("Your data", "ISSeeYou collects no personal data and never asks for your location. It has no account, no analytics, no ads and no tracking."),
    ("Network requests", ["The app loads the station's position from api.wheretheiss.at. To find the country below the station, it sends the station's coordinates to the same server. It never sends your position.",
                          "The requests carry no account, name or device identifier. Like any web request, they show your IP address to that server."]),
    ("Third parties", "No personal data goes to third parties. The map comes from Apple Maps, and Apple's privacy policy applies to the map data."),
    ("Data on your device", "Your settings (appearance, units, refresh interval) stay on the device. Deleting the app removes them."),
  ],
  faq=[
    ("Where does the position come from?", "ISSeeYou loads the position of the International Space Station from wheretheiss.at."),
    ("Where is the app on my Mac?", "ISSeeYou runs in the menu bar, not in the Dock. Click its icon in the menu bar to open it."),
    ("How often does the position update?", "Open the settings and choose a value under Refresh every. The choices go from 5 seconds to 15 minutes."),
    ("How do I switch between kilometers and miles?", "Open the settings and choose a value under Units to display."),
    ("Why does the map not move?", "Check that Auto Refresh is on. The app also needs a network connection to load the position."),
  ]),
"rakrak": dict(
  privacy=[
    ("Your data", ["Rak Rak collects no personal data. It has no server, no account, no analytics, no ads and no tracking.",
                   "The occasions you add, with any note or photo, stay on your device."]),
    ("iCloud sync", "If you use iCloud, Rak Rak syncs your occasions through your own iCloud account (CloudKit). Apple's privacy policy applies to iCloud."),
    ("Permissions", ["Notifications: only after you tap Enable Notifications.",
                     "Photos: you pick a photo in the system photo picker, and Rak Rak receives only that photo."]),
    ("Third parties", "No personal data goes to third parties. Rak Rak uses no third-party analytics, advertising or tracking SDK."),
    ("Data on your device", ["Delete an occasion in the app to remove it. If iCloud sync is on, this also removes it from iCloud.",
                             "Deleting the app removes the data from this device only. To remove the iCloud copy too, delete your occasions and categories in the app first."]),
  ],
  faq=[
    ("Where is my data stored?", "On your device. If you sign in to iCloud, Rak Rak also syncs it through your own iCloud account."),
    ("How do I show an occasion on the Home Screen widget?", "Swipe right on the occasion to pin it, or turn on Pinned in Edit. Then add the Rak Rak widget to your Home Screen."),
    ("How do I change the app's language?", "Settings &gt; Language. Rak Rak supports English, German, and Thai."),
    ("How do I get a reminder for an occasion?", "Open the occasion, tap Edit, turn on Same Day, and pick a Time. Second alert adds a reminder 1 to 30 days before."),
    ("How do I remove an occasion and its data?", "Open the occasion and tap Delete. If iCloud sync is on, this also removes it from iCloud."),
  ]),
"oh-shift": dict(
  privacy=[
    ("Your data", ["Oh Shift! collects no personal data. It has no server, sends nothing over the network, and has no account, analytics, ads or tracking.",
                   "Your shift types and departments stay on your device."]),
    ("Calendar access", "Oh Shift! saves each shift as an event in its own calendar, named \"Oh Shift!\". For this it asks for full calendar access. It reads and writes events only in that calendar."),
    ("iCloud", "If you use iCloud Calendar, the \"Oh Shift!\" calendar lives in your iCloud account, and Apple syncs it like any other calendar. Apple's privacy policy applies."),
    ("Third parties", "No personal data goes to third parties."),
    ("Data on your device", ["The Home Screen widget reads your next shifts from storage that only the app and its widget can open.",
                             "Delete a shift in the app to remove it and its calendar event. Deleting the app removes your shift types and departments. The \"Oh Shift!\" calendar stays in the Calendar app until you delete it there."]),
  ],
  faq=[
    ("Where are my shifts stored?", "In the Calendar app, in a calendar named \"Oh Shift!\". If you use iCloud Calendar, Apple syncs it like your other calendars."),
    ("Why does the app ask for calendar access?", "Oh Shift! saves each shift as a calendar event. It reads and writes events only in its own \"Oh Shift!\" calendar."),
    ("I denied calendar access. How do I turn it on?", "Open the Settings app, tap Apps, then Oh Shift!, then Calendars. Choose Full Access."),
    ("How do I get a reminder before a shift?", "Open the shift and pick a reminder. The Calendar app shows the alert, like for any other event."),
    ("I deleted the app. Where are my shifts?", "They are still in the \"Oh Shift!\" calendar in the Calendar app. To remove them, delete that calendar in the Calendar app."),
  ]),
"almanora": dict(
  privacy=[
    ("Your data", "Almanora collects no personal data. It has no account, no analytics, no ads and no tracking."),
    ("Network requests", "To show a day, the app sends the month and day to today.zenquotes.io. The request carries no account, name or device identifier. Like any web request, it shows your IP address to the ZenQuotes server."),
    ("Third parties", "No personal data goes to third parties. A tap on a Wikipedia link opens Wikipedia, and Wikipedia's privacy policy applies there."),
    ("Data on your device", "Loaded days stay on the device for up to 30 days. Deleting the app removes them."),
  ],
  faq=[
    ("Where do the entries come from?", "Almanora loads each day from today.zenquotes.io. The entries and links come from Wikipedia."),
    ("How do I see another day?", "Tap a day in the week strip, or swipe sideways. The calendar button picks any month and day. On the Mac, the Go menu has Previous Day, Next Day and Today."),
    ("Why does the app say \"Offline\"?", "The network failed, so the app shows the saved copy of the day. Tap Retry when the network is back. On the Mac, Reload Day (Command-R) does the same."),
    ("How do I hide births or deaths?", "Open the settings and switch off Show births or Show deaths. On iPhone and iPad, tap the gear button. On the Mac, choose Almanora &gt; Settings."),
    ("Where is my data stored?", "On your device only. The app keeps loaded days for up to 30 days and has no account."),
  ]),
}

def site_privacy():
    secs = [
        ("This website", "b347.dev is a static website: no cookies, no analytics, nothing loaded from other servers."),
        ("Hosting", "GitHub Pages hosts the site. GitHub processes visitors' IP addresses to deliver the pages and keep the service secure. GitHub's privacy statement applies."),
        ("Your data", "I collect no personal data through this website. If you email me, I use your message and address only to answer."),
        ("Apps", "Each app has its own privacy policy, linked on the start page."),
        ("Your rights", f"You can ask what data I hold about you, and ask to correct or delete it. Write to {mail()}."),
        ("Changes", "Changes to this policy appear on this page, with a new rev date."),
        ("Controller and contact", f"{CONTROLLER}<br>{mail()}"),
    ]
    body = "\n".join(f'''    <section>
      <h2>--[ {t} ]</h2>
      <p>{p}</p>
    </section>''' for t, p in secs)
    return head("Privacy — b347.dev", "Privacy policy for the b347.dev website.", "https://b347.dev/privacy.html") + f'''<main class="wrap" id="main">
  <header class="top">
    {BRAND}
    <nav class="crumb" aria-label="Breadcrumb"><a href="/">~</a>/<span class="here">privacy</span> <span class="prompt">$</span></nav>
  </header>

  <h1>b347.dev <span class="muted" style="font-weight: 400">[ Privacy ]</span></h1>
  <p class="sub">The website b347.dev. rev: {REV}</p>

  <div class="doc">
{body}
  </div>
</main>
''' + footer()

def redirect(slug):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="robots" content="noindex">
<link rel="canonical" href="https://b347.dev/#{slug}">
<meta http-equiv="refresh" content="0; url=/#{slug}">
<title>Moved — b347.dev</title>
</head>
<body><p>This page moved to <a href="/#{slug}">b347.dev/#{slug}</a>.</p></body>
</html>
'''

def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

write("index.html", home())
write("privacy.html", site_privacy())
for a in APPS:
    c = CONTENT[a["slug"]]
    write(f'{a["slug"]}/support.html', support(a, c["faq"]))
    write(f'{a["slug"]}/privacy.html', privacy(a, c["privacy"]))
    write(f'{a["slug"]}.html', redirect(a["slug"]))

# templates with placeholders, for adding an app by hand
T = dict(slug="{{SLUG}}", name="{{NAME}}", tag="{{TAGLINE}}", devices="{{DEVICES}}", state="live", store="{{STORE_URL}}")
write("_templates/support.html", support(T, [("{{QUESTION}}", "{{ANSWER}}"), ("Where is my data stored?", "{{DATA_ANSWER}}")]))
write("_templates/privacy.html", privacy(T, [
    ("Your data", "{{NAME}} collects no personal data. It has no account, no analytics, no ads and no tracking."),
    ("Network requests", "{{NETWORK: which server, what is sent. Or: The app sends nothing over the network.}}"),
    ("Third parties", "{{NAME}} shares no personal data with third parties. {{Name each service and what it receives.}}"),
    ("Data on your device", "{{What the app stores locally, and how to remove it.}}"),
]))
T_row = home().split('<div class="app" id="isseeyou">')[1].split('</div>\n      </div>')[0]
write("_templates/index-row.html", "<!-- One app row for index.html, inside <div class=\"apps\">. Status: live / testflight. Store link: [ App Store ], [ TestFlight ] or <span class=\"store muted\">[ beta full ]</span>. -->\n"
      + '      <div class="app" id="{{SLUG}}">' + T_row.replace("isseeyou", "{{SLUG}}").replace("ISSeeYou", "{{NAME}}").replace("Real-time ISS tracker.", "{{TAGLINE}}").replace("{{STORE_URL_{{SLUG}}}}", "{{STORE_URL}}").replace("{{STORE_URL_ISSEEYOU}}", "{{STORE_URL}}").replace('<span class="store"></span>', '<a class="store" href="{{STORE_URL}}">[ App Store ]</a>') + "</div>\n      </div>\n")
def not_found():
    return head("404 Not Found — b347.dev", "Page not found.", "https://b347.dev/") + f'''<main class="wrap" id="main">
  <header class="top">{BRAND}</header>
  <section>
    <div class="cmd">&gt; TYPE PAGE HTML A</div>
    <pre class="term">DMS002E File PAGE HTML A not found
Ready(00028);</pre>
    <h1>404 · Not found</h1>
    <p class="muted">This page does not exist, or it moved.</p>
  </section>
  <div class="links"><a href="/">[ cd ~ ]</a></div>
</main>
''' + footer()

write("404.html", not_found())
print("generated")
