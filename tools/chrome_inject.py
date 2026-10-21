#!/usr/bin/env python3
"""
Own the site header and footer on every content page.

Before this, both were hand-copied into 50 files, which is how /health-systems
and /bridge ended up with a "Talk to Us" button while every other page said
"Request a Demo", and how the footer's column list drifted page by page. The
header and footer are now generated from the two tables below, so a nav change
is one edit instead of fifty.

Same managed-block pattern as seo_inject.py and internal_links.py: the header
replaces the page's first bare <nav> element, the footer replaces its <footer>
element, and the shared style and script live between <!-- CHROME:VASL --> and
<!-- /CHROME:VASL --> so a re-run strips the old copy and writes a fresh one.
The <nav class="doc-toc"> on the legal pages is a table of contents, not site
chrome, and is left alone; the regex only matches the bare opening tag.

Not injected into SKIP below: the Search Console file, the two redirect pages
and the retired /outcomes stub have no chrome today and are not pages, and
404.html is a standalone centred error card whose body is a flex centring
container with no mono font loaded, so dropping a fixed header and a six
column footer into it would fight its layout rather than match the artboards.

Run:  python3 tools/chrome_inject.py            (writes)
      python3 tools/chrome_inject.py --check    (exits 1 if anything would change)
"""

import re
import sys
from pathlib import Path

from seo_shared import IGNORE

SITE = Path(__file__).resolve().parent.parent / "site"
MARK_OPEN = "<!-- CHROME:VASL -->"
MARK_CLOSE = "<!-- /CHROME:VASL -->"

SKIP = IGNORE | {"404.html"}

# ---------------------------------------------------------------------------
# The Solutions menu. One row per buyer, in the order the artboards draw them.
# ---------------------------------------------------------------------------
SOLUTIONS = [
    ("/health-systems", "Health Plans &amp; Systems",
     "VLAP and the platform inside the care you already deliver."),
    ("/bridge", "Vasl Bridge",
     "A text every day from ED discharge to the first visit."),
    ("/for-schools", "Schools",
     "Daily check-ins, peer support and coaching for K-12 districts."),
    ("/for-organizations", "Community Organizations",
     "The platform for youth-serving organizations."),
]

# ---------------------------------------------------------------------------
# The footer. Five columns beside the brand block, exactly as drawn.
# ---------------------------------------------------------------------------
FOOTER_COLS = [
    ("Platform", [
        ("/platform", "Platform"),
        ("/vlap", "VLAP"),
        ("/technology", "Technology"),
        ("/demo.html", "Signal Taxonomy"),
    ]),
    ("Solutions", [
        ("/health-systems", "Health Plans &amp; Systems"),
        ("/bridge", "Vasl Bridge"),
        ("/for-schools", "Schools"),
        ("/for-organizations", "Community Organizations"),
        ("/contact?subject=Pricing", "Talk to us about pricing"),
    ]),
    ("Company", [
        ("/about", "About"),
        ("/team", "Team"),
        ("/careers", "Careers"),
        ("/research", "Research"),
        ("/blog", "Blog"),
        ("/contact", "Contact"),
    ]),
    ("Resources", [
        ("/glossary", "Glossary"),
        ("/school-mental-health-rfp", "School Mental Health RFP Guide"),
        ("/dialect-bias-mental-health-screening", "Dialect Bias in Screening"),
        ("/hedis-behavioral-health-cultural-fit", "HEDIS &amp; Cultural Fit"),
        ("/for-families", "For Families"),
        ("/support", "Help Center"),
    ]),
    ("Legal", [
        ("/privacy.html", "Privacy"),
        ("/terms.html", "Terms"),
        ("/baa.html", "BAA"),
        ("/accessibility", "Accessibility"),
    ]),
]

COPYRIGHT = "&copy; 2026 Vasl Health PBC. All rights reserved."

# ---------------------------------------------------------------------------
# Which top-level item carries the active state. A page that is not listed
# gets no active item, which is the homepage case.
# ---------------------------------------------------------------------------
ACTIVE_PLATFORM = {"platform.html"}
ACTIVE_VLAP = {"vlap.html"}
ACTIVE_SOLUTIONS = {
    "health-systems.html", "bridge.html",
    "for-schools.html", "for-organizations.html",
}
ACTIVE_ABOUT = {"about.html", "team.html", "blog.html"}


