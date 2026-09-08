# Partner Package instant download

Free, code-only alternative to a paid form backend for delivering the
confidential Partner Package PDF instantly when someone requests it on
contact.html.

## How it works

1. Visitor checks "The Partner Package" on the contact form and submits.
2. Browser fires the existing `mailto:` lead notification (unchanged —
   the team still gets every request in their inbox) **and** POSTs the
   requester's name/email/org to a Lambda Function URL.
3. The Lambda mints a 24-hour presigned S3 URL for the PDF (stored in a
   private, non-public bucket) and returns it. The page opens it
   automatically and also shows the link inline.
4. If the endpoint isn't deployed yet, or the request fails, the page
   falls back to "we'll email it to you" — nothing breaks, the mailto
   lead still went out.

No SES, no third-party form service, no recurring cost beyond
pennies-a-month AWS usage (realistically $0/mo in the free tier at this
volume).

## What's in this directory

- `lambda/handler.py` — the Lambda function (Python, boto3 only).
- `infra.tf` — Terraform for the private S3 bucket, IAM role, Lambda,
  and Function URL (CORS locked to `https://gotovasl.com`).
- `../../site/contact.html` — frontend changes are already live in the
  site (the checkbox, status box, and `requestPartnerPackageDownload()`
  JS). It no-ops safely until `PARTNER_PACKAGE_ENDPOINT` is filled in.

## Deployment — one manual step required

I (Claude) have push access to this repo but **no AWS credentials or
console access** — I can't run `terraform apply` myself. The site's own
GitHub Actions deploy role is intentionally scoped to S3-sync +
CloudFront-invalidate for the existing marketing bucket only (see
`.github/workflows/deploy-site.yml`'s header comment); it isn't and
shouldn't be widened to create Lambda/IAM/S3 resources.

So this feature ships as complete, ready-to-run code, but someone with
AWS access to the Vasl Health account needs to do this once:

```bash
cd tools/partner-package-download
terraform init
terraform apply

# Upload the PDF to the new private bucket (one time):
aws s3 cp /path/to/Vasl-Partner-Package-COMPLETE4.pdf \
  s3://$(terraform output -raw bucket_name)/partner-package.pdf

terraform output function_url
```

Then paste that Function URL into the `PARTNER_PACKAGE_ENDPOINT`
constant at the top of the `<script>` block in `site/contact.html` and
push to `main` — the existing deploy pipeline handles that HTML change
automatically, same as any other content edit.

Until that one apply happens, the site behaves exactly as it does
today (mailto-only) — nothing is broken by merging this.
