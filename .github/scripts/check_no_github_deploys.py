#!/usr/bin/env python3
"""Fail if a GitHub Actions workflow can deploy, hold AWS credentials, or use a deploy key.

Enforces the DEPLOY RULE at the top of CLAUDE.md: everything runs in AWS, GitHub
holds source code only. GitHub has no BAA, so a GitHub runner must never hold an
AWS credential, assume an AWS role, push an artifact, or mutate infrastructure.

Usage:
    check_no_github_deploys.py --changed BASE_REF   # workflows added/edited vs BASE_REF
    check_no_github_deploys.py --all                # every workflow in the tree
    check_no_github_deploys.py FILE [FILE ...]      # named files

A workflow that is ADDED or EDITED is scanned in full, not only on its added
lines. Editing a workflow that still carries a deploy path fails: the rule is
that the path is gone, not that this particular commit did not widen it.
Deleting a workflow is never a finding -- that is the fix.

Comment-only lines are skipped. A comment cannot deploy anything, and the
workflows here carry long decommission notes that quote the commands they
removed.

Exit 0 clean, 1 on any finding, 2 on a usage error.
"""

import os
import re
import subprocess
import sys

WORKFLOW_DIR = ".github/workflows"

# Literal values that are not credentials. botocore needs something in the
# environment or it walks the provider chain and dies on NoRegionError; CI
# fixtures set these so nothing reaches for a real provider.
DUMMY_VALUES = set("""
testing test tests dummy fake foo bar none null localstack minioadmin
accesskey secretkey changeme 000000000000 123456789012 xxx placeholder unset
""".split())

CRED_KEYS = re.compile(
    r"\b(AWS_ACCESS_KEY_ID|AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN)\b\s*[:=]\s*(.*)"
)
AKIA_LITERAL = re.compile(r"\bAKIA[0-9A-Z]{16}\b")

# Anything that assumes an AWS role from a runner.
OIDC_PATTERNS = [
    (re.compile(r"aws-actions/configure-aws-credentials"),
     "assumes an AWS role from the runner (aws-actions/configure-aws-credentials)"),
    (re.compile(r"^\s*role-to-assume\s*:"),
     "assumes an AWS role from the runner (role-to-assume)"),
    (re.compile(r"\baws\s+sts\s+assume-role(-with-web-identity)?\b"),
     "assumes an AWS role from the runner (aws sts assume-role)"),
    (re.compile(r"\bweb-identity-token-file\b"),
     "assumes an AWS role from the runner (web identity token)"),
]

# Mutating AWS and release commands. Read-only calls (describe-*, list-*, get-*)
# are deliberately absent: reading state is not deploying.
DEPLOY_PATTERNS = [
    (re.compile(r"\baws\s+ecs\s+(update-service|register-task-definition|create-service|delete-service|deploy|run-task|start-task|execute-command)\b"),
     "ECS deploy command"),
    (re.compile(r"\baws\s+s3\s+(cp|sync|mv|rm|rb|mb|website)\b"),
     "S3 write command"),
    (re.compile(r"\baws\s+s3api\s+(put-|delete-|create-|copy-)"),
     "S3 write command"),
    (re.compile(r"\baws\s+ecr(-public)?\s+(get-login-password|put-image|batch-delete-image|create-repository|delete-repository|put-lifecycle-policy)\b"),
     "ECR write command"),
    (re.compile(r"aws-actions/amazon-ecr-login"),
     "ECR login action"),
    (re.compile(r"aws-actions/amazon-ecs-(deploy|render)-task-definition"),
     "ECS deploy action"),
    (re.compile(r"\bdocker\s+push\b"),
     "container image push"),
    (re.compile(r"\baws\s+lambda\s+(update-function-code|update-function-configuration|publish-version|create-function)\b"),
     "Lambda deploy command"),
    (re.compile(r"\baws\s+cloudfront\s+create-invalidation\b"),
     "CloudFront invalidation"),
    (re.compile(r"\baws\s+cloudformation\s+(deploy|create-stack|update-stack|execute-change-set)\b"),
     "CloudFormation deploy"),
    (re.compile(r"\baws\s+deploy\s+create-deployment\b"),
     "CodeDeploy deployment"),
    (re.compile(r"\baws\s+ec2\s+(run-instances|terminate-instances|start-instances)\b"),
     "EC2 instance control"),
    (re.compile(r"\baws\s+ssm\s+(send-command|start-session)\b"),
     "SSM remote execution"),
    (re.compile(r"\baws\s+(apprunner|amplify|elasticbeanstalk)\s+(start-deployment|create-deployment|update-service|start-job)\b"),
     "managed-service deploy"),
    (re.compile(r"\b(sam|cdk|serverless|sls|eb|wrangler|flyctl|vercel|netlify)\s+deploy\b"),
     "third-party deploy command"),
    (re.compile(r"\bkubectl\s+(apply|delete|set|rollout)\b"),
     "Kubernetes deploy command"),
    (re.compile(r"\bhelm\s+(install|upgrade)\b"),
     "Helm deploy command"),
    (re.compile(r"\bterraform\s+(apply|destroy|import)\b"),
     "Terraform mutation"),
]

DEPLOY_KEY_PATTERNS = [
    (re.compile(r"webfactory/ssh-agent|shimataro/ssh-key-action"),
     "deploy-key / ssh-agent action"),
    (re.compile(r"\b(DEPLOY_KEY|DEPLOY_SSH_KEY|SSH_PRIVATE_KEY|SSH_DEPLOY_KEY)\b"),
     "deploy-key secret"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
     "inline private key"),
    (re.compile(r"\bssh-add\b"),
     "ssh-add (deploy key into agent)"),
]

