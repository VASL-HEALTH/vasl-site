"""For-organizations page: youth / schools / campus framing -> Medicaid plans, health systems, patients, members.
Exact old/new pairs, each asserted. Related-reading block (tools/link_map.py) left alone."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/for-organizations.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # meta / og / twitter
    ("Community health centers, FQHCs, and youth-serving nonprofits use Vasl to extend behavioral health support without hiring a clinical team of their own.",
     "Medicaid plans, health systems, community health centers and FQHCs use Vasl to extend behavioral health support without hiring a clinical team of their own.", 3),
    ("Youth Mental Health for Community Organizations | Vasl",
     "Behavioral Health for Community Organizations | Vasl", 3),
    # nav (desktop + mobile)
    ("<span class=\"vh-sm-line\">The platform for youth-serving organizations.</span>",
     "<span class=\"vh-sm-line\">Behavioral health support for community organizations.</span>", 2),
    # hero
    ("Universities, health plans, community health centers, and non-profits all face the same structural problem:",
     "Medicaid plans, health systems, community health centers, and non-profits all face the same structural problem:", 1),
    ("rural and Medicaid youth actually describe distress.</p>",
     "rural and Medicaid members actually describe distress.</p>", 1),
    ("""        <div class="ot-label">Universities</div>
        <div class="ot-right">
          <div class="ot-name">Higher Education</div>
          <div class="ot-desc">Campus counseling center capacity gaps, student mental health crisis statistics, and the specific needs of first-generation and Black and Latino students that standard campus care misses.</div>""",
     """        <div class="ot-label">Hospitals</div>
        <div class="ot-right">
          <div class="ot-name">Emergency Departments</div>
          <div class="ot-desc">Follow-up after an emergency visit or discharge, seven-day follow-up rates, and the specific needs of Black and Latino, rural, and first-generation patients that standard discharge care misses.</div>""", 1),
    ("<div class=\"ot-name\">Youth-Serving Organizations</div>",
     "<div class=\"ot-name\">Community-Based Organizations</div>", 1),
    # chapter 01
    ("Every organization that serves Black and Latino, LGBTQ+, and first-generation youth faces the same structural gap:",
     "Every organization that serves Black and Latino, LGBTQ+, rural, and first-generation patients and members faces the same structural gap:", 1),
    # segment 01: universities -> hospitals and emergency departments
    ("<div class=\"seg-type-tag\">01 &middot; Higher Education</div>",
     "<div class=\"seg-type-tag\">01 &middot; Emergency Care</div>", 1),
    ("<div class=\"seg-type-name\">Universities & Colleges</div>",
     "<div class=\"seg-type-name\">Hospitals & Emergency Departments</div>", 1),
    ("<div class=\"seg-type-ex\">State systems, HBCUs, HSIs, community colleges</div>",
     "<div class=\"seg-type-ex\">Health systems, safety-net hospitals, rural and critical access hospitals</div>", 1),
    ("Campus counseling centers are operating at structurally unsustainable ratios, often 1 counselor for every 1,500+ students. Wait times of 3 to 6 weeks for an initial appointment are common. When students in crisis finally reach the front of the queue, they've often already disengaged or decompensated. For first-generation, Black and Latino, and LGBTQ+ students specifically, the additional barrier of culturally misaligned care means many never return after the first session.",
     "After an emergency visit for a mental health crisis, the days before the first follow-up appointment are when patients are most often lost. Discharge instructions go home on paper, follow-up depends on a phone call that may not be answered, and nobody reads what the patient says in between. For first-generation, Black and Latino, rural, and LGBTQ+ patients specifically, the additional barrier of culturally misaligned care means many never make the first follow-up visit.", 1),
    ("""<div class="seg-stat">1,500<span style="font-size:20px">:1</span></div>
        <div class="seg-stat-label">Typical counselor-to-student ratio at large universities, 6&times; the IACS recommended standard</div>""",
     """<div class="seg-stat">10<span style="font-size:20px"> of 10</span></div>
        <div class="seg-stat-label">Vasl Bridge steps passed live, real texts delivered</div>""", 1),
    ("<div class=\"svi\">Coaching available within 48 hours of enrollment, no waitlist</div>",
     "<div class=\"svi\">A text from Vasl Bridge every day, starting the day the patient leaves the emergency department</div>", 1),
    ("<div class=\"svi\">VLAP signal detection and clinical escalation for students in distress before they reach the counseling center queue</div>",
     "<div class=\"svi\">VLAP signal detection and clinical escalation for patients in distress before the first follow-up visit</div>", 1),
    ("<div class=\"svi\">Culturally matched coaches for first-gen, Black and Latino, and LGBTQ+ student cohorts</div>",
     "<div class=\"svi\">Culturally matched coaches for first-generation, Black and Latino, rural, and LGBTQ+ patients</div>", 1),
    ("<div class=\"svi\">Warm handoff infrastructure to campus counseling center, students arrive with clinical context, not starting from zero</div>",
     "<div class=\"svi\">Warm handoff to your behavioral health team, patients arrive with clinical context, not starting from zero</div>", 1),
    ("<div class=\"svi\">Aggregate population data for campus mental health planning and reporting</div>",
     "<div class=\"svi\">Aggregate population data for seven-day follow-up planning and reporting</div>", 1),
    ("<div class=\"svi\">FERPA-compliant architecture, student health data never accessible to academic staff</div>",
     "<div class=\"svi\">HIPAA, BAA signed before any patient data is shared, patient text read on Vasl infrastructure and never sent to an outside AI company</div>", 1),
    # segment 04: youth-serving -> community-based
    ("<div class=\"seg-type-name\">Youth-Serving Organizations</div>",
     "<div class=\"seg-type-name\">Community-Based Organizations</div>", 1),
    ("<div class=\"seg-type-ex\">Youth empowerment NGOs, after-school programs, community organizations</div>",
     "<div class=\"seg-type-ex\">Community NGOs, outreach programs, community organizations</div>", 1),
    ("Non-profit youth-serving organizations often have the most direct relationships with the young people who most need",
     "Non-profit community organizations often have the most direct relationships with the people who most need", 1),
    ("Culturally matched coaching for youth who have never engaged with traditional mental health systems",
     "Culturally matched coaching for members who have never engaged with traditional mental health systems", 1),
    # implementation
    ("compliance documentation (BAA, FERPA alignment for schools), and Medicaid billing setup",
     "compliance documentation (HIPAA, BAA), and Medicaid billing setup", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
