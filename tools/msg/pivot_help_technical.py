"""Help: technical. School network/device framing to work and clinic. Exact pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/technical.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ('<div class="st-label">School networks</div>',
     '<div class="st-label">Work and clinic networks</div>', 1),
    ("should be whitelisted on school content filters.",
     "should be whitelisted on organization content filters.", 1),
    ("If using a school device, confirm the domain isn't blocked",
     "If using a work or clinic device, confirm the domain isn't blocked", 1),
    ('<div class="tr-problem">Platform blocked on school network</div>',
     '<div class="tr-problem">Platform blocked on a work or clinic network</div>', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(x[1] for x in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
