"""Blog stale-claim sweep: site/blog-crisis-without-solving.html. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/blog-crisis-without-solving.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("<p>This requires peer community as a first step because for many young people, particularly those from communities where mental health treatment carries stigma or where there is no family framework for understanding it, peer connection is the trust-building layer that makes professional care possible. It requires culturally matched coaches as a middle layer, people who share relevant cultural context with the young people they are supporting and who can serve as a bridge between peer community and clinical care.",
     "<p>This requires culturally matched coaches, people who share relevant cultural context with the young people they are supporting and who can serve as a bridge to clinical care.", 1),
    (" on suicide-attempt severity, and 23 of its 47 signals have no counterpart in that lexicon&rsquo;s 6,910 terms. Those are the measures that matter.",
     " on suicide-attempt severity, same corpus, same split. Those are the measures that matter.", 1),
    ("They are not the only measures that matter, the IRB validation study with a university research partner is building the independent evidence base that clinical AI requires.",
     "They are not the only measures that matter, and clinical AI still needs an independent evidence base.", 1),
    ('<div class="as-stat-num">23 of 47</div><div class="as-stat-label">VLAP signals with no counterpart in the lexicon&rsquo;s 6,910 terms</div><div class="as-stat-caveat">Measured</div>',
     '<div class="as-stat-num">55</div><div class="as-stat-label">VLAP signals across seven dimensions, Taxonomy v2.0</div><div class="as-stat-caveat">Measured</div>', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(p[1] for p in PAIRS) and "&mdash;" not in "".join(p[1] for p in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
