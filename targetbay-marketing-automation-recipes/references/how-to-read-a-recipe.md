# How to Read a Recipe

Every recipe in this skill uses the same eight fields, in the same order. This file explains what each
one means, then records the platform surface the recipes are written against — including what that
surface does not offer.

## The eight fields

**Problem** — one sentence, in the words a store owner would use. If a recipe's problem statement
does not describe something the store actually has, the recipe is the wrong one regardless of how
well it is built.

**Trigger** — one of four kinds, and the choice has consequences:

| Kind | Fires when | Consequence |
|---|---|---|
| Platform event | The platform emits one of its webhook events | Near-real-time; needs a verified signature and an idempotent handler |
| Schedule | A clock in the orchestrator | Predictable and cheap to reason about; latency is the interval |
| Inbound form | A person submits something | The only trigger that carries a live human at the other end |
| Store-pushed event | Your systems record an event against a contact | Needs `event: track`, and it is unconfirmed whether the platform can trigger an automation from one |

**Preconditions** — what must already exist before the recipe can run at all: a list, a consent
state, an approved template, an integration, a field that is actually populated. A recipe whose
preconditions are unmet is not "ready with caveats" — it is blocked, and the work that meets the
precondition comes first.

**Steps** — numbered. Each step that touches the platform names the operation it calls.

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

## The platform surface

**This is the only file in this skill that contains HTTP paths.** Recipes name operations
(`contact: upsert`) instead, so that when the API moves, this file changes and nothing else does.

Base path: `https://developer.targetbay.com/bayengage/v2`. The `bayengage` segment is the platform's
former name; the product is TargetBay Email & SMS.

| Resource | Operation | Request |
|---|---|---|
| `contact` | `create` | `POST /contacts` |
| `contact` | `upsert` | `POST /contacts/upsert` |
| `contact` | `get` | `GET /contacts/{contactId}`, or `GET /contacts?email=` |
| `contact` | `list` | `GET /contacts?limit=&page=` |
| `contact` | `update` | `PUT /contacts/{contactId}` |
| `list` | `create` | `POST /lists` |
| `list` | `get` | `GET /lists/{listId}` |
| `list` | `list` | `GET /lists?limit=&page=` |
| `list` | `addContact` | `POST /lists/{listId}/contacts` |
| `list` | `removeContact` | `DELETE /lists/{listId}/contacts` |
| `campaign` | `get` | `GET /campaigns/{campaignId}` |
| `campaign` | `list` | `GET /campaigns?limit=&page=` |
| `campaign` | `send` | `POST /campaigns/{campaignId}/send` |
| `campaign` | `getReports` | `GET /campaigns/{campaignId}/reports` |
| `campaign` | **create** | **Does not exist** — see below |
| `template` | `create` | `POST /templates` |
| `template` | `get` | `GET /templates/{templateId}` |
| `template` | `list` | `GET /templates?limit=&page=` |
| `event` | `track` | `POST /events` |

Contact fields observed: email, first name, last name, phone, and arbitrary custom fields flattened
onto the request body. Confirm the exact field names before relying on them.

There is **no segment resource**. Segmentation is done as lists: create a list, add contacts to it.
Every recipe here that talks about a segment means a list.

### The missing campaign-create operation

The campaign resource supports read, list, send and reports. It does not support creation.

This matters more than it sounds. The obvious shape for an automated journey — assemble content,
create a campaign, send it — cannot be built against this surface, and the failure is quiet: a call
to an operation that does not exist can return nothing rather than failing loudly, so the workflow
reports success and no email is sent.

**The working shape:** build the campaign or template once in the interface, and have the recipe
select it by id and send it. Where content genuinely must vary per recipient, vary it through the
template's own personalisation rather than by generating a new campaign per person.

Each recipe file states this in its opening lines, and the recipes whose source workflow depended on
creation carry it in their **Not verified** block. Confirm against TargetBay's own documentation
before assuming either way — the surface described here is one reading at one moment, and the
absence of an operation from it is not proof of absence in the API.

### Webhook events

A subscription receives `contact.created`, `contact.updated`, `contact.deleted`, `list.created`,
`list.updated`, `list.deleted`, `campaign.sent`, `campaign.opened`, `campaign.clicked`,
`campaign.bounced`, `campaign.unsubscribed`, `order.created`, `order.updated` — individually or all
at once.

Observed payload keys: `event_type`, `timestamp`, `data`, `contact_id`, `list_id`, `campaign_id`,
`order_id`, and the raw body. Filtering by contact id or list id was available at subscription time.

Signature: HMAC-SHA256 over the raw body, presented as `sha256=<hex>` in a signature header. See
[Guardrails](./guardrails.md) for how to verify it without introducing a timing or re-serialisation
bug.

**Not verified across the whole surface:** whether subscriptions are configured through an API or
only in the interface; whether an event recorded through `event: track` can itself trigger a
platform-side automation; whether event names are free-form or enumerated; and whether SMS dispatch
is exposed at all. Where a recipe depends on one of these, it says so.

## A standing caution

This skill was written by reading an integration, not a specification. Confirm the real request
signatures, webhook headers, field names and event names in TargetBay's own documentation before
shipping anything here to production. Where a recipe and the documentation disagree, the
documentation is right and this file needs a correction.
