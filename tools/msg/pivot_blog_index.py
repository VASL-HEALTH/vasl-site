"""Youth pivot: blog.html (index). Exact pairs, each count asserted.
Hoffmann et al. stat in the featured sidebar stays verbatim: cited source."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_common import apply
PAIRS = [
 ("and Black youth are less likely still. What happens in that week, why check-in replies",
  "and Black youth are less likely still (Pediatrics, 2023). What happens in that week for Medicaid members, why check-in replies", 1),
 ("why it matters most for the young people whose risk is rising fastest.", "why it matters most for the patients standard tools hear least clearly.", 1),
 ("no notifications to principals or parents,", "no notifications to employers or family members,", 1),
 ("continue to fail Black, Latino, and LGBTQ+ youth.", "continue to fail Black, Latino, and LGBTQ+ patients.", 1),
 ('<span class="ar-tag">Youth Mental Health</span>', '<span class="ar-tag">Behavioral Health</span>', 1),
 ("traditional approaches to the youth mental health crisis", "traditional approaches to the behavioral health crisis", 1),
 ("the full picture for Black, Latino, and LGBTQ+ youth.", "the full picture for Black, Latino, and LGBTQ+ patients.", 1),
]
apply(sys.argv[1] if len(sys.argv) > 1 else "site/blog.html", PAIRS)
