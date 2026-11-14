"""for-organizations: stale-claim sweep (claims only). Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/for-organizations.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    # Chapter 01 stat: "23 of 47" was counted on the retired 47-signal taxonomy -> approved result
    ("""        <div class="cs-num">23 of 47</div>
                <div class="cs-label">VLAP signals with no counterpart in the lexicon&rsquo;s 6,910 terms</div>""",
     """        <div class="cs-num">0.97</div>
                <div class="cs-label">F1 on substance use in clinical notes, n2c2 2022 SHAC test, 518 notes, against 0.83 for a keyword rule</div>""", 1),

    # Chapter 02: peer community as an offering
    ("The same platform infrastructure, peer community, culturally matched coaching,",
     "The same platform infrastructure, culturally matched coaching,", 1),
    ('<div class="svi">Peer community and coaching available within 48 hours of enrollment, no waitlist</div>',
     '<div class="svi">Coaching available within 48 hours of enrollment, no waitlist</div>', 1),
    ('<div class="svi">Early intervention through peer community and coaching, before crisis-level utilization</div>',
     '<div class="svi">Early intervention through coaching, before crisis-level utilization</div>', 1),
    ("Behavioral health capacity that scales without equivalent staffing, peer community and AI-supported coaching extend reach",
     "Behavioral health capacity that scales without equivalent staffing, AI-supported coaching extends reach", 1),
    ("Peer community and culturally matched coaching for youth who have never engaged",
     "Culturally matched coaching for youth who have never engaged", 1),
    # IRB as a Vasl claim
    ('<div class="svi">IRB study outcome data and grant documentation package for foundation and government grant applications</div>',
     '<div class="svi">Grant documentation package for foundation and government grant applications</div>', 1),

    # Chapter 03 outcomes
    (" No pilot has run, so nothing here reports pilot outcomes. The IRB study with a university research partner is building the independent clinical evidence base.</p>",
     " No pilot has run, so nothing here reports pilot outcomes.</p>", 1),
    ("""      <div class="os-label">Distinct Vocabulary</div>
          <div class="os-num">23 of 47</div>
          <div class="os-sub">VLAP signals with no counterpart in the lexicon&rsquo;s 6,910 terms</div>""",
     """      <div class="os-label">Substance Use in Clinical Notes</div>
          <div class="os-num">0.97</div>
          <div class="os-sub">F1 on the n2c2 2022 SHAC test, 518 notes, against 0.83 for a keyword rule</div>""", 1),
    ('<div class="os-sub">Peer community and a coach from the day of enrollment, against',
     '<div class="os-sub">A coach from the day of enrollment, against', 1),
    ("""      <div class="os-label">VLAP Sensitivity</div>
      <div class="os-num">90<span style="font-size:26px">%</span></div>
      <div class="os-sub">On high-distress signal detection, IRB validation in progress, results pending publication</div>""",
     """      <div class="os-label">VLAP Signals</div>
      <div class="os-num">55</div>
      <div class="os-sub">Signals across seven dimensions, each flagged with the words behind it, never a score or a diagnosis</div>""", 1),

    # Chapter 04
    ("for your specific population, peer group design, coach matching parameters,",
     "for your specific population, coach matching parameters,", 1),

    # CTA documentation: IRB and SOC 2 out, HIPAA, BAA in
    ("IRB study protocol, SOC 2 Type II report, and HIPAA technical safeguards documentation available under NDA for institutional evaluation.",
     "HIPAA technical safeguards documentation and our BAA available under NDA for institutional evaluation.", 1),

    # Related reading
    ("Daily check-ins, a peer community and a coach, for an organization without its own clinical team.",
     "Daily check-ins and a coach, for an organization without its own clinical team.", 1),
]

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:90]!r}"
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"for-organizations: {len(PAIRS)} pairs applied")
