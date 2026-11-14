"""Help: billing. Schools/Title I framing to Medicaid plans and health systems; approved VLAP pricing. Exact pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/billing.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # meta, og, twitter
    ("How Vasl supports school-based and community health Medicaid billing, documentation exports, CPT code guidance, and recovery estimates for org finance teams.",
     "How Vasl supports health system and community health Medicaid billing, documentation exports, CPT code guidance, and recovery estimates for org finance teams.", 3),
    ("How Vasl supports school-based and community health Medicaid billing, what documentation we provide",
     "How Vasl supports health system and community health Medicaid billing, what documentation we provide", 1),
    ('<span class="audience-tag primary">School Finance Directors</span>',
     '<span class="audience-tag primary">Health System Finance Directors</span>', 1),
    ("formatted for your district's or organization's Medicaid billing system.",
     "formatted for your organization's Medicaid billing system.", 1),
    # The math: approved VLAP pricing replaces the Title I district model
    ("Vasl pricing has two components: a platform fee and a per member per month (PMPM) fee, both scoped to your enrollment and setting. For a Title I district, approximately 50% of contract cost is recoverable through school-based Medicaid billing for qualifying services, and Title IV-A or ESSER funds often cover part of the remainder. Your implementation lead builds the figures with you during scoping.",
     "VLAP Enterprise is $300,000 a year for up to 50,000 members, then $0.50 per member per month. The VLAP API is $50,000 a year. Most partners start with a pilot. Your implementation lead builds the figures with you during scoping, including any Medicaid recovery for qualifying services.", 1),
    ('<div class="mb-label">Title I District &middot; 500 Students &middot; How the math works</div>',
     '<div class="mb-label">Medicaid Plans &amp; Health Systems &middot; How the math works</div>', 1),
    ('<span>Platform fee, annual</span><span class="mb-val">Scoped</span>',
     '<span>VLAP Enterprise, up to 50,000 members, annual</span><span class="mb-val">$300,000</span>', 1),
    ('<span>PMPM, schools, by enrollment</span><span class="mb-val">Scoped</span>',
     '<span>Each member above 50,000, per member per month</span><span class="mb-val">$0.50</span>', 1),
    ('<span>Medicaid recovery estimate</span><span class="mb-val">~50%</span>',
     '<span>VLAP API, annual</span><span class="mb-val">$50,000</span>', 1),
    ('<span>Additional funding, Title IV-A and ESSER</span><span class="mb-val">Variable</span>',
     '<span>Medicaid recovery, qualifying services</span><span class="mb-val">Modeled at scoping</span>', 1),
    ('<span>Net annual district cost</span><span class="mb-val">The remainder</span>',
     '<span>Where to start</span><span class="mb-val">A pilot</span>', 1),
    ('<div class="callout-label">This Is an Estimate, Not a Guarantee</div>',
     '<div class="callout-label">Recovery Is an Estimate, Not a Guarantee</div>', 1),
    ("The ~50% recovery figure is a modelled estimate, not measured experience; no pilot has run. Your actual recovery depends on: your state's Medicaid reimbursement rates, your student population's Medicaid eligibility rate,",
     "Any Medicaid recovery figure is a modeled estimate, not measured experience; no pilot has run. Your actual recovery depends on: your state's Medicaid reimbursement rates, your members' Medicaid eligibility rate,", 1),
    ("build a recovery model specific to your district during the scoping process.",
     "build a recovery model specific to your organization during the scoping process.", 1),
    ("verifies against your student Medicaid eligibility list,",
     "verifies against your member Medicaid eligibility list,", 1),
    # State variation
    ("School-based Medicaid billing operates under federal Medicaid guidelines but is administered by each state",
     "Medicaid billing for behavioral health operates under federal Medicaid guidelines but is administered by each state", 1),
    ("Some states have well-developed school-based behavioral health billing infrastructure.",
     "Some states have well-developed community behavioral health billing infrastructure.", 1),
    ("Vasl's compliance team has worked with districts and organizations across multiple states and can provide state-specific guidance during your implementation scoping.",
     "Vasl's compliance team can provide state-specific guidance during your implementation scoping.", 1),
    # Additional funding: school-only rows removed cleanly
    ('        <div class="st-row">\n          <div class="st-label">Title IV-A</div>\n'
     '          <div class="st-value">Student Support and Academic Enrichment grants, covers student mental health programs as part of a "well-rounded educational opportunity." Available to all Title I districts. Contact your district\'s federal programs coordinator.</div>\n'
     '        </div>\n', "", 1),
    ('        <div class="st-row">\n          <div class="st-label">ESSER Funds</div>\n'
     '          <div class="st-value">Elementary and Secondary School Emergency Relief, remaining ESSER III funds may be applicable where mental health support programs qualify under your state\'s guidance. Check current availability with your state education agency.</div>\n'
     '        </div>\n', "", 1),
    # Related sidebar (static in page, not a LINKS:VASL block)
    ('<a href="/for-schools" class="related-item">\n        <div class="ri-cat">For Schools</div>\n        <div class="ri-title">The Medicaid Model, Concept & Math</div>',
     '<a href="/health-systems" class="related-item">\n        <div class="ri-cat">For Health Systems</div>\n        <div class="ri-title">For Medicaid Plans &amp; Health Systems</div>', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(x[1] for x in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
