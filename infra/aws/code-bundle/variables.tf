variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "github_repo" {
  description = "owner/repo allowed to assume the upload role, pinned to refs/heads/main."
  type        = string
  default     = "VASL-HEALTH/vasl-site"
}
