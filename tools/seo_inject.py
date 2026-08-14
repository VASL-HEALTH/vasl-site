#!/usr/bin/env python3
"""
Inject the SEO head layer into site/*.html.

Idempotent: every block we own is wrapped in <!-- SEO:VASL --> ... <!-- /SEO:VASL -->.
Re-running strips the old block and writes a fresh one, so this is safe to run in
CI or by hand after any content edit.

Adds, per page:
  - rel=canonical on the pretty URL (kills the /about vs /about.html duplicate)
  - Open Graph + Twitter card (share previews in Slack, LinkedIn, iMessage)
  - meta robots (noindex on legal/utility pages)
  - a meta description where the page is missing one
  - JSON-LD: Organization + WebSite sitewide, BlogPosting on posts,
    BreadcrumbList on nested pages

Run:  python3 tools/seo_inject.py            (writes)
      python3 tools/seo_inject.py --check    (exits 1 if anything would change)
"""

import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
ORIGIN = "https://gotovasl.com"
OG_IMAGE = f"{ORIGIN}/og-image.png"
ORG_NAME = "Vasl Health"
MARK_OPEN = "<!-- SEO:VASL -->"
MARK_CLOSE = "<!-- /SEO:VASL -->"

# Pages that should stay out of the index: legal boilerplate, utility pages,
# and the prototype shell. They remain crawlable so link equity still flows.
NOINDEX = {
    "404.html",
    "terms.html",
    "privacy.html",
    "baa.html",
    "prototype.html",
}

# Descriptions for the pages that shipped without one. Written for the SERP:
# ~150 chars, buyer-facing, no diagnostic claims.
MISSING_DESC = {
    "ai-model.html": (
        "CulturalBERT is the language model behind Vasl — trained on how Black, Latino, "
        "and first-generation youth actually describe distress. Detection, not diagnosis."
    ),
    "platform.html": (
        "A five-layer behavioral health continuum for youth: peer community, daily check-ins, "
        "culturally matched coaching, licensed therapy, and crisis support in one system."
    ),
    "peer-groups.html": (
        "Moderated peer community groups where youth show up as themselves — the relationship "
        "that exists before a crisis does, staffed by facilitators from their own communities."
    ),
    "vlap.html": (
        "VLAP is Vasl's language analysis layer: 47 culturally specific distress signals across "
        "coded language, AAVE, and youth vernacular — surfaced to humans, never used to diagnose."
    ),
    "prototype.html": "Interactive prototype of the Vasl Health platform.",
    "404.html": "That page could not be found. Return to gotovasl.com.",
}

# Post -> ISO publish date, pulled from the bylines on each post.
POST_DATES = {
    "blog-healing-great-divide.html": "2026-05-01",
    "blog-mental-health-equity-crisis.html": "2026-04-20",
    "blog-bridging-chasm.html": "2026-04-01",
    "blog-medicaid-populations.html": "2026-03-01",
    "blog-future-culturally-responsive.html": "2026-02-01",
    "blog-crisis-without-solving.html": "2026-01-01",
    "blog-other-diagnosis.html": "2025-12-01",
}

HELP_LABELS = {
    "assessments.html": "Assessments",
    "billing.html": "Billing",
    "clinical.html": "Clinical",
    "compliance.html": "Compliance",
    "getting-started.html": "Getting Started",
    "technical.html": "Technical",
    "vlap-technology.html": "VLAP Technology",
}


def canonical_for(rel: str) -> str:
    """Pretty URL. The origin serves /about and /about.html identically, so we
    pick one and declare it — otherwise every page competes with its own twin."""
    if rel == "index.html":
        return f"{ORIGIN}/"
    return f"{ORIGIN}/{rel[:-len('.html')]}"


def head_of(html: str) -> str:
    end = html.find("</head>")
    return html[:end] if end != -1 else html[:8000]


def strip_existing(html: str) -> str:
    return re.sub(
        re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE) + r"\n?",
        "",
        html,
        flags=re.S,
    )


