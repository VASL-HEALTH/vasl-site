"""Blog stale-claim sweep: site/blog-human-is-the-system.html. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/blog-human-is-the-system.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("47 signals across six clinical categories,", "55 signals across seven dimensions,", 1),
    ("VLAP&rsquo;s high-distress signal sensitivity is 90% in preliminary results from an active IRB-approved validation study with a university research partner, measured against clinician-adjudicated ground truth. Those results are pending peer-reviewed publication, and we say so every time we cite the number. Sensitivity",
     "On suicide-attempt severity, VLAP scores 0.83 ROC-AUC against 0.65 for MIT&rsquo;s Suicide Risk Lexicon, on the same corpus and the same split. Sensitivity", 1),
    (" It flags. It does not decide. In our pilot cohorts, roughly one in five members is connected to licensed clinical care through a warm handoff from the coaching layer, and every one of those handoffs runs through a person.</p>",
     " It flags. It does not decide.</p>", 1),
    ("VLAP sensitivity, retention, and escalation figures are from Vasl pilot cohorts and an active IRB study; see",
     "VLAP results are from held-out test data, same corpus, same split; see", 1),
    ('<div class="as-stat-num">90%</div><div class="as-stat-label">High-distress signal sensitivity against clinician-adjudicated ground truth</div><div class="as-stat-caveat">Preliminary &middot; IRB validation in progress &middot; pending publication</div>',
     '<div class="as-stat-num">0.83</div><div class="as-stat-label">VLAP ROC-AUC on suicide-attempt severity, against 0.65 for MIT&rsquo;s Suicide Risk Lexicon</div><div class="as-stat-caveat">Same corpus &middot; same split</div>', 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(p[1] for p in PAIRS) and "&mdash;" not in "".join(p[1] for p in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
