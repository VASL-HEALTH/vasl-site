"""for-schools: stale-claim sweep (claims only). Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/for-schools.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # meta, og, twitter
    ("A tiered program for K-12 districts, peer support through a warm handoff to licensed care,",
     "A tiered program for K-12 districts, coaching through a warm handoff to licensed care,", 3),
    # nav menu line (desktop + phone sheet)
    ("Daily check-ins, peer support and coaching for K-12 districts.",
     "Daily check-ins and coaching for K-12 districts.", 2),

    # Chapter 02
    ("Vasl operates in the space before that. Peer community from day one. Proactive coaching before the crisis.",
     "Vasl operates in the space before that. Proactive coaching before the crisis.", 1),
    ("Every enrolled student gets peer community and a coach from day one,",
     "Every enrolled student gets a coach from day one,", 1),
    ("<strong>Day one.</strong> Peer group access and coach assignment begin at enrollment, no intake form.",
     "<strong>Day one.</strong> Coach assignment begins at enrollment, no intake form.", 1),
    ("VLAP reads AAVE, queer vernacular, and coded youth language. Peer groups organized around shared cultural experience.</span>",
     "VLAP reads AAVE, queer vernacular, and coded youth language.</span>", 1),
    ("80% of member needs resolved at peer/coach tier.", "80% of member needs resolved at the coach tier.", 1),

    # Chapter 03
    ("the early-stage distress, the peer connection needs, the proactive outreach,",
     "the early-stage distress, the proactive outreach,", 1),
    ("They can't run peer support groups and manage crisis response",
     "They can't run proactive outreach and manage crisis response", 1),
    ("things a peer support platform could handle", "things a support platform could handle", 1),
    ('<div class="cf-title">Early-stage peer support and community connection</div>',
     '<div class="cf-title">Early-stage support and connection</div>', 1),
    ("Vasl's peer groups and coaching handle the first tier of student need,",
     "Vasl's coaching handles the first tier of student need,", 1),
    ("Your counselor receives students who've already found community, not students in cold isolation.",
     "Your counselor receives students who already have support, not students in cold isolation.", 1),
    ("The Client Org Portal gives your counseling director aggregate signal trend data",
     "Vasl gives your counseling director aggregate signal trend data", 1),

    # Chapter 04 billing
    ("Each certified coaching session and structured peer support facilitation is documented",
     "Each certified coaching session is documented", 1),

    # Chapter 05 student moments: testimonial quote kept, peer-group claims removed
    ("the peer group is often the only affirming space in the school day. Vasl's peer groups are explicitly identity-affirming, organized around shared experience, moderated by trained human moderators, and private from school administration.",
     "an affirming space is often missing from the school day. Vasl's coaching is explicitly identity-affirming and private from school administration.", 1),
    ('<div class="sm-outcome">Active in peer group &middot; Coach relationship established</div>',
     '<div class="sm-outcome">Coach relationship established</div>', 1),
    ("""        <div class="se-step-title">Peer groups, immediately available</div>
        <p class="se-step-body">70+ groups organized around shared identities and experiences. The student finds a group that feels like them, not a clinical category. First-gen stress. Queer identity. Grief. Racial trauma. Community before clinical care.</p>""",
     """        <div class="se-step-title">Check-ins, immediately available</div>
        <p class="se-step-body">The student can check in from the first day, in their own words, not a clinical category. Nothing to fill out first.</p>""", 1),

    # Chapter 06 access table: peer group row removed cleanly
    ("""    <div class="st-row">
      <div class="st-cell">Peer group content</div>
      <div class="st-cell"><span class="st-yes">Sees their groups</span></div>
      <div class="st-cell"><span class="st-no">Not visible to coaches</span></div>
      <div class="st-cell"><span class="st-no">Not visible to clinicians</span></div>
      <div class="st-cell"><span class="st-no">Never</span></div>
    </div>
