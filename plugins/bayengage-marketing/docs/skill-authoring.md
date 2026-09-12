# Skill Authoring

## Before writing anything

Answer these. If any answer is weak, the skill should not exist yet.

1. **What objective does it serve?** If it cannot be stated as something a store owner would ask for, it is
   not a skill.
2. **Does an existing skill already cover it?** Extending one is almost always better than adding a near
   duplicate — the same rule the skills apply to campaigns and automations
   ([../rules/global-rules.md#G7](../rules/global-rules.md)).
3. **What decisions does it own?** A skill that only reads and reports is analysis; a skill earns its place
   by making decisions.
4. **Which capabilities does it need?** Every one must already exist in
   [../capabilities.yaml](../capabilities.yaml). Needing a new capability is a signal to check whether the
   platform actually provides it.
5. **What is the highest-risk action it can reach?** That determines `targetbay.risk_level` and
   `targetbay.execution_mode`.

## Create the files

```
skills/<skill-name>/SKILL.md
```

The directory name **is** the skill name: lowercase, hyphenated, unique.

## Frontmatter

The top level is exactly the [Agent Skills specification](https://agentskills.io/specification),
which permits only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools`.
Its reference validator **rejects** anything else, so everything this package adds lives under
`metadata`, namespaced `targetbay.`, as **string** values — `metadata` admits no other type, which is
why lists are comma-separated.

```yaml
---
name: skill-name                 # == directory name, unique, ^[a-z0-9]+(-[a-z0-9]+)*$
description: Use when ...        # trigger form, 40–1024 chars, one line
license: MIT
metadata:
  targetbay.display_name: Skill Name
  targetbay.version: "1.0.0"
  targetbay.category: automation # see schemas/skill.schema.json for the enum
  targetbay.requires: bayengage.customer_intelligence, bayengage.order_intelligence
  targetbay.composes: audience-discovery   # optional; must resolve; graph stays acyclic
  targetbay.risk_level: plan
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---
```

Keep `description` on one line. The specification's parser is `strictyaml`, not PyYAML, and a
single-line plain scalar sidesteps any question about how it handles folded blocks.

The `description` is what an agent host matches against user intent. Write it as a **situation**, not a
summary of the implementation:

- Good: *Use when a store needs its automation journeys designed — deciding how many automations an
  objective needs, which audiences deserve separate journeys …*
- Bad: *This skill designs automations using customer and product data.*

Include the phrases a user would actually say, and say which neighbouring skill to use instead — that is
what stops the wrong skill firing.

## The fourteen sections

All required, in this order, all non-empty.

| Section | What belongs in it |
|---|---|
| `Purpose` | The objective, and the failure mode the skill exists to prevent |
| `When to Use` | Concrete situations, in the user's language |
| `When Not to Use` | The neighbouring skills, with links. This is what prevents misfires |
| `Required Context` | A table: context, why it is needed, and what happens without it |
| `Required MCP Capabilities` | Each capability and what it is used for |
| `Inputs` | A table: input, required, notes |
| `Decision Process` | The ordered reasoning, usually as a diagram |
| `Decision Rules` | The specific rules, citing `rules/` by number rather than restating them |
| `Workflow` | The lifecycle phases with the risk level of each |
| `Expected Output` | The shape of the result, referencing the schemas |
| `Validation` | A checklist the skill runs before presenting |
| `Approval Requirements` | A table: action, risk, approval |
| `Examples` | Two or three realistic situations with the reasoning, not just the answer |
| `Failure Handling` | A table: situation, response. Every degraded path stated |

Extra sections are allowed after these, but the fourteen must all be present and in order.

## Writing the content

**Cite, do not restate.** Rules live in [../rules/](../rules/README.md), theory in
[../knowledge/](../knowledge/README.md). Link to them by number — `automation-rules.md#R4` — rather than
paraphrasing. Paraphrase drifts.

**Be deterministic.** The reader is a model deciding what to do. Prefer "check X, then Y; if Z, stop" over
"consider the various factors involved".

**Never hard-code business assumptions.** No fixed campaign counts, no fixed node counts, no fixed
sequence lengths, no holiday dates, no threshold numbers. Derive everything from store data and say how it
was derived.

**Make degradation explicit.** For every required capability, say what happens when it is missing.
`blocked` and `partial` are correct outcomes; a fabricated answer is not.

**Keep it concise.** Length is not thoroughness. A skill that cannot be read in a few minutes will be
skimmed, and a skimmed skill is a skill whose rules get missed.

## Composition

Declare delegation in `targetbay.composes`, and link to the skill in the body where the delegation
happens. Do not
copy another skill's reasoning — if two skills need the same logic, it belongs in the composed skill, or in
`rules/` or `knowledge/`.

The composition graph must stay acyclic. If A composes B, B must not compose A: decide which one is
upstream. A "use X first" pointer in `When Not to Use` is a prerequisite, not composition, and does not
create an edge.

## Validate

```bash
python3 tests/validate.py
python3 tests/evals/run_evals.py
```

Checks structure, the Agent Skills specification (via the reference validator, in the `spec` group),
frontmatter against this package's stricter schema, section presence and order, capability and skill
references, the acyclic composition graph, name uniqueness, and every relative link in the repository.

## Then

- Add a golden prompt for it in [tests/evals/golden-prompts/bayengage-marketing/](https://github.com/targetbay360/targetbay-agent-skills/blob/main/tests/evals/README.md) — the
  `coverage` check fails until every skill is the expected answer to at least one prompt. If the
  selection check cannot find your skill from a prompt a user would plausibly type, the description
  is the problem, not the prompt
- Add the skill to the index and the question table in [../skills/README.md](../skills/README.md)
- Remove it from the roadmap list there if it was on it
- Add an entry to [../CHANGELOG.md](../CHANGELOG.md)
- If it changes how the package is used, update [../README.md](../README.md)

## Checklist

- [ ] The objective is one a store owner would state
- [ ] No existing skill already covers it
- [ ] All fourteen sections present, in order, non-empty
- [ ] `description` is in trigger form and names the neighbouring skills
- [ ] Every `targetbay.requires` entry exists in `capabilities.yaml`
- [ ] Every `targetbay.composes` entry exists, and the graph stays acyclic
- [ ] No custom key at the top level — the `spec` group rejects it
- [ ] Rules cited, not restated
- [ ] No hard-coded counts, thresholds or dates
- [ ] Every capability's absence handled in `Failure Handling`
- [ ] Approval requirements match the declared `targetbay.risk_level`
- [ ] `python3 tests/validate.py` passes
- [ ] A golden prompt exists and `python3 tests/evals/run_evals.py` passes
- [ ] README index and CHANGELOG updated
