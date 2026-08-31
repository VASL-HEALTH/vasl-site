# Generates site/demo.html — the static VLAP explainer.
#
# The page describes the engine and never runs it. There is no textarea, no
# input, no scoring and no model on visitor text; see the commit that replaced
# the previous /demo.html for why that is a hard constraint and not a taste
# preference.
#
# The signal reference is EMITTED FROM the live engine's SIGNAL_TAXONOMY rather
# than transcribed, because the page it replaced got 15 of its 16 signal codes
# wrong by hand-copying them. Point VLAP_ENGINE_PATH at
# services/vlap-service/vlap_engine.py in the VASL-PLATFORM checkout:
#
#   VLAP_ENGINE_PATH=<path-to>/vlap_engine.py python tools/gen_demo_explainer.py
#
# Then run the site-wide head layer, same as any other page -- it owns the
# SEO:VASL block and CI (seo-check) fails if it has not been run:
#
#   python tools/seo_inject.py
#
# seo_inject also rewrites index.html, which is unrelated to this page and has
# been failing seo-check on main since 2026-08-22. Check that diff and drop it
# unless you actually mean to change the logo in its ld+json.
#
# Keep the page description apostrophe-free: seo_inject truncates the og and
# twitter description at the first one.
#
# Combination rules (R1-R8), risk-level definitions and validation status are
# maintained in this file against docs/VLAP_TAXONOMY_v1.0.md Sections 2, 4 and 5.
# If the taxonomy moves, they move here. The 47 signals take care of themselves.
import json, re, os, sys

_DEFAULT_ENGINE = os.path.expanduser("~/VASL-PLATFORM/services/vlap-service/vlap_engine.py")
ENGINE = os.environ.get("VLAP_ENGINE_PATH", _DEFAULT_ENGINE)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "site", "demo.html")

if not os.path.exists(ENGINE):
    sys.exit(
        f"vlap_engine.py not found at {ENGINE}. "
        "Set VLAP_ENGINE_PATH to services/vlap-service/vlap_engine.py in your "
        "VASL-PLATFORM checkout. The signal list is generated from it on purpose "
        "-- do not hand-edit the signal rows in site/demo.html."
    )

src = open(ENGINE, encoding="utf-8").read()
entries = re.findall(r'"((?:HOP|SHA|CCM|ISO|TRM|PFE)-\d\d)": \{(.*?)\n    \},', src, re.S)
assert len(entries) == 47, f"expected 47 signals in SIGNAL_TAXONOMY, found {len(entries)}"

dims = {}
for code, body in entries:
    label = re.search(r'"label": "(.*?)"', body).group(1)
    dim = re.search(r'"dimension": "(.*?)"', body).group(1)
    risk = re.search(r'"risk_level": "(.*?)"', body).group(1)
    # design-handoff/SKILL.md: named entities in text, so escape both the
    # ampersands and the literal em dashes ISO-03/ISO-06 carry in the engine source.
    label = label.replace("&", "&amp;").replace("\u2014", "&mdash;").replace("\ufffd", "&mdash;")
    dims.setdefault(dim, {"code": code[:3], "rows": []})["rows"].append((code, label, risk))

ORDER = [
    ("Hopelessness & Futility",
     "Futility, foreclosed futures, and burden narratives &mdash; including the vernacular constructions generic models read as venting."),
    ("Coded Suicidal Ideation",
     "Ideation as it is actually written by youth: euphemism built to evade platform moderation, inverted framing, community-specific reference."),
    ("Minimization & Disclosure Suppression",
     "The hedge, the joke, the walk-back. Patterns that precede disclosure rather than contradict it."),
    ("Social Isolation & Withdrawal",
     "Severance, withdrawal, and the specific isolation of being unwelcome at home."),
    ("Trauma & Acute Stressor Markers",
     "Social determinants as they surface in language &mdash; housing, food, policing, immigration status, cumulative loss."),
    ("Protective Factor Erosion",
     "What a young person is losing. Erosion signals, not credits: every one of the seven adds to concern rather than subtracting from it."),
]
assert set(k for k, _ in ORDER) == set(dims), set(dims) ^ set(k for k, _ in ORDER)

RISK_NOTE = {
    "High": "Warrants human review on its own.",
    "Moderate": "Logged and monitored; reviewed in combination.",
    "Low": "Contextual or longitudinal marker.",
    "Variable": "Context-dependent &mdash; read against co-occurring signals.",
}

# Section 4 rules, verbatim from vlap_engine.py COMBINATION_RULES.
RULES = [
    ("R1", "HIGH", "Any SHA signal together with any HOP signal",
     "Ideation alongside futility. Either alone is a signal; together the taxonomy treats it as immediate human review."),
    ("R2", "HIGH", "SHA-02, SHA-05 or SHA-08 on their own",
     "The three the taxonomy will not wait on: platform-evasion euphemism, method inquiry inside a minimising wrapper, and community-specific death reference."),
    ("R3", "HIGH", "HOP-03 together with HOP-07",
     "AAVE futility construction plus burden narrative. The taxonomy names this its highest-risk pattern."),
    ("R4", "HIGH", "ISO-06 together with any SHA signal",
     "Family rejection alongside ideation &mdash; the combination that carries the most weight for LGBTQIA+ youth."),
    ("R5", "HIGH", "CCM-04 together with SHA-02",
     "Ideation delivered as a joke. The humour is the disclosure mechanism, not a discount on the content."),
    ("R6", "MODERATE", "Three or more CCM signals in one session",
     "Not one hedge but a pattern of them. Reads as heavy suppression, and the response is to create an opening rather than to press."),
    ("R7", "MODERATE", "PFE-02, ISO-01 and HOP-04 together",
     "Trusted-adult loss, withdrawal and coded exhaustion. A slow-burn pattern no single signal would surface."),
    ("R8", "MODERATE", "Three or more TRM signals in one session",
     "Social determinants stacking. Documents the circumstances and points at resource connection."),
]

