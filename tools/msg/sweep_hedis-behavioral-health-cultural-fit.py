"""hedis-behavioral-health-cultural-fit: stale-claim sweep. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/hedis-behavioral-health-cultural-fit.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # peer community as a Vasl offering
    ("the mechanism is peer community and coaching that starts",
     "the mechanism is coaching that starts", 1),
    ("matched with a coach or peer community from the same",
     "matched with a coach from the same", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"hedis-behavioral-health-cultural-fit: {len(PAIRS)} pairs applied")
