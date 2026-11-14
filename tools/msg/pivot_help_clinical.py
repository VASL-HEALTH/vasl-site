"""Help: clinical. Youth framing in dimension notes to patients/everyday speech. Exact pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/clinical.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("In AAVE and youth vernacular, these often appear through minimization",
     "In African American Language and other everyday speech, these often appear through minimization", 1),
    ("particularly significant for Black, Latino, and LGBTQ+ youth whose support networks",
     "particularly significant for Black, Latino, and LGBTQ+ patients whose support networks", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(x[1] for x in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
