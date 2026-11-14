"""Careers page: youth framing -> patients / members. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/careers.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("what we expect from people building for youth who are usually built around.",
     "what we expect from people building for patients who are usually built around.", 3),
    ("never built for Black, Brown, LGBTQ+, rural and Medicaid youth.",
     "never built for Black, Brown, LGBTQ+, rural and Medicaid members.", 1),
    ("The gap isn't that underserved youth can't find mental health support.",
     "The gap isn't that underserved patients can't find mental health support.", 1),
    ("before they see youth in crisis.", "before they see patients in crisis.", 1),
    ("understand AAVE, code-switching, and youth vernacular</div>",
     "understand African American Language, rural speech, queer vernacular, coded phrases and code-switching</div>", 1),
    ("Clinical impact for youth who had no prior access to care that worked for them.",
     "Clinical impact for patients who had no prior access to care that worked for them.", 1),
    ("Youth voices are part of the design process from the beginning.",
     "Community voices are part of the design process from the beginning.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
