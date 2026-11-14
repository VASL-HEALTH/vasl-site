"""Team page: old page kept; stale claims only."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/team.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("Delaware PBC · Techstars alumni · IRB active", "Delaware PBC · Techstars alumni", 1),
    ("We've built VLAP, the first culturally intelligent early-signal detection engine. We mapped 47 clinical signals across 6 categories, built a 2,400-token AAVE and youth-vernacular library, validated 90% sensitivity, and completed pilot-readiness with schools and youth-serving organizations.",
     "We've built VLAP, our own language model with our own weights. It flags 55 signals across seven dimensions with the words behind each, scores 0.83 against 0.65 for MIT's Suicide Risk Lexicon on suicide-attempt severity, and reaches 0.97 F1 on substance use in clinical notes.", 1),
    ("Co-Founder & CEO, Vasl Health, Inc.", "Co-Founder & CEO, Vasl Health PBC", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"team: {len(PAIRS)} pairs applied")
