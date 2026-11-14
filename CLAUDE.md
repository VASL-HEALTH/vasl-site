# CLAUDE.md — vasl-site

DEPLOY RULE: Everything runs in AWS. Builds run in AWS (CodeBuild or the AWS workbench), artifacts go to ECR/S3, deploys run from AWS with Rodney's approval. GitHub holds source code only. GitHub has no BAA: no PHI, patient text, member replies, data samples, secrets or deploy credentials in any repo, PR, issue or Actions log. Never propose or build a GitHub Actions deploy, GitHub Environment deploy, deploy key, or GitHub-to-AWS OIDC role.

Enforced by `.github/workflows/no-github-deploys.yml`, a required check, which runs
`.github/scripts/check_no_github_deploys.py` over every workflow a PR adds or edits.
Run it yourself with `python .github/scripts/check_no_github_deploys.py --all`.

## Parallel work

**Parallel or side work runs as subagents (model: opus) inside this session.
Never ask the user to open another terminal.**

A second terminal is a second session with its own context, and the two then
race: on 2026-11-13 three sessions built the same production safety gate in
parallel and produced two duplicate Semgrep workflows, two CODEOWNERS files
and a PR that deleted the code-bundle publisher another PR's pipeline read
from. Subagents share this session's context and report back into it, so the
work is divided rather than duplicated.
