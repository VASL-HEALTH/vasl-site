# Backlog — vasl-site

Triaged and deliberately NOT fixed. One line each. Opened 2026-10-12 from the
UPMC-diligence review of main (`04d4651..HEAD`). A line leaving this file means
it was measured, not that it was commented on.

## Claims — FOUNDER / COUNSEL DECISION, not an engineering fix

These are CONFIRMED and several are Critical. They were deliberately left alone:
rewriting public compliance and clinical claims is not a change to make silently.

- `site/privacy.html:6,16,25` — "HIPAA, FERPA, and SOC 2 Type II compliant" in the indexed meta description; nothing in the repo substantiates any of the three.
- `site/about.html:988-990`, `site/ai-model.html:1546,1549` — "SOC 2 Type II **certification** … audit conducted **annually**"; SOC 2 Type II is an attestation report, not a certification, and "annually" asserts a plural audit history.
- Same claim rendered five different ways across the site, from "certification" to "documentation" — `site/pricing.html:381,481`, `site/technology.html:2165,2262`, `site/help/compliance.html:537`, `site/platform.html:1635`, `site/team.html:1014`, `site/support.html:671,809`, `site/privacy.html:174,263,283`.
- `site/ai-model.html:1524` — "it **is in active clinical deployment**", against a model recorded NOT PRODUCTION READY and no live client orgs; `site/about.html:917` and `ai-model.html:1530` say validation is "in production deployment".
- `site/ai-model.html:1528-1530` — "IRB Approved", protocol `VASL-IRB-001`; no IRB of record, institution, approval number or date appears anywhere in the repo. Also `about.html:740,917`, `blog-bridging-chasm.html:259`, `blog-human-is-the-system.html:280`, `careers.html:809,909,925,993`.
- The "90% sensitivity" figure — `blog-bridging-chasm.html:276` ("~90%"), `blog-human-is-the-system.html:280,302` ("90%"), `about.html:739,1105`, `ai-model.html:940`, `for-organizations.html:488`. Recall is explicitly NOT measured; the precision mismatch between pages is its own inconsistency.
- `0.8255`/`0.6489` quoted bare on 11 pages with no register, n, or comparator — only `site/clinical-outcomes.html` carries them. Ground truth's weak-register figures (0.7417 pooled ROC-AUC n=18; 0.2986 SI recall @ 0.6923 precision) appear on NO page.
- `site/clinical-outcomes.html:349` — the 0.8088/0.5074 VLAP-SHA-REAL-001 result is quoted accurately but the page does not say that run is recorded NON_SHIPPABLE.
- `site/about.html:1083` — "The numbers below are measurements… not projected", on the same page as the unmeasured 90% figure.
- `site/pricing.html:503`, `site/for-schools.html:1255` — the "~50% Medicaid recovery" assumption that the headline "~$38 per student per year" depends on, presented beside hard prices as though quoted.
- `site/team.html:800-801,840-841` — "Chief Clinical Director" and "Chief Medical Officer" (the CMO being a PhD psychologist while the page's MD is titled "Senior Medical Advisor"); `:750-751,783` titles Hants Williams "Head of Data Science" while listing a full-time Fordham role.
- `site/about.html:977-979` — "FERPA-compliant" alongside the claim that Vasl is not a school agent, which is the posture under which FERPA does not apply.
- `site/team.html:582`, `site/blog-missing-infrastructure.html:235` — unfalsifiable "the first" claims.
- "2,400+ community-specific tokens" — stable at 2,400+ across 16 occurrences, but what it counts drifts ("community-specific", "AAVE and youth vernacular", "cultural tokens"), and nothing substantiates the count or its provenance.

## Tooling and CI

- No branch protection on main at all (`gh api .../branches/main/protection` → 404), and `deploy-site.yml` never references `seo-check.yml`: a red seo-check blocks nothing, on a PR or on main.
- `tools/seo_validate.py:201-202` — the broken-internal-link check is `warn()`, not `err()`, so the invariant its docstring advertises cannot fail the build. (No link is currently broken.)
- `tools/seo_validate.py:180` — the link regex excludes `#` and `?` from the character class, so every fragment- and query-bearing href is never examined at all.
- `tools/seo_validate.py:136-138` — the OG check is a substring test for `property="og:title"`; `content=""` or a wrong value passes. This is the class of bug that shipped `/vlap` with `og:description="Vasl"`.
- `tools/seo_validate.py:142` — the JSON-LD scan requires one exact literal, so a hand-written block with different quoting is not found and the check passes over an empty collection.
- `tools/seo_validate.py:68-70` — `head_of()` falls back to the first 8000 bytes when `</head>` is absent, with no error.
- `tools/seo_inject.py:398-406,419-421` and `tools/internal_links.py:131-138` — a page missing its anchor is skipped and `--check` still exits 0; internal_links counts the skipped page's links in its success total.
- `tools/gen_sitemap.py:80-81` — bare `except Exception: pass` turns a git failure into today's date as `<lastmod>` for every page.
- `tools/seo_inject.py:436` — `write_text` without `newline=""` rewrites every page's line endings on a Windows run.
- `deploy-site.yml:143-164` — the smoke test covers 6 of 47 pages, reads only the status code (`-o /dev/null`), asserts no `Cache-Control`, never fetches sitemap/robots/og-image, probes neither `/blog` nor `/blog/<slug>`, and cannot detect a failed invalidation.
- No Python tests anywhere; nothing collects `tools/` (~130KB of generators). `--check` modes compare a generator's output to the file the same generator wrote, so a bug symmetric in the generator is undetectable.
- `tools/seo_inject.py:73-89` — `POST_DATES` is a hand-maintained dict; a new nested blog post that is forgotten silently loses its BlogPosting and BreadcrumbList, and no check asserts a post has article markup.
- `tools/gen_sitemap.py` PRIORITY — dead entry for the retired `outcomes.html`.

## Links and SEO

- 38 pages link to `demo.html` relative (plus 1 as `/demo.html`), a `noindex` meta-refresh stub that bounces cross-origin to `vlap-standalone.gotovasl.com` (verified live, 200). Two hops, no 301, so the "VLAP Signal Taxonomy" anchor text is spent on a deindexed page.
- `site/netlify.toml:19` — declares a `/demo → /demo.html` 301 in a file whose own header says CloudFront does not read it.
- Four pages carry over-long meta descriptions (`blog/what-a-suicide-risk-word-list-cant-hear.html` 289 chars, `clinical-outcomes.html` 188, `blog-human-is-the-system.html` 175, `blog-missing-infrastructure.html` 174).
- Substantive claim-level duplication between `vlap.html`, `ai-model.html` and `technology.html` is unreviewed.

## Forms — follow-on work

- No browser-level test that the three forms actually submit end to end; `tools/check_forms.py` is a static contract check only. Needs a headless run asserting the success state renders and no console error on load.
- Server-side validation is authoritative but untested from the client's side: 400/422/429/500 and a network rejection each need an asserted visible error.
- The PII-in-analytics promise on `contact.html` is enforced by a comment plus `tools/check_forms.py`'s structural check, not by an assertion on the event payload itself.

## Server-side form contract (VASL-PLATFORM, follow-on PR)

- `forms/handler.py:218,513` — `email` is capped to 320 BEFORE `EMAIL_RE` runs, so a 325-char address truncating to a valid shorter one is accepted as a DIFFERENT address and the acknowledgment is sent to a domain the visitor does not own. Validate first, cap second, or reject over-length. (`maxlength="320"` now on all three inputs as a client-side mitigation only.)
- `forms/handler.py:249-267` — `_interests` coerces a bare string to a one-element list instead of splitting it, so a comma-joined `interest` value silently misses the `partner-package` membership test and template B, the only one carrying the PDF link, becomes unreachable with no 400 and no log.
- `forms/handler.py:285,305` — a `SUPPORT_CATEGORY` or `ORG_TYPE_PARAGRAPH` miss falls through to a plausible default ("Support", the "Other" paragraph) with no log line, so a renamed option value is indistinguishable from a visitor choosing Other. Log the miss.
- `forms/handler.py:313` — `_opted_in` is a truthiness test, so `{"updates":"off"}` or `"false"` would record marketing consent. Accept only `on`/`true`/`1`/`True`.
- `forms/handler.py:363-374,443` — `unsubscribed` is never cleared, so a re-subscribe returns 200, suppresses the welcome email, and the site says "You're subscribed. Check your inbox." while the unsubscribe page says re-subscribing from the blog works.
- `forms/handler.py:372-374` — a DynamoDB throttle makes `_is_suppressed` fail closed, suppressing a legitimate welcome email while the visitor sees success; nothing on the row marks it, so it is unrecoverable without log archaeology.
- `forms/handler.py:502` — the honeypot key is `website`, an obvious field for an org-profile form; the day one is added every submission is silently discarded behind a success message. Rename to something no designer reaches for.
- `forms/handler.py:168,510` — `MAX["form"]` is dead (`form` is capped by the `category` entry), contradicting the comment that every submittable field is named.
- The `vaslPost`/`vaslRenderError` helper and the API id are triplicated across the three pages — deliberate, because a shared `.js` asset ships under the deploy's one-year immutable cache and is not in the invalidation path, but it means an endpoint change is three edits.

## Tooling, from the contract review

- `tools/internal_links.py:125` — the loop iterates the hand-maintained `LINKS` dict, not the filesystem, so **21 eligible pages get no related-reading block and are never named in the output**, including `blog.html`, `contact.html`, `team.html`, all 7 `help/*`, both flat blog posts and the new nested post. `--check` exits 0.
- `tools/gen_sitemap.py:34,102` — `PRIORITY.get(rel, DEFAULT)` reads a missing page as 0.5/monthly rather than flagging it; the table still carries an entry for the retired `outcomes.html`.
- The page set is independently re-derived five times (three `rglob` filters plus two hand-maintained dicts), sharing only `IGNORE`.
