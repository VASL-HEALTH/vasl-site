# Vasl Health — Public Site

One deployment: `site/` → **gotovasl.com** on S3 + CloudFront.

| Page | Source | URL |
|------|--------|-----|
| Marketing site | `site/` | gotovasl.com |
| Platform prototype | `site/prototype.html` | gotovasl.com/prototype.html |
| VLAP live demo | not in this repo | https://vlap.gotovasl.com/ |
| Retired demo redirect | `site/demo.html` | gotovasl.com/demo.html |

Every page's footer links the live demo as **Signal Taxonomy**, pointing
straight at `https://vlap.gotovasl.com/`. The homepage outcomes chapter and
the `/vlap` hero link the same URL, in the same tab. The footer link is
generated from `FOOTER_COLS` in `tools/chrome_inject.py`, so repointing it
again is one edit and a re-run, not fifty hand-edits.

`site/demo.html` is no longer linked from anywhere. It stays live as a
noindex meta-refresh to `vlap-standalone.gotovasl.com` so the old URL still
resolves; retiring it is a separate decision.

> **`gotovasl.com/demo` (no extension) is broken and is not ours to fix here.**
> It 301s to `https://demo.gotovasl.com/`, which is NXDOMAIN. `/prototype`,
> `/about` and `/contact` all serve 200, so this is a stale per-path rule, not
> general extensionless routing. The rule lives in the CloudFront/S3 config
> under [`VASL-PLATFORM/infra/aws/static-sites`](https://github.com/VASL-HEALTH/VASL-PLATFORM/tree/main/infra/aws/static-sites),
> not in this repo — `site/netlify.toml` is inert since the move to CloudFront.
> **Use `gotovasl.com/demo.html`**, which is what the page's canonical and
> og:url now point at.

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

The site is deployed **by hand from committed `main`**. The push trigger was
removed from `.github/workflows/deploy-site.yml` on 2026-10-13, so pushing to
`main` ships nothing; both workflows in this repo are `workflow_dispatch` only.
Run the three cache-control passes yourself, then invalidate.

```bash
# 1. assets, long cache (everything but HTML, sitemap.xml, robots.txt)
aws s3 sync site/ s3://vasl-marketing-site/ --delete   --exclude '*.html' --exclude 'sitemap.xml' --exclude 'robots.txt'   --cache-control 'public,max-age=31536000,immutable' --no-progress

# 2. sitemap.xml + robots.txt, short cache. cp, not sync: sync skips a file
#    whose size and mtime look unchanged and would leave a stale header.
aws s3 cp site/sitemap.xml s3://vasl-marketing-site/sitemap.xml   --cache-control 'public,max-age=300' --no-progress
aws s3 cp site/robots.txt  s3://vasl-marketing-site/robots.txt   --cache-control 'public,max-age=300' --no-progress

# 3. HTML last, so a page is never live before the asset it needs
aws s3 sync site/ s3://vasl-marketing-site/ --delete   --exclude '*' --include '*.html'   --cache-control 'public,max-age=0,must-revalidate'   --content-type 'text/html; charset=utf-8' --no-progress

# 4. invalidate, then wait for Completed (see the Git Bash note below)
MSYS_NO_PATHCONV=1 aws cloudfront create-invalidation   --distribution-id E11DM7B5W2KRCQ   --paths '/' '/*.html' '/help/*' '/sitemap.xml' '/robots.txt'
```

Both `sync` passes carry `--delete`. **Add `--dryrun` and read the `delete:`
lines before running either one for real.** An object that is live but absent
from `site/` is deleted with nothing to restore it from, which is how
`tour.html` was nearly lost on 2026-11-03.

### Git Bash rewrites the invalidation paths

On Windows, MSYS argument conversion rewrites any argument beginning with `/`,
so `--paths '/' '/blog' '/sitemap.xml'` reaches CloudFront as
`C:/Program Files/Git/`, `C:/Program Files/Git/blog` and
`C:/Program Files/Git/sitemap.xml`. Single quotes do **not** prevent it. A path
containing a wildcard (`/*`, `/*.html`) is exempt and passes through intact.

Prefix the command with `MSYS_NO_PATHCONV=1`, or run it from PowerShell, and
check the returned `InvalidationBatch.Paths.Items` against what you intended.
The failure is usually loud (`InvalidArgument ... invalid invalidation paths`),
but a set of only extensionless paths can convert into something CloudFront
accepts, then invalidate the wrong keys while reporting `Completed`.

This is a *different* bug from the `--paths` globbing one commented in
`deploy-site.yml`: that one is bash expanding an unquoted `/*` against the
Actions runner's filesystem, and its fix does not cover the by-hand path.

### `site/tour.html` is byte-frozen

`site/tour.html` serves gotovasl.com/tour and `/tour.html`. **Never edit it in
this repo.** Its source is
[`VASL-PLATFORM/infra/aws/demo-site/content/portal-tour.html`](https://github.com/VASL-HEALTH/VASL-PLATFORM/blob/main/infra/aws/demo-site/content/portal-tour.html).
Change it there, then copy the bytes across so the two stay identical
(md5 `5728de78989dda2f93c687ee927f1021`, 22,206 bytes, verified with `cmp`).

Two guards keep it frozen and both must survive:

- **`.gitattributes` pins `site/tour.html -text`.** The blob is LF. This repo
  sets `core.autocrlf=true`, which converts LF to CRLF *on checkout*, so
  without the pin a Windows working copy of this file would be 22,537 bytes
  (22,206 + 331 line endings) and a deploy from that checkout would upload
  CRLF: same rendering, different `Content-Length`, and the repo copy would
  stop being the record of what S3 serves. With the pin, a checkout is
  byte-identical to the blob on every platform. The platform repo pins
  `content/*.html -text` for the same reason.

  Verified on 2026-11-03: `site/tour.html` is the only HTML file here whose
  working copy matches its blob. Every other page has an LF blob and a CRLF
  working copy, so HTML deployed from this laptop is CRLF while the same
  commit deployed from Linux would be LF. Harmless for rendering, but it means
  a deploy run from a different platform rewrites every HTML object's bytes.
- **`tour.html` is listed in `tools/seo_shared.IGNORE`.** Without it
  `seo_inject.py` injects a head layer, `gen_sitemap.py` lists a deliberately
  unlinked `noindex` page, and `seo_validate.py` fails it for a canonical and
  four `og:` tags it never had. Each of those changes the bytes. Note that
  `seo_validate.py` does **not** gate its canonical and `og:` checks on
  `noindex`, so the page's own `noindex, nofollow` is not enough to exempt it.

The page was hand-uploaded straight to S3 on 2026-11-03 02:34 UTC and existed
in no commit on any branch, so S3 held the only copy. It was committed in
`d4ab746` so `--delete` could go back on the HTML pass.

## Updating a Page

All pages are plain HTML — edit any `.html` file under `site/`, commit, push,
then run the deploy passes under **Deploying** above. Pushing alone ships
nothing. `site/tour.html` is the one file never to edit here.

## Structure

```
vasl-site/
  site/                   ← gotovasl.com (S3 + CloudFront)
    prototype.html        ← gotovasl.com/prototype.html
    demo.html             ← gotovasl.com/demo.html (VLAP live demo)
  prototype/              ← superseded by site/prototype.html; nothing serves it
```

## Deployment (site/ → AWS)

`site/` (gotovasl.com) deploys to **S3 + CloudFront**, not Netlify. Treat
`.github/workflows/deploy-site.yml` as the reference for the exact sync flags;
it no longer runs on push and is `workflow_dispatch` only, so deploys happen by
hand as described under **Deploying** above. Infrastructure lives in
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
