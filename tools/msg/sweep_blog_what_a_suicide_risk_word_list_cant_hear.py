"""Blog stale-claim sweep: site/blog/what-a-suicide-risk-word-list-cant-hear.html. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/blog/what-a-suicide-risk-word-list-cant-hear.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("screener free text, check-ins and peer messages.", "screener free text, check-ins and text replies.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(p[1] for p in PAIRS) and "&mdash;" not in "".join(p[1] for p in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
