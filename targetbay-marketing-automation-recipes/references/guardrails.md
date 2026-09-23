# Guardrails Every Recipe Inherits

These apply to every recipe in this skill. A recipe's own `Guardrails` field names the ones specific
to it; everything here is assumed.

Most automation failures are not logic errors. They are a message sent twice, a message sent to
someone who opted out, or three recipes firing at the same person in the same hour because each one
was reasonable on its own.

**This file states what an orchestrated recipe must do.** The underlying mechanics — key strategies,
retry curves, event-handling patterns, suppression scopes, quiet-hours law — belong to
[Email & SMS Best Practices](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/SKILL.md)
and are linked per section rather than repeated here. Where the two disagree, that skill is right.

## Idempotency and the dedupe key

**Derive the key from the event that happened, not the time it was processed.** For a recipe the
natural key is the triggering entity plus the step number — a cart or order identifier plus which
message in the sequence this is.

Retries are the normal case. An event that is re-read after the send succeeded but before it was recorded
will be processed again; a scheduled job that crashes mid-batch will run again from the start. Check the key
before sending rather than after — checking after is a race, and two deliveries arriving together
both find no record and both send.

**Record the intent before the send, then confirm it.** If the recipe sends and then records that it
sent, a failure between the two loses the record and the next run sends again. Recording first makes
the failure mode a missed send you can detect rather than a duplicate the customer detects.

Key strategies, bounded length, and what to do when the platform has no idempotency support:
[Sending Reliability](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/sending-reliability.md).

## The already-messaged guard

Distinct from dedupe. Dedupe stops the same event being processed twice; this stops a person
receiving the same *kind* of message again too soon.

A win-back recipe that runs daily will find the same lapsed customer every day. Without a guard it
mails them every day. The guard is a per-contact record of which recipe last touched them and when,
checked before the audience is assembled — filtering at query time is cheaper and safer than
filtering after.

Set the window from the store's own repeat interval rather than copying one
([automation-rules.md#R13](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/automation-rules.md)).

## Suppression and consent, before every send

**Re-check immediately before sending, not when the audience was assembled.** A batch built at 06:00
and sent at 09:00 will mail people who unsubscribed at 07:00. The gap between assembly and send is
exactly where opt-outs land, and it is the gap an orchestrated recipe widens
([audience-rules.md#A13](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/audience-rules.md)).

Consent is per channel
([audience-rules.md#A10](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/audience-rules.md)).

**Never maintain a parallel suppression list in orchestrator code.** It will drift from the
platform's, and the drift always resolves in the direction of sending to someone who opted out. The
platform enforces; recipes check
([global-rules.md#G10](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/global-rules.md)).

Suppression scopes, per-channel consent records and hygiene jobs:
[List Management](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/list-management.md).

## Frequency budget across recipes

Each recipe is defensible alone. The customer experiences all of them at once.

Hold one budget per contact across every recipe and campaign, and have each recipe spend from it
rather than count its own sends
([frequency-rules.md#F2, #F3](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/frequency-rules.md)).
Give transactional messages priority when the budget is tight — noting that several messages which
feel operational are legally marketing
([Email Types](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/email-types.md)).

When the budget refuses a send, log the refusal. A recipe that silently drops sends looks identical
to a recipe that is broken.

## Quiet hours and local time

Send times are in the recipient's local time, not the store's. A schedule expressed in one time zone
delivers overnight to part of an international list, and an automated flow fires whenever its trigger
fires unless the recipe explicitly defers.

The legal windows, how to derive the zone, and what to do when it is unknown:
[SMS Compliance](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/sms-compliance.md).
Follow that file rather than inventing a rule here.

## Approval gates

Any recipe that generates customer-facing content stops for a human before it sends. The gate is a
blocking step with an explicit approve or reject, and a reject path that feeds the objection back
rather than discarding it.

Two constraints bind every such recipe, and neither is negotiable:
[content-rules.md#N13](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/content-rules.md) —
a failed generation sends nothing; and
[safety-rules.md#S13](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/safety-rules.md) —
a gate that expires into a send is not a gate.

What may ship unreviewed, and what the reviewer checks, is a policy decision this skill does not
make. See
[ai-content-governance](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/ai-content-governance/SKILL.md).

## Consuming platform events

Platform events reach a recipe through the TargetBay MCP (`email_sms.event_stream`), never through a
handler the recipe exposes itself. Assume every event may arrive twice and out of order, advance the
cursor only after the event is recorded, and log what was skipped. The recipe:
[Consuming the event stream](./integration-recipes.md#consuming-the-event-stream).

## Retry and backoff

Retry transport failures and rate limiting; do not retry a rejected request, which will be rejected
again. Cap the attempts and make the give-up path visible — a recipe that retries forever is a recipe
whose failures nobody sees.

Backoff curves, jitter and honouring the platform's retry-after signal:
[Sending Reliability](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/sending-reliability.md).

## Credentials

Platform access is authenticated by the MCP host. No recipe holds, passes or stores TargetBay
credentials. Credentials for the store's own systems live in the orchestrator's secret store, never
in a workflow definition — workflow definitions are frequently exported and shared.

## What the orchestrator must never re-implement

Suppression state, consent records, legal opt-out handling and hard frequency caps are enforced by
the platform. A recipe that keeps its own copy of any of them has created a second source of truth
that will disagree with the first (G10, above).
