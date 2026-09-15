# Sending Reliability

Making sure each message goes exactly once, even when the network does not cooperate.

> The code here uses your own thin wrapper around the sending platform's API —
> `sendEmail(...)`, `sendSms(...)` — rather than a specific SDK call. The patterns are what
> transfer; check your platform's actual request signature, idempotency support and error codes
> before shipping.

## Idempotency

### The problem

```
Your service  ──── send request ────▶  Sending platform
                                        ✓ message queued
              ◀──── (timeout) ─────  ✗ response lost
```

The message went. Your code does not know that. A naive retry sends it twice. For an order
confirmation that is embarrassing; for an OTP it invalidates the code the user is already typing;
for an SMS it costs money and interrupts someone twice.

### Idempotency keys

An idempotency key lets the platform recognise a retry of a request it already processed and return
the original result instead of acting again.

```ts
const key = `order-confirmation:${orderId}`;

await sendEmail({
  to: customer.email,
  template: 'order-confirmation',
  data: { orderId },
  idempotencyKey: key,
});
```

**The key must be derived, not random.** A key generated fresh on each attempt defeats the purpose —
the retry carries a different key and is treated as a new request. Derive it from the business event
that caused the send.

### Key strategies

| Pattern | Use for | Example |
|---|---|---|
| Event id | Anything with a natural unique event | `order-confirmation:10482` |
| Entity + action + version | Repeatable actions on one entity | `password-reset:user_884:v3` |
| Entity + time bucket | Digests and scheduled sends | `weekly-digest:user_884:2026-W37` |
| Flow step | Automated sequences | `cart-abandon:cart_5591:step_2` |

Rules:
- Stable across retries of the same logical send
- Different for a genuinely new send — a second password reset is a new event, not a retry
- Bounded length, and no personal data in the key if it appears in logs

Where the platform does not support idempotency keys, implement the same guarantee yourself: record
`(idempotency_key → message_id)` in your own database inside the same transaction that decides to
send, and check it before dispatching.

## Retry

### What to retry

| Condition | Retry? | Why |
|---|---|---|
| Network timeout, connection reset | Yes | The request may not have arrived |
| HTTP 429 | Yes — honour `Retry-After` | Rate limited |
| HTTP 500, 502, 503, 504 | Yes | Server-side, probably transient |
| HTTP 400, 422 | No | The request is malformed; retrying changes nothing |
| HTTP 401, 403 | No | Credentials or permission — fix the config |
| HTTP 404 | No | Wrong endpoint or missing resource |
| Suppressed / no consent | No | A deliberate refusal, not a failure |

### Exponential backoff with jitter

```ts
function isRetryable(status?: number): boolean {
  if (status === undefined) return true;          // network-level failure
  if (status === 429) return true;
  return status >= 500 && status < 600;
}

async function sendWithRetry(payload: SendPayload, maxAttempts = 4) {
  let lastError: unknown;

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    try {
      return await sendEmail(payload);           // carries a stable idempotencyKey
    } catch (error) {
      lastError = error;

      if (!isRetryable((error as ApiError).status)) {
        throw error;
      }

      if (attempt === maxAttempts - 1) {
        break;
      }

      // 1s, 2s, 4s ... plus jitter so retries do not synchronise
      const backoff = 1000 * 2 ** attempt;
      const jitter = Math.random() * backoff * 0.3;
      await new Promise((resolve) => setTimeout(resolve, backoff + jitter));
    }
  }

  throw lastError;
}
```

**Jitter is not optional.** Without it, every client that failed during the same outage retries at
the same instant and re-creates the outage the moment the service recovers.

**Cap the attempts.** An unbounded retry loop against a permanently failing endpoint is a queue that
never drains.

## Timeouts

A request with no timeout can hang until the process is restarted, holding a worker and blocking
everything behind it.

```ts
async function sendWithTimeout(payload: SendPayload, ms = 10_000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);

  try {
    return await sendEmail(payload, { signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}
```

A timeout is ambiguous — the request may have succeeded. This is exactly why the idempotency key has
to be in place before you add timeouts, not after.

## Queueing

Send asynchronously. Putting a network call to a third party on the critical path of a checkout
means their bad minute becomes your failed order.

```
[Order placed] → [Commit to DB] → [Enqueue send job] → [Return to customer]
                                          ↓
                                   [Worker: sendWithRetry]
                                          ↓
                          [Success: record id] / [Fail: dead-letter]
```

- Enqueue inside the transaction that commits the business event, or use an outbox table, so you
  never enqueue a send for an order that rolled back
- Separate queues by priority: OTPs and password resets must not sit behind a campaign
- Give every queue a dead-letter destination and actually monitor it — a silent dead-letter queue is
  a backlog of messages nobody ever sent
- Rate-limit workers to your platform's documented limits rather than discovering them via 429s

## Error handling

```ts
const result = await sendWithRetry(payload).then(
  (r) => ({ ok: true as const, r }),
  (e) => ({ ok: false as const, e }),
);

if (!result.ok) {
  // Log with enough context to replay: the idempotency key, the event, the final error.
  logger.error('send_failed', {
    idempotencyKey: payload.idempotencyKey,
    event: payload.template,
    status: (result.e as ApiError).status,
  });

  // Decide per message type. A failed OTP needs a user-visible error and a way to try again.
  // A failed campaign message needs a dead-letter entry, not an exception thrown at the caller.
}
```

Never swallow a send failure. A message that silently did not go is worse than an error, because
nobody finds out until the customer does.

## SMS is stricter

The same patterns apply with tighter constraints:

- **Every attempt costs money.** The retry budget is smaller.
- **A duplicate is a real interruption**, not a duplicate in an inbox — the idempotency requirement
  is harder, not softer.
- **Quiet hours interact with retries.** A message that failed at 8:45pm and retries with backoff can
  land after the permitted window. Check the window again at send time, on every attempt, and defer
  rather than deliver late. See [SMS Compliance](./sms-compliance.md).
- **Throughput is capped by your registered tier**, so queue rate-limiting is a hard requirement, not
  a nicety — see [SMS Deliverability](./sms-deliverability.md).

## Related

- [Webhooks & Events](./webhooks-events.md) — finding out what actually happened after the send
- [List Management](./list-management.md) — the suppression guard inside the send path
- [Transactional Emails](./transactional-emails.md) — the messages that most need this
