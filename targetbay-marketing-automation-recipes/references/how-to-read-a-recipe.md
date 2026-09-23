# How to Read a Recipe

Every recipe in this skill uses the same eight fields, in the same order. This file explains what each
one means, then maps the recipes to the TargetBay MCP capabilities they consume — including what those
capabilities do not offer.

## The eight fields

**Problem** — one sentence, in the words a store owner would use. If a recipe's problem statement
does not describe something the store actually has, the recipe is the wrong one regardless of how
well it is built.

**Trigger** — one of four kinds, and the choice has consequences:

| Kind | Fires when | Consequence |
|---|---|---|
| Platform event | An event arrives through `email_sms.event_stream` | Near-real-time; needs an idempotent consumer, and the MCP must expose the stream |
| Schedule | A clock in the orchestrator | Predictable and cheap to reason about; latency is the interval |
| Inbound form | A person submits something | The only trigger that carries a live human at the other end |
| Store-pushed event | Your systems record an event against a contact | Needs `email_sms.event_tracking`, and it is unconfirmed whether the platform can trigger an automation from one |

**Preconditions** — what must already exist before the recipe can run at all: a list, a consent
state, an approved template, an integration, a field that is actually populated. A recipe whose
preconditions are unmet is not "ready with caveats" — it is blocked, and the work that meets the
precondition comes first.

**Steps** — numbered. Each step that touches the platform names the capability it consumes.

**Guardrails** — the specific dedupe key, suppression check, frequency budget and approval gate this
recipe needs. The shared versions are in [Guardrails](./guardrails.md); this field names the
recipe-specific ones.

**What to measure** — two metrics, never one. The outcome metric says whether the recipe worked.
The guard metric says whether it worked at someone's expense — a recovery flow that lifts revenue
while doubling the unsubscribe rate has not worked.

**Failure modes** — what breaks, what it looks like from the outside when it does, and what the
recipe does about it. "Retry" is not a failure mode; "the send succeeds but the write-back fails, so
the next run sends again" is.

**Not verified** — anything the recipe assumes that reading the integration did not prove. Present
on most recipes. Read it before building, not after.

## Capabilities

Recipes reach the platform only through the TargetBay MCP. Each step names an abstract capability
from the
[capability registry](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/capabilities.yaml);
the MCP host resolves it to a tool and owns authentication. This skill contains no endpoints, request
shapes or credentials, and a recipe never calls the platform any other way.

| Recipes need to... | Capability |
|---|---|
| Read a contact, or page through contacts | `email_sms.customer_intelligence` |
| Create, update or remove a list, or change its members | `email_sms.segmentation` |
| Find or select a pre-built campaign | `email_sms.campaign_management` |
| Send a campaign | `email_sms.messaging_email`, `email_sms.messaging_sms` |
| Read campaign results | `email_sms.campaign_analytics` |
| Create or read templates | `email_sms.template_management` |
| Check suppression, consent and frequency configuration | `email_sms.suppression_and_consent` |
| React to contact, list, campaign and order activity | `email_sms.event_stream` |
| Record an event against a contact | `email_sms.event_tracking` |
| Create or update a contact | **none registered** |

Before building, confirm the connected MCP exposes every capability the recipe names. A recipe whose
capability is missing is blocked — it is not built against some other route to the platform.

**Contact writes have no capability.** The registry has none for creating or updating a contact, so
every recipe step that writes a contact is blocked until the MCP exposes one and the registry records
it. The recipes that depend on it — contact sync, lead capture, bounce and complaint response, double
opt-in verification and click-branched nurture — say so at the step.

**SMS is unverified.** `email_sms.messaging_sms` is declared but unconfirmed. Recipes that sequence
email and SMS degrade to email-only when it is absent.

There is **no segment resource distinct from lists.** Segmentation is done as lists: create a list,
add contacts to it. Every recipe here that talks about a segment means a list.

### No campaign creation

Campaign management here covers finding, reading and selecting campaigns. Recipes do not create one.

This matters more than it sounds. The obvious shape for an automated journey — assemble content,
create a campaign, send it — has no supported route, and the failure is quiet: a workflow that
assumes creation succeeded reports success and no email is sent.

**The working shape:** build the campaign or template once in the interface, and have the recipe
select it and send it. Where content genuinely must vary per recipient, vary it through the
template's own personalisation rather than by generating a new campaign per person.

Each recipe file states this in its opening lines, and the recipes whose source workflow depended on
creation carry it in their **Not verified** block. Confirm against the connected MCP's tool list
before assuming either way.

### Platform events

Event-triggered recipes name event types such as `contact.created`, `contact.updated`,
`order.created`, `order.updated`, `campaign.bounced` and `campaign.unsubscribed`. They arrive through
`email_sms.event_stream`; consuming them correctly is
[Consuming the event stream](./integration-recipes.md#consuming-the-event-stream).

**Not verified:** whether the MCP exposes the event stream at all, the exact event names it uses,
whether an event recorded through `email_sms.event_tracking` can itself trigger a platform-side
automation, and whether SMS dispatch is exposed. Where a recipe depends on one of these, it says so.

## A standing caution

The capability map above is a contract, not an inspection of the MCP. Confirm the tools, field names
and event names the connected TargetBay MCP actually exposes before shipping anything here to
production. Where a recipe and the MCP disagree, the MCP is right and this file needs a correction.
