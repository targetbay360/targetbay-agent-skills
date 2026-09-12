# Examples

The [examples/](../examples/) directory holds narrated traces: a user prompt, the skills that fire, the
capabilities read, the decisions made and why, and the shape of the output.

They exist because the skills describe *how to decide*, and a trace shows what that produces. They are the
closest thing this package has to a test of its own reasoning until evaluations are added.

## What a trace is and is not

**Is:** a realistic walkthrough of reasoning, citing rules by number, using abstract capability
identifiers, showing what was rejected as well as what was chosen.

**Is not:** real store data, real API payloads, real MCP tool calls, or a promise of a particular outcome.
Figures in the traces are illustrative and labelled as such — the same rule the skills obey
([../rules/global-rules.md#G3](../rules/global-rules.md)) applies to the documentation about them.

## The traces

| Trace | Prompt | Skills exercised |
|---|---|---|
| [increase-revenue.md](../examples/increase-revenue.md) | "Increase revenue this month." | revenue-growth → audience-discovery, automation-strategy, campaign-optimization |
| [plan-next-month.md](../examples/plan-next-month.md) | "Plan next month's marketing." | monthly-marketing-planner → audience-discovery, holiday-marketing, product-launch |
| [holiday-drip.md](../examples/holiday-drip.md) | "Prepare a Diwali campaign." | holiday-marketing → holiday-drip-campaign → audience-discovery |
| [automation-strategy.md](../examples/automation-strategy.md) | "Improve our post-purchase marketing." | automation-strategy → automation-architect → audience-discovery |
| [customer-winback.md](../examples/customer-winback.md) | "Win back our lapsed customers." | customer-winback → audience-discovery |

## Reading them

Each trace has the same shape:

1. **Prompt** — what the user said
2. **Skill selection** — which skill fires and why, including the ones that did not
3. **DISCOVER** — which capabilities are read and what for
4. **ANALYZE** — what the data shows
5. **Decisions** — each one with the rule that governs it and the alternative rejected
6. **Output** — the shape of the result, against the schemas
7. **Approval** — what stops for a human, and what that request looks like
8. **What the skill refused to do** — usually the most informative section

## Adding a trace

Pick a prompt that exercises composition or a decision that is easy to get wrong. Follow the same shape,
cite rules by number, keep illustrative figures obviously illustrative, and include the rejected
alternatives — a trace where everything is chosen and nothing is rejected teaches nothing.

Run `python3 tests/validate.py` afterwards; traces are link-checked like every other document.
