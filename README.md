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
