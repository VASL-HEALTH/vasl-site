"""Related-reading copy lives in tools/link_map.py; internal_links.py regenerates pages from it.
Port the new-message versions into the source so a rerun cannot bring the old claims back."""
from pathlib import Path

P = Path("tools/link_map.py")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ('"The literature, the active IRB study, and how we handle claims we can\'t yet support."',
     '"The literature, the measurements, and how we handle claims we can\'t yet support."', 1),
    ('"The peer-reviewed literature and active IRB study this data builds on."',
     '"The peer-reviewed literature this data builds on."', 1),
    ('"The peer-reviewed literature and active validation study behind Vasl\'s approach."',
     '"The peer-reviewed literature and validation results behind Vasl\'s approach."', 1),
    ('"Daily check-ins, a peer community and a coach, for an organization without its own clinical team."',
     '"Daily check-ins and a coach, for an organization without its own clinical team."', 1),
    ('"The IRB validation process this infrastructure is built to support."',
     '"The published results this infrastructure is built to support."', 1),
    ('"PHQ-8 change, retention, and escalation rates from pilot cohorts, with methodology."',
     '"The outcomes a pilot measures, and the methodology behind them."', 1),
    ('''        ("vlap.html", "VLAP in depth",
         "The language analysis layer that reads for distress signal across the platform."),
        # peer-groups left the footer in the navigation restructure, so this is
        # now its only inbound link. Dropping it orphans an indexable page.
        ("peer-groups.html", "the peer community layer",
         "How peer groups are organized around shared identity and experience, and who moderates them."),
        ("ai-model.html", "the model behind the platform",
         "VLAP's architecture and vocabulary extension process."),
        ("teletherapy.html", "the licensed therapy layer",
         "Culturally matched teletherapy, and when a member is routed to it."),''',
     '''        ("vlap.html", "VLAP in depth",
         "Our own language model, with our own weights: 55 signals across seven dimensions, each with the words behind it."),
        ("bridge.html", "Vasl Bridge",
         "A daily text from emergency discharge to the first follow-up visit. 10 of 10 steps passed live, with real texts delivered."),
        ("keep.html", "Vasl Keep",
         "Eligible Medicaid members keep the coverage they qualify for. Each reply is sorted for a navigator."),
        ("health-systems.html", "Health plans and systems",
         "VLAP inside the care you already deliver, with intake through HL7 FHIR R4 from Epic, Cerner and athenahealth."),''', 1),
]
for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
P.write_text(s, encoding="utf-8")
print(f"link_map: {len(PAIRS)} pairs applied")
