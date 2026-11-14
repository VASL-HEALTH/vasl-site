"""Team page: youth framing -> patients / members. Career facts untouched. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/team.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("communities being served, Black, Brown, LGBTQ+, rural and Medicaid youth, and advisors",
     "communities being served, Black, Brown, LGBTQ+, rural and Medicaid members, and advisors", 1),
    # Rodney: bio
    ("a culturally intelligent mental-health platform built to close the gap between underserved youth and the support systems that have historically failed them.",
     "a culturally intelligent behavioral health company that works with Medicaid plans and health systems to close the gap between underserved patients and the support systems that have historically failed them.", 1),
    ("immigrant, and first-generation young people.</p>",
     "immigrant, rural, and first-generation patients and members.</p>", 1),
    # Rodney: pull quote
    ("I grew up watching young people communicate distress in ways adults didn't recognize,",
     "I grew up watching people in my community communicate distress in ways the systems around them didn't recognize,", 1),
    ("In my work across youth development, mental health, and community-based programs,",
     "In my work across health care, mental health, and community-based programs,", 1),
    ("Black, Brown, immigrant, and multilingual youth were expressing early emotional shifts",
     "Black, Brown, rural, immigrant, and multilingual patients were expressing early emotional shifts", 1),
    ("building programs that honor the lived experiences of young people,",
     "building programs that honor the lived experiences of the people they serve,", 1),
    ("the gap is structural and young people deserve a mental-health system that understands them.",
     "the gap is structural and patients deserve a behavioral health system that understands them.", 1),
    # Advisors / clinicians
    ("how a clinician sits with a young person who's struggling.",
     "how a clinician sits with a patient who's struggling.", 1),
    ("what BIPOC and LGBTQ+ youth are actually communicating",
     "what BIPOC and LGBTQ+ patients are actually communicating", 1),
    ("Her work with immigrant and diaspora youth, where distress manifests",
     "Her work with immigrant and diaspora communities, where distress manifests", 1),
    ("For many of the youth Vasl serves,", "For many of the people Vasl serves,", 1),
    ("Collectivist cultural frameworks · First-generation youth</div>",
     "Collectivist cultural frameworks · First-generation families</div>", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
