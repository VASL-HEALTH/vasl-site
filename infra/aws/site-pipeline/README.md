# The gotovasl.com deploy pipeline

Builds from `main` and publishes gotovasl.com, entirely inside AWS.

    Source (S3: main's bundle)  ->  Build (CodeBuild)  ->  Deploy (S3 + CloudFront)

**The site auto-deploys.** Ruling, Rodney 2026-11-14: a merge to `main` reaches
the live site with no human stop. There is no approval stage.

**The build is the gate.** That is not a softening of the old rule, it is where
the rule now lives. Every blocking check in `buildspec.yml` runs before the
Deploy stage exists as a possibility, and a red check fails Build, so Deploy is
never reached and the site keeps serving what it served before. The practical
consequence is worth stating plainly: **weakening a check in `buildspec.yml` is
now the same act as weakening the deploy gate.** `tools/internal_links.py
--check` and `tools/seo_validate.py` are blocking and must stay that way.

**Scope.** This applies to the marketing site only. The product pipelines --
the portals and VLAP -- keep their manual approvals. The asymmetry is
deliberate: the worst case here is a wrong page on a public brochure, and the
worst case there is a wrong answer about somebody in distress.

## What the real deploy target is

`s3://vasl-marketing-site` plus an invalidation of CloudFront distribution
`E11DM7B5W2KRCQ`. Not Amplify, not a bucket website endpoint, not ECS.

That came from `.github/workflows/deploy-site.yml`, which was deleted from
`main` in `2e1b40f` and read back with
`git show 2e1b40f^:.github/workflows/deploy-site.yml`. Everything it did was
then checked against the live account on 2026-11-13 under `rodney-admin`,
read-only:

| Checked | With | Result |
|---|---|---|
| the bucket exists, region | `aws s3api get-bucket-location` | `vasl-marketing-site`, us-east-1 |
| its encryption | `get-bucket-encryption` | AES256, no CMK, bucket keys on |
| whether an IAM role can write to it | `get-bucket-policy` | only an OAC read Allow and a DenyInsecureTransport; nothing denies a same-account principal, so an identity policy suffices |
| the distribution | `aws cloudfront get-distribution` | `E11DM7B5W2KRCQ`, Deployed, aliases `gotovasl.com` and `www.gotovasl.com` |
| its origins and behaviors | `get-distribution-config` | default origin `s3-vasl-marketing-site` behind OAC `E2QCFYRBWNPYQQ`; `/.well-known/*` goes to a different bucket; CachingOptimized cache policy; viewer-request function `vasl-marketing-viewer-request` for pretty URLs; 403/404 both map to `/404.html` with a 404 |

One thing the old workflow depended on does **not** exist: the repo variable
`MARKETING_DISTRIBUTION_ID`. `gh api repos/VASL-HEALTH/vasl-site/actions/variables`
returns `total_count: 0`, so that workflow would have failed its own fail-fast
step if anyone had run it. The distribution id is a literal in `main.tf` here.

## Why the source is S3

Standing ruling: *"Git never deploys; S3 does."*

A CodePipeline GitHub source needs a CodeConnections connection, and a new
connection sits in `PENDING` until somebody completes an OAuth handshake in a
browser — which nothing unattended can close.

But the repo already publishes itself to S3 on every push to `main`:
`.github/workflows/code-bundle.yml` writes `git bundle create repo.bundle main`
to `s3://vasl-site-code-bundle-558215002439/main/repo.bundle`. The pipeline
sources that object. Same commits, no connection, no browser.

That bundle bucket is created by `../code-bundle` with versioning enabled,
which an S3 source action requires — it triggers on a new object version.
**Apply `../code-bundle` first**: this pipeline has no source until that bucket
and that workflow exist.

## What stops a bad deploy now

Not a person. Four things, in order:

1. **`main`'s branch protection — but read what it actually covers.** The
   required contexts are *No GitHub Deploy Paths*, *CodeQL*, *Analyze
   (actions)* and *Analyze (python)*, and `required_approving_review_count` is
   **0**. **None of them inspects `site/`, and no human review is required.**
   `.github/workflows/seo-check.yml` would, but its push and `pull_request`
   triggers were removed on 2026-10-13 and it is `workflow_dispatch:` only. So
   this line is about *provenance*, not content: `enforce_admins` is on and
   force-push and deletion are blocked, so the bundle is genuinely whatever is
   on `main`. It is not a content gate, and listing it as one would inflate the
   apparent margin exactly where the human was removed.
2. **The blocking checks in `buildspec.yml`.** These fail the Build stage, and
   the Deploy stage cannot run without Build's output artifact.
3. **Separate roles.** `vasl-site-build` has CloudWatch Logs and the artifact
   bucket and nothing else -- no write on `vasl-marketing-site`, no CloudFront.
   Only `vasl-site-deploy` can publish, and only the Deploy stage can start it.
   That separation predates the auto-deploy ruling and still holds: a build that
   could also publish would let a compromised build step skip the Deploy stage's
   buildspec entirely.
4. **Versioned buckets.** The bundle bucket keeps three noncurrent versions for
   seven days, so a bad bundle is addressable by version id, and the site bucket
   is versioned too.

What is genuinely gone is the human read of the build log before publishing.
The build still prints the commit, the page count, the file count and the byte
count -- it is now a record to read *after* the fact rather than a gate.

## Why the deploy is a CodeBuild action

CodePipeline's S3 deploy provider sets **one** `Cache-Control` for everything
it writes, cannot delete files that left the repo, and cannot invalidate
CloudFront. The site needs three cache classes (immutable assets, 5-minute
sitemap/robots, must-revalidate HTML), `--delete` so a removed page stops being
live, an invalidation, and a smoke test. `buildspec-deploy.yml` does all of it
and still runs inside AWS, in the Deploy stage.

`buildspec-deploy.yml` is copied into the build artifact and read from there,
because a CodeBuild action reads its buildspec from its *input artifact* — so
the deploy script that runs is the one from the commit that was built.

## Scope, deliberately narrow

`site/` only. `prototype/` was already out of scope in the workflow this
replaces. Every grant names its resource: one source key, one site bucket, one
distribution, two CodeBuild projects by ARN.

## Applying it

IAM roots are applied by hand under `rodney-admin`, never from a session or
from CI. `../code-bundle` first, then:

```bash
cd infra/aws/site-pipeline
AWS_PROFILE=rodney-admin terraform init
AWS_PROFILE=rodney-admin terraform plan -out site-pipeline.tfplan
AWS_PROFILE=rodney-admin terraform apply site-pipeline.tfplan
```

**The stack is applied.** The first apply — 16 to add — happened on
2026-11-14: the artifact bucket and its four settings (public access block,
encryption, versioning, lifecycle), the two CodeBuild projects, the pipeline,
three roles with an inline policy each, and the approval policy with its
attachment to `rodney-admin`. State is
`vasl-site/site-pipeline/terraform.tfstate` in `vasl-terraform-state`.

**For the auto-deploy change the measured plan is 0 to add, 1 to change, 2 to
destroy.** The one change is `aws_codepipeline.site` updated **in place** —
removing a stage is not a replacement, though Terraform renders it as a
re-index (`~ name = "Approve" -> "Deploy"`) which reads more alarmingly than it
is. The two destroys are `aws_iam_policy.approve_site_deploy` and
`aws_iam_user_policy_attachment.rodney_approves`, which granted approval of a
stage that no longer exists. **Anything else is drift — stop and read it.**

`terraform fmt`: clean. `terraform validate`: **Success** (Terraform v1.15.8).

## Prove it before trusting it

None of this can be done from a session:

1. **Watch the first execution, do not assume it.** Push a no-op commit to
   `main`, confirm the pipeline starts on the new bundle version, and confirm
   it runs **Source -> Build -> Deploy with no stop**.
2. **Prove a red check stops the deploy.** Break a blocking check on a branch,
   merge it, and confirm Build fails and Deploy never runs. That is now the only
   gate, so it is the one worth proving rather than assuming.
3. **Read the build log.** It prints the
   commit, the page count, the file count and the byte count. 53 HTML pages is
   what `main` has today (`find site -name '*.html' | wc -l`, 2026-11-13).
4. **All eight build checks block, and that is now the whole gate.** The two
   that were advisory — `tools/seo_inject.py --check` and
   `tools/gen_sitemap.py --check` — had their `|| echo` tails removed by the
   November 2026 rebuild (`dd494e3`) and now fail the build like the rest.
   Measured on `7e4c4fc`: all eight exit 0, including `seo_inject` ("SEO head
   layer is current") and `gen_sitemap` ("sitemap.xml is current (26 URLs)").
   The blocking set is `build_pages`, `chrome_inject`, `retire_pages`,
   `check_forms`, `internal_links`, `seo_validate`, `seo_inject` and
   `gen_sitemap` — eight, not the two this file used to name. Restoring a
   `|| echo` tail to any of them removes a check from the only gate the deploy
   has.

## There is no deploy path until this is applied

`deploy-site.yml` is gone from `main` (deleted in `2e1b40f`, before this
directory existed) and its push trigger had already been removed on
2026-10-13, so the last real deploys were done by hand with `aws s3 sync` and a
CloudFront invalidation from a laptop. This pipeline replaces that, and **until
somebody applies it, the repo has no working deploy path at all.** That is the
intended end state of the ruling that put this here — nothing ships without a
deliberate merge to `main` — but it should not come as a surprise to
whoever next tries to publish a page.
