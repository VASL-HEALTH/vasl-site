"""Youth pivot, VLAP page. Exact old/new pairs, each asserted."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_lib import run
PAIRS = [
    ('A youth who says "I don\'t fw anything no more"', 'A patient who says "I don\'t fw anything no more"', 1),
    ("A youth who has learned to scan the room", "A member who has learned to scan the room", 1),
    ("Three different youth. Three different meanings.", "Three different patients. Three different meanings.", 1),
    ("The detection systems deployed on these young people were trained and validated on everyone else.",
     "The detection systems deployed on Medicaid members in these communities were trained and validated on everyone else.", 1),
    ("Rural and Appalachian youth are next,", "Rural and Appalachian speech is next,", 1),
    ("for a clinician's independent review, in the language youth actually use.",
     "for a clinician's independent review, in the words patients actually use.", 1),
    ("built on <em>how<br>youth actually speak.</em>", "built on <em>how<br>patients actually speak.</em>", 1),
    ("converting the language youth actually use into signal", "converting the words patients actually use into signal", 1),
    ("Five ways<br>youth signal<br>what words", "Five ways<br>patients signal<br>what words", 1),
    ("each is a different way a young person tells the truth", "each is a different way a patient tells the truth", 1),
    ("Youth often communicate serious distress through affect", "People often communicate serious distress through affect", 1),
    ("Withdrawal in youth often precedes escalation", "Withdrawal often precedes escalation", 1),
    ("Reads coded alertness language common in youth navigating", "Reads coded alertness language common in people navigating", 1),
]
run(sys.argv[1] if len(sys.argv) > 1 else "site/vlap.html", PAIRS, "vlap")
