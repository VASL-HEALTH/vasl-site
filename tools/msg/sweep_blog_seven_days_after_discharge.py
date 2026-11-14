"""Blog stale-claim sweep: site/blog-seven-days-after-discharge.html. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/blog-seven-days-after-discharge.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("a taxonomy of 47 clinical signals across six categories,", "a taxonomy of 55 signals across seven dimensions,", 1),
    ("Their mood map and their peer community open in the phone&rsquo;s browser,",
     "Their mood map opens in the phone&rsquo;s browser,", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(p[1] for p in PAIRS) and "&mdash;" not in "".join(p[1] for p in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
