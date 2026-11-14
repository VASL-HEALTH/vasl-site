"""dialect-bias-mental-health-screening: stale-claim sweep. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/dialect-bias-mental-health-screening.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # 2,400+ tokens -> no number
    ("VLAP's vocabulary extension, over 2,400 AAVE and youth vernacular tokens, developed through",
     "VLAP's vocabulary extension, a community-annotated language library developed through", 1),
    # 47 signals / six categories
    ("a taxonomy of 47 signals across six categories, developed",
     "a taxonomy of 55 signals across seven dimensions, developed", 1),
    # IRB study + 90% sensitivity -> approved results
    ("Vasl is conducting an active IRB-approved study with a university research partner, validating VLAP's signal detection against clinician-adjudicated ground truth, with preliminary findings indicating approximately 90% sensitivity on high-distress signal detection. That figure is preliminary and the study is ongoing, we report it as the current state of what we know, not as a settled result.",
     "On held-out data, VLAP scored 0.83 ROC-AUC on suicide-attempt severity against 0.65 for MIT's Suicide Risk Lexicon on the same corpus and split, and 0.97 F1 on substance use in clinical notes (n2c2 2022 SHAC test, 518 notes) against 0.83 for a keyword rule.", 1),
    # CTA: 47 signals
    ("How VLAP's 47 signals are organized,",
     "How VLAP's 55 signals across seven dimensions are organized,", 1),
    # Related reading: the "active validation study" was the IRB study
    ("The peer-reviewed literature and active validation study behind Vasl's approach.",
     "The peer-reviewed literature and validation results behind Vasl's approach.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"dialect-bias-mental-health-screening: {len(PAIRS)} pairs applied")
