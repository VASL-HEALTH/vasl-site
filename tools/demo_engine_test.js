/**
 * Regression test for the VLAP demo's in-page engine (site/demo.html).
 *
 * The demo is a single self-contained file, so the only way to test it without
 * a browser is to lift the engine <script> out and run it under Node against a
 * DOM stub. analyzeLocal() is DOM-free by construction, which is what makes
 * this work — if that ever stops being true, this test is the thing that fails.
 *
 * Three things it checks, and they pull against each other:
 *
 *   SENSITIVITY  every scenario button in a distress category must surface at
 *                least one signal and escalate to at least MONITOR. A button
 *                labelled for a signal that renders CLEAR reads as broken.
 *   POSITIVES    all five CLEAR examples must stay at 0 signals and tier=clear.
 *                This is the constraint that stops "fix the false CLEARs" from
 *                degenerating into "escalate everything".
 *   SPECIFICITY  benign and sarcastic distress-shaped text must not fire. This
 *                mirrors the iSarcasm probe in eval_social_registers.py, which
 *                is the project's standing specificity control.
 *
 * Usage:  node tools/demo_engine_test.js [path/to/demo.html]
 * Exits non-zero if any check fails.
 */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const target = process.argv[2] || path.join(__dirname, "..", "site", "demo.html");
const html = fs.readFileSync(target, "utf8");

// The engine is the largest inline <script> with no src attribute.
const blocks = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (!blocks.length) { console.error("no inline <script> found in " + target); process.exit(2); }
const engine = blocks.reduce((a, b) => (b.length > a.length ? b : a), "");

// Evaluated in a vm context rather than the test's own scope: the engine
// declares a lot of top-level consts and this keeps them out of here. The
// source is a file from this repo, not user input — but it is still evaluated
// code, so it gets its own sandbox and an explicit DOM stub rather than the
// real globals.
const noop = () => {};
const stubEl = {
  addEventListener: noop, appendChild: noop, style: {}, value: "", disabled: false,
  textContent: "", innerHTML: "", classList: { add: noop, remove: noop, contains: () => false },
  querySelectorAll: () => [], querySelector: () => null,
};
const sandbox = {
  document: {
    getElementById: () => stubEl, createElement: () => ({ ...stubEl }),
    addEventListener: noop, querySelectorAll: () => [], querySelector: () => null,
  },
  alert: noop, console, performance, Math, Date, JSON, RegExp, Object, Set, Array, String, Number,
};
sandbox.window = sandbox;
vm.createContext(sandbox);
// The engine's top-level `const` bindings are lexically scoped to the script and
// do not become sandbox properties, so hand them out explicitly. This suffix is
// a fixed literal, not built from anything read off the page.
vm.runInContext(
  engine + "\n;globalThis.__SCENARIOS = SCENARIOS;\nglobalThis.__analyzeLocal = analyzeLocal;\n",
  sandbox,
  { filename: path.basename(target) + ":engine" });

const SCENARIOS = sandbox.__SCENARIOS;
const analyzeLocal = sandbox.__analyzeLocal;
if (typeof analyzeLocal !== "function" || !SCENARIOS) {
  console.error("engine did not expose analyzeLocal/SCENARIOS — page structure changed?");
  process.exit(2);
}

// Free-text a visitor would plausibly type. None of these are curated buttons;
// they exist because the buttons passing is not evidence the engine reads
// natural phrasing.
const FREE_TEXT = [
  "I have been feeling really low lately and I do not see the point anymore",
  "i don't see the point anymore",
  "what's the point of any of this",
  "i've been really down for weeks and nothing helps",
  "i feel like there's no way out of this",
];

// Must NOT escalate. Sarcastic hyperbole and ordinary complaint share vocabulary
// with distress; firing on these is the failure mode that makes a screening tool
// useless in production.
//
// The back half of this list is deliberately adversarial — each entry reuses the
// exact phrasing of a real signal in a benign context ("down at the beach",
// "no way out of this parking garage", "we don't do therapy, we do barbecue").
// They were written after an earlier tuning pass hit 42.9% false-fire on them,
// including a CRISIS on "i've been down at the beach all week". Keep them.
const SPECIFICITY = [
  "lmao this weather is killing me",
  "i'm dying at this meme",
  "this homework is the death of me",
  "i could kill for a coffee right now",
  "my phone died again, so annoying",
  "that movie was depressing but good",
  "i'm so done with this group project lol",
  "nobody gets my sense of humor",
  "just finished a great workout, feeling strong",
  "traffic was brutal but i made it on time",
  "the wifi has been down all day and it's driving me nuts",
  "i stayed in bed until noon on saturday because it was raining",
  "my back is numb from sitting in this chair too long",
  "no one told me the meeting moved, typical",
  "i have no one to play doubles with this weekend",
  "this show is so sad but i love it",
  "work has been a lot lately but manageable",
  "i'm tired, going to sleep early tonight",
  "the team depends on me for the demo tomorrow",
  "we don't do therapy in my family, we do barbecue",
  "honestly the point of this class escapes me",
  "there's no way out of this parking garage lol",
  "feeling low energy today, need more coffee",
  "i've been down at the beach all week",
  "nothing helps this headache except sleep",
  "asking for a friend, what's a good pizza place",
  "avoiding everyone until i finish this deadline",
  "i can't fall apart before the wedding, too much to plan",
];

