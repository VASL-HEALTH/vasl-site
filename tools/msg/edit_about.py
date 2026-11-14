"""About page: new message into the existing design. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/about.html")
s = P.read_text(encoding="utf-8")

OLD_DESC = ("Behavioral health for Black, Latino, LGBTQ+, and first-generation youth, designed inside "
            "their language and culture from the start, not retrofitted after.")
NEW_DESC = ("Vasl Health PBC builds language intelligence for Medicaid plans and health systems. VLAP, "
            "our own language model, reads how patients actually describe what they are going through.")

PAIRS = [
    # meta, title, og, twitter
    (OLD_DESC, NEW_DESC, 3),
    ("About Vasl Health: Built for the Youth Systems Miss",
     "About Vasl Health: Built for the Patients Other Tools Miss", 3),

    # Chapter 01, mission
    ("""      Built for the youth<br>
      every other platform<br>""",
     """      Built for the patients<br>
      every other tool<br>""", 1),
    ("To eliminate mental health disparities by building AI that understands how Black, Brown, LGBTQ+, rural and Medicaid youth actually communicate about distress, trauma, and healing.",
     "To eliminate mental health disparities by building AI that understands how Black, Brown, LGBTQ+, rural and Medicaid patients actually communicate about distress, trauma, and healing.", 1),
    ("We are building the first behavioral health platform designed by and for Black and Latino, LGBTQ+, and first-generation youth communities. Not retrofitted. Not translated. Built from inside the language, the culture, and the lived experience, from the beginning.",
     "Vasl Health PBC builds language intelligence for Medicaid plans and health systems. VLAP, our own language model, reads how patients actually describe what they are going through. Vasl Bridge and Vasl Keep turn what it reads into follow-up. Built from inside the language, the culture, and the lived experience, from the beginning.", 1),
    ("""      <a href="/contact" class="btn-outline">Partner with us</a>""",
     """      <a href="/contact" class="btn-outline">Talk to us about a pilot</a>""", 1),

    # Chapter 01, mission stats
    ("""      <div class="ms-num">47</div>
      <div class="ms-right">
        <div class="ms-label">Culturally specific distress signals detected across six clinical categories</div>
        <div class="ms-desc">VLAP signal taxonomy</div>""",
     """      <div class="ms-num">55</div>
      <div class="ms-right">
        <div class="ms-label">Signals across seven dimensions, each flagged with the words behind it</div>
        <div class="ms-desc">VLAP Taxonomy v2.0</div>""", 1),
    ("""      <div class="ms-num">2,400<span style="font-size:18px">+</span></div>
      <div class="ms-right">
        <div class="ms-label">AAVE and youth vernacular tokens in the VLAP model vocabulary</div>
        <div class="ms-desc">Community-sourced, clinically annotated</div>""",
     """      <div class="ms-num">0.83</div>
      <div class="ms-right">
        <div class="ms-label">ROC-AUC on suicide-attempt severity, against 0.65 for MIT&rsquo;s Suicide Risk Lexicon</div>
        <div class="ms-desc">Same corpus &middot; same split</div>""", 1),
    ("""      <div class="ms-num">90<span style="font-size:22px">%</span></div>
      <div class="ms-right">
        <div class="ms-label">Sensitivity on high-distress signal detection, clinical validation in progress</div>
        <div class="ms-desc">IRB study active &middot; university research partner</div>""",
     """      <div class="ms-num">0.97</div>
      <div class="ms-right">
        <div class="ms-label">F1 on substance use in clinical notes, against 0.83 for a keyword rule</div>
        <div class="ms-desc">n2c2 2022 SHAC test &middot; 518 notes</div>""", 1),
    ("""      <div class="ms-num">Day one</div>
      <div class="ms-right">
        <div class="ms-label">Support begins the day a member is enrolled</div>
        <div class="ms-desc">Org and payer funded &middot; Access is not a billing question</div>""",
     """      <div class="ms-num">10 of 10</div>
      <div class="ms-right">
        <div class="ms-label">Vasl Bridge steps passed live, real texts delivered</div>
        <div class="ms-desc">Follow-up after an emergency visit</div>""", 1),

    # Chapter 02, story
    ("Vasl Health was built from a specific observation: existing mental health AI doesn't understand how Black and Latino, LGBTQ+, and first-generation youth actually communicate about distress. Generic models are trained on majority-White internet text. They consistently miss AAVE, code-switching, youth vernacular, and the coded language communities develop when the dominant culture's vocabulary isn't safe, available, or accurate. The gap isn't fine-tuning. It's architecture. We built something different.",
     "Vasl Health was built from a specific observation: existing mental health AI doesn't understand how Black, Brown, LGBTQ+, rural and Medicaid patients actually communicate about distress. Generic tools are built on textbook English. They consistently miss African American Language, code-switching, rural speech, and the coded language communities develop when the dominant culture's vocabulary isn't safe, available, or accurate. Nobody built the instrument because nobody in the room spoke the language. We do.", 1),
    ("producing dangerous gaps in clinical awareness for diverse youth populations. The problem wasn't access to AI. It was that the AI available had never been trained on the communities it was being deployed to serve.",
     "producing dangerous gaps in clinical awareness for Black, Brown, LGBTQ+, rural and Medicaid patients. The AI available had never been trained on the communities it was being deployed to serve.", 1),
    ("We began developing VLAP, the Vasl Language Analysis Platform, training a BERT-architecture model on culturally specific mental health language samples drawn from BIPOC and LGBTQ+ youth communities. Every training sample was clinically annotated by licensed clinicians with community competency training. The 2,400+ token vocabulary extension was built from community language, not from clinical corpora or majority-population datasets.",
     "We began developing VLAP, the Vasl Language Analysis Platform, as our own language model with our own weights, trained on how patients actually write, starting with African American Language. Training samples were clinically annotated by licensed clinicians with community competency training. The vocabulary was built from community language, not from clinical corpora or majority-population datasets.", 1),
    ("We measured VLAP against the field&rsquo;s published standard. VLAP scores 0.83 against the MIT / Child Mind / Crisis Text Line lexicon&rsquo;s 0.65 on suicide-attempt severity, and 23 of its 47 signals have no counterpart in that lexicon&rsquo;s 6,910 terms. The data matched the framework. When the platform understands how youth actually communicate, they stay. An IRB study with a university research partner began validating clinical signal accuracy in production deployment.",
     "We measured VLAP against the field&rsquo;s published standard. VLAP scores 0.83 ROC-AUC against 0.65 for MIT&rsquo;s Suicide Risk Lexicon on suicide-attempt severity, scored on the same corpus and the same split. The lexicon, from MIT, the Child Mind Institute and Crisis Text Line, holds 6,910 terms. The data matched the framework.", 1),
    ("""      <span class="tl-tag">0.83 vs 0.65 &middot; 23 of 47 signals unmatched</span>""",
     """      <span class="tl-tag">0.83 vs 0.65 &middot; Same Corpus, Same Split</span>""", 1),
    ("""      <div class="tl-name">National Scale</div>
      <p class="tl-body">Expanding partnerships with healthcare systems, school districts, and community organizations to bring the Vasl platform and VLAP clinical interpretation infrastructure to communities nationwide. An active health-system research collaboration is underway to support VLAP model development, validation, and LEP population baseline work across a two-year arc. IRB study ongoing.</p>
      <span class="tl-tag">Health-System Research Collaboration &middot; National Expansion</span>""",
     """      <div class="tl-name">Medicaid Plans and Health Systems</div>
      <p class="tl-body">Vasl Health PBC now sells to Medicaid plans and health systems. Vasl Bridge follows patients by text from emergency discharge to the first visit, with 10 of 10 steps passed live and real texts delivered. Vasl Keep helps eligible Medicaid members keep the coverage they qualify for. VLAP reads 55 signals across seven dimensions and scores 0.97 F1 on substance use on the n2c2 2022 SHAC test, 518 notes, against 0.83 for a keyword rule.</p>
      <span class="tl-tag">Vasl Bridge &middot; Vasl Keep &middot; VLAP</span>""", 1),

    # Chapter 03, how VLAP works
    ("""      The language youth<br>""", """      The language patients<br>""", 1),
    ("VLAP, the Vasl Language Analysis Platform, detects culturally specific distress signals across six clinical categories. It processes language youth share through their care channels and surfaces interpretive context to licensed clinicians before sessions begin. It does not diagnose. It does not prescribe. It does not respond to members. It is a precision interpretation instrument, clinician-facing only.",
     "VLAP, the Vasl Language Analysis Platform, is our own language model, with our own weights. It reads patient messages, text replies, clinician notes and scribe text, and flags 55 signals across seven dimensions (Taxonomy v2.0), each with the words behind it. It does not diagnose. It does not prescribe. It does not respond to patients. What the clinician and care team get is a named signal with the words behind it, never a score or a diagnosis.", 1),
    ("Signal context surfaces to licensed clinicians only, never to members, school staff, or administrators",
     "Signal context surfaces to the clinician and care team only. Outside parties see nothing.", 1),
    ("is a documented pre-disclosure frame in youth language, a hedge",
     "is a documented pre-disclosure frame in patient language, a hedge", 1),
    ("""      <div class="vmn-num">47</div>
      <div class="vmn-label">Clinical signals<br>across 6 categories</div>""",
     """      <div class="vmn-num">55</div>
      <div class="vmn-label">Signals across<br>seven dimensions</div>""", 1),

    # Chapter 04, partners
    ("Vasl works with healthcare systems, research institutions, and community organizations that are already doing the work of mental health equity and need the platform infrastructure to do it better. These are active deployments, research collaborations, and clinical validation relationships.",
     "Vasl works with research institutions and community organizations that are already doing the work of mental health equity. These are research and community relationships.", 1),
    ("""      <div class="partners-col-label">Healthcare & Research</div>""",
     """      <div class="partners-col-label">Research</div>""", 1),
    ("""        <div class="partner-item">
          <div class="partner-desc">Active IRB study validating VLAP clinical signal accuracy in production deployment</div>
        </div>
