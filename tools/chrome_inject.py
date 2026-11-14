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

SKIP = IGNORE | {"404.html"}  # extended below with the ten generated pages

# November 2026: the header and footer are the same markup tools/build_pages.py
# writes on the ten main pages, so the blog and legal pages match them exactly.
# Styles live in /assets/chrome.css, scoped to nav.vx-nav and footer.vx-foot so
# they do not touch the older body styles on these pages.
from build_pages import header as _header, footer as _footer  # noqa: E402

from build_pages import PAGES as _PAGES  # noqa: E402

SKIP = SKIP | set(_PAGES)

STYLE = '<link rel="stylesheet" href="/assets/chrome.css">'
SCRIPT = ""


def active_for(rel: str) -> str:
    return ""


def header_html(rel: str) -> str:
    return _header(rel)


def footer_html() -> str:
    return _footer()


NAV_RE = re.compile(
    r'(?:<a class="vx-skip"[^\n]*\n)?<nav(?: class="vx-nav"[^>]*)?>.*?</nav>', re.S
)
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
