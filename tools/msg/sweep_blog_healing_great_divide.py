"""Blog stale-claim sweep: site/blog-healing-great-divide.html. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/blog-healing-great-divide.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    (" It means peer community as a first step rather than a supplement because for many young people, peer connection is where trust is built before professional care becomes possible.</p>",
     "</p>", 1),
    ("It means a care model that treats therapy as the end of a continuum rather than the beginning because for a first-generation",
     "It means a care model that does not make therapy the only door, because for a first-generation", 1),
    ("Peer community, culturally matched coaching, and AI-supported check-ins that actually understand how you communicate are accessible first steps. Therapy becomes accessible when trust has been built through those earlier layers.",
     "Culturally matched coaching and AI-supported check-ins that actually understand how you communicate are accessible first steps, and they lead to clinical care rather than replace it.", 1),
    ("The 2,400+ AAVE and youth vernacular tokens were not in any existing vocabulary before Vasl added them. The IRB study validating VLAP&rsquo;s signal detection against clinician-adjudicated ground truth takes years",
     "The community-annotated AAVE and youth vernacular in its language library was not in any existing vocabulary before Vasl added it. Validating VLAP&rsquo;s signal detection against clinician-adjudicated ground truth takes years", 1),
    (" on suicide-attempt severity, and 23 of its 47 signals have no counterpart in that lexicon&rsquo;s 6,910 terms. Those are measurements on a held-out split.",
     " on suicide-attempt severity. Those are measurements on a held-out split.", 1),
    ('<div class="as-stat-label">Peer community and a coach from the day of enrollment,',
     '<div class="as-stat-label">A coach from the day of enrollment,', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(p[1] for p in PAIRS) and "&mdash;" not in "".join(p[1] for p in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
