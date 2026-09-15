# Email Deliverability

Getting the message into the inbox. Everything else in marketing is downstream of this.

## Email Authentication

**Not optional.** Gmail, Yahoo and Outlook reject or spam-filter unauthenticated mail. For a domain
sending 5,000 or more messages a day to any of them, all three of SPF, DKIM and DMARC are required.

### SPF (Sender Policy Framework)

Declares which servers may send mail for your domain. A TXT record on the sending domain.

```
v=spf1 include:_spf.yoursendingprovider.com ~all
```

- Use the exact `include:` your sending platform gives you — a guessed one silently fails.
- End with `~all` (soft fail) rather than `-all` while you are still finding stray senders.
- **One SPF record per domain.** Two TXT records both starting `v=spf1` is a permanent error, not a
  merge. Combine the `include:` mechanisms into a single record instead.
- SPF has a hard limit of 10 DNS lookups. Chaining several vendor includes blows past it and the
  record stops evaluating.

### DKIM (DomainKeys Identified Mail)

A cryptographic signature proving the message was not altered and came from your domain. Your
sending platform issues the public key as a TXT (or CNAME) record at
`<selector>._domainkey.example.com`.

- The selector is platform-specific. Publish whichever one you are given, verbatim.
- Rotating keys is good hygiene; rotate by publishing a second selector before retiring the first.

### DMARC

Tells receivers what to do when SPF and DKIM fail, and gets you the reports that show who is sending
as you.

```
v=DMARC1; p=none; rua=mailto:dmarc@example.com; fo=1
```

**Rollout, in order — never start at reject:**

1. `p=none` — monitor only. Read the aggregate reports until you recognise every sender.
2. `p=quarantine; pct=25` — then raise the percentage as the reports stay clean.
3. `p=reject` — enforcement.

Going to `p=reject` before the reports are clean blocks your own mail. That includes the mail you
forgot about: the helpdesk, the invoicing system, the recruiter tool.

### Alignment is the part people miss

SPF and DKIM can both pass and DMARC still fail. DMARC requires **alignment** — the domain in the
visible `From:` header has to match the domain that SPF or DKIM authenticated. A platform sending
with its own return-path domain passes SPF for *itself*, not for you. This is what a custom sending
domain fixes.

### Verify Your Setup

```bash
# SPF
dig TXT example.com +short

# DKIM — substitute your platform's selector
dig TXT tb._domainkey.example.com +short

# DMARC
dig TXT _dmarc.example.com +short
```

Each should return the record you published. Empty output means the record is missing, or DNS has
not propagated yet.

## What the mailbox providers now require

| Requirement | Gmail | Yahoo | Outlook |
|---|---|---|---|
| SPF + DKIM + DMARC on the sending domain | Yes | Yes | Yes |
| Applies from | Feb 2024 | Feb 2024 | 5 May 2025 |
| Volume trigger | ~5,000/day | ~5,000/day | ~5,000/day |
| One-click unsubscribe (RFC 8058) | Required | Required | Strongly expected |
| Spam complaint rate | Under 0.3%, aim under 0.1% | Under 0.3% | Under 0.3% |
| Valid forward and reverse DNS | Yes | Yes | Yes |

These are the providers' own published requirements, not a target anyone invented. Failing them
produces SMTP-level rejection — the mail does not arrive in spam, it does not arrive at all.

A store below 5,000/day is not exempt in practice. The same signals are used to rank you; the
threshold only marks where they become hard gates.

### BIMI

BIMI puts your logo next to the message in supporting clients. It requires DMARC already at
`p=quarantine` or `p=reject`, plus a Verified Mark Certificate for most providers. Treat it as the
reward for finishing DMARC enforcement, never as a shortcut to reputation.

## Sender Reputation

Reputation attaches to the domain and the IP, accumulates over months, and is spent in days. It is
shared across every message the store sends, which is why a promotional blast can take down password
resets.

### Warming a new domain or IP

Ramp volume gradually, starting with your most engaged contacts — recent purchasers and recent
openers — because early engagement is what the ramp is buying.

*Illustrative ramp only. The real constraint is that engagement stays high while volume rises; if
complaints climb, hold the volume rather than continuing the schedule.*

