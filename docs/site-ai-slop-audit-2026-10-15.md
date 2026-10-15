# AI-slop audit, gotovasl.com

Audit date: 2026-10-15 (UTC). Report only. No file in `site/` or `tools/` was changed.

Measured against the live site, not the repo. Crawl method: BFS over every internal
link from the apex, plus `sitemap.xml`, plus a sweep of every HTML file in
`site/` requested in both its `.html` and extensionless form, plus the linked PDF.
Every finding below was re-read in context before being recorded; the
false-positive register at the end lists what the detectors flagged and I rejected.

## Scope correction, read this first

Two things in the brief do not match the ground truth:

1. **Repo.** gotovasl.com ships from **`VASL-HEALTH/vasl-site`** (local clone
   `C:/Users/rodne/vasl-site`), not VASL-PLATFORM. This report and any rewrite
   belong there. Hosting is S3 `vasl-marketing-site` behind CloudFront
   `E11DM7B5W2KRCQ`, deployed by manual sync plus invalidation, as the brief says.
2. **Host.** `https://www.gotovasl.com` 301s to the apex `https://gotovasl.com`
   via a CloudFront function. The apex is canonical and is what was crawled.

## Summary

### The headline

**The 1,569 encoded em dashes are gone, and the live site is clean in every
encoded form.** That figure is confirmed exactly: `&mdash;` appeared 1,569 times
in `site/` at `9bb7fc1^`, the commit before PR #25 stripped them (plus 16 in
`tools/`, 564 literal `U+2014`, 111 `&ndash;`, 13 literal `U+2013`). All 51 live
pages were deployed 2026-10-13 06:36 UTC, after that fix landed on 2026-10-12.

**One real dash finding remains: the linked PDF.** `partner-package.pdf` carries
**32 literal em dashes (U+2014)** and 1 en dash. It was committed as a static
binary on 2026-09-08, predates PR #25, has no generator in `tools/`, and
`check_copy.py` does not scan PDFs. It is the only dash-bearing asset the live
site serves.

### Page count and dash census

| Measure | Count |
|---|---|
| Distinct pages on gotovasl.com | **51** (matches the 51 HTML files in `site/`) |
| Live URLs crawled (incl. `.html`/extensionless aliases, assets, PDF) | **121** |
| URLs in `sitemap.xml` | 43 (8 live pages are unlisted: `/404`, `/baa`, `/privacy`, `/terms`, `/outcomes`, `/prototype`, `/demo.html`, `/google21b71dccc4b8882d`) |
| Pages where live HTML differs from repo source | **0** (all differ by line endings only: repo CRLF, live LF) |
| Off-site page linked from the site | 1 (`/demo` 301s to `demo.gotovasl.com`) |

Dash forms counted in rendered text, `<title>`, meta description, OG/Twitter tags,
alt text, aria-labels, JSON-LD and raw page source, across all 51 pages:

| Form | Rendered text | Title/meta/OG/alt/aria/JSON-LD | Raw source | PDF |
|---|---|---|---|---|
| `—` U+2014 | 0 | 0 | 0 | **32** |
| `&mdash;` | 0 | 0 | 0 | n/a |
| `&#8212;` | 0 | 0 | 0 | n/a |
| `&#x2014;` / `&#X2014;` | 0 | 0 | 0 | n/a |
| `–` U+2013 | 0 | 0 | 0 | **1** |
| `&ndash;` | 0 | 0 | 0 | n/a |
| `&#8211;` | 0 | 0 | 0 | n/a |
| `&#x2013;` / `&#X2013;` | 0 | 0 | 0 | n/a |
| `--` as an em-dash substitute | 0 | 0 | 0 | 0 |

**En dashes used as dashes: 0.** The single en dash in the PDF is `6-9 mo` (written
with an en dash), a numeric range, which is correct typography and not a
dash-as-punctuation.

Verified twice by independent paths: a static scan of the fetched bytes, and in
Chrome by parsing all 50 sitemap-plus-extras pages through `DOMParser` and reading
`textContent` (779,220 characters of decoded text), where any encoded entity would
have decoded to a literal dash. Both returned zero.

### Findings by tell type

| Tell type | Findings | Note |
|---|---|---|
| Rhetorical colon setup | 26 | Largest category. Includes the literal `The result ...:` shape. |
| Contrast, "not X, but Y" | 20 | Mostly defensible one at a time; a tell by repetition across 14 pages. |
| Contrast, "not just / only / merely / simply" | 9 | 3 are inside attributed quotes. |
| Adjective or adverb triplet | 11 | Of 162 regex hits; the other 151 are real enumerations. |
| Em dashes in a linked PDF | 33 | 32 em + 1 en, `partner-package.pdf`. |
| Banned vocabulary | 4 | `comprehensive` x3, `journey` x1. |
| Three parallel clauses | 2 | |
| Hedge or filler phrasing | 2 | Both mild; one sits directly above its citations. |
| UI glyphs (check mark, warning sign) | 48 | Reported for completeness; recommend no change. |
| Em dashes on gotovasl.com HTML | **0** | |
| True emoji | **0** | |
| Vendor names (Anthropic/Claude/OpenAI/Bedrock) | **0** | Checked in rendered DOM, raw source, HTML comments, JS, CSS, SVG, XML and the PDF. |
| Stray markdown (`**`, `##`) | **0** | |
| Curly-quote mismatches | **0** | |
| Repeated question-style headings | **0** | No heading anywhere on the site ends in a question mark. |
| Over-precise decimals with no source | **0** | Every figure carries corpus, n, split or run ID. |
| Inflated phrasing ("stands as", "pivotal", "testament", "underscores", "plays a vital role") | **0** | |
| Filler ("It's worth noting", "In today's", "In summary", "Overall,") | **0** | |

