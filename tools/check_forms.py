# -*- coding: utf-8 -*-
"""Static contract check for the three site forms. No browser, no network.

Each form POSTs JSON to the Vasl forms API. Three ways that silently breaks:
an id the handler reads is renamed in the markup (TypeError before the fetch,
so the form just does nothing), a field name drifts from what the handler
reads, or a success state is shown on something other than a 200.

Run: python tools/check_forms.py
"""
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
ENDPOINT = "2hwpnt5k46.execute-api.us-east-1.amazonaws.com"

# form file -> (hidden `form` value, field names the handler must receive)
FORMS = {
    "contact.html": ("contact", {
        "form", "first_name", "last_name", "email", "org_name", "role",
        "org_type", "pop_size", "timeline", "additional", "interest", "page",
    }),
    "support.html": ("support", {
        "form", "name", "email", "organization", "category", "message", "page",
    }),
    "blog.html": ("newsletter", {"form", "email", "page"}),
}

errors = []


def err(msg):
    errors.append(msg)


for fname, (form_value, expected_fields) in FORMS.items():
    src = (SITE / fname).read_text(encoding="utf-8")

    # 1. the endpoint is the production one, and there is exactly one
    if src.count(ENDPOINT) != 1:
        err(f"{fname}: expected exactly one reference to the production endpoint, found {src.count(ENDPOINT)}")
    for bad in ("localhost", "127.0.0.1", "execute-api.us-west", "staging"):
        if bad in src:
            err(f"{fname}: non-production host {bad!r} in the shipped page")

    # 2. the hidden field the handler routes on
    if f'name="form" value="{form_value}"' not in src:
        err(f'{fname}: missing hidden <input name="form" value="{form_value}">')

    # 3. every getElementById the handler dereferences must exist as an id
    ids_read = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", src))
    ids_read |= set(re.findall(r"val\('([^']+)'\)", src))
    ids_present = set(re.findall(r'\bid="([^"]+)"', src))
    for i in sorted(ids_read - ids_present):
        err(f"{fname}: script reads #{i} but no element has that id")

    # 4. the payload keys the handler sends must be the contract
    body = src[src.index("const payload = {"):] if "const payload = {" in src else ""
    if fname == "blog.html":
        body = src[src.index("vaslPost({"):]
    sent = set(re.findall(r"^\s{6}([a-z_]+):", body[:1200], re.M))
    sent |= set(re.findall(r"\b(form|email|page)\s*:", body[:400]))
    missing = expected_fields - sent - {"interest"} if fname != "contact.html" else expected_fields - sent
    if fname == "contact.html" and "interest" not in body[:1200]:
        err("contact.html: payload omits `interest`, so template B is unreachable")
    for m in sorted(missing):
        err(f"{fname}: payload omits {m!r}")

    # 5. no mailto: submission path left in a handler
    if re.search(r"location\.href\s*=\s*[`'\"]mailto:", src):
        err(f"{fname}: a handler still navigates to mailto: instead of posting")

    # 6. the success state must be inside the try, after the await
    # anchor on `catch (err)`: vaslPost has its own inner try/catch
    # around the JSON parse, and that is not the request guard.
    try_block = re.search(r"try \{(.*?)\} catch \(err\)", src, re.S)
    if not try_block:
        err(f"{fname}: handler has no try/catch around the request")
    else:
        inner = try_block.group(1)
        if "await vaslPost" not in inner:
            err(f"{fname}: vaslPost is not awaited inside the try block")
        if fname == "contact.html":
            if "showPartnerPackageDownload()" not in inner:
                err("contact.html: Partner Package reveal is not gated on a successful response")
            if "plausible(" not in inner:
                err("contact.html: the Plausible event is not gated on a successful response")

    # 7. the failure path must be visible to the user
    catch = re.search(r"\} catch \(err\) \{(.*?)\n  \}", src, re.S)
    if not catch or "vaslRenderError" not in catch.group(1):
        err(f"{fname}: the catch block does not render a visible error")

    # 8a. the body must declare UTF-8. Without the charset parameter API
    #     Gateway mis-decodes every non-ASCII character the visitor typed.
    if "'Content-Type': 'application/json; charset=utf-8'" not in src:
        err(f"{fname}: Content-Type does not declare charset=utf-8")

    # 8. vaslPost must treat a non-200 or ok!=true as a failure
    if "if (!res.ok || !data || data.ok !== true)" not in src:
        err(f"{fname}: vaslPost does not reject a non-200 / ok!=true response")

# 9. the dead-CTA regex must accept the canonical pretty URL
inj = (SITE.parent / "tools" / "seo_inject.py").read_text(encoding="utf-8")
m = re.search(r"'if\(/(.*?)/\.test\(href\)\)\{'", inj)
if not m:
    err("seo_inject.py: could not find the CTA regex")
else:
    pattern = m.group(1).replace("\\\\", "\\")
    for href, should in (("/contact", True), ("/contact.html", True),
                         ("/contact?subject=Pro Plan", True), ("/contact-us", False)):
        if bool(re.search(pattern, href)) is not should:
            err(f"seo_inject.py CTA regex: {href!r} should {'match' if should else 'not match'}")

if errors:
    print("FORM CONTRACT: %d problem(s)" % len(errors))
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("FORM CONTRACT: all checks pass (3 forms)")
