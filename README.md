# Vasl Health — Public Sites

Three Netlify deployments from this single repo.

| Site | Directory | Domain |
|------|-----------|--------|
| Main marketing site | `site/` | gotovasl.com |
| Platform prototype | `prototype/` | prototype.gotovasl.com |
| VLAP demo | `demo/` | demo.gotovasl.com |

## Deploying

Each subdirectory deploys independently on Netlify.
Push to `main` → Netlify auto-deploys all three sites.

### Netlify Setup (one-time per site)
1. New site → Import from GitHub → `VASL-HEALTH/vasl-site`
2. Set **Base directory** to `site/`, `prototype/`, or `demo/`
3. Set **Publish directory** same as base directory
4. Leave build command empty (static HTML — no build needed)
5. Assign custom domain

## Updating a Page

All pages are plain HTML — edit any `.html` file and push.
Changes go live in ~30 seconds via Netlify's CDN.

## Structure

```
vasl-site/
  site/          ← gotovasl.com (30 HTML pages)
  prototype/     ← prototype.gotovasl.com (single HTML file)
  demo/          ← demo.gotovasl.com (single HTML file)
```

## Deployment (site/ → AWS)

`site/` (gotovasl.com) deploys to **S3 + CloudFront**, not Netlify, via
`.github/workflows/deploy-site.yml` on every push to `main` that touches
`site/`. Infrastructure lives in
[`VASL-PLATFORM/infra/aws/static-sites`](https://github.com/VASL-HEALTH/VASL-PLATFORM/tree/main/infra/aws/static-sites).

The workflow authenticates with GitHub OIDC — there are no AWS keys in repo
secrets. It needs one repo variable, `MARKETING_DISTRIBUTION_ID`, set to the
`distribution_id` Terraform output.

`prototype/` and `vlap-live-demo/` are still Netlify sites and are unaffected.

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
