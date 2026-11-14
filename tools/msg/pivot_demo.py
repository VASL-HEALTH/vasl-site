"""Youth pivot, demo page (meta and og description)."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_lib import run
PAIRS = [
    ("showing how it reads distress in the language youth actually write.", "showing how it reads distress in the words patients actually write.", 2),
]
run(sys.argv[1] if len(sys.argv) > 1 else "site/demo.html", PAIRS, "demo")
