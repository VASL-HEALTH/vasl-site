"""Youth pivot, technology page. Exact old/new pairs, each asserted."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_lib import run
PAIRS = [
    ('Written for a patient&rsquo;s family as much as a clinician, see the <a href="/for-families" style="color:var(--clay);text-decoration:underline;">plain-language version for families</a>.',
     'Written for a patient as much as a clinician, see the <a href="/vlap" style="color:var(--clay);text-decoration:underline;">plain-language overview of VLAP</a>.', 1),
    ("these are the expressions young people actually use,", "these are the expressions patients actually use,", 1),
    ("Humor framing is the most common disclosure suppression mechanism in youth aged 13-22.", "Humor framing is a common disclosure suppression mechanism.", 1),
    ("a documented pre-disclosure mechanism in adolescents.", "a documented pre-disclosure mechanism.", 1),
    ("documented in Black male youth in particular,", "documented in Black men in particular,", 1),
    ("for many younger patients, digital social networks", "for many patients, digital social networks", 1),
    ("&ldquo;Been eating at school cause there's nothing at home&rdquo;", "&ldquo;Been eating at work cause there's nothing at home&rdquo;", 1),
    ('<span class="sig-label">School discipline and push-out</span>', '<span class="sig-label">Workplace discipline and job loss</span>', 1),
    ("&ldquo;Got suspended again&rdquo;", "&ldquo;Got written up again&rdquo;", 1),
    ("&ldquo;They're trying to expel me&rdquo;", "&ldquo;They're trying to fire me&rdquo;", 1),
    ("&ldquo;I don't think I can go back to that school&rdquo;", "&ldquo;I don't think I can go back to that job&rdquo;", 1),
    ("School push-out is a documented trauma, disproportionate for Black students and students with disabilities, and part of the school-to-prison pipeline stressor. VLAP flags for engagement and connection to educational support.",
     "Job loss and workplace discipline are documented stressors, and losing work can put a member&rsquo;s coverage at risk. VLAP flags for engagement and connection to employment and benefits support.", 1),
    ("Parentified youth, children assuming caregiver roles, experience heightened stress, accelerated loss of childhood, and reduced access to their own emotional needs.",
     "People carrying the caregiver role for a parent or household experience heightened stress and reduced access to their own emotional needs.", 1),
    ("scores in Black and Latino youth aged 13-25?", "scores in Black and Latino patients?", 1),
    ("rate in Black, Latino, and LGBTQIA+ youth?", "rate in Black, Latino, and LGBTQIA+ patients?", 1),
]
run(sys.argv[1] if len(sys.argv) > 1 else "site/technology.html", PAIRS, "technology")
