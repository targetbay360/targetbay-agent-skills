# List Management

Suppression, hygiene and consent state. This is the least glamorous part of the channel and the part
that decides whether anything else works.

## Suppression

### What to suppress, and for how long

| Reason | Scope | Duration | Notes |
|---|---|---|---|
| Hard bounce | All sending on that channel | Permanent | The address does not exist |
| Complaint | All sending | Permanent | Legally load-bearing; never re-engage |
| Unsubscribe | Marketing, that channel | Permanent until they resubscribe | Transactional continues |
| SMS STOP | Marketing SMS | Permanent until START | Does not affect email |
| Repeated soft bounce | All sending on that channel | Temporary, re-testable | Suppress after repeated failures across separate sends, not repeated attempts within one |
| Sunset (no engagement) | Marketing | Until they re-engage | Reputation protection, not a penalty |
| Manual / support request | As requested | As requested | Record who and why |

### Two scopes, not one

Keep "do not market to" separate from "do not send anything to". Collapsing them means an
unsubscribed customer stops receiving order confirmations, which is a support problem and, for
things like renewal notices, a legal one.

### Per channel

An email unsubscribe is not an SMS opt-out, and an SMS STOP is not an email unsubscribe. Store
consent and suppression per channel per contact. Collapsing them is both a compliance failure — you
stop honouring a specific instruction — and a revenue leak, because you silence a channel the
customer never objected to.

The exception is a global opt-out or an erasure request, which applies everywhere by definition.

### The pre-send check

Suppression is only real if the send path cannot bypass it. Put the check inside the send function,
not in the calling code, so a new caller cannot forget it.

```ts
type SendResult =
  | { ok: true; id: string }
  | { ok: false; reason: 'suppressed' | 'no_consent' | 'quiet_hours' };

async function sendMarketingEmail(to: string, message: Message): Promise<SendResult> {
  if (await isSuppressed(to, 'email')) {
    return { ok: false, reason: 'suppressed' };
  }

  if (!(await hasMarketingConsent(to, 'email'))) {
    return { ok: false, reason: 'no_consent' };
  }

  // sendEmail() is your own wrapper around the sending platform's API.
  const id = await sendEmail(to, message);
  return { ok: true, id };
}
```

The same guard for SMS additionally checks the recipient's local time against the permitted window —
see [SMS Compliance](./sms-compliance.md).

Suppression checks run at **send time**, not only at segment-build time. A segment built on Monday
and sent on Thursday will contain people who unsubscribed on Tuesday.

### Suppression outlives the contact

When a contact record is deleted — including through an erasure request — the suppression entry
stays. Otherwise the next CSV import silently re-subscribes someone who unsubscribed. Store a hash
of the address rather than the plaintext where the deletion was an erasure request.

## Hygiene

### Scheduled cleanup

Run regularly, and log what each job removed so an over-aggressive rule is visible:

- Promote repeated soft bouncers to permanent suppression
- Retire never-confirmed double opt-in pending records past their expiry
- Re-normalise and re-deduplicate addresses
- Move the long-unengaged into the sunset flow
- Re-check role and disposable domains against a current list

### Re-engagement, then sunset

Before suppressing the unengaged, ask once. See the sunset flow in
[Ecommerce Flows](./ecommerce-flows.md).

The counter-intuitive part: removing a large unengaged portion usually **raises** total revenue.
Sending to people who never open suppresses inbox placement for the people who do, so the list gets
smaller and the revenue gets larger. The number on the dashboard is not the asset; the deliverable
portion is.

### What "unengaged" means

Define it from the store's own purchase cycle, not a fixed number of days. A customer who buys
annually is not unengaged at six months. A consumable buyer might be unengaged at eight weeks. Use
the distribution of actual repeat intervals for the segment.

Engagement means click or purchase. Do not define it by opens — Apple Mail Privacy Protection makes
opens unreliable, so an opens-based engagement window quietly keeps dead addresses and suppresses
live ones.

## Data retention

- Set a retention period per data class and enforce it with a scheduled job
- Keep full event logs for a shorter window; keep aggregates longer
- Keep consent records for as long as you mail the contact plus the relevant limitation period
- Keep suppression entries indefinitely
- Document the policy, and make sure the job actually runs — an unenforced policy is worse than none
  because it is stated and false

## Metrics worth watching

Trend these, do not stare at single sends:

| Metric | What it tells you | Watch for |
|---|---|---|
| Delivery rate | Reaching the mail server at all | A sudden drop at one provider — that is filtering |
| Hard bounce rate | List quality | A spike after an import means the import was bad |
| Complaint rate | Whether the message was wanted | The most expensive metric; act on any rise immediately |
| Unsubscribe rate | Whether cadence and relevance hold | Rising at steady content means the frequency is too high |
| Click rate | Whether the content worked | Sudden drops can indicate rendering or deliverability problems |
| SMS opt-out rate | Channel health | Effectively permanent losses |
| Revenue per recipient | Whether any of it is working | The metric that ranks flows against each other |

Provider-published thresholds — for example a spam complaint rate below 0.3%, ideally below 0.1% —
belong in [Deliverability](./deliverability.md). Your own targets should be tighter than the
threshold at which you get blocked.

## Related

- [Deliverability](./deliverability.md) — why suppression protects the whole list
- [SMS Deliverability](./sms-deliverability.md) — opt-out rate as a carrier signal
- [Compliance](./compliance.md) — consent records and retention obligations
- [Ecommerce Flows](./ecommerce-flows.md) — the win-back and sunset sequences
- [Webhooks & Events](./webhooks-events.md) — where suppression updates come from
