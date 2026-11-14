"""Stale-claim sweep: clinical. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/clinical.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("applying VLAP signal context in the Coach Portal, before", "applying VLAP signal context in the clinician&rsquo;s workflow, before", 1),
    ("From any page in the Coach Portal, go to My Dashboard", "From any page in the clinician&rsquo;s workflow, go to My Dashboard", 1),
    ("over 7 days. Active in peer group. No action indicated.", "over 7 days. No action indicated.", 1),
    ("your pre-session view in the Coach Portal includes", "your pre-session view in the clinician&rsquo;s workflow includes", 1),
    ("Here's a reference for all six categories and what each covers clinically.",
     "VLAP flags 55 signals across seven dimensions. Here's a reference for the core categories and what each covers clinically.", 1),
    ("The full taxonomy with all 47 signal definitions,", "The full taxonomy with all 55 signal definitions,", 1),
    ("These are surfaced in the Member App at all times,", "These are surfaced to members at all times,", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(n for _, n, _ in PAIRS) and "&mdash;" not in "".join(n for _, n, _ in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")

