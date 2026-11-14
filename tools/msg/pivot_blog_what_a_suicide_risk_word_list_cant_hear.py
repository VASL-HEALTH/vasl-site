"""Youth pivot: blog/what-a-suicide-risk-word-list-cant-hear. Exact pairs, each count asserted.
Stone et al. (MMWR 2025) and Hoffmann et al. (Pediatrics 2023) figures stay verbatim: cited sources."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_common import apply
PAIRS = [
 ("why it matters most for the young people whose risk is rising fastest.", "why it matters most for the patients standard tools hear least clearly.", 4),
 ("against the language young people actually use", "against the words patients actually use", 1),
 ("first-generation and rural young people describe being in trouble", "first-generation and rural patients describe being in trouble", 1),
 ("reads the text that already exists around a young person in care", "reads the text that already exists around a patient in care", 1),
 ("and the young people whose risk is rising fastest rarely describe distress that way. Between 2018 and 2023,",
  "and many of the patients those tools miss rarely describe distress that way. The gap shows up in the numbers: between 2018 and 2023,", 1),
 ("a futility narrative common among LGBTQ+ youth.", "a futility narrative common among LGBTQ+ people.", 1),
 ("a foreclosure narrative common among first-generation young people.", "a foreclosure narrative common among first-generation patients.", 1),
 ("because some of these young people text crisis lines", "because some of these patients text crisis lines", 1),
 ("overlaps heavily with the young people whose suicide risk is rising fastest.", "overlaps heavily with the groups whose suicide risk is rising fastest.", 1),
 ("Every one of those returns is a young person whose distress", "Every one of those returns is a patient whose distress", 1),
 ("LGBTQ+ youth language is built", "queer vernacular is built", 1),
 ("especially for the young people the current tools hear least.", "especially for the patients the current tools hear least.", 1),
]
apply(sys.argv[1] if len(sys.argv) > 1 else "site/blog/what-a-suicide-risk-word-list-cant-hear.html", PAIRS)
