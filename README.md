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
1. New site → Import from GitHub → `Vaslhealth/vasl-site`
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
