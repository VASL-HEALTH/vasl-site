import sys
from pathlib import Path

P = Path("site/blog-missing-infrastructure.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ('the detection systems deployed in schools and clinics during', 'the detection systems deployed in clinics, emergency departments and Medicaid plans during', 1),
    ('A young person who codes-witches into AAL', 'A patient who code-switches into AAL', 1),
    ('Rural and Appalachian youth are next,', 'Rural and Appalachian speech is next,', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
joined = "".join(p[1] for p in PAIRS)
assert "—" not in joined and "&mdash;" not in joined and "&#8212;" not in joined
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
