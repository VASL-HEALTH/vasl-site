# -*- coding: utf-8 -*-
"""Fail on a claim the site is not allowed to make.

Run by hand before a push, next to tools/check_copy.py:

    python tools/check_claims.py

DELIBERATELY NOT A CI JOB, for the same reason check_copy.py is not: the brief
for this surface says no new Actions checks.

check_copy.py owns the dash forms and the slop words, including the one word
it exempts in its screen-orientation sense. This file owns the claims. Together
they are the scan the outbound PDF build runs in
vasl-dataroom/scripts/build_outbound.py, pointed at the site instead.

WHY EACH RULE EXISTS

  HIPAA compliant     "Compliant" is a conclusion nobody certifies. The one
                      approved sentence names the rules and the agreement:
                      "Vasl operates under the HIPAA Privacy and Security
                      Rules and signs a business associate agreement with
                      every customer that shares protected health
                      information." Ruled 2026-11-15.

  Two Black founders  Off the founders line. The line is "Nobody built the
                      instrument because nobody in the room spoke the
                      language. We do."

  separate agreement  The data clause is "De-identified data and reviewer
                      decisions improve VLAP unless the customer opts out.
                      Identified data never leaves Vasl's AWS account."
                      "Nothing trains on it without a separate agreement"
                      said less and promised more.

  relative-% gain     A benchmark gain is points: +0.18, +0.22, +0.14. A
                      percentage invites the reader to compute a ratio of two
                      numbers that are not ratios.

  VLAP validated      VLAP is measured, not validated. No prospective
                      clinical validation is complete and no IRB-approved
                      prospective study has finished, so the word cannot
                      attach to VLAP, its signals, its taxonomy or its
                      corpus. It stays available for the instruments that
                      genuinely carry it, the PHQ-9 and its peers, and for
                      naming work that is not yet done.

  token counts        143M and 229.7M are internal corpus arithmetic that
                      moved. The public figure is "more than 120 million
                      tokens".

  DEP / ANX           Depression and anxiety are the next dimensions. There
                      is no public score for either.

  UTSW confirmed      The Dallas site is in negotiation. "Confirmed" is a
                      state it has not reached in public copy.

  vendor names        No outside AI vendor is in the inference path, so no
                      vendor belongs in the copy either.

REPORT ONLY: "trained" and "training". The outbound PDF build fails on both,
because in a two-page brief every use is about the model. On the site they are
overwhelmingly ordinary English (a clinically trained social worker, staff
training, a training program), so a hard rule here would mangle correct
sentences. The count is printed so a sweep is a decision somebody makes, not
something that happens silently.

Exit 0 clean, 1 with a report of every offending file:line.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
TOOLS = ROOT / "tools"
SELF = pathlib.Path(__file__).resolve()

# Literal strings, matched case-insensitively.
BANNED = [
    ("HIPAA compliant", "say that Vasl operates under the HIPAA Privacy and Security Rules"),
    ("HIPAA-compliant", "say that Vasl operates under the HIPAA Privacy and Security Rules"),
    ("HIPAA-aligned", "say that Vasl operates under the HIPAA Privacy and Security Rules"),
    ("Two Black founders", "the founders line stands on its own"),
    ("separate agreement", "use the data clause: improves VLAP unless the customer opts out"),
    ("Anthropic", "no outside AI vendor is in the inference path"),
    ("Claude", "no outside AI vendor is in the inference path"),
    ("143M tokens", "the public figure is more than 120 million tokens"),
    ("143 million tokens", "the public figure is more than 120 million tokens"),
    ("229.7M", "the public figure is more than 120 million tokens"),
    ("229.7 million", "the public figure is more than 120 million tokens"),
]

# Patterns, matched case-insensitively against the visible copy of one line.
PATTERNS = [
    (re.compile(r"\+\s?\d+(?:\.\d+)?\s?%"),
     "a benchmark gain is points, +0.18, not a relative percentage"),
    (re.compile(r"\d+(?:\.\d+)?\s?%\s+(?:gain|better|improvement|higher|lift|more accurate|relative)"),
     "a benchmark gain is points, +0.18, not a relative percentage"),
    (re.compile(r"(?:gain|improvement|lift|better)\s+of\s+\d+(?:\.\d+)?\s?%"),
     "a benchmark gain is points, +0.18, not a relative percentage"),
    # Only an affirmative, completed-state claim. "validation approach",
    # "validation status", "will be validated in SBIR Phase I" and the
    # emotional-validation sense a coach practises are all legitimate, and
    # "not itself a clinically validated figure" is the honest form of the
    # sentence, so the rule has to be narrower than the word.
    (re.compile(r"(?:vlap|our (?:own )?(?:model|engine)|the vasl (?:model|engine))"
                r"[^.<]{0,70}\b(?:is|are|was|were|has been|have been)\s+"
                r"(?:fully\s+|clinically\s+|independently\s+)*validated\b"),
     "VLAP is measured, not validated"),
    (re.compile(r"(?<!not )(?<!not itself a )\bclinically validated\b"),
     "VLAP is measured, not validated; clinically reviewed is the approved word"),
    (re.compile(r"\bvalidated (?:signal|taxonomy|corpus|weights|capabilit)"),
     "VLAP is measured, not validated"),
    (re.compile(r"\b(?:dep|anx)\b[^.<]{0,40}\b(?:roc-?auc|f1|score of)\b"),
     "there is no public depression or anxiety score"),
    (re.compile(r"(?:utsw|ut southwestern|southwestern medical)[^.<]{0,60}\bconfirm"),
     "the Dallas site is in negotiation, not confirmed"),
]

REPORT_ONLY = ["trained", "training"]

# A rise in a suicide rate is not a benchmark gain. The figure is cited on
# several pages with its source and must not trip the points rule. It is
# matched against a three-line window, because in a stat block the number and
# the label that makes it a rate are on different lines.
RATE_RISE = re.compile(
    r"\b(?:rose|rise|risen|fell|fall|fallen|change in|increase|decrease|decline|"
    r"suicide rate|per year|year over year)\b")

# A filename, not a vendor in the inference path.
FILENAME_EXEMPT = ("claude.md",)

TAG = re.compile(r"<[^>]+>")
COMMENT = re.compile(r"<!--.*?-->", re.S)
ENTITY = re.compile(r"&[a-zA-Z]+;|&#\d+;")


def visible(line: str) -> str:
    s = COMMENT.sub(" ", line)
    s = TAG.sub(" ", s)
    return ENTITY.sub(" ", s)


def targets():
    for p in sorted(SITE.rglob("*")):
        if p.is_file() and p.suffix in (".html", ".xml", ".txt"):
            yield p
    for p in sorted(TOOLS.glob("*.py")):
        if p.resolve() != SELF:
            yield p


def main() -> int:
    problems = []
    report = {w: 0 for w in REPORT_ONLY}
    scanned = 0
    in_style = False

    for path in targets():
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        html = path.suffix == ".html"
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            problems.append((rel, 0, "not valid UTF-8"))
            continue

        in_style = False
        for n, line in enumerate(lines, 1):
            if html:
                low_raw = line.lower()
                if "<style" in low_raw or "<script" in low_raw:
                    in_style = True
                if "</style" in low_raw or "</script" in low_raw:
                    in_style = False
                    continue
                if in_style:
                    continue
                text = visible(line)
            else:
                text = line
            low = text.lower()
            window = " ".join(visible(x) if html else x
                              for x in lines[max(0, n - 2):n + 2]).lower()

            for word, fix in BANNED:
                if word.lower() not in low:
                    continue
                if word == "Claude" and any(ex in low for ex in FILENAME_EXEMPT):
                    continue
                problems.append((rel, n, "%r: %s" % (word, fix)))
            for pattern, fix in PATTERNS:
                if pattern.search(low) and not RATE_RISE.search(window):
                    problems.append((rel, n, fix))
            for word in REPORT_ONLY:
                report[word] += len(re.findall(
                    r"(?<![\w-])" + word + r"(?![\w-])", low))

    if problems:
        print("CLAIM CHECK: %d problem(s) in %d files\n" % (len(problems), scanned))
        last = None
        for rel, n, what in problems:
            if rel != last:
                print("  " + rel)
                last = rel
            print("      line %d: %s" % (n, what))
        print("\n%d problem(s). No banned claim may ship." % len(problems))
        return 1

    print("CLAIM CHECK: clean. %d files, %d banned strings and %d patterns, zero hits."
          % (scanned, len(BANNED), len(PATTERNS)))
    print("REPORT ONLY (not a failure): %s."
          % ", ".join("%s x%d" % (w, report[w]) for w in REPORT_ONLY))
    return 0


if __name__ == "__main__":
    sys.exit(main())
