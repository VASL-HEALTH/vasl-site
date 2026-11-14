"""
Data file for tools/internal_links.py, one entry per page that gets a
"related reading" block. Kept separate from the generator so the editorial
decisions (which pages connect, and why a human would click through) are easy
to review and change without touching rendering code.

Each value is a list of (target_rel, anchor_text, one_line_reason) tuples.
target_rel is relative to site/ (e.g. "vlap.html" or "help/billing.html").
Order is preserved in the rendered block.

A tuple may carry a fourth item, (href, label), for a card that needs a second
target of its own. The homepage health plans card uses it so Vasl Bridge is a
link in its own right rather than buried inside the card's one big hit area.

Edges required by SEO-WEEK2.md workstream 1, plus enough additional coverage
to land in the 60-80 new-link target without turning any page into a link
dump, every entry earns its place with a reason someone would click it.
"""

# November 2026 rebuild: the related-reading block now lives only on blog
# posts, and every link points at a page in the new ten-page site.
LINKS = {
    "blog-crisis-without-solving.html": [
        ('bridge.html', 'Vasl Bridge', 'A daily text from emergency department discharge to the first follow-up visit.'),
        ('vlap.html', 'VLAP, the language engine', 'How VLAP flags a signal, shows the exact words and leaves the decision to a clinician.'),
    ],
    "blog-future-culturally-responsive.html": [
        ('vlap.html', 'VLAP, the language engine', 'How VLAP flags a signal, shows the exact words and leaves the decision to a clinician.'),
        ('research.html', 'what VLAP has measured', 'Held-out tests against the tools in use today, with every dataset named.'),
    ],
    "blog-healing-great-divide.html": [
        ('vlap.html', 'VLAP, the language engine', 'How VLAP flags a signal, shows the exact words and leaves the decision to a clinician.'),
        ('health-systems.html', 'Vasl for health plans and systems', 'Clinical decision support inside the workflows plans and health systems already run.'),
    ],
    "blog-human-is-the-system.html": [
        ('technology.html', 'where patient text goes', 'Our own model on our own infrastructure. No patient text goes to an outside AI company.'),
        ('vlap.html', 'VLAP, the language engine', 'How VLAP flags a signal, shows the exact words and leaves the decision to a clinician.'),
    ],
    "blog-mental-health-equity-crisis.html": [
        ('research.html', 'what VLAP has measured', 'Held-out tests against the tools in use today, with every dataset named.'),
        ('health-systems.html', 'Vasl for health plans and systems', 'Clinical decision support inside the workflows plans and health systems already run.'),
    ],
    "blog-missing-infrastructure.html": [
        ('vlap.html', 'VLAP, the language engine', 'How VLAP flags a signal, shows the exact words and leaves the decision to a clinician.'),
        ('technology.html', 'where patient text goes', 'Our own model on our own infrastructure. No patient text goes to an outside AI company.'),
    ],
    "blog-other-diagnosis.html": [
        ('research.html', 'what VLAP has measured', 'Held-out tests against the tools in use today, with every dataset named.'),
        ('vlap.html', 'VLAP, the language engine', 'How VLAP flags a signal, shows the exact words and leaves the decision to a clinician.'),
    ],
    "blog-seven-days-after-discharge.html": [
        ('bridge.html', 'Vasl Bridge', 'A daily text from emergency department discharge to the first follow-up visit.'),
        ('health-systems.html', 'Vasl for health plans and systems', 'Clinical decision support inside the workflows plans and health systems already run.'),
    ],
    "blog/what-a-suicide-risk-word-list-cant-hear.html": [
        ('research.html', 'what VLAP has measured', 'Held-out tests against the tools in use today, with every dataset named.'),
        ('vlap.html', 'VLAP, the language engine', 'How VLAP flags a signal, shows the exact words and leaves the decision to a clinician.'),
    ],
}

HEADER_OVERRIDES = {}