# docs/VLAP_TAXONOMY_v1.0.md Section 5, current status column.
VALIDATION = [
    ("HOP", "HOP-01 validated in pilot cohorts (n=47). HOP-02 through HOP-09 annotated; sensitivity and specificity pending a powered study."),
    ("SHA", "SHA-01 validated. SHA-02 detected in 23 pilot instances with 100% clinical confirmation. SHA-03 through SHA-08 annotated; underpowered."),
    ("CCM", "All signals annotated in pilot data. CCM-04 the most frequently occurring. No powered validation study completed."),
    ("ISO", "ISO-01 validated. ISO-06 flagged in 8 pilot instances. Others annotated only."),
    ("TRM", "All signals annotated. No powered validation. Normalisation in community language makes annotation complex; an inter-rater reliability study is required."),
    ("PFE", "All signals annotated as longitudinal markers. Validation requires accumulated session data."),
]

TIERS = [
    ("LOW", "No row written."),
    ("MODERATE", "No row written, unless the message is flagged for review."),
    ("HIGH", "Writes a row in the clinician queue."),
    ("CRISIS", "Writes a row in the clinician queue, carrying the shortest review window."),
]


def dim_section(name, blurb):
    d = dims[name]
    rows = "\n".join(
        f'        <div class="sig-row"><span class="sig-code">{c}</span>'
        f'<span class="sig-label">{l}</span>'
        f'<span class="sig-risk r-{r.lower()}">{r}</span></div>'
        for c, l, r in d["rows"]
    )
    return f"""    <div class="dim reveal">
      <div class="dim-head">
        <span class="dim-code">{d['code']}</span>
        <h3 class="dim-name">{name.replace('&', '&amp;')}</h3>
        <span class="dim-count">{len(d['rows'])} signals</span>
      </div>
      <p class="dim-blurb">{blurb}</p>
      <div class="sig-list">
{rows}
      </div>
    </div>"""


DIMS_HTML = "\n".join(dim_section(n, b) for n, b in ORDER)

RULES_HTML = "\n".join(
    f"""      <div class="rule reveal">
        <div class="rule-top"><span class="rule-id">{rid}</span><span class="rule-level">combined level: {lvl}</span></div>
        <div class="rule-when">{when}</div>
        <div class="rule-why">{why}</div>
      </div>"""
    for rid, lvl, when, why in RULES
)

VAL_HTML = "\n".join(
    f'      <div class="val-row"><span class="val-cat">{c}</span><span class="val-txt">{t}</span></div>'
    for c, t in VALIDATION
)

TIER_HTML = "\n".join(
    f'      <div class="tier-row"><span class="tier-name">{n}</span><span class="tier-what">{w}</span></div>'
    for n, w in TIERS
)

RISK_KEY_HTML = "\n".join(
    f'      <div class="rk-row"><span class="rk-name r-{k.lower()}">{k}</span><span class="rk-def">{v}</span></div>'
    for k, v in RISK_NOTE.items()
)

