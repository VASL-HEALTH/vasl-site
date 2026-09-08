"""
Partner Package self-serve download — Lambda handler.

Request flow:
  1. Visitor fills the 3-field widget on contact.html (name, email, org).
  2. Browser POSTs JSON to this function's Lambda Function URL.
  3. This handler mints a short-lived presigned S3 GET URL for the
     confidential PDF (object stays private; nothing about it is ever
     public) and returns it to the browser for immediate download.
  4. The browser ALSO fires the existing mailto: flow (see contact.html)
     so the team gets the same lead notification as every other form
     submission -- no new email service, no SES setup required.

Why a presigned URL and not an email attachment: it needs zero email
infrastructure (no SES domain verification, no sandbox limits) and the
link expires (see PRESIGN_EXPIRY_SECONDS below), so a stale/forwarded
link stops working instead of becoming a permanent public copy.

Env vars (set in Terraform, see ../infra.tf):
  BUCKET       - private S3 bucket holding the PDF (not the public
                 marketing bucket -- see infra.tf comments)
  OBJECT_KEY   - key of the PDF within that bucket
  ALLOWED_ORIGIN - value for Access-Control-Allow-Origin (set to
                 https://gotovasl.com in prod; Function URL CORS config
                 in Terraform is the primary enforcement, this is a
                 defense-in-depth echo)
"""
import json
import os
import re
import time

import boto3

s3 = boto3.client("s3")

BUCKET = os.environ["BUCKET"]
OBJECT_KEY = os.environ["OBJECT_KEY"]
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "https://gotovasl.com")
PRESIGN_EXPIRY_SECONDS = 60 * 60 * 24  # 24 hours

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Simple in-Lambda rate limit is not possible statelessly; abuse control is
# handled by CloudWatch alarms on invocation count (see infra.tf) rather
# than in-function logic. A malicious actor can at most mint disposable
# 24-hour links to a single non-sensitive-beyond-its-own-content PDF --
# the blast radius of over-requesting this endpoint is low.


def _response(status, body_dict):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": ALLOWED_ORIGIN,
        },
        "body": json.dumps(body_dict),
    }


def handler(event, context):
    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        # Function URL CORS config (infra.tf) answers preflight directly,
        # this branch only fires if that's ever misconfigured.
        return _response(204, {})

    try:
        payload = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return _response(400, {"error": "Malformed request."})

    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    org = (payload.get("org") or "").strip()

    if not name or not org:
        return _response(400, {"error": "Name and organization are required."})
    if not EMAIL_RE.match(email):
        return _response(400, {"error": "A valid work email is required."})

    # Log the request to CloudWatch (free, already-on infra) so the team
    # has a durable record even if the mailto step is skipped or blocked
    # by the requester's browser/mail client config.
    print(json.dumps({
        "event": "partner_package_requested",
        "name": name,
        "email": email,
        "org": org,
        "ts": int(time.time()),
    }))

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": OBJECT_KEY},
        ExpiresIn=PRESIGN_EXPIRY_SECONDS,
    )

    return _response(200, {"url": url, "expires_in_seconds": PRESIGN_EXPIRY_SECONDS})
