# Rules

Constraints that bind every skill in this plugin. Skills cite rules by number rather than restating them,
because a constraint restated in four skills drifts in four directions.

| File | Binds | Cited as |
|---|---|---|
| [safety-rules.md](safety-rules.md) | Everything. Highest precedence in the package | `safety-rules.md#S2` |
| [global-rules.md](global-rules.md) | Every skill's reasoning and output | `global-rules.md#G14` |
| [contact-ownership-rules.md](contact-ownership-rules.md) | Who may contact a customer, and how often, across all four products | `contact-ownership-rules.md#X2` |
| [sequencing-rules.md](sequencing-rules.md) | The order of an onboarding plan and what gates each step | `sequencing-rules.md#SQ1` |

## Precedence

```
safety-rules.md                overrides everything
   ↓
global-rules.md                overrides domain rules and store context
   ↓
contact-ownership-rules.md     overrides sequencing where the two touch
   ↓
sequencing-rules.md
   ↓
store context, intake answers and stated preferences
```

A store may tighten any rule. No store, playbook or instruction inside a skill run may loosen
`safety-rules.md`, `global-rules.md` G10, G11 or G12, or `contact-ownership-rules.md` X1, X4 or X7.

## Why contact ownership lives here

Email & SMS, Reviews and Loyalty can each decide to contact the same customer, and each product's rules
are correct in isolation. The conflict is only visible when all four programmes are designed together,
which happens exactly once per store: at onboarding. That is why the rule lives in this plugin rather
than being duplicated, and drifting, across the other four.

## Adding a rule

A rule belongs here when it binds more than one skill and stating it in each would duplicate it. A
constraint used by exactly one skill belongs in that skill. Number new rules at the end of their file;
never renumber, because skills cite by number.
