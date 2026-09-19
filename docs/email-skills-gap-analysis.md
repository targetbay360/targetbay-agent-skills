# Email Skills Gap Analysis

What an external email-discipline corpus ([aaron-he-zhu/aaron-marketing-skills](https://github.com/aaron-he-zhu/aaron-marketing-skills),
`email/`) covers, what `targetbay-email-sms` already covered, and what was built, merged or rejected as
a result. Produced for the 4.2.0 release.

The corpus was used as a **capability benchmark, not a source**. No wording was taken from it. What it
was useful for is the question it answers well: which decisions does a serious email programme have to
make? Two of its structural ideas were adopted — a pre-send gate that distinguishes *fixable* from
*never ship*, and the separation of authentication from reputation from content. Its scoring apparatus
was not: a fixed rubric of weighted items lets a genuine defect be offset by unrelated strengths, and
this package derives its thresholds from store data rather than from a published scale.

## The comparison

| Capability | In the benchmark | In `targetbay-email-sms` before 4.2.0 | Action | Reason |
|---|---|---|---|---|
| Pre-send quality gate | `email-quality-auditor` | Nothing | **Added** `email-quality-auditor` | Every dimension had an owner; nothing swept them together, so a send could be correct in each part and wrong as a whole |
| Authentication and reputation | `deliverability-qa` | One paragraph in `knowledge/email-principles.md`; `list-hygiene` owned the population layer only | **Added** `deliverability-qa` | A store whose authentication does not align was being routed to content fixes. The layer above list health had no owner |
| List hygiene, sunset, suppression | `list-hygiene-monitor` | `list-hygiene` 1.0.0 | **Enhanced** to 1.1.0 | Trend reading and receiving-domain splits were the gap, not the skill |
| Inbox placement monitoring | `inbox-placement-monitor` | Nothing | **Rejected as a skill; folded into `list-hygiene` and `deliverability-qa`** | No placement capability exists. A monitor with no seed-list or provider feed is a skill that cannot run, and shipping one would have implied data the platform does not have |
| Segment building | `list-segment-builder` | `audience-discovery` 2.1.0, in-degree 21 | **No change** | Targeting already lives in exactly one place, which is the stronger position |
| Email sequence design | `email-sequence-designer` | `automation-architect` 2.0.0 | **Enhanced** to 2.1.0 | Journey topology was already derived rather than templated. What it lacked was delegating product and offer choice instead of embedding them |
| Reactivation | `reactivation-specialist` | `customer-winback` 2.1.0 | **Merged** into `customer-winback` 2.2.0 | A separate skill would have owned nothing win-back does not. Dormancy classification and the sunset handoff were the real gaps |
| Frequency and preference management | `preference-frequency-manager` | `rules/frequency-rules.md` F1..F12, cited by every skill | **Merged** into `consent-verification` 1.1.0 | The rules existed; the ceiling they bound was never derived anywhere. Permission and cadence are one standing policy |
| Subject line generation and scoring | `subject-line-lab` | `content-optimization` 2.0.0, which owns subject lines | **Merged** into `content-optimization` 2.1.0 | A separate skill would have split one message's copy across two owners. Subject and preheader are now worked as one unit against a downstream metric |
| Email creative composition | `email-creative-builder` | `content-optimization`, plus the standalone `targetbay-email-template-design` reference skill | **Merged** into `content-optimization` 2.1.0 | Message architecture was the missing decision; the visual layer already had a home outside the plugin |
| Render and client QA | `email-render-builder` | Nothing in the plugin; `targetbay-email-template-design` held the design rules | **Added** `email-render-qa` | The rules existed as guidance with no skill applying them to a specific built message |
| Dynamic personalisation and fallbacks | `dynamic-content-personalizer` | `rules/personalization-rules.md` P1..P12, cited but never applied by a skill | **Added** `dynamic-content-personalizer` | Same shape as the frequency gap: binding rules, no owner |
| Experiment design | `send-experiment-designer` | `ab-testing` 2.0.0 | **Enhanced** to 2.1.0 | Sizing, thresholds and "inconclusive is a result" were already right. Holdout design and non-content dimensions were missing |
| List growth and capture | `list-growth-designer` | `consent-verification` for the policy; capture mechanics in the standalone best-practices skill | **Rejected** | Acquisition capture is a platform and onboarding concern. A skill here would have duplicated two existing homes |
| Newsletter monetisation | `newsletter-monetization-planner` | Nothing | **Rejected** | Sponsorship inventory and paid subscriptions are not an ecommerce store's email programme |
| B2B cold outbound | `cold-outbound-sequencer` | Nothing | **Rejected** | Outside this product. It also sits uneasily with `consent-verification`, which refuses to plan sends to contacts with no evidenced consent |

## Decisions the benchmark does not make, and this package does

The comparison above is one-directional by design — it asks what the benchmark has that this package
lacked. The reverse list is longer, and it is where the differentiation actually sits:

- **Which customers, derived from this store's data** — `audience-discovery`, `customer-lifecycle`,
  and the eight-stage lifecycle model behind them.
- **Which products, with the evidence rung named** — `product-recommendation-strategy`, and the five
  skills that route through it.
- **Whether to discount at all** — `offer-strategy`, which makes the null offer the default.
- **Email and SMS as one programme** — `channel-optimization` and a combined contact ceiling, rather
  than an email discipline with SMS bolted on.
- **Arbitration between contending sends** — `campaign-conflict-resolver`. Campaigns and automations
  share a budget that neither can see alone.
- **Automation portfolio reasoning** — `automation-strategy`, `automation-architect`,
  `automation-optimization`, `automation-orchestration`, `automation-recipe-selector`.
- **Explicit capability honesty** — every skill states what it could not read, and `blocked` and
  `partial` are first-class results rather than failure states.

## Skills proposed and not built

The release brief proposed sixteen new skills. Nine were not built because an existing skill or rule
family already owned the decision. Recording them here is the point of this document — the next person
to propose them should find the reasoning rather than the gap.

| Proposed | Already owned by |
|---|---|
| `send-time-optimization` | `skills/send-time-optimization/`, shipped in 4.1.0 under the same name |
| `list-hygiene-monitor` | `skills/list-hygiene/` |
| `channel-orchestration` | `skills/channel-optimization/`, extended in this release |
| `marketing-performance-analyzer` | `skills/opportunity-discovery/`, which scans every lens and routes each finding |
| `subject-line-lab` | `skills/content-optimization/` |
| `email-creative-builder` | `skills/content-optimization/` and `targetbay-email-template-design` |
| `customer-contact-policy` | `skills/consent-verification/` and `rules/frequency-rules.md` |
| `preference-frequency-manager` | as above |
| `inbox-placement-monitor` | `skills/list-hygiene/` and `skills/deliverability-qa/` |

Four documents the brief also proposed were not created, for the same reason:
`email-architecture.md` would restate
[plugins/targetbay-email-sms/docs/architecture.md](../plugins/targetbay-email-sms/docs/architecture.md);
`channel-orchestration.md` would restate
[the skill itself](../plugins/targetbay-email-sms/skills/channel-optimization/SKILL.md);
`deliverability.md` would restate
[knowledge/deliverability-principles.md](../plugins/targetbay-email-sms/knowledge/deliverability-principles.md);
and `skill-composition.md` would restate the composition graph in
[skills/README.md](../plugins/targetbay-email-sms/skills/README.md). The review standard for this
repository is whether the agent decides better, not whether text was added.

## Related

- [skill-priorities.md](skill-priorities.md) — what was built in what order, and what is next
- [mcp-capability-gap-analysis.md](mcp-capability-gap-analysis.md) — what the new skills need that the MCP may not provide
- [plugins/targetbay-email-sms/docs/email-quality-architecture.md](../plugins/targetbay-email-sms/docs/email-quality-architecture.md) — how the quality layer is composed
