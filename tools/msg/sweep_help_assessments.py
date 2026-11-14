"""Stale-claim sweep: assessments. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/assessments.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("Your coach and peer community are particularly well-suited", "Your coach is particularly well-suited", 1),
    ("Peer support, coaching, and practical coping strategies are", "Coaching and practical coping strategies are", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(n for _, n, _ in PAIRS) and "&mdash;" not in "".join(n for _, n, _ in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")

