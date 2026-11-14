"""infrastructure: stale-claim sweep. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/infrastructure.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # "therapy last" headline
    ("Therapy Last, <em>Not Therapy Never.</em>",
     "Early Support, <em>Full Spectrum of Care.</em>", 1),
    # Related reading: IRB claim
    ("The IRB validation process this infrastructure is built to support.",
     "The published results this infrastructure is built to support.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"infrastructure: {len(PAIRS)} pairs applied")