def active_for(rel: str) -> str:
    """platform, vlap, solutions, about, or "" for no active item."""
    if rel in ACTIVE_PLATFORM:
        return "platform"
    if rel in ACTIVE_VLAP:
        return "vlap"
    if rel in ACTIVE_SOLUTIONS:
        return "solutions"
    if rel in ACTIVE_ABOUT or rel.startswith("blog-") or rel.startswith("blog/"):
        return "about"
    return ""


CHEVRON = (
    '<svg class="vh-chev" width="10" height="10" viewBox="0 0 10 10" aria-hidden="true">'
    '<path d="M2 3.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.2"></path>'
    "</svg>"
)
CHEVRON_LG = (
    '<svg class="vh-chev" width="14" height="14" viewBox="0 0 10 10" aria-hidden="true">'
    '<path d="M2 3.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1"></path>'
    "</svg>"
)

STYLE = """<style>
/* Header, Solutions menu, phone sheet and footer. Values come from the
   navigation artboards; every colour falls back to a literal so the block
   also works on a page that does not define the full token set. */
/* The logo image is inline by default, so its line box added 13px of leading
   and made the bar 94px instead of the 81px the artboards draw. */
.nav-logo img{display:block;}
.nav-links{align-items:center;}
.nav-links > li{display:flex;align-items:center;}
.nav-links a,.vh-sol-btn{height:40px;display:inline-flex;align-items:center;}
.vh-sol-btn{gap:6px;background:none;border:0;padding:0;cursor:pointer;line-height:1.2;
  font-family:var(--mono,'IBM Plex Mono',monospace);font-size:10px;letter-spacing:0.09em;
  text-transform:uppercase;color:var(--dust,#8B7B6B);transition:color 0.2s;}
.vh-sol-btn:hover{color:var(--ink,#1C1C1C);}
.vh-sol[data-open="true"] .vh-sol-btn{color:var(--ink,#1C1C1C);}
.vh-sol[data-open="true"] .vh-chev{transform:rotate(180deg);}
.vh-chev{transition:transform 0.18s;}
.nav-links > li > a.is-active,.vh-sol.is-active .vh-sol-btn{color:var(--ink,#1C1C1C);
  padding-bottom:4px;border-bottom:1px solid var(--clay,#C4896F);}
.vh-sol-menu{position:absolute;top:100%;margin-top:1px;left:0;width:440px;z-index:120;
  background:var(--warm-white,#FAF7F2);border:1px solid var(--chalk,#E2DAD0);
  border-top:2px solid var(--deep-green,#2D4A3E);box-shadow:0 18px 40px rgba(28,28,28,0.10);
  display:flex;flex-direction:column;}
.vh-sol-menu[hidden]{display:none;}
.vh-sol-menu a{display:flex;flex-direction:column;align-items:flex-start;gap:4px;
  padding:18px 24px;height:auto;
  border-bottom:1px solid var(--chalk,#E2DAD0);text-decoration:none;text-transform:none;
  letter-spacing:normal;transition:background 0.15s;}
.vh-sol-menu a:last-child{border-bottom:none;}
.vh-sol-menu a:hover{background:var(--parchment,#F0EAE0);}
.vh-sol-menu a.is-active{border-left:2px solid var(--ink,#1C1C1C);padding-left:22px;}
.vh-sm-name{font-family:var(--serif,'Newsreader',Georgia,serif);font-size:20px;font-weight:400;
  letter-spacing:-0.01em;line-height:1.25;color:var(--ink,#1C1C1C);text-transform:none;}
.vh-sm-line{font-family:var(--sans,'IBM Plex Sans',sans-serif);font-size:14px;font-weight:300;
  line-height:1.55;color:var(--ink-70,rgba(28,28,28,0.70));text-transform:none;}

/* Phone sheet */
.vh-sheet{position:fixed;inset:0;z-index:300;background:var(--warm-white,#FAF7F2);
  display:flex;flex-direction:column;}
.vh-sheet[hidden]{display:none;}
.vh-sheet-top{height:72px;flex-shrink:0;padding:16px 20px;display:flex;align-items:center;
  justify-content:space-between;border-bottom:1px solid var(--ink-12,rgba(28,28,28,0.12));}
.vh-close{width:44px;height:44px;position:relative;background:none;border:0;cursor:pointer;padding:0;}
.vh-close span{position:absolute;left:11px;top:21px;width:22px;height:1.5px;
  background:var(--ink,#1C1C1C);display:block;}
.vh-close span:first-child{transform:rotate(45deg);}
.vh-close span:last-child{transform:rotate(-45deg);}
.vh-sheet-body{flex:1;min-height:0;overflow-y:auto;padding:8px 20px;display:flex;flex-direction:column;}
.vh-sheet-body > a,.vh-sheet-sol{height:64px;flex-shrink:0;display:flex;align-items:center;
  border-bottom:1px solid var(--chalk,#E2DAD0);background:none;border-left:0;border-right:0;border-top:0;
  font-family:var(--mono,'IBM Plex Mono',monospace);font-size:14px;letter-spacing:0.09em;
  text-transform:uppercase;color:var(--ink,#1C1C1C);text-decoration:none;cursor:pointer;
  width:100%;justify-content:flex-start;padding:0;}
.vh-sheet-sol{justify-content:space-between;}
.vh-sheet-sol[aria-expanded="true"]{border-bottom:none;}
.vh-sheet-sol[aria-expanded="true"] .vh-chev{transform:rotate(180deg);}
.vh-sheet-sub{background:var(--parchment,#F0EAE0);border-top:2px solid var(--deep-green,#2D4A3E);
  display:flex;flex-direction:column;flex-shrink:0;}
.vh-sheet-sub[hidden]{display:none;}
.vh-sheet-sub a{display:flex;flex-direction:column;align-items:flex-start;gap:2px;
  padding:13px 16px;height:auto;
  border-bottom:1px solid var(--chalk,#E2DAD0);text-decoration:none;}
.vh-sheet-sub .vh-sm-name{font-size:19px;}
.vh-sheet-sub .vh-sm-line{font-size:13.5px;line-height:1.5;}
.vh-sheet-foot{padding:16px 20px 28px;border-top:1px solid var(--chalk,#E2DAD0);flex-shrink:0;
  background:var(--warm-white,#FAF7F2);}
.vh-sheet-cta{display:block;text-align:center;font-family:var(--mono,'IBM Plex Mono',monospace);
  font-size:11px;letter-spacing:0.08em;text-transform:uppercase;text-decoration:none;
  background:var(--ink,#1C1C1C);color:var(--warm-white,#FAF7F2);padding:18px 32px;}
body.vh-locked{overflow:hidden;}

/* The help pages never carried a hamburger, so the button styling ships here
   rather than relying on each page's own copy. */
.ham-btn{display:none;flex-direction:column;gap:5px;background:none;border:none;
  cursor:pointer;padding:6px;margin-left:8px;}
.ham-btn span{display:block;width:22px;height:1.5px;background:var(--ink,#1C1C1C);}
@media(min-width:781px){.vh-sheet{display:none;}}
@media(max-width:780px){
  .ham-btn{display:flex;}
  .nav-links{display:none;}
  .nav-cta{display:none;}
  .vh-sol-menu{display:none;}
  nav{padding-top:16px;padding-bottom:16px;}
  nav > .nav-logo img{width:144px;height:36px;}
}
</style>"""