# No apostrophe: tools/seo_inject.py truncates the og/twitter description at the
# first one, which silently shipped a social preview reading "...in young people".
DESC = ("How VLAP reads distress in the language youth actually write: the 47-signal, "
        "six-dimension taxonomy, the register-aware analysis behind it, and the clinical "
        "decision support boundary it operates inside.")

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{DESC}">
<title>How VLAP Reads Language | Vasl Health</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<!-- SEO:VASL -->
<link rel="canonical" href="https://gotovasl.com/demo">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Vasl Health">
<meta property="og:title" content="How VLAP Reads Language | Vasl Health">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="https://gotovasl.com/demo">
<meta property="og:image" content="https://gotovasl.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Vasl Health &mdash; Language Is Care">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="How VLAP Reads Language | Vasl Health">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="https://gotovasl.com/og-image.png">
<script defer data-domain="gotovasl.com" src="https://plausible.io/js/script.outbound-links.tagged-events.js"></script>
<script>window.plausible=window.plausible||function(){{(window.plausible.q=window.plausible.q||[]).push(arguments)}}</script>
<script>(function(){{var PAGE="demo";document.addEventListener("click",function(e){{var a=e.target.closest("a[href]");if(!a)return;var href=a.getAttribute("href");if(!href)return;if(/(^|\\/)contact\\.html(\\?|#|$)/.test(href)){{window.plausible("Contact CTA",{{props:{{page:PAGE}}}});}}}},true);}})();</script>
<!-- /SEO:VASL -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400;1,6..72,500&family=IBM+Plex+Sans:ital,wght@0,300;0,400;0,500;1,300;1,400&family=IBM+Plex+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0;}}
html{{scroll-behavior:smooth;}}
:root{{
  --warm-white:#FAF7F2;--parchment:#F0EAE0;--ink:#1C1C1C;
  --ink-70:rgba(28,28,28,0.70);--ink-50:rgba(28,28,28,0.50);--ink-12:rgba(28,28,28,0.12);
  --clay:#C4896F;--clay-light:#E8C4AE;--clay-pale:#F5E6DC;
  --deep-green:#2D4A3E;--dust:#8B7B6B;--chalk:#E2DAD0;--charcoal:#222222;
  --serif:'Newsreader',Georgia,serif;--sans:'IBM Plex Sans',sans-serif;--mono:'IBM Plex Mono',monospace;
  --gutter:7vw;
}}
body{{background:var(--warm-white);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.65;overflow-x:hidden;}}
.reveal{{transition:opacity 0.9s cubic-bezier(0.16,1,0.3,1),transform 0.9s cubic-bezier(0.16,1,0.3,1);}}
.js-ready .reveal{{opacity:0;transform:translateY(20px);}}
.js-ready .reveal.visible{{opacity:1;transform:translateY(0);}}
.d1{{transition-delay:0.08s;}}.d2{{transition-delay:0.16s;}}.d3{{transition-delay:0.24s;}}
nav{{position:fixed;top:0;left:0;right:0;z-index:100;padding:20px var(--gutter);display:flex;align-items:center;justify-content:space-between;background:rgba(250,247,242,0.93);backdrop-filter:blur(14px);border-bottom:1px solid var(--ink-12);}}
.nav-logo{{font-family:var(--serif);font-size:22px;font-weight:400;letter-spacing:-0.02em;color:var(--ink);text-decoration:none;}}
.nav-logo span{{color:var(--clay);font-style:italic;}}
.nav-links{{display:flex;gap:28px;list-style:none;}}
.nav-links a{{font-family:var(--mono);font-size:10px;letter-spacing:0.09em;text-transform:uppercase;color:var(--dust);text-decoration:none;transition:color 0.2s;}}
.nav-links a:hover,.nav-links a.active{{color:var(--ink);}}
.nav-cta{{font-family:var(--mono);font-size:10px;letter-spacing:0.07em;text-transform:uppercase;color:var(--deep-green);border:1px solid var(--deep-green);padding:9px 20px;text-decoration:none;transition:background 0.22s,color 0.22s;}}
.nav-cta:hover{{background:var(--deep-green);color:var(--warm-white);}}
section{{padding:130px var(--gutter);position:relative;}}
.chapter-label{{font-family:var(--mono);font-size:10px;font-weight:300;letter-spacing:0.16em;text-transform:uppercase;color:var(--clay);display:flex;align-items:center;gap:12px;margin-bottom:52px;}}
.chapter-label::after{{content:'';display:block;width:36px;height:1px;background:var(--clay);opacity:0.45;}}
.chapter-label.light{{color:var(--clay-light);}}
.chapter-label.light::after{{background:var(--clay-light);}}
.btn-dark{{font-family:var(--mono);font-size:11px;letter-spacing:0.08em;text-transform:uppercase;background:var(--ink);color:var(--warm-white);padding:16px 32px;text-decoration:none;display:inline-block;transition:background 0.22s;}}
.btn-dark:hover{{background:var(--deep-green);}}
.btn-ghost{{font-family:var(--mono);font-size:11px;letter-spacing:0.08em;text-transform:uppercase;color:var(--dust);text-decoration:none;display:inline-flex;align-items:center;gap:8px;transition:color 0.2s;}}
.btn-ghost:hover{{color:var(--ink);}}
.btn-ghost::after{{content:'\\2192';}}
.btn-light{{font-family:var(--mono);font-size:11px;letter-spacing:0.08em;text-transform:uppercase;background:var(--warm-white);color:var(--ink);padding:16px 32px;text-decoration:none;display:inline-block;transition:background 0.22s;}}
.btn-light:hover{{background:var(--clay-light);}}
.btn-ghost-light{{font-family:var(--mono);font-size:11px;letter-spacing:0.08em;text-transform:uppercase;color:rgba(250,247,242,0.40);text-decoration:none;display:inline-flex;align-items:center;gap:8px;transition:color 0.2s;}}
.btn-ghost-light:hover{{color:var(--warm-white);}}
.btn-ghost-light::after{{content:'\\2192';}}

/* HERO */
#hero{{padding-top:170px;padding-bottom:110px;background:var(--warm-white);border-bottom:1px solid var(--chalk);display:grid;grid-template-columns:1.15fr 1fr;gap:0 80px;align-items:end;}}
.hero-kicker{{font-family:var(--mono);font-size:10px;letter-spacing:0.18em;text-transform:uppercase;color:var(--dust);margin-bottom:36px;display:block;}}
.hero-headline{{font-family:var(--serif);font-size:clamp(40px,4.8vw,68px);font-weight:300;line-height:1.06;letter-spacing:-0.03em;color:var(--ink);margin-bottom:34px;}}
.hero-headline em{{font-style:italic;color:var(--clay);}}
.hero-body{{font-size:19px;font-weight:300;line-height:1.72;color:var(--ink-70);max-width:520px;margin-bottom:30px;}}
.hero-actions{{display:flex;align-items:center;gap:28px;flex-wrap:wrap;margin-top:44px;}}
.hero-right{{border-left:1px solid var(--chalk);padding-left:64px;}}
.stat-item{{padding:20px 0;border-bottom:1px solid var(--chalk);}}
.stat-item:last-child{{border-bottom:none;}}
.stat-num{{font-family:var(--serif);font-size:38px;font-weight:300;line-height:1;letter-spacing:-0.03em;color:var(--deep-green);margin-bottom:8px;}}
.stat-desc{{font-size:14px;font-weight:300;color:var(--ink-70);line-height:1.6;}}

/* STATIC-PAGE NOTICE */
.notice{{border:1px solid var(--chalk);background:var(--clay-pale);padding:22px 26px;max-width:520px;}}
.notice-head{{font-family:var(--mono);font-size:9px;letter-spacing:0.14em;text-transform:uppercase;color:var(--clay);margin-bottom:10px;}}
.notice-body{{font-size:14px;font-weight:300;line-height:1.65;color:var(--ink-70);}}

/* DIFFERENTIATOR (dark) */
#register{{background:var(--charcoal);color:var(--warm-white);}}
.reg-head{{max-width:860px;margin-bottom:64px;}}
.reg-headline{{font-family:var(--serif);font-size:clamp(34px,4vw,54px);font-weight:300;line-height:1.1;letter-spacing:-0.025em;color:var(--warm-white);margin-bottom:30px;}}
.reg-headline em{{font-style:italic;color:var(--clay-light);}}
.reg-body{{font-size:18px;font-weight:300;line-height:1.75;color:rgba(250,247,242,0.62);margin-bottom:20px;}}
.reg-body:last-child{{margin-bottom:0;}}
.reg-body strong{{color:var(--warm-white);font-weight:500;}}
.reg-grid{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1px;background:rgba(250,247,242,0.10);}}
.reg-card{{background:var(--charcoal);padding:34px 32px;}}
.reg-card-label{{font-family:var(--mono);font-size:9px;letter-spacing:0.12em;text-transform:uppercase;color:var(--clay-light);margin-bottom:14px;}}
.reg-card-title{{font-family:var(--serif);font-size:21px;font-weight:400;color:var(--warm-white);margin-bottom:12px;letter-spacing:-0.01em;}}
.reg-card-desc{{font-size:14px;font-weight:300;color:rgba(250,247,242,0.60);line-height:1.65;}}
.reg-foot{{margin-top:44px;padding-top:26px;border-top:1px solid rgba(250,247,242,0.12);font-size:13px;font-weight:300;line-height:1.7;color:rgba(250,247,242,0.45);max-width:860px;}}

/* TAXONOMY */
#taxonomy{{background:var(--warm-white);border-bottom:1px solid var(--chalk);}}
.tax-head{{max-width:720px;margin-bottom:26px;}}
.tax-headline{{font-family:var(--serif);font-size:clamp(34px,4vw,54px);font-weight:300;line-height:1.1;letter-spacing:-0.025em;color:var(--ink);margin-bottom:24px;}}
.tax-headline em{{font-style:italic;color:var(--clay);}}
.tax-body{{font-size:17px;font-weight:300;line-height:1.72;color:var(--ink-70);}}
.risk-key{{margin:44px 0 64px;padding:26px 30px;background:var(--parchment);border:1px solid var(--chalk);max-width:780px;}}
.risk-key-head{{font-family:var(--mono);font-size:9px;letter-spacing:0.14em;text-transform:uppercase;color:var(--dust);margin-bottom:18px;}}
.rk-row{{display:grid;grid-template-columns:92px 1fr;gap:16px;padding:7px 0;align-items:baseline;}}
.rk-def{{font-size:14px;font-weight:300;color:var(--ink-70);line-height:1.6;}}
.dim{{padding:40px 0;border-top:1px solid var(--chalk);}}
.dim-head{{display:flex;align-items:baseline;gap:16px;margin-bottom:12px;flex-wrap:wrap;}}
.dim-code{{font-family:var(--mono);font-size:11px;letter-spacing:0.14em;color:var(--clay);}}
.dim-name{{font-family:var(--serif);font-size:26px;font-weight:400;letter-spacing:-0.015em;color:var(--ink);}}
.dim-count{{font-family:var(--mono);font-size:10px;letter-spacing:0.1em;text-transform:uppercase;color:var(--dust);margin-left:auto;}}
.dim-blurb{{font-size:15px;font-weight:300;color:var(--ink-70);line-height:1.65;max-width:720px;margin-bottom:26px;}}
.sig-list{{display:grid;grid-template-columns:1fr 1fr;gap:0 48px;}}
.sig-row{{display:grid;grid-template-columns:64px 1fr auto;gap:14px;align-items:baseline;padding:9px 0;border-bottom:1px solid var(--ink-12);}}
.sig-code{{font-family:var(--mono);font-size:11px;letter-spacing:0.05em;color:var(--dust);}}
.sig-label{{font-size:14px;font-weight:300;color:var(--ink);line-height:1.5;}}
/* Signal risk level is typographic, never a tier colour: weight, case and rule only. */
.sig-risk{{font-family:var(--mono);font-size:9px;letter-spacing:0.1em;text-transform:uppercase;color:var(--ink-50);white-space:nowrap;}}
.r-high{{color:var(--ink);font-weight:500;}}
.r-moderate{{color:var(--ink-70);font-weight:400;}}
.r-low{{color:var(--ink-50);font-weight:300;}}
.r-variable{{color:var(--ink-50);font-weight:300;font-style:italic;text-transform:none;letter-spacing:0.02em;font-size:11px;}}

/* COMBINATION RULES */
#rules{{background:var(--parchment);border-bottom:1px solid var(--chalk);}}
.rules-head{{max-width:760px;margin-bottom:60px;}}
.rules-headline{{font-family:var(--serif);font-size:clamp(34px,4vw,54px);font-weight:300;line-height:1.1;letter-spacing:-0.025em;color:var(--ink);margin-bottom:24px;}}
.rules-headline em{{font-style:italic;color:var(--clay);}}
.rules-body{{font-size:17px;font-weight:300;line-height:1.72;color:var(--ink-70);}}
.rules-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--chalk);}}
.rule{{background:var(--parchment);padding:30px 32px;}}
.rule-top{{display:flex;align-items:baseline;gap:14px;margin-bottom:14px;}}
.rule-id{{font-family:var(--mono);font-size:12px;font-weight:500;letter-spacing:0.06em;color:var(--clay);}}
.rule-level{{font-family:var(--mono);font-size:9px;letter-spacing:0.1em;text-transform:uppercase;color:var(--dust);margin-left:auto;}}
.rule-when{{font-family:var(--serif);font-size:19px;font-weight:400;color:var(--ink);line-height:1.35;letter-spacing:-0.01em;margin-bottom:10px;}}
.rule-why{{font-size:14px;font-weight:300;color:var(--ink-70);line-height:1.65;}}
.rules-foot{{margin-top:44px;font-size:14px;font-weight:300;line-height:1.7;color:var(--ink-50);max-width:820px;}}

/* CDS BOUNDARY (green) */
#cds{{background:var(--deep-green);color:var(--warm-white);}}
.cds-head{{max-width:820px;margin-bottom:56px;}}
.cds-headline{{font-family:var(--serif);font-size:clamp(32px,3.8vw,50px);font-weight:300;line-height:1.12;letter-spacing:-0.025em;color:var(--warm-white);margin-bottom:26px;}}
.cds-headline em{{font-style:italic;color:var(--clay-light);}}
.cds-body{{font-size:18px;font-weight:300;line-height:1.75;color:rgba(250,247,242,0.62);margin-bottom:18px;}}
.cds-cols{{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:rgba(250,247,242,0.14);margin-bottom:50px;}}
.cds-col{{background:var(--deep-green);padding:32px 34px;}}
.cds-col-head{{font-family:var(--mono);font-size:9px;letter-spacing:0.14em;text-transform:uppercase;color:var(--clay-light);margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid rgba(250,247,242,0.14);}}
.cds-col p{{font-size:15px;font-weight:300;color:rgba(250,247,242,0.72);line-height:1.6;padding:9px 0;}}
.cds-col.not p{{color:rgba(250,247,242,0.50);}}
.tier-block{{max-width:840px;}}
.tier-head{{font-family:var(--mono);font-size:9px;letter-spacing:0.14em;text-transform:uppercase;color:rgba(250,247,242,0.40);margin-bottom:6px;}}
.tier-sub{{font-size:14px;font-weight:300;line-height:1.7;color:rgba(250,247,242,0.50);margin-bottom:22px;}}
.tier-row{{display:grid;grid-template-columns:130px 1fr;gap:20px;padding:13px 0;border-bottom:1px solid rgba(250,247,242,0.12);align-items:baseline;}}
.tier-name{{font-family:var(--mono);font-size:11px;letter-spacing:0.12em;color:var(--warm-white);}}
.tier-what{{font-size:14px;font-weight:300;color:rgba(250,247,242,0.62);line-height:1.6;}}

/* VALIDATION */
#validation{{background:var(--warm-white);border-bottom:1px solid var(--chalk);}}
.val-head{{max-width:760px;margin-bottom:48px;}}
.val-headline{{font-family:var(--serif);font-size:clamp(32px,3.8vw,50px);font-weight:300;line-height:1.12;letter-spacing:-0.025em;color:var(--ink);margin-bottom:24px;}}
.val-headline em{{font-style:italic;color:var(--clay);}}
.val-lead{{font-size:17px;font-weight:300;line-height:1.72;color:var(--ink-70);}}
.val-row{{display:grid;grid-template-columns:80px 1fr;gap:24px;padding:18px 0;border-bottom:1px solid var(--chalk);align-items:baseline;max-width:960px;}}
.val-cat{{font-family:var(--mono);font-size:12px;letter-spacing:0.1em;color:var(--clay);}}
.val-txt{{font-size:15px;font-weight:300;color:var(--ink-70);line-height:1.65;}}
.val-foot{{margin-top:40px;padding-top:24px;border-top:1px solid var(--chalk);max-width:960px;font-size:14px;font-weight:300;line-height:1.7;color:var(--ink-50);}}

/* CTA */
#cta{{background:var(--ink);color:var(--warm-white);text-align:center;}}
.cta-headline{{font-family:var(--serif);font-size:clamp(32px,4.2vw,56px);font-weight:300;font-style:italic;line-height:1.12;letter-spacing:-0.02em;color:var(--warm-white);max-width:800px;margin:0 auto 26px;}}
.cta-headline em{{color:var(--clay-light);font-style:italic;}}
.cta-body{{font-size:17px;font-weight:300;line-height:1.75;color:rgba(250,247,242,0.58);max-width:600px;margin:0 auto 40px;}}
.cta-actions{{display:flex;align-items:center;justify-content:center;gap:26px;flex-wrap:wrap;}}

@media(max-width:1100px){{
  #hero{{grid-template-columns:1fr;gap:64px;}}
  .hero-right{{border-left:none;padding-left:0;border-top:1px solid var(--chalk);padding-top:40px;}}
  .reg-grid{{grid-template-columns:1fr;}}
  .rules-grid{{grid-template-columns:1fr;}}
  .cds-cols{{grid-template-columns:1fr;}}
  .sig-list{{grid-template-columns:1fr;gap:0;}}
}}
@media(max-width:768px){{
  :root{{--gutter:5vw;}}
  section{{padding:90px var(--gutter);}}
  .nav-links{{display:none;}}
  .sig-row{{grid-template-columns:60px 1fr;gap:10px;}}
  .sig-risk{{grid-column:2;padding-top:2px;}}
  .rk-row,.val-row,.tier-row{{grid-template-columns:1fr;gap:4px;}}
}}

.ham-btn{{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:6px;margin-left:8px;}}
.ham-btn span{{display:block;width:22px;height:1.5px;background:var(--ink);transition:all 0.2s;}}
.ham-btn.open span:nth-child(1){{transform:translateY(6.5px) rotate(45deg);}}
.ham-btn.open span:nth-child(2){{opacity:0;}}
.ham-btn.open span:nth-child(3){{transform:translateY(-6.5px) rotate(-45deg);}}
@media(max-width:780px){{
  .ham-btn{{display:flex;}}
  .nav-links{{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:var(--warm-white);z-index:200;flex-direction:column;align-items:center;justify-content:center;gap:32px;}}
  .nav-links.open{{display:flex;}}
  .nav-links a{{font-size:22px;letter-spacing:0.04em;}}
  .nav-cta{{display:none;}}
}}

footer{{background:var(--charcoal);border-top:1px solid rgba(250,247,242,0.08);padding:0;}}
.footer-sitemap{{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr 1fr 1fr;gap:0;padding:56px 7vw 40px;border-bottom:1px solid rgba(250,247,242,0.08);}}
.fs-brand{{padding-right:40px;}}
.footer-logo{{font-family:var(--serif);font-size:22px;color:var(--warm-white);letter-spacing:-0.02em;text-decoration:none;display:block;margin-bottom:12px;}}
.footer-logo span{{color:var(--clay);font-style:italic;}}
.footer-mission{{font-family:var(--mono);font-size:9px;letter-spacing:0.08em;text-transform:uppercase;color:rgba(250,247,242,0.28);line-height:1.8;margin-bottom:20px;}}
.fs-cta{{display:inline-block;font-family:var(--mono);font-size:9px;letter-spacing:0.10em;text-transform:uppercase;color:var(--clay);border:1px solid rgba(196,137,111,0.40);padding:9px 18px;text-decoration:none;transition:all 0.18s;}}
.fs-cta:hover{{background:rgba(196,137,111,0.12);}}
.fs-col{{padding-left:32px;border-left:1px solid rgba(250,247,242,0.06);}}
.fs-head{{font-family:var(--mono);font-size:9px;letter-spacing:0.14em;text-transform:uppercase;color:rgba(250,247,242,0.30);margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid rgba(250,247,242,0.06);}}
.fs-col a{{display:block;font-family:var(--mono);font-size:10px;letter-spacing:0.06em;text-transform:uppercase;color:rgba(250,247,242,0.45);text-decoration:none;margin-bottom:10px;transition:color 0.15s;}}
.fs-col a:hover{{color:var(--clay);}}
.footer-bottom{{padding:20px 7vw;display:flex;align-items:center;justify-content:space-between;}}
.footer-copy{{font-family:var(--mono);font-size:9px;color:rgba(250,247,242,0.20);}}
.footer-legal{{display:flex;gap:20px;}}
.footer-legal a{{font-family:var(--mono);font-size:9px;letter-spacing:0.08em;text-transform:uppercase;color:rgba(250,247,242,0.22);text-decoration:none;}}
.footer-legal a:hover{{color:var(--clay);}}
@media(max-width:1100px){{.footer-sitemap{{grid-template-columns:1fr 1fr 1fr;gap:32px;}}.fs-brand{{grid-column:1/-1;padding-right:0;}}.fs-col{{border-left:none;padding-left:0;}}}}
@media(max-width:680px){{.footer-sitemap{{grid-template-columns:1fr 1fr;}}.footer-bottom{{flex-direction:column;gap:12px;text-align:center;}}}}
@media(max-width:400px){{.footer-sitemap{{grid-template-columns:1fr;}}}}
</style>
</head>
<body>

<nav>
  <a href="index.html" class="nav-logo">Vasl <span>Health</span></a>
  <ul class="nav-links">
    <li><a href="about.html">About</a></li>
    <li><a href="platform.html">Platform</a></li>
    <li><a href="outcomes.html">Outcomes</a></li>
    <li><a href="blog.html">Blog</a></li>
    <li><a href="team.html">Team</a></li>
    <li><a href="contact.html">Contact</a></li>
  </ul>
  <button class="ham-btn" id="ham-btn" onclick="toggleNav()" aria-label="Menu">
    <span></span><span></span><span></span>
  </button>
  <a href="contact.html" class="nav-cta">Request a Demo</a>
</nav>

<!-- HERO -->
<section id="hero">
  <div>
    <span class="hero-kicker reveal">Vasl Language Analysis Platform</span>
    <h1 class="hero-headline reveal d1">The distress a young person <em>has already told you about</em> &mdash; in the words they actually used.</h1>
    <p class="hero-body reveal d2">VLAP is Vasl's natural-language engine for behavioral-health distress in youth communication. It is built for the language Black youth actually write &mdash; vernacular futility constructions, coded ideation, humour-masked disclosure &mdash; the constructions generic screening models read as venting and drop.</p>
    <p class="hero-body reveal d2">Forty-seven signals across six clinical dimensions, a rules layer that reads them in combination, and a single output: a signal made visible to a licensed clinician, who decides what happens next.</p>
    <div class="hero-actions reveal d3">
      <a href="contact.html" class="btn-dark">Request a clinical walkthrough</a>
      <a href="vlap.html" class="btn-ghost">Why VLAP exists</a>
    </div>
  </div>
  <div class="hero-right">
    <div class="stat-item reveal d1">
      <div class="stat-num">47</div>
      <div class="stat-desc">Discrete linguistic, behavioral and contextual signals in the v1.0 taxonomy.</div>
    </div>
    <div class="stat-item reveal d2">
      <div class="stat-num">6</div>
      <div class="stat-desc">Clinical dimensions: hopelessness, coded ideation, minimisation, isolation, trauma markers, and protective-factor erosion.</div>
    </div>
    <div class="stat-item reveal d3">
      <div class="stat-num">8</div>
      <div class="stat-desc">Combination rules evaluated after inference, so a co-occurrence no single signal would surface still reaches a clinician.</div>
    </div>
  </div>
</section>

<!-- THE DIFFERENTIATOR -->
<section id="register">
  <div class="chapter-label light">Where VLAP is different</div>
  <div class="reg-head">
    <h2 class="reg-headline">A screening tool that reads dialect as noise <em>will read distress as attitude.</em></h2>
    <p class="reg-body">Most language models were trained on text that does not sound like the young people Vasl serves. Presented with a vernacular futility construction &mdash; the double negation, the intensifier doing the emotional work &mdash; a generic model returns frustration, or venting, and moves on. The young person disclosed. The instrument did not hear it.</p>
    <p class="reg-body"><strong>VLAP detects the register first, then reads the message inside it.</strong> When the engine identifies African American English, Spanish-English code-switching, or a pre-disclosure minimisation move, it does not discount what follows. It raises the weight it gives the distress evidence, because in this population that framing is where the disclosure lives.</p>
  </div>
  <div class="reg-grid">
    <div class="reg-card reveal">
      <div class="reg-card-label">Register detection</div>
      <div class="reg-card-title">Dialect is read, not corrected</div>
      <div class="reg-card-desc">The engine scores dialect markers and grammatical constructions across the whole message before scoring risk. Register is an input to the analysis, not something normalised away before it starts.</div>
    </div>
    <div class="reg-card reveal d1">
      <div class="reg-card-label">Weighting</div>
      <div class="reg-card-title">Vernacular raises the read, it does not lower it</div>
      <div class="reg-card-desc">Detected AAVE register and pre-disclosure minimisation both increase the weight carried by co-occurring distress signals. The bias being corrected runs in one direction, so the correction does too.</div>
    </div>
    <div class="reg-card reveal d2">
      <div class="reg-card-label">Privacy</div>
      <div class="reg-card-title">The words themselves stay out of the chart</div>
      <div class="reg-card-desc">A clinician sees that the register was detected and that the analysis was tuned for it. The specific dialect tokens a young person used are never rendered on a clinical screen as evidence against them.</div>
    </div>
  </div>
  <p class="reg-foot">HOP-03, the AAVE futility construction, is the signal the taxonomy names as carrying the largest single share of VLAP's sensitivity advantage over baseline, and the one with the highest false-negative rate in generic models. Register weighting is an engineering calibration and is not itself a clinically validated figure; see validation status below.</p>
</section>

<!-- TAXONOMY -->
<section id="taxonomy">
  <div class="chapter-label">The taxonomy</div>
  <div class="tax-head">
    <h2 class="tax-headline">Forty-seven signals, <em>six dimensions,</em> one codebook.</h2>
    <p class="tax-body">Each signal has a code, a clinical label, and a risk level describing what it means on its own. The list below is the live v1.0 taxonomy, generated from the engine's own signal definitions. It is the same reference a clinician reads, and the same codebook used for annotation.</p>
  </div>
  <div class="risk-key">
    <div class="risk-key-head">Risk level &mdash; the significance of one signal in isolation</div>
{RISK_KEY_HTML}
  </div>
{DIMS_HTML}
</section>

<!-- COMBINATION RULES -->
<section id="rules">
  <div class="chapter-label">The reasoning</div>
  <div class="rules-head">
    <h2 class="rules-headline">A score tells a clinician how worried to be. <em>These tell them why.</em></h2>
    <p class="rules-body">Signals are not read in isolation. After inference, a separate rules layer evaluates the detected set against eight combination rules drawn from the taxonomy. A rule that fires is recorded with its reason, so what reaches the clinician is not a number but a pattern with a name. The combined level a rule elevates to has exactly two values, and it is always shown labelled, because the same words appear on other scales that mean other things.</p>
  </div>
  <div class="rules-grid">
{RULES_HTML}
  </div>
  <p class="rules-foot">These are post-inference business logic, not a model training target. A fired rule is what the rules layer concluded from the model's output &mdash; not, itself, something the model detected. Keeping the two separable is what lets a clinician see the difference.</p>
</section>

<!-- CDS BOUNDARY -->
<section id="cds">
  <div class="chapter-label light">The boundary</div>
  <div class="cds-head">
    <h2 class="cds-headline">Vasl surfaces the signal. <em>A licensed clinician decides.</em></h2>
    <p class="cds-body">VLAP is clinical decision support. It does not diagnose, and it is never member-facing. It does not contact a young person, a guardian, a clinician or a crisis service on anyone's behalf, and it does not decide that somebody must be reached right now. That judgement belongs to the treating provider.</p>
  </div>
  <div class="cds-cols">
    <div class="cds-col">
      <div class="cds-col-head">What Vasl does</div>
      <p>Writes a row in the clinician's queue when a message crosses a surfacing threshold.</p>
      <p>Makes a high signal prominent in that queue, with the signals and rules behind it.</p>
      <p>Scopes which clinician can see which members' signals.</p>
      <p>Records who read what, and when.</p>
    </div>
    <div class="cds-col not">
      <div class="cds-col-head">What Vasl does not do</div>
      <p>Email, page, text or otherwise notify a human that a signal was found.</p>
      <p>Decide that a signal warrants immediate contact.</p>
      <p>Choose a recipient and send to them.</p>
      <p>Diagnose, close, resolve or act on a case.</p>
    </div>
  </div>
  <div class="tier-block">
    <div class="tier-head">Surfacing tier</div>
    <p class="tier-sub">An operational routing bucket, not a clinical grade and not part of the taxonomy. It decides one thing: whether a queue row is written, and how quickly it asks to be looked at.</p>
{TIER_HTML}
    <p class="tier-sub" style="margin-top:26px;margin-bottom:0;">Because Vasl does not dispatch, a surfaced signal is seen when a clinician looks. The safety property lives in a monitored queue and in whatever alerting the client organisation runs on its own side. Vasl does not claim to reach anyone.</p>
  </div>
</section>

<!-- VALIDATION -->
<section id="validation">
  <div class="chapter-label">Validation status</div>
  <div class="val-head">
    <h2 class="val-headline">What has been validated, <em>and what has not.</em></h2>
    <p class="val-lead">The taxonomy's own status line is "pending independent clinical review and validation." Four signals carry pilot evidence today. Stating which four, and what the rest are, is more useful than a blanket disclaimer.</p>
  </div>
{VAL_HTML}
  <p class="val-foot">Validation in progress toward NIMH SBIR Phase I. HOP-01, SHA-01, ISO-01 and SHA-02 carry pilot evidence; taxonomy-wide sensitivity and specificity are the Phase I aim. Independent clinical review, sociolinguistic review, community advisory review, inter-rater reliability and a powered sensitivity and specificity study are the named steps before this is a validated instrument.</p>
</section>

<!-- CTA -->
<section id="cta">
  <h2 class="cta-headline">Language is culture, <em>not pathology.</em> Interpretation is care.</h2>
  <p class="cta-body">This page describes the engine. Seeing it read real clinical language is a conversation with a clinician on our team, under the access controls the product actually ships with.</p>
  <div class="cta-actions">
    <a href="contact.html" class="btn-light">Request a clinical walkthrough</a>
    <a href="research.html" class="btn-ghost-light">The validation agenda</a>
  </div>
</section>

<!-- LINKS:VASL -->
<style>
.vrl-wrap{{padding:70px var(--gutter);border-top:1px solid var(--chalk);background:var(--warm-white,var(--parchment));}}
.vrl-head{{font-family:var(--mono);font-size:10px;letter-spacing:0.16em;text-transform:uppercase;color:var(--clay);margin-bottom:36px;display:flex;align-items:center;gap:12px;}}
.vrl-head::after{{content:'';display:block;width:36px;height:1px;background:var(--clay);opacity:0.45;}}
.vrl-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px 40px;}}
.vrl-item{{display:block;text-decoration:none;}}
.vrl-item-title{{font-family:var(--serif);font-size:18px;font-weight:400;color:var(--ink);margin-bottom:8px;line-height:1.3;letter-spacing:-0.01em;transition:color 0.2s;}}
.vrl-item:hover .vrl-item-title{{color:var(--clay);}}
.vrl-item-desc{{font-size:13px;font-weight:300;color:var(--ink-70);line-height:1.6;}}
</style>
<div class="vrl-wrap">
  <div class="vrl-head">Related Reading</div>
  <div class="vrl-grid">
    <a href="vlap.html" class="vrl-item"><div class="vrl-item-title">why an instrument built for someone else keeps missing</div><div class="vrl-item-desc">The case for a language platform built on how youth actually speak.</div></a>
    <a href="dialect-bias-mental-health-screening.html" class="vrl-item"><div class="vrl-item-title">dialect bias in mental health screening</div><div class="vrl-item-desc">Where standard instruments lose signal, and what it costs the young people they lose it on.</div></a>
    <a href="technology.html" class="vrl-item"><div class="vrl-item-title">the architecture and security model</div><div class="vrl-item-desc">PHI boundaries, auditability, and the human-in-the-loop escalation design.</div></a>
    <a href="research.html" class="vrl-item"><div class="vrl-item-title">how this holds up under independent review</div><div class="vrl-item-desc">The validation process the taxonomy is being taken through.</div></a>
  </div>
