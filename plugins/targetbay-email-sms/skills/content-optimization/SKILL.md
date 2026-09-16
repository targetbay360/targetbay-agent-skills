---
name: content-optimization
description: Use when the message itself is the problem — subject lines that under-deliver, body copy that does not convert, offers stated ambiguously, or content that no longer matches the audience it goes to. Produces content direction and testable variants, not finished creative. Use campaign-optimization first if it is not yet established that content is the failure point.
license: MIT
metadata:
  targetbay.display_name: Content Optimization
  targetbay.version: "2.0.0"
  targetbay.category: content
  targetbay.requires: email_sms.campaign_analytics, email_sms.template_management, email_sms.customer_intelligence, email_sms.product_intelligence, email_sms.segmentation
  targetbay.composes: ab-testing
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Content Optimization

## Purpose

Improve what a message says, once it is established that what it says is the problem.

This skill produces **content direction** — the angle, the proof, the offer statement, the single call to
action — not finished creative. That boundary is deliberate: the reasoning is portable across brands, and
the final wording belongs to the people who own the brand voice.

## When to Use

- Click rate is below baseline while reach and opens are not
- A message's premise no longer matches its audience
- An offer is stated ambiguously enough to produce support tickets
- Subject lines under-deliver against their bodies
- Content direction is needed for a planned campaign or journey node

## When Not to Use

- The failure point is not yet known. Use
  [campaign-optimization](../campaign-optimization/SKILL.md) first — most "content problems" are audience
  or offer problems.
- The audience is wrong. Use [audience-discovery](../audience-discovery/SKILL.md).
- A test needs designing. Use [ab-testing](../ab-testing/SKILL.md), which this skill composes.
- Finished creative is wanted. This package produces direction, not assets.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| The message content and its performance | The subject of the work | Blocked |
| The audience definition it went to | Content is judged against who received it | Blocked |
| Comparable messages from this store | What this store's audience responds to | Partial; lower confidence |
| The store's voice and terminology | Recommendations must sound like the store | Partial; keep direction structural |
| Product and offer facts | Claims must be supportable | Blocked for claims |
| Prior content test results | Avoids re-testing settled questions | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.campaign_analytics` | Message performance and comparisons |
| `email_sms.template_management` | Existing content and blocks; creating variants after approval |
| `email_sms.customer_intelligence` | Who the audience is and what they respond to |
| `email_sms.product_intelligence` | Product facts, stock, what can be claimed |
| `email_sms.segmentation` | The audience the content is judged against |

## Decision Process

```
1. Read the content against its audience   ← does the premise even apply to them?
2. Check the funnel position               ← which stage is the content responsible for?
3. Check the fundamentals                  ← one CTA, first-screen message, images-off, accessibility
4. Check the claims                        ← is every assertion supportable?
5. Check the offer statement               ← amount, applicability, exclusions, expiry, redemption
6. Identify the single largest weakness
7. Produce direction and a testable variant
```

## Decision Rules

Binding: [../../rules/content-rules.md](../../rules/content-rules.md),
[../../rules/personalization-rules.md](../../rules/personalization-rules.md),
[../../knowledge/email-principles.md](../../knowledge/email-principles.md),
[../../knowledge/sms-principles.md](../../knowledge/sms-principles.md).

- Content is judged against its audience, never in isolation (N1). A message with the wrong premise cannot
  be fixed by better wording.
- One primary call to action (N2).
- No claim the store cannot support — no invented statistics, scarcity or deadlines (N3).
- Subject line and body must agree (N4).
- Lead with the reason the message exists (N5).
- Write for the channel; never port email copy into SMS (N6).
- Offers stated exactly: amount, applicability, exclusions, expiry, redemption (N7).
- Accessibility is a requirement: alt text, contrast, descriptive links, works with images off (N8).
- Follow the store's voice where one exists; do not import generic marketing register (N10).
- Personalised elements need an empty-state that reads correctly (P2, P12).
- Mark judgement calls as testable rather than presenting them as settled (N12).
- Change one thing at a time if the change is going to be tested.

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read content, performance, audience, comparables, product facts | `read_only` |
| ANALYZE | Check premise, funnel position, fundamentals, claims, offer statement | `analysis` |
| PLAN | Content direction and a testable variant | `recommendation` |
| PREVIEW | Present the direction with the reasoning and the evidence | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the direction and the variant | — |
| EXECUTE | Create the variant template | `mutation` |
| — | **Sending it** | `high_impact`, separate approval |
| MEASURE | Via [ab-testing](../ab-testing/SKILL.md) where volume allows | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the weakness identified with its
evidence; content direction — angle, proof, offer statement, single call to action; the empty-state
behaviour for every personalised element; an accessibility check; what should be tested versus what should
simply be fixed; and the claims that need verification before sending.

## Validation

- [ ] Content judged against its actual audience (N1)
- [ ] One primary call to action (N2)
- [ ] Every claim supportable from product or store data (N3)
- [ ] Subject line and body agree (N4)
- [ ] Channel-appropriate — not ported between email and SMS (N6)
- [ ] Offer stated exactly (N7)
- [ ] Accessibility checked: alt text, contrast, links, images-off (N8)
- [ ] Empty state defined for every personalised element (P2)
- [ ] Judgement calls marked testable (N12)
- [ ] Store voice respected where one exists (N10)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Produce content direction | `recommendation` | None |
| Create a variant template | `mutation` | Preview, then confirm |
| **Send anything using it** | `high_impact` | **Explicit** |

## Examples

**"Rewrite this subject line, it's underperforming."**
Opens are at baseline; clicks are not. The subject line is doing its job. The body opens with brand
narrative and puts the reason for the message below the first screen. Recommends restructuring the body
lead (N5) and explicitly not changing the subject line — with the evidence for why.

**"This promotion generated support tickets."**
The offer statement omits exclusions and the expiry is stated only in the image, which fails with images
off (N7, N8). Recommends an exact offer statement in text, and flags that the underlying policy needs
confirming before the next send.

## Failure Handling

| Situation | Response |
|---|---|
| Content unreadable through the capabilities | **Blocked** |
| No comparable messages | **Partial.** Work from fundamentals, lower confidence, mark choices testable |
| Store voice unknown | Keep direction structural and flag that wording needs a brand owner |
| A claim cannot be verified | Remove it from the direction and say why (N3) |
| Audience mismatch is the real problem | Report that content changes will not fix it, and hand to [audience-discovery](../audience-discovery/SKILL.md) |
| Volume too low to test the change | Recommend fixing the objective faults outright and testing nothing |

Degraded outcomes set `status` and populate `unmet_requirements`.
