# Integration Recipes

Getting data in and out, and consuming the platform's event stream correctly. The event-stream recipe
is last here but should be built first — every event-triggered recipe in this skill assumes it works.

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
2. Read the source side — `email_sms.customer_intelligence`, paged, for a platform-outbound sync.
3. Filter to what changed since the last watermark. A full sync every run is expensive and, on a
   two-way sync, a reliable way to produce update storms.
4. Map fields. Drop anything the destination does not need rather than carrying it.
5. Write to the destination, keyed idempotently. For a platform-inbound sync that is
   a contact write, which has no registered capability yet (see [Capabilities](./how-to-read-a-recipe.md#capabilities)).
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

**Not verified** — whether the MCP exposes contact writes at all, and if it does, whether it matches
on email only or on other keys, which decides how fragile the join is.

---

### Inbound lead capture

**Problem** — "Leads arrive from a form and someone copies them across by hand."

**Trigger** — inbound form, delivered by whatever system hosts it.

**Preconditions** — **consent captured at the point of submission**, with a record of what was agreed
to and when. A destination list. A welcome or nurture that actually follows.

**Steps**
1. Receive the submission. Verify it came from where it claims to.
2. Validate the address shape. Reject malformed rather than storing them.
3. **Check what consent was given.** A contact form submission is not marketing consent. A ticked box
   for updates is. Route them differently; do not conflate them.
4. Create or update the contact, carrying the consent evidence — a contact write, which has no registered capability yet (see [Capabilities](./how-to-read-a-recipe.md#capabilities)).
5. Add to the appropriate list — `email_sms.segmentation`.
6. Record the source event — `email_sms.event_tracking`. Source is what lets the welcome recipe branch later.
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

### Consuming the event stream

**Problem** — "We want to react to what happens on the platform, and we have never consumed its
events before."

**Trigger** — events from `email_sms.event_stream`, read through the TargetBay MCP. Consume one event
type while building; taking all of them first makes debugging much harder.

**Preconditions** — the connected MCP exposes `email_sms.event_stream`. If it does not, this recipe is
blocked, and every event-triggered recipe degrades to a schedule reading aggregate results from
`email_sms.campaign_analytics`.

**Steps**
1. Confirm the stream is available and which event types it carries.
2. Read events for one type. Keep a cursor or watermark so a restart resumes rather than replays.
3. Check each event's identifier against recently processed ones. Redelivery is normal.
4. Process: branch on the event type, act, record.
5. Advance the cursor only after the event is recorded. Advancing first loses events on a crash.
6. Log every event skipped as a duplicate or rejected as malformed, with its reason. A silent skip is
   indistinguishable from the platform not emitting.

**Capabilities** — `email_sms.event_stream` only. Downstream recipes call the rest.

**Guardrails** — assume every event may arrive twice and out of order. Act on the state the event
describes, re-read through the relevant capability, not on the event's own copy of it where the two
can differ.

**What to measure** — outcome: events processed and processing latency. Guard: duplicates skipped and
malformed events — a rise in either means a consumer or cursor fault.

**Failure modes** — the cursor advances before processing and a crash loses events. The cursor never
advances and every run reprocesses from the start. A consumer falls behind and event-triggered sends
go out hours late, which is worse for a cart recovery than not sending.

**Not verified** — whether the MCP delivers the stream as a subscription or as a readable log, how far
back it can be read, and whether event names are enumerated. Confirm against the connected MCP's
tool list before relying on this. The capability is declared in
[capabilities.yaml](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/capabilities.yaml).
