# Automation Rules

Topology decisions — how many automations, how many nodes, which branches. Cited as
`automation-rules.md#R1`.

These rules exist because automation architecture is where agents most reliably over-build. The default
failure is not a missing branch; it is eleven branches nobody can measure or maintain.

---

## Variants — how many automations

### R1. One objective does not mean one automation.
An objective such as "post-purchase" may correctly resolve to one journey or to several. The number is
derived from the store, never assumed.

### R2. Create a separate variant only when a *meaningful* difference exists.
Meaningful differences are differences that change the message, the offer, the timing, the channel or the
goal. Candidate axes:

- lifecycle stage (first-time vs repeat vs VIP vs at-risk)
- customer value (AOV band, LTV band)
- product purchased
- product category
- price band
- product attribute that changes the follow-up (consumable vs durable, sized vs unsized, perishable)
- purchase frequency / replenishment interval
- engagement level
- channel preference and consent
- the business objective itself differing per group

### R3. Do not create a variant merely because segmentation is technically possible.
The platform will let you split on anything. That is not a reason.

### R4. A variant must clear all four tests.
Before creating one, confirm:

1. **Size** — the audience is large enough to produce a readable result.
2. **Difference** — the treatment genuinely differs, not just the label.
3. **Value** — the expected gain exceeds the cost of building and maintaining it.
4. **Coverage** — no existing automation already handles this case.

If any test fails, fold the case into an existing journey as a branch, a personalisation, or nothing.

### R5. Record rejected variants and why.
A variant considered and deliberately not built is a decision worth keeping, otherwise it gets
re-proposed every review. See `rejected_variants` in
[../schemas/workflow.schema.json](../schemas/workflow.schema.json).

### R6. Consolidate before you add.
If two existing automations trigger on the same event with near-identical content, propose merging them
before proposing a third.

---

## Topology — how many nodes

### R7. Never assume a fixed node count.
There is no correct number. Node count follows from the journey the business needs, the length of the
decision window, and how much the store can actually say. A schema, a template or a habit must never
supply the number.

### R8. Every node justifies itself.
Each node states why it exists. A node whose purpose is "because sequences usually have one" is removed.

### R9. Prefer fewer meaningful nodes.
Three nodes that each change the outcome beat nine that pad a sequence. Length is not thoroughness.

### R10. Branch only when the branches diverge.
A branch whose sides converge immediately onto the same content is a condition, a personalisation, or
nothing at all. See [global-rules.md#G9](global-rules.md).

### R11. Avoid branching when any of these hold.
- the resulting audience is too small to measure
- the difference is not commercially meaningful
- an existing automation already covers the case
- the complexity produces no measurable benefit

### R12. Depth costs more than width.
Nested conditions are exponentially harder to test, debug and explain. Prefer a flat journey with a
condition node over a tree three levels deep.

---

## Timing, channel, goals, exit

### R13. Timing follows the customer's clock.
Wait durations derive from observed behaviour — repeat purchase interval, decision window, consumption
cycle, delivery time — not from round numbers.

### R14. Channel follows consent and preference, then cost.
Check consent per channel first, observed channel response second, cost third. SMS is not a louder email;
see [../knowledge/sms-principles.md](../knowledge/sms-principles.md).

### R15. Every automation has a goal and an exit.
State what completion means and what removes a contact early — usually the goal being met, or entry into
a higher-priority journey. An automation with no exit keeps messaging people who already converted.

### R16. Automations must not compete with each other.
Check for contacts who could be in two journeys simultaneously and decide precedence explicitly.

### R17. Read the existing topology before changing it.
Before modifying an automation, read its current nodes, its performance per node, and what depends on it.
Changing a live journey is a `mutation`; activating one is `high_impact`. See
[safety-rules.md](safety-rules.md).

### R18. Optimise the node that loses people.
When improving an existing automation, find the drop-off through `bayengage.automation_analytics` and fix
that node. Adding a node at the end of a journey people already abandoned changes nothing.
