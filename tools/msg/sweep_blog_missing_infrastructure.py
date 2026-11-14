"""Blog stale-claim sweep: site/blog-missing-infrastructure.html. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/blog-missing-infrastructure.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("VLAP&rsquo;s 47 signals across 6 categories,", "VLAP&rsquo;s 55 signals across seven dimensions,", 1),
    ('<div class="as-stat-num">47 / 6</div><div class="as-stat-label">VLAP signals mapped across clinical categories, annotated against the AAL corpus</div><div class="as-stat-caveat">Vasl taxonomy v1.0</div>',
     '<div class="as-stat-num">55 / 7</div><div class="as-stat-label">VLAP signals across seven dimensions</div><div class="as-stat-caveat">Vasl taxonomy v2.0</div>', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(p[1] for p in PAIRS) and "&mdash;" not in "".join(p[1] for p in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