""", "", 1),
    # SOC 2 out
    (" Session records retained for HIPAA-required duration. Annual SOC 2 Type II audit. All staff",
     " Session records retained for HIPAA-required duration. All staff", 1),
    # portals as current products
    ("accessibility standards across all portals, Member App, Coach Portal, and Client Org Portal.",
     "accessibility standards across the platform.", 1),
    ("It does not monitor peer group posts, social media, school email,",
     "It does not monitor social media, school email,", 1),
    ("aggregate, de-identified population trend data through the Client Org Portal.",
     "aggregate, de-identified population trend data.", 1),

    # Chapter 07 deployment
    ("Student focus groups to co-design the peer group ecosystem. Group names, community norms, and moderator selection, done with students, not for them.",
     "Student focus groups to shape how check-ins and coaching are introduced, done with students, not for them.", 1),
    ("Coach matching, peer group launch, first check-ins.", "Coach matching, first check-ins.", 1),

    # Chapter 08 outcomes: "23 of 47" was counted on the retired 47-signal taxonomy -> approved result
    ("""    <div class="or-big">23<span class="or-unit"> of 47</span></div>
    <div>
      <div class="or-title">VLAP signals with no counterpart in the field&rsquo;s published lexicon.</div>
      <p class="or-body">In 2026 MIT&rsquo;s McGovern Institute, the Child Mind Institute and Crisis Text Line released the Suicide Risk Lexicon, 50 constructs, 6,910 terms, built from roughly 16,000 real crisis conversations. We compared it against our 47 signals term by term. Twenty-three have no counterpart anywhere in those 6,910 terms, across five of our six dimensions. Among them the signals for <em>unaliving</em> and <em>catching a fade</em>. The claim is narrow and checkable by anyone who downloads their file: the specific vernacular is absent.</p>
    </div>
    <div>
      <div class="or-bench-label">Benchmark Context</div>
      <div class="or-bench-item"><span class="orbi-label">Suicide Risk Lexicon</span>50 constructs &middot; 6,910 terms, openly released, clinician-validated</div>
      <div class="or-bench-item"><span class="orbi-label">Overlap</span>24 of 47 VLAP signals share at least one string with it</div>
      <div class="or-bench-item"><span class="orbi-label">What we do not claim</span>Whether a construct and a signal measure the same thing is a clinical mapping question we have not done</div>
    </div>""",
     """    <div class="or-big">0.97</div>
    <div>
      <div class="or-title">Substance use in clinical notes, scored on a public benchmark.</div>
      <p class="or-body">VLAP reads 55 signals across seven dimensions. On substance use it scores 0.97 F1 on the n2c2 2022 SHAC test, 518 notes labeled by human annotators, against 0.83 for a keyword rule.</p>
    </div>
    <div>
      <div class="or-bench-label">Benchmark Context</div>
      <div class="or-bench-item"><span class="orbi-label">VLAP</span>0.97 F1</div>
      <div class="or-bench-item"><span class="orbi-label">Keyword rule</span>0.83 F1</div>
      <div class="or-bench-item"><span class="orbi-label">Test set</span>n2c2 2022 SHAC, 518 notes</div>
    </div>""", 1),
    ('<div class="or-title">Peer groups and a coach from the day of enrollment, versus 9 months nationally.</div>',
     '<div class="or-title">A coach from the day of enrollment, versus 9 months nationally.</div>', 1),
    ("Peer group access and coach assignment begin at enrollment, not after an intake form and a waitlist. For many students the first meaningful exchange is same-day: a peer group post, a coach response, a check-in that goes somewhere.",
     "Coach assignment begins at enrollment, not after an intake form and a waitlist. For many students the first meaningful exchange is same-day: a coach response, a check-in that goes somewhere.", 1),
    ('<span class="orbi-label">Vasl</span>Peer group access and coach assignment at enrollment</div>',
     '<span class="orbi-label">Vasl</span>Coach assignment at enrollment</div>', 1),
    ("is met at the peer community or coaching tier, and only what needs a clinician reaches one.",
     "is met at the coaching tier, and only what needs a clinician reaches one.", 1),
    ('<div class="or-bench-label">The Three Tiers</div>\n      <div class="or-bench-item"><span class="orbi-label">Peer tier</span>Moderated peer community, open at enrollment</div>\n',
     '<div class="or-bench-label">The Tiers</div>\n', 1),

    # Chapter 09 pilot
    ('<div class="pi-title">Student community alignment, groups built by students</div>',
     '<div class="pi-title">Student community alignment, built with students</div>', 1),
    ("Before launch, we facilitate student focus groups to identify the peer group categories that reflect your specific student community's lived experiences. The groups are theirs, not a default library imposed on them.",
     "Before launch, we facilitate student focus groups so the program reflects your specific student community's lived experiences. It is theirs, not a default imposed on them.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"for-schools: {len(PAIRS)} pairs applied")
