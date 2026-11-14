"""Youth pivot, Clinical Outcomes page."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_lib import run
PAIRS = [
    ("rural and Medicaid youth actually describe distress", "rural and Medicaid patients actually describe distress", 1),
    ("The real-post corpus is adult writing, not the 15 to 26 population VLAP serves, so it is supporting evidence",
     "The real-post corpus is public writing, not the patient messages and clinical text VLAP reads, so it is supporting evidence", 1),
]
run(sys.argv[1] if len(sys.argv) > 1 else "site/clinical-outcomes.html", PAIRS, "clinical-outcomes")
