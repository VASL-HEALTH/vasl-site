"""
Canonical term list for site/glossary.html.

Single source of truth so the visible page and the DefinedTermSet JSON-LD
(emitted by seo_inject.py) never drift apart. Each entry is
(term, slug, definition). slug becomes both the anchor id on the page and
the fragment in the term's JSON-LD url.

Definitions are plain-language, 40-80 words, no diagnostic or surveillance
framing, no invented figures. Where a definition references a Vasl-specific
number, that number must already be published elsewhere on the site.
"""

TERMS = [
    ("AAVE", "aave",
     "African American Vernacular English — a rule-governed dialect of English with its own "
     "grammar, phonology, and vocabulary, spoken by many Black Americans alongside or instead of "
     "Mainstream American English. Standard clinical language models are trained almost entirely "
     "on Mainstream American English, so they systematically misread AAVE — not because the "
     "dialect is imprecise, but because the model was never taught it."),
    ("Behavioral health equity", "behavioral-health-equity",
     "The absence of avoidable, unfair differences in behavioral health access, quality, and "
     "outcomes across groups defined by race, ethnicity, language, or socioeconomic status. In "
     "youth mental health, inequity shows up as longer wait times, lower engagement, and higher "
     "dropout for Black, Latino, and first-generation populations — not because need is lower, "
     "but because the systems built to reach them usually weren't."),
    ("Care continuum", "care-continuum",
     "The full range of support available to a person, from lowest-intensity (peer community, "
     "self-guided check-ins) to highest-intensity (licensed therapy, crisis support), with clear "
     "pathways between levels. A continuum only works if movement between levels is easy in both "
     "directions — stepping up when needed, stepping down when it's not."),
    ("Coded language", "coded-language",
     "Words or phrases a community develops, often deliberately, to communicate sensitive meaning "
     "without triggering automated moderation or drawing unwanted attention. “Unaliving” "
     "is the most widely cited example. Coded language evolves continuously, which is why a "
     "one-time vocabulary update can't keep a detection system current."),
    ("Crisis support", "crisis-support",
     "The highest-acuity layer of a behavioral health system, activated when a member may be at "
     "imminent risk. Vasl surfaces signals that may warrant crisis support to a human — a coach, "
     "a counselor, a clinician — who makes the actual determination and initiates response. The "
     "system does not make crisis determinations on its own."),
    ("Cultural humility", "cultural-humility",
     "An ongoing practice of self-reflection about one's own cultural assumptions, paired with "
     "genuine curiosity about someone else's, rather than a credential earned once. In clinical "
     "training it's often contrasted with “cultural competence,” which can imply a fixed "
     "body of knowledge is sufficient."),
    ("Cultural idioms of distress", "cultural-idioms-of-distress",
     "Culturally specific ways of expressing or experiencing psychological pain that don't map "
     "cleanly onto standard clinical categories — a phrase, a somatic complaint, a way of "
     "describing a feeling that carries meaning inside a community but reads as ambiguous or even "
     "invisible outside it. Reading these correctly requires a model to have learned them, not "
     "translate them from a standard baseline."),
    ("Culturally responsive care", "culturally-responsive-care",
     "Support designed around a population's language, communication norms, and lived context "
     "from the start, rather than a standard model retrofitted with cultural add-ons afterward. "
     "The distinction matters because retrofitting tends to preserve the original model's blind "
     "spots."),
    ("Dialect bias", "dialect-bias",
     "Systematic misreading of meaning, tone, or severity by a system trained primarily on one "
     "dialect when it encounters another. In clinical NLP, dialect bias can cause identical "
     "distress language to be scored differently depending on which dialect it's expressed in. "
     "See differential item functioning."),
    ("Differential item functioning", "differential-item-functioning",
     "A measurement phenomenon where a test item behaves differently across groups even when the "
     "underlying trait it measures is held equal — meaning an identical score does not always "
     "reflect an identical clinical reality. Differential item functioning has been documented in "
     "standard screening instruments including the PHQ-9 across race and ethnicity."),
    ("Engagement", "engagement",
     "Active, ongoing use of a behavioral health platform or service, as distinct from enrollment "
     "or access alone. A member can be enrolled and never meaningfully engage; engagement is the "
     "metric that actually predicts benefit. Vasl reports 30-day retention and time to first "
     "substantive interaction as engagement indicators."),
    ("Escalation pathway", "escalation-pathway",
     "The defined route by which a concern moves from a lower-intensity layer of support to a "
     "higher one — for example, from a peer community moderator to a coach, or from a coach to a "
     "licensed clinician — with clear criteria for when and how the handoff happens."),
    ("False negative", "false-negative",
     "An instance where a detection system fails to flag a genuine signal of distress. In "
     "screening and detection contexts, false negatives are generally treated as the more serious "
     "error type, since they mean a person who needed support wasn't identified. Sensitivity is "
     "the metric most directly tied to minimizing false negatives."),
    ("FERPA", "ferpa",
     "The Family Educational Rights and Privacy Act — the federal law governing the privacy of "
     "student education records. School-based behavioral health tools need to be architected "
     "around FERPA's boundaries on what counts as an education record and who can access it, "
     "distinct from HIPAA, which governs health records in clinical settings."),
    ("FQHC", "fqhc",
     "A Federally Qualified Health Center — a community-based clinic that receives federal "
     "funding to provide primary and preventive care, including behavioral health, in "
     "underserved areas, regardless of a patient's ability to pay. FQHCs are a common deployment "
     "setting for youth behavioral health programs serving Medicaid populations."),
    ("FUH", "fuh",
     "Follow-Up After Hospitalization for Mental Illness — a HEDIS measure tracking whether a "
     "patient received outpatient follow-up care within 7 and 30 days of a mental health "
     "hospitalization. FUH is considered a strong proxy for care coordination quality, and "
     "follow-up completion depends heavily on whether the patient stays engaged after discharge."),
    ("FUM", "fum",
     "Follow-Up After Emergency Department Visit for Mental Illness — a HEDIS measure similar to "
     "FUH, but tracking follow-up after an emergency department visit rather than an inpatient "
     "stay. Like FUH, FUM outcomes depend heavily on whether a patient can be reached and "
     "re-engaged quickly after the ED encounter."),
    ("Help-seeking mismatch", "help-seeking-mismatch",
     "The gap between how a person actually asks for help — often indirectly, in coded or "
     "culturally specific language — and how a system is built to recognize a request for help. "
     "When the mismatch is large, real requests go unanswered not because no one was listening, "
     "but because the system was listening for the wrong signal."),
    ("HEDIS", "hedis",
     "The Healthcare Effectiveness Data and Information Set — a standardized set of performance "
     "measures used by health plans to report on care quality, including several specific to "
     "behavioral health engagement and follow-up."),
    ("HIPAA", "hipaa",
     "The Health Insurance Portability and Accountability Act — the federal law governing the "
     "privacy and security of individually identifiable health information in clinical and payer "
     "settings. Vasl's architecture is built around HIPAA's boundaries on protected health "
     "information, distinct from the FERPA boundaries that apply in school settings."),
    ("Human-in-the-loop", "human-in-the-loop",
     "A system design principle where a human reviews and makes the final determination on any "
     "consequential output, rather than the system acting autonomously. Vasl surfaces signals to "
     "a human — never to an automated decision or an external authority — who applies clinical "
     "and relational judgment before anything happens."),
    ("IET", "iet",
     "Initiation and Engagement of Substance Use Disorder Treatment — a HEDIS measure tracking "
     "whether a patient with a new SUD diagnosis both initiates treatment and stays engaged with "
     "it over time. IET is a two-part measure precisely because starting treatment and remaining "
     "in it are different challenges with different drop-off points."),
    ("Large language model", "large-language-model",
     "A machine learning model trained on large volumes of text to represent and generate "
     "language. General-purpose large language models are trained predominantly on internet text "
     "that underrepresents culturally specific and dialect-marked language — the starting problem "
     "VLAP was built to address."),
    ("Linguistic masking", "linguistic-masking",
     "Expressing distress in a form that minimizes social risk or the chance of an unwanted "
     "response — hedged, indirect, or coded language that carries real weight to someone who "
     "reads it correctly, but reads as minor or ambiguous otherwise."),
    ("MTSS", "mtss",
     "Multi-Tiered System of Supports — a framework used in K-12 education for matching the "
     "intensity of support to the intensity of student need, typically organized in three tiers. "
     "See Tier 1/2/3 supports."),
    ("Natural language processing", "natural-language-processing",
     "The field of computing concerned with how systems process, interpret, and generate human "
     "language. Clinical NLP applies these methods to language generated in health and behavioral "
     "health contexts, where the cost of misreading meaning is higher than in most other NLP "
     "applications."),
    ("Peer support specialist", "peer-support-specialist",
     "A trained facilitator, often with lived experience relevant to the population served, who "
     "supports peer community spaces and provides connection that does not require licensure. "
     "Peer support sits at the access layer of a care continuum — the relationship that exists "
     "before a clinical need is identified."),
    ("PHQ-8", "phq-8",
     "The Patient Health Questionnaire, 8-item version — a self-report depression screening "
     "instrument, functionally identical to the PHQ-9 minus the item on suicidal ideation. Vasl "
     "uses the PHQ-8 as its primary outcome instrument for pilot cohort reporting because it is a "
     "widely validated short-form screener suitable for non-clinical administration."),
    ("PHQ-9", "phq-9",
     "The Patient Health Questionnaire, 9-item version — the PHQ depression screener including an "
     "item on thoughts of self-harm. Research has documented differential item functioning in the "
     "PHQ-9 across race and ethnicity, meaning the same score does not always represent the same "
     "underlying symptom severity across groups."),
    ("Population-level insight", "population-level-insight",
     "Aggregate, de-identified patterns across a group of members — trends, not individual "
     "records. Vasl's organizational reporting operates at this level; a minimum cohort size is "
     "enforced before any aggregate data is surfaced, specifically to prevent identifying an "
     "individual by inference from a small group."),
    ("Protected health information", "protected-health-information",
     "Individually identifiable health information subject to HIPAA's privacy and security "
     "requirements. Vasl's platform reporting to organizational administrators is built to "
     "exclude protected health information — no member name, session content, or individual "
     "clinical detail is accessible outside the direct care relationship."),
    ("Retention", "retention",
     "The proportion of enrolled members who remain actively engaged with a platform or service "
     "over a defined period. Vasl reports 30-day retention because early disengagement is the "
     "point at which most behavioral health interventions lose their ability to help."),
    ("Sensitivity", "sensitivity",
     "In detection and screening contexts, the proportion of true positive cases a system "
     "correctly identifies — the inverse of the false negative rate. High sensitivity is "
     "prioritized in early-detection contexts because the cost of missing a genuine signal "
     "generally outweighs the cost of a false alarm reviewed and dismissed by a human."),
    ("Teletherapy", "teletherapy",
     "Licensed mental health therapy delivered remotely, typically by video or phone, by a "
     "clinician credentialed in the client's state. Teletherapy extends the reach of licensed "
     "care without requiring a young person to access it in person, which matters most in areas "
     "with clinician shortages."),
    ("Tier 1/2/3 supports", "tier-1-2-3-supports",
     "The three levels of MTSS: Tier 1 is universal support available to every student; Tier 2 is "
     "targeted support for students showing early signs of need; Tier 3 is intensive, "
     "individualized support for students with significant need. A well-mapped program has clear "
     "criteria for moving between tiers in both directions."),
    ("Transition-age youth", "transition-age-youth",
     "Young people roughly ages 16–25 moving out of child-serving systems (pediatric care, "
     "K-12 schools, foster care) and into adult-serving ones — a period associated with "
     "significant drop-off in behavioral health engagement, since eligibility, providers, and "
     "sometimes insurance all change at once."),
    ("Universal screening", "universal-screening",
     "Administering a standardized assessment to an entire population, rather than only to "
     "individuals already flagged for concern, so that need is identified consistently rather "
     "than depending on who happens to ask for help or who happens to be noticed."),
    ("Warm handoff", "warm-handoff",
     "A transfer of care between two people — for example, a coach and a licensed clinician — "
     "that includes direct introduction and context-sharing, rather than a referral the member "
     "has to navigate alone. Warm handoffs are associated with meaningfully higher follow-through "
     "than cold referrals."),
]