### Findings by page

| Page | Findings |
|---|---|
| `partner-package.pdf` | 33 dashes (1 table row below) |
| `/technology` | 7 |
| `/careers` | 7 |
| `/team` | 6 |
| `/glossary` | 4 |
| `/dialect-bias-mental-health-screening` | 3 |
| `/for-schools` | 3 |
| `/peer-groups` | 3 |
| `/vlap` | 3 |
| `/about` | 2 |
| `/blog-bridging-chasm` | 2 |
| `/blog-crisis-without-solving` | 2 |
| `/blog-future-culturally-responsive` | 2 |
| `/blog-medicaid-populations` | 2 |
| `/blog-mental-health-equity-crisis` | 2 |
| `/blog-other-diagnosis` | 2 |
| `/help/vlap-technology` | 2 |
| `/hedis-behavioral-health-cultural-fit` | 2 |
| `/infrastructure` | 2 |
| `/platform` | 2 |
| `/school-mental-health-rfp` | 2 |
| `/teletherapy` | 2 |
| `/ai-model` | 1 |
| `/blog-healing-great-divide` | 1 |
| `/blog-missing-infrastructure` | 1 |
| `/clinical-outcomes` | 1 |
| `/for-organizations` | 1 |
| `/help/compliance` | 1 |
| `/help/getting-started` | 1 |
| `/support` | 1 |
| `/help/clinical` | 1 (glyphs only) |
| `/pricing` | 1 (glyphs only) |
| `/privacy` | 1 (protected, legal) |
| `/for-families`, `/health-systems`, `/contact`, `/research`, `/blog`, `/accessibility`, `/terms`, `/baa`, `/404`, `/outcomes`, `/prototype`, `/demo.html`, `/help/assessments`, `/help/billing`, `/help/technical`, `/blog/what-a-suicide-risk-word-list-cant-hear`, `/blog-human-is-the-system`, `/google21b71dccc4b8882d` | 0 |

## Findings

Rewrites are proposals only. Rows marked **PROTECTED** or **QUOTE** carry no
rewrite: see the Protected section for why.

### Em dashes

| URL | Tell type | Exact text | Proposed rewrite |
|---|---|---|---|
| `/partner-package.pdf` | em dash, 32 occurrences | p1 "Vasl reads the language youth actually use [em dash] in clinical notes, screeners, coaching, and peer community [em dash] and surfaces distress signals"; p2 "Support starts that day [em dash] not in the second quarter of next year"; p3 "Signal detail stops at the clinician boundary by design [em dash] a coach never sees a score"; p3 "Integration by HL7 FHIR R4 [em dash] Epic, Cerner, athenahealth [em dash] or flat CSV/JSON"; p4 "47 signals across six clinical categories [em dash] HOP, SHA, CCM, ISO, TRM, PFE"; p4 "Vasl's own weights on Vasl's own infrastructure [em dash] not a prompt wrapper around a general-purpose LLM"; p9 "or in Appalachian English, or any other non-standard register [em dash] is not a slightly less accurate model"; plus the 9 page-header separators "Vasl. 01 [em dash] THE GAP THIS CLOSES" through "09 [em dash]" | Regenerate the PDF from its source document with the same comma, colon and sentence-split rules PR #25 applied to the pages. 23 of the 32 are prose dashes; the other 9 are per-page section-header separators, a layout device that could become a middot or an en space instead. **The PDF source is not in this repo and has no generator in `tools/`, so this needs the originating document, not a text edit.** |
| `/partner-package.pdf` | en dash, 1 occurrence | p2 "6[en dash]9 mo Typical wait for a first therapy appointment" | None. A numeric range is correct typography. Listed for completeness. |

### Rhetorical colon setups

