"""Technology page: new message into the existing design. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/technology.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # CSS comment only (no style change)
    ("/* Category blocks (47-signal taxonomy) */", "/* Category blocks (taxonomy examples) */", 1),

    # ── HERO ──
    (" Standard NLP models are trained on majority-White internet text. They were never designed to read how Black, Brown, LGBTQ+, rural and Medicaid youth communicate distress and they consistently fail to. VLAP was built specifically for those communities. Not adapted. Built.",
     " Standard language models are trained on textbook and internet English. They were never designed to read how Black, Brown, LGBTQ+, rural and Medicaid patients describe what they are going through, and they are least accurate for exactly those patients. VLAP is our own language model, with our own weights, built on them first. Not adapted. Built.", 1),
    ('<div class="ab-label">High-Distress Signal Sensitivity</div>',
     '<div class="ab-label">Suicide-Attempt Severity, ROC-AUC</div>', 1),
    ('<div class="ab-num">90<span>%</span></div>',
     '<div class="ab-num">0.83<span> vs 0.65</span></div>', 1),
    ("On high-distress signal detection in active IRB validation with a university research partner. Specificity and predictive-value results will be published with the completed study because half a statistic isn&rsquo;t transparency.",
     "VLAP against MIT&rsquo;s Suicide Risk Lexicon, the field&rsquo;s reference, on the same corpus and the same split. On substance use, VLAP scores 0.97 F1 on the n2c2 2022 SHAC test, 518 notes, against 0.83 for a keyword rule.", 1),
    ('<div class="ab-caveat">Active validation &middot; Results pending &middot; Non-diagnostic output</div>',
     '<div class="ab-caveat">Same corpus &middot; Same split &middot; Non-diagnostic output</div>', 1),
    ('''        <div class="hs-num">2,400<span style="font-size:16px">+</span></div>
        <div class="hs-label">AAVE and youth vernacular tokens added beyond standard BERT-family vocabulary</div>''',
     '''        <div class="hs-num">0.97</div>
        <div class="hs-label">F1 on substance use, n2c2 2022 SHAC test, 518 notes</div>''', 1),
    ('''        <div class="hs-num">47</div>
        <div class="hs-label">Clinical signals across 6 categories</div>''',
     '''        <div class="hs-num">55</div>
        <div class="hs-label">Signals across seven dimensions (Taxonomy v2.0)</div>''', 1),
    ('''        <div class="hs-num">5</div>
        <div class="hs-label">Cultural communities represented in the training annotation cohort</div>''',
     '''        <div class="hs-num">0</div>
        <div class="hs-label">Patient text sent to an outside AI company</div>''', 1),

    # ── CHAPTER 01 ──
    ("Standard models therefore miss the specific ways Black and Latino, LGBTQ+, and first-generation youth signal emotional distress.",
     "Standard models therefore miss the specific ways Black and Latino, LGBTQ+, rural, and first-generation patients signal emotional distress.", 1),
    ('In clinical practice, it means a youth saying "lowkey been struggling fr" is read as casual.',
     'In clinical practice, it means a patient saying "lowkey been struggling fr" is read as casual.', 1),
    ('"it\'s not that deep but lowkey been struggling since school started."',
     '"it\'s not that deep but lowkey been struggling since I got laid off."', 1),

    # ── CHAPTER 02 ──
    ("VLAP analyzes the language members choose to share on the platform, check-ins, peer-group messages, coach conversations. It looks for 47 clinical signals across 6 categories: patterns like pre-disclosure minimization, withdrawal, and escalating distress, expressed the way young people actually express them.",
     "VLAP reads patient messages, text replies, clinician notes and scribe text: replies to Vasl Bridge texts, and notes over HL7 FHIR R4 from Epic, Cerner and athenahealth. It flags 55 signals across seven dimensions (Taxonomy v2.0), from behavioral health risk to substance use and social needs: patterns like pre-disclosure minimization, withdrawal, and escalating distress, expressed the way patients actually express them.", 1),
    ("It never diagnoses. It never labels or scores a young person. It never sends alerts to police, principals, or parents. It never shows individual conversations to schools or funders. Every escalation goes to one place only: a licensed clinician, who reviews the full context before anything happens.",
     "It never diagnoses. It never labels or scores a patient. It never sends alerts to police, employers, or family. It never shows individual conversations to outside parties. Every flag goes to the clinician and care team responsible for the patient, who review the full context before anything happens.", 1),
    ("Members see their own experience. Coaches see the context they need to reach out well. Licensed clinicians see signal context before sessions. Organizations see only aggregate, de-identified trends, never an individual young person.",
     "Patients see their own messages. Coaches see the context they need to reach out well. Clinicians see a named signal with the words behind it, in the workflow they already run. Plan and health-system leadership see only aggregate, de-identified totals. Outside parties see nothing.", 1),
    ("Our signal accuracy and member outcomes are being independently validated through an IRB-approved study with a university research partner. We publish our measurement definitions, and when the study concludes, we&rsquo;ll publish what it finds, including accuracy across demographic groups.",
     "We measure VLAP against the field&rsquo;s reference tools on the same data. On suicide-attempt severity, it scores 0.83 ROC-AUC against 0.65 for MIT&rsquo;s Suicide Risk Lexicon, same corpus, same split. On substance use, it scores 0.97 F1 on the n2c2 2022 SHAC test, 518 notes, against 0.83 for a keyword rule. We publish our measurement definitions with each result.", 1),
    ("Written for a parent as much as a clinician, see the",
     "Written for a patient&rsquo;s family as much as a clinician, see the", 1),

    # ── CHAPTER 03 ──
    ('''      Built on BERT-family.<br>
      Fine-tuned for<br>
      <em>cultural fluency.</em>''',
     '''      Our own model.<br>
      Trained for<br>
      <em>cultural fluency.</em>''', 1),
    ("VLAP is a fine-tuned BERT-family transformer model, trained on a purpose-built corpus of culturally specific mental health language. The BERT-family architecture was selected for its bidirectional context processing, essential for reading the layered meaning in code-switching, minimization patterns, and culturally framed expressions where individual words carry different weight depending on surrounding context. The model was then extended with a culturally specific vocabulary and fine-tuned against a clinically annotated training corpus.",
     "VLAP is our own language model, with our own weights, trained on a purpose-built corpus of culturally specific behavioral health language. It reads the layered meaning in code-switching, minimization patterns, and culturally framed expressions, where individual words carry different weight depending on surrounding context. Patient text is read on Vasl infrastructure and never sent to an outside AI company.", 1),
    ('<div class="al-title">BERT-Family Base Architecture, Bidirectional Transformer</div>',
     '<div class="al-title">Our Own Model, Our Own Weights</div>', 1),
    ('The bidirectional encoding layer processes the full context window simultaneously in both directions, unlike unidirectional models that read left-to-right. This is architecturally necessary for cultural signal detection:',
     'VLAP reads each message as a whole, so every word is weighed by what surrounds it. That matters for cultural signal detection:', 1),
    ('<div class="al-tech">BERT-family base &middot; fine-tuned &middot; behavioral health corpus</div>',
     '<div class="al-tech">Own model &middot; Own weights &middot; Behavioral health corpus</div>', 1),
    ('<div class="al-title">Vocabulary Extension, 2,400+ Cultural Tokens</div>',
     '<div class="al-title">Vocabulary Built With the Communities</div>', 1),
    ('Standard BERT-family vocabulary was extended with 2,400+ AAVE terms, youth vernacular expressions, code-switching patterns, and community-developed coded language, including terms built specifically to circumvent content filters (e.g., "unaliving"). This extension was compiled through community engagement with BIPOC and LGBTQ+ youth populations and validated by licensed clinicians with relevant community competency. Without this extension, approximately 23% of the training corpus would be processed as unknown tokens by the base model.',
     'VLAP&rsquo;s vocabulary covers African American Language, rural speech, queer vernacular, code-switching patterns, and community-developed coded language, including terms built specifically to get past content filters (e.g., "unaliving"). It was compiled through community engagement with BIPOC, LGBTQ+, and rural communities and validated by licensed clinicians with relevant community competency. Standard models read much of this language as unknown words or as noise.', 1),
    ("The extended BERT-family model was fine-tuned on annotated language samples drawn from the communities VLAP serves,",
     "VLAP was trained on annotated language samples drawn from the communities it serves,", 1),
    ("against the 47-signal taxonomy across six clinical categories.",
     "against the VLAP taxonomy, now 55 signals across seven dimensions (Taxonomy v2.0).", 1),
    ('<div class="al-title">Dimensional Signal Profiling, Non-Diagnostic Output Layer</div>',
     '<div class="al-title">Named Signals, Non-Diagnostic Output Layer</div>', 1),
    ("The model output layer generates dimensional signal profiles across the six-category taxonomy, not diagnostic outputs, not severity scores, and not clinical recommendations. The output is an interpretive context package containing which signal patterns are present, their dimensional classification, and cultural interpretation notes that help clinicians understand what the patterns typically indicate in the communities that produce them. Every output includes a non-diagnostic disclaimer and is designed to support clinical judgment, not substitute for it.",
     "The output layer generates named signals across the seven dimensions, each with the words behind it. Not diagnostic outputs, not scores, and not clinical recommendations. The output shows which signal patterns are present, the exact words behind each, and cultural interpretation notes that help clinicians understand what the patterns typically indicate in the communities that produce them. VLAP is non-device clinical decision support under Section 3060 of the 21st Century Cures Act, built to support clinical judgment, not substitute for it.", 1),
    ('<div class="al-tech">Non-diagnostic &middot; Interpretive context &middot; 47-signal taxonomy &middot; Clinician-surfaced only</div>',
     '<div class="al-tech">Non-diagnostic &middot; Words behind every flag &middot; 55 signals, seven dimensions &middot; Clinician-facing</div>', 1),
    ('<div class="al-title">In-Memory Processing, No Verbatim Storage</div>',
     '<div class="al-title">Read on Vasl Infrastructure, Never Sent Out</div>', 1),
    ("VLAP processes member language in-memory. Verbatim input text is not stored after signal profile generation. The retained output is a dimensional signal profile, not a transcript, not a quote, not a record of the member's exact language. This architectural constraint is a HIPAA technical safeguard, not a configurable setting. It cannot be disabled by organizational administrators or overridden by clinical staff.",
     "VLAP reads patient text on Vasl infrastructure. Patient text is never sent to an outside AI company. The output is a named signal with the words behind it, delivered only to the clinician and care team responsible for the patient. This architectural constraint is a HIPAA technical safeguard, not a configurable setting. It cannot be disabled by organizational administrators or overridden by clinical staff.", 1),
    ('<div class="al-tech">In-memory inference &middot; No PHI retention post-processing &middot; HIPAA technical safeguard</div>',
     '<div class="al-tech">Vasl infrastructure &middot; No outside AI company &middot; HIPAA technical safeguard</div>', 1),

    # ── CHAPTER 04 ──
    ('''        <div class="tg-stat-num">2,400<span style="font-size:24px">+</span></div>
        <div class="tg-stat-label">Extended vocabulary tokens beyond base BERT-family vocabulary</div>''',
     '''        <div class="tg-stat-num">55</div>
        <div class="tg-stat-label">Signals across seven dimensions (Taxonomy v2.0)</div>''', 1),
    ('''        <div class="tg-stat-num">47</div>
        <div class="tg-stat-label">Distress signal patterns across 6 clinical categories</div>''',
     '''        <div class="tg-stat-num">518</div>
        <div class="tg-stat-label">Clinical notes in the n2c2 2022 SHAC test, where VLAP scores 0.97 F1 on substance use</div>''', 1),
    ("serving Black, Latino, LGBTQ+, first-generation, and youth in urban and rural communities,",
     "serving Black, Latino, LGBTQ+, and first-generation people in urban and rural communities,", 1),
    ("The 2,400+ vocabulary extension was compiled through structured engagement with youth from the target communities,",
     "The vocabulary was compiled through structured engagement with people from the target communities,", 1),

    # ── CHAPTER 05 TAXONOMY ──
    ("Chapter 05, The 47-Signal Distress Signal Taxonomy", "Chapter 05, The VLAP Signal Taxonomy, v2.0", 1),
    ('''      47 signals.<br>
      <em>Six categories.</em>''',
     '''      55 signals.<br>
      <em>Seven dimensions.</em>''', 1),
    ("The VLAP Distress Signal Taxonomy (v1.0) is the clinical reference document behind VLAP, it defines the 47 discrete linguistic, behavioral, and contextual signals VLAP is trained to detect, organized into six clinically grounded categories. It serves as the model specification, the annotation codebook for IRB study data labeling, and the signal-level evidence base for VLAP&rsquo;s NIMH SBIR Phase I application. The taxonomy is updated as language evolves and as clinical review proceeds.",
     "The VLAP Signal Taxonomy (v2.0) is the clinical reference document behind VLAP. It defines 55 linguistic, behavioral, and contextual signals across seven dimensions, from behavioral health risk to substance use and social needs. It serves as the model specification, the annotation codebook, and the signal-level evidence base for VLAP&rsquo;s NIMH SBIR Phase I application. The signals below are illustrative examples of how VLAP reads culturally specific distress, not the full taxonomy. The taxonomy is updated as language evolves and as clinical review proceeds.", 1),
    ('<div class="cat-signal-count">9 signals</div>', '<div class="cat-signal-count">Examples</div>', 1),
    ('<div class="cat-signal-count">8 signals</div>', '<div class="cat-signal-count">Examples</div>', 3),
    ('<div class="cat-signal-count">7 signals</div>', '<div class="cat-signal-count">Examples</div>', 2),
    ("The 47-signal taxonomy is justified by performance on SHA-02 through SHA-08 and the other five categories, not SHA-01.",
     "The taxonomy is justified by performance on SHA-02 through SHA-08 and the other dimensions, not SHA-01.", 1),
    ("Flags for V2 cross-session modeling.", "Flags for cross-session modeling.", 1),
    ("For LGBTQIA+ youth, this expression carries", "For LGBTQIA+ patients, this expression carries", 1),
    ("Specific to first-generation and immigrant youth, the weight", "Specific to first-generation and immigrant patients, the weight", 1),
    ("CRITICAL, youth-specific euphemism developed explicitly", "CRITICAL, euphemism developed explicitly", 1),
    ("'ending the run' are youth-vernacular constructions.", "'ending the run' are vernacular constructions.", 1),
    ("Particularly significant in youth who have previously disclosed to an adult and experienced a negative response.",
     "Particularly significant in patients who have previously disclosed to someone and experienced a negative response.", 1),
    ("Particularly documented in Black, Latino, and LGBTQIA+ youth. The comparison",
     "Particularly documented in Black, Latino, and LGBTQIA+ communities. The comparison", 1),
    ("VLAP adds detection of AAVE and youth-vernacular variants.", "VLAP adds detection of AAVE and other vernacular variants.", 1),
    ("Documented psychological stressor specific to Black, Latino, and LGBTQIA+ youth, the exhaustion",
     "Documented psychological stressor specific to Black, Latino, and LGBTQIA+ people, the exhaustion", 1),
    ("particularly painful for youth who experience intersectional marginalization.",
     "particularly painful for people who experience intersectional marginalization.", 1),
    ("Withdrawal from digital social spaces, for youth, digital social networks are primary social infrastructure.",
     "Withdrawal from digital social spaces, for many younger patients, digital social networks are primary social infrastructure.", 1),
    ("a documented trauma and acute stressor for urban youth.", "a documented trauma and acute stressor in urban communities.", 1),
    ("Housing instability is a strong predictor of youth mental health crisis,", "Housing instability is a strong predictor of mental health crisis,", 1),
    ("stressor for immigrant youth and families.", "stressor for immigrant families.", 1),
    ("stressors for Black and Latino youth disproportionately.", "stressors for Black and Latino communities disproportionately.", 1),
    ("Particularly significant for Black and Latino youth in communities with high rates of gun violence.",
     "Particularly significant for Black and Latino patients in communities with high rates of gun violence.", 1),
    ("connection to youth support resources.", "connection to caregiver support resources.", 1),
    ("longitudinal markers (V2 cross-session modeling)", "longitudinal markers (cross-session modeling)", 1),
    ("faith community, mentors, peer networks, cultural identity, and aspirational goals, are different from those in the clinical literature developed for White, middle-class youth populations.",
     "faith community, mentors, friendships, cultural identity, and aspirational goals, are different from those in the clinical literature developed for White, middle-class populations.", 1),
    ("For youth with limited trusted adult relationships, losing one trusted adult",
     "For patients with few trusted adults in their lives, losing one", 1),
    ("Particularly significant for first-generation youth for whom educational aspirations",
     "Particularly significant for first-generation patients for whom educational aspirations", 1),
    ("Cultural identity is a documented protective factor for BIPOC youth.", "Cultural identity is a documented protective factor in BIPOC communities.", 1),
    ("Particularly relevant in first-generation, immigrant, and mixed-heritage youth.",
     "Particularly relevant for first-generation, immigrant, and mixed-heritage patients.", 1),
    ("Primarily a V2 research agenda.", "Primarily a longitudinal research agenda.", 1),

    # ── CHAPTER 06 VALIDATION ──
    ('''      Validated against<br>
      real clinical<br>
      <em>populations.</em>''',
     '''      Measured against<br>
      the field&rsquo;s<br>
      <em>reference tools.</em>''', 1),
    ("VLAP's accuracy claims are grounded in active IRB-approved clinical research with a university research partner, not internal testing, not synthetic benchmarks, and not general NLP performance metrics that don't account for cultural signal specificity.",
     "VLAP&rsquo;s accuracy claims are measured head to head against the field&rsquo;s reference tools on the same data, on a held-out test split, with the corpus, the split and the limitations stated. Not projected targets, and not general NLP performance metrics that don't account for cultural signal specificity.", 1),
    ('''        <div class="val-metric-num">90<span style="font-size:24px">%</span></div>
        <div class="val-metric-label">High-distress signal sensitivity</div>''',
     '''        <div class="val-metric-num">0.83<span style="font-size:24px"> vs 0.65</span></div>
        <div class="val-metric-label">Suicide-attempt severity, ROC-AUC</div>''', 1),
    ("VLAP's ability to detect high-distress signals when they are present in member language, measured against clinician-adjudicated ground truth in the IRB study cohort. Sensitivity is optimized conservatively",
     "VLAP against MIT&rsquo;s Suicide Risk Lexicon, the field&rsquo;s reference, on the same corpus and the same split. The lexicon scores 0.65. Sensitivity is set conservatively", 1),
    ('''        <div class="val-metric-num">23<span style="font-size:24px">%</span></div>
        <div class="val-metric-label">Standard NLP vocabulary gap</div>
        <p class="val-metric-body">Percentage of the VLAP training corpus that would be processed as unknown tokens by a standard BERT model without the extended vocabulary, representing the portion of culturally specific language that standard models are structurally unable to read.</p>''',
     '''        <div class="val-metric-num">0.97<span style="font-size:24px"> F1</span></div>
        <div class="val-metric-label">Substance use in clinical notes</div>
        <p class="val-metric-body">On the n2c2 2022 SHAC test, 518 clinical notes, VLAP scores 0.97 F1 on substance use. A keyword rule scores 0.83 on the same notes.</p>''', 1),
    ('''        <div class="val-metric-label">Active IRB Study, University Research Partner</div>
        <p class="val-metric-body">VLAP signal accuracy is being validated through an IRB-approved clinical study with a university research partner, using production deployment data from live Vasl cohorts. The study compares VLAP signal output against clinician-adjudicated gold-standard assessments of the same member language. Results will be published in peer-reviewed literature upon study completion.</p>''',
     '''        <div class="val-metric-label">Head-to-Head Measurement</div>
        <p class="val-metric-body">Every result is measured against a named reference on the same data: MIT&rsquo;s Suicide Risk Lexicon for suicide-attempt severity, and a keyword rule for substance use on the n2c2 2022 SHAC test. Each result names its corpus, its split and what it was compared against.</p>''', 1),
    ("in both the training validation and the IRB study.", "in training validation and in every measurement.", 1),
    ('''      <div class="irb-label">IRB Study, University Research Partner</div>
      <p class="irb-body">The active IRB study is currently in the data collection and preliminary analysis phase. Results will be published in a peer-reviewed journal upon completion. The study protocol and preliminary design documentation are available to institutional evaluators under NDA. Contact clinical@gotovasl.com to request access.</p>''',
     '''      <div class="irb-label">Model Measurement Report</div>
      <p class="irb-body">The Model Measurement Report sets out the 0.83 vs 0.65 result on suicide-attempt severity and the 0.97 F1 result on substance use, with the corpus, the split and the limitations stated. It is available to institutional evaluators under NDA. Contact clinical@gotovasl.com to request access.</p>''', 1),

    # ── CHAPTER 07 CLINICAL INTEGRATION ──
    ('''      <div class="cf-title">Member check-in or coach message</div>
      <p class="cf-body">VLAP processes only language shared through Vasl's care channels, daily check-ins and coach messaging threads. Peer group posts, external social media, school email, and any other channel are not processed.</p>''',
     '''      <div class="cf-title">Patient reply or clinical note</div>
      <p class="cf-body">VLAP reads only text shared through the care channels a partner sets up: replies to Vasl Bridge texts, patient messages, and clinician notes and scribe text over HL7 FHIR R4 from Epic, Cerner and athenahealth. External social media and any other channel are not read.</p>''', 1),
    ('''      <div class="cf-title">In-memory VLAP inference</div>
      <p class="cf-body">VLAP processes the language against the 47-signal taxonomy. In-memory only, verbatim text is not retained after processing. Output: a dimensional signal profile.</p>''',
     '''      <div class="cf-title">VLAP reads on Vasl infrastructure</div>
      <p class="cf-body">VLAP reads the text across 55 signals in seven dimensions, on Vasl infrastructure. Patient text is never sent to an outside AI company. Output: a named signal with the words behind it.</p>''', 1),
    ('''      <div class="cf-title">AI Client Insights surface to coach dashboard</div>
      <p class="cf-body">Coaches see a simplified surface of VLAP output in the AI Client Insights panel: plain-language pattern alerts and mood trajectory summaries for their active members. No dimensional codes, no clinical jargon.</p>''',
     '''      <div class="cf-title">Signals land in the workflow the team already runs</div>
      <p class="cf-body">Signals are delivered into the workflow the care team already runs. No new screen to learn. Coaches and care coordinators see plain-language pattern alerts for the patients they follow. No dimensional codes, no clinical jargon.</p>''', 1),
    ('''      <div class="cf-title">Full dimensional panel surfaces to licensed clinician</div>
      <p class="cf-body">When a member is connected to a licensed clinician, the pre-session view includes the full VLAP dimensional signal profile, dimensional codes, pattern descriptions, cultural interpretation notes, and coaching context. Accessible only to licensed clinicians.</p>''',
     '''      <div class="cf-title">Full signal context surfaces to the clinician</div>
      <p class="cf-body">The clinician responsible for the patient sees each named signal, the exact words behind it, pattern descriptions, and cultural interpretation notes. The clinician decides.</p>''', 1),
    ('''      <div class="cf-title">High-risk escalations surface to clinical supervisor, 90-minute SLA</div>
      <p class="cf-body">Signals or signal combinations that meet High-risk escalation criteria are surfaced immediately to Vasl's licensed clinical supervisor team. A licensed clinician reviews the signal and determines the appropriate response. No automated action. Human judgment initiates every response.</p>''',
     '''      <div class="cf-title">High-risk signals surface for immediate clinician review</div>
      <p class="cf-body">Signals or signal combinations that meet High-risk escalation criteria surface immediately to the responsible clinician. A clinician reviews the signal and decides the response. No automated action. Human judgment starts every response.</p>''', 1),
    ('<div class="cd-item">Scan peer group posts or external channels</div>',
     '<div class="cd-item">Read social media or other outside channels</div>', 1),
    ('<div class="cd-item">Store verbatim member language after processing</div>',
     '<div class="cd-item">Send patient text to an outside AI company</div>', 1),
    ('<div class="cd-item">Surface individual signal data to school or org administrators</div>',
     '<div class="cd-item">Share individual signal data with outside parties</div>', 1),
    ('<div class="cd-item">Surface dimensional signal profiles to coaches and clinicians</div>',
     '<div class="cd-item">Deliver named signals, with the words behind them, to care teams</div>', 1),
    ('<div class="cd-item">Provide pre-session cultural context to licensed clinicians</div>',
     '<div class="cd-item">Provide cultural context to clinicians</div>', 1),
    ('<div class="cd-item">Support coaches with AI Client Insights summaries</div>',
     '<div class="cd-item">Give coaches plain-language pattern alerts</div>', 1),
    ('<div class="cd-item">Enable aggregate, de-identified population trend data for org dashboards</div>',
     '<div class="cd-item">Give plans and health systems aggregate, de-identified totals</div>', 1),
    ('<div class="cd-item">Process in-memory without verbatim PHI retention</div>',
     '<div class="cd-item">Read patient text on Vasl infrastructure</div>', 1),

    # ── CHAPTER 08 SECURITY ──
    ("VLAP processes the most sensitive category of user data, mental health language from youth in underserved communities. The security architecture was designed specifically for HIPAA-regulated, school-based, and community health deployment contexts.",
     "VLAP reads the most sensitive category of data there is, behavioral health language from patients in underserved communities. The security architecture was designed specifically for HIPAA-regulated Medicaid plan and health-system deployment.", 1),
    ('''      <div class="si-title">In-Memory Processing</div>
      <p class="si-body">VLAP processes member language in-memory. Verbatim input text is not stored after signal profile generation. The retained output is a dimensional signal profile, not a transcript, not a quote. This is a HIPAA technical safeguard, not a configurable setting.</p>''',
     '''      <div class="si-title">Vasl Infrastructure Only</div>
      <p class="si-body">Patient text is read by VLAP on Vasl infrastructure and never sent to an outside AI company. The output is a named signal with the words behind it, delivered only to the care team responsible for the patient. This is a HIPAA technical safeguard, not a configurable setting.</p>''', 1),
    ('<div class="si-code">02 &middot; HIPAA</div>', '<div class="si-code">02 &middot; HIPAA, BAA</div>', 1),
    ("Business Associate Agreement required for all organizational deployments. Annual third-party security audit.",
     "We sign a business associate agreement before any patient data is shared.", 1),
    ('''      <div class="si-code">03 &middot; Certification</div>
      <div class="si-title">SOC 2 Type II</div>
      <p class="si-body">Annual SOC 2 Type II audit covering security, availability, and confidentiality trust service criteria. Full audit report available to institutional evaluators under NDA. Audit conducted by an independent third-party auditor.</p>''',
     '''      <div class="si-code">03 &middot; Integration</div>
      <div class="si-title">HL7 FHIR R4</div>
      <p class="si-body">Intake over HL7 FHIR R4 from Epic, Cerner and athenahealth. Named signals are delivered into the workflow your teams already run. No new screen to learn.</p>''', 1),
    ("Individual VLAP signal context is accessible only to the assigned coach (AI Client Insights summary) and the assigned licensed clinician (full dimensional profile). School staff, org administrators, and Vasl team members outside clinical supervisory functions have zero access to individual signal data, architecturally enforced.",
     "Individual VLAP signal context is accessible only to the clinician and care team responsible for the patient. Outside parties, administrators outside the care team, and Vasl team members outside clinical supervisory functions have zero access to individual signal data, architecturally enforced.", 1),
    ('''      <div class="si-code">05 &middot; FERPA</div>
      <div class="si-title">School-Based Deployment</div>
      <p class="si-body">For school district deployments, Vasl operates as a direct service provider to students. Student health data generated in Vasl is classified as health information under HIPAA, not as an education record under FERPA, and is structurally inaccessible to school administrators under any circumstances.</p>''',
     '''      <div class="si-code">05 &middot; Regulatory</div>
      <div class="si-title">Non-Device Clinical Decision Support</div>
      <p class="si-body">VLAP is non-device clinical decision support under Section 3060 of the 21st Century Cures Act. It gives the clinician a named signal with the words behind it, never a score or a diagnosis, so the clinician can see the basis for every flag.</p>''', 1),
    ("Population-level aggregate signal trends surfaced to org administrators use minimum cohort size enforcement",
     "Population-level aggregate signal trends reported to plan and health-system administrators use minimum cohort size enforcement", 1),

    # ── CHAPTER 09 PARTNERSHIPS ──
    ('''      Validated by<br>
      the institutions<br>
      <em>that matter.</em>''',
     '''      Checked against<br>
      the references<br>
      <em>that matter.</em>''', 1),
    ("VLAP's clinical credibility is grounded in active institutional partnerships, not aspirational affiliations or advisory relationships that don't involve actual work. The partnerships listed below involve ongoing operational collaboration, active research, or formal clinical oversight.",
     "VLAP&rsquo;s clinical credibility rests on measurement against independent references and on formal clinical oversight, not aspirational affiliations or advisory relationships that don't involve actual work.", 1),
    ('''        <div class="part-org">Academic Research Partner</div>
        <div class="part-type">Research University, IRB Study</div>
      </div>
      <div class="part-body">
        <div class="part-relationship">Active IRB Study, VLAP Clinical Signal Validation</div>
        <p class="part-desc">An IRB-approved clinical study is in progress with an academic research partner validating VLAP's signal detection accuracy against clinician-adjudicated ground truth assessments. The study uses production deployment data from live Vasl cohorts. Results will be published in a peer-reviewed journal upon completion. The study represents the first formal independent validation of VLAP's culturally specific signal detection capabilities.</p>
      </div>
      <div class="part-status"><span class="part-status-badge psb-active">IRB Active</span></div>''',
     '''        <div class="part-org">Independent References</div>
        <div class="part-type">MIT Suicide Risk Lexicon &middot; n2c2 2022 SHAC</div>
      </div>
      <div class="part-body">
        <div class="part-relationship">Head-to-Head Measurement, Same Data</div>
        <p class="part-desc">On suicide-attempt severity, VLAP scores 0.83 ROC-AUC against 0.65 for MIT&rsquo;s Suicide Risk Lexicon, on the same corpus and the same split. On substance use, VLAP scores 0.97 F1 on the n2c2 2022 SHAC test, 518 notes, against 0.83 for a keyword rule. The Model Measurement Report states the corpus, the split and the limitations.</p>
      </div>
      <div class="part-status"><span class="part-status-badge psb-active">Measured</span></div>''', 1),

    # ── CHAPTER 10 ACCESS ──
    ("qualified institutional evaluators, health systems, research institutions, school district technology teams, and health plan medical directors.",
     "qualified institutional evaluators: Medicaid plans, health systems, research institutions, and health plan medical directors.", 1),
    ('<a href="/contact" class="btn-light">Request Evaluation Package</a>',
     '<a href="/contact" class="btn-light">Talk to us about a pilot</a>', 1),
    ("37-page model specification, architecture, training methodology, signal taxonomy with full annotation guidelines,",
     "37-page model specification, training methodology, signal taxonomy (v2.0) with full annotation guidelines,", 1),
    ('''          <div class="ad-title">IRB Study Protocol</div>
          <div class="ad-desc">IRB study design, methodology, data collection protocol, and preliminary validation framework. Results pending publication.</div>''',
     '''          <div class="ad-title">VLAP Signal Taxonomy, v2.0</div>
          <div class="ad-desc">55 signals across seven dimensions, with the definition, examples and annotation guidance behind each.</div>''', 1),
    ('''          <div class="ad-title">SOC 2 Type II Report</div>
          <div class="ad-desc">Full annual third-party security audit report covering security, availability, and confidentiality trust service criteria.</div>
        </div>
        <div class="ad-req">NDA Required</div>''',
     '''          <div class="ad-title">Business Associate Agreement</div>
          <div class="ad-desc">The BAA we sign before any patient data is shared.</div>
        </div>
        <div class="ad-req">Available on Request</div>''', 1),
    ('''          <div class="ad-title">Health-System Data Collaboration Brief</div>
          <div class="ad-desc">Overview of the two-year data collaboration scope, data domains, formats (HL7 FHIR / CSV / JSON), HIPAA Safe Harbor de-identification specifications, and Year 1/Year 2 objectives.</div>''',
     '''          <div class="ad-title">Pilot Brief</div>
          <div class="ad-desc">How a pilot is set up around your population, your workflow and the measure you are scored on, with intake over HL7 FHIR R4 and a BAA signed before any patient data is shared.</div>''', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"technology: {len(PAIRS)} pairs applied")
