# Rules

Constraints that bind every skill in this plugin. Skills cite rules by number rather than restating them,
because a constraint restated in seven skills drifts in seven directions.

| File | Binds | Cited as |
|---|---|---|
| [safety-rules.md](safety-rules.md) | Everything. Highest precedence in the package | `safety-rules.md#S5` |
| [global-rules.md](global-rules.md) | Every skill's reasoning and output | `global-rules.md#G3` |
| [request-rules.md](request-rules.md) | Asking a customer for a review | `request-rules.md#R3` |
| [response-rules.md](response-rules.md) | Replying to reviews; responding to a rating problem | `response-rules.md#P2` |
| [placement-rules.md](placement-rules.md) | Where and how proof is displayed and reused | `placement-rules.md#D2` |

## Precedence

```
safety-rules.md          overrides everything
   ↓
global-rules.md          overrides domain rules and store context
   ↓
request / response / placement rules
   ↓
store context and stated preferences
```

A store may tighten any rule. No store, playbook or instruction inside a skill run may loosen
`safety-rules.md`, or `global-rules.md` G10, G11 or G12.

## Adding a rule

A rule belongs here when it binds more than one skill and stating it in each would duplicate it. A
constraint used by exactly one skill belongs in that skill. Number new rules at the end of their file;
never renumber, because skills cite by number.
