---
name: targetbay-marketing-automation-recipes
description: Use when wiring a concrete marketing automation against TargetBay Email & SMS — building a welcome, cart-recovery, order, review-request or VIP journey on platform webhook events, running a scheduled churn, re-engagement, list-hygiene or KPI job, syncing contacts with a CRM or a spreadsheet, verifying a webhook signature, adding a human approval gate before a generated message is sent, or deciding which steps belong inside the platform and which belong in an external workflow tool.
license: MIT
metadata:
  author: TargetBay
  version: "1.0.0"
  homepage: https://targetbay.com
---

# TargetBay Marketing Automation Recipes

Runnable patterns for wiring marketing automations against TargetBay Email & SMS. Each recipe names
its trigger, its preconditions, the platform operations it calls, the guardrails it must carry and
what to measure afterwards.

A recipe is a pattern with its guardrails, not a product feature. The guardrails are the part that
gets dropped first and costs the most: a recipe without a dedupe key sends twice, a recipe without a
suppression check mails someone who opted out, and a recipe that generates its own copy without an
approval gate will eventually say something untrue about a product. Every recipe here carries them
explicitly, and every recipe states what it assumes that has not been verified.

## The Verified Surface

What follows was established by reading the platform API, not from product documentation. Treat it as a floor: confirm the real request signatures, field names and
event names in TargetBay's own documentation before shipping.

A naming note. The product is **TargetBay Email & SMS**. The API path segment says `bayengage`,
the platform's former name. This skill uses the product name in prose
and quotes `bayengage` only where it is a literal path or identifier.

**Resources and operations.** Recipes refer to these by name throughout — `contact: upsert`,
`campaign: send`. The HTTP shapes appear in exactly one file,
[How to Read a Recipe](./references/how-to-read-a-recipe.md), so that endpoint drift is a one-file fix.

| Resource | Operations |
|---|---|
| `contact` | `create`, `upsert`, `get`, `list`, `update` |
| `list` | `create`, `get`, `list`, `addContact`, `removeContact` |
| `campaign` | `get`, `list`, `send`, `getReports` |
| `template` | `create`, `get`, `list` |
| `event` | `track` |

**Webhook events.** A subscription covers contact, list, campaign and order activity — thirteen event
types, individually or all at once. **Authentication** is OAuth client credentials or a header key
pair, and is the host's concern; no recipe handles credentials itself. Deliveries are signed. The
event names, the payload keys, the signature format and the subscription filters are listed in
[How to Read a Recipe](./references/how-to-read-a-recipe.md); verifying one correctly is in
[Guardrails](./references/guardrails.md).

**There is no campaign-create operation.** The campaign resource exposes read, list, send and
reports. A recipe that ends "and then it creates and sends a campaign" cannot run as written against
this surface. The working shape is a campaign or template built once in the interface, which the
recipe then selects and sends. Each recipe file states the working shape in its opening lines.

## Architecture Overview

```
[Trigger]   platform event  ·  schedule  ·  inbound form  ·  store-pushed event
                              ↓
                     [Orchestrator step]
                              ↓
   [Guardrail gate]   dedupe key · suppression · consent · frequency budget
                      quiet hours · approval gate, where required
                              ↓
                              ├── refused → log and stop, never send
                              ↓
   [Platform operations]   contacts · lists · templates · send · events
                              ↓
              [Platform event stream — signed]
                              ↓
   [Measurement]   outcome metric · guard metric · write-back
```

## Quick Reference

| Need to... | See |
|------------|-----|
| Understand the recipe format, and what has not been verified | [How to Read a Recipe](./references/how-to-read-a-recipe.md) |
| Add the checks every recipe must carry before it sends | [Guardrails](./references/guardrails.md) |
| Build welcome, cart, order, review or VIP journeys | [Lifecycle Recipes](./references/lifecycle-recipes.md) |
| Vary the offer per person, or sequence email and SMS | [Personalisation and Channel Recipes](./references/personalisation-and-channel-recipes.md) |
| Catch customers going quiet, or win back lapsed ones | [Retention Recipes](./references/retention-recipes.md) |
| Audit the list, react to bounces, verify opt-ins | [List Health Recipes](./references/list-health-recipes.md) |
| Run an A/B cycle, summarise KPIs, export campaign data | [Measurement Recipes](./references/measurement-recipes.md) |
| Let a model draft copy, with a human gate before it sends | [AI-Assisted Recipes](./references/ai-assisted-recipes.md) |
| Sync contacts with a CRM, capture inbound leads, consume webhooks | [Integration Recipes](./references/integration-recipes.md) |
| Understand what was deliberately refused, and why | [Deliberately Not Shipped](./references/not-shipped.md) |
| Design what the message looks like once the wiring works | [Email Template Design](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-template-design) |
| Decide which recipes this store should adopt first | [Automation Recipe Selector](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/automation-recipe-selector/SKILL.md) |

## Start Here

**New store, nothing wired yet?**
[How to Read a Recipe](./references/how-to-read-a-recipe.md) →
[Guardrails](./references/guardrails.md) →
[Integration Recipes](./references/integration-recipes.md) for the signed-webhook primer, then one
lifecycle recipe. Wire the webhook and verify its signature before building anything on top of it;
every event-triggered recipe assumes that layer works.

**After the cart and lifecycle revenue?**
[Lifecycle Recipes](./references/lifecycle-recipes.md). Cart recovery first — it is the highest
return per hour of setup in the set — then order confirmation, then the review request. Welcome
before any of them if capture is already running.

**List going bad — bounces, complaints, spam placement?**
[List Health Recipes](./references/list-health-recipes.md), and the hygiene audit before the bounce
responder: knowing the shape of the problem changes which response is right. The decision about
*who leaves the sending population and when* is a separate question — see
[List Hygiene](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/list-hygiene/SKILL.md).

**Want a model to write the copy?**
[AI-Assisted Recipes](./references/ai-assisted-recipes.md), and read the approval gate before the
generation patterns. Which message classes may ship unreviewed is a policy decision, not a wiring
one — see
[AI Content Governance](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/ai-content-governance/SKILL.md).

**Connecting to other systems?**
[Integration Recipes](./references/integration-recipes.md). Whether a step belongs inside the
platform or outside it is decided by
[Automation Orchestration](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/automation-orchestration/SKILL.md);
this skill covers how to wire it once that is settled.

**Wondering why something is not here?**
[Deliberately Not Shipped](./references/not-shipped.md) — the four patterns that were asked for and
refused, and the reason for each.

## What this skill will not do

**No cold outreach.** Nothing here sends marketing email to a contact who did not opt in. Recipes
that scrape addresses or mail an acquired list are not included, and the reason is recorded in
[Deliberately Not Shipped](./references/not-shipped.md). An ESP's sending reputation is shared across
its customers; a recipe that damages it damages everyone on the platform.

**No generated copy reaching a recipient without a human gate.** Any recipe that generates
customer-facing content carries an approval step, and its failure mode is "send nothing", never
"send the last good version".

**No reimplementation of platform enforcement.** Suppression, consent, legal opt-out and hard
frequency caps are the platform's job. A recipe checks them; it never maintains its own parallel copy
in orchestrator code, because the copy will drift and the drift will send to someone who opted out.

**No copied timings.** Where a recipe states an interval, it is the value the source workflow used,
labelled as such. Derive yours from the store's own data — see
[automation-rules.md#R13](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/automation-rules.md).
