#!/usr/bin/env python3
"""Assemble the six-page site into one self-contained, hash-routed HTML file."""

import re
import pathlib

SRC = pathlib.Path(__file__).parent
OUT = pathlib.Path(__file__).parent / "Fairfund Recovery-recovery-single.html"

ROUTES = [
    ("index.html", "home", "Home"),
    ("services.html", "services", "What we handle"),
    ("how-it-works.html", "how-it-works", "How it works"),
    ("resources.html", "resources", "Report it yourself"),
    ("about.html", "about", "About"),
    ("contact.html", "contact", "Request a case review"),
]
FILE_TO_ROUTE = {f: r for f, r, _ in ROUTES}


def rewrite_links(html: str) -> str:
    """page.html -> #/page   ·   page.html#frag -> #/page:frag"""

    def sub(m):
        page, frag = m.group(1), m.group(2)
        route = FILE_TO_ROUTE.get(page)
        if not route:
            return m.group(0)
        return f'href="#/{route}:{frag}"' if frag else f'href="#/{route}"'

    return re.sub(r'href="([a-z0-9\-]+\.html)(?:#([\w\-]+))?"', sub, html)


def grab(html: str, tag: str, attrs: str = "") -> str:
    pattern = rf"<{tag}{attrs}[^>]*>(.*?)</{tag}>"
    m = re.search(pattern, html, re.S)
    if not m:
        raise SystemExit(f"could not find <{tag}> block")
    return m.group(1)


pages = {}
for filename, route, _ in ROUTES:
    raw = (SRC / filename).read_text(encoding="utf-8")
    pages[route] = rewrite_links(grab(raw, "main"))

home_raw = (SRC / "index.html").read_text(encoding="utf-8")
header = rewrite_links(grab(home_raw, "header"))
footer = rewrite_links(grab(home_raw, "footer"))

css = (SRC / "assets" / "styles.css").read_text(encoding="utf-8")
base_js = (SRC / "assets" / "site.js").read_text(encoding="utf-8")

nav_links = "\n".join(
    f'      <a href="#/{r}" data-route="{r}"'
    + (' class="btn btn--solid"' if r == "contact" else "")
    + f">{label}</a>"
    for _, r, label in ROUTES
)
# rebuild the nav from the route table so aria-current is router-driven
header = re.sub(
    r'(<nav class="nav" id="site-nav" aria-label="Main">).*?(</nav>)',
    lambda m: m.group(1) + "\n" + nav_links + "\n    " + m.group(2),
    header,
    flags=re.S,
)

sections = "\n".join(
    f'  <div class="page" id="page-{r}" data-route="{r}" hidden>{pages[r]}</div>'
    for _, r, _ in ROUTES
)

ROUTER_CSS = """
/* --- single-file router --- */
[hidden] { display: none !important; }
.page:focus { outline: none; }
"""

ROUTER_JS = """
// ---- hash router -------------------------------------------------------
(function () {
  var pages = Array.prototype.slice.call(document.querySelectorAll('.page'));
  var links = Array.prototype.slice.call(document.querySelectorAll('[data-route]'));
  var titles = %TITLES%;
  var DEFAULT = 'home';

  function parse() {
    var hash = location.hash || '';
    // Plain in-page anchors (#main, #recovery-scams) are not routes — leave the
    // current page alone and let the browser scroll.
    if (hash && hash.charAt(1) !== '/') return null;
    var bits = hash.replace(/^#\\//, '').split(':');
    var route = bits[0] || DEFAULT;
    if (!document.getElementById('page-' + route)) route = DEFAULT;
    return { route: route, anchor: bits[1] || null };
  }

  function render(push) {
    var r = parse();
    if (!r) return;

    pages.forEach(function (p) { p.hidden = p.dataset.route !== r.route; });

    links.forEach(function (a) {
      if (a.dataset.route === r.route) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });

    document.title = titles[r.route] + ' — Fairfund Recovery Partners';

    // close the mobile menu on navigation
    var nav = document.getElementById('site-nav');
    var toggle = document.querySelector('.nav-toggle');
    if (nav && toggle && window.matchMedia('(max-width: 940px)').matches) {
      nav.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      toggle.textContent = 'Menu';
    }

    if (r.anchor) {
      var target = document.getElementById(r.anchor);
      if (target) { target.scrollIntoView({ behavior: 'auto', block: 'start' }); return; }
    }
    if (push) window.scrollTo(0, 0);
  }

  window.addEventListener('hashchange', function () { render(true); });
  render(false);
})();
"""

titles_js = "{" + ", ".join(f"'{r}': '{label}'" for _, r, label in ROUTES) + "}"

doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Fairfund Recovery Partners — Fraud investigation and asset tracing</title>
<meta name="description" content="Fairfund Recovery Partners investigates fraud losses, traces where money went, and builds the evidence banks, regulators and law enforcement need to act.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=Newsreader:opsz,wght@6..72,300;6..72,400;6..72,500&display=swap" rel="stylesheet">
<style>
{css}
{ROUTER_CSS}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="masthead">{header}</header>

<main id="main">
{sections}
</main>

<footer class="foot">{footer}</footer>

<script>
{base_js}
{ROUTER_JS.replace('%TITLES%', titles_js)}
</script>
</body>
</html>
"""

OUT.write_text(doc, encoding="utf-8")
print(f"wrote {OUT} ({len(doc):,} bytes)")
