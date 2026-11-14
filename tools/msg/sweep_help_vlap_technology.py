"""Stale-claim sweep: vlap_technology. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/vlap-technology.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("including a vocabulary extension of 2,400+ AAVE and youth vernacular tokens not found in standard NLP training corpora. The model identifies patterns across six clinical categories and surfaces",
     "including a community-annotated language library not found in standard NLP training corpora. The model flags 55 signals across seven dimensions and surfaces", 1),
    ("VLAP analyzes language across six clinical categories. Each captures",
     "VLAP flags 55 signals across seven dimensions. The core categories are below. Each captures", 1),
    ("""        <div class="callout-label">90% Sensitivity, What This Means</div>
        <p class="callout-text">VLAP achieves approximately 90% sensitivity on high-distress signal detection in active IRB validation with a university research partner. Sensitivity measures how consistently the model detects signals when present, not the rate at which all surfaced signals are clinically significant. The clinical significance of any surfaced signal is determined through human review.</p>""",
     """        <div class="callout-label">Measured Results</div>
        <p class="callout-text">On suicide-attempt severity, VLAP scores 0.83 ROC-AUC against 0.65 for MIT&rsquo;s Suicide Risk Lexicon on the same corpus and split. On substance use in clinical notes, it scores 0.97 F1 on the n2c2 2022 SHAC test set (518 notes). The clinical significance of any surfaced signal is determined through human review.</p>""", 1),
    ("It does not scan peer group posts, social media,", "It does not scan social media,", 1),
    ("against the 47-signal taxonomy across six categories.", "against 55 signals across seven dimensions.", 1),
    ("""          <div class="does-item">Scan or process peer group posts</div>\n""", "", 1),
    ("<strong>2,400+</strong> AAVE and youth vernacular tokens beyond standard BERT vocabulary, community-sourced, clinically validated",
     "Community-annotated language library beyond standard BERT vocabulary, community-sourced, clinically validated", 1),
    ("<strong>47 signals</strong> across 6 clinical categories: HOP, SHA, CCM, ISO, TRM, PFE",
     "<strong>55 signals</strong> across seven dimensions (Taxonomy v2.0)", 1),
    ("""          <div class="st-label">Sensitivity</div>
          <div class="st-value"><strong>~90%</strong> on high-distress signal detection, active IRB validation with a university research partner. Results to be published upon study completion.</div>""",
     """          <div class="st-label">Results</div>
          <div class="st-value"><strong>0.83 vs 0.65</strong> ROC-AUC on suicide-attempt severity against MIT&rsquo;s Suicide Risk Lexicon; 0.97 F1 on substance use, n2c2 2022 SHAC test, 518 notes</div>""", 1),
    ("BAA required for all organizational deployments. Annual SOC 2 Type II audit.", "BAA required for all organizational deployments.", 1),
    ("surface to Client Org Portal,", "surface to organization reporting,", 1),
    ("the 37-page model specification, IRB study protocol, signal taxonomy", "the 37-page model specification, signal taxonomy", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)
assert "—" not in "".join(n for _, n, _ in PAIRS) and "&mdash;" not in "".join(n for _, n, _ in PAIRS)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")


# Follow-up: output carries the words behind it.
FOLLOW_UP = [("Processing happens in-memory, verbatim content is not stored after signal profile generation. The output is a dimensional signal profile, not a transcript or quote.", "Patient text is read on Vasl infrastructure and never sent to an outside AI company. The output is a named signal with the words behind it, never a score or a diagnosis.")]
