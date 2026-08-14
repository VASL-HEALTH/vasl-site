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
}
