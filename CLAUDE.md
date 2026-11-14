# CLAUDE.md — vasl-site

DEPLOY RULE: Everything runs in AWS. Builds run in AWS (CodeBuild or the AWS workbench), artifacts go to ECR/S3, deploys run from AWS with Rodney's approval. GitHub holds source code only. GitHub has no BAA: no PHI, patient text, member replies, data samples, secrets or deploy credentials in any repo, PR, issue or Actions log. Never propose or build a GitHub Actions deploy, GitHub Environment deploy, deploy key, or GitHub-to-AWS OIDC role.

Enforced by `.github/workflows/no-github-deploys.yml`, a required check, which runs
`.github/scripts/check_no_github_deploys.py` over every workflow a PR adds or edits.
Run it yourself with `python .github/scripts/check_no_github_deploys.py --all`.

ONE EXEMPTION, by filename: `.github/workflows/code-bundle.yml`. It assumes a
GitHub-to-AWS OIDC role, which the paragraph above forbids, and it is allowed
anyway because it is a source mirror and not a deploy. Its role holds
`s3:PutObject` on one key of one private bucket
(`s3://vasl-site-code-bundle-558215002439/main/repo.bundle`) and nothing else:
no write on `vasl-marketing-site`, no `cloudfront:CreateInvalidation`, no
PassRole. Nothing it can do changes what a visitor sees. It exists because the
AWS deploy pipeline (`infra/aws/site-pipeline/`) sources that object — a
CodePipeline GitHub source would need a CodeConnections OAuth handshake in a
browser, which no unattended path can complete, so git never deploys and S3
does. **Do not delete it to "finish" removing GitHub deploy paths.** Deleting
it leaves the pipeline with no source, which is the mistake named at the end of
the next section.

## Parallel work

**Parallel or side work runs as subagents (model: opus) inside this session.
Never ask the user to open another terminal.**

A second terminal is a second session with its own context, and the two then
race: on 2026-11-13 three sessions built the same production safety gate in
parallel and produced two duplicate Semgrep workflows, two CODEOWNERS files
and a PR that deleted the code-bundle publisher another PR's pipeline read
from. Subagents share this session's context and report back into it, so the
work is divided rather than duplicated.

## Docker

**Never install or use Docker on the laptop. Container builds run in AWS only.**

Docker Desktop was uninstalled on 2026-11-14 after its disk file reached
85 GB on a 476 GB laptop with 23 GB free. Nothing needs it locally: images
are built by CodeBuild in the production pipeline, or on the workbench and
pushed to ECR from inside AWS. The only callers of a local daemon were the
laptop push scripts, which are the deploy bypass the production gate
removed.
