"""
Shared configuration for the SEO tooling.

IGNORE holds paths, relative to site/, that no generator may ever touch,
add to the sitemap, inject into, or validate against normal HTML-page
invariants. Import this in every generator rather than hard-coding the set
separately, so there is exactly one place to add the next exception.

Currently just the Google Search Console verification file: it's plain text
("google-site-verification: <token>") wearing an .html extension, not a real
page, and Google rejects the verification if a single byte of it changes —
so seo_inject.py must never inject a head layer into it, seo_titles.py must
never rewrite a <title> it doesn't have, gen_sitemap.py must never list it as
an indexable URL, seo_validate.py must never check it for a canonical/h1/
title/description it was never going to have, and internal_links.py must
never treat it as a page that can carry or receive a related-reading link.
"""

IGNORE = {
    "google21b71dccc4b8882d.html",
    # demo.html is a redirect to vlap-standalone.gotovasl.com, not a page. It
    # carries noindex and a canonical pointing at another origin; seo_inject
    # would overwrite both with index,follow and a self-canonical on
    # gotovasl.com/demo, which is the opposite of what a redirect needs, and
    # canonical_for() cannot express a cross-origin target. It has no title,
    # description or h1 story for the other generators to validate either.
    "demo.html",
    # prototype.html is the same shape: a redirect to
    # vlap-standalone.gotovasl.com, not a page. Same reasons as demo.html --
    # the injector would replace its noindex and cross-origin canonical with
    # index,follow and a self-canonical.
    "prototype.html",
}
