# SMS Principles

SMS is the opposite of email in nearly every dimension: expensive per message, near-guaranteed attention,
zero tolerance for irrelevance, and a much harder consent regime.

> **Capability note.** SMS dispatch (`bayengage.messaging_sms`) is declared in
> [../capabilities.yaml](../capabilities.yaml) but has not been verified against a BayEngage MCP
> implementation. Confirm the capability exists before planning SMS execution, and degrade to email-only
> when it does not. See [../docs/mcp-integration.md](../docs/mcp-integration.md).

## Consent is separate and stricter

Email consent is not SMS consent. SMS consent is channel-specific, must be explicit, and is regulated
differently across jurisdictions. Never plan an SMS audience without confirming SMS consent through
`bayengage.suppression_and_consent`.

Quiet hours and local-time delivery are not courtesies — in several jurisdictions they are legal
requirements, and everywhere they are the difference between a useful message and a 2am interruption that
produces an opt-out.

Compliance specifics (required disclosures, opt-out keyword handling, jurisdiction rules) are platform
and legal responsibilities, not skill logic. See [../rules/global-rules.md#G10](../rules/global-rules.md).

## The economics change the strategy

Email's marginal cost is near zero, so broad sends can be justified by a small response. SMS costs real
money per recipient, so every message must clear a higher bar. This pushes SMS toward:

- Smaller, higher-intent audiences
- Moments where timing genuinely matters
- High-value customers and high-value events

## What SMS is good at

- Time-critical single messages: a deadline, a drop, a restock, a delivery
- Reaching people who no longer open email
- Very short transactional-adjacent updates
- High-value moments where the interruption is welcome

## What it is bad at

- Explaining anything
- Browsing, comparison, or multiple options
- Routine promotional volume — it burns the channel fast
- Anything that would be equally effective by email

## Writing for the channel

- One idea, one link, one action
- Identify the sender immediately — an unidentified message reads as spam or fraud
- Message length affects cost; brevity is economic as well as stylistic
- Never port email copy into SMS. See [../rules/content-rules.md#N6](../rules/content-rules.md).

## Cadence

SMS has its own, much smaller frequency budget, tracked separately from email. Over-messaging here does
not produce a gradual decline; it produces immediate opt-outs, and SMS opt-outs are usually permanent.
See [../rules/frequency-rules.md#F7](../rules/frequency-rules.md).

## Sequencing with email

The useful pattern is complementary, not duplicative:

| Moment | Channel | Why |
|---|---|---|
| Explain, show, educate | Email | Context and space |
| Remind at the deadline | SMS | Immediacy |
| Re-engage a non-opener | SMS | Different channel, not louder email |
| Recover an abandoned high-value cart | SMS after email | Cost justified by order value |

Sending the same content on both channels at the same time is the most common SMS mistake: it doubles the
cost, doubles the fatigue, and adds nothing.