| Week | Daily volume |
|------|-------------|
| 1 | 50–100 |
| 2 | 200–500 |
| 3 | 1,000–2,000 |
| 4 | 5,000–10,000 |

Send consistently. An irregular pattern is itself a negative signal — a store that mails 10% of its
list weekly and then blasts 100% has changed the pattern being judged.

### Maintaining it

**Do:** mail engaged contacts, act on bounces the same day, remove complainers immediately, keep
volume and cadence steady, segment so the unengaged get less.

**Do not:** buy or rent lists, import an old list wholesale into a new platform, ignore soft bounces
forever, send to an address that has not engaged in a year because the list looks smaller without it.

## Bounce Handling

| Type | Meaning | Action |
|------|---------|--------|
| Hard bounce | Permanent — address does not exist | Suppress immediately, permanently |
| Soft bounce | Transient — mailbox full, server down, greylisted | Retry with widening gaps; suppress after repeated failures across separate sends |
| Block | Receiver refused for reputation or content | Do not retry blindly; read the SMTP response and fix the cause |

Treat the SMTP response text as data. "Mailbox full" and "user unknown" are different problems and a
single bounce counter hides that.

## Complaint Handling

A complaint is someone pressing *report spam*. It is the most expensive metric in the channel because
it is a direct statement that the message was unwanted.

**Reduce complaints by:**
- Only sending to contacts who opted in on that channel
- Making unsubscribe obvious and instant — a hidden link converts into a complaint
- Using a recognisable From name; recognition is what prevents the reflex
- Matching cadence to segment engagement rather than to the campaign calendar
- Honouring what the signup promised — if the popup said "10% off", the first message delivers it

**Feedback loops:** register with Google Postmaster Tools, Yahoo's CFL, and Microsoft SNDS/JMRP.
Suppress every complainer on receipt, with no re-engagement attempt.

## Measurement — rank these correctly

1. **Revenue and conversion** — what the send was for
2. **Unsubscribe and complaint rate** — what it cost
3. **Click rate** — whether the content worked
4. **Open rate** — a weak diagnostic

Apple Mail Privacy Protection prefetches images, which inflates opens for a large and unknowable
share of your list. Open rate is still valid *inside* a controlled subject-line test where the
inflation applies equally to both arms. It is not valid as a success criterion, and a flow that
branches on "opened" is branching on noise.

## Infrastructure

**Separate subdomains by purpose.** `t.example.com` for transactional, `m.example.com` for
marketing. A complaint spike from a promotion then cannot take the order confirmations down with it.
Both subdomains still need their own authentication.

**Never send marketing from a shared free-mail domain.** `From: you@gmail.com` fails DMARC at the
provider that owns it.

**DNS TTL:** keep it low (300s) while setting records up, raise it (3600s+) once stable.

## Troubleshooting

**"We're going to spam."** Check in this order — the list is ordered by how often each is the
actual cause:

1. **Authentication** — SPF, DKIM, DMARC, and alignment. Most of the time it stops here.
2. **Unsubscribe headers** — `List-Unsubscribe` plus `List-Unsubscribe-Post`. See
   [Compliance](./compliance.md).
3. **Reputation** — complaint rate, blacklist status, a recent volume spike.
4. **List quality** — an imported or aged list producing hard bounces on send.
5. **Content** — image-only messages, link shorteners, spam-trigger phrasing, mismatched link domains.
6. **Pattern** — a sudden change in volume, frequency or audience.

**Diagnostics:**
- [Google Postmaster Tools](https://postmaster.google.com) — domain reputation, spam rate, auth pass rates
- [Microsoft SNDS](https://sendersupport.olc.protection.outlook.com/snds/) — Outlook-side data
- [mail-tester.com](https://www.mail-tester.com) — send one message, get a scored report
- [MXToolbox](https://mxtoolbox.com/blacklists.aspx) — blacklist status

TargetBay publishes its own sender guidelines, which restate the same provider requirements:
https://targetbay.com/products/bayengage/sender-guidelines/

## Related

- [SMS Deliverability](./sms-deliverability.md) — the equivalent problem on the other channel
- [List Management](./list-management.md) — acting on bounces and complaints
- [Compliance](./compliance.md) — unsubscribe headers and legal requirements
- [Sending Reliability](./sending-reliability.md) — retries and error handling
