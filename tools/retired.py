"""
Pages retired in the November 2026 rebuild, and where each one now sends a
visitor. One table, read by three places:

  * tools/retire_pages.py writes each file as a noindex stub that refreshes
    to the target, so an old link still lands somewhere even before the
    CloudFront function is updated;
  * tools/seo_shared.py adds every key to IGNORE, so the SEO generators and
    validators leave the stubs alone and the sitemap never lists them;
  * infra/aws/site-pipeline/viewer-request.js carries the same map as 301s.
    Keep the two in step: tools/retire_pages.py --check fails if they differ.
"""

RETIRED = {
    # Design's list
    "for-schools.html": "/",
    "for-organizations.html": "/",
    "for-families.html": "/",
    "school-mental-health-rfp.html": "/",
    "platform.html": "/",
    # The rest of the pre-November site, each to its nearest new page
    "peer-groups.html": "/",
    "ai-model.html": "/vlap",
    "glossary.html": "/vlap",
    "teletherapy.html": "/vlap",
    "outcomes.html": "/research",
    "clinical-outcomes.html": "/research",
    "dialect-bias-mental-health-screening.html": "/research",
    "hedis-behavioral-health-cultural-fit.html": "/bridge",
    "infrastructure.html": "/technology",
    "careers.html": "/team",
    "support.html": "/contact",
    "help/assessments.html": "/technology",
    "help/billing.html": "/technology",
    "help/clinical.html": "/technology",
    "help/compliance.html": "/technology",
    "help/getting-started.html": "/technology",
    "help/technical.html": "/technology",
    "help/vlap-technology.html": "/vlap",
}
