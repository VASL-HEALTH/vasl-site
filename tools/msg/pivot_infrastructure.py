"""Youth pivot, Infrastructure page."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_lib import run
PAIRS = [
    ("what a district IT reviewer or plan security team needs before a deployment.", "what a health system IT reviewer or plan security team needs before a deployment.", 3),
    ("rural and Medicaid youth. Not additional work", "rural and Medicaid patients. Not additional work", 1),
    ('<div class="sh-card-title">Young People &amp; Families</div>', '<div class="sh-card-title">Patients &amp; Members</div>', 1),
    ("removes the barriers between young people and the support they need", "removes the barriers between patients and the support they need", 1),
]
run(sys.argv[1] if len(sys.argv) > 1 else "site/infrastructure.html", PAIRS, "infrastructure")
