import sys
from pathlib import Path

P = Path("site/blog-mental-health-equity-crisis.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ('Why the access gap for Black, Latino, and LGBTQ+ youth is also', 'Why the access gap for Black, Latino, and LGBTQ+ patients is also', 4),
    ('continue to fail Black, Latino, and LGBTQ+ youth.', 'continue to fail Black, Latino, and LGBTQ+ patients.', 1),
    ('Black and Latino youth are more likely to drop out of mental health treatment before the third session than their white peers. LGBTQ+ youth experience', 'Black and Latino patients are more likely to drop out of mental health treatment before the third session than white patients. LGBTQ+ people experience', 1),
    ('First-generation youth, navigating the dual pressure of academic performance and cultural identity, arrive at campus counseling centers with presentations', 'People who are the first in their families to seek care, navigating the dual pressure of work and cultural identity, arrive at clinics and emergency departments with presentations', 1),
    ('When applied to Black and Latino youth, it consistently', 'When applied to Black and Latino patients, it consistently', 1),
    ('When a Black and Latino youth writes', 'When a member writes', 1),
    ('that Black, Latino, and LGBTQ+ youth use to communicate', 'that Black, Latino, and LGBTQ+ patients use to communicate', 1),
    ('a word that LGBTQ+ youth developed specifically', 'a word people online developed specifically', 1),
    ('community-annotated AAVE and youth vernacular, was', 'community-annotated AAVE and everyday speech, was', 1),
    ('When young people feel seen', 'When patients feel seen', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
joined = "".join(p[1] for p in PAIRS)
assert "—" not in joined and "&mdash;" not in joined and "&#8212;" not in joined
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
