#!/usr/bin/env python3
"""
Generate site/sitemap.xml from the pages that are actually indexable.

Source of truth is the page itself: anything carrying <meta name="robots"
content="noindex..."> is excluded, so the sitemap can never disagree with the
directive on the page. Priorities are set by page role, not guessed per-page.

Run:  python3 tools/gen_sitemap.py
      python3 tools/gen_sitemap.py --check   (exits 1 if stale)
"""

import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
ORIGIN = "https://gotovasl.com"
OUT = SITE / "sitemap.xml"

# Priority by role. Buyer-path pages outrank support and legal pages, which is
# the only signal priority actually carries.
PRIORITY = {
    "index.html": ("1.0", "weekly"),
    "for-schools.html": ("0.9", "monthly"),
    "health-systems.html": ("0.9", "monthly"),
    "for-organizations.html": ("0.9", "monthly"),
    "platform.html": ("0.9", "monthly"),
    "outcomes.html": ("0.9", "monthly"),
    "pricing.html": ("0.9", "monthly"),
    "vlap.html": ("0.9", "monthly"),
    "ai-model.html": ("0.8", "monthly"),
    "technology.html": ("0.8", "monthly"),
    "clinical-outcomes.html": ("0.8", "monthly"),
    "research.html": ("0.8", "monthly"),
    "about.html": ("0.8", "monthly"),
    "blog.html": ("0.8", "weekly"),
    "contact.html": ("0.7", "yearly"),
    "team.html": ("0.7", "monthly"),
    "teletherapy.html": ("0.7", "monthly"),
    "peer-groups.html": ("0.7", "monthly"),
    "for-families.html": ("0.7", "monthly"),
    "careers.html": ("0.6", "weekly"),
    "infrastructure.html": ("0.6", "monthly"),
    "support.html": ("0.5", "monthly"),
    "accessibility.html": ("0.3", "yearly"),
}
DEFAULT_BLOG = ("0.7", "yearly")
DEFAULT_HELP = ("0.5", "monthly")
DEFAULT = ("0.5", "monthly")


def canonical_for(rel: str) -> str:
    if rel == "index.html":
        return f"{ORIGIN}/"
    return f"{ORIGIN}/{rel[:-len('.html')]}"


def git_lastmod(path: Path) -> str:
    """Last commit date for the file. Falls back to today for untracked files."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path.relative_to(ROOT))],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", out):
            return out
    except Exception:
        pass
    return date.today().isoformat()


def build() -> str:
    rows = []
    for path in sorted(SITE.rglob("*.html")):
        rel = str(path.relative_to(SITE))
        html = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', html, re.I):
            continue
        if rel.startswith("blog-"):
            prio, freq = DEFAULT_BLOG
        elif rel.startswith("help/"):
            prio, freq = DEFAULT_HELP
        else:
            prio, freq = PRIORITY.get(rel, DEFAULT)
        rows.append((canonical_for(rel), git_lastmod(path), freq, prio))

    # Highest priority first — purely for human readability of the file.
    rows.sort(key=lambda r: (-float(r[3]), r[0]))

    body = "\n".join(
        f"  <url>\n"
        f"    <loc>{loc}</loc>\n"
        f"    <lastmod>{mod}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n"
        f"    <priority>{prio}</priority>\n"
        f"  </url>"
        for loc, mod, freq, prio in rows
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )


def main() -> int:
    new = build()
    check = "--check" in sys.argv
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    n = new.count("<url>")
    if check:
        if old != new:
            print("sitemap.xml is stale. Run: python3 tools/gen_sitemap.py")
            return 1
        print(f"sitemap.xml is current ({n} URLs).")
        return 0
    OUT.write_text(new, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} — {n} URLs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
