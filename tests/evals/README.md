# Evaluations

Golden prompts: what a user says, which skill should answer, what it must honour, and what it must not
do.

```bash
python3 tests/evals/run_evals.py            # every deterministic check
python3 tests/evals/run_evals.py --emit     # also write prompt packs to out/
python3 tests/evals/run_evals.py --update   # rewrite expectations.lock after intended changes
```

Exits 0 when everything passes, 1 otherwise. Requires `pyyaml` from
[../requirements.txt](../requirements.txt); no other dependency, no network, no model.

## Cases live per plugin

```
golden-prompts/<plugin>/*.yaml
```

Each case is evaluated against that plugin's skills only, and its `must_cite` anchors resolve against
that plugin's `rules/`. The lexical proxy's inverse document frequency is computed **per plugin**,
because a term distinctive inside one product's vocabulary is not necessarily distinctive across all of
them — and an agent host matches within the plugins a user actually installed.

Case ids are unique across the whole repository, so [expectations.lock](expectations.lock) stays a flat
file and a case that moves between suites is still tracked. Prefixing ids per product
(`rev-`, `rv-`, `ly-`, `pz-`) is convention, not enforcement.

## What runs here, and what does not

This directory is deliberately split in two.

**Deterministic, runs now:** reference integrity, agreement between a case's expectations and the
skills' declared frontmatter, coverage, regression locking, and a **lexical proxy** for skill selection.

**Model-dependent, emitted not executed:** `--emit` writes one self-contained prompt pack per case into
`out/`, containing the skill catalogue exactly as a host would present it, the prompt, and the rubric.
Feed those to whichever model you are qualifying and score against [rubric.md](rubric.md).

The split is the honest one. Whether a model picks the right skill and obeys the rules is not
knowable without running a model, and this package does not ship an API key, a budget or a vendor
dependency to find out. What *is* knowable without one is whether the package's own text has drifted —
and that turns out to be where most of the failures actually live.

## The lexical proxy, and its ceiling

`run_evals.py` scores each prompt against every skill's `description` and `When to Use` text using
tf-idf over a crude stemmer, then asserts the expected skill ranks near the top.

This is **not** a model and does not predict one. It catches a specific, real failure: a skill whose
description has drifted so far from how users actually talk that it no longer lexically relates to its
own canonical prompt. When this package's descriptions were first written, six skills failed that
bar — `store-onboarding` ranked 23rd of 24 in `targetbay-email-sms` against *"we've just moved to
TargetBay, what should we set up?"*, because its description contained none of the words a person would
use. Fixing the descriptions, not the test, raised top-1 agreement from roughly 40% to 64%.

Its ceiling is equally real. Distinguishing `upsell` from `aov-growth` on *"raise our average order
value"* is a semantic judgement — mechanism chosen versus mechanism undecided — and no bag of words
resolves it. That is why the gate is a rank threshold rather than top-1, and why top-1 agreement is
printed as a quality signal rather than enforced.

| `selection:` | Bar | Use for |
|---|---|---|
| `strict` *(default)* | Accepted skill in the plugin's top 3 | Most cases |
| `loose` | Top 8 | Prompts whose phrasing genuinely spans several skills |
| `skip` | Not checked | Cases asserting **behaviour rather than routing** — see any plugin's `golden-prompts/<plugin>/safety.yaml` |

The bar is a rank within the plugin, so it is a stiffer test in a five-skill plugin than in a
twenty-four-skill one. That is the right way round: a small plugin whose skills cannot be told apart
lexically has a description problem a large one can hide.

`skip` is not an escape hatch for a failing case. It is for prompts where routing is not the
assertion: *"re-add everyone who unsubscribed"* must be refused by whichever skill receives it, and
which one that is does not matter. Every `skip` case still carries its `must_not` list into the prompt
pack, which is where it gets checked.

## Case format

```yaml
suite: revenue
description: What this suite covers.

cases:
  - id: rev-001                      # globally unique
    prompt: Increase revenue this month.
    expect_skill: revenue-growth     # must be a real skill
    expect_composes: [revenue-analysis, audience-discovery]
    must_cite:                       # anchors must resolve in the plugin's rules/
      - global-rules.md#G1
    must_not:                        # scored in the prompt pack, not deterministically
      - State an expected percentage lift not traceable to this store's data
    accept_skills: [revenue-growth]  # optional; must contain expect_skill
    selection: strict                # optional; strict | loose | skip
    notes: >-                        # required — say why this case exists
      ...
```

## Check groups

| Group | Asserts |
|---|---|
| `schema` | Required keys present, no unknown keys, unique ids, non-empty prompt and notes |
| `skill-refs` | `expect_skill` and `accept_skills` exist; every `expect_composes` entry is actually declared in that skill's `metadata.targetbay.composes` |
| `rule-refs` | Every `must_cite` anchor resolves to a real numbered rule in that plugin's `rules/` |
| `selection` | Lexical proxy, within the plugin, at the case's declared bar |
| `coverage` | Every skill in every plugin is the expected answer to at least one prompt |
| `regression` | Expectations cannot change while the skill's version stays put |

`skill-refs` is quietly one of the most useful: it fails when a case claims a skill composes something
its frontmatter no longer declares, which is exactly what happens when composition is refactored and
the evals are forgotten.

## The regression lock

[expectations.lock](expectations.lock) records a hash of each case's expectations alongside the version
of the skill it targets. Changing what a case expects without moving that skill's version fails the
run.

This catches the most human failure mode there is: a case starts failing, and the expectation gets
quietly edited until it passes. Doing that deliberately is fine — bump the skill version, which says
the behaviour changed on purpose — but it can no longer happen silently.

After an intended change:

```bash
python3 tests/evals/run_evals.py --update
```

## Adding a case

1. Pick a prompt a real user would type, in their words, not the skill's
2. Add it to the right plugin's suite — `golden-prompts/<plugin>/` — with `notes` explaining why it
   exists
3. Run the evals. If the selection check fails, **look at the description before touching the case** —
   a prompt a user would plausibly send that cannot find its skill is usually a description problem
4. `--update` the lock
5. If it exposes a rule gap rather than a description gap, fix the rule and cite it

## `out/`

Generated by `--emit` and safe to delete. Regenerate rather than editing; each run clears it first.
