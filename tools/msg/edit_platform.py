"""Platform page: new message into the existing design. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/platform.html")
s = P.read_text(encoding="utf-8")

OLD_DESC = ("What happens after VLAP reads a reply: a check-in text every day, a mood map, a peer community, "
            "a coach the same day, and a warm handoff to a licensed clinician.")
NEW_DESC = ("What happens after VLAP reads a reply: Vasl Bridge texts every day from emergency discharge to the "
            "first visit, Vasl Keep helps eligible Medicaid members keep their coverage, and a clinician sees the words that matter.")

PAIRS = [
    # meta, og, twitter descriptions
    (OLD_DESC, NEW_DESC, 3),

    # Hero
    ("VLAP reads how Black, Brown, LGBTQ+, rural and Medicaid youth actually describe distress. A signal that reaches a clinician and stops there changes nothing for the young person who wrote it, so Vasl built the place where the next step happens.",
     "VLAP reads how Black, Brown, LGBTQ+, rural and Medicaid patients actually describe distress. A signal that reaches a clinician and stops there changes nothing for the patient who wrote it, so Vasl built Vasl Bridge and Vasl Keep for Medicaid plans and health systems, where the next step happens.", 1),

    # Path intro
    ("A young person is enrolled the day they are discharged from the emergency department, referred by a school, or invited by a community partner. There is no app to download: the platform is text-first.",
     "A patient is enrolled by text before leaving the emergency department, and a Medicaid member answers by text to keep the coverage they qualify for. There is no app to download: the platform is text-first.", 1),

    # Step 01
    ("<div class=\"step-body\">At ED discharge, from a school referral, or by a community partner.</div>",
     "<div class=\"step-body\">By text, before the patient leaves the emergency department. No app.</div>", 1),
    ("At ED discharge, this is Vasl Bridge &rarr;",
     "At emergency discharge, this is Vasl Bridge &rarr;", 1),

    # Step 02 card
    ("<div class=\"card-label\">Mood map</div>",
     "<div class=\"card-label\">Silence is a signal</div>", 1),
    ("A mood map they can see for themselves, built from those check-ins.",
     "If the patient goes quiet, a coach reaches out.", 1),

    # Step 03
    ("When a reply matters, the partner&rsquo;s clinician sees it, with the exact words.",
     "VLAP reads every reply. When one matters, the partner&rsquo;s clinician sees the flag and the exact words behind it.", 1),

    # Step 04: peer community -> Vasl Keep
    ("<div class=\"step-title\" data-n=\"04\">Peer community and coach</div>",
     "<div class=\"step-title\" data-n=\"04\">Coverage kept with Vasl Keep</div>", 1),
    ("Peer communities organized around shared identity and experience, moderated where needed by licensed staff. A coach, who is a licensed social worker employed by the partner, assigned the same day.",
     "Under the community engagement rule of 80 hours a month, members answer by text. Each reply is sorted into one of seven categories, and navigators reach the members who need a person first.", 1),
    ("<div class=\"card-label\">Grow</div>",
     "<div class=\"card-label\">Vasl Keep</div>", 1),
    ("Grow, a structured eight-week curriculum they can work through with their coach.",
     "Eligible members keep the coverage they qualify for, and the plan sees the totals.", 1),

    # Step 05
    ("<div class=\"step-title\" data-n=\"05\">Warm handoff</div>",
     "<div class=\"step-title\" data-n=\"05\">First visit recorded</div>", 1),
    ("A warm handoff to the partner&rsquo;s own licensed clinician when that is what they need. Crisis runs on the partner&rsquo;s own protocol. Vasl delivers no therapy.",
     "A warm handoff to the partner&rsquo;s own licensed clinician, and the first follow-up visit recorded: the seven-day follow-up rate every Medicaid plan is scored on. Crisis runs on the partner&rsquo;s own protocol.", 1),

    # Path note
    ("Screening never stands in the way. PHQ-8 and GAD-7 are optional.",
     "VLAP reads patient messages, text replies, clinician notes and scribe text, and flags 55 signals across seven dimensions with the words behind each.", 1),

    # Privacy
    ("Members never see scores. Only the partner&rsquo;s credentialed clinicians see clinical detail. Each partner sees its own population&rsquo;s outcomes, the numbers it reports to Medicaid.",
     "VLAP gives a named signal with the words behind it, never a score or a diagnosis. Only the partner&rsquo;s credentialed clinicians see clinical detail. Each partner sees its own population&rsquo;s outcomes, the numbers it reports to Medicaid. Outside parties see nothing. HIPAA, BAA: we sign a business associate agreement before any patient data is shared, and patient text is read on Vasl infrastructure, never sent to an outside AI company.", 1),

    # Related reading
    ("The language analysis layer that reads for distress signal across the platform.",
     "Our own language model, with our own weights: 55 signals across seven dimensions, each with the words behind it.", 1),
    ("<a href=\"/peer-groups\" class=\"vrl-item\"><div class=\"vrl-item-title\">the peer community layer</div><div class=\"vrl-item-desc\">How peer groups are organized around shared identity and experience, and who moderates them.</div></a>",
     "<a href=\"/bridge\" class=\"vrl-item\"><div class=\"vrl-item-title\">Vasl Bridge</div><div class=\"vrl-item-desc\">A daily text from emergency discharge to the first follow-up visit. 10 of 10 steps passed live, with real texts delivered.</div></a>", 1),
    ("<a href=\"/ai-model\" class=\"vrl-item\"><div class=\"vrl-item-title\">the model behind the platform</div><div class=\"vrl-item-desc\">VLAP's architecture and vocabulary extension process.</div></a>",
     "<a href=\"/keep\" class=\"vrl-item\"><div class=\"vrl-item-title\">Vasl Keep</div><div class=\"vrl-item-desc\">Eligible Medicaid members keep the coverage they qualify for. Each reply is sorted for a navigator.</div></a>", 1),
    ("<a href=\"/teletherapy\" class=\"vrl-item\"><div class=\"vrl-item-title\">the licensed therapy layer</div><div class=\"vrl-item-desc\">Culturally matched teletherapy, and when a member is routed to it.</div></a>",
     "<a href=\"/health-systems\" class=\"vrl-item\"><div class=\"vrl-item-title\">Health plans and systems</div><div class=\"vrl-item-desc\">VLAP inside the care you already deliver, with intake through HL7 FHIR R4 from Epic, Cerner and athenahealth.</div></a>", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)

assert "—" not in s and "&mdash;" not in s and "&#8212;" not in s, "em dash present"
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