SCRIPT = """<script>
(function () {
  var sol = document.querySelector('.vh-sol');
  var btn = sol && sol.querySelector('.vh-sol-btn');
  var menu = sol && sol.querySelector('.vh-sol-menu');

  // The panel hangs off <nav>, so its left edge is set from the button rather
  // than inherited from a positioned list item. Measuring beats a hard-coded
  // offset here: nav height varies by a few pixels from page to page.
  function placeMenu() {
    if (!menu || !btn) return;
    var nav = btn.closest('nav');
    var pad = parseFloat(getComputedStyle(nav).paddingRight) || 0;
    var max = nav.clientWidth - pad - menu.offsetWidth;
    menu.style.left = Math.max(0, Math.min(btn.offsetLeft, max)) + 'px';
  }

  function setSolutions(open) {
    if (!sol) return;
    sol.setAttribute('data-open', open ? 'true' : 'false');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    menu.hidden = !open;
    if (open) placeMenu();
  }

  if (sol) {
    setSolutions(false);
    // Hover and click both open it, so a pointer user never has to click and
    // a keyboard user never has to hover.
    sol.addEventListener('mouseenter', function () { setSolutions(true); });
    sol.addEventListener('mouseleave', function () { setSolutions(false); });
    btn.addEventListener('click', function () {
      setSolutions(btn.getAttribute('aria-expanded') !== 'true');
    });
    sol.addEventListener('focusout', function (e) {
      if (!sol.contains(e.relatedTarget)) setSolutions(false);
    });
    window.addEventListener('resize', function () {
      if (!menu.hidden) placeMenu();
    });
  }

  var sheet = document.getElementById('vh-sheet');
  var ham = document.getElementById('ham-btn');
  var close = document.getElementById('vh-close');
  var sub = document.getElementById('vh-sheet-sub');
  var subBtn = sheet && sheet.querySelector('.vh-sheet-sol');

  function setSheet(open) {
    if (!sheet) return;
    sheet.hidden = !open;
    document.body.classList.toggle('vh-locked', open);
    if (ham) ham.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open && close) close.focus();
    else if (!open && ham) ham.focus();
  }

  function setSub(open) {
    if (!sub) return;
    sub.hidden = !open;
    subBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  if (ham) ham.addEventListener('click', function () { setSheet(sheet.hidden); });
  if (close) close.addEventListener('click', function () { setSheet(false); });
  if (subBtn) subBtn.addEventListener('click', function () {
    setSub(subBtn.getAttribute('aria-expanded') !== 'true');
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    setSolutions(false);
    if (sheet && !sheet.hidden) setSheet(false);
  });

  // A click anywhere else closes the menu, which a pointer that never enters
  // the panel would otherwise leave open on a touch device.
  document.addEventListener('click', function (e) {
    if (sol && !sol.contains(e.target)) setSolutions(false);
  });
})();
</script>"""


