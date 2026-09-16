```
  ╔═══════════════════════════════════════════╗
  ║                                           ║
  ║   T A R G E T B A Y                       ║
  ║                                           ║
  ║   Email & SMS — Best Practices            ║
  ║                                           ║
  ╚═══════════════════════════════════════════╝
```

# TargetBay Email & SMS Best Practices

An agent skill for building production-grade email and SMS for an ecommerce store. Covers DNS
authentication, A2P 10DLC registration, consent and compliance, lifecycle flows, delivery events,
list hygiene and accessibility.

Two channels, one reputation, one consent record — and most failures in this domain are
infrastructural rather than creative.

Its companion,
[Email Template Design](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-template-design),
covers the visual layer — layout, typography, colour and dark mode, template anatomy, calls to action
and imagery.

## What it covers

**Getting delivered**
- SPF, DKIM, DMARC, alignment, and what Gmail, Yahoo and Outlook now require
- A2P 10DLC registration, carrier filtering, GSM-7 vs UCS-2 segment economics

**Staying legal**
- CAN-SPAM, GDPR, CASL, one-click unsubscribe headers
- TCPA, state texting laws, quiet hours, STOP/HELP keyword handling

**Sending the right things**
- Transactional vs marketing, and the ecommerce messages that are legally marketing even when they
  feel operational
- The full transactional message catalog, by store type
- Cart, browse, post-purchase, review request, replenishment, win-back and sunset flows

**Production infrastructure**
- Idempotency keys, retry with jitter, timeouts, queueing
- Webhook signature verification, idempotent event processing, suppression handlers
- Suppression scopes, per-channel consent, hygiene jobs

**Being readable**
- Screen readers, alt text, heading order, contrast, dark mode

## Structure

```
targetbay-email-sms-best-practices/
├── SKILL.md                             # Start here — routes to the right reference
└── references/
    ├── deliverability.md                # SPF/DKIM/DMARC, reputation, provider requirements
    ├── sms-deliverability.md            # 10DLC, carrier filtering, segments, MMS
    ├── compliance.md                    # CAN-SPAM, GDPR, CASL, unsubscribe headers
    ├── sms-compliance.md                # TCPA, state laws, quiet hours, STOP/HELP
    ├── email-types.md                   # Transactional vs marketing
    ├── transactional-emails.md          # Receipts, resets, OTPs, shipping updates
    ├── transactional-email-catalog.md   # Which messages this store needs
    ├── marketing-emails.md              # Campaigns, consent, segmentation
    ├── ecommerce-flows.md               # Cart, post-purchase, review, win-back, sunset
    ├── email-capture.md                 # Forms, popups, double opt-in, SMS opt-in
    ├── list-management.md               # Suppression, hygiene, per-channel consent
    ├── sending-reliability.md           # Idempotency, retry, timeouts, queueing
    ├── webhooks-events.md               # Delivery events, signature verification
    └── accessibility.md                 # Screen readers, alt text, contrast, dark mode
```

## Quick start

Open `SKILL.md`. It has a routing table and five "Start Here" paths — new store, spam problems,
starting SMS, running campaigns, and production-grade sending.

## Two things this skill deliberately does not do

**It does not invent an API.** Code examples call your own thin wrapper — `sendEmail(...)`,
`verifySignature(...)` — rather than a specific SDK method. The patterns transfer; confirm the real
request signatures, webhook headers and event names in TargetBay's own documentation.

**It does not present benchmarks as your numbers.** Published external requirements are named as
such. Illustrative figures are labelled illustrative. Thresholds you should derive from the store's
own data are described as derivations, not as constants.

## License

MIT
