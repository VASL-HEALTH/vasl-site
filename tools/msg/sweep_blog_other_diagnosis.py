"""Blog stale-claim sweep: site/blog-other-diagnosis.html. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/blog-other-diagnosis.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ('<div class="as-stat-num">23 of 47</div><div class="as-stat-label">VLAP signals with no counterpart in the MIT / Child Mind / Crisis Text Line lexicon&rsquo;s 6,910 terms</div><div class="as-stat-caveat">Pilot data</div>',
     '<div class="as-stat-num">0.83 vs 0.65</div><div class="as-stat-label">VLAP against MIT&rsquo;s Suicide Risk Lexicon on suicide-attempt severity, ROC-AUC</div><div class="as-stat-caveat">Same corpus, same split</div>', 1),
    ('<div class="as-stat-num">5</div><div class="as-stat-label">Dimensions in the VLAP signal taxonomy, including CCM (Cultural Context Modifiers), which has no equivalent in standard NLP</div>',
     '<div class="as-stat-num">55</div><div class="as-stat-label">Signals across seven dimensions in the VLAP taxonomy, v2.0</div>', 1),
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
