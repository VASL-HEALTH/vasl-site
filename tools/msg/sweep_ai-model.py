"""AI model page: stale-claim sweep only. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/ai-model.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # meta, og, twitter
    ("VLAP is trained on it directly, 2,400+ tokens, six signal categories, no diagnostic output.",
     "VLAP is trained on it directly, with a community-annotated language library, 55 signals across seven dimensions and no diagnostic output.", 3),

    # Chapter 01 model stats
    ("""        <div class="ms-num">90<span style="font-size: 20px">%</span></div>
        <div class="ms-label">Sensitivity on high-distress<br>signal detection</div>""",
     """        <div class="ms-num">0.83<span style="font-size: 20px"> vs 0.65</span></div>
        <div class="ms-label">Suicide-attempt severity,<br>VLAP vs MIT&rsquo;s lexicon</div>""", 1),
    ("""        <div class="ms-num">47</div>
        <div class="ms-label">Clinical signals<br>across 6 categories</div>""",
     """        <div class="ms-num">55</div>
        <div class="ms-label">Signals across<br>seven dimensions</div>""", 1),
    ("""        <div class="ms-num">2,400<span style="font-size: 16px">+</span></div>
        <div class="ms-label">AAVE & youth vernacular<br>tokens in vocabulary</div>""",
     """        <div class="ms-num">0.97</div>
        <div class="ms-label">F1 on substance use<br>in clinical notes</div>""", 1),

    # Chapter 02 training block
    ("<div class=\"tb-value\">2,400+ tokens added to base vocabulary: AAVE constructions,",
     "<div class=\"tb-value\">A community-annotated language library added to the base vocabulary: AAVE constructions,", 1),
    ("<div class=\"tb-value\">Active IRB study in partnership with a university research partner validating clinical signal accuracy in production deployment. Study ongoing, results to be published upon completion</div>",
     "<div class=\"tb-value\">0.83 vs 0.65 ROC-AUC on suicide-attempt severity against MIT&rsquo;s Suicide Risk Lexicon, same corpus, same split. 0.97 F1 on substance use in clinical notes, n2c2 2022 SHAC test, 518 notes</div>", 1),

    # Chapter 03 taxonomy header
    ("""      47 signals.<br>
      6 categories.<br>""",
     """      55 signals.<br>
      Seven dimensions.<br>""", 1),
    ("The VLAP Distress Signal Taxonomy (v1.0) defines every signal",
     "The VLAP Distress Signal Taxonomy (v2.0) defines every signal", 1),

    # Pipeline
    ("Text is received from Member App check-ins and coach messaging, channels where",
     "Text is received from patient replies and messages in the clinician&rsquo;s workflow, channels where", 1),
    ("Channel: Member App &middot; Coach messaging &middot; Consent-gated input only",
     "Channel: Patient replies &middot; Clinician&rsquo;s workflow &middot; Consent-gated input only", 1),
    ("vocabulary which includes the 2,400+ AAVE and youth vernacular tokens added to the base vocabulary.",
     "vocabulary which includes a community-annotated library of AAVE and youth vernacular added to the base vocabulary.", 1),
    ("Extended BERT-family tokenizer &middot; 2,400+ custom tokens &middot;",
     "Extended BERT-family tokenizer &middot; Community-annotated language library &middot;", 1),
    ("evaluating the input against all 47 signals across six clinical categories simultaneously.",
     "evaluating the input against all 55 signals across seven dimensions simultaneously.", 1),
    ("and delivered to the clinician's Coach Portal view.",
     "and delivered into the clinician's workflow.", 1),
    ("Coach Portal delivery &middot; Raw text discarded",
     "Delivered in the clinician&rsquo;s workflow &middot; Raw text discarded", 1),
    ("Coach Portal access requires licensed clinician credential verification. Member-facing app has zero API surface to VLAP output.",
     "Access in the clinician&rsquo;s workflow requires licensed clinician credential verification. Nothing member-facing has any API surface to VLAP output.", 1),
    ("Access control is architectural, not policy-based, member app and clinical portal are separate systems.",
     "Access control is architectural, not policy-based. Member-facing systems and clinical systems are separate.", 1),

    # Validation (IRB claims out, approved results in)
    ("""        In active<br>
        <em>clinical validation.</em>""",
     """        Measured<br>
        <em>on clinical text.</em>""", 1),
    (" VLAP is in active clinical deployment, with a parallel IRB study underway at an independent academic research institution validating signal accuracy in production conditions. The model earns its claim in the real world, with real youth, under real clinical oversight. Results will be published upon study completion.",
     " VLAP is measured against outside benchmarks on clinical text. On suicide-attempt severity it scored 0.83 ROC-AUC against 0.65 for MIT&rsquo;s Suicide Risk Lexicon, on the same corpus and the same split. On substance use in clinical notes it scored 0.97 F1 on the n2c2 2022 SHAC test set of 518 notes, against 0.83 for a keyword rule.", 1),
    ("""        <div class="irb-label">Active Study, IRB Approved</div>
        <div class="irb-title">Clinical Signal Accuracy Validation, VASL-IRB-001</div>
        <div class="irb-desc">IRB-approved study validating VLAP signal accuracy against licensed clinician assessment in production deployment conditions. Study evaluates signal sensitivity, specificity, and demographic subgroup parity across Black, Latino, LGBTQ+, and youth in urban and rural communities.</div>
        <div class="irb-status">Study in progress, results to be published upon completion</div>""",
     """        <div class="irb-label">Results</div>
        <div class="irb-title">Suicide-attempt severity, VLAP vs MIT&rsquo;s Suicide Risk Lexicon</div>
        <div class="irb-desc">0.83 vs 0.65 ROC-AUC, same corpus, same split.</div>
        <div class="irb-status">Substance use in clinical notes: 0.97 F1, n2c2 2022 SHAC test, 518 notes</div>""", 1),

    # SOC 2 item removed (HIPAA, BAA item already present above it)
    ("""        <div class="compliance-item">
          <div class="ci-name">SOC 2 Type II</div>
          <div class="ci-right">
            <div class="ci-title">Annual third-party security audit. Full report available under NDA.</div>
            <div class="ci-desc">SOC 2 Type II certification covering security, availability, and confidentiality trust service criteria. Third-party audit conducted annually. Report available to clinical partners under NDA upon request.</div>
          </div>
        </div>

""", "", 1),

    # Spec TOC
    ("<div class=\"stoc-title\">VLAP Distress Signal Taxonomy v1.0, Full Definitions</div>",
     "<div class=\"stoc-title\">VLAP Distress Signal Taxonomy v2.0, Full Definitions</div>", 1),
    ("Pages 13 to 20 &middot; 47 signal definitions &middot;",
     "Pages 13 to 20 &middot; 55 signal definitions &middot;", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"ai-model: {len(PAIRS)} pairs applied")

# Follow-up (applied separately after the first run): intro no longer promises risk weighting.
FOLLOW_UP = [("Each signal has a clinical definition, a community-language annotation, and a risk-level weighting. None produce a diagnosis.",
              "Each signal has a clinical definition and a community-language annotation. The rows below are examples. None produce a score or a diagnosis.")]
