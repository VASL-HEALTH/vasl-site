#!/usr/bin/env python3
"""
Rewrite <title> and meta description on the pages where the shipped version was
too long for the SERP, too short to earn a click, or carried no buyer keyword.

Why this is a separate script from seo_inject.py: this one edits the page's own
source-of-truth tags, by hand-authored value. seo_inject.py then mirrors those
values into OG/Twitter/JSON-LD. Run this first, then seo_inject.py.

Every title targets a query a district, health plan, or community-org buyer
actually types. Nothing here makes a clinical or diagnostic claim.

Run: python3 tools/seo_titles.py
"""

import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"

# rel -> (title, description). Either may be None to leave that tag alone.
REWRITES = {
    # ---- Primary buyer paths -------------------------------------------------
    "index.html": (
        "Culturally Grounded Youth Behavioral Health | Vasl Health",
        "Behavioral health for Black, Latino, and first-generation youth 14–24 — "
        "built on how they actually speak. Detection, not diagnosis.",
    ),
    "for-schools.html": (
        "School-Based Mental Health Platform for Districts | Vasl",
        "A tiered youth behavioral health program for K-12 districts — peer support "
        "through licensed therapy, mapped to MTSS and staffed by people students "
        "recognize.",
    ),
    "health-systems.html": (
        "Youth Behavioral Health for Health Plans & Systems | Vasl",
        "Reach and retain the adolescent and transition-age members standard programs "
        "lose. Engagement built on cultural and linguistic fit, not translation.",
    ),
    "for-organizations.html": (
        "Youth Mental Health for Community Organizations | Vasl",
        "Community health centers, FQHCs, and youth-serving nonprofits use Vasl to "
        "extend behavioral health support without hiring a clinical team of their own.",
    ),
    "for-families.html": (
        "For Families: What Vasl Reads, and What It Never Does",
        "What Vasl looks at, what it never stores, and what a parent or guardian "
        "should expect. Plain language, no clinical jargon, no surveillance.",
    ),
    "pricing.html": (
        "Pricing for Schools, Health Plans & Nonprofits | Vasl",
        "How Vasl is priced by population size and setting, what a pilot includes, "
        "and which funding sources districts and plans typically use to pay for it.",
    ),
    # ---- Product -------------------------------------------------------------
    "platform.html": (
        "Youth Behavioral Health Platform: The Full Continuum | Vasl",
        "Five layers in one system: peer community, check-ins, culturally matched "
        "coaching, licensed therapy, and crisis support — human in the loop at every "
        "escalation.",
    ),
    "vlap.html": (
        "VLAP: Reading Youth Language for Distress Signals | Vasl",
        "Vasl's language layer — 47 culturally specific distress signals across coded "
        "language, AAVE, and youth vernacular, surfaced to humans, never used to "
        "diagnose.",
    ),
    "ai-model.html": (
        "CulturalBERT: AI Trained on How Youth Actually Speak",
        "Standard clinical NLP misreads AAVE and youth vernacular. CulturalBERT is "
        "trained on it directly — 2,400+ tokens, six signal categories, no "
        "diagnostic output.",
    ),
    "peer-groups.html": (
        "Moderated Peer Support Groups for Youth | Vasl Health",
        "Facilitated peer groups where youth show up as themselves — the relationship "
        "that exists before a crisis does, run by people from their own communities.",
    ),
    "teletherapy.html": (
        "Culturally Matched Teletherapy for Youth | Vasl Health",
        "Licensed therapy for youth 14–24, matched on culture and language rather than "
        "availability alone — the layer reached only when it is actually needed.",
    ),
    "technology.html": (
        "Architecture, Privacy & Security | Vasl Health",
        "PHI boundaries, auditability, human-in-the-loop escalation, and "
        "population-level insight without individual records — written for security "
        "and compliance reviewers.",
    ),
    "infrastructure.html": (
        "Infrastructure & Data Handling | Vasl Health",
        "The hosting, encryption, access control, and retention model behind Vasl — "
        "what a district IT reviewer or plan security team needs before a pilot.",
    ),
    # ---- Evidence ------------------------------------------------------------
    "outcomes.html": (
        "Youth Behavioral Health Outcomes & ROI | Vasl Health",
        "Pilot-cohort results and stakeholder ROI for districts, plans, and "
        "community organizations — with the methodology behind every number stated "
        "openly.",
    ),
    "clinical-outcomes.html": (
        "Clinical Outcomes: Symptom Change & Retention | Vasl",
        "PHQ-8 change at 90 days, 30-day retention, time to first meaningful "
        "support, and escalation rates from Vasl pilot cohorts — with methodology "
        "and limitations.",
    ),
    "research.html": (
        "Research & Evidence Base | Vasl Health",
        "The peer-reviewed literature Vasl is built on, the active IRB study "
        "underway with a university partner, and how we handle claims we cannot yet "
        "support.",
    ),
    # ---- Company -------------------------------------------------------------
    "about.html": (
        "About Vasl Health: Built for the Youth Systems Miss",
        "Behavioral health for Black, Latino, and first-generation youth — designed "
        "inside their language and culture from the start, not retrofitted after.",
    ),
    "team.html": (
        "Our Team & Clinical Advisors | Vasl Health",
        "The clinicians, engineers, and community practitioners building Vasl — and "
        "the advisory structure that governs what the platform is allowed to claim.",
    ),
    "careers.html": (
        "Careers at Vasl Health",
        "Open roles across clinical, engineering, and community partnerships — and "
        "what we expect from people building for youth who are usually built around.",
    ),
    "contact.html": (
        "Contact Vasl Health — Request a Demo",
        "Schedule a demo, ask about implementation timelines, or reach our clinical, "
        "education, research, or community partnerships teams directly.",
    ),
    "support.html": (
        "Help Center & Implementation Support | Vasl Health",
        "Answers on getting started, assessments, billing, clinical escalation, "
        "compliance, and VLAP — for partners already running Vasl.",
    ),
    "blog.html": (
        "Insights & Research on Behavioral Health Equity | Vasl",
        "Writing on mental health equity, culturally responsive AI, Medicaid policy, "
        "and building technology for communities that existing systems consistently "
        "miss.",
    ),
    "accessibility.html": (
        "Accessibility Statement | Vasl Health",
        "How Vasl approaches WCAG conformance, assistive technology support, and "
        "reporting an accessibility barrier you encounter on this site or in the "
        "product.",
    ),
    # ---- Blog posts: titles trimmed to fit the SERP --------------------------
    "blog-bridging-chasm.html": (
        "Bridging the Chasm: Health Equity in Mental Health AI",
        None,
    ),
    "blog-future-culturally-responsive.html": (
        "The Future of Mental Health Must Be Culturally Responsive",
        None,
    ),
    "blog-medicaid-populations.html": (
        "Why Medicaid Populations Are Central to BH Innovation",
        "Medicaid serves the populations where behavioral health need is highest and "
        "standard care fails hardest — plus the policy architecture that makes scale "
        "possible.",
    ),
    "blog-mental-health-equity-crisis.html": (
        "The Mental Health Equity Crisis and Cultural AI",
        "Why the access gap in youth behavioral health is also a language gap — and "
        "what culturally trained models can and cannot do about it.",
    ),
    "blog-other-diagnosis.html": (
        "The Other Diagnosis: Identity-Based Stress",
        "Identity-based stress is not a disorder, and treating it as one is part of "
        "the problem. What it looks like in youth language, and why systems keep "
        "reading it wrong.",
    ),
    # ---- Utility -------------------------------------------------------------
    "prototype.html": (
        "Interactive Prototype | Vasl Health",
        "A walkthrough of the Vasl member and facilitator experience. Illustrative "
        "only — no real member data appears anywhere in this prototype.",
    ),
    "404.html": (
        "Page Not Found | Vasl Health",
        "That page could not be found. Head back to gotovasl.com, or use the "
        "navigation above to find what you were looking for.",
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def main() -> int:
    changed = 0
    for rel, (title, desc) in sorted(REWRITES.items()):
        path = SITE / rel
        if not path.exists():
            print(f"  skip  {rel} (missing)")
            continue
        html = path.read_text(encoding="utf-8")
        before = html

        # Edit the page's own tags, never the generated block. If we rewrote the
        # copy inside <!-- SEO:VASL -->, the next seo_inject.py run would strip it
        # and silently revert this edit.
        block = re.search(r"<!-- SEO:VASL -->.*?<!-- /SEO:VASL -->", html, re.S)
        stash = block.group(0) if block else None
        if stash:
            html = html.replace(stash, "\x00SEOBLOCK\x00", 1)

        if title:
            html = re.sub(
                r"<title>.*?</title>", f"<title>{esc(title)}</title>", html, count=1, flags=re.S
            )
        if desc:
            new_tag = f'<meta name="description" content="{esc(desc)}">'
            if re.search(r'<meta[^>]+name=["\']description["\'][^>]*>', html, re.I):
                html = re.sub(
                    r'<meta[^>]+name=["\']description["\'][^>]*>',
                    new_tag,
                    html,
                    count=1,
                    flags=re.I,
                )
            else:
                html = html.replace("<title>", new_tag + "\n<title>", 1)

        if stash:
            html = html.replace("\x00SEOBLOCK\x00", stash, 1)

        if html != before:
            path.write_text(html, encoding="utf-8")
            changed += 1
            tl = len(title) if title else 0
            dl = len(desc) if desc else 0
            print(f"  update  {rel:42} title={tl:<3} desc={dl}")

    print(f"\nRewrote {changed} page(s). Now run: python3 tools/seo_inject.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
