#!/usr/bin/env python3
"""
Inject a "related reading" block before </footer> on every page listed in
tools/link_map.py.

Idempotent, same pattern as seo_inject.py: everything we own lives inside
<!-- LINKS:VASL --> ... <!-- /LINKS:VASL -->, so re-running strips the old
block and writes a fresh one. The block carries its own small <style> using
only CSS custom properties already defined in every page's :root, so it
drops cleanly into any of the site's page templates without a shared
stylesheet or a build step.

Run:  python3 tools/internal_links.py            (writes)
      python3 tools/internal_links.py --check    (exits 1 if anything would change)
"""

import re
import sys
from pathlib import Path

from link_map import LINKS, HEADER_OVERRIDES

SITE = Path(__file__).resolve().parent.parent / "site"
MARK_OPEN = "<!-- LINKS:VASL -->"
MARK_CLOSE = "<!-- /LINKS:VASL -->"

STYLE = """<style>
.vrl-wrap{padding:70px var(--gutter);border-top:1px solid var(--chalk);background:var(--warm-white,var(--parchment));}
.vrl-head{font-family:var(--mono);font-size:10px;letter-spacing:0.16em;text-transform:uppercase;color:var(--clay);margin-bottom:36px;display:flex;align-items:center;gap:12px;}
.vrl-head::after{content:'';display:block;width:36px;height:1px;background:var(--clay);opacity:0.45;}
.vrl-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px 40px;}
.vrl-item{display:block;text-decoration:none;}
.vrl-item-title{font-family:var(--serif);font-size:18px;font-weight:400;color:var(--ink);margin-bottom:8px;line-height:1.3;letter-spacing:-0.01em;transition:color 0.2s;}
.vrl-item:hover .vrl-item-title{color:var(--clay);}
.vrl-item-desc{font-size:13px;font-weight:300;color:var(--ink-70);line-height:1.6;}
</style>"""


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def build_block(rel: str) -> str:
    edges = LINKS[rel]
    header = HEADER_OVERRIDES.get(rel, "Related Reading")
    base = Path(rel).parent

    items = []
    for target, anchor, desc in edges:
        href = target if base == Path(".") else "../" * len(base.parts) + target
        items.append(
            f'<a href="{href}" class="vrl-item">'
            f'<div class="vrl-item-title">{esc(anchor)}</div>'
            f'<div class="vrl-item-desc">{esc(desc)}</div>'
            f"</a>"
        )

    lines = [
        MARK_OPEN,
        STYLE,
        '<div class="vrl-wrap">',
        f'  <div class="vrl-head">{esc(header)}</div>',
        '  <div class="vrl-grid">',
        "    " + "\n    ".join(items),
        "  </div>",
        "</div>",
        MARK_CLOSE,
    ]
    return "\n".join(lines)


def strip_existing(html: str) -> str:
    return re.sub(
        re.escape(MARK_OPEN) + r".*?" + re.escape(MARK_CLOSE) + r"\n?",
        "",
        html,
        flags=re.S,
    )


FOOTER = re.compile(r"<footer[ >]")


def process(path: Path, rel: str) -> tuple:
    original = path.read_text(encoding="utf-8")
    html = strip_existing(original)
    block = build_block(rel)

    m = FOOTER.search(html)
    if not m:
        return False, None
    new = html[: m.start()] + block + "\n" + html[m.start() :]
    return new != original, new


def main() -> int:
    check = "--check" in sys.argv
    pending = []
    total_links = 0

    for rel in sorted(LINKS):
        path = SITE / rel
        if not path.exists():
            print(f"  skip  {rel}  (page does not exist yet)")
            continue
        changed, new = process(path, rel)
        total_links += len(LINKS[rel])
        if new is None:
            print(f"  skip  {rel}  (no <footer> anchor)")
            continue
        if changed:
            pending.append((path, new))
            print(f"  {'would update' if check else 'update'}  {rel}  ({len(LINKS[rel])} links)")
        else:
            print(f"  ok    {rel}  ({len(LINKS[rel])} links)")

    if check:
        if pending:
            print(f"\n{len(pending)} page(s) out of date. Run: python3 tools/internal_links.py")
            return 1
        print(f"\nInternal links are current. {total_links} managed link(s) across {len(LINKS)} page(s).")
        return 0

    for path, content in pending:
        path.write_text(content, encoding="utf-8")
    print(f"\nWrote {len(pending)} page(s). {total_links} managed link(s) across {len(LINKS)} page(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
