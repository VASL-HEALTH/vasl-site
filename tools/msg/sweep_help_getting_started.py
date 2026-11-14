"""Stale-claim sweep: help/getting-started. Exact old/new pairs, each asserted."""
import sys
from pathlib import Path

P = Path(sys.argv[1] if len(sys.argv) > 1 else "site/help/getting-started.html")
s = P.read_text(encoding="utf-8")

PAIRS = [
    ("how your coach connects with you, how peer groups work, and what to expect", "how your coach connects with you, and what to expect", 3),
    ("""      <li class="toc-item"><a href="#peer-groups" class="toc-link">Peer Groups</a></li>\n""", "", 1),
    ("a certified coach who knows your background, peer groups made up of people who share your experience, and licensed clinical support",
     "a certified coach who knows your background and licensed clinical support", 1),
    ("Your coach is matched to your community. Your peer groups are organized around shared lived experience. The language",
     "Your coach is matched to your community. The language", 1),
    ("""        <div class="callout-label">Therapy Last, Not Therapy Never</div>
        <p class="callout-text">Vasl is built on the belief that community and coaching can address most of what people are carrying, before therapy is needed. You start with peer groups and a coach. If""",
     """        <div class="callout-label">Clinical Care When You&rsquo;re Ready</div>
        <p class="callout-text">You start with a coach. If""", 1),
    ("Vasl has three layers of support.", "Vasl has two layers of support.", 1),
    ("""        <div class="step-item">
          <div class="step-num">01</div>
          <div class="step-right">
            <div class="step-title">Peer Community</div>
            <p class="step-body">Peer groups organized around shared identity and lived experience, first-generation stress, cultural identity, LGBTQ+ community, grief, anxiety, and more. Real people who share something with you. Human-moderated. Available the day you enroll.</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-num">02</div>
          <div class="step-right">
            <div class="step-title">Certified Coach</div>""",
     """        <div class="step-item">
          <div class="step-num">01</div>
          <div class="step-right">
            <div class="step-title">Certified Coach</div>""", 1),
    ("""          <div class="step-num">03</div>
          <div class="step-right">
            <div class="step-title">Licensed Clinical Support, When You're Ready</div>""",
     """          <div class="step-num">02</div>
          <div class="step-right">
            <div class="step-title">Licensed Clinical Support, When You're Ready</div>""", 1),
    ("to match you with the right coach and peer groups.", "to match you with the right coach.", 1),
    ("You're in, peer groups and your coach available immediately", "You're in, your coach reaches out", 1),
    ("Once your profile is set up, peer groups are available right away. Your coach will reach out", "Once your profile is set up, your coach will reach out", 1),
]

# Whole peer-groups section and the privacy-table row: removed by slicing, with exact anchors asserted.
SEC_START = "    <!-- PEER GROUPS -->\n"
SEC_END = "    <!-- YOUR COACH -->\n"
ROW = """        <div class="pt-row">
          <div class="pt-cell">Peer group posts</div>
          <div class="pt-cell"><span class="pt-own">Groups you joined</span></div>
          <div class="pt-cell"><span class="pt-no">Not visible</span></div>
          <div class="pt-cell"><span class="pt-no">Not visible</span></div>
          <div class="pt-cell"><span class="pt-no">Never</span></div>
        </div>\n"""
FIRST_STEPS_OLD = """          <div class="step-num">01</div>
          <div class="step-right">
            <div class="step-title">Browse the peer groups and find one that feels right</div>
            <p class="step-body">You don't have to post right away. Just read, get a feel for the community, and join the group that resonates. Many members start here before anything else.</p>
          </div>
        </div>
        <div class="step-item">
          <div class="step-num">02</div>
          <div class="step-right">
            <div class="step-title">Wait for your coach"""
FIRST_STEPS_NEW = """          <div class="step-num">01</div>
          <div class="step-right">
            <div class="step-title">Wait for your coach"""

for old, new, n in PAIRS:
    c = s.count(old)
    assert c == n, f"expected {n}, found {c}: {old[:80]!r}"
    s = s.replace(old, new)

assert s.count(SEC_START) == 1 and s.count(SEC_END) == 1
a, b = s.index(SEC_START), s.index(SEC_END)
assert a < b and "peer-groups" in s[a:b]
s = s[:a] + s[b:]
assert s.count(ROW) == 1
s = s.replace(ROW, "")
assert s.count(FIRST_STEPS_OLD) == 1
s = s.replace(FIRST_STEPS_OLD, FIRST_STEPS_NEW)
for old, new in [("""<div class="step-num">03</div>
          <div class="step-right">
            <div class="step-title">Try a daily check-in""", """<div class="step-num">02</div>
          <div class="step-right">
            <div class="step-title">Try a daily check-in"""),
                 ("""<div class="step-num">04</div>
          <div class="step-right">
            <div class="step-title">If something isn't working, tell us""", """<div class="step-num">03</div>
          <div class="step-right">
            <div class="step-title">If something isn't working, tell us"""),
                 ("Ask for a rematch. Peer group isn't what you expected? Try a different one. Questions?", "Ask for a rematch. Questions?")]:
    assert s.count(old) == 1, old[:60]
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print(f"{P}: {len(PAIRS) + 6} pairs applied")
