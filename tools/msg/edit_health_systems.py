"""Health Plans & Systems page: new message into the existing design. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/health-systems.html")
s = P.read_text(encoding="utf-8")

OLD_DESC = ("Reach and retain the adolescent and transition-age members standard programs lose. "
            "Engagement built on cultural and linguistic fit, not translation.")
NEW_DESC = ("Vasl Bridge, Vasl Keep and VLAP for Medicaid plans and health systems: follow-up after an "
            "emergency visit, members who keep their coverage, and named signals from patient text inside "
            "the care you already deliver.")

PAIRS = [
    # meta, title, og, twitter
    (OLD_DESC, NEW_DESC, 3),
    ("Youth Behavioral Health for Health Plans &amp; Systems | Vasl",
     "For Medicaid Plans &amp; Health Systems | Vasl", 3),

    # Hero
    ("""      One engine.<br>
      Two ways to<br>
      <em>deploy it.</em>""",
     """      One engine.<br>
      Three ways to<br>
      <em>put it to work.</em>""", 1),
    ("Vasl runs a full care platform for Black, Brown, LGBTQ+, rural and Medicaid youth, inside schools, universities and community organizations: a daily check-in by text, peer community, coaching, and a warm handoff to the partner&rsquo;s own licensed clinicians. Health systems and FQHCs deploy the same intelligence a different way: VLAP as a clinical decision support layer inside your own care delivery.",
     "Vasl Health PBC works with Medicaid plans and health systems. Vasl Bridge sends a text every day from emergency discharge to the first visit, and VLAP reads every reply. Vasl Keep helps eligible Medicaid members keep the coverage they qualify for, and each reply is sorted. VLAP Enterprise puts the same language model inside your own care delivery.", 1),
    ("VLAP runs on the transcripts your teams already generate, including ambient scribe output, and surfaces culturally interpreted risk context to your clinicians before and between sessions. No new workflow. No new documentation burden. Your clinicians, better informed.",
     "VLAP is our own language model, with our own weights. It reads patient messages, text replies, clinician notes and scribe text, and flags 55 signals across seven dimensions with the words behind each. A named signal with the words behind it, never a score or a diagnosis, delivered into the workflow your teams already run. No new screen to learn.", 1),
    ("Vasl Bridge: a text from Vasl every day, from ED discharge to the first visit.",
     "Vasl Bridge: a text from Vasl every day, from emergency discharge to the first visit. 10 of 10 steps passed live, with real texts delivered.", 1),
    ("VLAP as clinical decision support inside your existing EHR and care workflow, not a separate platform your clinicians have to log into.",
     "VLAP as non-device clinical decision support inside your existing electronic health record and care workflow. Your clinicians do not log into a separate platform.", 1),
    ("Runs on the clinical documentation your teams already generate, intake notes, progress notes, discharge summaries, and telehealth encounter notes, including ambient scribe output. No new intake, no new documentation.",
     "Patient messages, text replies, clinician notes and scribe text your teams already generate. No new intake, no new documentation.", 1),
    ("Ingests via HL7 FHIR API or CSV/JSON under HIPAA Safe Harbor de-identification, with integration paths for major EHRs.",
     "Intake over HL7 FHIR R4 from Epic, Cerner and athenahealth. HIPAA, BAA: we sign a business associate agreement before any patient data is shared.", 1),

    # Governance
    ("VLAP is clinical decision support, not a diagnostic device. Signals route only to licensed clinicians, with mandatory human review before any escalation. Every step is documented for audit.",
     "VLAP is non-device clinical decision support under Section 3060 of the 21st Century Cures Act. Signals route only to the clinicians and care teams responsible for the patient, with human review before any escalation. Every step is documented for audit.", 1),
    ("Signals route only to licensed clinicians, never to administrators, payers, or automated systems.",
     "Signals route only to the clinicians and care teams responsible for the patient. Outside parties see nothing.", 1),
    ("Four-tier risk framing, low, moderate, elevated, acute, with mandatory human review before any escalation.",
     "A named signal with the exact words behind it, never a score or a diagnosis. The clinician decides.", 1),
    ("FHIR R4-ready, with integration paths for major EHRs.",
     "Patient text is read by VLAP on Vasl infrastructure and never sent to an outside AI company.", 1),

    # Calibration
    ("standard NLP was never built to read.", "standard clinical software was never built to read.", 1),
    ("VLAP, our clinical language model, is trained on youth-generated language, AAVE, coded phrasing, limited-English-proficiency patterns, with an SDOH-aware calibration layer (Provisional Patent VH-2026-001-PROV) that adjusts for the contexts standard NLP gets wrong.",
     "VLAP reads how Black, Brown, LGBTQ+, rural and Medicaid patients actually describe what they are going through, and flags 55 signals across seven dimensions (Taxonomy v2.0). On suicide-attempt severity it scores 0.83 ROC-AUC against 0.65 for MIT&rsquo;s Suicide Risk Lexicon, on the same corpus and the same split. On substance use in clinical notes it scores 0.97 F1 on the n2c2 2022 SHAC test, 518 notes, against 0.83 for a keyword rule.", 1),

    # Bridge
    ("from the day a young person leaves the emergency department to their first appointment.",
     "from the day a patient leaves the emergency department to their first appointment.", 1),

    # Status
    ("Currently in pilot-design conversations with academic medical centers and health-system innovation programs; no pilot has run yet. Independent validation via an IRB-approved university study is underway.",
     "Vasl Bridge passed 10 of 10 steps live, with real texts delivered. No pilot has run yet. Every pilot is set up around your population, your workflow and the measure you are scored on.", 1),
    ('<span class="status-tag">Structured Pilot Pathways</span>',
     '<span class="status-tag">HIPAA, BAA</span>', 1),
    ('<span class="status-tag">IRB-Approved University Study</span>',
     '<span class="status-tag">Non-Device Clinical Decision Support</span>', 1),

    # CTA
    ("Tell us about your care delivery model and data infrastructure, and we&rsquo;ll show you exactly how VLAP fits, as decision support, not another system to manage.",
     "Tell us who you serve and how your data flows, and we&rsquo;ll run VLAP on your own patients&rsquo; text with you, inside the workflow you already run.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"health-systems: {len(PAIRS)} pairs applied")
