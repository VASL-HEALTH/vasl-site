"""Youth pivot, Tour page."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_lib import run
PAIRS = [
    ('<span class="member-card__who">Nia Adeyemi, sixteen</span>', '<span class="member-card__who">Nia Adeyemi</span>', 1),
    ("Where a young person actually lives in the product: daily check-ins, Grow exercises, peer communities.",
     "Where a member actually lives in the product: daily check-ins and Grow exercises.", 1),
]
run(sys.argv[1] if len(sys.argv) > 1 else "site/tour.html", PAIRS, "tour")
