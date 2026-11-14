"""clinical-outcomes: stale-claim sweep. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/clinical-outcomes.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # Hero stat 2: 47-signal overlap count -> approved substance-use result
    ("""        <div class="as-num">23 of 47</div>
        <div class="as-label">Signals With No Counterpart</div>
        <div class="as-sub">VLAP signals with no match anywhere in the lexicon&rsquo;s 6,910 terms, across five of our six dimensions, among them the signals for <em>unaliving</em> and <em>catching a fade</em>. Checkable in a minute by anyone who downloads their file.</div>""",
     """        <div class="as-num">0.97</div>
        <div class="as-label">Substance Use in Clinical Notes, F1</div>
        <div class="as-sub">On the n2c2 2022 SHAC test, 518 notes labeled by human annotators, against 0.83 for a keyword rule. Held-out test.</div>""", 1),
    # Hero stat 3: 47-signal synthetic micro-F1 -> current taxonomy
    ("""        <div class="as-num">0.9673</div>
        <div class="as-label">Micro-F1, All 47 Signals</div>
        <div class="as-sub">First-person youth check-ins, held-out <strong>synthetic</strong> text, n&nbsp;=&nbsp;2,992, run <code>vlap47_20260817T223142Z</code>. This figure stands alone: the clinician-note comparison it used to be paired with was retired on 26 Sept 2026 and no replacement pairing is published.</div>
        <div class="as-caveat">Synthetic corpus &middot; Non-diagnostic &middot; Not clinical validation</div>""",
     """        <div class="as-num">55</div>
        <div class="as-label">Signals Across Seven Dimensions</div>
        <div class="as-sub">Taxonomy v2.0. Each flag names the signal and shows the words behind it, never a score or a diagnosis.</div>
        <div class="as-caveat">Non-diagnostic &middot; For a clinician&rsquo;s independent review</div>""", 1),
    # Method 03: 47-signal overlap claim -> approved substance-use result
    ("""      <div class="mi-title">What the overlap claim is, and is not</div>
      <p class="mi-body">The vocabulary finding is mechanical string overlap and nothing more: 24 of our 47 signals share at least one string with the lexicon, so 23 share none. Whether a given construct and a given signal measure the same underlying thing is a clinical mapping question we have not done and do not assert.</p>""",
     """      <div class="mi-title">The second result, on clinical notes</div>
      <p class="mi-body">On substance use in clinical notes, VLAP scored 0.97 F1 on the n2c2 2022 SHAC test, 518 notes labeled by human annotators, against 0.83 for a keyword rule. It is a held-out test on real clinical text, separate from the severity comparison above.</p>""", 1),
    # Method 04: drop the retired synthetic figure sentence
    ("The 0.9673 micro-F1 figure is on <strong>synthetic</strong> text and is labelled as such everywhere it appears. ", "", 1),
    # CTA: IRB claim
    ("""        <div class="ci-label">IRB study access</div>
        <div class="ci-text">The IRB study protocol and preliminary design documentation are available to institutional evaluators under NDA.""",
     """        <div class="ci-label">Methodology access</div>
        <div class="ci-text">The study protocol and design documentation are available to institutional evaluators under NDA.""", 1),
    # Related reading: IRB claim
    ("The peer-reviewed literature and active IRB study this data builds on.",
     "The peer-reviewed literature this data builds on.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"clinical-outcomes: {len(PAIRS)} pairs applied")
