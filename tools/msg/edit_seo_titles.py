"""seo_titles.py would put old youth/schools titles back on pages that now carry the new message.
Where a REWRITES entry no longer matches the live page, set that tag to None (leave the page alone)."""
import ast
import html
import re
from pathlib import Path

P = Path("tools/seo_titles.py")
src = P.read_text(encoding="utf-8")
lines = src.splitlines(keepends=True)
tree = ast.parse(src)
rewrites = next(n.value for n in tree.body
                if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "REWRITES")

edits = []
for k, v in zip(rewrites.keys, rewrites.values):
    rel = k.value
    t, d = ast.literal_eval(v)
    page = Path("site", rel)
    if not page.exists():
        continue
    h = page.read_text(encoding="utf-8")
    m_t = re.search(r"<title>(.*?)</title>", h, re.S)
    m_d = re.search(r'<meta name="description" content="(.*?)">', h, re.S)
    cur_t = html.unescape(m_t.group(1)) if m_t else None
    cur_d = html.unescape(m_d.group(1)) if m_d else None
    new_t = t if (t is None or t == cur_t) else None
    new_d = d if (d is None or d == cur_d) else None
    if (new_t, new_d) != (t, d):
        edits.append((v, rel, new_t, new_d))

for v, rel, new_t, new_d in sorted(edits, key=lambda e: e[0].lineno, reverse=True):
    start = sum(len(l) for l in lines[: v.lineno - 1]) + v.col_offset
    end = sum(len(l) for l in lines[: v.end_lineno - 1]) + v.end_col_offset
    src = src[:start] + f"({new_t!r}, {new_d!r})" + src[end:]
    lines = src.splitlines(keepends=True)
    print(f"{rel}: title {'kept' if new_t else 'left to page'}, description {'kept' if new_d else 'left to page'}")

ast.parse(src)
P.write_text(src, encoding="utf-8")
print(f"seo_titles: {len(edits)} entries neutralized")