""", "", 1),

    # Chapter 05, compliance
    ("Clinical platforms serving minors, Medicaid populations, and school-based programs operate in one of the most demanding compliance environments in software.",
     "Clinical platforms serving Medicaid plans and health systems operate in one of the most demanding compliance environments in software.", 1),
    ("""      <div class="comp-label">HIPAA</div>""", """      <div class="comp-label">HIPAA, BAA</div>""", 1),
    ("Business Associate Agreement required before any partner deployment. Annual SOC 2 Type II audit. VLAP processes language in-memory without verbatim storage.",
     "We sign a business associate agreement before any patient data is shared. Patient text is read by VLAP on Vasl infrastructure and never sent to an outside AI company.", 1),
    ("""      <div class="comp-label">FERPA</div>
      <div class="comp-title">Student education records protected. No individual data shared with school staff.</div>
      <p class="comp-body">Vasl operates as a direct service provider to students, not as an agent of the school district. Student health records are protected under HIPAA architecture and never disclosed to administrators, teachers, or parents without explicit student consent. FERPA-compliant data handling for all school and university partnerships.</p>
      <div class="comp-details">
        <span class="comp-detail">Educational record security</span>
        <span class="comp-detail">Parental consent processes, minor-specific</span>
        <span class="comp-detail">No individual data to school administrators</span>""",
     """      <div class="comp-label">21st Century Cures Act</div>
      <div class="comp-title">Non-device clinical decision support. A named signal, never a score or a diagnosis.</div>
      <p class="comp-body">VLAP produces a named signal with the words behind it, never a score or a diagnosis. It is non-device clinical decision support under Section 3060 of the 21st Century Cures Act. The clinician decides. Signal data goes to the clinician and care team only, and outside parties see nothing.</p>
      <div class="comp-details">
        <span class="comp-detail">Section 3060</span>
        <span class="comp-detail">The words behind every signal</span>
        <span class="comp-detail">The clinician decides</span>""", 1),
    ("""      <div class="comp-label">SOC 2 Type II</div>
      <div class="comp-title">Annual third-party security audit. Full report available under NDA.</div>
      <p class="comp-body">SOC 2 Type II certification covering security, availability, and confidentiality trust service criteria. Independent third-party audit conducted annually. Report available to clinical and institutional partners under NDA upon request. Processing integrity and confidentiality measures fully documented.</p>
      <div class="comp-details">
        <span class="comp-detail">Security and availability controls</span>
        <span class="comp-detail">Processing integrity</span>
        <span class="comp-detail">Confidentiality measures</span>""",
     """      <div class="comp-label">HL7 FHIR R4</div>
      <div class="comp-title">Intake from Epic, Cerner and athenahealth. No new screen to learn.</div>
      <p class="comp-body">VLAP reads clinical notes over HL7 FHIR R4 from Epic, Cerner and athenahealth. A flagged signal with the exact words behind it is delivered into the workflow your teams already run. There is no new screen to learn.</p>
      <div class="comp-details">
        <span class="comp-detail">Epic, Cerner, athenahealth</span>
        <span class="comp-detail">Delivered into your workflow</span>
        <span class="comp-detail">No new screen</span>""", 1),
    ("across all portals, Member App, Coach Portal, and Client Org Portal.",
     "across every screen it ships.", 1),
    ("""        <span class="comp-detail">Color contrast standards, all portals</span>""",
     """        <span class="comp-detail">Color contrast standards</span>""", 1),
    ("""      <div class="comp-title">Full accessibility compliance across all platform portals.</div>""",
     """      <div class="comp-title">Full accessibility compliance across the platform.</div>""", 1),

    # Chapter 06, values
    ("Every feature is backed by rigorous research, clinical validation, and real-world outcomes data. Claims are stated with methodology. IRB study data, not projected benchmarks. The 0.83 and 23-of-47 figures are measurements on a held-out test split, against a published lexicon anyone can download.",
     "Every claim is backed by a measurement and stated with its method, not a projected benchmark. The 0.83 figure is measured on a held-out test split against MIT&rsquo;s Suicide Risk Lexicon, which anyone can download. The 0.97 F1 is measured on the n2c2 2022 SHAC test, 518 notes.", 1),
    ("Youth voices guide our development process. Not as a consultation checkbox, as a structural requirement. The peer group norms, the VLAP training corpus, the care model sequencing:",
     "Patient and community voices guide our development process. Not as a consultation checkbox, as a structural requirement. The VLAP training corpus, the Vasl Bridge and Vasl Keep texts, the care model sequencing:", 1),
    ("VLAP processes language in-memory without verbatim storage. Individual member data never reaches school staff or org administrators.",
     "Patient text is read by VLAP on Vasl infrastructure and never sent to an outside AI company. Individual patient data never reaches organizational administrators, and outside parties see nothing.", 1),

    # Chapter 07, recognition
    ("The numbers below are measurements against the field&rsquo;s published standard, not projected, not benchmarked from comparable platforms. Scored on a held-out test split. The work is ongoing. The IRB study is active. The scale is beginning.",
     "The numbers below are measurements against the field&rsquo;s published standard and a public clinical test set, not projected, not benchmarked from comparable platforms. Scored on held-out test data. The work is ongoing.", 1),
    ("""        <a href="/contact" class="btn-light">Partner With Us</a>""",
     """        <a href="/contact" class="btn-light">Talk to us about a pilot</a>""", 1),
    ("""          <div class="impact-num">23 of 47</div>
              <div class="impact-label">Distinct Vocabulary</div>
              <div class="impact-bench">signals with no counterpart in its 6,910 terms</div>""",
     """          <div class="impact-num">0.97</div>
              <div class="impact-label">Substance Use in Notes</div>
              <div class="impact-bench">F1, n2c2 2022 SHAC test, 518 notes, vs. 0.83 keyword rule</div>""", 1),
    ("""          <div class="impact-num">90<span style="font-size:24px">%</span></div>
          <div class="impact-label">Signal Sensitivity</div>
          <div class="impact-bench">High-distress detection accuracy</div>""",
     """          <div class="impact-num">55</div>
          <div class="impact-label">Signals, Seven Dimensions</div>
          <div class="impact-bench">each with the words behind it</div>""", 1),
    ("""          <div class="impact-num">Day one</div>
          <div class="impact-label">Peer Community and a Coach</div>
          <div class="impact-bench">from the day of enrollment</div>""",
     """          <div class="impact-num">10 of 10</div>
          <div class="impact-label">Vasl Bridge Steps Passed Live</div>
          <div class="impact-bench">real texts delivered</div>""", 1),

    # Related reading
    ("The literature, the active IRB study, and how we handle claims we can't yet support.",
     "The literature, the measurements, and how we handle claims we can't yet support.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"about: {len(PAIRS)} pairs applied")
