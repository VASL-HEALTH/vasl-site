"""Site-wide sources of stale positioning: Organization schema, share image text, Health Plans pilot line."""
from pathlib import Path

EDITS = {
    "tools/seo_inject.py": [
        ('''                    "Vasl Health builds culturally grounded, clinically governed early "
                    "detection and behavioral health support for Black, Latino, and "
                    "first-generation youth ages 14 to 24."''',
         '''                    "Vasl Health PBC builds language intelligence for healthcare. "
                    "VLAP, Vasl Bridge and Vasl Keep serve Medicaid plans and health systems."''', 1),
        ('''                    "youth mental health",
                    "school-based mental health",''',
         '''                    "Medicaid member engagement",
                    "follow-up after emergency department visits",''', 1),
    ],
    "tools/gen_og_image.py": [
        ('"Culturally grounded behavioral health for youth 14 to 24."',
         '"Language intelligence for Medicaid plans and health systems."', 1),
        ('"Detection, not diagnosis. Human in the loop, every time."',
         '"A named signal with the words behind it. Never a diagnosis."', 1),
        ("# Positioning line, what a district or plan buyer needs to see in the preview.",
         "# Positioning line, what a plan or health-system buyer needs to see in the preview.", 1),
    ],
    "site/health-systems.html": [
        ("with real texts delivered. No pilot has run yet. Every pilot",
         "with real texts delivered. Every pilot", 1),
    ],
}

for path, pairs in EDITS.items():
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    for old, new, n in pairs:
        c = s.count(old)
        assert c == n, f"{path}: expected {n}, found {c}: {old[:80]!r}"
        s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
    print(f"{path}: {len(pairs)} pairs applied")
