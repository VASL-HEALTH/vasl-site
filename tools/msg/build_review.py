"""Build one self-contained review HTML: every listed page in an iframe, local /assets inlined."""
import base64
import html
import mimetypes
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parents[2] / "site"
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/claude/review/old_site_review.html")
PAGES = [
    ("index", "Home"), ("platform", "Platform"), ("vlap", "VLAP"),
    ("health-systems", "Health Plans & Systems"), ("bridge", "Vasl Bridge"), ("keep", "Vasl Keep"),
    ("technology", "Technology"), ("research", "Research"), ("team", "Team"),
    ("about", "About"), ("contact", "Contact"), ("blog", "Blog"),
]
ASSET = re.compile(r"""(?P<pre>(?:src|href|poster)=["']|url\(["']?)(?P<path>/?assets/[^"')\s?#]+)""")
SRCSET = re.compile(r'srcset="([^"]*)"')
cache: dict[str, str] = {}
missing: set[str] = set()


def data_uri(path: str) -> str | None:
    if path in cache:
        return cache[path]
    f = SITE / path.lstrip("/")
    if not f.is_file():
        missing.add(path)
        return None
    mime = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
    if f.suffix == ".svg":
        mime = "image/svg+xml"
    cache[path] = f"data:{mime};base64,{base64.b64encode(f.read_bytes()).decode()}"
    return cache[path]


def inline(doc: str) -> str:
    def sub(m):
        uri = data_uri(m.group("path"))
        return m.group("pre") + (uri or m.group("path"))

    def subset(m):
        parts = []
        for item in m.group(1).split(","):
            bits = item.strip().split(None, 1)
            if bits and re.match(r"/?assets/", bits[0]):
                bits[0] = data_uri(bits[0]) or bits[0]
            parts.append(" ".join(bits))
        return 'srcset="' + ", ".join(parts) + '"'

    return ASSET.sub(sub, SRCSET.sub(subset, doc))


nav = "".join(f'<a href="#{slug}">{html.escape(label)}</a>' for slug, label in PAGES)
sections = []
for slug, label in PAGES:
    doc = inline((SITE / f"{slug}.html").read_text(encoding="utf-8"))
    sections.append(
        f'<section id="{slug}" class="pg"><div class="lbl">{html.escape(label)} &middot; '
        f'<a href="#top">back to top</a></div><iframe title="{html.escape(label)}" loading="lazy" '
        f'srcdoc="{html.escape(doc, quote=True)}"></iframe></section>'
    )

head = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>gotovasl.com, your site with the new message</title>
<style>body{margin:0;font:14px/1.4 system-ui,sans-serif;background:#222;}
.bar{position:sticky;top:0;z-index:5;display:flex;gap:4px;overflow-x:auto;padding:8px 10px;background:#13201b;}
.bar a{color:#cfe0d8;text-decoration:none;padding:6px 10px;border-radius:6px;white-space:nowrap;}
.bar a:hover{background:#2d5f4f;color:#fff;}
.pg{scroll-margin-top:52px;}
.lbl{color:#fff;padding:10px 16px;background:#2d5f4f;} .lbl a{color:#d4a574;}
iframe{display:block;width:100%;height:92vh;border:0;background:#fff;}</style></head>
"""
out = head + f'<body id="top"><nav class="bar">{nav}</nav>' + "".join(sections) + "</body></html>"
out = out.replace("�", "&#xFFFD;")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(out, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB); missing assets: {sorted(missing) or 'none'}")
