import sys
from pathlib import Path

P = Path("site/blog-human-is-the-system.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ('the same young person writing about not sleeping, not eating with their family, and not seeing the point of school,', 'the same member writing about not sleeping, not eating with their family, and not seeing the point of going to work,', 1),
    ('draw it for the young people we serve.', 'draw it for the patients and members we serve.', 1),
    ('For Black, Latino, and LGBTQ+ youth, the blind spots', 'For Black, Latino, and LGBTQ+ patients, the blind spots', 1),
    ('A young person who writes &ldquo;been thinking about unaliving lately ngl&rdquo; is using a euphemism that youth communities developed', 'A member who writes &ldquo;been thinking about unaliving lately ngl&rdquo; is using a euphemism that online communities developed', 1),
    ('lowkey been struggling since school started', 'lowkey been struggling since the new job started', 1),
    ('escalates a young person to a principal or a parent for talking', 'escalates a patient to an employer or a relative for talking', 1),
    ('what it means for this young person, today.', 'what it means for this patient, today.', 1),
    ('No young person ever sees a signal code', 'No member ever sees a signal code', 1),
    ('Organizations, whether a school district, a university, a health plan, or a community nonprofit, see aggregate, de-identified trends and never an individual young person.', 'Organizations, whether a Medicaid plan, a health system, or a community clinic, see aggregate, de-identified trends and never an individual member.', 1),
    ('VLAP does not send alerts to police, principals, or parents. It does not show individual conversations to schools or funders.', 'VLAP does not send alerts to police, employers, or relatives. It does not show individual conversations to plan administrators or funders.', 1),
    ('that a family or a school needs to be involved', 'that a family or a caseworker needs to be involved', 1),
    ('Ask a sixteen-year-old in any of the communities we serve', 'Ask a member in any of the communities we serve', 1),
    ('why young people go quiet', 'why people go quiet', 1),
    ('who knows the young person&rsquo;s context', 'who knows the member&rsquo;s context', 1),
    ('never to administrators, payers, or automated systems', 'never to administrators, outside parties, or automated systems', 1),
    ('costs the young person something: a phone call home,', 'costs the member something: an unwanted phone call,', 1),
    ('before it reaches a young person.', 'before it reaches a patient.', 1),
    ('the districts, health systems, and families we work with', 'the Medicaid plans, health systems, and members we work with', 1),
    ('starting with rural and Appalachian youth after', 'starting with rural and Appalachian speech after', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
joined = "".join(p[1] for p in PAIRS)
assert "—" not in joined and "&mdash;" not in joined and "&#8212;" not in joined
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
