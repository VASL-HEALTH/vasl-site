"""Terms page claims sweep: company name, Member App / peer community. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/terms.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("legally binding agreement between you and Vasl Health, Inc. (",
     "legally binding agreement between you and Vasl Health PBC (", 1),
    ('<li class="doc-li">Member App providing peer community, daily check-ins, culturally matched coaching, and crisis resources</li>',
     '<li class="doc-li">Member services providing daily check-ins, culturally matched coaching, and crisis resources</li>', 1),
    ("Vasl Health, Inc. is a Delaware Public Benefit Corporation.",
     "Vasl Health PBC is a Delaware Public Benefit Corporation.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
