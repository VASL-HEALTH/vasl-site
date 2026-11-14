#!/usr/bin/env python3
"""Write every page in tools/retired.py as a noindex refresh stub, and check
that the CloudFront function carries the same map.

Run:  python3 tools/retire_pages.py            (writes)
      python3 tools/retire_pages.py --check    (exits 1 if anything would change)
"""
import re
import sys
from pathlib import Path

from retired import RETIRED

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
FUNC = ROOT / "infra" / "aws" / "site-pipeline" / "viewer-request.js"
ORIGIN = "https://gotovasl.com"


def stub(target: str) -> str:
    url = ORIGIN + target
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Vasl Health</title>
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={target}">
</head>
<body>
<p>This page has moved. <a href="{target}">Continue to {url}</a>.</p>
</body>
</html>
"""


def func_map() -> dict:
    src = FUNC.read_text(encoding="utf-8")
    body = src[src.index("var RETIRED = {"):src.index("};")]
    return dict(re.findall(r"'(/[^']+)':\s*'([^']*)'", body))


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for rel, target in RETIRED.items():
        path = SITE / rel
        want = stub(target)
        if not path.exists() or path.read_text(encoding="utf-8") != want:
            stale.append(rel)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(want, encoding="utf-8")
    expected = {"/" + rel[:-5]: t for rel, t in RETIRED.items()}
    fm = func_map()
    drift = sorted(set(expected.items()) ^ set(fm.items()))
    if drift:
        print("viewer-request.js RETIRED map differs from tools/retired.py:", drift)
        return 1
    if check and stale:
        print("stale stubs:", ", ".join(stale))
        return 1
    print(f"{'checked' if check else 'wrote'} {len(RETIRED)} retired page(s); {len(stale)} changed; function map matches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
