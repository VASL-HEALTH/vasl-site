"""Careers page: stale-claim sweep only. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/careers.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # Why-join 02: drop 23-of-47 and peer community claims, add approved substance-use result
    ("0.65. 23 of 47 signals with no counterpart in its 6,910 terms. Peer community and a coach from the day of enrollment, against a 9-month national average wait. These are measurements",
     "0.65 on suicide-attempt severity. 0.97 F1 on substance use in clinical notes (n2c2 2022 SHAC test, 518 notes). These are measurements", 1),
    # Why-join 04: drop research collaboration and IRB claims
    ("An active health-system research collaboration. IRB study with a university research partner. Senior Medical Advisor from Johns Hopkins.",
     "Senior Medical Advisor from Johns Hopkins. VLAP is non-device clinical decision support under Section 3060 of the 21st Century Cures Act.", 1),
    # Clinical research role body
    ("The active IRB study with a university research partner is the immediate context for this role. You will be working with real clinical data from real deployed cohorts, under real IRB oversight, with real peer-reviewed publication as an output.",
     "You will be working with real clinical data, with peer-reviewed publication as an output.", 1),
    ("clinical validation studies for the VLAP signal taxonomy, in partnership with an active university IRB study</div>",
     "clinical validation studies for the VLAP signal taxonomy</div>", 1),
    ("Publish research findings in peer-reviewed journals, IRB study publication is a primary deliverable</div>",
     "Publish research findings in peer-reviewed journals</div>", 1),
    # Culture 02
    ("rigorous research, IRB study data, and clinical validation.",
     "rigorous research and clinical validation.", 1),
    ("0.83 against the field&rsquo;s published lexicon, 23 of 47 signals it has no word for, it comes",
     "0.83 against the field&rsquo;s published lexicon, 0.97 F1 on substance use in clinical notes, it comes", 1),
    # Culture 03: peer group as an offering
    ("Design decisions, peer group architecture, VLAP training corpus annotation, all shaped",
     "Design decisions and VLAP training corpus annotation, all shaped", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"careers: {len(PAIRS)} pairs applied")