| URL | Tell type | Exact text | Proposed rewrite |
|---|---|---|---|
| `/technology` | colon setup | "The result is a systematic blind spot: the specific ways Black and Latino, LGBTQ+, and first-generation youth signal emotional distress are consistently missed" | "Standard models therefore miss the specific ways Black and Latino, LGBTQ+, and first-generation youth signal emotional distress." |
| `/technology` | colon setup | "The inversion is key: the date is a deadline, not a milestone." | "The date functions as a deadline rather than a milestone." |
| `/technology` | colon setup | "The joke is the test: if the listener laughs or deflects, the disclosure is abandoned." | "The joke tests the listener. If they laugh or deflect, the disclosure is abandoned." |
| `/technology` | colon setup | "The output is an interpretive context package: which signal patterns are present, their dimensional classification, and cultural interpretation notes" | "The output is an interpretive context package containing which signal patterns are present, their dimensional classification, and cultural interpretation notes." |
| `/about` | colon setup | "That realization became the mandate: build the language model that should have existed already." | "That realization set the mandate. Build the language model that should have existed already." |
| `/about` | colon setup | "The data proved what the framework promised: when the platform understands how youth actually communicate, they actually stay." | "The data matched the framework. When the platform understands how youth actually communicate, they stay." |
| `/blog-mental-health-equity-crisis` | colon setup | "The failure is structural: the tools themselves carry a bias that is invisible to the people using them" | "The failure is structural. The tools themselves carry a bias that is invisible to the people using them." |
| `/blog-mental-health-equity-crisis` | colon setup | "It has a validation gap problem: it was never tested on the populations it is now routinely used to screen." | "It has a validation gap. It was never tested on the populations it is now routinely used to screen." |
| `/blog-bridging-chasm` | colon setup | "The broader point is methodological: any mental health AI platform that makes accuracy claims without independent IRB-approved validation" | "The broader point is methodological. Any mental health AI platform that makes accuracy claims without independent IRB-approved validation ..." |
| `/dialect-bias-mental-health-screening` | colon setup | "It's quieter than that: a genuine signal reads as ambiguous, gets scored lower than it should, or gets missed entirely" | "It is quieter than that. A genuine signal reads as ambiguous, gets scored lower than it should, or gets missed entirely." |
| `/help/compliance` | colon setup | "The answer is architectural: the system is built so that individual disclosure to school administrators is structurally impossible." | "The answer is architectural. The system is built so that individual disclosure to school administrators is structurally impossible." |
| `/hedis-behavioral-health-cultural-fit` | colon setup | "The mechanism is straightforward: all four measures above depend on a member staying connected to care" | "The mechanism is straightforward. All four measures above depend on a member staying connected to care." |
| `/peer-groups` | colon setup | "The organizing principle is recognition: if a member reads the group's name and thinks \"that's me,\" they're in the right place." | "The organizing principle is recognition. If a member reads the group's name and thinks \"that's me,\" they are in the right place." |
| `/team` | colon setup | "The reason Dr. Williams matters to Vasl is this: he's a nurse-scientist who became a data expert." | "Dr. Williams matters to Vasl because he is a nurse-scientist who became a data expert." |
| `/team` | colon setup | "The evidence is clear: culturally matched care produces better outcomes." | "Culturally matched care produces better outcomes." |
| `/team` | colon setup | "At Vasl, that background translates directly: the platform operates at the intersection of healthcare regulation, community trust, institutional partnership" | "At Vasl that background translates directly, because the platform operates at the intersection of healthcare regulation, community trust and institutional partnership." |
| `/vlap` | colon setup | "That's what Vasl did: the first community-annotated corpus pairing African American Language with behavioral-health distress labels" | "Vasl built it. The first community-annotated corpus pairing African American Language with behavioral-health distress labels ..." |
| `/careers` | colon setup, twinned | "We apply the same standard internally: build on evidence, document what we don't know yet, and publish what we find." (L993) and "We apply the same principle internally: tools support the work, people make the decisions." (L1013) | Two near-identical constructions 20 lines apart on one page. Keep one, recast the other: "Internally, tools support the work and people make the decisions." |
| `/careers` | colon setup + banned word | "Onboarding is comprehensive: clinical context, platform architecture, team introductions, and the specific context you need to start contributing" | "Onboarding covers clinical context, platform architecture, team introductions and the specific context you need to start contributing." |
| `/blog-missing-infrastructure` | colon setup | "The gap is data. Specifically: a corpus pairing African American Language (AAL) with behavioral-health distress labels" | "The gap is data, specifically a corpus pairing African American Language (AAL) with behavioral-health distress labels." |
| `/blog-healing-great-divide` | colon setup | "Digital platforms have done real work here: the ability to access a check-in, a peer community, or a coaching session from a phone at 11pm" | "Digital platforms have done real work here. Reaching a check-in, a peer community or a coaching session from a phone at 11pm matters." |
| `/blog-future-culturally-responsive` | colon setup | "It is also true for clinical instruments: the PHQ-9, the most widely used depression screening tool in the United States, was validated primarily on adults" | "It is also true for clinical instruments. The PHQ-9, the most widely used depression screening tool in the United States, was validated primarily on adults." |
| `/blog-future-culturally-responsive` | colon setup | "The next step is alignment solutions: technology that is reachable by underserved communities and genuinely legible to them" | "The next step is alignment. Technology that is reachable by underserved communities and genuinely legible to them." |
| `/blog-medicaid-populations` | colon setup | "And it requires real work: understanding the billing codes, building documentation infrastructure, navigating state-by-state variation" | "And it requires real work, from understanding the billing codes to building documentation infrastructure and handling state-by-state variation." |
| `/support` | colon setup | "This distinction is intentional: clinical assessment is a clinician function, not a member-facing feature." | "This distinction is intentional. Clinical assessment is a clinician function, not a member-facing feature." |
| `/infrastructure` | colon setup | "Current perception: behavioral health platforms add layers, more data entry, more staff burden, more operational drag." | Fine if it stays visually a label. If it reads as prose: "Behavioral health platforms are assumed to add layers: more data entry, more staff burden, more operational drag." |
| `/school-mental-health-rfp` | colon setup | "One honest note: Vasl answers all ten of these, and we'd rather you evaluate us against this list than a sales deck." | "To be straight with you, Vasl answers all ten of these, and we would rather you evaluate us against this list than a sales deck." |

