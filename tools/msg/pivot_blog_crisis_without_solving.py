"""Youth pivot: blog-crisis-without-solving. Exact pairs, each count asserted."""
import sys; sys.path.insert(0, "tools/msg")
from _pivot_common import apply
PAIRS = [
 ("Every year the youth mental health crisis is documented in more detail.",
  "Every year the behavioral health crisis among Medicaid members is documented in more detail.", 4),
 ("Every year the youth mental health crisis is more thoroughly documented.",
  "Every year the behavioral health crisis in the communities we serve is more thoroughly documented.", 1),
 ("<p>The youth mental health crisis is one of the most thoroughly documented public health problems of the past decade. The data are consistent and alarming. Rates of anxiety, depression, and suicidality among adolescents have risen substantially. Emergency department visits for mental health crises among youth have increased. The proportion of young people who report feeling persistently sad or hopeless has grown. School counselors, pediatricians, and emergency physicians are all describing the same thing from different vantage points.</p>",
  "<p>The behavioral health crisis is one of the most thoroughly documented public health problems of the past decade. The data are consistent and alarming. Rates of anxiety, depression, and suicidality have risen substantially. Emergency department visits for mental health crises have increased. The proportion of people who report feeling persistently sad or hopeless has grown. Primary care physicians, health plan care managers, and emergency physicians are all describing the same thing from different vantage points.</p>", 1),
 ("The standard institutional response to the youth mental health crisis",
  "The standard institutional response to the behavioral health crisis", 1),
 ("<p>The counselor shortage problem is real. The national student-to-school-counselor ratio is approximately 464:1, nearly double the 250:1 ratio recommended by the American School Counselor Association. Adding counselors is necessary and not happening fast enough. But even if every school in the country met the recommended ratio overnight, the cultural alignment problem would remain: counselors who have not been trained in the specific cultural frameworks of the students they serve",
  "<p>The workforce shortage problem is real. In schools alone, the national student-to-school-counselor ratio is approximately 464:1, nearly double the 250:1 ratio recommended by the American School Counselor Association, and health systems and Medicaid plans face the same shortage of behavioral health clinicians. Adding clinicians is necessary and not happening fast enough. But even if every system in the country met its staffing target overnight, the cultural alignment problem would remain: clinicians who have not been trained in the specific cultural frameworks of the patients they serve", 1),
 ("We have been treating the youth mental health crisis as primarily",
  "We have been treating the behavioral health crisis as primarily", 1),
 ("A student who can access a telehealth appointment", "A patient who can access a telehealth appointment", 1),
 ("that student is not meaningfully better served", "that patient is not meaningfully better served", 1),
 ("For platforms specifically targeting underserved youth populations, the numbers are often worse.",
  "For platforms specifically targeting underserved populations, the numbers are often worse.", 1),
 ("Young people who feel understood, whose communication patterns", "People who feel understood, whose communication patterns", 1),
 ("remain engaged. Young people who do not feel understood leave.", "remain engaged. People who do not feel understood leave.", 1),
 ("missing from the youth mental health crisis response", "missing from the behavioral health crisis response", 1),
 ("share relevant cultural context with the young people they are supporting", "share relevant cultural context with the patients and members they are supporting", 1),
 ("trained on how these young people communicate", "trained on how these patients communicate", 1),
 ("<p>The youth mental health crisis will not be solved", "<p>The behavioral health crisis will not be solved", 1),
 ("The percentage of young people in the communities with the highest need", "The percentage of patients and members in the communities with the highest need", 1),
]
apply(sys.argv[1] if len(sys.argv) > 1 else "site/blog-crisis-without-solving.html", PAIRS)
