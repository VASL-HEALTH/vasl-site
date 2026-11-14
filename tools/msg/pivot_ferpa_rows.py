"""School offer retired: drop the FERPA rows from the help center (whole st-row elements)."""
import re
from pathlib import Path
for path, label in [("site/help/vlap-technology.html", "FERPA"), ("site/help/compliance.html", "FERPA alignment")]:
    p = Path(path); s = p.read_text(encoding="utf-8")
    pat = r'        <div class="st-row">\n          <div class="st-label">' + re.escape(label) + r'</div>\n          <div class="st-value">[^<]*</div>\n        </div>\n'
    s, n = re.subn(pat, "", s); assert n == 1, (path, n)
    p.write_text(s, encoding="utf-8"); print(path, "row removed")
