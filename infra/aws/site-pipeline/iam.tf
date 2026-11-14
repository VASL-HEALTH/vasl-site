# Three roles, and a gate that has moved.
#
# THE APPROVAL STAGE IS GONE. Ruling, Rodney 2026-11-14: the marketing site
# auto-deploys, so a merge to `main` publishes gotovasl.com with no human stop.
# What now stands between a built artifact and the live site is the set of
# blocking checks in buildspec.yml, which fail the Build stage and leave Deploy
# unreachable.
#
# THE SPLIT BETWEEN BUILD AND DEPLOY STILL MATTERS, AND MORE THAN BEFORE. The
# build role cannot write to the site bucket and has no CloudFront permission
# whatsoever; only the deploy role can publish, and only the Deploy stage can
# start it. That separation used to be what made the approval meaningful. It is
# now what stops a compromised build step from publishing directly and skipping
# the Deploy stage's buildspec -- the checks, the cache headers, the --delete
# and the invalidation -- altogether. Do not collapse these two roles.

# ------------------------------------------------------------------ pipeline

data "aws_iam_policy_document" "pipeline_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["codepipeline.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "pipeline" {
  name               = "vasl-site-pipeline"
  assume_role_policy = data.aws_iam_policy_document.pipeline_assume.json
}

data "aws_iam_policy_document" "pipeline" {
  # ONE KEY IN ONE BUCKET. GetBucketVersioning is on the bucket because an S3
  # source action checks versioning before it will poll; the object grants are
  # on the single key, so this role cannot read anything else CI ever puts in
  # that bucket.
  statement {
    sid    = "ReadMainsBundleOnly"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:GetBucketVersioning",
    ]
    resources = [
      "arn:aws:s3:::${local.source_bucket}",
      "arn:aws:s3:::${local.source_bucket}/${local.source_key}",
    ]
  }

  statement {
    sid    = "ArtifactStore"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:PutObject",
      "s3:GetBucketLocation",
    ]
    resources = [
      aws_s3_bucket.artifacts.arn,
      "${aws_s3_bucket.artifacts.arn}/*",
    ]
  }

  # The two projects by ARN. A `*` here would let this pipeline start any
  # CodeBuild project in the account, including one with wider permissions
  # than either of these -- which is a deploy path that no diff of this file
  # would show.
  statement {
    sid     = "StartTheseTwoBuildsOnly"
    effect  = "Allow"
    actions = ["codebuild:StartBuild", "codebuild:BatchGetBuilds"]
    resources = [
      aws_codebuild_project.site_build.arn,
      aws_codebuild_project.site_deploy.arn,
    ]
  }

  # NOTHING ELSE. In particular this role holds no s3:PutObject on
  # vasl-marketing-site and no cloudfront:* -- the deploy happens inside the
  # deploy project under its own role, which is reachable only after the
  # approval stage.
}

resource "aws_iam_role_policy" "pipeline" {
  name   = "vasl-site-pipeline"
  role   = aws_iam_role.pipeline.id
  policy = data.aws_iam_policy_document.pipeline.json
}

# ----------------------------------------------------------- build (no deploy)

data "aws_iam_policy_document" "codebuild_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["codebuild.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "codebuild" {
  name               = "vasl-site-build"
  assume_role_policy = data.aws_iam_policy_document.codebuild_assume.json
}

data "aws_iam_policy_document" "codebuild" {
  statement {
    sid    = "Logs"
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = [
      "arn:aws:logs:${local.region}:${local.account}:log-group:/aws/codebuild/vasl-site-build",
      "arn:aws:logs:${local.region}:${local.account}:log-group:/aws/codebuild/vasl-site-build:*",
    ]
  }

  statement {
    sid    = "Artifacts"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:PutObject",
    ]
    resources = ["${aws_s3_bucket.artifacts.arn}/*"]
  }

  # That is the entire build role: logs and the artifact store. No grant on
  # vasl-marketing-site, no cloudfront:CreateInvalidation, no ECR, no
  # PassRole. The build can produce a deployable artifact and cannot publish
  # it.
}

