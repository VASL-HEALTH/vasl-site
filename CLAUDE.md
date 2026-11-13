# CLAUDE.md — vasl-site

DEPLOY RULE: Everything runs in AWS. Builds run in AWS (CodeBuild or the AWS workbench), artifacts go to ECR/S3, deploys run from AWS with Rodney's approval. GitHub holds source code only. GitHub has no BAA: no PHI, patient text, member replies, data samples, secrets or deploy credentials in any repo, PR, issue or Actions log. Never propose or build a GitHub Actions deploy, GitHub Environment deploy, deploy key, or GitHub-to-AWS OIDC role.

Enforced by `.github/workflows/no-github-deploys.yml`, a required check, which runs
`.github/scripts/check_no_github_deploys.py` over every workflow a PR adds or edits.
Run it yourself with `python .github/scripts/check_no_github_deploys.py --all`.
