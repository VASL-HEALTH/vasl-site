"""Research page: new message into the existing design. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/research.html")
s = P.read_text(encoding="utf-8")

OLD_DESC = ("The peer-reviewed literature Vasl is built on, the active IRB study underway with a "
            "university partner, and how we handle claims we cannot yet support.")
NEW_DESC = ("How Vasl measures VLAP: 0.83 vs 0.65 against MIT's Suicide Risk Lexicon on "
            "suicide-attempt severity, 0.97 F1 on substance use in clinical notes, and how we "
            "handle claims we cannot yet support.")

PAIRS = [
    # meta, og, twitter
    (OLD_DESC, NEW_DESC, 3),

    # HERO body
    ("Vasl's research program, on how Black, Brown, LGBTQ+, rural and Medicaid youth describe distress, is in its early stages which is the honest description of where we are. We have one active IRB study, one active data collaboration with a leading academic medical center, and a clinical advisory relationship with Johns Hopkins. Peer-reviewed publication is in progress.",
     "Vasl&rsquo;s research asks how Black, Brown, LGBTQ+, rural and Medicaid patients describe distress in the words they actually use. It is early, and that is the honest description of where we are. We have two measured results on held-out test data: 0.83 vs 0.65 ROC-AUC against MIT&rsquo;s Suicide Risk Lexicon on suicide-attempt severity, and 0.97 F1 on substance use in clinical notes. We have a clinical advisory relationship with Johns Hopkins. Peer-reviewed publication is in progress.", 1),
    ('<a href="#active" class="btn-dark">Active Research</a>',
     '<a href="#active" class="btn-dark">Measured Results</a>', 1),

    # HERO status summary
    ("""        <span class="ss-status ss-active">Active</span>
        <div class="ss-right">
          <div class="ss-title">IRB Study, University Research Partner</div>
          <div class="ss-desc">VLAP signal detection accuracy validation against clinician-adjudicated ground truth. Results pending peer-reviewed publication.</div>""",
     """        <span class="ss-status ss-active">Measured</span>
        <div class="ss-right">
          <div class="ss-title">Suicide-Attempt Severity, VLAP vs MIT&rsquo;s Lexicon</div>
          <div class="ss-desc">0.83 vs 0.65 ROC-AUC against MIT&rsquo;s Suicide Risk Lexicon. Same corpus, same split, held-out test.</div>""", 1),
    ("""        <span class="ss-status ss-active">Active</span>
        <div class="ss-right">
          <div class="ss-title">Health-System Data Collaboration</div>
          <div class="ss-desc">Two-year data collaboration with an academic medical center, Year 1 model development, Year 2 prospective validation. HL7 FHIR behavioral health data infrastructure.</div>""",
     """        <span class="ss-status ss-active">Measured</span>
        <div class="ss-right">
          <div class="ss-title">Substance Use in Clinical Notes</div>
          <div class="ss-desc">0.97 F1 on the n2c2 2022 SHAC test, 518 notes, against 0.83 for a keyword rule.</div>""", 1),
    ("IRB study results will be published in a peer-reviewed journal upon study completion. Timeline subject to study progress.",
     "Both results are being prepared for submission to a peer-reviewed journal. Timeline subject to review.", 1),

    # CHAPTER 01
    ("Chapter 01, Active Research", "Chapter 01, Measured Results", 1),
    ("""      Two active<br>
      <em>collaborations.</em>""",
     """      Two measured<br>
      <em>results.</em>""", 1),
    ("Both are operational, not announced, not aspirational. The university research partner IRB study is in active data collection. The academic medical center data collaboration is in its first year of a two-year arc. These are the two research foundations that underpin every VLAP accuracy claim on this site.",
     "Both are measured, not projected. Each was scored on held-out test data against the reference a reviewer would choose, and each names its corpus, its split and what it was compared against. These two results underpin every VLAP accuracy claim on this site.", 1),

    # Study row 1
    ("<!-- UMD Study -->", "<!-- Suicide-attempt severity -->", 1),
    ("""      <span class="sr-status-badge sr-active">Active &middot; IRB</span>
      <div class="sr-type">Clinical Validation</div>
      <a href="mailto:research@gotovasl.com?subject=IRB Study Inquiry" class="sr-link">Request documentation</a>""",
     """      <span class="sr-status-badge sr-active">Measured &middot; Held-out test</span>
      <div class="sr-type">Benchmark</div>
      <a href="mailto:research@gotovasl.com?subject=Measurement Report Inquiry" class="sr-link">Request documentation</a>""", 1),
    ('<div class="sr-title">VLAP Clinical Signal Validation Study, University Research Partner</div>',
     '<div class="sr-title">Suicide-Attempt Severity, VLAP vs MIT&rsquo;s Suicide Risk Lexicon</div>', 1),
    ("An IRB-approved study validating VLAP's signal detection accuracy against clinician-adjudicated ground truth assessments. The study uses production deployment data from live Vasl cohorts, real members, real language, real clinical annotations by licensed clinicians with community competency training. This is the primary independent validation of VLAP's culturally specific signal detection capabilities. Results will be published in a peer-reviewed journal upon study completion.",
     "In 2026, MIT&rsquo;s McGovern Institute, the Child Mind Institute and Crisis Text Line published the Suicide Risk Lexicon, the field&rsquo;s reference standard for risk language. We measured VLAP against it, scoring both on the same corpus, the same split, the same way. VLAP reached 0.83 ROC-AUC on suicide-attempt severity. The lexicon reached 0.65. The first write-up is on our blog: <a href=\"/blog/what-a-suicide-risk-word-list-cant-hear\" style=\"color:var(--deep-green);text-decoration:none;border-bottom:1px solid rgba(45,74,62,0.3)\">what a suicide-risk word list can&rsquo;t hear</a>.", 1),
    ("""          <div class="srd-label">Institution</div>
          <div class="srd-value"><strong>Partner name withheld pending joint publicity approval</strong></div>""",
     """          <div class="srd-label">Reference</div>
          <div class="srd-value"><strong>MIT / Child Mind / Crisis Text Line Suicide Risk Lexicon</strong>, 50 constructs, 6,910 terms</div>""", 1),
    ("""          <div class="srd-label">Study Type</div>
          <div class="srd-value">IRB-approved observational validation study</div>""",
     """          <div class="srd-label">Study Type</div>
          <div class="srd-value">Head-to-head comparison, same corpus, same split</div>""", 1),
    ("""          <div class="srd-label">Data Source</div>
          <div class="srd-value">Production deployment data from live Vasl cohorts, de-identified</div>""",
     """          <div class="srd-label">Data Source</div>
          <div class="srd-value">Held-out test split, chunk level, n_pos 307</div>""", 1),
    ("""          <div class="srd-value">VLAP signal sensitivity vs. clinician-adjudicated ground truth</div>""",
     """          <div class="srd-value">ROC-AUC on suicide-attempt severity</div>""", 1),
    ("""          <div class="srd-label">Preliminary Finding</div>
          <div class="srd-value"><strong>90% sensitivity</strong> on high-distress signal detection, preliminary, pending publication</div>""",
     """          <div class="srd-label">Result</div>
          <div class="srd-value"><strong>0.83 vs 0.65</strong> ROC-AUC, VLAP vs the lexicon. Higher is better.</div>""", 1),
    ("""          <div class="srd-value">Active data collection &middot; Results pending peer-reviewed publication</div>""",
     """          <div class="srd-value">Measured &middot; Being prepared for peer-reviewed publication</div>""", 1),

    # Study row 2
    ("<!-- Health-System Data Collaboration -->", "<!-- Substance use in clinical notes -->", 1),
    ("""      <span class="sr-status-badge sr-active">Active &middot; Year 1</span>
      <div class="sr-type">Data Collaboration</div>
      <a href="mailto:research@gotovasl.com?subject=Health-System Collaboration Inquiry" class="sr-link">Request brief</a>""",
     """      <span class="sr-status-badge sr-active">Measured &middot; Held-out test</span>
      <div class="sr-type">Benchmark</div>
      <a href="mailto:research@gotovasl.com?subject=Substance Use Measurement Inquiry" class="sr-link">Request brief</a>""", 1),
    ('<div class="sr-title">Academic Medical Center, Two-Year Data Collaboration</div>',
     '<div class="sr-title">Substance Use in Clinical Notes, n2c2 2022 SHAC Test</div>', 1),
    ("Vasl Health is an active participant in a structured data-collaboration program with an academic medical center's research accelerator. The collaboration provides access to de-identified behavioral health data infrastructure for VLAP model development and validation. The two-year arc is structured specifically to support VLAP's NLP training, validation, and LEP (Limited English Proficiency) population baseline work, with Year 1 focused on model development and Year 2 on prospective validation. Partner name withheld pending joint publicity approval.",
     "Clinical notes are one of the four kinds of text VLAP reads, with patient messages, text replies and scribe text. We measured VLAP on the test set of the 2022 National NLP Clinical Challenges (n2c2) Social History Annotation Corpus (SHAC): 518 clinical notes labeled by human annotators. VLAP flagged substance use with 0.97 F1. A keyword rule on the same notes reached 0.83.", 1),
    ("""          <div class="srd-label">Data Domains</div>
          <div class="srd-value">BH encounters, ICD-10 (mood/anxiety/trauma/SUD), PHQ-9/GAD-7/PCL-5/AUDIT/DAST, demographics/SDoH</div>""",
     """          <div class="srd-label">Test Set</div>
          <div class="srd-value">n2c2 2022 SHAC test, 518 clinical notes labeled by human annotators</div>""", 1),
    ("""          <div class="srd-label">Format</div>
          <div class="srd-value">HL7 FHIR or CSV/JSON &middot; HIPAA Safe Harbor de-identification &middot; 12 to 36 months longitudinal</div>""",
     """          <div class="srd-label">Comparison</div>
          <div class="srd-value">Keyword rule, scored on the same notes</div>""", 1),
    ("""          <div class="srd-label">Year 1 Objective</div>
          <div class="srd-value">VLAP model development using behavioral health signal data</div>""",
     """          <div class="srd-label">Result</div>
          <div class="srd-value"><strong>0.97 F1</strong> vs 0.83 for the keyword rule</div>""", 1),
    ("""          <div class="srd-label">Year 2 Objective</div>
          <div class="srd-value">Prospective validation of VLAP signal accuracy</div>""",
     """          <div class="srd-label">Signal</div>
          <div class="srd-value">Substance use, one of 55 signals across seven dimensions (Taxonomy v2.0)</div>""", 1),

    # CHAPTER 02
    ("The research program is grounded in three active institutional relationships, each with a specific, documented role. These are not advisory relationships in name only. Each involves ongoing operational work, clinical oversight, or data access that directly informs VLAP's development and validation.",
     "The research rests on two published reference standards and one clinical advisory relationship. We measure VLAP against the benchmarks a reviewer would choose, and a senior clinician reviews how we frame what VLAP finds.", 1),
    ("""        <div class="fp-org-name">Academic Medical Center</div>
        <div class="fp-org-type">Health System &middot; Research Accelerator</div>""",
     """        <div class="fp-org-name">Suicide Risk Lexicon</div>
        <div class="fp-org-type">MIT McGovern Institute &middot; Child Mind Institute &middot; Crisis Text Line</div>""", 1),
    ('<div class="fp-relationship">Data Collaboration, Active Participant</div>',
     '<div class="fp-relationship">Published Reference Standard, Suicide-Attempt Severity</div>', 1),
    ("Access to de-identified behavioral health data infrastructure for VLAP model development and validation. Two-year structured collaboration, Year 1 model development, Year 2 prospective validation. Provides the data scale necessary for VLAP's NLP training on longitudinal behavioral health signals at clinical population level. Partner name withheld pending joint publicity approval.",
     "Published in 2026 as the field&rsquo;s reference standard for risk language: 50 constructs, 6,910 terms. We scored VLAP and the lexicon on the same corpus, the same split, the same way. VLAP reached 0.83 ROC-AUC on suicide-attempt severity. The lexicon reached 0.65.", 1),
    ('<span class="fp-badge">Active &middot; Year 1</span>', '<span class="fp-badge">Benchmark</span>', 1),
    ("""        <div class="fp-org-name">University Research Partner</div>
        <div class="fp-org-type">Research University &middot; IRB Study &middot; Name withheld pending joint publicity approval</div>""",
     """        <div class="fp-org-name">n2c2 2022 SHAC</div>
        <div class="fp-org-type">National NLP Clinical Challenges &middot; Social History Annotation Corpus</div>""", 1),
    ('<div class="fp-relationship">Active IRB Study, VLAP Signal Validation</div>',
     '<div class="fp-relationship">Public Clinical Benchmark, Substance Use</div>', 1),
    ("Independent academic validation of VLAP signal detection accuracy through an IRB-approved study comparing VLAP output against clinician-adjudicated ground truth. The study represents the first formal independent validation of VLAP's culturally specific signal detection capabilities. Results will be published in peer-reviewed literature upon completion.",
     "Clinical notes labeled by human annotators for substance use and other social history. On its test set of 518 notes, VLAP reached 0.97 F1 on substance use, against 0.83 for a keyword rule.", 1),
    ('<span class="fp-badge">IRB Active</span>', '<span class="fp-badge">Benchmark</span>', 1),

    # CHAPTER 03
    ("from the design of the IRB study to the way we report preliminary findings.",
     "from how we choose a benchmark to the way we report a result.", 1),
    ("No pilot has run, so no claim on this site reports pilot outcomes. Every measurement claim is drawn from a held-out test split or from active IRB research, not projected from internal estimates or aspirational targets. Where findings are preliminary, specifically VLAP signal accuracy, that is stated explicitly, with the caveat that results are pending peer-reviewed publication. We don't report IRB study findings before the study is complete.",
     "No pilot has run, so no claim on this site reports pilot outcomes. Every measurement claim is drawn from a held-out test split, not projected from internal estimates or aspirational targets. Each result names its corpus, its split and what it was compared against. Where a result is not yet published in a peer-reviewed journal, we say so.", 1),
    ("This standard is applied to the IRB validation study as a primary research outcome, not a secondary analysis.",
     "This standard applies to every result we report, as a primary outcome rather than a secondary analysis.", 1),
    ('<div class="ai-title">IRB oversight applies to every human subjects research activity</div>',
     '<div class="ai-title">Patient data is protected before any work begins</div>', 1),
    ("All research involving human subjects data, including the university research partner validation study and any future studies using Vasl deployment data, operates under IRB approval with informed consent, data privacy protection, and ongoing compliance monitoring. Institutional oversight is a minimum standard, not a credential for marketing purposes. The full IRB study protocol is available to qualified institutional evaluators under NDA.",
     "Any work with patient text runs under HIPAA, with a business associate agreement (BAA) signed before any patient data is shared. Patient text is read by VLAP on Vasl infrastructure and never sent to an outside AI company. Outside parties see nothing without explicit, documented consent. The full measurement report is available to qualified institutional evaluators under NDA.", 1),

    # CHAPTER 04
    ("Vasl Health does not currently have peer-reviewed publications. The IRB study with a university research partner is the primary vehicle for the first peer-reviewed publication. Here is what is in progress and when it is expected.",
     "Vasl Health PBC does not yet have peer-reviewed publications. The two measured results above are the first we will submit for peer review. Here is what is in progress.", 1),
    ('<div class="pn-title">VLAP Cultural Signal Detection Validation, University Research Partner IRB Study</div>',
     '<div class="pn-title">VLAP Measured Results, Suicide-Attempt Severity and Substance Use</div>', 1),
    ("The primary planned publication is the peer-reviewed results of the active IRB study with a university research partner, validating VLAP's signal detection accuracy against clinician-adjudicated ground truth in deployed pilot cohorts. The study uses production data from live Vasl deployments across BIPOC, LGBTQ+, and first-generation youth populations. Results will be submitted to a peer-reviewed journal upon study completion.",
     "The primary planned publication reports VLAP against MIT&rsquo;s Suicide Risk Lexicon on suicide-attempt severity (0.83 vs 0.65 ROC-AUC, same corpus, same split) and on substance use in the n2c2 2022 SHAC test (0.97 F1 on 518 notes, against 0.83 for a keyword rule). Results will be submitted to a peer-reviewed journal.", 1),
    ('<div class="pnd-item">Status: Active data collection</div>',
     '<div class="pnd-item">Status: Measured, write-up in preparation</div>', 1),
    ('<div class="pnd-item">Institution: Name withheld pending joint publicity approval</div>',
     '<div class="pnd-item">Authors: Vasl Health PBC</div>', 1),
    ('<div class="pnd-item">Target: Peer-reviewed journal submission upon completion</div>',
     '<div class="pnd-item">Target: Peer-reviewed journal submission</div>', 1),
    ("Study protocol and preliminary design documentation are available to institutional evaluators under NDA.",
     "The measurement report and method documentation are available to institutional evaluators under NDA.", 1),
    ("We will update this page when the study is submitted for publication and when it is published.",
     "We will update this page when the results are submitted for publication and when they are published.", 1),

    # COLLABORATE
    ("We bring the platform infrastructure, production deployment data, and community relationships.",
     "We bring VLAP, its measured results, and community relationships.", 1),
    ('<div class="cr-title">Platform, data, and community</div>',
     '<div class="cr-title">Model, results, and community</div>', 1),
    ("Production deployment data from live Vasl cohorts, BIPOC, LGBTQ+, and first-generation youth populations. The VLAP model and its clinical signal taxonomy. Community relationships built through years of co-design. Health-system-grade data infrastructure for behavioral health signal data at scale, via an active academic medical center collaboration.",
     "VLAP, our own language model with our own weights, and its clinical signal taxonomy: 55 signals across seven dimensions (Taxonomy v2.0). Measured results on held-out clinical benchmarks. Community relationships built through years of co-design. Intake over HL7 FHIR R4 from Epic, Cerner and athenahealth, under HIPAA and a business associate agreement.", 1),
    ("IRB-approved research protocols. Clinical expertise",
     "Human subjects review for any study involving patients. Clinical expertise", 1),
    ("37-page VLAP technical specification. IRB study protocol. Signal taxonomy",
     "37-page VLAP technical specification. Signal taxonomy", 1),
    (" Model measurement report: corpus, split, figures and limitations. Health-system data collaboration brief.</p>",
     " Model measurement report: corpus, split, figures and limitations.</p>", 1),

    # Related reading (no pilot has run)
    ("PHQ-8 change, retention, and escalation rates from pilot cohorts, with methodology.",
     "The outcomes a pilot measures, and the methodology behind them.", 1),
]

for old, new, n in PAIRS:
    got = s.count(old)
    assert got == n, f"expected {n}, found {got}: {old[:80]!r}"
    s = s.replace(old, new)

assert "—" not in s and "&mdash;" not in s and "&#8212;" not in s, "em dash present"
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
