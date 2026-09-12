# Rules

Constraints that bind every skill in this plugin. Skills cite rules by number rather than restating them,
because a constraint restated in six skills drifts in six directions.

| File | Binds | Cited as |
|---|---|---|
| [safety-rules.md](safety-rules.md) | Everything. Highest precedence in the package | `safety-rules.md#S5` |
| [global-rules.md](global-rules.md) | Every skill's reasoning and output | `global-rules.md#G4` |
| [economics-rules.md](economics-rules.md) | Point value, issuance, redemption, liability, rewards | `economics-rules.md#E3` |
| [tier-rules.md](tier-rules.md) | Tier count, thresholds, benefits, qualification | `tier-rules.md#T2` |
| [referral-rules.md](referral-rules.md) | Referral structure, incentives, fraud, measurement | `referral-rules.md#F2` |

## Precedence

```
safety-rules.md          overrides everything
   ↓
global-rules.md          overrides domain rules and store context
   ↓
economics / tier / referral rules
   ↓
store context and stated preferences
```

A store may tighten any rule. No store, playbook or instruction inside a skill run may loosen
`safety-rules.md`, or `global-rules.md` G10, G11 or G12.

## Adding a rule

A rule belongs here when it binds more than one skill and stating it in each would duplicate it. A
constraint used by exactly one skill belongs in that skill. Number new rules at the end of their file;
never renumber, because skills cite by number.
