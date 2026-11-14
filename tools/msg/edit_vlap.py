"""VLAP page: new message into the existing design. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/vlap.html")
s = P.read_text(encoding="utf-8")

OLD_DESC = ("Vasl's language layer, 47 culturally specific distress signals across coded language, "
            "AAVE, and youth vernacular, surfaced to humans, never used to diagnose.")
NEW_DESC = ("VLAP is Vasl's own language model. It reads the words patients actually use and flags "
            "55 signals across seven dimensions, each with the words behind it. It never diagnoses.")

PAIRS = [
    # meta, title, og, twitter (count-checked below)
    (OLD_DESC, NEW_DESC, 3),
    ("VLAP: Reading Youth Language for Distress Signals | Vasl",
     "VLAP: Language Intelligence for Healthcare | Vasl", 3),

    # Chapter 01
    ("rural and Medicaid youth do.", "rural and Medicaid members do.", 1),

    # Chapter 02 definition + specs
    ("A real-time language analysis layer that detects <em>culturally specific distress signals</em> across 47 clinical signals in six categories, surfaced exclusively to licensed clinicians as interpretive context, never as diagnostic output.",
     "Our own language model, with our own weights. It reads the words patients actually use and flags <em>55 signals across seven dimensions</em> (Taxonomy v2.0), each with the words behind it, for clinicians and care teams as context, never as a diagnosis.", 1),
    ("""          <div class="spec-num">2,400<span style="font-size:22px">+</span></div>
          <div class="spec-label">AAVE & youth vernacular<br>tokens in the corpus</div>""",
     """          <div class="spec-num">0.83<span style="font-size:22px"> vs 0.65</span></div>
          <div class="spec-label">Suicide-attempt severity,<br>VLAP vs MIT&rsquo;s lexicon</div>""", 1),
    ("""          <div class="spec-num">47</div>
          <div class="spec-label">Clinical signals<br>across 6 categories</div>""",
     """          <div class="spec-num">0.97</div>
          <div class="spec-label">F1 on substance use<br>in clinical notes</div>""", 1),
    ("""          <div class="spec-num">0</div>
          <div class="spec-label">Diagnostic outputs<br>ever produced</div>""",
     """          <div class="spec-num">55</div>
          <div class="spec-label">Signals across<br>seven dimensions</div>""", 1),
    ("""          <div class="spec-num">1</div>
          <div class="spec-label">Audience for signal data:<br>licensed clinicians only</div>""",
     """          <div class="spec-num">0</div>
          <div class="spec-label">Patient text sent<br>to an outside AI</div>""", 1),

    # Chapter 03
    ("across the 47 signals in its clinical taxonomy that clinical instruments",
     "across 55 signals in seven dimensions that clinical instruments", 1),
    ("The complete 47-signal taxonomy and five behavioral health scoring domains are documented in the",
     "The complete taxonomy, 55 signals across seven dimensions, is documented in the", 1),

    # Chapter 04 flow
    ("From youth voice<br>to clinical insight<br>", "From patient voice<br>to clinical insight<br>", 1),
    ("""<div class="stage-title">Youth Input</div>
        <div class="stage-desc">Youth communicate through the Member App, text, voice, or structured prompts, in their own language, on their own terms.</div>""",
     """<div class="stage-title">Patient Input</div>
        <div class="stage-desc">Patient replies to Vasl Bridge and Vasl Keep, plus clinical notes over HL7 FHIR R4, in the words people actually use.</div>""", 1),
    ("The language analysis layer runs in real time across the full 47-signal taxonomy. No human reviews this stage. No PHI leaves the system.",
     "Our own model and our own weights read the text across 55 signals in seven dimensions, on Vasl infrastructure. No patient text is sent to an outside AI.", 1),
    ("The signal profile surfaces in the Coach Portal before the session. The clinician, and only the clinician, receives and interprets it.",
     "A named signal with the words behind it lands in the clinician&rsquo;s workflow. No new screen to learn. The clinician interprets it.", 1),
    ("VLAP does not store youth language verbatim after processing. Signal data is clinician-facing only and never shared with organizations, payers, researchers, or third parties without explicit, documented consent.",
     "Patient text is read by VLAP on Vasl infrastructure and never sent to an outside AI company. Signal data goes to the clinician and care team only and is never shared with outside parties without explicit, documented consent.", 1),
    ('<span class="commitment-tag">HIPAA Safe Harbor</span>', '<span class="commitment-tag">HIPAA, BAA</span>', 1),
    ('<span class="commitment-tag">No verbatim storage</span>', '<span class="commitment-tag">No outside AI</span>', 1),

    # Chapter 05
    ("VLAP produces no clinical diagnosis, no risk level, no flag, and no score. It produces interpretive context.",
     "VLAP produces a named signal with the words behind it, never a score or a diagnosis. It is non-device clinical decision support under Section 3060 of the 21st Century Cures Act.", 1),
    ("VLAP does not watch youth. It processes what youth choose to share within the platform, for the purpose of improving their care. There is no passive collection. There is no behavioral profiling. There is no alert sent to a school, a parent, or a platform algorithm.",
     "VLAP does not watch patients. It reads what patients choose to share with their care team, for the purpose of improving their care. There is no passive collection. There is no behavioral profiling. There is no alert sent to anyone outside the care team.", 1),
    ("Its outputs are not visible to youth. Making youth feel supported is the clinician's role.",
     "Its outputs are not visible to patients. Making patients feel supported is the clinician's role.", 1),

    # Chapter 06
    ("Every technical choice reflects a commitment to the youth who never agreed to be studied.",
     "Every technical choice reflects a commitment to the patients who never agreed to be studied.", 1),
    ('<div class="integrity-cert">HIPAA-Aligned Architecture</div>', '<div class="integrity-cert">HIPAA, BAA</div>', 1),
    (" No behavioral metadata harvested outside the session window. The platform is learning for youth.",
     " No behavioral metadata harvested outside the care relationship.", 1),
    ("Youth language is processed and converted to dimensional signal data. Verbatim content is not stored after processing. The youth's words don't live in a database, their meaning does, in a form that protects them.",
     "Patient text is read by VLAP on Vasl infrastructure and never sent to an outside AI company. What comes out is a named signal with the words behind it, delivered only to the care team.", 1),
    ("Signal data surfaces in the Coach Portal and stops there.",
     "Signal data surfaces in the clinician&rsquo;s workflow and stops there.", 1),
    ("Payers, researchers, and third parties see nothing.", "Outside parties see nothing.", 1),
    ("VLAP's training data strategy, behavioral health encounters, ICD-10 codes, standardized assessments, SDoH demographics, is being developed in an active health-system research collaboration, with HIPAA Safe Harbor de-identification and HL7 FHIR-compliant formatting as non-negotiable requirements.",
     "VLAP reads clinical notes over HL7 FHIR R4 from Epic, Cerner and athenahealth. We sign a business associate agreement before any patient data is shared, and HIPAA applies from the first record.", 1),
    ("Youth consent is obtained at enrollment and revisited at each stage of data use. Minors' consent frameworks are designed with legal counsel and community input,",
     "Member consent is obtained at enrollment and revisited at each stage of data use. Consent frameworks are designed with legal counsel and community input,", 1),

    # Chapter 07
    ("""        VLAP is not<br>
        a product you buy.<br>
        It's a capacity<br>
        you <em>build into.</em>""",
     """        Start with<br>
        a pilot on<br>
        your own<br>
        <em>patients&rsquo; text.</em>""", 1),
    (" We partner with community health centers, school-based behavioral health programs, and youth-serving organizations who are ready to meet youth where they are, in language and in clinical practice. Access is by application, deployment is supported, and community alignment is required.",
     " We don&rsquo;t do generic demos. Every pilot is set up around your population, your workflow and the measure you are scored on. Tell us who you serve and we&rsquo;ll run VLAP on your own patients&rsquo; text with you.", 1),
    ('<a href="/contact" class="btn-primary-light">Request Access</a>',
     '<a href="/contact" class="btn-primary-light">Talk to us about a pilot</a>', 1),
    ("""        <div class="tier-label">Community Health Centers</div>
        <div class="tier-name">Full VLAP Integration</div>
        <div class="tier-desc">Complete deployment across Member App, Coach Portal, and Client Org Portal. Includes clinician onboarding, cultural competency alignment session, and ongoing signal calibration support.</div>""",
     """        <div class="tier-label">Medicaid Plans &amp; Health Systems</div>
        <div class="tier-name">VLAP Enterprise</div>
        <div class="tier-desc">$300,000 a year for up to 50,000 members, then $0.50 per member per month. Named signals from Vasl Bridge and Vasl Keep replies and from clinical notes over HL7 FHIR R4, delivered into the workflow your teams already run.</div>""", 1),
    ("""        <div class="tier-label">School-Based Programs</div>
        <div class="tier-name">Coach Portal Access</div>
        <div class="tier-desc">VLAP signal data surfaces for school-based licensed clinicians operating within existing MTSS or behavioral health frameworks. Designed for high-caseload environments where pre-session insight matters most.</div>""",
     """        <div class="tier-label">Product Teams</div>
        <div class="tier-name">VLAP API</div>
        <div class="tier-desc">$50,000 a year. VLAP&rsquo;s named signals through an API, for teams building them into their own product, with a business associate agreement signed before any patient data is shared.</div>""", 1),
    ("""        <div class="tier-label">Research & Validation Partners</div>
        <div class="tier-name">VLAP Data Partnership</div>
        <div class="tier-desc">For academic institutions and health systems developing culturally informed behavioral health research. Data access governed by IRB oversight, HIPAA Safe Harbor de-identification, and bilateral data use agreements.</div>""",
     """        <div class="tier-label">Start Here</div>
        <div class="tier-name">VLAP Pilot</div>
        <div class="tier-desc">Set up around your population, your workflow and the measure you are scored on, and run on your own patients&rsquo; text with you.</div>""", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"vlap: {len(PAIRS)} pairs applied")
