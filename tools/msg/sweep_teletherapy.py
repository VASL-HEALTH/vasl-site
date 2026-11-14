"""Stale-claim sweep: teletherapy. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/teletherapy.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("Chapter 01, Therapy Last. Not Therapy Never.", "Chapter 01, Clinical Care When Ready.", 1),
    ("on day one, before you've found community, before anyone knows", "on day one, before anyone knows", 1),
    ("""      <div class="cs-item">
        <div class="cs-dot">01</div>
        <div class="cs-right">
          <div class="cs-stage">First Step</div>
          <div class="cs-name">Peer Community</div>
          <p class="cs-desc">70+ groups organized around shared identity and lived experience. Recognition before intervention. Community before clinical care. Available same day, no waitlist, no intake.</p>
          <span class="cs-tag immediate">Same day</span>
        </div>
      </div>

      <div class="cs-item">
        <div class="cs-dot">02</div>
        <div class="cs-right">
          <div class="cs-stage">Second Step</div>""",
     """      <div class="cs-item">
        <div class="cs-dot">01</div>
        <div class="cs-right">
          <div class="cs-stage">First Step</div>""", 1),
    ("""        <div class="cs-dot">03</div>
        <div class="cs-right">
          <div class="cs-stage">Third Step, When Ready</div>""",
     """        <div class="cs-dot">02</div>
        <div class="cs-right">
          <div class="cs-stage">Second Step, When Ready</div>""", 1),
    ("arrives in the clinician's Coach Portal view in the 24 hours", "arrives in the clinician's workflow in the 24 hours", 1),
    ("Check-in patterns, peer group activity, and communication cadence.", "Check-in patterns and communication cadence.", 1),
    ("coach message cadence, peer group activity, and the pattern", "coach message cadence, and the pattern", 1),
    ("within the same ecosystem as their peer community and coaching.", "within the same ecosystem as their coaching.", 1),
    ("The Vasl Member App keeps the member's peer and coaching relationships active throughout.", "Vasl keeps the member's coaching relationship active throughout.", 1),
    ("coaching context: Vasl Coach Portal, clinician-facing only.", "coaching context: the clinician's workflow, clinician-facing only.", 1),
    ("the connection from peer support and coaching to clinical care", "the connection from coaching to clinical care", 1),
    ("escalation from peer/coach support to clinical care", "escalation from coaching to clinical care", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(n for _, n, _ in PAIRS) and "&mdash;" not in "".join(n for _, n, _ in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")

