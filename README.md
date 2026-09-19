# Refund Fairfund Partners — static site

Six pages, plain HTML + CSS + a little vanilla JS. No build step. Open `index.html`
or serve the folder (`python3 -m http.server`).

```
index.html         Home — hero, "first 24 hours" triage strip, services, FAQ, recovery-scam warning
services.html      What we handle — five fraud types, plus an explicit "what we don't do"
how-it-works.html  Five-stage case process, timings, and what limits outcomes
resources.html     Free self-help: first-48-hours steps, official reporting bodies, recovery-scam red flags
about.html         Team, registration/licensing table, fees, standards
contact.html       Intake form + what happens next
assets/styles.css  All styling, token-driven
assets/site.js     Mobile nav + form validation
```

## Design tokens

Edit the `:root` block in `styles.css`. Palette: `--ink` #0F2231, `--paper` #F4F5F2,
`--pine` #1E5B4F (actions), `--brass` #A9812F (rules and markers, used sparingly),
`--flag` #8A2F24 (warnings only). Type: Newsreader for display, IBM Plex Sans for
everything else, loaded from Google Fonts.

## Before launch

**Replace every `[bracketed placeholder]`.** They mark the places where a real fact has
to go — company number, licence and registration numbers, fee structure, turnaround
times, team names and backgrounds, office address, phone. I deliberately did not invent
these. On a site in this sector, empty or vague credentials are the first thing an
informed visitor treats as a warning sign.

Also:

1. Wire the contact form to a real backend or form service. Right now `site.js` only
   validates and shows a notice. Add server-side validation, a spam control, and TLS.
2. Verify the reporting-agency links in `resources.html` and trim the list to the
   countries the firm actually serves. Agencies reorganise and URLs change.
3. Write the three linked legal pages — privacy policy, terms of engagement, complaints
   procedure — and point the footer links at them.
4. Add favicon, Open Graph image, `robots.txt`, `sitemap.xml`.
5. Have a lawyer in each target jurisdiction review the claims. Consumer-protection and
   financial-promotion rules bite hard on this category of business.

## What I deliberately left out

No guaranteed-recovery language, no invented success rates or "£XXm recovered" counters,
no testimonials, no countdown timers or urgency devices, no live-chat popup. Those are the
exact signals that regulators, banks and search engines use to flag recovery-fraud sites —
and they are also what makes real victims, who have already been fooled once by something
polished, close the tab. The credibility here comes from the verification table on
`about.html` and the free-help page, not from persuasion.

## Single-file build

`Refund Fairfund-recovery-single.html` is the whole site — all six pages, inlined CSS and JS —
in one self-contained file with a hash router. Routes are `#/home`, `#/services`,
`#/how-it-works`, `#/resources`, `#/about`, `#/contact`. A deep link to a section
inside a page uses a colon: `#/resources:recovery-scams`.

Regenerate it after editing any of the six page files:

```
python3 build_single.py
```

The script pulls the `<main>` out of each page, rebuilds the nav from its own route
table, rewrites every `page.html` link to the matching hash route, and inlines
`assets/styles.css` and `assets/site.js`. So the six files stay the source of truth —
edit those, not the bundle.

Use the single file when you want one artefact to host, email or drop onto any static
host with no server config. Use the six-file version when the client wants real URLs
and per-page SEO — a hash-routed page is one document to a crawler, which matters for
a site that should rank on "how to report fraud" style queries.
