# Automation Principles

An automation is a journey the *customer* triggers. That single difference from campaigns drives
everything else: timing is relative to the individual, content must stay true for months, and the same
structure serves everyone who enters it.

## Anatomy

| Element | Question it answers |
|---|---|
| **Trigger** | What event puts someone in this journey? |
| **Entry conditions** | Who qualifies, and who is excluded at entry? |
| **Nodes** | What happens, in what order? |
| **Timing** | How long between steps, measured against what? |
| **Conditions / branches** | Where does the path legitimately diverge? |
| **Channel** | Email, SMS, or a sequence of both? |
| **Goal** | What outcome means this worked? |
| **Exit** | What removes someone early? |

An automation missing a goal or an exit is not finished. It will keep messaging people who already
converted.

## Triggers

Good triggers are unambiguous, observable, and happen at a moment when the message is useful: an order
placed, an order delivered, a first purchase, a cart or browse abandoned, a lifecycle stage crossed, a
replenishment interval elapsed, an anniversary, a subscription event.

A trigger that fires constantly for the same person needs a re-entry rule. A trigger that fires rarely
may not justify an automation at all.

## Node types

The vocabulary this package uses is defined in
[../schemas/workflow.schema.json](../schemas/workflow.schema.json):

`trigger`, `wait`, `condition`, `branch`, `email`, `sms`, `audience_check`, `purchase_check`,
`engagement_check`, `product_condition`, `price_condition`, `attribute_condition`, `goal`, `exit`.

These are abstract planning types. The concrete node types a BayEngage automation actually supports are a
platform question — see [../docs/mcp-integration.md](../docs/mcp-integration.md).

## Topology is a decision, not a template

There is no correct number of automations for an objective, and no correct number of nodes for an
automation. Both are derived from the store: its lifecycle shape, catalogue, purchase intervals, audience
sizes, existing coverage and objectives.

The binding rules are in [../rules/automation-rules.md](../rules/automation-rules.md). The reasoning:

- **More variants** help when groups need genuinely different journeys; they hurt when they fragment
  audiences below measurability and multiply maintenance.
- **More nodes** help when each one does work; they hurt by lengthening the journey past the decision
  window the customer is actually in.
- **Deeper branching** is the most expensive kind of complexity. Every level multiplies the paths that
  must be tested, measured and explained.

## Timing

Wait durations come from observed behaviour, not round numbers:

- Post-purchase follow-up → delivery time, then usage time
- Replenishment → the store's observed repeat interval for that product, minus a lead window
- Abandonment → the length of the decision window for that price band
- Win-back → the point at which this contact has exceeded their own normal interval

A journey whose steps are spaced by habit rather than evidence is a journey optimised for the calendar
instead of the customer.

## Branching honestly

Branch when the paths stay different. If two branches reconverge on the same content two nodes later,
the branch was a condition or a personalisation. A useful check: can you state, for each branch, a
message that would be *wrong* to send down the other one? If not, do not branch.

## Automations interact

Contacts qualify for several journeys at once. Without explicit precedence, a customer can receive a
post-purchase message, a replenishment reminder and a win-back attempt in the same week. Decide
precedence deliberately, and give higher-priority journeys the power to exit lower-priority ones.

## Automations decay

Products get discontinued, links rot, offers expire, seasons change, and the audience that enters in
March is not the one that entered last August. Automations need scheduled review, which is what
[../skills/automation-optimization/SKILL.md](../skills/automation-optimization/SKILL.md) exists for.

## Improving an automation means finding where it loses people

Per-node drop-off from `bayengage.automation_analytics` tells you which node is the problem. Adding a
step after the point where people already left changes nothing.
