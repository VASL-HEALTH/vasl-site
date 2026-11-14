"""Help: VLAP technology. Youth framing to the language patients actually use. FERPA row kept. Exact pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/vlap-technology.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("consistently miss the coded, vernacular, and culturally framed ways that BIPOC, LGBTQ+, and first-generation youth communicate distress.",
     "consistently miss the coded, vernacular, and culturally framed ways patients communicate distress: African American Language, rural speech, queer vernacular, coded phrases.", 1),
    ("expressed through AAVE, coded youth language, and minimization patterns",
     "expressed through AAVE, coded language, and minimization patterns", 1),
    ('"it\'s not that deep but lowkey been struggling since school started."',
     '"it\'s not that deep but lowkey been struggling since this job started."', 1),
    ('<div class="sp-term">"since school started"</div>',
     '<div class="sp-term">"since this job started"</div>', 1),
    ("Coded suicidal ideation term developed in youth communities to circumvent content filters.",
     "Coded suicidal ideation term developed in online communities to circumvent content filters.", 1),
    ("It does not scan social media, school email, or any external channel.",
     "It does not scan social media, work email, or any external channel.", 1),
    ("Surface individual signal data to school staff or org administrators",
     "Surface individual signal data to org administrators", 1),
    ("Never accessible to school staff, org administrators, or Vasl team members",
     "Never accessible to org administrators or Vasl team members", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(x[1] for x in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
