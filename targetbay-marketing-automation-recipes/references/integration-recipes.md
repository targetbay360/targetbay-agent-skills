# Integration Recipes

Getting data in and out, and consuming the platform's event stream correctly. The webhook primer is
last here but should be built first — every event-triggered recipe in this skill assumes it works.

All recipes below inherit [Guardrails](./guardrails.md), select a pre-built campaign rather than
creating one, and quote the source workflow's intervals rather than recommending them. See
[How to Read a Recipe](./how-to-read-a-recipe.md).

Whether a step belongs inside the platform or outside it is decided by
[automation-orchestration](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/automation-orchestration/SKILL.md);
this file covers the wiring once that is settled.

---

### Contact sync with an external system

**Problem** — "Our CRM and our marketing platform disagree about who our customers are."

**Trigger** — schedule for a full reconcile, plus platform events `contact.created` and
`contact.updated` for live changes.

**Preconditions** — **a decision about which system wins on a conflict, made before building.** This
is the whole design; everything else is plumbing. A stable join key — email is the obvious choice and
a poor one, because people change it. A field mapping written down.

**Steps**
1. Decide direction. One-way is far cheaper to reason about than two-way and is usually enough.
2. Read the source side — `contact: list`, paged, for a platform-outbound sync.
3. Filter to what changed since the last watermark. A full sync every run is expensive and, on a
   two-way sync, a reliable way to produce update storms.
4. Map fields. Drop anything the destination does not need rather than carrying it.
5. Write to the destination, keyed idempotently — `contact: upsert` for a platform-inbound sync.
6. **Never sync consent state as an ordinary field.** Consent belongs to the platform, and a CRM
   overwriting it is a compliance incident.
7. Record the watermark and a per-run reconciliation count.


**Guardrails** — **suppression and consent are never overwritten by a sync.** A contact suppressed on
the platform stays suppressed regardless of what the other system thinks. On a two-way sync, guard
against echo: a write that fires the event that triggers the write back. Sync in bounded batches, so
a bad mapping damages a batch and not the base.

**What to measure** — outcome: how many records disagree between the systems after a run. Guard: how
many contacts had consent state touched, which should be zero.

**Failure modes** — the echo loop, which looks like the sync working hard and is actually the sync
fighting itself. A mapping change silently blanks a field across the base; the reconciliation count
at step 7 is what catches it. The join key changes and one person becomes two records.

**Not verified** — whether `contact: upsert` matches on email only or on other keys, which decides
how fragile the join is.

---

### Inbound lead capture

**Problem** — "Leads arrive from a form and someone copies them across by hand."

**Trigger** — inbound form, or a webhook from wherever the form lives.

**Preconditions** — **consent captured at the point of submission**, with a record of what was agreed
to and when. A destination list. A welcome or nurture that actually follows.

**Steps**
1. Receive the submission. Verify it came from where it claims to.
2. Validate the address shape. Reject malformed rather than storing them.
3. **Check what consent was given.** A contact form submission is not marketing consent. A ticked box
   for updates is. Route them differently; do not conflate them.
4. Create or update the contact — `contact: upsert`, carrying the consent evidence.
5. Add to the appropriate list — `list: addContact`.
6. Record the source event — `event: track`. Source is what lets the welcome recipe branch later.
7. Hand off to the welcome or nurture, which runs its own checks.


**Guardrails** — **marketing consent is not implied by contact.** Someone asking a question has not
asked for a newsletter. Where the store requires double opt-in, this recipe hands to the verification
flow in [List Health Recipes](./list-health-recipes.md) rather than adding directly at step 5.
Rate-limit by origin; an open form endpoint is an open contact-creation endpoint.

**What to measure** — outcome: leads captured and reaching the follow-up. Guard: complaint rate on
the follow-up, which is the signal that step 3 is conflating consent types.

**Failure modes** — a form change drops the consent field and everything routes as consented. Bot
submissions fill the list with addresses that will bounce.

**Not verified** — whether consent evidence can be stored on the contact in a form the platform
treats as authoritative, or is only a custom field the platform does not enforce against. Whether the
store needs a confirmation step at all is a policy decision — see
[consent-verification](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/consent-verification/SKILL.md).

---

### Signed webhook primer

**Problem** — "We want to react to what happens on the platform, and we have never consumed its
events before."

**Trigger** — platform event. Subscribe to one type while building; subscribing to all of them first
makes debugging much harder.

**Preconditions** — an endpoint reachable from the platform, over TLS, that can return quickly. The
signing secret in a secret store.

**Steps**
1. Expose the endpoint. It does one thing: verify, enqueue, respond.
2. **Capture the raw request body before any middleware parses it.** This is the step that is most
   often got wrong and produces the most confusing failures.
3. Verify the HMAC-SHA256 signature against those raw bytes, with a constant-time comparison. Reject
   on mismatch — do not log and continue.
4. Check the event's identifier against recently processed ones. Redelivery is normal.
5. Enqueue and **respond immediately.** Processing inside the request is how deliveries time out and
   get redelivered, which produces duplicate work and looks like a platform fault.
6. Process from the queue: branch on `event_type`, act, record.
7. Log every rejected delivery with its reason. A silent rejection is indistinguishable from the
   platform not sending.

**Platform calls** — none; this recipe consumes events. Downstream recipes make the calls.

**Guardrails** — verify before parsing. Verify against raw bytes, not a re-serialised object — key
order and whitespace are not preserved, and the resulting failures are intermittent and mystifying.
An unverified handler is an open path into the store's contact database. Assume every event may
arrive twice and out of order.

**What to measure** — outcome: delivery success rate and processing latency. Guard: rejected
deliveries — a rise means either an attack or a secret rotation nobody propagated.

**Failure modes** — a body parser consumes the stream before step 2 and every signature fails. The
endpoint is slow, the platform times out, and every event is delivered repeatedly. A rotated secret
is deployed on one side only.

**Not verified** — whether subscriptions are managed through an API or only in the interface, whether
the platform retries on a non-2xx response and how often, and the exact signature header name. Confirm
all three before relying on this in production. General webhook handling patterns are covered in
[Webhooks & Events](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/webhooks-events.md).