def esc_attr(s: str) -> str:
    return s.replace('"', "&quot;")


def header_html(rel: str) -> str:
    active = active_for(rel)
    items = []
    for name, href, label in (("platform", "/platform", "Platform"), ("vlap", "/vlap", "VLAP")):
        c = ' class="is-active"' if active == name else ""
        items.append(f'    <li><a href="{href}"{c}>{label}</a></li>')

    sol_items = []
    for href, name, line in SOLUTIONS:
        c = ' class="is-active"' if f"{href[1:]}.html" == rel else ""
        sol_items.append(
            f'        <a href="{href}"{c}>'
            f'<span class="vh-sm-name">{name}</span>'
            f'<span class="vh-sm-line">{line}</span></a>'
        )
    sol_block = "\n".join(sol_items)

    sol_li_cls = "vh-sol is-active" if active == "solutions" else "vh-sol"
    about_cls = ' class="is-active"' if active == "about" else ""

    return f"""<nav>
  <a href="/" class="nav-logo"><img src="/assets/logo-lockup.svg" alt="Vasl Health" width="160" height="40"></a>
  <ul class="nav-links">
{chr(10).join(items)}
    <li class="{sol_li_cls}">
      <button type="button" class="vh-sol-btn" id="vh-sol-btn" aria-expanded="false" aria-controls="vh-sol-menu">Solutions{CHEVRON}</button>
      <div class="vh-sol-menu" id="vh-sol-menu" hidden>
{sol_block}
      </div>
    </li>
    <li><a href="/about"{about_cls}>About</a></li>
  </ul>
  <button class="ham-btn" id="ham-btn" aria-label="Menu" aria-expanded="false" aria-controls="vh-sheet">
    <span></span><span></span><span></span>
  </button>
  <a href="/contact" class="nav-cta">Request a Demo</a>
</nav>

<div class="vh-sheet" id="vh-sheet" hidden>
  <div class="vh-sheet-top">
    <a href="/" class="nav-logo"><img src="/assets/logo-lockup.svg" alt="Vasl Health" width="144" height="36"></a>
    <button type="button" class="vh-close" id="vh-close" aria-label="Close menu"><span></span><span></span></button>
  </div>
  <div class="vh-sheet-body">
    <a href="/platform">Platform</a>
    <a href="/vlap">VLAP</a>
    <button type="button" class="vh-sheet-sol" aria-expanded="false" aria-controls="vh-sheet-sub">Solutions{CHEVRON_LG}</button>
    <div class="vh-sheet-sub" id="vh-sheet-sub" hidden>
{sol_block}
    </div>
    <a href="/about">About</a>
  </div>
  <div class="vh-sheet-foot">
    <a href="/contact" class="vh-sheet-cta">Request a Demo</a>
  </div>
</div>"""


