"""
Data file for tools/internal_links.py — one entry per page that gets a
"related reading" block. Kept separate from the generator so the editorial
decisions (which pages connect, and why a human would click through) are easy
to review and change without touching rendering code.

Each value is a list of (target_rel, anchor_text, one_line_reason) tuples.
target_rel is relative to site/ (e.g. "vlap.html" or "help/billing.html").
Order is preserved in the rendered block.

Edges required by SEO-WEEK2.md workstream 1, plus enough additional coverage
to land in the 60-80 new-link target without turning any page into a link
dump — every entry earns its place with a reason someone would click it.
"""

LINKS = {
    # ---- Buyer pages: platform, vlap, ai-model, outcomes, pricing ------------
    "for-schools.html": [
        ("platform.html", "the full five-layer platform",
         "Peer community, coaching, and licensed therapy in one continuum — see how the layers connect."),
        ("vlap.html", "how VLAP reads distress signals",
         "The language layer behind every alert a counselor sees — what it flags and what it deliberately leaves alone."),
        ("ai-model.html", "the model trained on youth vernacular",
         "CulturalBERT, and why standard clinical NLP misses the way your students actually talk about distress."),
        ("outcomes.html", "pilot cohort outcomes and ROI",
         "Retention, symptom change, and the budget case for your board and grants office."),
        ("pricing.html", "how pricing works for districts",
         "Cost structure by enrollment size, and how Title I and Medicaid billing typically offset it."),
    ],
    "health-systems.html": [
        ("platform.html", "the platform's five care layers",
         "From peer community to licensed therapy — where each layer sits in a member's care continuum."),
        ("vlap.html", "VLAP's signal detection layer",
         "How language analysis surfaces risk to a human reviewer without ever assigning a diagnosis."),
        ("ai-model.html", "CulturalBERT's training approach",
         "Why a model trained on standard clinical text underperforms with the members you're trying to retain."),
        ("outcomes.html", "engagement and retention data",
         "30-day retention and symptom-change figures from pilot cohorts, benchmarked against digital health norms."),
        ("pricing.html", "pricing for health plans and systems",
         "Population-based pricing and what a pilot deployment typically includes."),
    ],
    "for-organizations.html": [
        ("platform.html", "the platform's care layers",
         "Peer support, coaching, and licensed therapy — sized for an organization without its own clinical team."),
        ("vlap.html", "how VLAP surfaces distress signals",
         "The language layer that flags risk to a human who already knows the young person."),
        ("ai-model.html", "the model behind VLAP",
         "CulturalBERT and the vocabulary work that lets it read AAVE and youth vernacular directly."),
        ("outcomes.html", "outcomes across pilot cohorts",
         "Retention and engagement figures, with the methodology behind each number."),
        ("pricing.html", "pricing for community organizations",
         "How cost scales with population size, and what a pilot includes."),
    ],

    # ---- Blog posts: single most relevant buyer page + vlap or ai-model ------
    "blog-bridging-chasm.html": [
        ("health-systems.html", "what this means for health plans",
         "How the vocabulary and validation work described here translates into member retention for payers."),
        ("ai-model.html", "CulturalBERT in full",
         "The architecture and vocabulary extension process behind the model this piece describes."),
    ],
    "blog-future-culturally-responsive.html": [
        ("for-organizations.html", "what this looks like for community organizations",
         "How FQHCs and youth-serving nonprofits put a culturally responsive model into practice."),
        ("vlap.html", "VLAP, the layer built to read for it",
         "The signal-detection layer built to act on the argument this piece makes."),
    ],
    "blog-medicaid-populations.html": [
        ("health-systems.html", "the health plan case for this approach",
         "How Medicaid-serving plans use Vasl to reach members standard outreach doesn't retain."),
        ("vlap.html", "the language layer behind engagement",
         "Why cultural and linguistic fit, not just access, is what actually drives retention."),
    ],
    "blog-mental-health-equity-crisis.html": [
        ("for-schools.html", "what districts can do about it",
         "The tiered program built to close this gap inside a school's existing MTSS structure."),
        ("ai-model.html", "the model built to close the language gap",
         "CulturalBERT's approach to the vocabulary and context problem this piece describes."),
    ],
    "blog-other-diagnosis.html": [
        ("for-schools.html", "how this shows up in a school setting",
         "Why counselors need a way to distinguish identity-based stress from pathology before it escalates."),
        ("vlap.html", "how VLAP is built to avoid this",
         "The signal taxonomy designed to separate cultural expression from clinical risk."),
    ],
    "blog-healing-great-divide.html": [
        ("for-organizations.html", "closing structural gaps at the community level",
         "How community organizations extend behavioral health reach without building a clinical team from scratch."),
        ("ai-model.html", "the model built for this population",
         "What training a language model directly on underserved communities' speech patterns actually requires."),
    ],
    "blog-crisis-without-solving.html": [
        ("for-organizations.html", "an implementation, not another report",
         "What Vasl actually deploys for community organizations, past the documentation stage."),
        ("vlap.html", "the detection layer this argues for",
         "How VLAP turns language signal into an early, human-reviewed intervention point."),
    ],

    # ---- support.html: complete help index ------------------------------------
    "support.html": [
        ("help/getting-started.html", "Getting Started",
         "Onboarding steps for a new partner organization, from contract to first member enrolled."),
        ("help/assessments.html", "Assessments",
         "Which clinical instruments are used, when, and how results are handled."),
        ("help/billing.html", "Billing",
         "Invoicing, Medicaid billing support, and how contract costs are structured."),
        ("help/clinical.html", "Clinical Escalation",
         "How warm handoffs to licensed care work, and who is involved at each step."),
        ("help/compliance.html", "Compliance",
         "FERPA, HIPAA, and the data-handling questions partners ask before signing."),
        ("help/technical.html", "Technical",
         "Integration, access, and platform administration questions."),
        ("help/vlap-technology.html", "VLAP Technology",
         "How the language analysis layer works, in plain terms, for a non-technical reader."),
    ],

    # ---- research.html <-> clinical-outcomes.html <-> outcomes.html ----------
    "research.html": [
        ("clinical-outcomes.html", "clinical outcomes data",
         "PHQ-8 change, retention, and escalation rates from pilot cohorts, with methodology."),
        ("outcomes.html", "stakeholder and ROI outcomes",
         "What the research translates into for districts, plans, and community partners."),
        ("about.html", "who reviews this research",
         "The clinical governance structure that reviews every claim before it's published."),
    ],
    "clinical-outcomes.html": [
        ("research.html", "the research base behind these numbers",
         "The peer-reviewed literature and active IRB study this data builds on."),
        ("outcomes.html", "what these numbers mean for stakeholders",
         "Cost and ROI implications of the retention and symptom data on this page."),
        ("vlap.html", "the signal layer behind the data",
         "How VLAP's detection informs the clinical escalation figures reported here."),
    ],
    "outcomes.html": [
        ("research.html", "the evidence base",
         "The literature and ongoing validation study behind Vasl's clinical approach."),
        ("clinical-outcomes.html", "the full clinical outcomes breakdown",
         "PHQ-8 trajectories, retention checkpoints, and escalation methodology in detail."),
        ("pricing.html", "what this costs to deploy",
         "How these outcomes map to pricing by population size and setting."),
    ],

    # ---- technology.html <-> infrastructure.html <-> vlap.html ---------------
    "technology.html": [
        ("infrastructure.html", "the infrastructure and data handling model",
         "Hosting, encryption, and retention specifics for a security or IT reviewer."),
        ("vlap.html", "VLAP, the layer this architecture supports",
         "What the language analysis layer actually does with the data described here."),
        ("ai-model.html", "the model running inside this architecture",
         "CulturalBERT's training approach and current validation status."),
    ],
    "infrastructure.html": [
        ("technology.html", "the full architecture and security model",
         "PHI boundaries, auditability, and human-in-the-loop escalation design."),
        ("vlap.html", "what runs on this infrastructure",
         "The signal-detection layer this hosting and access model is built to support."),
        ("research.html", "how this holds up under independent review",
         "The IRB validation process this infrastructure is built to support."),
    ],
    "vlap.html": [
        ("technology.html", "the architecture VLAP runs on",
         "PHI handling, access control, and the security model behind the signal layer."),
        ("infrastructure.html", "the infrastructure and data handling behind it",
         "Hosting, encryption, and retention specifics for a compliance reviewer."),
        ("ai-model.html", "CulturalBERT, the model behind VLAP",
         "The language model that powers VLAP's signal detection."),
    ],

    # ---- broader coverage: homepage, about, platform --------------------------
    "index.html": [
        ("for-schools.html", "Vasl for K-12 districts",
         "A tiered program mapped to MTSS, staffed by people students recognize."),
        ("health-systems.html", "Vasl for health plans and systems",
         "Engagement built on cultural fit for the members standard outreach loses."),
        ("for-organizations.html", "Vasl for community organizations",
         "Extend behavioral health reach without hiring a clinical team of your own."),
    ],
    "about.html": [
        ("research.html", "the research and evidence base",
         "The literature, the active IRB study, and how we handle claims we can't yet support."),
        ("vlap.html", "VLAP, the platform's language layer",
         "How language analysis surfaces signal without ever assigning a diagnosis."),
        ("team.html", "the team and clinical advisors",
         "Who reviews what the platform is allowed to claim, and how."),
    ],
    "platform.html": [
        ("vlap.html", "VLAP in depth",
         "The language analysis layer that reads for distress signal across the platform."),
        ("ai-model.html", "the model behind the platform",
         "CulturalBERT's architecture and vocabulary extension process."),
        ("teletherapy.html", "the licensed therapy layer",
         "Culturally matched teletherapy, and when a member is routed to it."),
    ],

    # ---- new pages (workstream 2) ---------------------------------------------
    "school-mental-health-rfp.html": [
        ("for-schools.html", "Vasl's program for K-12 districts",
         "The tiered model this checklist's criteria map to, if you want to see it end to end."),
        ("vlap.html", "how the language layer works",
         "What VLAP actually reads for, and what it deliberately never does."),
        ("outcomes.html", "outcomes data with methodology",
         "Retention and symptom-change figures, reported with the rigor an RFP evaluator would expect."),
        ("contact.html", "talk to an implementation lead",
         "A 45-minute conversation, not a sales pitch — bring your RFP and we'll answer it directly."),
    ],
    "dialect-bias-mental-health-screening.html": [
        ("vlap.html", "VLAP's signal taxonomy",
         "How the detection layer built for this problem is actually structured."),
        ("ai-model.html", "CulturalBERT's architecture",
         "The bidirectional model and vocabulary extension this piece describes in plain terms."),
        ("research.html", "the full research base",
         "The peer-reviewed literature and active validation study behind Vasl's approach."),
        ("glossary.html", "definitions for the terms used here",
         "Differential item functioning, dialect bias, and related terms, defined plainly."),
    ],
    "hedis-behavioral-health-cultural-fit.html": [
        ("health-systems.html", "Vasl for health plans",
         "How the engagement model described here fits into a plan's broader behavioral health strategy."),
        ("outcomes.html", "engagement and retention data",
         "The pilot-cohort figures referenced throughout this page, with full methodology."),
        ("clinical-outcomes.html", "the clinical outcomes detail",
         "PHQ-8 trajectories and escalation rates behind the summary numbers here."),
        ("pricing.html", "pricing for health plans and systems",
         "Population-based cost structure for a quality or behavioral health lead evaluating this."),
    ],
    "glossary.html": [
        ("vlap.html", "VLAP",
         "The language analysis layer many of these terms describe."),
        ("ai-model.html", "CulturalBERT",
         "The model architecture behind several of the technical terms above."),
        ("research.html", "the research base",
         "Where the clinical and technical terms above come from in the literature."),
    ],
}

# Per-page header override. Default is "Related Reading".
HEADER_OVERRIDES = {
    "support.html": "Complete Help Center",
}
