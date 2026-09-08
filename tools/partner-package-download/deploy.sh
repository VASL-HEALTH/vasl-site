#!/usr/bin/env bash
# One-shot deploy for the Partner Package instant-download feature.
#
# Requires: AWS credentials with permission to create S3/IAM/Lambda
# resources, terraform, and the awscli — all run from your machine,
# not by Claude (no AWS access here, see README.md).
#
# Usage:
#   ./deploy.sh /path/to/Vasl-Partner-Package-COMPLETE4.pdf
#
# What it does:
#   1. terraform init + apply (private S3 bucket, IAM role, Lambda,
#      Function URL)
#   2. Uploads the PDF to the new private bucket
#   3. Patches PARTNER_PACKAGE_ENDPOINT in ../../site/contact.html with
#      the live Function URL
#   4. Prints the git commands to commit + push that one-line change
#      (deploy is on you to review — this script does not push)

set -euo pipefail

PDF_PATH="${1:-}"
if [[ -z "$PDF_PATH" || ! -f "$PDF_PATH" ]]; then
  echo "Usage: ./deploy.sh /path/to/Vasl-Partner-Package-COMPLETE4.pdf" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTACT_HTML="$SCRIPT_DIR/../../site/contact.html"

cd "$SCRIPT_DIR"

echo "==> terraform init"
terraform init -input=false

echo "==> terraform apply"
terraform apply -auto-approve

BUCKET="$(terraform output -raw bucket_name)"
FUNCTION_URL="$(terraform output -raw function_url)"

echo "==> Uploading PDF to s3://$BUCKET/partner-package.pdf"
aws s3 cp "$PDF_PATH" "s3://$BUCKET/partner-package.pdf"

echo "==> Patching PARTNER_PACKAGE_ENDPOINT in contact.html"
if [[ ! -f "$CONTACT_HTML" ]]; then
  echo "Could not find $CONTACT_HTML — patch it manually with:" >&2
  echo "  const PARTNER_PACKAGE_ENDPOINT = '$FUNCTION_URL';" >&2
  exit 1
fi

# macOS/BSD sed and GNU sed have different -i syntax; this handles both.
if sed --version >/dev/null 2>&1; then
  sed -i "s|const PARTNER_PACKAGE_ENDPOINT = '.*';|const PARTNER_PACKAGE_ENDPOINT = '${FUNCTION_URL}';|" "$CONTACT_HTML"
else
  sed -i '' "s|const PARTNER_PACKAGE_ENDPOINT = '.*';|const PARTNER_PACKAGE_ENDPOINT = '${FUNCTION_URL}';|" "$CONTACT_HTML"
fi

echo ""
echo "Done. Function URL: $FUNCTION_URL"
echo ""
echo "Review the diff, then ship it:"
echo "  git -C \"$SCRIPT_DIR/../..\" diff site/contact.html"
echo "  git -C \"$SCRIPT_DIR/../..\" add site/contact.html"
echo "  git -C \"$SCRIPT_DIR/../..\" commit -m 'Wire up Partner Package instant download endpoint'"
echo "  git -C \"$SCRIPT_DIR/../..\" push origin main"