### Contrast constructions: "not X, but Y"

20 instances across 14 pages. Individually most are doing real corrective work;
the tell is the frequency of one shape. Recommendation: vary or absorb roughly
half, keeping the ones where the correction is the actual point.

| URL | Tell type | Exact text | Proposed rewrite |
|---|---|---|---|
| `/glossary` | not X, but Y | "not because the dialect is imprecise, but ..." | Keep. The correction is the point of the definition. |
| `/glossary` | not X, but Y | "not because need is lower, but ..." | Keep. |
| `/glossary` | not X, but Y | "not because no one was listening, but ..." | Three on one page. Recast this one: "Listening was never the problem." |
| `/peer-groups` | not X, but Y | "not because someone pushed them, but ..." | "Members arrive on their own." |
| `/peer-groups` | not X, but Y | "not because a flag was triggered, but ..." | Keep one of the two on this page, recast the other. |
| `/team` | not X, but Y | "not in research conditions, but ..." | "in live clinical conditions" |
| `/team` | not X, but Y | "not theoretically, but ..." | "in practice" |
| `/team` | not X, but Y | "not as a diversity metric, but ..." | "as a design requirement" |
| `/technology` | not X, but Y | "not web-scraped text, but ..." | "The corpus is community-annotated, not web-scraped." |
| `/ai-model` | not X, but Y | "not because of a tuning problem, but ..." | Keep. Distinguishes two causes. |
| `/blog-bridging-chasm` | not X, but Y | "not in principle, but ..." | "in practice" |
| `/blog-bridging-chasm` | not X, but Y | "not misread, but ..." | Keep. |
| `/blog-crisis-without-solving` | not X, but Y, stacked | "not general text, not adapted clinical instruments, but ..." | Double negation before the reveal. "The training data has to be the language itself." |
| `/careers` | not X, but Y | "not as a separate program, but ..." | "as part of the core work" |
| `/for-organizations` | not X, but Y | "not as a supplement to existing care, but ..." | "as part of the care pathway itself" |
| `/infrastructure` | not X, but Y | "not as an additional task, but ..." | "inside work the team already does" |
| `/platform` | not X, but Y | "not as automated alerts, but ..." | "as context a clinician reads" |
| `/school-mental-health-rfp` | not X, they're | "not an afterthought to the pitch, they're ..." | "These are the terms of the engagement." |
| `/teletherapy` | not X, but Y | "not a summary, but ..." | Keep. |
| `/team` | not X, but Y | "not because the signals weren't there, but because they weren't culturally legible" | **QUOTE.** Attributed first-person founder quote. Your words, your call. |

### Contrast constructions: "not just / only / merely / simply"

| URL | Tell type | Exact text | Proposed rewrite |
|---|---|---|---|
| `/blog-medicaid-populations` | not just | "Why cultural and linguistic fit, not just access, is what actually drives retention." | "Why cultural and linguistic fit, more than access, is what actually drives retention." |
| `/blog-other-diagnosis` | not simply X, it is Y | "The clinical standard ... is not simply to administer standard instruments and adjust for cultural context as an afterthought. It is to build ..." | "The clinical standard is to build the cultural context in from the start, rather than adjust for it afterwards." |
| `/careers` | don't just | "Different perspectives don't just make us stronger, for Vasl specifically, they make the product better." | "For Vasl specifically, different perspectives make the product better." |
| `/hedis-behavioral-health-cultural-fit` | isn't only | "SSD is a useful reminder that engagement isn't only about the behavioral health visit itself." | "SSD is a useful reminder that engagement extends past the behavioral health visit itself." |
| `/for-schools` | not merely | "The platform is architected so that FERPA disclosure is structurally impossible, not merely policy-prohibited." | Keep the distinction, drop the shape: "FERPA disclosure is structurally impossible rather than policy-prohibited." |
| `/help/vlap-technology` | not merely | "the actions below are structurally impossible, not merely prohibited by guidelines" | Same construction as the `/for-schools` line above, on a second page. Recast one: "structurally impossible rather than prohibited by guidelines." |
| `/blog-bridging-chasm` | not just | "The problem is not just missing vocabulary. It is missing the cultural framework that determines what words mean in context." | **QUOTE.** Attributed to Rodney Bell, Founder and CEO. Your words, your call. |
| `/careers` | aren't just | "Our differences aren't just welcomed. They're essential to our success." | **QUOTE.** Attributed founder quote. Your words, your call. |
| `/teletherapy` | not just | "This type of clinician understands that for many youth, grief is not just personal loss. It is also the loss of a home, a language, a version of themselves that did not have to hold two worlds at once." | Unattributed illustrative quote. If it is not a real person's words: "... grief includes the loss of a home, a language, a version of themselves that did not have to hold two worlds at once." |

### Triplets

11 rhetorical triplets, out of 162 raw "X, Y, and Z" matches. The other 151 are
genuine enumerations (populations served, the SOC 2 criteria, named statutes,
benefits lists) and are listed in the false-positive register.

