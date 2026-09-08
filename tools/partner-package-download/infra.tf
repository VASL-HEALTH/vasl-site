# Partner Package self-serve download -- infrastructure.
#
# WHERE THIS LIVES: this file documents/defines resources for the
# Partner Package download endpoint. It is checked into vasl-site for
# visibility, but per .github/workflows/deploy-site.yml's own comment
# ("Infrastructure lives in VASL-PLATFORM/infra/aws/static-sites"),
# actual AWS provisioning for this project happens OUTSIDE the vasl-site
# repo's deploy pipeline. The GitHub Actions OIDC role that deploys
# gotovasl.com is scoped to S3 sync + CloudFront invalidation only -- it
# cannot create Lambda functions, IAM roles, or new S3 buckets, and it
# should not be widened just for this feature.
#
# HOW TO DEPLOY (one-time, by whoever holds AWS console/CLI access to
# the Vasl Health account -- same person/process that manages the
# VASL-PLATFORM infra repo):
#   1. cd into a scratch dir with this file (or copy it into
#      VASL-PLATFORM/infra/aws/ alongside the other site infra, which is
#      the more correct long-term home for it).
#   2. terraform init && terraform apply
#   3. Upload the PDF once:
#        aws s3 cp Vasl-Partner-Package-COMPLETE4.pdf \
#          s3://$(terraform output -raw bucket_name)/partner-package.pdf
#   4. terraform output function_url  ->  paste that URL into
#      site/contact.html's PARTNER_PACKAGE_ENDPOINT constant (see the
#      comment at the top of the script block in that file) and push to
#      main. The existing deploy pipeline handles the HTML change as
#      usual -- only the AWS side needs this manual apply.
#
# COST: Lambda + a single-object S3 bucket + on-demand invocations is
# within AWS's always-free tier at any realistic Partner Package
# request volume ($0/mo in practice). No form SaaS subscription needed.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "allowed_origin" {
  description = "Origin allowed to call the download endpoint via CORS."
  type        = string
  default     = "https://gotovasl.com"
}

variable "object_key" {
  description = "S3 key of the Partner Package PDF inside the private bucket."
  type        = string
  default     = "partner-package.pdf"
}

# Private bucket -- NOT the public marketing-site bucket. Block all
# public access; the Lambda reaches it via IAM, visitors reach it only
# via a presigned, time-limited URL minted per-request.
resource "aws_s3_bucket" "partner_package" {
  bucket = "vasl-partner-package-private"
}

resource "aws_s3_bucket_public_access_block" "partner_package" {
  bucket                  = aws_s3_bucket.partner_package.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "partner_package" {
  bucket = aws_s3_bucket.partner_package.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda/handler.py"
  output_path = "${path.module}/lambda/handler.zip"
}

resource "aws_iam_role" "partner_package_lambda" {
  name = "vasl-partner-package-download"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "partner_package_lambda" {
  name = "s3-get-and-logs"
  role = aws_iam_role.partner_package_lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject"]
        Resource = "${aws_s3_bucket.partner_package.arn}/${var.object_key}"
      },
      {
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

resource "aws_lambda_function" "partner_package_download" {
  function_name    = "vasl-partner-package-download"
  role             = aws_iam_role.partner_package_lambda.arn
  handler          = "handler.handler"
  runtime          = "python3.12"
  timeout          = 10
  memory_size      = 128
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      BUCKET         = aws_s3_bucket.partner_package.id
      OBJECT_KEY     = var.object_key
      ALLOWED_ORIGIN = var.allowed_origin
    }
  }
}

# Function URL -- no API Gateway needed, keeps this to two resources
# and zero extra monthly cost. CORS is enforced here (primary) as well
# as echoed by the handler (defense in depth).
resource "aws_lambda_function_url" "partner_package_download" {
  function_name      = aws_lambda_function.partner_package_download.function_name
  authorization_type = "NONE"

  cors {
    allow_origins = [var.allowed_origin]
    allow_methods = ["POST"]
    allow_headers = ["content-type"]
    max_age       = 300
  }
}

output "bucket_name" {
  value = aws_s3_bucket.partner_package.id
}

output "function_url" {
  value = aws_lambda_function_url.partner_package_download.function_url
}
