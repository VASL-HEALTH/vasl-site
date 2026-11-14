"""Youth pivot, home page. Exact old/new pairs, each asserted."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_lib import run
PAIRS = [
    ('"Unaliving" is a youth-community coded term for self-harm ideation', '"Unaliving" is an online coded term for self-harm ideation', 1),
    ("lowkey been struggling since school started.", "lowkey been struggling since winter started.", 1),
    ("a documented pre-disclosure pattern in youth language.", "a documented pre-disclosure pattern in everyday speech.", 1),
    ("Our young people <em>aren&rsquo;t on it.</em>", "Our patients <em>aren&rsquo;t on it.</em>", 1),
    ("The language our young people use isn&rsquo;t on the field&rsquo;s map.", "The language our patients use isn&rsquo;t on the field&rsquo;s map.", 1),
    ('<div class="vc-persona">Youth Member, University of Maryland, Junior</div>', '<div class="vc-persona">Member, University of Maryland, Junior</div>', 1),
    ("The population-level insight from Vasl's org portal changes what a school counselor can see and when.",
     "Seeing the whole population at once changes what a counselor can see and when.", 1),
]
run(sys.argv[1] if len(sys.argv) > 1 else "site/index.html", PAIRS, "index")
