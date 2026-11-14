"""Stale-claim sweep: technical. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/technical.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("for the Vasl Health platform, Member App, Coach Portal, and Client Org Portal.", "for the Vasl Health platform and the clinician&rsquo;s workflow.", 3),
    ("The Member App, Coach Portal, Client Org Portal, and Super Admin Dashboard all run in the browser.", "Every part of the Vasl platform runs in the browser.", 1),
    ("The Member App is optimized for mobile and provides the best experience on a current-generation smartphone. Coach Portal and Client Org Portal are primarily designed for desktop",
     "Member access is optimized for mobile and provides the best experience on a current-generation smartphone. The clinician&rsquo;s workflow and organization reporting are primarily designed for desktop", 1),
    ("Landscape orientation recommended for Coach Portal and Org Portal use.", "Landscape orientation recommended for clinician and organization use.", 1),
    ("Member App: 375px minimum width. Coach Portal and Org Portal: 768px", "Member access: 375px minimum width. Clinician and organization views: 768px", 1),
    ("including check-ins, messaging, and peer groups.", "including check-ins and messaging.", 1),
    ("smooth loading of the Coach Portal dashboard with", "smooth loading of the clinician&rsquo;s workflow with", 1),
    ("""<div class="portal-col-label">Member App</div>""", """<div class="portal-col-label">Member access</div>""", 1),
    ("""<div class="portal-col-label">Coach Portal</div>""", """<div class="portal-col-label">Clinician&rsquo;s workflow</div>""", 1),
    ("""<div class="portal-col-label">Client Org Portal</div>""", """<div class="portal-col-label">Organization reporting</div>""", 1),
    ("A high contrast mode toggle is available in Member App settings.", "A high contrast mode toggle is available in member settings.", 1),
    ("VLAP signal panel not loading in Coach Portal", "VLAP signal panel not loading in the clinician&rsquo;s workflow", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(n for _, n, _ in PAIRS) and "&mdash;" not in "".join(n for _, n, _ in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")

