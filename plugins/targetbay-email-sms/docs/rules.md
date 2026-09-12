# Rules

## Why rules are separate from skills

A constraint restated inside fourteen skills becomes fourteen slightly different constraints. Rules are
written once, cited by number, and changed in one place.

| | Answers | Lives in |
|---|---|---|
| **Rule** | What is never acceptable? | [../rules/](../rules/README.md) |
| **Knowledge** | Why does this work? | [../knowledge/](../knowledge/README.md) |
| **Skill** | What do I do for this objective? | [../skills/](../skills/README.md) |
| **Playbook** | What differs in this vertical? | [../playbooks/](../playbooks/README.md) |

## The rule set

| File | Scope |
|---|---|
| [safety-rules.md](../rules/safety-rules.md) | Approval gates, irreversibility, blast radius |
| [global-rules.md](../rules/global-rules.md) | Principles binding every skill |
| [audience-rules.md](../rules/audience-rules.md) | Targeting, exclusion, sizing, suppression |
| [campaign-rules.md](../rules/campaign-rules.md) | Campaign creation, scheduling, offers |
| [automation-rules.md](../rules/automation-rules.md) | Variants, branching, topology |
| [personalization-rules.md](../rules/personalization-rules.md) | What may be used to personalise |
| [content-rules.md](../rules/content-rules.md) | Copy, offers, claims, accessibility |
| [frequency-rules.md](../rules/frequency-rules.md) | Cadence, fatigue, collisions |

## Precedence

```
1. safety-rules            never overridden
2. global-rules
3. domain rules            audience / campaign / automation / personalization / content / frequency
4. playbook overlay
5. store context
```

A lower layer may **tighten** a higher one. It may never loosen one. A store that wants a lower frequency
cap than the rules suggest is applying the rules correctly; a store that wants to skip an approval gate is
not, and [safety-rules](../rules/safety-rules.md) does not yield to store preference.

## Citation

Rules are numbered per file so skills can point precisely:

```markdown
Never assume an audience exists ([../../rules/global-rules.md#G4](../../rules/global-rules.md)).
```

Prefixes: `G` global, `S` safety, `A` audience, `C` campaign, `R` automation, `P` personalisation,
`N` content, `F` frequency.

Cite rather than restate. If a skill needs to explain a rule at length, the explanation belongs in
[../knowledge/](../knowledge/README.md) and the skill links to both.

## What is not a rule here

**Deterministic platform enforcement.** Consent, suppression, legal opt-out, sending limits and hard frequency
caps are enforced by TargetBay Email & SMS services. The rules in this package exist to stop an agent from
*planning* something the platform would reject, or something the platform cannot see is a bad idea. They do
not reimplement enforcement ([global-rules.md#G10](../rules/global-rules.md)).

**Vertical conventions.** Those are playbooks.

**Marketing theory.** That is knowledge. A rule states a constraint; the reasoning behind it lives
elsewhere.

## Adding or changing a rule

1. Confirm it is a constraint, not advice or theory
2. Confirm no existing rule covers it — a near-duplicate rule is worse than none
3. Add it to the right file with the next number in sequence. **Never renumber existing rules** — skills
   cite them by number
4. State the rule as an imperative, give the reason in one line, and state when it does not apply
5. Update any skills whose behaviour it changes
6. Run `python3 tests/validate.py`
7. Record it in [../CHANGELOG.md](../CHANGELOG.md) — a new binding rule is at least a MINOR change, and a
   rule that invalidates existing skill behaviour is MAJOR

## How skills consume rules

A skill's `Decision Rules` section states the rules that bind it and links to them. Its `Validation`
section turns the relevant ones into a checklist run before presenting output. Its
`Approval Requirements` section applies [safety-rules](../rules/safety-rules.md) to that skill's specific
actions.

A skill that cites no rules is either trivial or under-specified.
