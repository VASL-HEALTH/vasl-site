"""Privacy page claims sweep: company name, SOC 2. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/privacy.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("HIPAA, FERPA, and SOC 2 Type II compliant.", "HIPAA and FERPA compliant.", 3),
    ('    <span class="doc-badge">FERPA Compliant</span>\n    <span class="doc-badge">SOC 2 Type II</span>\n',
     '    <span class="doc-badge">FERPA Compliant</span>\n', 1),
    ("This Privacy Policy describes how Vasl Health, Inc. (",
     "This Privacy Policy describes how Vasl Health PBC (", 1),
    ("The platform is hosted on SOC 2 Type II compliant cloud infrastructure with",
     "The platform is hosted on cloud infrastructure with", 1),
    ('\n\n      <div class="section-sub">SOC 2 Type II</div>\n'
     '      <p class="doc-p">Our annual SOC 2 Type II audit covers security, availability, and confidentiality trust service criteria. The full audit report is available to institutional partners under NDA. Audit is conducted by an independent third-party auditor.</p>\n',
     "\n", 1),
    ("Vasl Health, Inc. is a Delaware Public Benefit Corporation.",
     "Vasl Health PBC is a Delaware Public Benefit Corporation.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:70]!r}"
    s = s.replace(old, new)
P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS)} pairs applied")
