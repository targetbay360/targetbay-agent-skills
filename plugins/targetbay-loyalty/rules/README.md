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

## Contact ownership across products

This plugin is not the only TargetBay product that can decide to contact a customer. Email & SMS,
Reviews and Loyalty each have their own frequency limits, and a customer receives the sum of all three —
a total no single product can see.

Which moment belongs to which product is settled once, in
[contact-ownership-rules.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-onboarding/rules/contact-ownership-rules.md), which ships with the
`targetbay-onboarding` plugin because it is the only one whose registry may span all four products.
**Owns the programme-state moment — points, tiers, rewards, referrals — though the messages themselves may dispatch through Email & SMS (X2, X5).**

Those rules are not installed with this plugin. When a store runs more than one TargetBay product, read
them alongside the rules here — the frequency rules in this file bound this product only.

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
