"""Pivot follow-ups (14 Nov 2026, 2:50 PM PT).
- Headline stat: the youth-only 31.2% (Hoffmann, Pediatrics 2023) moves off the hero and the stat cells;
  they lead with the HEDIS FUM 7-day window Medicaid plans are scored on. No new numbers.
- Real advisor quotes and the SBIR questions go back to their original words.
- clinical-outcomes keeps the factual "adult writing" qualifier.
- The school-counselor ratio comes out of the crisis post."""
from pathlib import Path

FUM_LINE = ("Medicaid plans are scored on whether a patient sees a clinician within 7 days "
            "of a mental health emergency visit.")
FUM_DESC = (FUM_LINE + " Vasl Bridge texts every day from discharge to that first visit.")
OLD_DESC = ("Only 31.2% of Medicaid youth see a clinician within 7 days of a mental health emergency visit. "
            "Vasl Bridge texts every day from discharge to that first visit.")

EDITS = {
    "site/bridge.html": [
        (OLD_DESC, FUM_DESC, 3),
        ('<div class="hero-figure reveal d1">31.2%</div>', '<div class="hero-figure reveal d1">7 days</div>', 1),
        ('<h1 class="hero-headline reveal d1">Only 31.2% of Medicaid youth see a clinician within 7 days of a mental health emergency visit.</h1>',
         f'<h1 class="hero-headline reveal d1">{FUM_LINE}</h1>', 1),
        ('<div class="hero-source reveal d2">Hoffmann et al., Pediatrics 2023</div>',
         '<div class="hero-source reveal d2">HEDIS FUM, Follow-Up After Emergency Department Visit for Mental Illness</div>', 1),
    ],
    "site/health-systems.html": [
        ('<div class="bridge-figure">31.2%</div>', '<div class="bridge-figure">7 days</div>', 1),
        ('<div class="bridge-stat">Only 31.2% of Medicaid youth see a clinician within 7 days of a mental health emergency visit.</div>',
         f'<div class="bridge-stat">{FUM_LINE}</div>', 1),
    ],
    "site/team.html": [
        ("how a clinician sits with a patient who's struggling.",
         "how a clinician sits with a young person who's struggling.", 1),
        ("what BIPOC and LGBTQ+ patients are actually communicating",
         "what BIPOC and LGBTQ+ youth are actually communicating", 1),
        ("For many of the people Vasl serves,", "For many of the youth Vasl serves,", 1),
    ],
    "site/technology.html": [
        ("scores in Black and Latino patients?", "scores in Black and Latino youth aged 13-25?", 1),
        ("rate in Black, Latino, and LGBTQIA+ patients?", "rate in Black, Latino, and LGBTQIA+ youth?", 1),
    ],
    "site/clinical-outcomes.html": [
        ("The real-post corpus is public writing, not the patient messages and clinical text VLAP reads,",
         "The real-post corpus is adult public writing, not the patient messages and clinical text VLAP reads,", 1),
    ],
    "site/blog-crisis-without-solving.html": [
        ("In schools alone, the national student-to-school-counselor ratio is approximately 464:1, nearly double the 250:1 ratio recommended by the American School Counselor Association, and health systems and Medicaid plans face the same shortage of behavioral health clinicians.",
         "Health systems and Medicaid plans face a shortage of behavioral health clinicians.", 1),
    ],
}

for path, pairs in EDITS.items():
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    for old, new, n in pairs:
        c = s.count(old)
        assert c == n, f"{path}: expected {n}, found {c}: {old[:80]!r}"
        s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
    print(f"{path}: {len(pairs)} pairs applied")

# Applied inline after the run above: home hero and stat cells moved to the HEDIS FUM 7-day window;
# crisis-post sidebar ASCA 464:1 item removed; seo_titles and link_map youth strings pivoted.
