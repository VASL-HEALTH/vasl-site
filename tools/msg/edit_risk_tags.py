"""No scores on the site: strip per-signal risk tags, severity labels, old per-category counts and
unverified training-data counts from Technology and the AI model page. Add Keep to what VLAP reads.
Contact prefill string loses its em dash."""
import re
from pathlib import Path


def apply(path, pairs=(), regexes=()):
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    for old, new, n in pairs:
        c = s.count(old)
        assert c == n, f"{path}: expected {n}, found {c}: {old[:80]!r}"
        s = s.replace(old, new)
    for pat, repl, n in regexes:
        s, c = re.subn(pat, repl, s)
        assert c == n, f"{path}: regex {pat!r} expected {n}, got {c}"
    p.write_text(s, encoding="utf-8")
    print(f"{path}: {len(pairs)} pairs, {len(regexes)} patterns applied")


apply("site/technology.html",
    pairs=[
        ("VLAP training data includes 340+ AAVE futility constructions. This single signal accounts for the largest share of VLAP's sensitivity advantage over baseline.",
         "This is one of the clearest gaps between VLAP and generic models.", 1),
        ("VLAP's training data includes 180+ documented uses with clinical annotation. This is one of the clearest demonstrations of generic model failure and VLAP's advantage.",
         "VLAP's training data includes documented uses with clinical annotation.", 1),
        ("VLAP's training data includes 95+ community-specific death euphemisms with clinical annotation.",
         "VLAP's training data includes community-specific death euphemisms with clinical annotation.", 1),
        ("replies to Vasl Bridge texts, and notes over HL7 FHIR R4",
         "replies to Vasl Bridge and Vasl Keep texts, and notes over HL7 FHIR R4", 1),
        ("replies to Vasl Bridge texts, patient messages,",
         "replies to Vasl Bridge and Vasl Keep texts, patient messages,", 1),
    ],
    regexes=[
        (r'<span class="sig-risk risk-(?:high|low|mod|var)">[^<]*</span>', "", 47),
        (r'<p class="sig-note">CRITICAL, ([a-z])', lambda m: '<p class="sig-note">' + m.group(1).upper(), 4),
    ])

apply("site/ai-model.html",
    regexes=[
        (r'<span class="tax-signal-risk tsr-(?:high|low|mod|var)">[^<]*</span>', "", 47),
        (r'<div class="tax-count">\d+</div>', '<div class="tax-count"></div>', 6),
    ])

apply("site/contact.html", pairs=[
    ('"Requesting the Vasl Partner Package (PDF) \\u2014 technology, deployment patterns, and evidence/validation status."',
     '"Requesting the Vasl Partner Package (PDF): technology, deployment patterns, and evidence/validation status."', 1),
])
