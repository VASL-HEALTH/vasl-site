import sys
from pathlib import Path

P = Path("site/blog-healing-great-divide.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ('Black and Latino youth access mental health care', 'Black and Latino patients access mental health care', 1),
    ('LGBTQ+ youth experience mental health crises', 'LGBTQ+ people experience mental health crises', 1),
    ('First-generation college students, many of whom', 'Members who are the first in their families to seek care, many of whom', 1),
    ('Reaching a check-in, a peer community or a coaching session', 'Reaching a check-in or a coaching session', 1),
    ('for a first-generation college student who has never spoken', 'for a member who has never spoken', 1),
    ('community-annotated AAVE and youth vernacular in', 'community-annotated AAVE and everyday speech in', 1),
    ('<div class="as-stat"><div class="as-stat-num">464:1</div><div class="as-stat-label">National average student-to-counselor ratio in K-12 schools, 6x the recommended standard</div><div class="as-stat-caveat">ASCA 2024</div></div>\n', '', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
joined = "".join(p[1] for p in PAIRS)
assert "—" not in joined and "&mdash;" not in joined and "&#8212;" not in joined
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
