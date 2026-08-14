#!/usr/bin/env python3
"""
Render site/og-image.png — the default share card for every page.

Until this existed, every link Rodney pasted into Slack, LinkedIn, or a funder
email rendered as a bare grey box. This is the fallback card; per-page cards can
come later, but a site with zero OG images loses the click before the page loads.

Colors are lifted from the site's own :root custom properties so the card and
the site cannot drift apart.

Run: python3 tools/gen_og_image.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "site" / "og-image.png"
W, H = 1200, 630

WARM_WHITE = (250, 247, 242)
INK        = (28, 28, 28)
CLAY       = (196, 137, 111)
DEEP_GREEN = (45, 74, 62)
DUST       = (139, 123, 107)
INK_12     = (225, 221, 215)

SERIF = "/usr/share/fonts/truetype/crosextra/Caladea-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/crosextra/Caladea-Italic.ttf"
MONO  = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def main():
    img = Image.new("RGB", (W, H), WARM_WHITE)
    d = ImageDraw.Draw(img)

    # Left rule in clay — the site's own accent, so the card reads as Vasl at a glance.
    d.rectangle([0, 0, 10, H], fill=CLAY)

    pad = 84

    # Eyebrow
    d.text((pad, 92), "VASL HEALTH", font=f(MONO, 22), fill=DUST)

    # Wordmark-scale statement. Two lines, the second in clay italic — this is the
    # site's actual typographic move (roman + italic emphasis), not a generic headline.
    d.text((pad, 176), "Language", font=f(SERIF, 104), fill=INK)
    d.text((pad, 292), "is care.", font=f(SERIF_I, 104), fill=CLAY)

    # Hairline
    d.rectangle([pad, 440, W - pad, 441], fill=INK_12)

    # Positioning line — what a district or plan buyer needs to see in the preview.
    d.text(
        (pad, 474),
        "Culturally grounded behavioral health for youth 14–24.",
        font=f(SERIF, 34),
        fill=INK,
    )
    d.text(
        (pad, 522),
        "Detection, not diagnosis. Human in the loop, every time.",
        font=f(SERIF, 34),
        fill=DEEP_GREEN,
    )

    d.text((pad, 578), "gotovasl.com", font=f(MONO, 21), fill=DUST)

    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT}  ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
