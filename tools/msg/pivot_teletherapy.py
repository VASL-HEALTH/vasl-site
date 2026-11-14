"""Teletherapy page: youth framing -> patients / members. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/teletherapy.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("rural and Medicaid youth actually describe distress.", "rural and Medicaid members actually describe distress.", 1),
    ("A first-generation Somali student is not connected", "A first-generation Somali immigrant is not connected", 1),
    ("navigating predominantly white institutions as a young person of color.", "navigating predominantly white institutions as a person of color.", 1),
    ("skilled at working with youth whose distress presents", "skilled at working with patients whose distress presents", 1),
    ("Black, Brown, and Indigenous youth; first-gen college students; multilingual families",
     "Black, Brown, and Indigenous patients; first-generation families; multilingual families", 1),
    ("LGBTQ+ Youth &middot; Black & Brown Queer Youth &middot; Trans & Non-Binary",
     "LGBTQ+ Members &middot; Black & Brown Queer Members &middot; Trans & Non-Binary", 1),
    ("doesn't ask youth to justify their identity", "doesn't ask members to justify their identity", 1),
    ("serve LGBTQ+ youth with a specific understanding", "serve LGBTQ+ members with a specific understanding", 1),
    ("Black and Brown queer and trans youth whose mental health needs", "Black and Brown queer and trans members whose mental health needs", 1),
    ("LGBTQ+ youth across identity spectrum; intersectional Black and Brown queer youth",
     "LGBTQ+ members across identity spectrum; intersectional Black and Brown queer members", 1),
    ("AAPI Communities &middot; Diaspora Youth", "AAPI Communities &middot; Diaspora Communities", 1),
    ("understands that for many youth, grief", "understands that for many members, grief", 1),
    ("emotional experience of immigrant and diaspora youth,", "emotional experience of immigrant and diaspora members,", 1),
    ("Immigrant and first-gen youth; AAPI communities;", "Immigrant and first-generation families; AAPI communities;", 1),
    # Org types: same four items, new segments
    ("<div class=\"ot-title\">Universities and Higher Education</div>",
     "<div class=\"ot-title\">Health Systems and Emergency Departments</div>", 1),
    ("Vasl integrates with your existing counseling center, providing VLAP signal context and coaching notes that prepare your licensed counselors before sessions, and warm handoffs that make escalation from coaching to clinical care a continuation, not a cold start. Your counselors see students who are already known.",
     "Vasl integrates with your existing behavioral health team, providing VLAP signal context and follow-up notes that prepare your licensed clinicians before sessions, and warm handoffs that make the step from follow-up after an emergency visit to clinical care a continuation, not a cold start. Your clinicians see patients who are already known.", 1),
    ("<div class=\"ot-title\">K-12 Districts and School-Based Programs</div>",
     "<div class=\"ot-title\">Rural Clinics and Critical Access Hospitals</div>", 1),
    ("Vasl supports your school counselors and contracted clinical staff with the coordination infrastructure,",
     "Vasl supports your counselors and contracted clinical staff with the coordination infrastructure,", 1),
    ("Students are protected from school administrative access under HIPAA architecture.",
     "Patient text stays on Vasl infrastructure under HIPAA, BAA, and outside parties see nothing.", 1),
    ("culturally accurate for Medicaid-enrolled youth.", "culturally accurate for Medicaid members.", 1),
    ("<a href=\"/for-schools\" class=\"btn-ghost-light\">For schools specifically</a>",
     "<a href=\"/health-systems\" class=\"btn-ghost-light\">For health systems</a>", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