ALL_LINE_PATTERNS = OIDC_PATTERNS + DEPLOY_PATTERNS + DEPLOY_KEY_PATTERNS


def is_comment(line):
    return line.lstrip().startswith("#")


def cred_finding(line):
    """Return a label if the line assigns a real AWS credential, else None."""
    if AKIA_LITERAL.search(line):
        return "hardcoded AWS access key id"
    match = CRED_KEYS.search(line)
    if not match:
        return None
    key, raw = match.group(1), match.group(2).strip()
    raw = raw.split("#", 1)[0].strip()
    value = raw.strip("'").strip('"').strip()
    if not value:
        return None
    if value.lower() in DUMMY_VALUES:
        return None
    if "secrets." in value or "vars." in value:
        return key + " sourced from a GitHub secret or variable"
    if value.startswith("${{"):
        return key + " sourced from a GitHub expression"
    return key + " set to a literal value"


def structural_findings(text):
    """Findings regex cannot judge: job-level GitHub Environments, and an
    id-token mint that is actually paired with AWS use in the same workflow.

    `environment:` is also a common workflow_dispatch INPUT name, so matching it
    by regex flags the wrong thing. Parsing tells a deploy Environment apart
    from an input that happens to share the word.
    """
    out = []
    try:
        import yaml
    except ImportError:
        return out
    try:
        doc = yaml.safe_load(text)
    except Exception:
        return out
    if not isinstance(doc, dict):
        return out

    touches_aws = bool(
        any(p.search(text) for p, _ in OIDC_PATTERNS)
        or re.search(r"\baws\s+[a-z0-9-]+\s", text)
    )

    def id_token_write(node):
        perms = node.get("permissions") if isinstance(node, dict) else None
        return isinstance(perms, dict) and perms.get("id-token") == "write"

    if id_token_write(doc) and touches_aws:
        out.append("workflow mints an OIDC id-token and touches AWS "
                   "(GitHub-to-AWS OIDC)")

    jobs = doc.get("jobs")
    if isinstance(jobs, dict):
        for job_name, job in jobs.items():
            if not isinstance(job, dict):
                continue
            env = job.get("environment")
            if env:
                name = env.get("name") if isinstance(env, dict) else env
                out.append("job %s uses GitHub Environment %r "
                           "(GitHub Environment deploy)" % (job_name, name))
            if id_token_write(job) and touches_aws:
                out.append("job %s mints an OIDC id-token in a workflow that "
                           "touches AWS (GitHub-to-AWS OIDC)" % job_name)
    return out


def scan_file(path):
    findings = []
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            text = handle.read()
    except OSError as exc:
        return [(path, 0, "unreadable: %s" % exc)]

    for lineno, line in enumerate(text.splitlines(), 1):
        if is_comment(line):
            continue
        label = cred_finding(line)
        if label:
            findings.append((path, lineno, label))
        for pattern, pattern_label in ALL_LINE_PATTERNS:
            if pattern.search(line):
                findings.append((path, lineno, pattern_label))

    for label in structural_findings(text):
        findings.append((path, 0, label))
    return findings


def git_stdout(*args):
    result = subprocess.run(["git"] + list(args), capture_output=True,
                            text=True, check=False)
    return result.stdout


def changed_workflows(base):
    """Workflows added, modified or renamed relative to base. Deletions excluded."""
    out = git_stdout("diff", "--name-status", "--diff-filter=AMR",
                     base + "...HEAD")
    if not out.strip():
        out = git_stdout("diff", "--name-status", "--diff-filter=AMR", base, "HEAD")
    paths = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        path = parts[-1].replace("\\", "/")
        if path.startswith(WORKFLOW_DIR) and path.endswith((".yml", ".yaml")):
            paths.append(path)
    return paths


def all_workflows():
    if not os.path.isdir(WORKFLOW_DIR):
        return []
    return sorted(
        WORKFLOW_DIR + "/" + name
        for name in os.listdir(WORKFLOW_DIR)
        if name.endswith((".yml", ".yaml"))
    )


EXPLANATION = """
Everything runs in AWS. GitHub holds source code only, and has no BAA.
Builds belong in CodeBuild or the AWS workbench, artifacts in ECR/S3, and
deploys run from AWS with Rodney's approval. A GitHub Actions deploy, a GitHub
Environment deploy, a deploy key and a GitHub-to-AWS OIDC role are all out of
bounds. See the DEPLOY RULE at the top of CLAUDE.md.
"""


def main(argv):
    if not argv:
        sys.stderr.write(__doc__)
        return 2
    if argv[0] == "--changed":
        if len(argv) < 2:
            sys.stderr.write("--changed needs a base ref\n")
            return 2
        targets = changed_workflows(argv[1])
    elif argv[0] == "--all":
        targets = all_workflows()
    else:
        targets = argv

    targets = [t for t in targets if os.path.exists(t)]
    if not targets:
        print("No workflow file added or edited. Nothing to check.")
        return 0

    print("Scanned %d workflow file(s):" % len(targets))
    for path in targets:
        print("  " + path)

    findings = []
    for path in targets:
        findings.extend(scan_file(path))

    if not findings:
        print("\nClean. No AWS credential, role assumption, deploy command, "
              "GitHub Environment or deploy key.")
        return 0

    print("\nDEPLOY RULE violation -- %d finding(s):\n" % len(findings))
    for path, lineno, label in findings:
        where = "%s:%d" % (path, lineno) if lineno else path
        print("  %s\n      %s" % (where, label))
        if lineno:
            print("::error file=%s,line=%d::DEPLOY RULE: %s" % (path, lineno, label))
        else:
            print("::error file=%s::DEPLOY RULE: %s" % (path, label))
    print(EXPLANATION)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