def get_title(html: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    t = m.group(1).strip() if m else ORG_NAME
    return t.replace("&mdash;", "—").replace("&amp;", "&")


def get_desc(html: str, rel: str) -> str:
    m = re.search(
        r'name=["\']description["\'][^>]*content=["\'](.*?)["\']', head_of(html), re.S | re.I
    )
    if m:
        return m.group(1).strip()
    return MISSING_DESC.get(rel, "")


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def jsonld_blocks(rel: str, title: str, desc: str, canonical: str) -> list:
    blocks = []

    if rel == "index.html":
        blocks.append(
            {
                "@context": "https://schema.org",
                "@type": "Organization",
                "@id": f"{ORIGIN}/#organization",
                "name": ORG_NAME,
                "url": f"{ORIGIN}/",
                "logo": f"{ORIGIN}/apple-touch-icon.png",
                "description": (
                    "Vasl Health builds culturally grounded, clinically governed early "
                    "detection and behavioral health support for Black, Latino, and "
                    "first-generation youth ages 14–24."
                ),
                "email": "hello@vaslhealth.com",
                "foundingLocation": {
                    "@type": "Place",
                    "address": {"@type": "PostalAddress", "addressCountry": "US"},
                },
                "contactPoint": [
                    {
                        "@type": "ContactPoint",
                        "contactType": "sales",
                        "email": "hello@vaslhealth.com",
                        "areaServed": "US",
                        "availableLanguage": ["en", "es"],
                    },
                    {
                        "@type": "ContactPoint",
                        "contactType": "media relations",
                        "email": "press@vaslhealth.com",
                        "areaServed": "US",
                    },
                    {
                        "@type": "ContactPoint",
                        "contactType": "research",
                        "email": "research@vaslhealth.com",
                        "areaServed": "US",
                    },
                ],
                "knowsAbout": [
                    "culturally responsive behavioral health",
                    "youth mental health",
                    "school-based mental health",
                    "behavioral health equity",
                    "natural language processing in mental health",
                ],
            }
        )
        blocks.append(
            {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "@id": f"{ORIGIN}/#website",
                "url": f"{ORIGIN}/",
                "name": ORG_NAME,
                "publisher": {"@id": f"{ORIGIN}/#organization"},
            }
        )

    if rel in POST_DATES:
        blocks.append(
            {
                "@context": "https://schema.org",
                "@type": "BlogPosting",
                "headline": title.split(" — ")[0],
                "description": desc,
                "datePublished": POST_DATES[rel],
                "dateModified": POST_DATES[rel],
                "author": {"@type": "Person", "name": "Rodney Bell"},
                "publisher": {"@id": f"{ORIGIN}/#organization"},
                "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
                "image": OG_IMAGE,
                "isPartOf": {"@type": "Blog", "@id": f"{ORIGIN}/blog"},
            }
        )
        blocks.append(
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{ORIGIN}/"},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Insights & Research",
                        "item": f"{ORIGIN}/blog",
                    },
                    {"@type": "ListItem", "position": 3, "name": title.split(" — ")[0]},
                ],
            }
        )

    if rel.startswith("help/"):
        leaf = rel.split("/", 1)[1]
        blocks.append(
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{ORIGIN}/"},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Support",
                        "item": f"{ORIGIN}/support",
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": HELP_LABELS.get(leaf, leaf),
                    },
                ],
            }
        )

    return blocks


def build_block(rel: str, html: str) -> str:
    canonical = canonical_for(rel)
    title = get_title(html)
    desc = get_desc(html, rel)
    noindex = rel in NOINDEX
    og_type = "article" if rel in POST_DATES else "website"

    lines = [MARK_OPEN]
    lines.append(f'<link rel="canonical" href="{canonical}">')

    if noindex:
        lines.append('<meta name="robots" content="noindex,follow">')
    else:
        lines.append(
            '<meta name="robots" content="index,follow,max-image-preview:large,'
            'max-snippet:-1,max-video-preview:-1">'
        )

    # Only emit a description if the page lacked one; otherwise we would ship a duplicate tag.
    has_desc = bool(
        re.search(r'name=["\']description["\']', head_of(html), re.I)
    )
    if not has_desc and desc:
        lines.append(f'<meta name="description" content="{esc(desc)}">')

    lines.append(f'<meta property="og:type" content="{og_type}">')
    lines.append(f'<meta property="og:site_name" content="{ORG_NAME}">')
    lines.append(f'<meta property="og:title" content="{esc(title)}">')
    if desc:
        lines.append(f'<meta property="og:description" content="{esc(desc)}">')
    lines.append(f'<meta property="og:url" content="{canonical}">')
    lines.append(f'<meta property="og:image" content="{OG_IMAGE}">')
    lines.append('<meta property="og:image:width" content="1200">')
    lines.append('<meta property="og:image:height" content="630">')
    lines.append(f'<meta property="og:image:alt" content="Vasl Health — Language Is Care">')
    lines.append('<meta property="og:locale" content="en_US">')

    if rel in POST_DATES:
        lines.append(
            f'<meta property="article:published_time" content="{POST_DATES[rel]}">'
        )
        lines.append('<meta property="article:author" content="Rodney Bell">')

    lines.append('<meta name="twitter:card" content="summary_large_image">')
    lines.append(f'<meta name="twitter:title" content="{esc(title)}">')
    if desc:
        lines.append(f'<meta name="twitter:description" content="{esc(desc)}">')
    lines.append(f'<meta name="twitter:image" content="{OG_IMAGE}">')

    for b in jsonld_blocks(rel, title, desc, canonical):
        lines.append(
            '<script type="application/ld+json">'
            + json.dumps(b, ensure_ascii=False, separators=(",", ":"))
            + "</script>"
        )

    lines.append(MARK_CLOSE)
    return "\n".join(lines)


ANCHOR = re.compile(r'(<link rel="apple-touch-icon"[^>]*>)')


def process(path: Path) -> tuple:
    rel = path.relative_to(SITE).as_posix()
    original = path.read_text(encoding="utf-8")
    html = strip_existing(original)
    block = build_block(rel, html)

    if ANCHOR.search(html):
        new = ANCHOR.sub(lambda m: m.group(1) + "\n" + block, html, count=1)
    elif "</head>" in html:
        new = html.replace("</head>", block + "\n</head>", 1)
    else:
        # No place to put the block. Return None for content so main() can tell
        # this apart from "unchanged" — returning the reason as a string here
        # made main() print the entire file as the skip reason.
        return rel, False, None

    changed = new != original
    return rel, changed, new


def main() -> int:
    check = "--check" in sys.argv
    pending = []
    for path in sorted(SITE.rglob("*.html")):
        rel, changed, result = process(path)
        if result is None:
            print(f"  skip  {rel}  (no <head> anchor)")
            continue
        if changed:
            pending.append((path, result))
            print(f"  {'would update' if check else 'update'}  {rel}")
        else:
            print(f"  ok    {rel}")

    if check:
        if pending:
            print(f"\n{len(pending)} page(s) out of date. Run: python3 tools/seo_inject.py")
            return 1
        print("\nSEO head layer is current.")
        return 0

    for path, content in pending:
        path.write_text(content, encoding="utf-8")
    print(f"\nWrote {len(pending)} page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
