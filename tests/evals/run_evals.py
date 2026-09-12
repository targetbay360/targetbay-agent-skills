#!/usr/bin/env python3
"""Run the golden-prompt evaluations.

    python3 tests/evals/run_evals.py            # run every deterministic check
    python3 tests/evals/run_evals.py --emit     # also write prompt packs to tests/evals/out/
    python3 tests/evals/run_evals.py --update   # rewrite expectations.lock after intended changes

Exits 0 when every check passes, 1 otherwise.

What is deterministic here and what is not
------------------------------------------
Everything below runs with no model and no network: reference integrity, declared-composition
agreement, and a LEXICAL PROXY for skill selection. The proxy is not the agent — it scores a prompt
against each skill's `description` and `When to Use` text. It catches description drift and genuine
overlap between skills, which is the failure mode that actually bites. It does not tell you how a
model will behave.

The model-dependent half is emitted, not executed: `--emit` writes one self-contained prompt pack
per case containing the skill catalogue exactly as a host would present it, the prompt, and the
rubric. Feed those to whichever model you are qualifying. See rubric.md.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    sys.exit(f"missing dependency: {exc}\ninstall with: python3 -m pip install -r tests/requirements.txt")

EVALS = Path(__file__).resolve().parent
ROOT = EVALS.parent.parent
LOCK = EVALS / "expectations.lock"
OUT = EVALS / "out"

CASE_KEYS = {
    "id", "prompt", "expect_skill", "expect_composes", "must_cite", "must_not",
    "accept_skills", "selection", "notes",
}
# How strictly the lexical proxy is held. See the module docstring: this is a proxy for
# selection, not a model. "strict" is the default and the bar most cases should meet.
SELECTION_BARS = {"strict": 3, "loose": 8, "skip": None}
REQUIRED_CASE_KEYS = {"id", "prompt", "expect_skill", "notes"}

RULE_REF = re.compile(r"^([a-z-]+\.md)#([A-Z]{1,2}\d{1,3})$")
WHEN_TO_USE = re.compile(r"^## When to Use\s*$(.*?)^## ", re.MULTILINE | re.DOTALL)
WORD = re.compile(r"[a-z]{3,}")

STOPWORDS = {
    "the", "and", "for", "use", "when", "with", "that", "this", "has", "not", "are", "how",
    "what", "which", "who", "should", "our", "its", "from", "into", "than", "then", "them",
    "they", "their", "his", "her", "one", "two", "all", "any", "but", "can", "may", "will",
    "was", "were", "been", "being", "have", "had", "does", "did", "doing", "also", "more",
    "most", "some", "such", "only", "own", "same", "each", "other", "after", "before",
    "over", "under", "again", "once", "here", "there", "where", "why", "both", "few",
    "need", "needs", "needed", "want", "wants", "help", "make", "makes", "made", "get",
    "gets", "give", "gives", "take", "takes", "put", "set", "let", "now", "next", "new",
    "out", "off", "still", "yet", "already", "instead", "rather", "well", "just", "like",
    "using", "used", "uses", "skill", "store", "stores", "bayengage",
}

failures: list[str] = []
warnings: list[str] = []
counts: Counter = Counter()


def check(group: str, ok: bool, message: str) -> bool:
    counts[group] += 1
    if not ok:
        failures.append(f"{group}: {message}")
    return ok


def meta_list(fm: dict, key: str) -> list[str]:
    """Read a comma-separated `metadata.targetbay.*` value as a list. The Agent Skills
    spec allows no custom top-level frontmatter keys, so this package's data lives there."""
    raw = (fm.get("metadata") or {}).get(f"targetbay.{key}", "")
    return [v.strip() for v in raw.split(",") if v.strip()]


def stem(word: str) -> str:
    """Crude suffix stripping. Enough to match automations/automation, sending/send."""
    for suffix in ("ies", "ing", "ed", "es", "s"):
        if word.endswith(suffix) and len(word) - len(suffix) >= 4:
            base = word[: -len(suffix)]
            return base + "y" if suffix == "ies" else base
    return word


def terms(text: str) -> Counter:
    return Counter(
        stem(w) for w in WORD.findall(text.lower()) if w not in STOPWORDS
    )


# ------------------------------------------------------------------ load skills

skills: dict[str, dict] = {}
for path in sorted(ROOT.glob("skills/*/SKILL.md")):
    text = path.read_text()
    end = text.find("\n---\n", 4)
    fm = yaml.safe_load(text[4:end])
    body = text[end + 5:]
    when = WHEN_TO_USE.search(body)
    skills[fm["name"]] = {
        "fm": fm,
        # description is weighted 3x: it is what an agent host actually matches on
        "description_terms": terms(fm["description"]),
        "when_terms": terms(when.group(1) if when else ""),
    }

if not skills:
    sys.exit("no skills found; run from inside the repository")

# inverse document frequency over skills, so shared vocabulary ("customer", "campaign")
# does not decide the match
doc_freq: Counter = Counter()
for s in skills.values():
    for term in set(s["description_terms"]) | set(s["when_terms"]):
        doc_freq[term] += 1
