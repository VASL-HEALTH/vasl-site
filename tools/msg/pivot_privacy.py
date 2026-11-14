"""Privacy: meta copy only. FERPA/minors legal clauses in the body are left untouched. Exact pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/privacy.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # meta description, og:description, twitter:description
    ("how we collect, use, protect, and retain your information. HIPAA and FERPA compliant.\">",
     "how we collect, use, protect, and retain your information. HIPAA compliant.\">", 3),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(x[1] for x in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
