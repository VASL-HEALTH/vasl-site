# -*- coding: utf-8 -*-
"""Builds site/partner-package.pdf.

    python tools/gen_partner_package.py            # writes site/partner-package.pdf
    python tools/gen_partner_package.py out.pdf    # writes somewhere else

WHY THIS FILE EXISTS
--------------------
The Partner Package shipped as a committed binary on 2026-09-08 with no
generator kept anywhere. That left 33 em dashes in a public, partner-facing
asset that `tools/check_copy.py` could not see, because check_copy only reads
.html/.xml/.txt. There was no source to fix, so the document is rebuilt here
and the copy now lives in `tools/partner_package_content.py`, where the copy
guard reads it like any other generator.

The layout is transcribed from that 2026-09-08 build: same 612x792 page, same
six faces, same palette, same coordinates. Design has not re-approved it, so
treat the output as a candidate, not the final artefact.

FONTS
-----
`tools/fonts/` holds six static TrueType faces pulled from Google Fonts, the
same source `site/*.html` already loads at runtime. Newsreader and IBM Plex
are both SIL Open Font License 1.1; `tools/fonts/OFL.txt` is the license.
They are committed because the build has to be reproducible, and because the
subsets embedded in the old PDF are not usable: each one carries only the
glyphs its own page happened to use, so IBM Plex Mono Medium has almost no
lowercase and Newsreader SemiBold is missing B, F, G, J, K, Q, U, X and Z.

DASHES
------
`assert_no_dashes()` fails the build on any em dash, en dash, or horizontal
bar, in the copy and in the PDF metadata, in literal or entity form. It runs
before anything is drawn. Do not route around it: the site has no dashes and
neither does this document.
"""
import pathlib
import re
import sys

import pymupdf

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from partner_package_content import PAGES  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "tools" / "fonts"
DEFAULT_OUT = ROOT / "site" / "partner-package.pdf"

FACE_FILE = {
    "news_sb": "Newsreader-SemiBold.ttf",
    "news_r": "Newsreader-Regular.ttf",
    "sans_r": "IBMPlexSans-Regular.ttf",
    "sans_sb": "IBMPlexSans-SemiBold.ttf",
    "mono_r": "IBMPlexMono-Regular.ttf",
    "mono_m": "IBMPlexMono-Medium.ttf",
}

# Every dash form, literal and encoded. Mirrors tools/check_copy.py.
#
# Built from codepoints rather than written out, so this file contains no
# literal dash and no dash entity of its own. check_copy.py scans tools/*.py
# and exempts only itself; spelling the forms here would make the guard fail
# on the file whose job is to enforce it.
DASH_FORMS = tuple(
    [chr(c) for c in (0x2014, 0x2013, 0x2015)]
    + ["&%s;" % n for n in ("mdash", "ndash")]
    + ["&#%d;" % c for c in (8212, 8211)]
    + ["&#%s%s;" % (x, h) for x in ("x", "X") for h in ("2014", "2013")]
)

META = {
    "title": "Vasl Health, Partner Package",
    "author": "Vasl Health PBC",
    "subject": "VLAP non-device clinical decision support for behavioral health",
    "creator": "tools/gen_partner_package.py",
    "keywords": "",
}

CARD_RADIUS = 3.0


def rgb(h):
    """'#1e4437' -> (0.117, 0.266, 0.215)"""
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def item_strings(it):
    """Every piece of copy an item carries."""
    out = []
    if "text" in it:
        out.append(it["text"])
    out.extend(it.get("lines", []))
    out.extend(r["t"] for r in it.get("runs", []))
    return out


def assert_no_dashes():
    bad = []
    for pg in PAGES:
        for it in pg["items"]:
            for t in item_strings(it):
                for form in DASH_FORMS:
                    if form in t:
                        bad.append((pg["page"], form, t[:80]))
    for k, v in META.items():
        for form in DASH_FORMS:
            if form in v:
                bad.append(("metadata:" + k, form, v))
    if bad:
        for where, form, t in bad:
            print("  DASH %-14s %-10r %r" % (where, form, t), file=sys.stderr)
        raise SystemExit("gen_partner_package: %d dash(es) in the copy. Refusing to "
                         "build." % len(bad))


def load_fonts():
    fonts = {}
    missing = [f for f in FACE_FILE.values() if not (FONT_DIR / f).is_file()]
    if missing:
        raise SystemExit("gen_partner_package: missing font file(s) in %s: %s"
                         % (FONT_DIR, ", ".join(missing)))
    for face, fname in FACE_FILE.items():
        fonts[face] = pymupdf.Font(fontfile=str(FONT_DIR / fname))
    return fonts


