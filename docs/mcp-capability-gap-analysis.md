# MCP Capability Gap Analysis — the 4.2.0 email quality layer

What the seven skills added in `targetbay-email-sms` 4.2.0 need, and how confident this repository is
that the TargetBay MCP can supply it.

This is deliberately **narrow**. The repo-wide position on capability mapping is
[mcp-capability-inventory.md](mcp-capability-inventory.md), which says the answers belong in each
plugin's `capabilities.yaml` rather than in a worksheet that drifts alongside it. That still holds.
What is recorded here is only what the new skills introduced: one capability that had to be added, one
that had to be refused, and the degradation path for each new skill when the data is not there.

Nothing below has been verified against a live MCP. No skill in this marketplace can execute yet.

## Status vocabulary

| Status | Meaning |
|---|---|
| `AVAILABLE` | The capability is in `capabilities.yaml` and the class of data plainly exists in any sending platform. Still `mcp_tools: TODO` |
| `PARTIALLY_AVAILABLE` | The capability exists, but the specific shape a skill needs from it is not confirmed |
| `MISSING` | No capability covers it, and none was added. The skill degrades and says so |
| `UNKNOWN` | A capability was added because the data must exist somewhere, but whether the MCP exposes it has never been inspected |

## Per skill

### `email-quality-auditor`

| Needs | Capability | Status |
|---|---|---|
| The campaign as configured | `email_sms.campaign_management` | `AVAILABLE` |
| Resolved audience size after exclusions | `email_sms.segmentation` | `AVAILABLE` |
| Consent and suppression for that audience | `email_sms.suppression_and_consent` | `AVAILABLE` |
| Recent contact history for the same audience | `email_sms.campaign_analytics` | `PARTIALLY_AVAILABLE` — aggregate performance is clearly in scope; per-contact recent-contact counts across campaigns *and* automations may not be |
| Calendar occupancy over the send window | `email_sms.marketing_calendar` | `AVAILABLE` |
| Product availability for referenced items | `email_sms.product_intelligence` | `PARTIALLY_AVAILABLE` — inventory posture is described but its granularity is unconfirmed |
| Offer terms as configured against as written | `email_sms.campaign_management` | `PARTIALLY_AVAILABLE` — whether promotion configuration is readable is unconfirmed |

Degradation: blocks only on campaign configuration, audience resolution, and consent. Everything else
is reported as an unchecked dimension by name.

### `deliverability-qa`

| Needs | Capability | Status |
|---|---|---|
| Authentication records and alignment | `email_sms.sending_infrastructure` | `UNKNOWN` — **added in `capabilities.yaml` 1.3.0**, flagged unverified |
| IP posture and warm-up state | `email_sms.sending_infrastructure` | `UNKNOWN` |
| Bounce and complaint rates over time | `email_sms.campaign_analytics` | `AVAILABLE` |
| Engagement split by **receiving domain** | `email_sms.campaign_analytics` | `PARTIALLY_AVAILABLE` — the dimension is the whole point of D6 and its availability is unconfirmed |
| Seed-list or provider inbox placement | — | **`MISSING`** |

Degradation: reports the identity layer as unverified rather than sound when
`sending_infrastructure` is absent; stays programme-wide when the receiving-domain split is absent;
and always states that placement is unknown, because it always is.

### `email-render-qa`

| Needs | Capability | Status |
|---|---|---|
| The built message, markup and plain-text part | `email_sms.template_management` | `PARTIALLY_AVAILABLE` — the capability covers templates; whether a rendered campaign instance is readable is unconfirmed |
| Image assets and their alt text | `email_sms.template_management` | `PARTIALLY_AVAILABLE` |
| Client and device mix of this store's opens | `email_sms.campaign_analytics` | `PARTIALLY_AVAILABLE` |
| Brand colours, locale, writing direction | `email_sms.store_profile` | `PARTIALLY_AVAILABLE` |
| Actual rendering in a mail client | — | **`MISSING`** — no capability renders a message. The skill reasons about the markup and reports views it could not inspect as unchecked |

### `dynamic-content-personalizer`

| Needs | Capability | Status |
|---|---|---|
| Which fields exist per contact | `email_sms.customer_intelligence` | `AVAILABLE` |
| **Fill rate** per field | `email_sms.customer_intelligence` | `PARTIALLY_AVAILABLE` — the load-bearing input for P3, and the one most likely to be absent |
| Purchase history and intervals | `email_sms.order_intelligence` | `AVAILABLE` |
| Product attributes for referenced items | `email_sms.product_intelligence` | `AVAILABLE` |
| Recency of each signal | `email_sms.customer_intelligence` | `PARTIALLY_AVAILABLE` — without it, P9's staleness bound cannot be set |
| Message structure and variable slots | `email_sms.template_management` | `PARTIALLY_AVAILABLE` |

### `offer-strategy`

