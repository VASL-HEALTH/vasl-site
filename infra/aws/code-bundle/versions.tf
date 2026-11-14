# Vasl Health, PBC -- this repo as a git bundle in S3, for the AWS-side
# site pipeline.
#
# WHY THIS EXISTS. The site's deploy moved out of GitHub Actions and into
# CodePipeline, and a pipeline has to read the source from somewhere inside
# AWS. A CodePipeline GitHub source needs a CodeConnections connection, which
# sits in PENDING until a human finishes an OAuth handshake in a browser; an
# S3 source needs nothing but an object. Standing ruling: git never deploys,
# S3 does. So CI publishes `main` to S3 on every push and the pipeline reads
# that object.
#
# THIS ROOT IS SOURCE BACKUP, NOT A DEPLOY. Nothing here can reach
# gotovasl.com. The bucket is private, no distribution has it as an origin,
# and the only write permission that exists is PutObject on a single key. The
# deploy lives in ../site-pipeline, behind a manual approval.
#
# A BUNDLE AND NOT A TARBALL, deliberately. `git clone` from a bundle gives
# the build a real repository -- a resolvable HEAD, branches, and a commit SHA
# it can stamp onto what it publishes. A tarball gives a directory of files
# that cannot answer "which commit is live?", which is the question that
# matters when somebody asks what is on gotovasl.com.
#
# NOT APPLIED. IAM roots are applied by hand under `rodney-admin`, never from
# a session or from CI. Plan and apply:
#
#   cd infra/aws/code-bundle
#   AWS_PROFILE=rodney-admin terraform init
#   AWS_PROFILE=rodney-admin terraform plan -out code-bundle.tfplan
#   AWS_PROFILE=rodney-admin terraform apply code-bundle.tfplan
#
# Expected plan: 8 to add, 0 to change, 0 to destroy. The 8: the bucket and
# its five settings (versioning, lifecycle, encryption, public access block,
# policy), the upload role, and the role's one inline policy.

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # The shared state bucket and lock table, both of which already exist
  # [checked 2026-11-13: `aws s3 ls s3://vasl-terraform-state/` lists 18
  # prefixes, `aws dynamodb list-tables` lists vasl-terraform-locks]. The key
  # is namespaced by repo because VASL-PLATFORM already holds
  # `code-bundle/terraform.tfstate` for its own bundle.
  backend "s3" {
    bucket         = "vasl-terraform-state"
    key            = "vasl-site/code-bundle/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "vasl-terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = "vasl-site"
      ManagedBy = "terraform"
      Stack     = "code-bundle"
    }
  }
}

data "aws_caller_identity" "current" {}

# The provider already exists and is shared
# [checked 2026-11-13, `aws iam list-open-id-connect-providers` lists
# token.actions.githubusercontent.com]. Read, never created here: a shared
# trust anchor must not sit behind one stack's destroy.
data "aws_iam_openid_connect_provider" "github" {
  url = "https://token.actions.githubusercontent.com"
}
