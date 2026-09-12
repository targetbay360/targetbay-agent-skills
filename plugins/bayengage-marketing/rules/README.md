# Rules

Rules are the constraints that bind every skill. A skill decides *what to do*; rules decide *what is
never acceptable regardless of what the skill concluded*.

Rules live here rather than inside skills for one reason: a constraint restated in fourteen places
drifts in fourteen directions. Skills link to rules; they do not copy them.

## Files

| File | Scope |
|---|---|
| [safety-rules.md](safety-rules.md) | Approval gates, irreversibility, blast radius. Highest precedence. |
| [global-rules.md](global-rules.md) | Principles that apply to every skill and every decision. |
| [audience-rules.md](audience-rules.md) | Targeting, exclusion, segment sizing, suppression. |
| [campaign-rules.md](campaign-rules.md) | Campaign creation, scheduling, offers, duplication. |
| [automation-rules.md](automation-rules.md) | Variants, branching, topology, node justification. |
| [personalization-rules.md](personalization-rules.md) | What may be used to personalise, and what may not. |
| [content-rules.md](content-rules.md) | Subject lines, body content, offers, claims, accessibility. |
| [frequency-rules.md](frequency-rules.md) | Contact cadence, fatigue, channel pressure, collisions. |

## Precedence

When two rules conflict, the higher layer wins:

```
1. safety-rules            (never overridden)
2. global-rules
3. domain rules            (audience / campaign / automation / personalization / content / frequency)
4. playbook overlay        (playbooks/<vertical>/PLAYBOOK.md)
5. store context           (the individual store's stated preferences)
```

A playbook or a store may **tighten** a rule. Neither may loosen a safety rule. See
[../docs/rules.md](../docs/rules.md) for how skills consume this layering.

## Deterministic rules are not our job

Anything the platform can enforce deterministically — consent, suppression, hard frequency caps,
sending limits, legal opt-out handling — is enforced by BayEngage services. Rules here exist to stop an
agent from *planning* something the platform would later reject or that the platform cannot see is a bad
idea. Do not reimplement platform enforcement in this package.

## Writing a rule

- State the rule as an imperative. "Check X before Y", not "It is generally advisable to consider X."
- Give the reason in one line. A rule nobody understands is a rule that gets argued away.
- Say when the rule does **not** apply, if there is such a case. Rules without exits get ignored wholesale.
- Number rules within a file so skills can cite them precisely (e.g. `automation-rules.md#R4`).
