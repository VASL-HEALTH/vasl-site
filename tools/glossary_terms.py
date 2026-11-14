"""
Canonical term list for site/glossary.html.

Single source of truth so the visible page (tools/build_pages.py) and the
DefinedTermSet JSON-LD (tools/seo_inject.py) never drift apart. Each entry is
(term, slug, definition). slug becomes both the anchor id on the page and the
fragment in the term's JSON-LD url.

Definitions are plain language. Any Vasl number used here must already be
published elsewhere on the site.
"""

TERMS = [
    ("African American Language", "african-american-language",
     "The variety of English spoken by many Black Americans, with its own grammar, sounds and "
     "vocabulary. It is also called African American English or AAVE. Language tools trained "
     "mostly on Mainstream American English misread it, not because it is imprecise, but because "
     "the tools were never built on it. VLAP reports every result by language variety, starting "
     "with African American Language."),
    ("Ambient scribe", "ambient-scribe",
     "Software that listens to a clinical visit and drafts the note. The draft is text about the "
     "patient, often close to their own words, and it is one of the kinds of text VLAP can read "
     "alongside messages, text replies and clinician notes."),
    ("Clinical decision support", "clinical-decision-support",
     "Software that gives a clinician information to inform a decision. VLAP is non-device "
     "clinical decision support under the 21st Century Cures Act, Section 3060: it surfaces a "
     "signal and shows the exact words behind it so the clinician can check the basis, and it "
     "never decides or acts on its own."),
    ("Community engagement requirement", "community-engagement-requirement",
     "The Medicaid rule under which some adult members must show 80 hours a month of work, "
     "school, volunteering or another qualifying activity to keep their coverage. Vasl Keep helps "
     "eligible members keep the coverage they qualify for: members answer by text, each reply is "
     "sorted, and navigators reach the members who need a person first."),
    ("Dialect bias", "dialect-bias",
     "When a test, screener or language model performs worse for people who speak a particular "
     "variety of a language. Research has found language-based depression models over three times "
     "less predictive for Black users (Penn, PNAS 2024). In screening, the cost is usually a quiet "
     "one: a real signal reads as nothing, and nobody follows up."),
    ("F1 score", "f1-score",
     "A measure of how well a system finds what it is looking for, combining how many of its "
     "flags are right (precision) with how many of the real cases it catches (recall). It runs "
     "from 0 to 1, higher is better. VLAP scored 0.97 F1 on substance use in clinical notes, "
     "against 0.83 for a keyword rule."),
    ("FHIR R4", "fhir-r4",
     "Fast Healthcare Interoperability Resources, Release 4, the HL7 standard electronic health "
     "records use to exchange data. VLAP takes intake through FHIR R4 from Epic, Cerner and "
     "athenahealth, so it reads the text a health system already has without a new screen for "
     "clinicians to learn."),
    ("Follow-up after an emergency visit (FUM)", "fum",
     "The HEDIS measure Follow-Up After Emergency Department Visit for Mental Illness. It counts "
     "members 6 and older with a follow-up visit within 7 and 30 days of an emergency department "
     "visit for mental illness or intentional self-harm. Medicaid plans are scored on it, and it "
     "is the measure Vasl Bridge is built around."),
    ("Held-out test", "held-out-test",
     "A test on data the model never saw while it was being built. It is the honest way to "
     "measure a model, because a model can look accurate on text it has already learned from. "
     "Every VLAP result on this site comes from a held-out test with a named dataset and a named "
     "comparison."),
    ("n2c2 2022", "n2c2-2022",
     "A shared-task dataset of clinical notes annotated by people, used by researchers to compare "
     "systems on the same ground. VLAP is tested on its substance use (SHAC) and social needs "
     "tasks, including 518 notes in the SHAC test set."),
    ("Navigator", "navigator",
     "A person on a health plan or care team who helps members get what they need, such as "
     "paperwork, appointments or benefits. In Vasl Keep, navigators work one queue of sorted "
     "replies and reach the members who need a person first."),
    ("ROC-AUC", "roc-auc",
     "A measure of how well a model ranks real cases above non-cases, from 0.5 (chance) to 1 "
     "(perfect). VLAP scored 0.83 on suicide-attempt severity in held-out posts, against 0.65 for "
     "MIT's Suicide Risk Lexicon (Low, Ghosh et al., 2026)."),
    ("Signal", "signal",
     "A named finding VLAP flags in a piece of text, such as isolation or substance use. A "
     "signal is not a score or a diagnosis. Every flag carries the sentence behind it, and a "
     "clinician reviews it and decides what to do."),
    ("Taxonomy v2.0", "taxonomy",
     "The list of signals VLAP reads for: 55 signals across seven dimensions, including "
     "behavioral health risk, substance use and social needs. The taxonomy is what makes a VLAP "
     "flag specific enough for a clinician to act on."),
    ("VLAP", "vlap",
     "The Vasl Language Analysis Platform, the language model Vasl built and owns. It reads "
     "patient messages, text replies, clinician notes and scribe text, flags clinically relevant "
     "signals with the exact words behind them, and runs on Vasl infrastructure. No patient text "
     "goes to an outside AI company."),
    ("Vasl Bridge", "vasl-bridge",
     "A daily text from emergency department discharge to the first follow-up visit, with no app. "
     "VLAP reads every reply, a clinician sees the flag, and a coach reaches out when a patient "
     "goes quiet. It passed 10 of 10 steps live, with real texts delivered."),
    ("Vasl Keep", "vasl-keep",
     "A text workflow that helps eligible Medicaid members keep the coverage they qualify for "
     "under the community engagement requirement. Each reply is sorted into one of seven "
     "categories or no reply, navigators work the queue, and the plan sees the totals."),
]
