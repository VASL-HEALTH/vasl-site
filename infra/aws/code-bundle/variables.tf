variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "github_repo" {
  description = "owner/repo allowed to assume the upload role, pinned to refs/heads/main."
  type        = string
  default     = "VASL-HEALTH/vasl-site"
}

# IMMUTABLE-ID SUBJECT FORM, AND IT IS NOT OPTIONAL HERE.
#
# This repo has GitHub's immutable subject claim turned on:
#
#   GET repos/VASL-HEALTH/vasl-site/actions/oidc/customization/sub
#   {"sub_claim_prefix":"repo:VASL-HEALTH@291104715/vasl-site@1249759898",
#    "use_default":true,"use_immutable_subject":true}
#
# So the token's `sub` is `repo:VASL-HEALTH@291104715/vasl-site@1249759898:
# ref:refs/heads/main` -- the owner and repo names each carry their numeric
# id. A trust policy written as `repo:VASL-HEALTH/vasl-site:ref:...` never
# matches, and STS answers "Not authorized to perform
# sts:AssumeRoleWithWebIdentity" with no hint as to which claim failed
# [measured 2026-11-14: runs 43547821488, 43548080887, 43555291587 and
# 43631781619 all died there]. The account's other working GitHub OIDC role,
# `github-actions-fordham-ellucian-s3-sync`, carries the same `@<id>` form.
#
# The ids are immutable -- that is the point of the setting. Renaming the org
# or the repo does NOT break this, which is the opposite of the name form.
# Do not "simplify" this back to owner/repo.
variable "github_sub_prefix" {
  description = "Immutable-id subject prefix for this repo's OIDC tokens. From repos/:owner/:repo/actions/oidc/customization/sub."
  type        = string
  default     = "repo:VASL-HEALTH@291104715/vasl-site@1249759898"
}
