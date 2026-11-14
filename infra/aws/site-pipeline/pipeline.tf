# Source (S3, main's bundle) -> Build (CodeBuild) -> Approve (Rodney) -> Deploy (S3 + CloudFront)
#
# THE APPROVAL IS A SEPARATE STAGE, NOT AN OPTION ON THE DEPLOY. A manual
# approval action in its own stage cannot be skipped by a pipeline execution:
# the deploy stage has no other way to be reached. An approval attached to the
# deploy stage could be reordered by a later edit without the diff looking
# like it removed a gate.
#
# WHO MAY APPROVE IS AN IAM QUESTION, NOT A PIPELINE SETTING. CodePipeline has
# no "approver" field -- the gate is `codepipeline:PutApprovalResult`, and
# iam.tf grants it to exactly one principal on exactly this action. Anyone
# else with console access sees the button and gets AccessDenied.

resource "aws_s3_bucket" "artifacts" {
  bucket = "vasl-site-pipeline-artifacts-${local.account}"
}

resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket                  = aws_s3_bucket.artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# CodePipeline requires a versioned artifact store.
resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Pipeline artifacts are disposable: every execution writes a fresh one and
# nothing reads an old one. Versioning is on because CodePipeline demands it,
# which means without this rule the bucket keeps a copy of the whole site for
# every deploy that ever ran, forever.
resource "aws_s3_bucket_lifecycle_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id

  rule {
    id     = "expire-pipeline-artifacts"
    status = "Enabled"

    filter {}

    # Thirty days is long enough to read back what a past execution built
    # while investigating something, and short enough that the bucket does not
    # become an accidental archive.
    expiration {
      days = 30
    }

    noncurrent_version_expiration {
      noncurrent_days = 7
    }

    abort_incomplete_multipart_upload {
      days_after_initiation = 1
    }
  }
}

# --------------------------------------------------------------- build stage

# BUILDS, DOES NOT DEPLOY. It has no write permission on vasl-marketing-site
# and no CloudFront permission at all -- see iam.tf. A build that could also
# deploy would make the approval optional, which is the whole thing this
# pipeline exists to prevent.
resource "aws_codebuild_project" "site_build" {
  name         = "vasl-site-build"
  description  = "Clones main's bundle, checks the generated SEO layer, emits site/ as the deploy artifact. Cannot deploy."
  service_role = aws_iam_role.codebuild.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/amazonlinux2-x86_64-standard:5.0"
    type         = "LINUX_CONTAINER"
    # No privileged_mode: nothing here builds a container image. A static
    # site build does not need docker, and privileged_mode on a project that
    # does not need it is a larger blast radius for free.
  }

  source {
    type = "CODEPIPELINE"
    # In the repository so the build is reviewed like any other change, not
    # typed into a console field where a diff can never show it.
    #
    # PASSED AS CONTENTS, NOT AS A PATH, and it has to be. A CodeBuild action
    # resolves a buildspec path inside its INPUT ARTIFACT, and this project's
    # input artifact is the Source stage's output: the single object
    # `main/repo.bundle`. There is no `infra/` directory in it to find, so the
    # path form fails in DOWNLOAD_SOURCE, before any command runs, with
    # `YAML_FILE_ERROR: stat .../src/infra/aws/site-pipeline/buildspec.yml: no
    # such file or directory` [measured 2026-11-14, build
    # vasl-site-build:d61622ea-b7c5-49ff-9873-d807aff954d8].
    #
    # `file()` inlines it, which is also the only form consistent with what
    # buildspec.yml does: its first commands are `git bundle verify
    # repo.bundle` and `git clone -b main repo.bundle src`, i.e. it expects the
    # bundle at the artifact root and creates the working tree itself.
    #
    # The deploy project below is the opposite case and is correct as a path:
    # its input artifact is this build's OUTPUT, which contains
    # buildspec-deploy.yml at its root, so the deploy script that runs is the
    # one from the commit that was approved.
    buildspec = file("${path.module}/buildspec.yml")
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "/aws/codebuild/vasl-site-build"
      stream_name = "build"
    }
  }
}

