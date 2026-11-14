"""Generator sources carry youth/schools copy that a rerun would write back onto pages.
Pivot the copy; retire for-schools, for-families, school-mental-health-rfp and peer-groups
(noindex, so gen_sitemap drops them; inbound related-reading links repointed)."""
from pathlib import Path


def apply(path, pairs):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    for old, new, n in pairs:
        c = s.count(old)
        assert c == n, f"{path}: expected {n}, found {c}: {old[:80]!r}"
        s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
    print(f"{path}: {len(pairs)} pairs applied")


apply("tools/link_map.py", [
    ('"The language layer that flags risk to a human who already knows the young person."',
     '"The language layer that flags a named signal, with the words behind it, to the clinician who knows the patient."', 1),
    ('"DeBERTa-v3 and the vocabulary work that lets it read AAVE and youth vernacular directly."',
     '"Our own model, our own weights, reading the words patients actually use."', 1),
    ('"How FQHCs and youth-serving nonprofits put a culturally responsive model into practice."',
     '"How Medicaid plans and health systems put VLAP to work."', 1),
    ('''        ("for-schools.html", "what districts can do about it",
         "The tiered program built to close this gap inside a school's existing MTSS structure."),''',
     '''        ("health-systems.html", "what plans and health systems can do about it",
         "VLAP, Vasl Bridge and Vasl Keep inside the care you already deliver."),''', 1),
    ('"What the research translates into for districts, plans, and community partners."',
     '"What the research translates into for Medicaid plans and health systems."', 1),
    ('''        ("school-mental-health-rfp.html", "MTSS, FERPA, and HIPAA in an RFP context",
         "How several of the terms above show up as actual evaluation criteria in a district RFP."),''',
     '''        ("vlap.html", "VLAP, the language engine",
         "Our own model, our own weights. A named signal with the exact words behind it."),''', 1),
])

# for-schools in blog-other-diagnosis: read the entry first, then repoint
lm = Path("tools/link_map.py").read_text(encoding="utf-8")
i = lm.index('("for-schools.html", "how this shows up in a school setting",')
old_entry = lm[i: lm.index("),", i) + 2]
apply("tools/link_map.py", [
    (old_entry,
     '("health-systems.html", "how this shows up in a health system",\n'
     '         "Why clinicians need a way to tell identity-based stress from pathology before it escalates."),', 1),
])

apply("tools/seo_inject.py", [
    ('''NOINDEX = {
    "404.html",''',
     '''NOINDEX = {
    "404.html",
    # Retired with the pivot to Medicaid plans and health systems (14 Nov 2026):
    # kept on disk, out of the sitemap and search.
    "for-schools.html",
    "for-families.html",
    "school-mental-health-rfp.html",
    "peer-groups.html",''', 1),
    ('"and first-generation youth actually describe distress. Detection, not diagnosis."',
     '"and first-generation patients actually describe distress. Detection, not diagnosis."', 1),
    ('"A five-layer behavioral health continuum for youth: peer community, daily check-ins, "',
     '"Vasl Bridge, Vasl Keep and VLAP for Medicaid plans and health systems: daily check-ins, "', 1),
])
