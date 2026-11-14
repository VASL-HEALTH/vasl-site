"""ai-model.html: youth -> patients/members pivot (BRIEF_YOUTH). Copy only."""
from pathlib import Path

P = Path("site/ai-model.html")

PAIRS = [
    ("VLAP: AI Trained on How Youth Actually Speak",
     "VLAP: AI Trained on How Patients Actually Speak", 3),
    ("Standard clinical NLP misreads AAVE and youth vernacular. VLAP is trained on it directly,",
     "Standard clinical NLP misreads AAVE, rural speech and queer vernacular. VLAP is trained on them directly,", 3),
    ("the coded language Black, Brown, LGBTQ+, rural and Medicaid youth use to describe pain",
     "the coded language Black, Brown, LGBTQ+, rural and Medicaid members use to describe pain", 1),
    ("Utterances drawn from Black, Latino, LGBTQ+, and youth in urban and rural communities mental health language corpora,",
     "Mental health language corpora drawn from Black, Latino, LGBTQ+, and Medicaid patients in urban and rural communities,", 1),
    ("drawn from Black, Latino, LGBTQ+, and youth in urban and rural communities.",
     "drawn from Black, Latino, LGBTQ+, and Medicaid patients in urban and rural communities.", 1),
    ("trauma-adjacent idiom, and youth-specific coded language.",
     "trauma-adjacent idiom, and community-specific coded language.", 1),
    ("queer vernacular, youth coded language (including euphemisms for self-harm ideation)",
     "queer vernacular, community coded language (including euphemisms for self-harm ideation)", 1),
    ("lowkey been struggling since school started.", "lowkey been struggling since winter started.", 2),
    ("these are the expressions young people actually use,", "these are the expressions patients actually use,", 1),
    ("School discipline and push-out (“they're trying to expel me”)",
     "Discipline and push-out at school, work or home (“they're trying to put me out”)", 1),
    ('"They\'re trying to expel me."', '"They\'re trying to put me out."', 1),
    ("TRM-06, School discipline and push-out.", "TRM-06, Discipline and push-out.", 1),
    ("developed for White, middle-class youth populations.", "developed for White, middle-class populations.", 1),
    ('"Unaliving" is a youth-community euphemism', '"Unaliving" is an online-community euphemism', 1),
    ("a documented pattern in youth language where the speaker hedges",
     "a documented pattern in everyday speech where the speaker hedges", 1),
    ("channels where youth have explicitly chosen to share", "channels where patients have explicitly chosen to share", 1),
    ("a community-annotated library of AAVE and youth vernacular added",
     "a community-annotated library of AAVE, rural speech and queer vernacular added", 1),
    # FERPA compliance item: school-only, removes cleanly
    ('        <div class="compliance-item">\n'
     '          <div class="ci-name">FERPA</div>\n'
     '          <div class="ci-right">\n'
     '            <div class="ci-title">Student records handled per FERPA requirements for school-based deployments.</div>\n'
     '            <div class="ci-desc">School-based program deployments operate under FERPA-compliant data handling protocols. Student health records segregated from academic records. Consent architecture designed for minor students and their guardians.</div>\n'
     '          </div>\n'
     '        </div>\n\n', "", 1),
]

s = P.read_text(encoding="utf-8")
for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)
P.write_text(s, encoding="utf-8")
print(f"ai-model: {len(PAIRS)} pairs applied")
