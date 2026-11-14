"""dialect-bias-mental-health-screening.html: youth -> patients/members pivot (BRIEF_YOUTH). Copy only."""
from pathlib import Path

P = Path("site/dialect-bias-mental-health-screening.html")

PAIRS = [
    ("the district administrator choosing a screening tool, the health plan quality lead",
     "the health system leader choosing a screening tool, the Medicaid plan quality lead", 1),
    ("A young person who expresses distress through", "A patient who expresses distress through", 1),
    ("structured engagement with youth from the communities represented",
     "structured engagement with people from the communities represented", 1),
    ("Youth vernacular carries sincerity markers, phrasing",
     "In many communities, everyday speech carries sincerity markers, phrasing", 1),
    ("automated systems reading youth language for signs of risk, includes a real and growing set of "
     "student-surveillance vendors, tools built to monitor, flag, or score students for administrators",
     "automated systems reading patient language for signs of risk, includes a real and growing set of "
     "surveillance vendors, tools built to monitor, flag, or score people for administrators", 1),
    ("a relationship with the young person, a coach,", "a relationship with the patient or member, a coach,", 1),
    ("Monitor, score, or rank individual students for administrators.",
     "Monitor, score, or rank individual patients or members for administrators.", 1),
    ("Flag students to school security, law enforcement,",
     "Flag patients or members to security, law enforcement,", 1),
]

s = P.read_text(encoding="utf-8")
for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
P.write_text(s, encoding="utf-8")
print(f"dialect-bias: {len(PAIRS)} pairs applied")
