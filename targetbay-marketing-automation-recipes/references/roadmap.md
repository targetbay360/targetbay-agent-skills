# Roadmap and Deliberately Not Shipped

**Nothing in the first section is built.** These are ideas catalogued from a specification document,
not recipes — there is no workflow behind any of them and none of them can be imported or run. They
are here because knowing what is *not* available, and what each one would need first, is more useful
than discovering it halfway through building.

The second section records what was deliberately refused, and why. That is a decision on the record,
not an omission.

## Status markers

| Marker | Meaning |
|---|---|
| **Shipped** | Already covered by a recipe in this skill, sometimes under a different name |
| **Verified** | Everything it needs exists on the inspected surface; it is unbuilt, not blocked |
| **Unverified** | Depends on something the inspection did not prove either way |
| **Not exposed** | Needs something the inspected surface does not offer at all |

## The catalogue

| Idea | Extends | Needs | Status |
|---|---|---|---|
| Predictive send-time optimisation | — | Per-contact engagement timestamps, and a way to schedule per recipient | **Not exposed** |
| Smart re-send to non-openers | Measurement | Per-contact open data from reports, and a send to a derived sub-audience | **Unverified** |
| Multi-source newsletter aggregation | Newsletter assembly | — | **Shipped** |
| Personalised newsletter | Newsletter assembly | Per-recipient content variation within one campaign | **Unverified** |
| Product restock alert | — | An availability event, and a waitlist of who asked | **Not exposed** |
| Price drop notification | — | A price-change event, and view or save history | **Not exposed** |
| Repeat purchase reminder | Retention | Per-contact purchase intervals | **Verified** |
| Post-review thank-you | Lifecycle | A review event from the reviews product | **Unverified** |
| Lifecycle stage migration | — | A stage field on the contact, and transition detection | **Verified** |
| Ads audience retargeting sync | Contact sync | An advertising platform integration; consent to share data with it | **Not exposed** |
| CRM sync | Contact sync | — | **Shipped** |
| Campaign KPI dashboard | KPI summary | A dashboard destination rather than an email | **Shipped**, in a different shape |
| Bounce rate monitor | Bounce response | — | **Shipped** |
| Deliverability health monitor | Hygiene audit | Reputation and placement signals the platform does not surface | **Not exposed** |
| UTM link aggregation | Event capture | Per-link click data with UTM parameters preserved | **Unverified** |
| Sentiment-based campaign adjustment | — | A sentiment source, and per-campaign content adjustment | **Not exposed** |
| Performance summary writer | KPI summary | The approval gate, since it generates prose about the business | **Verified** |
| Dynamic content testing | A/B cycle | Per-block variation and per-block reporting within one campaign | **Not exposed** |
| Pre-order launch | — | A waitlist, and an inventory-independent purchase path | **Unverified** |
| Daily trend email | Newsletter assembly | A trend source | **Verified** |

The strategic questions behind several of these are owned by skills rather than recipes:
[send-time-optimization](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/send-time-optimization/SKILL.md)
for the first row,
[stock-and-price-alerts](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/stock-and-price-alerts/SKILL.md)
for restock, price drop and pre-order,
[customer-lifecycle](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/customer-lifecycle/SKILL.md)
for stage migration, and
[campaign-optimization](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/campaign-optimization/SKILL.md)
for the non-opener re-send. The idea being unbuilt does not mean the decision is unowned.

## Deliberately not shipped

Four patterns exist in the source material and are **not** included here. Each was a decision, not an
oversight.

### Cold outreach to contacts who did not opt in

Two source workflows send marketing email to people who never subscribed — one scraping business
listings for addresses, the other working through a purchased spreadsheet.

**Refused.** It is unlawful under CAN-SPAM's and GDPR's consent requirements as documented in
[Compliance](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/references/compliance.md),
and it collides with
[safety-rules.md#S7](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/rules/safety-rules.md).

The commercial reason is sharper than the legal one. Sending reputation on a marketing platform is
shared infrastructure: one customer mailing a scraped list degrades inbox placement for every other
customer on the same sending pool. An ESP publishing a cold-outreach recipe under its own name is
handing its customers a way to damage each other.

**What to do instead:** inbound lead capture in
[Integration Recipes](./integration-recipes.md), with the verification flow in
[List Health Recipes](./list-health-recipes.md). It is slower and it works.

### Address scraping

One source workflow searches a mapping service for businesses, extracts addresses from their
websites, and mails them.

**Refused**, for the reasons above. Collecting an address from a website is not consent to market to
it, and being a business address does not change that in most jurisdictions.

### Invoice parsing and payment chasing

One source workflow extracts amounts and due dates from invoice emails and drives payment reminders
through the marketing platform.

**Not shipped** — out of scope rather than unsafe. Accounts-receivable messaging has different
consent, different retention and different audit requirements from marketing, and running it through
a marketing sending reputation mixes two things that should stay apart. It is a reasonable
automation; it belongs somewhere else.

### Attachment routing

One source workflow reads inbound attachments and forwards them to internal recipients.

**Not shipped** — internal document routing, not marketing automation. It also creates a path where
customer-supplied files are forwarded automatically, which wants a security review this skill is not
the place for.

## Adding to this file

An idea belongs here when someone asked for it and the answer was "not yet". Record what it would
extend, what it needs, and which of the four markers applies. When something moves from **Unverified**
to **Verified**, the thing that changed is worth recording in
[How to Read a Recipe](./how-to-read-a-recipe.md) too — that file is where the surface is described,
and it is the one that goes stale first.