| URL | Tell type | Exact text | Proposed rewrite |
|---|---|---|---|
| `/blog-crisis-without-solving` | adjective triplet + banned word | "The data are comprehensive, consistent, and deeply alarming." | "The data are consistent and alarming." |
| `/careers` | adjective triplet, doubled | "The benefits below are real, competitive, and designed around sustainable work on a hard problem. No foosball tables. No vague \"unlimited PTO\" that no one actually uses. Specific, documented, and yours from day one." | Two triplets in one short paragraph. "The benefits below are real and designed around sustainable work on a hard problem. No foosball tables. No vague \"unlimited PTO\" that no one actually uses. Specific and yours from day one." |
| `/dialect-bias-mental-health-screening` | adjective triplet | "differential item functioning and dialect bias are documented, real, and consequential problems in how distress gets measured" | "differential item functioning and dialect bias are documented and consequential problems in how distress gets measured" |
| `/vlap` | adverb triplet + clause run | "ready to meet youth where they are, linguistically, culturally, and clinically. Access is by application. Deployment is supported. Community alignment is required." | "ready to meet youth where they are, in language and in clinical practice. Access is by application, deployment is supported, and community alignment is required." |
| `/peer-groups` | adjective triplet | "Response is human, direct, and without delay." | "A person responds, without delay." |
| `/platform` | adjective triplet | "Peer group infrastructure, moderated, measured, and org-aligned." | "Peer group infrastructure, moderated and org-aligned." |
| `/help/getting-started` | adjective triplet | "The coaching relationship is ongoing, text-based, and proactive." | "Coaching is ongoing and text-based. Your coach reaches out first." |
| `/school-mental-health-rfp` | adjective triplet | "drawn from RFPs that are real, dated, and public" | "drawn from real RFPs, dated and public" |
| `/careers` | adjective triplet | "We apply the same standards we hold the platform to, evidence-based, documented, and open to correction when we get it wrong." | "We hold ourselves to the platform's standard: documented, and open to correction when we get it wrong." |
| `/blog-other-diagnosis` | adjective triplet | "a young person whose distress is real, significant, and shaped in ways the assessment instrument was not built to see" | "a young person whose distress is real and shaped in ways the assessment instrument was not built to see" |
| `/vlap` | adjective triplet | "its language is subtle, coded, and frequently read as attitude rather than distress" | "its language is coded, and frequently read as attitude rather than distress" |

### Three parallel clauses

| URL | Tell type | Exact text | Proposed rewrite |
|---|---|---|---|
| `/team` | three parallel clauses | "Vasl Health exists because the need is urgent, the gap is structural, and young people deserve a mental-health system that finally understands them." | "Vasl Health exists because the gap is structural and young people deserve a mental-health system that understands them." |
| `/for-schools` | three parallel clauses | "At a cost that Title I districts can sustain, with compliance your legal team can sign off on, and with outcomes your board can present" | Defensible: each clause names a different stakeholder. Keep, or drop to two. |

### Banned vocabulary

| URL | Tell type | Exact text | Proposed rewrite |
|---|---|---|---|
| `/blog-crisis-without-solving` | banned: comprehensive | "The data are comprehensive, consistent, and deeply alarming." | Covered by the triplet row above: "The data are consistent and alarming." |
| `/careers` | banned: comprehensive | "Onboarding is comprehensive: clinical context, platform architecture ..." | Covered by the colon-setup row above. |
| `/privacy` | banned: comprehensive | "Vasl Health implements comprehensive technical and administrative safeguards to protect your information." | **PROTECTED, legal page.** Reported only. "comprehensive safeguards" is also a claim, so changing it is a legal review question, not a copy question. |
| `/team` | banned: journey | "Vasl is the culmination of that journey, a platform built with and for the communities that shaped me." | **QUOTE.** Inside a long first-person founder quote. Your words, your call. |

### Hedge and filler phrasing

| URL | Tell type | Exact text | Proposed rewrite |
|---|---|---|---|
| `/dialect-bias-mental-health-screening` | hedge, unattributed | "Emerging evidence suggests that models built directly on the language of the population being screened can narrow ..." | Low severity: the page carries numbered references two lines below (DIF of the PHQ-9 in *Journal of Affective Disorders*; Straw and Callison-Burch, *PLOS ONE*). Name the source inline: "Straw and Callison-Burch report that models built directly on ..." |
| `/dialect-bias-mental-health-screening` | filler variant | "It's worth being precise about the limits here." | A variant of "It's worth noting". It does introduce a real limitation, so: "The limits here are worth stating precisely." |

### UI glyphs, reported for completeness

| URL | Tell type | Exact text | Proposed rewrite |
|---|---|---|---|
| `/pricing` | glyph, check mark x38 | U+2713 in the plan comparison table cells | None. U+2713 CHECK MARK is a dingbat with no emoji presentation, and a comparison table is its conventional use. Not slop. |
| `/help/clinical` | glyph, warning sign x2 + check mark x1 | `<div class="ii-icon">` warning sign `</div>` | None recommended. U+26A0 does render with emoji presentation on some platforms, so if you want zero emoji-rendering risk, swap these three for inline SVG. Cosmetic, your call. |
| 7 `/help/*` pages | glyph, check mark | `onclick="this.textContent='Thanks [check mark]'"` in the article-feedback button | None. Same reasoning. |

## Protected: reported, not rewritten