</div>
<!-- /LINKS:VASL -->

<footer>
  <div class="footer-sitemap">
    <div class="fs-brand">
      <a href="index.html" class="footer-logo">Vasl <span>Health</span></a>
      <div class="footer-mission">Language is culture, not pathology.<br>Interpretation is care.<br>Delaware Public Benefit Corporation.</div>
      <a href="contact.html" class="fs-cta">Request a Demo &rarr;</a>
    </div>
    <div class="fs-col">
      <div class="fs-head">Platform</div>
      <a href="platform.html">Platform Overview</a>
      <a href="vlap.html">VLAP</a>
      <a href="ai-model.html">AI Model</a>
      <a href="technology.html">Technology</a>
      <a href="infrastructure.html">Infrastructure, Not Burden</a>
      <a href="health-systems.html">VLAP for Health Systems</a>
      <a href="peer-groups.html">Peer Groups</a>
      <a href="teletherapy.html">Teletherapy</a>
      <a href="prototype.html">Live Demo Portal</a>
      <a href="demo.html">VLAP Signal Taxonomy</a>
    </div>
    <div class="fs-col">
      <div class="fs-head">Who We Serve</div>
      <a href="for-schools.html">For Schools</a>
      <a href="for-organizations.html">For Organizations</a>
      <a href="outcomes.html">Outcomes</a>
      <a href="clinical-outcomes.html">Clinical Outcomes</a>
      <a href="pricing.html">Pricing</a>
    </div>
    <div class="fs-col">
      <div class="fs-head">Company</div>
      <a href="about.html">About Vasl</a>
      <a href="team.html">Team</a>
      <a href="careers.html">Careers</a>
      <a href="research.html">Research</a>
      <a href="blog.html">Blog &amp; Insights</a>
      <a href="contact.html">Contact</a>
      <a href="glossary.html">Glossary</a>
    </div>
    <div class="fs-col">
      <div class="fs-head">Support &amp; Legal</div>
      <a href="support.html">Help Center</a>
      <a href="for-families.html">For Families</a>
      <a href="privacy.html">Privacy Policy</a>
      <a href="terms.html">Terms of Service</a>
      <a href="baa.html">Business Associate Agreement</a>
      <a href="accessibility.html">Accessibility</a>
    </div>
    <div class="fs-col">
      <div class="fs-head">Resources</div>
      <a href="glossary.html">Glossary</a>
      <a href="school-mental-health-rfp.html">School Mental Health RFP Guide</a>
      <a href="dialect-bias-mental-health-screening.html">Dialect Bias in Screening</a>
      <a href="hedis-behavioral-health-cultural-fit.html">HEDIS &amp; Cultural Fit</a>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="footer-copy">&copy; 2026 Vasl Health, Inc. All rights reserved.</div>
    <div class="footer-legal">
      <a href="privacy.html">Privacy</a>
      <a href="terms.html">Terms</a>
      <a href="baa.html">BAA</a>
    </div>
  </div>
</footer>

<script>
  document.documentElement.classList.add('js-ready');
  const reveals = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver((entries) => {{
    entries.forEach(e => {{ if (e.isIntersecting) e.target.classList.add('visible'); }});
  }}, {{ threshold: 0.06, rootMargin: '0px 0px -24px 0px' }});
  reveals.forEach(el => io.observe(el));
  window.addEventListener('load', () => {{
    reveals.forEach((el, i) => {{
      if (el.getBoundingClientRect().top < window.innerHeight) {{
        setTimeout(() => el.classList.add('visible'), i * 55);
      }}
    }});
  }});
  function toggleNav() {{
    document.querySelector('.nav-links').classList.toggle('open');
    document.getElementById('ham-btn').classList.toggle('open');
  }}
</script>
</body>
</html>
"""

open(OUT, "w", encoding="utf-8", newline="\n").write(HTML)
print("wrote", OUT, len(HTML), "bytes")
