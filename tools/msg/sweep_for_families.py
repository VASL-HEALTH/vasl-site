"""for-families: stale-claim sweep (claims only). Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/for-families.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # peer groups as a Vasl offering
    ("Only what members share on Vasl, their check-ins, messages in peer groups, and conversations with their coach.",
     "Only what members share on Vasl, their check-ins and conversations with their coach.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"for-families: {len(PAIRS)} pairs applied")
