output "bundle_bucket" {
  value = aws_s3_bucket.code_bundle.id
}

output "bundle_key" {
  value = local.bundle_key
}

output "bundle_s3_uri" {
  description = "What the site pipeline's Source stage reads, and what the workflow writes to."
  value       = "s3://${aws_s3_bucket.code_bundle.id}/${local.bundle_key}"
}

output "upload_role_arn" {
  description = "Set as the role-to-assume in .github/workflows/code-bundle.yml."
  value       = aws_iam_role.bundle_upload.arn
}
