# Webhooks and Events

A successful API call means the platform accepted the message. It says nothing about whether it
arrived. Everything you know after that comes from events.

> **Map these to your platform's real names.** The event names below are the canonical set the
> industry uses; confirm the exact names, payload shape, signature header and signing algorithm in
> TargetBay's own documentation before implementing. Do not guess a header name.

## Event types

| Event | Meaning | Act on it by |
|---|---|---|
| `sent` | Accepted by the platform for delivery | Recording the message id |
| `delivered` | Accepted by the receiving mail server | Confirming delivery; closing a retry |
| `bounced` | Delivery failed | Suppressing, hard or soft per the bounce type |
| `complained` | Recipient marked it as spam | Suppressing permanently |
| `opened` | Image pixel loaded | Almost nothing — see the caveat below |
| `clicked` | A tracked link was followed | Engagement scoring, flow branching |
| `unsubscribed` | Opted out of marketing | Suppressing marketing on that channel |
| `sms.delivered` | Carrier confirmed handset delivery | Confirming delivery |
| `sms.failed` | Carrier rejected or could not deliver | Investigating the carrier error code |
| `sms.opted_out` | STOP or equivalent received | Suppressing marketing SMS immediately |

**The `opened` caveat.** Apple Mail Privacy Protection and similar proxies prefetch images, which
fires an open event with no human involved. Do not branch flows on opens, and do not define
engagement by them. Use clicks, purchases and cart state. See [Deliverability](./deliverability.md).

## Endpoint

```ts
app.post('/webhooks/messaging', express.raw({ type: 'application/json' }), async (req, res) => {
  // 1. Verify before parsing anything as trusted input
  if (!verifySignature(req.headers, req.body)) {
    return res.status(401).send('invalid signature');
  }

  const event = JSON.parse(req.body.toString());

  // 2. Acknowledge fast, process out of band
  res.status(200).send('ok');

  // 3. Queue — never do the work inside the request
  await eventQueue.enqueue(event);
});
```

Three things this gets right:

1. **Verify first.** An unverified webhook endpoint lets anyone suppress your entire list by posting
   fake complaint events.
2. **Acknowledge within seconds.** Providers time out and retry. Slow processing turns one event into
   a retry storm.
3. **Do the work in a worker.** A database write, a suppression update and a flow exit are too much
   for a request that has a two-second budget.

Read the raw body. Parsing and re-serialising JSON before verifying the signature changes the bytes
and breaks verification — this is the most common reason signature checks fail on day one.

## Signature verification

The usual scheme is an HMAC of a timestamp plus the raw body, using a shared secret, delivered in a
header. The specifics — header names, whether the timestamp is separate, the exact string being
signed — vary by platform and must come from its documentation.

```ts
import crypto from 'node:crypto';

// Header names and the signed-payload format are platform-specific.
// Confirm them in TargetBay's webhook documentation before relying on this.
function verifySignature(headers: Record<string, string>, rawBody: Buffer): boolean {
  const secret = process.env.TARGETBAY_WEBHOOK_SECRET;
  if (!secret) throw new Error('TARGETBAY_WEBHOOK_SECRET is not set');

  const timestamp = headers['x-webhook-timestamp'];
  const provided  = headers['x-webhook-signature'];
  if (!timestamp || !provided) return false;

  // Reject old timestamps so a captured request cannot be replayed later.
  const ageSeconds = Math.abs(Date.now() / 1000 - Number(timestamp));
  if (!Number.isFinite(ageSeconds) || ageSeconds > 300) return false;

  const expected = crypto
    .createHmac('sha256', secret)
    .update(`${timestamp}.${rawBody.toString()}`)
    .digest('hex');

  const a = Buffer.from(expected);
  const b = Buffer.from(provided);
  if (a.length !== b.length) return false;

  // Constant-time compare — a plain === leaks the signature one byte at a time.
  return crypto.timingSafeEqual(a, b);
}
```