N = len(skills)
idf = {t: math.log(N / (1 + df)) + 0.1 for t, df in doc_freq.items()}

for s in skills.values():
    weighted: Counter = Counter()
    for term, n in s["description_terms"].items():
        weighted[term] += 3.0 * n * idf.get(term, 0.1)
    for term, n in s["when_terms"].items():
        weighted[term] += 1.0 * n * idf.get(term, 0.1)
    norm = math.sqrt(sum(v * v for v in weighted.values())) or 1.0
    s["vector"] = {t: v / norm for t, v in weighted.items()}


def rank(prompt: str) -> list[tuple[str, float]]:
    q = {t: n * idf.get(t, 0.0) for t, n in terms(prompt).items()}
    qnorm = math.sqrt(sum(v * v for v in q.values())) or 1.0
    q = {t: v / qnorm for t, v in q.items()}
    scored = [
        (name, sum(s["vector"].get(t, 0.0) * v for t, v in q.items()))
        for name, s in skills.items()
    ]
    return sorted(scored, key=lambda x: (-x[1], x[0]))


# ------------------------------------------------------------------- load cases

cases: list[dict] = []
suites: list[str] = []
for path in sorted((EVALS / "golden-prompts").glob("*.yaml")):
    doc = yaml.safe_load(path.read_text()) or {}
    suites.append(path.stem)
    check("schema", "suite" in doc and "cases" in doc, f"{path.name}: missing 'suite' or 'cases'")
    for case in doc.get("cases", []) or []:
        case["_suite"] = doc.get("suite", path.stem)
        case["_file"] = path.name
        cases.append(case)

check("schema", bool(cases), "no eval cases found")

print(f"\ngolden prompts — {len(cases)} cases across {len(suites)} suites, {len(skills)} skills\n")


# ----------------------------------------------------------------------- schema

seen_ids: dict[str, str] = {}
for case in cases:
    cid = case.get("id", "<missing id>")
    missing = REQUIRED_CASE_KEYS - set(case)
    check("schema", not missing, f"{cid}: missing keys {sorted(missing)}")
    unknown = set(case) - CASE_KEYS - {"_suite", "_file"}
    check("schema", not unknown, f"{cid}: unknown keys {sorted(unknown)}")
    check("schema", cid not in seen_ids, f"duplicate case id '{cid}' in {case['_file']} and {seen_ids.get(cid)}")
    seen_ids[cid] = case["_file"]
    check("schema", bool(str(case.get("prompt", "")).strip()), f"{cid}: empty prompt")
    check("schema", bool(str(case.get("notes", "")).strip()), f"{cid}: empty notes — say why this case exists")


# ------------------------------------------------------------------ skill-refs

for case in cases:
    cid = case["id"]
    expect = case.get("expect_skill")
    check("skill-refs", expect in skills, f"{cid}: expect_skill '{expect}' is not a skill")
    for alt in case.get("accept_skills", []) or []:
        check("skill-refs", alt in skills, f"{cid}: accept_skills names unknown skill '{alt}'")
    if expect in skills:
        declared = set(meta_list(skills[expect]["fm"], "composes"))
        for dep in case.get("expect_composes", []) or []:
            check(
                "skill-refs", dep in declared,
                f"{cid}: expects {expect} to compose '{dep}', but its frontmatter does not declare it",
            )
    if case.get("accept_skills"):
        check("skill-refs", expect in case["accept_skills"],
              f"{cid}: expect_skill '{expect}' must also appear in accept_skills")


# ------------------------------------------------------------------- rule-refs

rule_cache: dict[str, str] = {}
for case in cases:
    cid = case["id"]
    for ref in case.get("must_cite", []) or []:
        m = RULE_REF.match(ref)
        if not check("rule-refs", bool(m), f"{cid}: malformed rule reference '{ref}'"):
            continue
        fname, anchor = m.groups()
        path = ROOT / "rules" / fname
        if not check("rule-refs", path.is_file(), f"{cid}: rule file '{fname}' does not exist"):
            continue
        text = rule_cache.setdefault(fname, path.read_text())
        check("rule-refs", re.search(rf"^### {anchor}\.", text, re.MULTILINE) is not None,
              f"{cid}: rule '{anchor}' not found in {fname}")
    for item in case.get("must_not", []) or []:
        check("rule-refs", bool(str(item).strip()), f"{cid}: empty must_not entry")


# ------------------------------------------------------- selection (lexical proxy)

