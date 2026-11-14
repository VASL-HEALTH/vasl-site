"""Youth pivot, Bridge page. The 31.2% / 26.5% Medicaid-youth figures are the cited Hoffmann et al., Pediatrics 2023 stats and stay verbatim."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_lib import run
PAIRS = [
    ("Every kid you miss comes back.", "Every patient you miss comes back.", 1),
    ('alt="A young person lying on a bed at home, holding a phone above them."', 'alt="A person lying on a bed at home, holding a phone above them."', 1),
    ("from the day a young person leaves the emergency department", "from the day a patient leaves the emergency department", 1),
    ("rural and Medicaid youth actually describe distress", "rural and Medicaid patients actually describe distress", 1),
    ("the social worker enrolls the young person,", "the social worker enrolls the patient,", 1),
]
run(sys.argv[1] if len(sys.argv) > 1 else "site/bridge.html", PAIRS, "bridge")
