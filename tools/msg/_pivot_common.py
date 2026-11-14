import sys
from pathlib import Path
def apply(path, pairs):
    p = Path(path); s = p.read_text(encoding="utf-8")
    for old, new, n in pairs:
        c = s.count(old)
        assert c == n, f"{p}: expected {n}, found {c}: {old[:90]!r}"
        s = s.replace(old, new)
    p.write_text(s, encoding="utf-8")
    print(f"{p}: {len(pairs)} pairs applied clean")
