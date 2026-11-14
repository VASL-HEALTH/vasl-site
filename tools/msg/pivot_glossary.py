"""glossary.html + tools/glossary_terms.py: youth/schools -> patients/members pivot (BRIEF_YOUTH).
Edits the page (visible list + DefinedTermSet JSON-LD) and its source, glossary_terms.py,
so a seo_inject rebuild matches. Drops the four school/youth-only terms
(FERPA, MTSS, Tier 1/2/3 supports, Transition-age youth): 38 -> 34 terms."""
from pathlib import Path

HTML = Path("site/glossary.html")
SRC = Path("tools/glossary_terms.py")
TS = '"inDefinedTermSet":"https://gotovasl.com/glossary#termset"}'

DROP = {
    "ferpa": ("FERPA",
        "The Family Educational Rights and Privacy Act, the federal law governing the privacy of student education records. School-based behavioral health tools need to be architected around FERPA's boundaries on what counts as an education record and who can access it, distinct from HIPAA, which governs health records in clinical settings."),
    "mtss": ("MTSS",
        "Multi-Tiered System of Supports, a framework used in K-12 education for matching the intensity of support to the intensity of student need, typically organized in three tiers. See Tier 1/2/3 supports."),
    "tier-1-2-3-supports": ("Tier 1/2/3 supports",
        "The three levels of MTSS: Tier 1 is universal support available to every student; Tier 2 is targeted support for students showing early signs of need; Tier 3 is intensive, individualized support for students with significant need. A well-mapped program has clear criteria for moving between tiers in both directions."),
    "transition-age-youth": ("Transition-age youth",
        "Young people roughly ages 16 to 25 moving out of child-serving systems (pediatric care, K-12 schools, foster care) and into adult-serving ones, a period associated with significant drop-off in behavioral health engagement, since eligibility, providers, and sometimes insurance all change at once."),
}

HTML_PAIRS = [
    ("Glossary: Youth Behavioral Health &amp; AI Terms | Vasl", "Glossary: Behavioral Health &amp; AI Terms | Vasl", 3),
    ("In youth mental health, inequity shows up", "In behavioral health, inequity shows up", 2),
    ("setting for youth behavioral health programs serving Medicaid populations.",
     "setting for behavioral health programs serving Medicaid populations.", 2),
    ("protected health information, distinct from the FERPA boundaries that apply in school settings.",
     "protected health information.", 2),
    ("without requiring a young person to access it in person", "without requiring a patient to access it in person", 2),
    ("the questions we get from districts, plans, and community partners change.",
     "the questions we get from health systems, plans, and community partners change.", 1),
    ('<span class="ah-meta-item">38 Terms</span>', '<span class="ah-meta-item">34 Terms</span>', 1),
    ('<a href="#g-m" class="glossary-az-link">M</a>\n', "", 1),
]
for slug, (name, d) in DROP.items():
    # JSON-LD entry (none of the four is last in the list, so each carries a trailing comma)
    HTML_PAIRS.append((f'{{"@type":"DefinedTerm","name":"{name}","description":"{d}","url":"https://gotovasl.com/glossary#{slug}",{TS},', "", 1))
    vis = d.replace("See Tier 1/2/3 supports.", 'See <a href="/for-schools">Tier 1/2/3 supports</a>.')
    span = '<span id="g-m"></span>' if slug == "mtss" else ""
    HTML_PAIRS.append((f'  {span}<div class="glossary-item" id="{slug}">\n'
                       f'    <dt class="glossary-term">{name}</dt>\n'
                       f'    <dd class="glossary-def">{vis}</dd>\n'
                       f'  </div>\n', "", 1))

SRC_PAIRS = [
    ('"youth mental health, inequity shows up as', '"behavioral health, inequity shows up as', 1),
    ('"setting for youth behavioral health programs serving Medicaid populations."',
     '"setting for behavioral health programs serving Medicaid populations."', 1),
    ('"settings. Vasl\'s architecture is built around HIPAA\'s boundaries on protected health "\n'
     '     "information, distinct from the FERPA boundaries that apply in school settings."',
     '"settings. Vasl\'s architecture is built around HIPAA\'s boundaries on protected health "\n'
     '     "information."', 1),
    ('"care without requiring a young person to access it', '"care without requiring a patient to access it', 1),
    ('    ("FERPA", "ferpa",\n'
     '     "The Family Educational Rights and Privacy Act, the federal law governing the privacy of "\n'
     '     "student education records. School-based behavioral health tools need to be architected "\n'
     '     "around FERPA\'s boundaries on what counts as an education record and who can access it, "\n'
     '     "distinct from HIPAA, which governs health records in clinical settings."),\n', "", 1),
    ('    ("MTSS", "mtss",\n'
     '     "Multi-Tiered System of Supports, a framework used in K-12 education for matching the "\n'
     '     "intensity of support to the intensity of student need, typically organized in three tiers. "\n'
     '     "See Tier 1/2/3 supports."),\n', "", 1),
    ('    ("Tier 1/2/3 supports", "tier-1-2-3-supports",\n'
     '     "The three levels of MTSS: Tier 1 is universal support available to every student; Tier 2 is "\n'
     '     "targeted support for students showing early signs of need; Tier 3 is intensive, "\n'
     '     "individualized support for students with significant need. A well-mapped program has clear "\n'
     '     "criteria for moving between tiers in both directions."),\n', "", 1),
    ('    ("Transition-age youth", "transition-age-youth",\n'
     '     "Young people roughly ages 16 to 25 moving out of child-serving systems (pediatric care, "\n'
     '     "K-12 schools, foster care) and into adult-serving ones, a period associated with "\n'
     '     "significant drop-off in behavioral health engagement, since eligibility, providers, and "\n'
     '     "sometimes insurance all change at once."),\n', "", 1),
]

for P, PAIRS in ((HTML, HTML_PAIRS), (SRC, SRC_PAIRS)):
    s = P.read_text(encoding="utf-8")
    for old, new, n in PAIRS:
        c = s.count(old)
        assert c == n, f"{P}: expected {n}, found {c}: {old[:100]!r}"
        s = s.replace(old, new)
    P.write_text(s, encoding="utf-8")
    print(f"{P}: {len(PAIRS)} pairs applied")
