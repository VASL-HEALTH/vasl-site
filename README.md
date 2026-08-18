# Vasl Health — Public Site

One deployment: `site/` → **gotovasl.com** on S3 + CloudFront.

| Page | Source | URL |
|------|--------|-----|
| Marketing site | `site/` | gotovasl.com |
| Platform prototype | `site/prototype.html` | gotovasl.com/prototype.html |
| VLAP live demo | `site/demo.html` | gotovasl.com/demo.html |

Every page's footer links to it as **VLAP Signal Demo**, alongside
**Live Demo Portal** (`prototype.html`) — they are different artifacts and both
are linked.

**There are no `demo.` or `prototype.` subdomains.** Both are NXDOMAIN and are
not coming back; the pages are served as paths on the main site. Do not cite the
subdomains in decks, docs or email — they are dead links.

History, so this does not get "fixed" back the wrong way:

- `demo/` was a static, hardcoded sales demo with no backend. Deleted
  2026-07-28 (`e2f7b24`) at Rodney's request and replaced the same day by a
  real one (`27db9ff`) that calls vlap-service directly.
- `demo.gotovasl.com` has been NXDOMAIN since that deletion — it predates the
  Netlify→AWS migration and is *deliberately* absent from the zone. See the
  comments in `VASL-PLATFORM/infra/aws/dns/records_web.tf`.
- `prototype/` is the older standalone Netlify copy, superseded by
  `site/prototype.html`. It is kept for now but nothing serves from it.

## Deploying

Push to `main` touching `site/**` → `.github/workflows/deploy-site.yml` syncs
to S3 and invalidates CloudFront. That is the whole pipeline.

## Updating a Page

All pages are plain HTML — edit any `.html` file under `site/` and push to
`main`. Changes go live once the deploy workflow finishes the S3 sync and the
CloudFront invalidation.

## Structure

```
vasl-site/
  site/                   ← gotovasl.com (S3 + CloudFront)
    prototype.html        ← gotovasl.com/prototype.html
    demo.html             ← gotovasl.com/demo.html (VLAP live demo)
  prototype/              ← superseded by site/prototype.html; nothing serves it
```

## Deployment (site/ → AWS)

`site/` (gotovasl.com) deploys to **S3 + CloudFront**, not Netlify, via
`.github/workflows/deploy-site.yml` on every push to `main` that touches
`site/`. Infrastructure lives in
[`VASL-PLATFORM/infra/aws/static-sites`](https://github.com/VASL-HEALTH/VASL-PLATFORM/tree/main/infra/aws/static-sites).

The workflow authenticates with GitHub OIDC — there are no AWS keys in repo
secrets. It needs one repo variable, `MARKETING_DISTRIBUTION_ID`, set to the
`distribution_id` Terraform output.

`site/demo.html` (the VLAP live demo) is **fully self-contained**. The regex
engine is ported to JavaScript and embedded in the page, so Analyze runs in the
visitor's browser. There is no `fetch`, no API call, no backend dependency and
no ingress to wire — the page cannot 404 because it never leaves itself.

That is deliberate, and it is why this page ships. The earlier backend-calling
version posted to `https://api.gotovasl.com/api/vlap/demo/analyze`, which
returns 404: the phase1 ALB routes `/api/*` to `vasl-backend` and has no rule or
target group for vlap-service, whose ECS service has no load balancer attached.
Wiring public ingress to an inference service is a security-relevant change that
belongs in Terraform with explicit sign-off — not a prerequisite for a marketing
page. The self-contained build removes the need entirely.

**Do not repoint this page at a backend or at DeBERTa weights.** It runs the
**vlap-1.1.0-class regex engine**, deliberately not the trained checkpoint. The
EQ5 waiver covers training only and does not permit putting model weights in
front of members. This page is investor- and marketing-facing, illustrative,
and operates on text the visitor types into their own browser — no member data
reaches it, because nothing reaches it.

## Analytics

`site/` (gotovasl.com) uses [Plausible](https://plausible.io) for traffic
analytics. Plausible was chosen because it's cookieless and collects no
personal data, so it doesn't need a consent banner and doesn't put a youth
behavioral health site in the position of tracking individual visitors — a
posture that matters here more than it would for a typical marketing site,
and one that avoids an awkward conversation in any district or health plan
privacy review.

The script is added by `tools/seo_inject.py`, inside the same managed
`<!-- SEO:VASL -->` block as the rest of the head layer, so it ships on every
page consistently and can't be silently dropped by a hand-edit to one page.

**What is tracked:**
- Standard pageviews (URL, referrer, browser, device type, country — all
  aggregated, nothing tied to an individual visitor)
- Outbound link clicks (e.g. to the public RFPs and research cited on
  `site/school-mental-health-rfp.html` and
  `site/dialect-bias-mental-health-screening.html`)
- `Contact CTA` — fired when any link to `contact.html` is clicked, tagged
  with the page the click came from
- `Pricing CTA` — fired in addition to `Contact CTA` when that click happens
  on `pricing.html`, so pricing-page conversion can be tracked as its own goal
- `Demo Request` — fired on submission of the contact page's demo request
  form, tagged only with the organization type selected (school, health
  system, community organization, etc.)

**What is not tracked:** no cookies, no cross-site identifiers, no IP address
storage, and no personal or member data of any kind — not name, not email,
not organization name, not anything entered in the demo request form. The
`Demo Request` event carries a single non-identifying category value and
nothing else. Plausible has no visibility into anything that happens inside
the Vasl platform itself; this is marketing-site traffic analytics only.

If this is ever swapped for GA4, only one analytics tool should run at a
time — see `analytics_block()` in `tools/seo_inject.py`.