def footer_html() -> str:
    cols = []
    for head, links in FOOTER_COLS:
        rows = "\n".join(
            f'      <a href="{href}">{label}</a>' for href, label in links
        )
        cols.append(
            f'    <div class="fs-col">\n'
            f'      <div class="fs-head">{head}</div>\n'
            f"{rows}\n"
            f"    </div>"
        )
    return f"""<footer>
  <div class="footer-sitemap">
    <div class="fs-brand">
      <a href="/" class="footer-logo"><img src="/assets/logo-lockup-dark.svg" alt="Vasl Health" width="160" height="40"></a>
      <div class="footer-mission">Language is culture, not pathology.<br>Interpretation is care.<br>Delaware Public Benefit Corporation.</div>
      <a href="/contact" class="fs-cta">Request a Demo &rarr;</a>
    </div>
{chr(10).join(cols)}
  </div>
  <div class="footer-bottom">
    <div class="footer-copy">{COPYRIGHT}</div>
  </div>
</footer>"""


NAV_RE = re.compile(r"<nav>.*?</nav>", re.S)
SHEET_RE = re.compile(
    r'\n*<div class="vh-sheet" id="vh-sheet" hidden>.*?\n</div>', re.S
)
FOOTER_RE = re.compile(r"<footer[^>]*>.*?</footer>", re.S)
BLOCK_RE = re.compile(
    re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE) + r"\n?", re.S
)
# The per-page toggleNav() only ever drove the old fullscreen .nav-links menu,
# which the sheet replaces. Left in place it is dead code that still answers to
# an onclick this generator no longer writes.
TOGGLE_RE = re.compile(
    r"\n*  function toggleNav\(\) \{\n"
    r"    document\.querySelector\('\.nav-links'\)\.classList\.toggle\('open'\);\n"
    r"    document\.getElementById\('ham-btn'\)\.classList\.toggle\('open'\);\n"
    r"  \}\n",
    re.S,
)


def process(path: Path, rel: str):
    original = path.read_text(encoding="utf-8")
    html = BLOCK_RE.sub("", original)
    html = SHEET_RE.sub("", html)
    html = TOGGLE_RE.sub("\n", html)

    if not NAV_RE.search(html) or not FOOTER_RE.search(html):
        return False, None

    html = NAV_RE.sub(lambda m: header_html(rel), html, count=1)
    html = FOOTER_RE.sub(lambda m: footer_html(), html, count=1)

    block = f"{MARK_OPEN}\n{STYLE}\n{SCRIPT}\n{MARK_CLOSE}"
    html = html.replace("</body>", block + "\n</body>", 1)

    return html != original, html


def main() -> int:
    check = "--check" in sys.argv
    pending = []
    for path in sorted(SITE.rglob("*.html")):
        rel = path.relative_to(SITE).as_posix()
        if rel in SKIP:
            print(f"  skip  {rel}")
            continue
        changed, result = process(path, rel)
        if result is None:
            print(f"  skip  {rel}  (no <nav> or <footer> anchor)")
            continue
        if changed:
            pending.append((path, result))
            print(f"  {'would update' if check else 'update'}  {rel}  ({active_for(rel) or 'no active item'})")
        else:
            print(f"  ok    {rel}")

    if check:
        if pending:
            print(f"\n{len(pending)} page(s) out of date. Run: python3 tools/chrome_inject.py")
            return 1
        print("\nHeader and footer are current.")
        return 0

    for path, content in pending:
        path.write_text(content, encoding="utf-8")
    print(f"\nWrote {len(pending)} page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
