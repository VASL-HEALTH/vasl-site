"""BAA page claims sweep: company name only. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/baa.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("<strong>Vasl Health, Inc.</strong>, a Delaware Public Benefit Corporation (",
     "<strong>Vasl Health PBC</strong>, a Delaware Public Benefit Corporation (", 1),
    ('<p class="doc-p">Vasl Health, Inc., acting in its capacity as a Business Associate',
     '<p class="doc-p">Vasl Health PBC, acting in its capacity as a Business Associate', 1),
    ("services provided by Vasl Health, Inc. to Covered Entity",
     "services provided by Vasl Health PBC to Covered Entity", 1),
    ("<strong>Vasl Health, Inc.</strong><br>A Delaware Public Benefit Corporation",
     "<strong>Vasl Health PBC</strong><br>A Delaware Public Benefit Corporation", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
