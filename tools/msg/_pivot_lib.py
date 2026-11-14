import sys
from pathlib import Path
def run(path, pairs, name):
    P = Path(path); s = P.read_text(encoding="utf-8")
    for old, new, n in pairs:
        c = s.count(old)
        assert c == n, f"{name}: expected {n}, found {c}: {old[:90]!r}"
        s = s.replace(old, new)
    P.write_text(s, encoding="utf-8")
    print(f"{name}: {len(pairs)} pairs applied")