// Two standards, because they are not equally serious. A benign line nudged to
// MONITOR is a tuning cost; a benign line reaching HIGH or CRISIS is a broken
// demo in front of an investor. The monitor allowance is a ceiling to regress
// against, not a target — it currently sits at 2/28.
const MAX_MONITOR_FALSE_RATE = 0.15;

const ESCALATED = new Set(["monitor", "high", "crisis"]);
const pad = (s, n) => String(s).padEnd(n);
let failures = 0;

function run(text) {
  const r = analyzeLocal(text);
  return { tier: String(r.risk_tier), n: (r.signals || []).length, score: r.risk_score };
}

console.log("=".repeat(78));
console.log("SCENARIO BUTTONS");
console.log("=".repeat(78));
for (const [cat, items] of Object.entries(SCENARIOS)) {
  console.log("\n[" + cat + "]");
  for (const s of items) {
    const { tier, n } = run(s.text);
    const isClearCat = cat === "clear";
    let ok, why = "";
    if (isClearCat) {
      ok = tier === "clear" && n === 0;
      if (!ok) why = "  <-- positive example must stay clear at 0 signals";
    } else {
      ok = ESCALATED.has(tier) && n >= 1;
      if (!ok) why = "  <-- distress scenario must surface >=1 signal and escalate";
    }
    if (/\(CRISIS\)/.test(s.label) && tier !== "crisis") { ok = false; why = "  <-- labelled CRISIS"; }
    if (!ok) failures++;
    console.log("  " + (ok ? "ok  " : "FAIL") + " tier=" + pad(tier, 8) + " sig=" + pad(n, 2) + " " + s.label + why);
  }
}

console.log("\n" + "=".repeat(78));
console.log("FREE-TEXT DISTRESS  (must escalate)");
console.log("=".repeat(78));
for (const t of FREE_TEXT) {
  const { tier, n } = run(t);
  const ok = ESCALATED.has(tier) && n >= 1;
  if (!ok) failures++;
  console.log("  " + (ok ? "ok  " : "FAIL") + " tier=" + pad(tier, 8) + " sig=" + pad(n, 2) + " " + t.slice(0, 52));
}

console.log("\n" + "=".repeat(78));
console.log("SPECIFICITY  (must NOT escalate)");
console.log("=".repeat(78));
let monitorFalse = 0, severeFalse = 0;
for (const t of SPECIFICITY) {
  const { tier, n } = run(t);
  const severe = tier === "high" || tier === "crisis";
  if (severe) { severeFalse++; failures++; }
  else if (tier !== "clear") monitorFalse++;
  const mark = severe ? "FAIL" : (tier === "clear" ? "ok  " : "warn");
  console.log("  " + mark + " tier=" + pad(tier, 8) + " sig=" + pad(n, 2) + " " + t.slice(0, 52) +
              (severe ? "  <-- benign text must never reach high/crisis" : ""));
}
const rate = monitorFalse / SPECIFICITY.length;
console.log("\n  high/crisis on benign text: " + severeFalse + "/" + SPECIFICITY.length + "  (must be 0)");
console.log("  monitor on benign text:     " + monitorFalse + "/" + SPECIFICITY.length +
            "  (" + Math.round(rate * 1000) / 10 + "%, ceiling " + Math.round(MAX_MONITOR_FALSE_RATE * 100) + "%)");
if (rate > MAX_MONITOR_FALSE_RATE) {
  failures++;
  console.log("  FAIL monitor false-fire rate above ceiling");
}

console.log("\n" + "=".repeat(78));
console.log(failures === 0 ? "ALL CHECKS PASS" : failures + " CHECK(S) FAILED");
console.log("=".repeat(78));
process.exit(failures === 0 ? 0 : 1);
