"""Glossary: stale-claim sweep. No replacements were needed; this asserts the
stale claims are absent from both the page and its source (tools/glossary_terms.py,
which seo_inject.py uses for the JSON-LD), so a rebuild cannot reintroduce them."""
import re
import sys
from pathlib import Path

FILES = [Path(sys.argv[1] if len(sys.argv) > 1 else "site/glossary.html"),
         Path("tools/glossary_terms.py")]

PAIRS = []  # (old, new, expected_count): none required on this page

STALE = [r"47[ -](clinical )?signal", r"\b(six|6) (clinical )?categories", r"2,400\+|2,400[- ]token",
         r"90% sensitivity", r"\bIRB\b", r"SOC 2", r"Vasl Health, Inc\.", r"therapy last",
         r"Coach Portal", r"Member App", r"Client Org Portal", r"Abridge", r"Hazel", r"UPMC",
         r"\bpeer groups?\b"]

for P in FILES:
    s = P.read_text(encoding="utf-8")
    for old, new, n in PAIRS:
        c = s.count(old)
        assert c == n, f"{P}: expected {n}, found {c}: {old[:90]!r}"
        s = s.replace(old, new)
    for pat in STALE:
        hits = re.findall(pat, s, flags=re.I)
        assert not hits, f"{P}: stale claim still present: {pat!r} x{len(hits)}"
    P.write_text(s, encoding="utf-8")

print(f"glossary: {len(PAIRS)} pairs applied, {len(STALE)} stale patterns absent in {len(FILES)} files")
