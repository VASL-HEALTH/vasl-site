# The gotovasl.com deploy pipeline

Builds from `main`, runs inside AWS, reaches the live site only after Rodney
approves. **Written and validated, NOT APPLIED** — see the apply section, and
read the warning at the bottom first.

    Source (S3: main's bundle)  ->  Build (CodeBuild)  ->  Approve  ->  Deploy (S3 + CloudFront)

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

## Where the approval actually lives

CodePipeline has **no "approver" field.** The gate is
`codepipeline:PutApprovalResult`, and `iam.tf` grants it to exactly one
principal (`user/rodney-admin`) on exactly one action
(`vasl-site/Approve/RodneyApprovesTheSite`). Anyone else with console access
sees the button and gets `AccessDenied`.

The approval is its **own stage**, not an option on the deploy: the deploy
stage has no other way to be reached, and a reordering edit would have to
delete a stage for the diff to hide it.

It is also enforced a second way, by permissions. The build role
(`vasl-site-build`) has CloudWatch Logs and the artifact bucket and *nothing
else* — no write on `vasl-marketing-site`, no CloudFront. Only
`vasl-site-deploy` can publish, and the only thing that can start it is the
Deploy stage, which sits behind the approval. If one role did both jobs the
approval would be decoration.

**What it cannot do:** an account administrator can attach themselves the same
action. That is true of every IAM control. This closes the ordinary route, not
the privileged one.

## Why the deploy is a CodeBuild action

CodePipeline's S3 deploy provider sets **one** `Cache-Control` for everything
it writes, cannot delete files that left the repo, and cannot invalidate
CloudFront. The site needs three cache classes (immutable assets, 5-minute
sitemap/robots, must-revalidate HTML), `--delete` so a removed page stops being
live, an invalidation, and a smoke test. `buildspec-deploy.yml` does all of it
and still runs inside AWS, after the approval.

`buildspec-deploy.yml` is copied into the build artifact and read from there,
because a CodeBuild action reads its buildspec from its *input artifact* — so
the deploy script that runs is the one from the commit that was approved.

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

**Expected plan: 16 to add, 0 to change, 0 to destroy.** Anything else is
drift — stop and read it. The 16: the artifact bucket and its four settings
(public access block, encryption, versioning, lifecycle), the two CodeBuild
projects, the pipeline, three roles with an inline policy each, the approval
policy and its attachment to `rodney-admin`.

`terraform fmt`: clean. `terraform validate`: **Success** (Terraform v1.15.8,
`init -backend=false`), 2026-11-13. State goes to
`vasl-site/site-pipeline/terraform.tfstate` in `vasl-terraform-state`.

## Prove it before trusting it

None of this can be done from a session:

1. **Watch the first execution, do not assume it.** Push a no-op commit to
   `main`, confirm the pipeline starts on the new bundle version, and confirm
   it **stops at Approve**.
2. **Prove the gate denies.** Have some other principal attempt
   `codepipeline:PutApprovalResult` and confirm `AccessDenied`. A gate nobody
   has seen refuse is a gate nobody has tested.
3. **Read the build log before approving the first time.** It prints the
   commit, the page count, the file count and the byte count. 53 HTML pages is
   what `main` has today (`find site -name '*.html' | wc -l`, 2026-11-13).
4. **Two build checks are ADVISORY and should not stay that way.**
   `tools/seo_inject.py --check` and `tools/gen_sitemap.py --check` both FAIL
   on `main` today — measured 2026-11-13 on `f607253`: 2 pages with an
   out-of-date head layer, and a stale `sitemap.xml`. Making them blocking
   would mean a pipeline that can never reach its own approval stage, and
   fixing them means regenerating files under `site/`, which the change that
   introduced this pipeline was scoped not to touch. So they print and do not
   fail. Run `python3 tools/seo_inject.py` and `python3 tools/gen_sitemap.py`,
   commit the result, then delete the `|| echo ...` tails in `buildspec.yml`.
   `tools/internal_links.py --check` and `tools/seo_validate.py` pass today and
   are already blocking.

## There is no deploy path until this is applied

`deploy-site.yml` is gone from `main` (deleted in `2e1b40f`, before this
directory existed) and its push trigger had already been removed on
2026-10-13, so the last real deploys were done by hand with `aws s3 sync` and a
CloudFront invalidation from a laptop. This pipeline replaces that, and **until
somebody applies it, the repo has no working deploy path at all.** That is the
intended end state of the ruling that put this here — nothing ships without a
deliberate approval, and nothing can ship until the approval exists — but it
should not come as a surprise to whoever next tries to publish a page.
