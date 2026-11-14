import sys
from pathlib import Path

P = Path("site/blog-other-diagnosis.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ('what it looks like for Black, Latino, and LGBTQ+ youth.', 'what it looks like for Black, Latino, and LGBTQ+ patients.', 4),
    ('The stressors Black, Latino, and LGBTQ+ youth carry', 'The stressors Black, Latino, and LGBTQ+ patients carry', 1),
    ('When a Black and Latino adolescent sits', 'When a Black or Latino patient sits', 1),
    ('code-switching between home and school', 'code-switching between home and work', 1),
    ('For Black, Latino, and LGBTQ+ youth, the stress', 'For Black, Latino, and LGBTQ+ patients, the stress', 1),
    ('&rdquo; in a classroom, a workplace, or a clinical setting', '&rdquo; in a workplace, a waiting room, or a clinical setting', 1),
    ('A student who ', 'A patient who ', 2),
    ('LGBTQ+ youth face a related', 'LGBTQ+ patients face a related', 1),
    ('A teenager who presents as anxious', 'A patient who presents as anxious', 1),
    ('what a young person is saying', 'what a patient is saying', 1),
    ('A young person who has learned that their distress is not legible to adults in their environment', 'A patient who has learned that their distress is not legible to the people around them', 1),
    ('working with Black, Latino, and LGBTQ+ youth is', 'working with Black, Latino, and LGBTQ+ patients is', 1),
    ('the diagnosis of a young person whose distress', 'the diagnosis of a patient whose distress', 1),
    ('many of the young people who most need', 'many of the people who most need', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
joined = "".join(p[1] for p in PAIRS)
assert "—" not in joined and "&mdash;" not in joined and "&#8212;" not in joined
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
