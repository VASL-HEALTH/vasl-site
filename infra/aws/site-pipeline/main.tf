# The gotovasl.com deploy pipeline. Builds from `main`, runs inside AWS, and
# cannot reach the live site until Rodney approves it.
#
#   Source (S3: main's bundle) -> Build (CodeBuild) -> Approve -> Deploy (S3 + CloudFront)
#
# ============================================================================
# WHAT THE REAL DEPLOY TARGET IS, AND HOW THAT WAS ESTABLISHED
# ============================================================================
#
# The deploy this replaces was `.github/workflows/deploy-site.yml`, deleted
# from `main` in 2e1b40f ("Remove every GitHub-side deploy path"). Read back
# out of git (`git show 2e1b40f^:.github/workflows/deploy-site.yml`), it did
# exactly four things:
#
#   1. `aws s3 sync site/ s3://vasl-marketing-site/` in three passes, because
#      Cache-Control differs by asset class;
#   2. `aws cloudfront create-invalidation` against the distribution in the
#      repo variable MARKETING_DISTRIBUTION_ID;
#   3. waited for the invalidation to complete;
#   4. smoke-tested seven paths against the distribution domain.
#
# Each of those was checked against the live account on 2026-11-13 under
# user/rodney-admin, read-only:
#
#   * `vasl-marketing-site` exists in us-east-1 [`aws s3api
#     get-bucket-location`], is AES256-encrypted with no CMK
#     [`get-bucket-encryption`], and its bucket policy allows only the
#     CloudFront OAC to read plus a DenyInsecureTransport -- no statement
#     denies a same-account IAM principal, so an identity policy is enough to
#     write to it [`get-bucket-policy`].
#   * Distribution E11DM7B5W2KRCQ is Deployed, carries the aliases
#     `gotovasl.com` and `www.gotovasl.com`, has `s3-vasl-marketing-site` as
#     its default origin behind OAC E2QCFYRBWNPYQQ, routes `/.well-known/*`
#     to a different bucket, uses the CachingOptimized cache policy
#     (658327ea-f89d-4fab-a63d-7e88639e58f6), rewrites pretty URLs in a
#     viewer-request CloudFront Function (`vasl-marketing-viewer-request`),
#     and maps 403/404 to /404.html with a 404
#     [`aws cloudfront get-distribution`, `get-distribution-config`].
#
# So: S3 bucket plus CloudFront invalidation. Not Amplify, not a bare bucket
# website, not an ECS service. The distribution id is a LITERAL here and not a
# variable, because the repo variable the old workflow read from
# (MARKETING_DISTRIBUTION_ID) does not exist -- `gh api
# repos/VASL-HEALTH/vasl-site/actions/variables` returns total_count 0, so
# that workflow would have failed its own fail-fast step if anybody had run
# it.
#
# ============================================================================
# WHY THE SOURCE IS S3 AND NOT GITHUB
# ============================================================================
#
# Standing ruling: "Git never deploys; S3 does." A CodePipeline GitHub source
# needs a CodeConnections connection, and a new connection sits in PENDING
# until somebody completes an OAuth handshake in a browser -- which no
# unattended path can do.
#
# The repo already publishes itself to S3 on every push to `main`:
# `.github/workflows/code-bundle.yml` writes `git bundle create repo.bundle
# main` to s3://vasl-site-code-bundle-558215002439/main/repo.bundle. This
# pipeline sources that object. Same commits, no connection, no browser.
#
# The bundle bucket has versioning enabled by ../code-bundle, which an S3
# source action requires: the pipeline triggers on a new object version.
#
# A BUNDLE IS NOT A TARBALL, and the build cares. CodeBuild clones it
# (`git clone -b main repo.bundle`), so the build has real history: the commit
# is readable, and `tools/gen_sitemap.py` reads `git log` for <lastmod>.
#
# ============================================================================
# WHAT THIS DOES NOT DO
# ============================================================================
#
# IT IS NOT APPLIED, and no AWS resource was created while writing it. IAM
# roots are applied by hand under `rodney-admin`, never from a session or from
# CI. This directory is the code record; README.md carries the plan and apply
# commands and the expected resource count.
#
# IT DOES NOT MANAGE `vasl-marketing-site` OR THE DISTRIBUTION. Both belong to
# VASL-PLATFORM's `static-sites` state. This root only grants itself narrow
# access to them, so two states never hold opinions about one bucket.
#
# IT DEPLOYS `site/` ONLY. `prototype/` is a separate thing in this repo and
# was already out of scope in the workflow this replaces.

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # REMOTE STATE, which is where this departs from VASL-PLATFORM's
  # production-pipeline root -- that one keeps state locally. State for a root
  # that creates IAM roles and a deploy pipeline should not live on one
  # laptop: it is not shared, it is not versioned, and it is not backed up.
  # Both the bucket and the lock table already exist [checked 2026-11-13,
  # `aws s3 ls s3://vasl-terraform-state/` and `aws dynamodb list-tables`].
  backend "s3" {
    bucket         = "vasl-terraform-state"
    key            = "vasl-site/site-pipeline/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "vasl-terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = "us-east-1"

  default_tags {
    tags = {
      Project   = "vasl-site"
      ManagedBy = "terraform"
      Stack     = "site-pipeline"
    }
  }
}

data "aws_caller_identity" "current" {}

locals {
  account = "558215002439"
  region  = "us-east-1"

  #: Where CI publishes `main` as a git bundle, per push. Written by
  #: ../code-bundle; read here.
  source_bucket = "vasl-site-code-bundle-558215002439"
  source_key    = "main/repo.bundle"

  #: THE LIVE SITE. Named explicitly and never defaulted: a deploy target that
  #: falls back to something is a deploy target that eventually publishes to
  #: the wrong place.
  site_bucket     = "vasl-marketing-site"
  distribution_id = "E11DM7B5W2KRCQ"

  #: The ONLY principal that may approve a site deploy. Ruling,
  #: Rodney 2026-11-14: his approval sits on the deploy, not on the merge.
  approver_arn = "arn:aws:iam::558215002439:user/rodney-admin"
}
