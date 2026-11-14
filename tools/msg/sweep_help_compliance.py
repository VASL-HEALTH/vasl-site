"""Stale-claim sweep: compliance. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/compliance.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("""        <div class="dt-row">
          <div class="dtc">Peer group posts</div>
          <div class="dtc">Posts and replies you make in peer groups</div>
          <div class="dtc"><span class="dtc-stored">Yes</span></div>
        </div>\n""", "", 1),
    ("""        <div class="at-row">
          <div class="atc">Peer group posts</div>
          <div class="atc"><span class="atc-own">Groups you joined</span></div>
          <div class="atc"><span class="atc-no">Not visible</span></div>
          <div class="atc"><span class="atc-no">Not visible</span></div>
          <div class="atc"><span class="atc-no">Never</span></div>
        </div>\n""", "", 1),
    ("make clinical decisions, initiate contact, or scan peer groups.", "make clinical decisions, or initiate contact.", 1),
    ("""        <div class="st-row">
          <div class="st-label">Peer groups</div>
          <div class="st-value"><strong>VLAP does not process peer group posts.</strong> Peer group content is not scanned by any AI system. Human moderators oversee peer groups.</div>
        </div>\n""", "", 1),
    ("""<div class="st-label">Security certifications</div>
          <div class="st-value">SOC 2 Type II, annual third-party security audit covering security, availability, and confidentiality. Full report available under NDA to partner organizations upon request.</div>""",
     """<div class="st-label">Security</div>
          <div class="st-value">HIPAA, BAA. Compliance documentation available under NDA to partner organizations upon request.</div>""", 1),
    ("BAA template, SOC 2 report (under NDA), compliance documentation", "BAA template, compliance documentation (under NDA)", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(n for _, n, _ in PAIRS) and "&mdash;" not in "".join(n for _, n, _ in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")

