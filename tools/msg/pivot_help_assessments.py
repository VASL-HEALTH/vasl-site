"""Help: assessments. School/parents framing to members and organizations. Exact pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/assessments.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("They are never shared with your school, your employer, your parents, or your organization's administrators.",
     "They are never shared with your employer, your family, or your organization's administrators.", 1),
    ("Your assessment scores are classified as protected health information under HIPAA, not as an education record under FERPA. Your school cannot access them under any circumstances.",
     "Your assessment scores are classified as protected health information under HIPAA. Your organization's administrators cannot access them under any circumstances.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(x[1] for x in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
