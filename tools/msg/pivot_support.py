"""Support page: youth/schools framing to Medicaid plans, health systems and members. Exact pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/support.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("Resources and answers for members, coaches, clinicians, school administrators, and organizational partners.",
     "Resources and answers for members, coaches, clinicians, and partners at Medicaid plans and health systems.", 1),
    ("initial configuration for schools, health centers, and community organizations.",
     "initial configuration for Medicaid plans, health systems, and community health centers.", 1),
    ("Pricing plans, Medicaid billing setup and documentation, Title I funding, and organizational contract questions.",
     "Pricing plans, Medicaid billing setup and documentation, and organizational contract questions.", 1),
    ("HIPAA compliance, FERPA alignment, WCAG accessibility, BAA execution, and privacy policy.",
     "HIPAA compliance, WCAG accessibility, BAA execution, and privacy policy.", 1),
    ("your Vasl Health account, for schools, community health centers, and organizational partners.",
     "your Vasl Health account, for Medicaid plans, health systems, and community health centers.", 1),
    ("Step-by-step guide to school-based and community health center Medicaid billing for Vasl deployments. Includes CPT code mapping, documentation export formats, and estimated recovery rates for Title I districts.",
     "Step-by-step guide to health system and community health center Medicaid billing for Vasl deployments. Includes CPT code mapping, documentation export formats, and how recovery is modeled during scoping.", 1),
    ("we receive most often from school administrators, organizational partners, clinicians, and members.",
     "we receive most often from Medicaid plans, health systems, clinicians, and members.", 1),
    ("is specifically trained on language samples from BIPOC and LGBTQ+ youth communities, including a community-annotated library of AAVE and youth vernacular that standard NLP models have never encountered.",
     "is specifically trained on the language patients actually use, including a community-annotated library of African American Language, rural speech, queer vernacular, and coded phrases that standard NLP models have never encountered.", 1),
    ("not to members, not to school staff, not to administrators.",
     "not to members, not to administrators.", 1),
    ("invisible to members, coaches, and school staff.",
     "invisible to members, coaches, and org staff.", 1),
    ("formatted for your district's or organization's Medicaid billing system.",
     "formatted for your organization's Medicaid billing system.", 1),
    ("For qualifying Title I school deployments, approximately 50% of contract cost is recoverable through school-based Medicaid billing for qualifying services. Your exact recovery depends on your state Medicaid plan and student eligibility rates, we model this during your implementation scoping process.",
     "Your recovery depends on your state Medicaid plan and your members' Medicaid eligibility; we model this during your implementation scoping process.", 1),
    ("not to coaches, school staff, org administrators, or Vasl team members",
     "not to coaches, org administrators, or Vasl team members", 1),
    ("Individual member records are never shared with school administrators or org staff under any circumstances.",
     "Individual member records are never shared with org administrators or staff under any circumstances.", 1),
    ('<span class="faq-tag">HIPAA &middot; BAA &middot; FERPA</span>',
     '<span class="faq-tag">HIPAA &middot; BAA</span>', 1),
    ("compliance documentation, counselor and clinical staff orientation, student community alignment sessions (for school deployments), and the first Medicaid billing cycle.",
     "compliance documentation, care team and clinical staff orientation, and the first Medicaid billing cycle.", 1),
    ('placeholder="School district, health center, or organization name"',
     'placeholder="Health plan, health system, or organization name"', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(x[1] for x in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
