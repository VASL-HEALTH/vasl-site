import sys
from pathlib import Path

P = Path("site/blog-future-culturally-responsive.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ('in Black and Latino youth when applied', 'in Black and Latino patients when applied', 1),
    ('Black and Latino youth', 'Black and Latino communities', 3),
    ('The AAVE and youth vernacular in', 'The AAVE and everyday speech in', 1),
    ('engagement with youth from the communities', 'engagement with people from the communities', 1),
    ('When young people feel that', 'When patients feel that', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
joined = "".join(p[1] for p in PAIRS)
assert "—" not in joined and "&mdash;" not in joined and "&#8212;" not in joined
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
