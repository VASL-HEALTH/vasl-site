#!/usr/bin/env python3
"""
Assert the SEO invariants that actually cost traffic when they break.

This is not a lint. Each check below maps to a specific, known failure mode:

  1. Every indexable page has exactly one canonical, pointing at its own pretty
     URL. Two canonicals, or a canonical pointing elsewhere, deindexes the page.
  2. Exactly one <title> and one meta description per page. Duplicates make
     Google pick one at random.
  3. Title length 15-65 chars, description 70-165. Outside that range the SERP
     truncates or Google rewrites the snippet itself.
  4. Exactly one <h1>. Zero means no topical anchor; more than one splits it.
  5. No two indexable pages share a title or a description — that is the
     signature of cannibalization.
  6. All JSON-LD parses. A malformed block is silently discarded, which is worse
     than having none because it looks done.
  7. Every sitemap URL resolves to a real file, and every indexable file is in
     the sitemap.
  8. No internal link points at a URL the sitemap says does not exist.

Run: python3 tools/seo_validate.py
"""

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from seo_shared import IGNORE

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
ORIGIN = "https://gotovasl.com"

TITLE_MIN, TITLE_MAX = 15, 65
DESC_MIN, DESC_MAX = 70, 165

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def canonical_for(rel: str) -> str:
    if rel == "index.html":
        return f"{ORIGIN}/"
    return f"{ORIGIN}/{rel[:-len('.html')]}"


def unescape(s: str) -> str:
    return (
        s.replace("&mdash;", "—")
        .replace("&amp;", "&")
        .replace("&nbsp;", " ")
        .replace("&quot;", '"')
        .replace("&middot;", "·")
    )


def head_of(html: str) -> str:
    end = html.find("</head>")
    return html[:end] if end != -1 else html[:8000]


pages = {}
for path in sorted(SITE.rglob("*.html")):
    rel = path.relative_to(SITE).as_posix()
    if rel in IGNORE:
        continue
    pages[rel] = path.read_text(encoding="utf-8", errors="ignore")

titles = defaultdict(list)
descs = defaultdict(list)
indexable = []

for rel, html in pages.items():
    head = head_of(html)
    noindex = bool(
        re.search(r'name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', head, re.I)
    )
    if not noindex:
        indexable.append(rel)

    # 1. canonical
    canons = re.findall(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', head, re.I)
    if len(canons) == 0:
        err(f"{rel}: no canonical")
    elif len(canons) > 1:
        err(f"{rel}: {len(canons)} canonicals ({canons})")
    elif canons[0] != canonical_for(rel):
        err(f"{rel}: canonical is {canons[0]}, expected {canonical_for(rel)}")

    # 2 + 3. title
    ts = re.findall(r"<title>(.*?)</title>", head, re.S)
    if len(ts) != 1:
        err(f"{rel}: {len(ts)} <title> tags, expected 1")
    else:
        t = unescape(ts[0].strip())
        if not (TITLE_MIN <= len(t) <= TITLE_MAX):
            warn(f"{rel}: title is {len(t)} chars (want {TITLE_MIN}-{TITLE_MAX}) — {t!r}")
        if not noindex:
            titles[t].append(rel)

    # Backreference the quote char — an apostrophe inside the copy ("Vasl's")
    # silently truncates a naive ["\'] alternation and fakes a length failure.
    ds = re.findall(
        r'<meta[^>]+name=(["\'])description\1[^>]*content=(["\'])(.*?)\2',
        head,
        re.S | re.I,
    )
    if len(ds) == 0:
        err(f"{rel}: no meta description")
    elif len(ds) > 1:
        err(f"{rel}: {len(ds)} meta descriptions")
    else:
        dtext = unescape(ds[0][2].strip())
        if not (DESC_MIN <= len(dtext) <= DESC_MAX):
            warn(f"{rel}: description is {len(dtext)} chars (want {DESC_MIN}-{DESC_MAX})")
        if not noindex:
            descs[dtext].append(rel)

    # 4. h1
    h1s = re.findall(r"<h1[\s>]", html, re.I)
    if len(h1s) != 1 and not noindex:
        err(f"{rel}: {len(h1s)} <h1> tags, expected 1")

    # og essentials
    for prop in ("og:title", "og:description", "og:url", "og:image"):
        if f'property="{prop}"' not in head:
            err(f"{rel}: missing {prop}")

    # 6. JSON-LD parses
    for i, block in enumerate(
        re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    ):
        try:
            json.loads(block)
        except json.JSONDecodeError as e:
            err(f"{rel}: JSON-LD block {i} does not parse — {e}")

# 5. cannibalization
for t, rels in titles.items():
    if len(rels) > 1:
        err(f"duplicate title across {rels}: {t!r}")
for d, rels in descs.items():
    if len(rels) > 1:
        err(f"duplicate description across {rels}")

# 7. sitemap <-> filesystem
sm_path = SITE / "sitemap.xml"
if not sm_path.exists():
    err("site/sitemap.xml is missing")
else:
    locs = set(re.findall(r"<loc>(.*?)</loc>", sm_path.read_text(encoding="utf-8")))
    expected = {canonical_for(r) for r in indexable}
    for extra in sorted(locs - expected):
        err(f"sitemap lists {extra} but no indexable page produces it")
    for missing in sorted(expected - locs):
        err(f"indexable page missing from sitemap: {missing}")

if not (SITE / "robots.txt").exists():
    err("site/robots.txt is missing")
elif "Sitemap: " not in (SITE / "robots.txt").read_text(encoding="utf-8"):
    err("robots.txt does not reference the sitemap")

if not (SITE / "og-image.png").exists():
    err("site/og-image.png is missing — every share preview will render blank")

# 8. internal links resolve
for rel, html in pages.items():
    base = Path(rel).parent
    for href in re.findall(r'href=["\']([^"\'#?]+)["\']', html):
        if href.startswith(("http", "mailto:", "tel:", "//", "javascript:")):
            continue
        target = href.lstrip("/")
        cand = (SITE / target) if href.startswith("/") else (SITE / base / target)
        if cand.suffix == "":
            cand = cand.with_suffix(".html")
        if not cand.exists() and not (cand.is_dir()):
            warn(f"{rel}: internal link to {href!r} does not resolve")

print(f"Checked {len(pages)} pages ({len(indexable)} indexable).\n")
for w in warnings:
    print(f"  warn   {w}")
if warnings:
    print()
for e in errors:
    print(f"  ERROR  {e}")

if errors:
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s). Failing.")
    sys.exit(1)
print(f"All invariants hold. {len(warnings)} warning(s).")
