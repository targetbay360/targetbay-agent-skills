---
name: channel-optimization
description: Use when deciding how email and SMS should divide the work — which messages belong on which channel, how to sequence them, which contacts should be reached where, and whether SMS is worth its cost for a given moment. Also use when a store is introducing SMS and needs a channel strategy rather than a second copy of its email programme.
license: MIT
metadata:
  targetbay.display_name: Channel Optimization
  targetbay.version: "2.0.0"
  targetbay.category: optimization
  targetbay.requires: email_sms.customer_intelligence, email_sms.campaign_analytics, email_sms.automation_analytics, email_sms.segmentation, email_sms.suppression_and_consent, email_sms.messaging_sms
  targetbay.composes: audience-discovery
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Channel Optimization

## Purpose

Decide which channel carries which message, for whom, and in what order.

The failure this skill prevents: treating SMS as a louder email. Sending the same content on both channels
doubles the cost, doubles the fatigue, and adds nothing.

## When to Use

- A store is introducing SMS and needs a channel strategy
- Deciding which moments in a journey or sequence warrant SMS
- Email engagement is falling in a segment that may be reachable elsewhere
- SMS costs are rising without matching revenue
- Sequencing email and SMS around a deadline or launch

## When Not to Use

- The question is who to target rather than where to reach them. Use
  [audience-discovery](../audience-discovery/SKILL.md).
- A specific campaign underperformed. Use
  [campaign-optimization](../campaign-optimization/SKILL.md) first; channel may not be the failure.
- The content is the problem. Use [content-optimization](../content-optimization/SKILL.md).

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Consent state per channel per contact | A hard eligibility constraint | Blocked |
| Engagement by channel per segment | Which channel each group actually responds to | Blocked |
| SMS availability and cost | Whether SMS is an option and what it costs | Blocked for SMS |
| Message-level performance by channel | What each channel earns here | Partial; lower confidence |
| Quiet hours and local time configuration | Timing constraints, and legal ones for SMS | Blocked for SMS |
| Existing channel mix across campaigns and journeys | Current cadence per channel | Blocked |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.customer_intelligence` | Channel preference and engagement per segment |
| `email_sms.campaign_analytics` | Per-channel campaign performance |
| `email_sms.automation_analytics` | Per-channel node performance in journeys |
| `email_sms.segmentation` | Sizing channel-eligible audiences |
| `email_sms.suppression_and_consent` | Consent per channel, quiet hours, caps |
| `email_sms.messaging_sms` | SMS availability. **Unverified** — see [../../docs/mcp-integration.md](../../docs/mcp-integration.md) |

## Decision Process

```
1. Establish eligibility        ← consent per channel, per segment; SMS capability present?
2. Measure current mix          ← what each channel currently carries and earns
3. Classify each message        ← context-carrying, or time-critical single-action?
4. Assign channel by fit        ← not by availability
5. Check cost against value     ← SMS must clear a higher bar per message
6. Sequence complementary sends ← email explains, SMS deadlines
7. Check per-channel cadence    ← SMS has its own, smaller budget
8. Recommend, with what NOT to move
```

## Decision Rules

Binding: [../../knowledge/sms-principles.md](../../knowledge/sms-principles.md),
[../../knowledge/email-principles.md](../../knowledge/email-principles.md),
[../../rules/frequency-rules.md](../../rules/frequency-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md).

- Consent first, observed response second, cost third (R14).
- Email consent is never SMS consent (A10).
- SMS carries one idea, one link, one action. If the message needs explaining, it is an email (N6).
- Never duplicate the same content on both channels at the same moment. Complementary sequencing or
  nothing.
- SMS must clear a higher bar: the value of immediacy must exceed the cost per recipient.
- SMS cadence is tracked separately and is much smaller (F7). SMS opt-outs are usually permanent.
- Quiet hours and local time are planning constraints, not courtesies (F9).
- For a segment that has stopped opening email, a different channel is a stronger move than more email —
  where consent exists (F6).
- Where `email_sms.messaging_sms` is unavailable, produce an email-only strategy and record the gap
  rather than planning sends that cannot happen (S12).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read consent, per-channel engagement, current mix, costs, quiet hours | `read_only` |
| ANALYZE | Classify messages, measure per-channel value, size eligible audiences | `analysis` |
| PLAN | Channel assignment, sequencing, per-channel cadence | `recommendation` |
| PREVIEW | Present the mix with cost and reach implications | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves | — |
| EXECUTE | Applied by the owning campaign or automation skill | `mutation` |
| — | **Any SMS send** | `high_impact`, explicit, with count and cost |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: consented and eligible audience size
per channel; per-message channel assignment with the reason; complementary sequences where both channels
are used; per-channel cadence budget; SMS cost exposure at the recommended volume; messages explicitly
recommended to stay on email; and the quiet-hours and local-time constraints that apply.

## Validation

- [ ] Consent checked per channel, never assumed from email consent (A10)
- [ ] SMS capability availability confirmed before planning SMS (S12)
- [ ] Every SMS assignment justified by immediacy, not availability
- [ ] No duplicate content on both channels at the same moment
- [ ] SMS cost stated at the recommended volume
- [ ] Per-channel cadence budgets separate, with SMS the smaller (F7)
- [ ] Quiet hours and local time applied (F9)
- [ ] Messages that should stay on email named explicitly

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse | `read_only` / `analysis` | None |
| Recommend a channel mix | `recommendation` | None |
| Apply to campaigns or journeys | `mutation` | In the owning skill; preview then confirm |
| **Any SMS send** | `high_impact` | **Explicit**, with recipient count and cost |

## Examples

**"We're adding SMS — what should we send on it?"**
Consent analysis shows a fraction of the list is SMS-eligible. Recommends four moments: delivery and
order updates, restock notifications, the final day of a sale window, and high-value cart recovery.
Explicitly recommends *against* moving the newsletter, launches or educational content — each needs
context SMS cannot carry, and moving them would burn the channel within weeks.

**"Our SMS costs are up but revenue isn't."**
Finds SMS carrying promotional content that duplicates email sends. The cost is real, the incremental
revenue is not. Recommends cutting to deadline and operational moments, and reports the expected saving
alongside the reach that is given up.

## Failure Handling

| Situation | Response |
|---|---|
| `email_sms.messaging_sms` unavailable | **Partial.** Produce an email-only strategy; record where SMS would have been used |
| Consent data unavailable | **Blocked** for SMS; email-only recommendations proceed |
| No per-channel performance history | **Partial.** Assign by message type and mark the assignments testable |
| SMS cost unknown | State the cost exposure as unquantified and recommend confirming it before volume rises |
| Quiet-hours configuration unavailable | **Blocked** for SMS scheduling; this is a legal exposure, not a preference |
| SMS-eligible audience very small | Report it; a channel strategy for a handful of contacts is not worth building |

Degraded outcomes set `status` and populate `unmet_requirements`.
