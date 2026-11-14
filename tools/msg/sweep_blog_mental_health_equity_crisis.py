"""Blog stale-claim sweep: site/blog-mental-health-equity-crisis.html. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/blog-mental-health-equity-crisis.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("The vocabulary extension, 2,400+ AAVE and youth vernacular tokens, was community-sourced",
     "The language library, community-annotated AAVE and youth vernacular, was community-sourced", 1),
    ("On Vasl, peer community and a coach are there from the day a member is enrolled.",
     "On Vasl, a coach is there from the day a member is enrolled.", 1),
    ("culturally matched human coaches, peer community, and clinical coordination.",
     "culturally matched human coaches and clinical coordination.", 1),
    ('<div class="as-stat-num">23 of 47</div><div class="as-stat-label">VLAP signals with no counterpart in the lexicon&rsquo;s 6,910 terms</div><div class="as-stat-caveat">Measured</div>',
     '<div class="as-stat-num">55</div><div class="as-stat-label">VLAP signals across seven dimensions, Taxonomy v2.0</div><div class="as-stat-caveat">Measured</div>', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(p[1] for p in PAIRS) and "&mdash;" not in "".join(p[1] for p in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
