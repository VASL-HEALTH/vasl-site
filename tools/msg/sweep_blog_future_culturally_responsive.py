"""Blog stale-claim sweep: site/blog-future-culturally-responsive.html. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/blog-future-culturally-responsive.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("The 2,400+ AAVE and youth vernacular tokens in Vasl&rsquo;s vocabulary extension were gathered",
     "The AAVE and youth vernacular in Vasl&rsquo;s community-annotated language library was gathered", 1),
    ('<div class="as-stat-num">2,400+</div><div class="as-stat-label">AAVE and youth vernacular tokens added to VLAP through community-partnered vocabulary development</div>',
     '<div class="as-stat-num">55</div><div class="as-stat-label">VLAP signals across seven dimensions, read against a community-annotated language library</div>', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(p[1] for p in PAIRS) and "&mdash;" not in "".join(p[1] for p in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
