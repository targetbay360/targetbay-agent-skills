# Deliberately Not Shipped

Four patterns were requested and are **not** included in this skill. Each was a decision, not an
oversight, and the reason is recorded here rather than left as a silent gap — knowing why something is
absent is what stops it being asked for again.

## The refusals

### Cold outreach to contacts who did not opt in

Two requested patterns send marketing email to people who never subscribed — one scraping business
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

One requested pattern searches a mapping service for businesses, extracts addresses from their
websites, and mails them.

**Refused**, for the reasons above. Collecting an address from a website is not consent to market to
it, and being a business address does not change that in most jurisdictions.

### Invoice parsing and payment chasing

One requested pattern extracts amounts and due dates from invoice emails and drives payment reminders
through the marketing platform.

**Not shipped** — out of scope rather than unsafe. Accounts-receivable messaging has different
consent, different retention and different audit requirements from marketing, and running it through
a marketing sending reputation mixes two things that should stay apart. It is a reasonable
automation; it belongs somewhere else.

### Attachment routing

One requested pattern reads inbound attachments and forwards them to internal recipients.

**Not shipped** — internal document routing, not marketing automation. It also creates a path where
customer-supplied files are forwarded automatically, which wants a security review this skill is not
the place for.

## Adding to this file

A pattern belongs here when someone asked for it and the answer was no. Record what was asked for,
why it is not shipped, and what to do instead where there is an alternative. The reason is the part
that earns its place; the request on its own does not.

Where a refusal turns on how the sending platform behaves, that behaviour is described in
[How to Read a Recipe](./how-to-read-a-recipe.md) — the file most likely to go stale as the platform
changes, and worth re-reading before adding an entry that leans on it.