# -------------------------------------------------------------- deploy stage

# WHY THE DEPLOY IS A CODEBUILD ACTION AND NOT CODEPIPELINE'S S3 DEPLOY
# PROVIDER. The S3 deploy provider can extract an artifact into a bucket and
# set ONE Cache-Control value for everything it writes. The site needs three,
# and the difference is not cosmetic:
#
#   * fingerprinted assets: public,max-age=31536000,immutable
#   * sitemap.xml and robots.txt: public,max-age=300
#   * HTML: public,max-age=0,must-revalidate
#
# which is what Netlify served on gotovasl.com (verified against the live
# response 2026-08-08, per the workflow this replaces) and what CloudFront's
# CachingOptimized policy honors from the origin. The S3 provider also cannot
# delete removed files and cannot invalidate CloudFront, so a page deleted
# from the repo would stay live and a changed asset would serve stale for a
# year. A CodeBuild action can do all three passes, the invalidation and a
# smoke test, and it still runs inside AWS after the approval.
resource "aws_codebuild_project" "site_deploy" {
  name         = "vasl-site-deploy"
  description  = "Publishes the approved artifact to s3://vasl-marketing-site, invalidates CloudFront, smoke-tests the result."
  service_role = aws_iam_role.deploy.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/amazonlinux2-x86_64-standard:5.0"
    type         = "LINUX_CONTAINER"

    environment_variable {
      name  = "SITE_BUCKET"
      value = local.site_bucket
    }
    environment_variable {
      name  = "DISTRIBUTION_ID"
      value = local.distribution_id
    }
  }

  source {
    type = "CODEPIPELINE"
    # AT THE ROOT OF THE ARTIFACT, NOT THE REPO PATH. This project's input is
    # the BUILD's output artifact, and a CodeBuild action reads its buildspec
    # from its input artifact -- where `infra/aws/site-pipeline/` does not
    # exist. The build copies this file to the artifact root for exactly that
    # reason, which also means the deploy script that runs is the one from the
    # commit that was approved.
    buildspec = "buildspec-deploy.yml"
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "/aws/codebuild/vasl-site-deploy"
      stream_name = "deploy"
    }
  }
}

# ------------------------------------------------------------------ pipeline

resource "aws_codepipeline" "site" {
  name     = "vasl-site"
  role_arn = aws_iam_role.pipeline.arn

  artifact_store {
    location = aws_s3_bucket.artifacts.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "MainBundle"
      category         = "Source"
      owner            = "AWS"
      provider         = "S3"
      version          = "1"
      output_artifacts = ["src"]

      configuration = {
        S3Bucket    = local.source_bucket
        S3ObjectKey = local.source_key
        # The pipeline starts itself on a new object version, which CI writes
        # on every push to main.
        PollForSourceChanges = "true"
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "SiteArtifact"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      input_artifacts  = ["src"]
      output_artifacts = ["site"]

      configuration = {
        ProjectName = aws_codebuild_project.site_build.name
      }
    }
  }

  stage {
    name = "Approve"

    action {
      name     = "RodneyApprovesTheSite"
      category = "Approval"
      owner    = "AWS"
      provider = "Manual"
      version  = "1"

      configuration = {
        CustomData = "Deploy of gotovasl.com. The build log prints the commit it built and the page count; check them before approving."
      }
    }
  }

  stage {
    name = "Deploy"

    action {
      name            = "S3AndCloudFront"
      category        = "Build"
      owner           = "AWS"
      provider        = "CodeBuild"
      version         = "1"
      input_artifacts = ["site"]

      configuration = {
        ProjectName = aws_codebuild_project.site_deploy.name
      }
    }
  }
}
