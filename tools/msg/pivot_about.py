"""Youth pivot, About page. Partner program descriptions (Thread YMCA, Boys & Girls Clubs) stay verbatim."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_lib import run
PAIRS = [
    ("lowkey been struggling since school started.", "lowkey been struggling since winter started.", 1),
]
run(sys.argv[1] if len(sys.argv) > 1 else "site/about.html", PAIRS, "about")
