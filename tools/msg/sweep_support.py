"""Support page: stale-claim sweep only. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/support.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # Category grid
    ("How the platform works, the Member App, Coach Portal, Client Org Portal, and VLAP clinical coordination infrastructure.",
     "How the platform works, the clinician's workflow, and VLAP clinical coordination infrastructure.", 1),
    ("WCAG accessibility, SOC 2 Type II documentation, BAA execution, and privacy policy.",
     "WCAG accessibility, BAA execution, and privacy policy.", 1),
    # Popular articles
    ("Covers enrollment setup, clinical network integration, and the Client Org Portal.",
     "Covers enrollment setup and clinical network integration.", 1),
    ("How VLAP detects culturally specific distress signals across six clinical categories and surfaces interpretive context",
     "How VLAP flags 55 signals across seven dimensions and surfaces interpretive context", 1),
    ("Covers the Coach Portal pre-session view, signal dimension interpretation,",
     "Covers the pre-session view in the clinician's workflow, signal dimension interpretation,", 1),
    ("supported browsers for the Member App, Coach Portal, and Client Org Portal.",
     "supported browsers for the clinician's workflow.", 1),
    ("BAA requirements, audit logging, and annual SOC 2 Type II audit.",
     "BAA requirements, and audit logging.", 1),
    # FAQ
    ("including 2,400+ AAVE and youth vernacular tokens that standard NLP models have never encountered. It detects culturally specific distress signals across six clinical categories and surfaces that context",
     "including a community-annotated library of AAVE and youth vernacular that standard NLP models have never encountered. It flags 55 signals across seven dimensions, each with the words behind it, and surfaces that context", 1),
    ("Members interact with certified coaches (human), peer groups (human-moderated), and licensed clinicians (human).",
     "Members interact with certified coaches (human) and licensed clinicians (human).", 1),
    ("no software installation required. The Member App is optimized for mobile (iOS 12+ and Android 8+) and desktop. We recommend",
     "no software installation required. We recommend", 1),
    ("For clinicians accessing the Coach Portal with VLAP signal data,",
     "For clinicians viewing VLAP signal data,", 1),
    ("outcome tracking through the Coach Portal. Members experience the coaching relationship and peer community, not clinical",
     "outcome tracking in the clinician's workflow. Members experience the coaching relationship, not clinical", 1),
    (" Annual SOC 2 Type II audit. BAA required", " BAA required", 1),
    ("HIPAA &middot; SOC 2 Type II &middot; FERPA", "HIPAA &middot; BAA &middot; FERPA", 1),
    ("(for school deployments), peer group setup, and the first Medicaid billing cycle.",
     "(for school deployments), and the first Medicaid billing cycle.", 1),
    ("the 988 Suicide and Crisis Lifeline is integrated and accessible directly through the Member App.",
     "the 988 Suicide and Crisis Lifeline is integrated and directly accessible.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"support: {len(PAIRS)} pairs applied")
