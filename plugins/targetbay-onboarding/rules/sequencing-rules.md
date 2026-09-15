# Sequencing Rules

Cited as `sequencing-rules.md#SQ4`.

Onboarding is an ordering problem before it is a configuration problem. The same set of resources built
in a different order produces a different outcome, because some configuration captures data it cannot
capture retroactively, and some decisions cannot be made until earlier ones have produced evidence.

---

### SQ1. Capture before consumption.
Configuration that captures data — review triggers, onsite tracking, event instrumentation — comes before
configuration that consumes it. A review trigger armed on day sixty cannot ask about a day-ten order.
Capture is the only kind of configuration whose delay destroys value permanently.

### SQ2. Sequence by what a step spends, not by what it is worth.
Onsite work spends no contact budget
([contact-ownership-rules.md#X3](contact-ownership-rules.md)), so it can run while everything else is
still being decided. Anything that reaches an inbox spends a scarce shared resource and waits its turn.

### SQ3. Nothing activates before the thing it depends on has been verified.
A journey that targets a segment activates after that segment exists and has been confirmed to hold who
it should. Verification is a step, not an assumption.

### SQ4. A precondition is an observation, never a date.
"After 200 orders" is a precondition. "In week six" is a guess about how fast the store will grow. Every
step in a blueprint states what must be observably true before it runs
([global-rules.md#G14](global-rules.md)).

### SQ5. A provisional value may not gate an irreversible step.
If a step's timing or audience depends on a threshold that is provisional rather than derived, either the
step waits until the threshold is derived, or the step is made reversible. Building something permanent on
a playbook default is how a store ends up with a programme nobody can explain.

### SQ6. Decisions that need evidence go last.
Loyalty tier thresholds, replenishment intervals and win-back timing all require history the store does
not have on day one. Sequencing them late is not deferral — it is the difference between a derived
programme and an invented one.

### SQ7. The sequence states what it is waiting for, per product.
Each product's position in the blueprint carries the reason it is there. "Loyalty last" is a decision;
"Loyalty last, because tier thresholds need a repeat rate and this store has three orders" is a decision
that can be reviewed and later reversed on evidence.