rank1_hits = 0
rank1_eligible = 0
for case in cases:
    cid = case["id"]
    mode = case.get("selection", "strict")
    if not check("selection", mode in SELECTION_BARS, f"{cid}: unknown selection mode '{mode}'"):
        continue
    bar = SELECTION_BARS[mode]
    if bar is None:
        continue
    accepted = set(case.get("accept_skills") or [case.get("expect_skill")])
    ranked = rank(case["prompt"])
    names = [n for n, _ in ranked]
    position = next((i + 1 for i, n in enumerate(names) if n in accepted), None)

    rank1_eligible += 1
    if position == 1:
        rank1_hits += 1

    ok = check(
        "selection", position is not None and position <= bar,
        f"{cid}: no accepted skill within top {bar}; best was "
        f"{f'#{position}' if position else 'unranked'}, top 3 were {names[:3]}",
    )
    if ok and position == 1 and ranked[0][1] > 0:
        margin = (ranked[0][1] - ranked[1][1]) / ranked[0][1]
        if margin < 0.10:
            warnings.append(
                f"{cid}: thin lexical margin over '{names[1]}' ({margin:.0%}) — descriptions may overlap"
            )

# ------------------------------------------------------------------- coverage

covered = set()
for case in cases:
    covered.add(case.get("expect_skill"))
    covered.update(case.get("accept_skills") or [])
missing_cover = sorted(set(skills) - covered)
check("coverage", not missing_cover, f"skills with no golden prompt: {', '.join(missing_cover)}")


# ------------------------------------------------------------------ regression

def canonical(case: dict) -> str:
    payload = {
        "prompt": case["prompt"],
        "expect_skill": case["expect_skill"],
        "expect_composes": sorted(case.get("expect_composes") or []),
        "must_cite": sorted(case.get("must_cite") or []),
        "must_not": sorted(case.get("must_not") or []),
        "accept_skills": sorted(case.get("accept_skills") or []),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]


current = {
    c["id"]: {
        "hash": canonical(c),
        "skill_version": skills.get(c.get("expect_skill"), {}).get("fm", {}).get("version"),
    }
    for c in cases if c.get("expect_skill") in skills
}

if "--update" in sys.argv:
    LOCK.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
    print(f"expectations.lock rewritten — {len(current)} cases\n")
elif LOCK.is_file():
    locked = json.loads(LOCK.read_text())
    for cid, now in sorted(current.items()):
        was = locked.get(cid)
        if was is None:
            warnings.append(f"{cid}: new case, not in expectations.lock — run --update")
            continue
        if now["hash"] == was["hash"]:
            check("regression", True, "")
            continue
        check(
            "regression", now["skill_version"] != was["skill_version"],
            f"{cid}: expectations changed while {now['skill_version'] and cases[0] and ''}"
            f"'{ {c['id']: c['expect_skill'] for c in cases}[cid] }' stayed at version "
            f"{was['skill_version']} — bump the skill version or revert the expectation",
        )
    for cid in sorted(set(locked) - set(current)):
        warnings.append(f"{cid}: in expectations.lock but no longer a case — run --update")
else:
    warnings.append("expectations.lock does not exist — run with --update to create it")


# ------------------------------------------------------------------ prompt packs

if "--emit" in sys.argv:
    OUT.mkdir(exist_ok=True)
    for stale in OUT.glob("*.md"):
        stale.unlink()
    catalogue = "\n".join(
        f"- **{n}** — {s['fm']['description']}" for n, s in sorted(skills.items())
    )
    for case in cases:
        accepted = case.get("accept_skills") or [case["expect_skill"]]
        body = [
            f"# Eval {case['id']} — suite `{case['_suite']}`",
            "",
            "## Skill catalogue presented to the agent",
            "",
            catalogue,
            "",
            "## Prompt",
            "",
            "```",
            case["prompt"],
            "```",
            "",
            "---",
            "",
            "## Rubric (do not show the agent)",
            "",
            f"**Accepted skill selection:** {', '.join(f'`{a}`' for a in accepted)}",
            "",
        ]
        if case.get("expect_composes"):
            body += ["**Should compose:** " + ", ".join(f"`{d}`" for d in case["expect_composes"]), ""]
        if case.get("must_cite"):
            body += ["**Should honour these rules:**", ""] + [f"- `{r}`" for r in case["must_cite"]] + [""]
        if case.get("must_not"):
            body += ["**Must not:**", ""] + [f"- {m}" for m in case["must_not"]] + [""]
        body += ["**Why this case exists:** " + str(case["notes"]).strip(), ""]
        (OUT / f"{case['id']}.md").write_text("\n".join(body))
    print(f"prompt packs written to {OUT.relative_to(ROOT)}/ — {len(cases)} files\n")


# ---------------------------------------------------------------------- report

total = sum(counts.values())
for w in warnings:
    print(f"  ! {w}")
if warnings:
    print()

if failures:
    print(f"FAILED — {len(failures)} of {total} checks\n")
    for f in failures:
        print(f"  ✗ {f}")
    print()
    sys.exit(1)

print(f"PASSED — {total} checks across {len(counts)} groups")
print(f"  {len(cases)} cases, {len(skills)} skills covered, {len(warnings)} warnings")
if rank1_eligible:
    print(f"  lexical top-1 agreement: {rank1_hits}/{rank1_eligible} "
          f"({rank1_hits / rank1_eligible:.0%}) — a quality signal, not a gate")
sys.exit(0)