Per the brief, no rewrite is proposed for numbers, claims, VLAP terms, the CDS
verbs, or legal pages. Specifically:

- **`0.8255` vs `0.6489`** appear 47 and 44 times. Untouched, and every instance
  carries its method ("Chunk level, n_pos 307, held-out test split, same treatment
  for all three").
- **`elevated` / `elevates`, 18 instances.** This is the four-tier name ("low,
  moderate, elevated, acute") and the rules-engine verb ("elevates co-occurring
  HOP/SHA signals"). It is on the brief's banned list and it is also the correct
  term. No change. **Do not add `elevate` to the guard's word list for that
  reason.**
- **`surfaces` / `surfacing tier`, "Vasl Language Analysis Platform"**: VLAP
  terminology, untouched.
- **Legal pages** `/privacy`, `/terms`, `/baa`, `/accessibility`: scanned. The
  only hits are 1 banned word (above) and standard boilerplate triplets
  ("accurate, current, and complete"). Reported, no rewrites.
- One claims-level observation, outside copy scope but worth your eye:
  `/clinical-outcomes` publishes `0.8088` and `0.5074` attributed to "Run
  VLAP-SHA-REAL-001, pre-registered before any model was fit". Confirm that
  publishing those figures is intended, given how that run is classified
  internally. I have not changed or recommended changing anything about them.

## What the guard catches that the live site still shows

`python tools/check_copy.py` exits **0**, clean, over 64 files, 10 dash forms and
22 slop words. So: **nothing.** There is no case where the guard fires and the live
site is still dirty. The gap runs the other way, and there are six of them.

1. **PDFs are invisible to it.** `targets()` yields only `.html`, `.xml` and
   `.txt` under `site/`, plus `tools/*.py`. The 33 dashes in
   `site/partner-package.pdf` are the only dashes the live site serves, and the
   guard cannot see them. **This is the one gap that matters today.**
2. **Nothing runs it.** `core.hooksPath` is unset and `.git/hooks/` holds only
   samples, so no pre-push hook is installed. The docstring says "Run by hand
   before a push" and is deliberately not a CI job. It is a script someone has to
   remember, not a guard.
3. **It scans the repo, not the live site.** A stale deploy would pass it. Not a
   live problem right now: all 51 pages match the repo byte for byte apart from
   line endings, and all carry the 2026-10-13 06:36 UTC deploy.
4. **Six words from the brief's banned list are missing** from `SLOP`: `journey`,
   `harness`, `foster`, `elevate`, `comprehensive`, `realm`. Of these, only
   `journey` and `comprehensive` found anything, and `elevate` and `foster` must
   stay out (clinical tier name; "foster care").
5. **Narrow filler match.** `SLOP` has `in today's world` but not bare
   `in today's`, and has neither `in summary`, `overall`, `stands as`,
   `plays a vital role`, `studies show` nor `experts say`. All are currently
   absent from the site, so this is a future-proofing gap, not a live miss.
6. **No structural coverage at all.** It is a word and dash matcher. The four
   largest categories in this report (colon setups, "not X but Y", triplets,
   parallel clauses) are invisible to it, as are emoji, stray markdown and
   curly-quote balance.

## Adjacent surface, out of the stated scope

`/demo` is not a page. It 301s to **`https://demo.gotovasl.com/`**, titled
`VASL-VLAP-TAX-001`, which is the VLAP taxonomy demonstrator from a different
repo on a different host and a different deploy path. It is linked from the
marketing site, and it carries **1 literal em dash and 2 `&ndash;` entities**.
An S3 sync of `vasl-site` will not fix it. Flagging it because the brief asked
for every page reachable from the site; it needs its own session.

Separately, `/demo.html` in this repo is a 3.5 KB "This page has moved" stub, as
is `/prototype`. Both are live and both are clean.

## False-positive register

What the detectors flagged and I rejected after reading context. Recorded so the
next pass does not re-raise them.

| Flag | Count | Why it is not a finding |
|---|---|---|
| banned: `elevate` | 18 | VLAP tier name and rules-engine verb. Protected. |
| banned: `landscape` | 4 | All screen orientation ("tablet in landscape", "Landscape orientation recommended"). The guard already exempts these. |
| banned: `navigate` | 4 | "navigated" in the ordinary human sense; 3 are in bios or quotes. |
| banned: `foster` | 1 | "foster care", the literal child-welfare term. |
| banned: `unlock` | 1 | "no feature unlocks", a literal pricing/gating term. |
| banned: `comprehensive` | 1 of 4 | "comprehensive psychological assessment" on `/team` is a standard clinical term of art. |
| over-precise decimals | 9 | `164.524`, `164.526`, `164.528`, `164.502`, `164.308`, `164.410`, `164.402`, `164.514`, `160.103` are 45 CFR citations on `/baa`, not decimals. |
| over-precise decimals | 1 | `10.1037` is a DOI prefix. |
| over-precise decimals | 82 | Model metrics, every one carrying corpus, n, split or run ID beside it. |
| emoji | 41 | U+2713 check marks and U+26A0 warning signs used as UI icons. Reported as glyphs instead. |
| triplets | 151 | Real enumerations: "Black, Latino, and LGBTQ+" (the populations served, ~25x), "security, availability, and confidentiality" (the SOC 2 criteria, 7x), "MTSS, FERPA, and HIPAA", "Title IV-A, ESSER, and grants", "health, dental, and vision", "grammar, phonology, and vocabulary". |
| filler: `overall` | 3 | "overall signal weight", "overall distress classification", "overall trends". Adjective, not the filler "Overall,". |
| colon setups | 67 of 93 | Label-and-value constructions, not rhetorical setups: "VLAP reads:", "Standard NLP:", "Week 1 to 2:", "Includes:", citation subtitles, "Left column:". |
| identical-rhythm paragraph runs | 3 | `/` is five member-voice sample quotes, `/support` is six support-category cards, `/terms` is three contact lines. All parallel by design. |

## Method notes and corrections made during the audit

Recorded because each one changed a number, and the first three would have put a
wrong figure in this report.

1. A first repo-vs-live sweep passed Python a Git Bash path (`/c/Users/...`),
   which Python resolved to a nonexistent `C:\c\Users\...`. `rglob` silently
   matched zero files, so the sweep "found" only 2 missing URLs. Rerun with
   `C:/Users/...`, it found 39.
2. `pdftotext` renders this PDF's em dashes as ASCII `--` and its middots as
   `U+FFFD`. On that output I would have reported "32 double hyphens, zero em
   dashes". `pypdf` decodes the same file as 32 `U+2014` and 1 `U+2013`. The
   `pypdf` reading is the correct one and is what this report uses.
3. `HEAD /demo` returns 301 while the crawler, following redirects, recorded a
   200 with 65 KB of body. Read as a same-bucket page, that looked like a live
   page diverging from the repo. It is an off-site redirect.
4. The emoji detector's range matched U+2713 and U+26A0. Both are dingbats used
   as UI icons, not emoji slop, so they are reported as glyphs with no rewrite
   rather than counted as emoji.
5. The decimal detector matched the 45 CFR citations on `/baa` and a DOI prefix.
   Not decimals.
6. Five crawl URLs returned status 0: `href` values with unencoded spaces in the
   query string (`/contact?subject=Starter Pilot`). They resolve to `/contact`,
   which was crawled, so no page was missed. The unencoded space is a small
   markup bug, not an AI tell, and is out of scope here.
7. JS text injection was checked before trusting a static crawl: 36 sites across
   the site write text via `textContent` or `innerHTML`. All are UI microcopy
   ("Sending...", "You're subscribed.", "Thanks"). No dashes, no tells. The
   static crawl is therefore a faithful read of the rendered text.
8. The clause-triplet detector is conservative and found 1 of the 2 instances
   reported; the `/team` one was found by reading. Treat that category as
   reviewed by eye, not exhaustively by regex.

## Appendix: every URL crawled

121 URLs. Extensionless and `.html` forms both serve and both were fetched; they
are byte-identical to each other.

| URL | Status | Bytes | Type |
|---|---|---|---|
| `/` | 200 | 80955 | html |
| `/404` | 200 | 4123 | html |
| `/404.html` | 200 | 4123 | html |
| `/about` | 200 | 58274 | html |
| `/about.html` | 200 | 58274 | html |
| `/accessibility` | 200 | 18487 | html |
| `/accessibility.html` | 200 | 18487 | html |
| `/ai-model` | 200 | 96750 | html |
| `/ai-model.html` | 200 | 96750 | html |
| `/apple-touch-icon.png` | 200 | 1580 | image/png |
| `/assets/favicon.svg` | 200 | 341 | image/svg+xml |
| `/assets/logo-lockup-dark.svg` | 200 | 7366 | image/svg+xml |
| `/assets/logo-lockup.svg` | 200 | 7366 | image/svg+xml |
| `/assets/mark-v-tile.svg` | 200 | 349 | image/svg+xml |
| `/baa` | 200 | 33887 | html |
| `/baa.html` | 200 | 33887 | html |
| `/blog` | 200 | 38831 | html |
| `/blog-bridging-chasm` | 200 | 30882 | html |
| `/blog-bridging-chasm.html` | 200 | 30882 | html |
| `/blog-crisis-without-solving` | 200 | 30154 | html |
| `/blog-crisis-without-solving.html` | 200 | 30154 | html |
| `/blog-future-culturally-responsive` | 200 | 29120 | html |
| `/blog-future-culturally-responsive.html` | 200 | 29120 | html |
| `/blog-healing-great-divide` | 200 | 29039 | html |
| `/blog-healing-great-divide.html` | 200 | 29039 | html |
| `/blog-human-is-the-system` | 200 | 37711 | html |
| `/blog-human-is-the-system.html` | 200 | 37711 | html |
| `/blog-medicaid-populations` | 200 | 30570 | html |
| `/blog-medicaid-populations.html` | 200 | 30570 | html |
| `/blog-mental-health-equity-crisis` | 200 | 31462 | html |
| `/blog-mental-health-equity-crisis.html` | 200 | 31462 | html |
| `/blog-missing-infrastructure` | 200 | 27670 | html |
| `/blog-missing-infrastructure.html` | 200 | 27670 | html |
| `/blog-other-diagnosis` | 200 | 29593 | html |
| `/blog-other-diagnosis.html` | 200 | 29593 | html |
| `/blog.html` | 200 | 38831 | html |
| `/blog/what-a-suicide-risk-word-list-cant-hear` | 200 | 36790 | html |
| `/blog/what-a-suicide-risk-word-list-cant-hear.html` | 200 | 36790 | html |
| `/careers` | 200 | 70740 | html |
| `/careers.html` | 200 | 70740 | html |
| `/clinical-outcomes` | 200 | 37651 | html |
| `/clinical-outcomes.html` | 200 | 37651 | html |
| `/contact` | 200 | 38930 | html |
| `/contact.html` | 200 | 38930 | html |
| `/contact?ref=partner-package` | 200 | 38930 | html |
| `/contact?subject=Enterprise` | 200 | 38930 | html |
| `/contact?subject=Health System Pilot` | 0 | 0 | err:URL can't contain control  |
| `/contact?subject=Pro Plan` | 0 | 0 | err:URL can't contain control  |
| `/contact?subject=School Pilot Request` | 0 | 0 | err:URL can't contain control  |
| `/contact?subject=Starter Pilot` | 0 | 0 | err:URL can't contain control  |
| `/contact?subject=VLAP Technical Spec Request` | 0 | 0 | err:URL can't contain control  |
| `/demo` | 200 | 65543 | html |
| `/demo.html` | 200 | 3489 | html |
| `/dialect-bias-mental-health-screening` | 200 | 26942 | html |
| `/dialect-bias-mental-health-screening.html` | 200 | 26942 | html |
| `/favicon.ico` | 200 | 966 | image/x-icon |
| `/favicon.svg` | 200 | 302 | image/svg+xml |
| `/for-families` | 200 | 16967 | html |
| `/for-families.html` | 200 | 16967 | html |
| `/for-organizations` | 200 | 45665 | html |
| `/for-organizations.html` | 200 | 45665 | html |
| `/for-schools` | 200 | 92326 | html |
| `/for-schools.html` | 200 | 92326 | html |
| `/glossary` | 200 | 56452 | html |
| `/glossary.html` | 200 | 56452 | html |
| `/google21b71dccc4b8882d` | 200 | 53 | html |
| `/google21b71dccc4b8882d.html` | 200 | 53 | html |
| `/health-systems` | 200 | 25474 | html |
| `/health-systems.html` | 200 | 25474 | html |
| `/hedis-behavioral-health-cultural-fit` | 200 | 27474 | html |
| `/hedis-behavioral-health-cultural-fit.html` | 200 | 27474 | html |
| `/help/assessments` | 200 | 31318 | html |
| `/help/assessments.html` | 200 | 31318 | html |
| `/help/billing` | 200 | 35381 | html |
| `/help/billing.html` | 200 | 35381 | html |
| `/help/clinical` | 200 | 50708 | html |
| `/help/clinical.html` | 200 | 50708 | html |
| `/help/compliance` | 200 | 47173 | html |
| `/help/compliance.html` | 200 | 47173 | html |
| `/help/getting-started` | 200 | 45124 | html |
| `/help/getting-started.html` | 200 | 45124 | html |
| `/help/technical` | 200 | 32154 | html |
| `/help/technical.html` | 200 | 32154 | html |
| `/help/vlap-technology` | 200 | 46056 | html |
| `/help/vlap-technology.html` | 200 | 46056 | html |
| `/index` | 200 | 80955 | html |
| `/index.html` | 200 | 80955 | html |
| `/infrastructure` | 200 | 29861 | html |
| `/infrastructure.html` | 200 | 29861 | html |
| `/og-image.png` | 200 | 48118 | image/png |
| `/outcomes` | 200 | 1332 | html |
| `/outcomes.html` | 200 | 1332 | html |
| `/partner-package.pdf` | 200 | 238951 | application/pdf |
| `/peer-groups` | 200 | 63327 | html |
| `/peer-groups.html` | 200 | 63327 | html |
| `/platform` | 200 | 71122 | html |
| `/platform.html` | 200 | 71122 | html |
| `/pricing` | 200 | 49225 | html |
| `/pricing.html` | 200 | 49225 | html |
| `/privacy` | 200 | 30187 | html |
| `/privacy.html` | 200 | 30187 | html |
| `/prototype` | 200 | 3316 | html |
| `/prototype.html` | 200 | 3316 | html |
| `/research` | 200 | 44367 | html |
| `/research.html` | 200 | 44367 | html |
| `/robots.txt` | 200 | 562 | text/plain |
| `/school-mental-health-rfp` | 200 | 28035 | html |
| `/school-mental-health-rfp.html` | 200 | 28035 | html |
| `/sitemap.xml` | 200 | 7406 | text/xml |
| `/support` | 200 | 57543 | html |
| `/support.html` | 200 | 57543 | html |
| `/team` | 200 | 57891 | html |
| `/team.html` | 200 | 57891 | html |
| `/technology` | 200 | 146954 | html |
| `/technology.html` | 200 | 146954 | html |
| `/teletherapy` | 200 | 76557 | html |
| `/teletherapy.html` | 200 | 76557 | html |
| `/terms` | 200 | 30332 | html |
| `/terms.html` | 200 | 30332 | html |
| `/vlap` | 200 | 75204 | html |
| `/vlap.html` | 200 | 75204 | html |
Status 0 rows are the five unencoded-space query strings described in method
note 6; they resolve to `/contact`.
