# Rules

Constraints that bind every skill in this plugin. Skills cite rules by number rather than restating them,
because a constraint restated in six skills drifts in six directions.

| File | Binds | Cited as |
|---|---|---|
| [safety-rules.md](safety-rules.md) | Everything. Highest precedence in the package | `safety-rules.md#S2` |
| [global-rules.md](global-rules.md) | Every skill's reasoning and output | `global-rules.md#G5` |
| [targeting-rules.md](targeting-rules.md) | Who sees what, and who must not | `targeting-rules.md#T3` |
| [surface-rules.md](surface-rules.md) | Placements and the pages carrying them | `surface-rules.md#U2` |
| [measurement-rules.md](measurement-rules.md) | How an onsite change is evaluated | `measurement-rules.md#M4` |

## Precedence

```
safety-rules.md          overrides everything
   ↓
global-rules.md          overrides domain rules and store context
   ↓
targeting / surface / measurement rules
   ↓
store context and stated preferences
```

A store may tighten any rule. No store, playbook or instruction inside a skill run may loosen
`safety-rules.md`, or `global-rules.md` G5, G10 or G11.

## Adding a rule

A rule belongs here when it binds more than one skill and stating it in each would duplicate it. A
constraint used by exactly one skill belongs in that skill. Number new rules at the end of their file;
never renumber, because skills cite by number.
