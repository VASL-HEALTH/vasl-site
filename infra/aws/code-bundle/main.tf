locals {
  bucket_name = "vasl-site-code-bundle-${data.aws_caller_identity.current.account_id}"
  bundle_key  = "main/repo.bundle"
}

# A BUCKET OF ITS OWN, NOT A PREFIX IN THE PLATFORM'S BUNDLE BUCKET.
# `vasl-code-bundle-558215002439` already exists [checked 2026-11-13,
# `aws s3api list-buckets`], and a `vasl-site/` prefix in it would have been
# fewer resources. Two reasons not to: that bucket is owned by
# VASL-PLATFORM's `code-bundle/terraform.tfstate` and carries
# prevent_destroy, so a second root writing into it means two states with
# opinions about one bucket's policy and lifecycle; and it is encrypted with
# `alias/vasl-development-app`, a CMK a third stack owns, which would make
# this repo's uploader depend on grants to a key nothing here manages. A
# separate bucket keeps this root readable on its own.
resource "aws_s3_bucket" "code_bundle" {
  bucket = local.bucket_name

  # The pipeline's only source. Losing it does not lose the code -- GitHub
  # has it -- but it does break every deploy until CI republishes, and a
  # bucket deleted by a `terraform destroy` run in the wrong directory is not
  # a failure mode worth leaving open.
  lifecycle {
    prevent_destroy = true
  }
}

# REQUIRED, NOT HYGIENE. A CodePipeline S3 source action triggers on a new
# OBJECT VERSION. Without versioning the pipeline has nothing to notice and
# every push leaves the deploy waiting for a manual start.
resource "aws_s3_bucket_versioning" "code_bundle" {
  bucket = aws_s3_bucket.code_bundle.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Versioning on plus nothing expiring old versions means every push to main
# keeps a bundle forever. This repo's bundle is small -- 4,304,119 bytes
# [measured 2026-11-13, `git bundle create` against origin/main;
# `git count-objects -vH` reports size-pack 4.18 MiB] -- so the bill is not
# the argument. The argument is that an unbounded version count is a thing
# nobody looks at until it is large, and the rule costs one resource.
#
# Three noncurrent versions for seven days is a rollback window: if a bad
# bundle lands, the previous one is still addressable by version id.
resource "aws_s3_bucket_lifecycle_configuration" "code_bundle" {
  bucket = aws_s3_bucket.code_bundle.id

  rule {
    id     = "expire-old-bundles"
    status = "Enabled"

    filter {}

    noncurrent_version_expiration {
      noncurrent_days           = 7
      newer_noncurrent_versions = 3
    }

    # An aborted upload leaves parts billable and invisible in a normal
    # listing, which is the classic way an S3 bill grows with nothing in the
    # bucket. Cheap insurance even at four megabytes.
    abort_incomplete_multipart_upload {
      days_after_initiation = 1
    }
  }
}

# SSE-S3 AND NOT THE SHARED CMK, which is where this departs from
# VASL-PLATFORM's bundle bucket. That repo's bundle is the source of systems
# that touch PHI, so its bundle sits under `alias/vasl-development-app`. This
# bundle is the source of a public marketing site: every byte in it is
# already served anonymously from gotovasl.com. A CMK would add a cross-stack
# key dependency, a kms:Decrypt grant on the uploader (which multipart
# UploadPart needs and which is easy to leave out), and a second grant on the
# pipeline role -- all to protect bytes that are public by design. AES256
# still encrypts at rest and needs no grants.
resource "aws_s3_bucket_server_side_encryption_configuration" "code_bundle" {
  bucket = aws_s3_bucket.code_bundle.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "code_bundle" {
  bucket                  = aws_s3_bucket.code_bundle.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_policy" "code_bundle" {
  bucket = aws_s3_bucket.code_bundle.id
  policy = data.aws_iam_policy_document.code_bundle_bucket.json

  # The policy below is a Deny with a `*` principal. Applied before the
  # public access block it would be evaluated against a bucket that still
  # permits public policies, so the ordering is stated rather than left to
  # Terraform's graph.
  depends_on = [aws_s3_bucket_public_access_block.code_bundle]
}

data "aws_iam_policy_document" "code_bundle_bucket" {
  statement {
    sid    = "DenyInsecureTransport"
    effect = "Deny"
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.code_bundle.arn,
      "${aws_s3_bucket.code_bundle.arn}/*",
    ]
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

# --- the uploader: GitHub Actions under OIDC -------------------------------
#
# A ROLE THAT CAN DO EXACTLY ONE THING. Every other role in this account
# carries permissions for a different job -- Amplify deploys, ECS deploys,
# RunInstances with PassRole. Hanging a bucket write on one of them would
# widen a role that already does something more dangerous. This one can put
# one object at one key and nothing else, which is the only reason a GitHub
# runner is allowed to hold it at all.
resource "aws_iam_role" "bundle_upload" {
  name                 = "vasl-site-code-bundle-github"
  description          = "GitHub Actions OIDC role. Writes the repo bundle to S3 on push to main. One action, one key. Cannot deploy."
  assume_role_policy   = data.aws_iam_policy_document.bundle_upload_trust.json
  max_session_duration = 3600
}

data "aws_iam_policy_document" "bundle_upload_trust" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [data.aws_iam_openid_connect_provider.github.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # BRANCH FORM, NOT ENVIRONMENT FORM, and the tradeoff is worth stating.
    #
    # The job runs automatically on every push to main, so it cannot sit
    # behind a GitHub Environment approval -- and a GitHub Environment is
    # itself forbidden by the DEPLOY RULE at the top of CLAUDE.md. The cost
    # of the branch form is that any workflow running on main can assume this
    # role, including one a later PR adds without touching this file.
    #
    # What makes that acceptable: the role can PutObject one key. The worst
    # case is a bad bundle overwriting a good one, which versioning above
    # makes recoverable, and which already requires getting a workflow past
    # main's required checks. It cannot reach the site bucket, the
    # distribution, or the pipeline.
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:${var.github_repo}:ref:refs/heads/main"]
    }
  }
}

resource "aws_iam_role_policy" "bundle_upload" {
  name   = "write-the-bundle"
  role   = aws_iam_role.bundle_upload.id
  policy = data.aws_iam_policy_document.bundle_upload.json
}

data "aws_iam_policy_document" "bundle_upload" {
  # PutObject only, on the one key.
  #
  # No GetObject: CI has the repo already and never needs to read back what
  # is in the bucket. No DeleteObject: nothing in this path should be able to
  # remove a bundle, and the lifecycle rule handles expiry. No ListBucket:
  # the writer knows its own key.
  #
  # This is also the whole reason the workflow is exempt from the no-deploy
  # check by name. A credential that can only write one private object is not
  # a deploy credential: what it would need to deploy -- s3:PutObject on
  # vasl-marketing-site, or cloudfront:CreateInvalidation -- is absent here
  # and exists only on the pipeline's own roles in ../site-pipeline.
  statement {
    sid       = "WriteTheBundleOnly"
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.code_bundle.arn}/${local.bundle_key}"]
  }
}
