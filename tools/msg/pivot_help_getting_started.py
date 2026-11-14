"""Help: getting started. Youth/school access framing to health plans, health systems and members. Exact pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/getting-started.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("built specifically for the communities it serves, BIPOC, LGBTQ+, and first-generation youth, with support rooted in cultural understanding,",
     "built specifically for the communities it serves, urban and rural, and the words people there actually use, with support rooted in cultural understanding,", 1),
    ("Access comes through an organization, your school, university, health plan, or community org, that has a Vasl partnership.",
     "Access comes through an organization, your health plan, health system, clinic, or community org, that has a Vasl partnership.", 1),
    ("Your school or org will send you an enrollment link or code, usually by email or through a student/member portal.",
     "Your health plan or org will send you an enrollment link or code, usually by email or through a member portal.", 1),
    ("<strong>None of this is shared with your school, your teachers, your parents, or your employer.</strong>",
     "<strong>None of this is shared with your employer, your family, or your organization's administrators.</strong>", 1),
    ("If you think your school or org should have Vasl but you haven't received access info, contact your school counselor, student services office, or HR department.",
     "If you think your health plan or org should have Vasl but you haven't received access info, contact your plan's member services, your care team, or your HR department.", 1),
    ("It is not seen by your school, your parents, your employer, or anyone outside your care team.",
     "It is not seen by your family, your employer, or anyone outside your care team.", 1),
    ('<div class="pt-h">School / Org Admin</div>',
     '<div class="pt-h">Org Admin</div>', 1),
    ("Your school administrator or employer sees only aggregate,",
     "Your organization's administrator or employer sees only aggregate,", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(x[1] for x in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
