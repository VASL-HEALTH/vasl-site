# -*- coding: utf-8 -*-
"""Fail on any dash form or slop word in the site or in the generators.

Run by hand before a push:

    python tools/check_copy.py

DELIBERATELY NOT A CI JOB. It is not referenced by any workflow and must not
be. The brief for this surface says no new Actions checks.

Why it covers tools/ as well as site/: the title REWRITES dict in
seo_titles.py, the definitions in glossary_terms.py, the anchor text in
link_map.py and the copy in gen_demo_explainer.py are all written INTO the
pages by generators. Cleaning a page without cleaning its generator means the
next `python tools/seo_inject.py` puts the dash back, and the page looks fixed
until someone regenerates. So both sides are checked.

Exit 0 clean, 1 with a report of every offending file:line.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
TOOLS = ROOT / "tools"

# Every form the inventory found, plus the three numeric-entity spellings that
# were absent but would read identically if anyone introduced them.
DASHES = {
    "—": "literal em dash",
    "–": "literal en dash",
    "&mdash;": "&mdash; entity",
    "&ndash;": "&ndash; entity",
    "&#8212;": "&#8212; entity",
    "&#8211;": "&#8211; entity",
    "&#x2014;": "&#x2014; entity",
    "&#x2013;": "&#x2013; entity",
    "&#X2014;": "&#X2014; entity",
    "&#X2013;": "&#X2013; entity",
}

SLOP = [
    "delve", "pivotal", "crucial", "landscape", "tapestry", "testament",
    "underscore", "navigate", "robust", "seamless", "leverage", "unlock",
    "empower", "game-changer", "cutting-edge", "transformative", "holistic",
    "synergy", "moreover", "furthermore", "in today's world",
    "it's worth noting",
]

# `prototype/` is not deployed and is out of scope. This file names the dash
# forms and the slop words it hunts, so it must exempt itself or it fails on
# its own source.
SELF = pathlib.Path(__file__).resolve()

# The one narrow sense of a slop word that is the correct technical term. See
# the exemption in main() for why it is scoped this tightly.
ORIENTATION = re.compile(
    r"landscape\s+(orientation|mode)|in\s+landscape\b|\(landscape\)|tablet[^.]{0,40}landscape")


def targets():
    for p in sorted(SITE.rglob("*")):
        if p.is_file() and p.suffix in (".html", ".xml", ".txt"):
            yield p
    for p in sorted(TOOLS.glob("*.py")):
        if p.resolve() != SELF:
            yield p


def main() -> int:
    problems = []
    scanned = 0

    for path in targets():
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            problems.append((rel, 0, "not valid UTF-8"))
            continue

        for n, line in enumerate(lines, 1):
            for form, label in DASHES.items():
                if form in line:
                    problems.append((rel, n, f"{label} x{line.count(form)}"))
            low = line.lower()
            for word in SLOP:
                # Word boundaries, so "unlocking" is caught but "flandscape"
                # would not be, and a hyphenated slop word still matches.
                if not re.search(r"(?<![\w-])" + re.escape(word) + r"(?![\w-])", low):
                    continue
                if word == "landscape" and ORIENTATION.search(low):
                    # "a tablet in landscape", "landscape orientation" is the
                    # literal name of a screen orientation, not the figurative
                    # noun. Four uses in help/technical.html and support.html
                    # are device requirements; replacing the word there would
                    # make the instruction wrong. The figurative sense is still
                    # caught, because this exemption needs the orientation
                    # context on the same line.
                    continue
                problems.append((rel, n, f"slop word {word!r}"))

    if problems:
        print(f"COPY CHECK: {len(problems)} problem(s) in {scanned} files\n")
        last = None
        for rel, n, what in problems:
            if rel != last:
                print(f"  {rel}")
                last = rel
            print(f"      line {n}: {what}")
        print(f"\n{len(problems)} problem(s). No dash form or slop word may ship.")
        return 1

    print(f"COPY CHECK: clean. {scanned} files, "
          f"{len(DASHES)} dash forms and {len(SLOP)} slop words, zero hits.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