resource "aws_iam_role_policy" "codebuild" {
  name   = "vasl-site-build"
  role   = aws_iam_role.codebuild.id
  policy = data.aws_iam_policy_document.codebuild.json
}

# ------------------------------------------- deploy (only reachable past the gate)

resource "aws_iam_role" "deploy" {
  name               = "vasl-site-deploy"
  description        = "Publishes the built artifact to the live site. Reachable only through the pipeline's Deploy stage, which runs only after Build succeeds."
  assume_role_policy = data.aws_iam_policy_document.codebuild_assume.json
}

data "aws_iam_policy_document" "deploy" {
  statement {
    sid    = "Logs"
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = [
      "arn:aws:logs:${local.region}:${local.account}:log-group:/aws/codebuild/vasl-site-deploy",
      "arn:aws:logs:${local.region}:${local.account}:log-group:/aws/codebuild/vasl-site-deploy:*",
    ]
  }

  statement {
    sid       = "ReadTheApprovedArtifact"
    effect    = "Allow"
    actions   = ["s3:GetObject", "s3:GetObjectVersion"]
    resources = ["${aws_s3_bucket.artifacts.arn}/*"]
  }

  # THE ONE SITE BUCKET, NAMED. `aws s3 sync --delete` needs ListBucket on the
  # bucket and Put/Delete on the objects; nothing needs GetObject, because
  # sync compares the listing and not the bytes. A PutObject whose resource is
  # `*` would let this role publish to any bucket in the account, which is
  # exactly the kind of grant this pipeline exists to replace.
  #
  # DeleteObject is required and deliberate: without it a page removed from
  # the repo stays live forever, and the old workflow's `--delete` was the
  # thing keeping the bucket equal to `site/`.
  statement {
    sid    = "PublishTheSite"
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:DeleteObject",
    ]
    resources = ["arn:aws:s3:::${local.site_bucket}/*"]
  }

  statement {
    sid       = "ListTheSiteBucketForSync"
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::${local.site_bucket}"]
  }

  # ONE DISTRIBUTION. CreateInvalidation to publish, Get* to wait for it and
  # to resolve the domain name the smoke test hits -- which is the
  # distribution domain rather than gotovasl.com so the test means something
  # even if DNS is pointed elsewhere.
  #
  # ListInvalidations is absent: the deploy knows the id of the invalidation
  # it created.
  statement {
    sid    = "InvalidateThatOneDistribution"
    effect = "Allow"
    actions = [
      "cloudfront:CreateInvalidation",
      "cloudfront:GetInvalidation",
      "cloudfront:GetDistribution",
    ]
    resources = ["arn:aws:cloudfront::${local.account}:distribution/${local.distribution_id}"]
  }
}

resource "aws_iam_role_policy" "deploy" {
  name   = "vasl-site-deploy"
  role   = aws_iam_role.deploy.id
  policy = data.aws_iam_policy_document.deploy.json
}

# ------------------------------------------- WHAT USED TO BE THE GATE, REMOVED

# THE APPROVAL POLICY IS GONE, not merely unused.
#
# `vasl-approve-site-deploy` granted `codepipeline:PutApprovalResult` on
# `<pipeline>/Approve/RodneyApprovesTheSite` and was attached to rodney-admin.
# With the Approve stage removed there is no action to approve, so the grant
# permitted an operation that could not be performed. It is deleted along with
# its user attachment rather than left inert: dead IAM is how somebody later
# mistakes a corpse for a live control, and a policy named "approve site
# deploy" is an unusually convincing corpse.
#
# Keeping it would also have cost something concrete. Its document interpolated
# `aws_codepipeline.site.name`, so Terraform deferred the data source and
# planned the policy as `policy -> (known after apply)` -- a second change whose
# content the plan could not show, on the one apply where every line should be
# readable in advance.
#
# THE GATE DID NOT GO WITH IT. It is buildspec.yml's blocking checks plus the
# build/deploy role split above.
