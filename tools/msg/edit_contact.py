"""Contact page: new message into the existing design. Exact old/new pairs, each asserted.

Form markup, field names, ids, checkbox VALUES and handler wiring are untouched.
Organization-type <option>s carry no value attribute, so the submitted value is
the label text; those labels change (reported to the caller for the handler).
"""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/contact.html")
s = P.read_text(encoding="utf-8")

OLD_DESC = ("Schedule a demo, ask about implementation timelines, or reach our clinical, education, "
            "research, or community partnerships teams directly.")
NEW_DESC = ("Talk to us about a pilot of Vasl Bridge, Vasl Keep or VLAP, ask about pricing, or reach "
            "our healthcare, research, community or press teams directly.")

PAIRS = [
    # meta, title, og, twitter
    (OLD_DESC, NEW_DESC, 3),
    ("Contact Vasl Health, Request a Demo", "Contact Vasl Health, Talk to Us About a Pilot", 3),

    # hero
    ("""      about your<br>
      <em>community.</em>""",
     """      about your<br>
      <em>members.</em>""", 1),
    ("Vasl is built on how Black, Brown, LGBTQ+, rural and Medicaid youth actually describe distress. Every Vasl conversation starts with your specific context, your population, your existing infrastructure, what outcomes you need. We don't pitch generically. Use the form below to schedule a demo or reach the right team directly.",
     "Vasl Health PBC works with Medicaid plans and health systems. VLAP is built on how Black, Brown, LGBTQ+, rural and Medicaid patients actually describe distress. Every Vasl conversation starts with your specific context, your population, your existing infrastructure, what outcomes you need. We don't pitch generically. Use the form below to talk to us about a pilot or reach the right team directly.", 1),

    # channels
    ("""      <div class="ch-title">Healthcare & Clinical Partnerships</div>""",
     """      <div class="ch-title">Medicaid Plans & Health Systems</div>""", 1),
    ("Clinical team response &middot; HIPAA-compliant discussions &middot; BAA execution",
     "Pilots &middot; HIPAA, BAA &middot; VLAP Enterprise and VLAP API", 1),
    ("""    <div class="channel-item">
      <div class="ch-purpose">Education</div>
      <div class="ch-title">School & University Partnerships</div>
      <a href="mailto:education@gotovasl.com" class="ch-email">education@gotovasl.com</a>
      <div class="ch-note">FERPA compliance &middot; Medicaid billing setup &middot; Title I districts</div>
    </div>
""", "", 1),
    ("Grant documentation &middot; Starter plan &middot; Mission-aligned deployments",
     "Community partnerships &middot; Mission-aligned work", 1),
    ("IRB study access &middot; VLAP technical documentation &middot; NDA required",
     "VLAP measurement report &middot; VLAP technical documentation &middot; NDA required", 1),

    # form intro
    ("""    <div class="fl-label reveal">Schedule a Demo</div>""",
     """    <div class="fl-label reveal">Talk to Us About a Pilot</div>""", 1),

    # placeholders (attributes only)
    ('placeholder="you@organization.edu"', 'placeholder="you@organization.org"', 1),
    ('placeholder="State University System"', 'placeholder="Regional Health Plan"', 1),
    ('placeholder="VP Student Affairs"', 'placeholder="VP Population Health"', 1),

    # organization type: labels only (no value attributes exist; value = label text)
    ("""          <option>University / College</option>
          <option>K-12 School District</option>
          <option>Community Health Center / FQHC</option>
          <option>Health Plan / Managed Care</option>
          <option>Hospital / Health System</option>
          <option>Non-Profit / Youth Organization</option>
          <option>Government Agency</option>
          <option>Other</option>""",
     """          <option>Medicaid Plan</option>
          <option>Health System</option>
          <option>VLAP API</option>
          <option>Other</option>""", 1),

    # interest checkbox LABELS only; values untouched
    ('<span class="form-checkbox-label">Culturally-responsive AI and VLAP signal detection</span>',
     '<span class="form-checkbox-label">VLAP Enterprise or VLAP API</span>', 1),
    ('<span class="form-checkbox-label">Peer community and coaching infrastructure</span>',
     '<span class="form-checkbox-label">Vasl Bridge, follow-up after an emergency visit</span>', 1),
    ('<span class="form-checkbox-label">Medicaid billing integration and cost recovery</span>',
     '<span class="form-checkbox-label">Vasl Keep, eligible Medicaid members keeping their coverage</span>', 1),
    ('<span class="form-checkbox-label">Clinical outcomes data and IRB validation</span>',
     '<span class="form-checkbox-label">VLAP measurement results</span>', 1),
    ('<span class="form-checkbox-label">HIPAA / FERPA compliance and security documentation</span>',
     '<span class="form-checkbox-label">HIPAA, BAA and security documentation</span>', 1),

    ('placeholder="Your current mental health infrastructure, specific population challenges, grant funding context, or any questions you want addressed in the demo."',
     'placeholder="Your current follow-up and outreach programs, the population you serve, or any questions you want addressed on the call."', 1),

    # primary CTA
    ("""<button type="submit" class="form-submit">Schedule Demo &rarr;</button>""",
     """<button type="submit" class="form-submit">Talk to us about a pilot &rarr;</button>""", 1),

    # FAQ
    ("Six weeks from contract signature to first member enrollment, consistently, across org types.",
     "Six weeks from contract signature to first member enrollment.", 1),
    ("Two components: a platform fee and a per member per month (PMPM) fee, both scoped to your population size and setting. Schools and non-profits sit at one rate, health systems and enterprise deployments at another, and large multi-site deployments are quoted on their own. Tell us the setting and the number of members and we will give you the actual figure.",
     "VLAP Enterprise is $300,000 a year for up to 50,000 members, then $0.50 per member per month. VLAP API is $50,000 a year. Most organizations start with a pilot. Tell us the setting and the number of members and we will give you the actual figure.", 1),
    ("HIPAA technical safeguards, full implementation across all platform components. BAA required for all organizational deployments and included in every contract. FERPA-aligned architecture for school deployments, student health data is structurally inaccessible to school administrators. SOC 2 Type II, annual third-party audit. Full compliance documentation is available under NDA for institutional review.",
     "HIPAA, BAA. We sign a business associate agreement before any patient data is shared, and it is included in every contract. Patient text is read by VLAP on Vasl infrastructure and never sent to an outside AI company. VLAP is non-device clinical decision support under Section 3060 of the 21st Century Cures Act. Full compliance documentation is available under NDA for institutional review.", 1),
    ("We provide grant documentation, IRB study data, the VLAP model measurement report, VLAP technical overview, and compliance documentation, in formats designed for grant applications. For school districts, we also support Medicaid billing setup and Title IV-A documentation. We don't write grants on your behalf, but we make sure you have the outcome evidence grant funders need to see.",
     "We provide the VLAP model measurement report, the VLAP technical overview, and compliance documentation, in formats designed for grant applications. We don't write grants on your behalf, but we make sure you have the evidence grant funders need to see.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"contact: {len(PAIRS)} pairs applied")