| Needs | Capability | Status |
|---|---|---|
| Discount usage history per customer | `email_sms.order_intelligence` | `PARTIALLY_AVAILABLE` — the capability names discount usage; per-customer granularity is unconfirmed |
| Prior offers and what each produced | `email_sms.campaign_analytics` | `AVAILABLE` |
| Order value distribution | `email_sms.order_intelligence` | `AVAILABLE` |
| Margin | `email_sms.product_intelligence` | `PARTIALLY_AVAILABLE` — described as "margin signals", which is not the same as margin. The skill is built to proceed without it |
| Shipping cost structure | — | **`MISSING`** — shipping offers are presented with their cost unknown rather than as cheap |

### `product-recommendation-strategy`

| Needs | Capability | Status |
|---|---|---|
| Catalogue, attributes, categories, price bands | `email_sms.product_intelligence` | `AVAILABLE` |
| Co-purchase relationships observed in this store | `email_sms.product_intelligence` | `PARTIALLY_AVAILABLE` — named as "affinity and co-purchase relationships"; whether it is computed or raw is unconfirmed |
| Per-contact purchase history | `email_sms.order_intelligence` | `AVAILABLE` |
| Browse or category affinity where no purchase exists | `email_sms.customer_intelligence` | `PARTIALLY_AVAILABLE` |
| Availability posture per product | `email_sms.product_intelligence` | `PARTIALLY_AVAILABLE` |

### `campaign-conflict-resolver`

| Needs | Capability | Status |
|---|---|---|
| Scheduled campaigns across the window | `email_sms.marketing_calendar` | `AVAILABLE` |
| Live automations and their entry conditions | `email_sms.automation` | `AVAILABLE` |
| **Which contacts are currently inside a journey** | `email_sms.automation` | `PARTIALLY_AVAILABLE` — measuring overlap needs contact-level journey membership, not just journey configuration. This is the single most important unconfirmed item for this skill |
| Per-entrant value of each journey | `email_sms.automation_analytics` | `AVAILABLE` |
| Channel consent per contact | `email_sms.suppression_and_consent` | `AVAILABLE` |

## The two registry decisions

**One capability was added.** `email_sms.sending_infrastructure` — sending domains, authentication
record state and alignment, IP posture, warm-up state and sending limits. Every sending platform must
hold this for mail to leave at all, which is why it was added rather than refused; whether the MCP
exposes it as readable data has never been inspected, which is why it carries a `notes` block saying
so. The expected contract:

```
read  -> sending domains and subdomains in use
         per domain: SPF / DKIM / DMARC / BIMI record presence and validity
         per domain: whether the verified identity aligns with the visible sender
         IP assignment (dedicated or shared), warm-up state, current sending limits
```

**One capability was refused.** Inbox placement. There is no seed-list account, no provider feed and
no mailbox-side evidence anywhere in this repository's understanding of the platform, and adding a
capability to justify a skill is exactly what `capabilities.yaml`'s own header forbids. The
consequence is written into the rules rather than hidden in a skill: `deliverability-rules.md#D7`
says placement is not observable from sending data and must not be inferred.

If a placement feed ever exists, the integration point is documented — see
[plugins/targetbay-email-sms/docs/email-quality-architecture.md](../plugins/targetbay-email-sms/docs/email-quality-architecture.md).

## Backlog, in the order that unblocks the most

1. **Contact-level journey membership** (`email_sms.automation`). Without it `campaign-conflict-resolver`
   cannot measure an overlap, and `email-quality-auditor` cannot count total contact. Two skills
   degrade to blocked or partial on one missing shape.
2. **Per-contact recent-contact counts across campaigns and automations** (`email_sms.campaign_analytics`).
   The same gap from the other side, and the input `consent-verification` needs to derive a ceiling.
3. **`email_sms.sending_infrastructure` verification.** Confirm it exists at all. If it does not, the
   identity layer is permanently unverifiable from here and `deliverability-qa` should say so in its
   `Purpose` rather than in its failure table.
4. **Engagement split by receiving domain** (`email_sms.campaign_analytics`). The closest available
   proxy for placement. Without it, D6 cannot be applied and three skills stay programme-wide.
5. **Field fill rates** (`email_sms.customer_intelligence`). The input that decides whether a
   personalised element ships or is dropped.
6. **Readable campaign instance, not just template** (`email_sms.template_management`). What
   `email-render-qa` and the auditor's rendering dimension actually inspect.
7. **Promotion configuration read** (`email_sms.campaign_management`). Needed to check an offer as
   written against the offer as configured, which is one of the auditor's four stop conditions.

Items 1 and 2 are the same underlying question — whether the platform can tell you what a single
contact has received recently — and answering it converts three skills from partial to complete.

## Related

- [mcp-capability-inventory.md](mcp-capability-inventory.md) — the repo-wide Phase 0 worksheet
- [plugins/targetbay-email-sms/capabilities.yaml](../plugins/targetbay-email-sms/capabilities.yaml) — the registry itself, and the only source of truth
- [plugins/targetbay-email-sms/docs/mcp-integration.md](../plugins/targetbay-email-sms/docs/mcp-integration.md) — why the indirection exists, and the per-plugin open questions
