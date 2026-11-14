"""Help: compliance. School/student framing to members and organizations. Legal FERPA row and minors clause kept. Exact pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/compliance.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("without your explicit consent, not your school, not your employer, not your parents (unless you're a minor and applicable state law requires it),",
     "without your explicit consent, not your employer, not your parents (unless you're a minor and applicable state law requires it),", 1),
    ("Your school administrator, your employer, and your parents do not have access to it.",
     "Your organization's administrators, your employer, and your family do not have access to it.", 1),
    ("They are not shared with your school, employer, or org administrator.",
     "They are not shared with your employer or org administrator.", 1),
    ('<div class="ath">School / Org Admin</div>',
     '<div class="ath">Org Admin</div>', 1),
    ("The school administrator or org admin column says",
     "The org admin column says", 1),
    ("<div class=\"callout-label\">Why Your School Can't See Your Data</div>",
     "<div class=\"callout-label\">Why Your Organization Can't See Your Data</div>", 1),
    ("This is a question many members have, especially students who worry that what they share will reach their counselors, teachers, or parents. The answer is architectural. The system is built so that individual disclosure to school administrators is structurally impossible. It is not a setting that can be changed, a policy that can be overridden by the school, or an exception that applies in any circumstance. Individual member data never reaches school staff.",
     "This is a question many members have, especially those who worry that what they share will reach their employer, their organization, or their family. The answer is architectural. The system is built so that individual disclosure to org administrators is structurally impossible. It is not a setting that can be changed, a policy that can be overridden by the organization, or an exception that applies in any circumstance. Individual member data never reaches org staff.", 1),
    ("No one else, not school staff, not org administrators,",
     "No one else, not org administrators,", 1),
    ("Every organization that deploys Vasl Health, school districts, universities, community health centers, health plans, is required",
     "Every organization that deploys Vasl Health, Medicaid plans, health systems, community health centers, is required", 1),
    ("For school and community health deployments using school-based Medicaid billing,",
     "For health system and community health deployments using Medicaid billing,", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(x[1] for x in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