def assert_glyph_coverage(fonts):
    """A glyph the face lacks renders blank, silently. Fail instead."""
    bad = []
    for pg in PAGES:
        for it in pg["items"]:
            pieces = [(it.get("face"), t) for t in
                      ([it["text"]] if "text" in it else []) + it.get("lines", [])]
            pieces += [(r["face"], r["t"]) for r in it.get("runs", [])]
            for face, t in pieces:
                f = fonts.get(face)
                if f is None:
                    bad.append((pg["page"], face, "unknown face"))
                    continue
                for ch in t:
                    if ch == " ":
                        continue
                    if not f.has_glyph(ord(ch)):
                        bad.append((pg["page"], face, "U+%04X %r" % (ord(ch), ch)))
    if bad:
        for pno, face, what in sorted(set(bad)):
            print("  MISSING GLYPH p%-3s %-8s %s" % (pno, face, what), file=sys.stderr)
        raise SystemExit("gen_partner_package: %d missing glyph(s)." % len(set(bad)))


def wrap(font, text, size, width):
    """Greedy wrap.

    Breaks on spaces and, like the 2026-09-08 build, after an existing hyphen,
    so 'member-to-member' can break as 'member-to-' / 'member' instead of being
    forced whole onto the next line.
    """
    # Split into break-opportunity chunks: a space-delimited word may itself
    # break after any internal hyphen. The hyphen stays on the left chunk.
    chunks = []
    for i, word in enumerate(text.split(" ")):
        parts = re.split(r"(?<=-)(?=.)", word)
        for j, part in enumerate(parts):
            chunks.append({"t": part, "space_before": i > 0 and j == 0})

    lines, cur = [], ""
    for c in chunks:
        sep = " " if (c["space_before"] and cur) else ""
        trial = cur + sep + c["t"]
        if font.text_length(trial, fontsize=size) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = c["t"]
    if cur:
        lines.append(cur)
    return lines


def put(page, pt, text, face, size, color, fonts):
    page.insert_text(pt, text, fontname=face, fontfile=str(FONT_DIR / FACE_FILE[face]),
                     fontsize=size, color=rgb(color))
    return fonts[face].text_length(text, fontsize=size)


def put_tracked(page, pt, text, face, size, color, track, fonts):
    """Letterspacing, drawn per character. The original did the same."""
    f, x, y = fonts[face], pt[0], pt[1]
    extra = track * size
    for ch in text:
        if ch != " ":
            page.insert_text((x, y), ch, fontname=face,
                             fontfile=str(FONT_DIR / FACE_FILE[face]),
                             fontsize=size, color=rgb(color))
        x += f.text_length(ch, fontsize=size) + extra
    return x - pt[0]


def draw_shapes(page, draws):
    for d in draws:
        r = pymupdf.Rect(*d["rect"])
        if r.is_empty or r.width <= 0 or r.height <= 0:
            continue
        rounded = "c" in "".join(d.get("items", []))
        fill = rgb(d["fill"]) if d.get("fill") else None
        stroke = rgb(d["stroke"]) if d.get("stroke") else None
        width = d.get("width") or 0
        kw = {"color": stroke, "fill": fill, "width": width if stroke else 0}
        if rounded and min(r.width, r.height) > 2 * CARD_RADIUS:
            # pymupdf wants the radius as a fraction of the shorter side
            kw["radius"] = CARD_RADIUS / min(r.width, r.height)
        page.draw_rect(r, **kw)


def render(out_path):
    assert_no_dashes()
    fonts = load_fonts()
    assert_glyph_coverage(fonts)

    doc = pymupdf.open()
    for pg in PAGES:
        page = doc.new_page(width=612, height=792)
        draw_shapes(page, pg["draws"])
        for it in pg["items"]:
            x, y = it["x"], it["y"]
            face, size, color = it["face"], it["size"], it["color"]
            if "track" in it:
                put_tracked(page, (x, y), it["text"], face, size, color,
                            it["track"], fonts)
            elif "runs" in it:
                cx = x
                for r in it["runs"]:
                    cx += put(page, (cx, y), r["t"], r["face"], r["size"],
                              r["color"], fonts)
            elif "text" in it:
                if "wrap" not in it:          # single line, nothing to re-flow
                    put(page, (x, y), it["text"], face, size, color, fonts)
                    continue
                lead = it.get("lead") or size * 1.42
                for i, line in enumerate(wrap(fonts[face], it["text"], size,
                                              it["wrap"])):
                    put(page, (x, y + i * lead), line, face, size, color, fonts)
            else:
                lead = it.get("lead") or size * 1.42
                for i, line in enumerate(it["lines"]):
                    put(page, (x, y + i * lead), line, face, size, color, fonts)

    doc.set_metadata(META)
    # The six faces embed in full otherwise, which roughly trebles the file for
    # a document that uses a few hundred glyphs. This is a public download.
    try:
        doc.subset_fonts()
    except Exception as exc:                      # pragma: no cover
        print("gen_partner_package: font subsetting skipped (%s)" % exc,
              file=sys.stderr)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path), garbage=4, deflate=True)
    doc.close()
    return out_path


def main():
    out = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUT
    p = render(out)
    size = p.stat().st_size
    print("gen_partner_package: wrote %s (%d pages, %d bytes)"
          % (p.relative_to(ROOT) if ROOT in p.parents else p, len(PAGES), size))


if __name__ == "__main__":
    main()
