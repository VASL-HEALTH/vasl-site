"""Stale-claim sweep: billing. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/billing.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("Available for download from the Client Org Portal at the start", "Available for download at the start", 1),
    ("Structured, moderated peer group sessions with documented participation", "Structured, moderated group sessions with documented participation", 1),
    ("""        <div class="st-row">
          <div class="st-label">Peer group posts</div>
          <div class="st-value"><strong>Do not qualify.</strong> Unstructured peer community activity is not a billable service under any state Medicaid program.</div>
        </div>\n""", "", 1),
    ("""<div class="step-title">Log in to the Client Org Portal</div>""", """<div class="step-title">Open billing documentation</div>""", 1),
    ("Billing documentation is available to org administrators in the Client Org Portal. Go to", "Billing documentation is available to org administrators. Go to", 1),
    ("Vasl provides grant documentation, IRB study data, the VLAP", "Vasl provides grant documentation, the VLAP", 1),
    ("funding, including IRB study protocol, the VLAP model", "funding, including the VLAP model", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(n for _, n, _ in PAIRS) and "&mdash;" not in "".join(n for _, n, _ in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")

