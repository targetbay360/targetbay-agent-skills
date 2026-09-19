# Skill Priorities

What was built in `targetbay-email-sms` 4.2.0, in what order and why — and what is deliberately not
built. The reasoning matters more than the ordering: a priority list without its rejections gets
re-litigated every release.

## Built

### P0 — the decisions with no owner at all

| # | Skill | Why it ranked here |
|---|---|---|
| 1 | [`email-quality-auditor`](../plugins/targetbay-email-sms/skills/email-quality-auditor/SKILL.md) | The only skill that sits between a finished campaign and a real audience. Every other gap costs a worse decision; this one costs a wrong send |
| 2 | [`deliverability-qa`](../plugins/targetbay-email-sms/skills/deliverability-qa/SKILL.md) | Deliverability caps the ceiling on every other skill's output. A programme that does not reach the inbox makes all downstream reasoning conditional |
| 3 | [`dynamic-content-personalizer`](../plugins/targetbay-email-sms/skills/dynamic-content-personalizer/SKILL.md) | `personalization-rules.md` P1..P12 bound the whole corpus and no skill applied them to a specific message. Binding rules with no owner are guidance, not constraint |

### P1 — the decisions duplicated across several skills

| # | Skill | Why it ranked here |
|---|---|---|
| 4 | [`product-recommendation-strategy`](../plugins/targetbay-email-sms/skills/product-recommendation-strategy/SKILL.md) | Five skills were each choosing products. Built as a leaf, like `audience-discovery`, so the logic exists once |
| 5 | [`offer-strategy`](../plugins/targetbay-email-sms/skills/offer-strategy/SKILL.md) | C4 and C5 required a discount to be justified; nothing constructed the justification |
| 6 | [`campaign-conflict-resolver`](../plugins/targetbay-email-sms/skills/campaign-conflict-resolver/SKILL.md) | F8 required collisions to be resolved explicitly; nothing arbitrated them |
| 7 | [`email-render-qa`](../plugins/targetbay-email-sms/skills/email-render-qa/SKILL.md) | Ranked last of the seven because the rules already existed in a standalone reference skill — the gap was application, not knowledge |

Build order departed from this ranking for one practical reason: the link sweep in `tests/validate.py`
rejects a skill whose `When Not to Use` points at a skill that does not exist yet, so the leaves were
written first and shipped in one commit.

### Enhanced rather than duplicated

`consent-verification` 1.1.0 · `channel-optimization` 2.1.0 · `campaign-optimization` 2.2.0 ·
`automation-architect` 2.1.0 · `customer-winback` 2.2.0 · `ab-testing` 2.1.0 ·
`content-optimization` 2.1.0 · `list-hygiene` 1.1.0 · `opportunity-discovery` 2.1.0.

Each already owned the objective; each gained the decision that had been missing from it. The
reasoning per skill is in the [4.2.0 changelog entry](../plugins/targetbay-email-sms/CHANGELOG.md).

## Not built, and why

Nine skills were proposed and rejected because an existing skill or rule family already owned the
decision. The full table is in [email-skills-gap-analysis.md](email-skills-gap-analysis.md); the
short version:

| Rejected | Owner |
|---|---|
| `send-time-optimization` | Exists under that exact name since 4.1.0 |
| `list-hygiene-monitor` | `list-hygiene` |
| `channel-orchestration` | `channel-optimization` |
| `marketing-performance-analyzer` | `opportunity-discovery` |
| `subject-line-lab` | `content-optimization` |
| `email-creative-builder` | `content-optimization` and `targetbay-email-template-design` |
| `customer-contact-policy` | `consent-verification` and `frequency-rules.md` |
| `preference-frequency-manager` | as above |
| `inbox-placement-monitor` | `list-hygiene` and `deliverability-qa` — and no placement capability exists to run it on |

Three more were rejected as out of scope for an ecommerce email and SMS product:
`cold-outbound-sequencer`, `newsletter-monetization-planner`, `list-growth-designer`.

The standing test, from [skill-authoring.md](../plugins/targetbay-email-sms/docs/skill-authoring.md):
**does an existing skill already cover it?** Extending one is almost always better than adding a near
duplicate — `global-rules.md#G7` applied to this package itself. A second consideration is now
measurable: the `selection` eval scores every skill's description against every prompt with per-plugin
IDF, so each near-duplicate description makes every neighbour harder to find. Seven additions already
pushed one existing case out of the top three.

## What is next

Sequenced by what unblocks the most, not by what is most interesting.

1. **Verify the MCP surface.** Nothing here executes. The seven highest-value capability questions are
   ranked in [mcp-capability-gap-analysis.md](mcp-capability-gap-analysis.md); the top two are the
   same underlying question — can the platform say what one contact has received recently — and
   answering it converts three skills from partial to complete.
2. **Run the new skills against a real store.** Every threshold in this package is derived rather than
   fixed, which is correct and untested. The first real store will show which derivations produce a
   usable number and which produce "insufficient data" on a store that plainly has enough.
3. **Playbook overlays for the quality layer.** The five vertical playbooks predate these skills. A
   grocery store's contact ceiling and a furniture store's are not the same shape, and the overlay is
   where that belongs rather than in the skill.
4. **Execution, once a write surface is confirmed.** `email-quality-auditor` is `recommend_only` by
   design and should stay that way; what changes is whether the skills it gates can act on its verdict.
5. **Placement data, if it ever exists.** The integration point is documented in
   [email-quality-architecture.md](../plugins/targetbay-email-sms/docs/email-quality-architecture.md).
   Until then `deliverability-rules.md#D7` holds and the package says placement is unknown.

Candidate future skills, none of which are justified yet: a landing-page-to-email coherence check
(blocked — no capability sees the destination page), a cross-product contact reconciler (belongs to
`targetbay-onboarding`, which is the only plugin that may span products), and an SMS-specific quality
auditor (premature — `email_sms.messaging_sms` is still unverified).
