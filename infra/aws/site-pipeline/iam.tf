# Three roles and one gate.
#
# THE GATE IS THE LAST POLICY IN THIS FILE. CodePipeline has no "who may
# approve" field; the only thing standing between a built artifact and
# gotovasl.com is who holds `codepipeline:PutApprovalResult` on the approval
# action. Everything above it is plumbing.
#
# THE SPLIT BETWEEN BUILD AND DEPLOY IS THE POINT. The build role cannot write
# to the site bucket and has no CloudFront permission whatsoever. The deploy
# role can, and the only way to reach it is through the approval stage. If one
# role did both, the approval would be decoration.

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
  description        = "Publishes the approved artifact to the live site. Reachable only through the pipeline's Deploy stage, which is behind the manual approval."
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

# ------------------------------------------------------------------- THE GATE

# RODNEY, AND NOBODY ELSE, MAY APPROVE A SITE DEPLOY.
#
# Ruling, Rodney 2026-11-14: approvals on `main` are 0 and his approval sits
# on the deploy instead. This policy is that sentence as IAM. The principal is
# local.approver_arn -- arn:aws:iam::558215002439:user/rodney-admin.
#
# SCOPED TO THE ACTION, NOT THE PIPELINE. The resource names the stage and the
# action, so a future stage added to this pipeline does not inherit the right
# to be approved by anyone.
#
# ATTACHED TO HIS USER, NOT TO A GROUP. A group is a second place the
# membership can change without this file changing.
#
# WHAT THIS CANNOT DO: an account administrator can attach themselves a policy
# granting the same action. That is true of every IAM control. This closes the
# ordinary route, not the privileged one.
data "aws_iam_policy_document" "approve_site_deploy" {
  statement {
    sid     = "ApproveTheSiteDeploy"
    effect  = "Allow"
    actions = ["codepipeline:PutApprovalResult"]
    resources = [
      "arn:aws:codepipeline:${local.region}:${local.account}:${aws_codepipeline.site.name}/Approve/RodneyApprovesTheSite",
    ]
  }

  statement {
    sid    = "AndSeeWhatHeIsApproving"
    effect = "Allow"
    actions = [
      "codepipeline:GetPipeline",
      "codepipeline:GetPipelineState",
      "codepipeline:GetPipelineExecution",
      "codepipeline:ListPipelineExecutions",
      "codepipeline:ListActionExecutions",
    ]
    resources = [
      "arn:aws:codepipeline:${local.region}:${local.account}:${aws_codepipeline.site.name}",
    ]
  }
}

resource "aws_iam_policy" "approve_site_deploy" {
  name        = "vasl-approve-site-deploy"
  description = "The only principal holding this may approve a deploy of gotovasl.com."
  policy      = data.aws_iam_policy_document.approve_site_deploy.json
}

resource "aws_iam_user_policy_attachment" "rodney_approves" {
  # The user half of local.approver_arn. Written out rather than parsed from
  # the ARN so a reader does not have to evaluate a split() to learn who can
  # ship the site.
  user       = "rodney-admin"
  policy_arn = aws_iam_policy.approve_site_deploy.arn
}