Non-negotiables: constant-time comparison, a timestamp window to prevent replay, and the secret from
the environment rather than the source tree.

## Idempotent processing

Providers retry on any non-2xx, and on timeouts. You will receive duplicates. Dedupe on the
provider's event id.

```ts
async function processEvent(event: WebhookEvent) {
  // Insert-or-ignore on a unique event id. If the row already existed, we have seen this event.
  const isNew = await db.events.insertIfAbsent({
    id: event.id,
    type: event.type,
    receivedAt: new Date(),
  });

  if (!isNew) return;

  switch (event.type) {
    case 'bounced':     return handleBounce(event);
    case 'complained':  return handleComplaint(event);
    case 'unsubscribed':
    case 'sms.opted_out': return handleOptOut(event);
    case 'delivered':
    case 'sms.delivered': return markDelivered(event);
    case 'clicked':     return recordClick(event);
    default:            return; // unknown types are logged, not errors
  }
}
```

Events also **arrive out of order**. A `delivered` can land after a `bounced` for a different
recipient in the same batch, and a retry can deliver an old event after a newer one. Make each
handler describe a state transition rather than assuming a sequence, and ignore transitions that
would move the record backwards.

## Handlers

### Bounce

```ts
async function handleBounce(event: BounceEvent) {
  if (event.bounceType === 'hard') {
    await suppress(event.recipient, event.channel, 'hard_bounce', { permanent: true });
    return;
  }

  // Soft: count failures across distinct sends, not attempts within one send.
  const failures = await recordSoftBounce(event.recipient, event.messageId);
  if (failures >= SOFT_BOUNCE_LIMIT) {
    await suppress(event.recipient, event.channel, 'repeated_soft_bounce', { permanent: false });
  }
}
```

Keep the raw SMTP or carrier response. "Mailbox full" and "user unknown" need different treatment,
and a single bounce counter hides that.

### Complaint

```ts
async function handleComplaint(event: ComplaintEvent) {
  await suppress(event.recipient, event.channel, 'complaint', { permanent: true });
  await removeFromAllFlows(event.recipient);
  await alertIfComplaintRateRising(event.campaignId);
}
```

Suppress permanently, remove from every flow, and never re-engage. A complaint is not a preference
to be managed; it is a statement that the message should not have been sent.

The alert matters as much as the suppression — one complaint is noise, a rising rate on one campaign
is a problem you have a few hours to catch.

### Opt-out

```ts
async function handleOptOut(event: OptOutEvent) {
  // Per channel. An SMS STOP does not unsubscribe them from email.
  await suppress(event.recipient, event.channel, 'unsubscribed', { scope: 'marketing' });
  await removeFromMarketingFlows(event.recipient, event.channel);
}
```

Marketing scope only — transactional messages continue. See [List Management](./list-management.md).

## Failure and replay

- Return non-2xx only when you genuinely could not accept the event; providers retry on it
- Expect retries with backoff over hours, and expect them to stop eventually
- Keep a raw-event log so a bug in a handler can be replayed rather than losing the events
- Alert when event volume drops sharply — a silent webhook endpoint looks exactly like a quiet day

## Testing

- Use a tunnelling tool (`ngrok`, `cloudflared`) to expose a local endpoint and register that URL
- Trigger each event type from the platform's dashboard where it offers test events
- Test the duplicate case explicitly: post the same event id twice and confirm one effect
- Test signature failure: post with a bad signature and confirm a 401 and no side effect
- Test out-of-order: post `delivered` after `bounced` and confirm the state does not regress

## Related

- [Sending Reliability](./sending-reliability.md) — the send side of the same loop
- [List Management](./list-management.md) — what the suppression handlers write to
- [Deliverability](./deliverability.md) — why complaint and bounce rates matter
- [SMS Deliverability](./sms-deliverability.md) — carrier error codes behind `sms.failed`
