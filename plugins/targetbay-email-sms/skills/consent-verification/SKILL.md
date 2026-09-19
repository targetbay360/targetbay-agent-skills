---
name: consent-verification
description: Use when deciding how a store establishes and proves permission to message — whether people should have to confirm their address before anything is sent to them, whether that confirmation step is worth what it costs in signups, whether it applies to email, to SMS or to both, what to do with contacts imported or inherited with no provable consent record, and whether a re-permission pass is justified before a list is mailed again. Answers "should we use double opt-in?", "should we make people confirm their email before we send anything?" and "can we mail this list we acquired?". Use list-hygiene when the list is already consented and the problem is bounces or complaints, and audience-discovery when the question is who to target rather than who may lawfully be reached.
license: MIT
metadata:
  targetbay.display_name: Consent Verification
  targetbay.version: "1.0.0"
  targetbay.category: audience
  targetbay.requires: email_sms.suppression_and_consent, email_sms.customer_intelligence, email_sms.segmentation, email_sms.campaign_analytics, email_sms.store_profile
  targetbay.risk_level: recommendation
  targetbay.execution_mode: plan_then_execute
  targetbay.status: foundation
---

# Consent Verification

## Purpose

Decide how a store establishes and evidences permission to message, per channel — and decide what
happens to contacts whose permission cannot be evidenced at all.

Confirming everywhere loses real subscribers at the point of highest intent and gains nothing where
capture was already clean. Confirming nowhere accumulates typos, other people's addresses and records
of unknown origin, and the cost arrives as complaints and blocks. Make the trade explicitly rather
than defaulting either way.

This skill decides the policy; the capture and confirmation mechanics belong to the platform and to
[the best-practices skill](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/SKILL.md)
([../../rules/global-rules.md#G10](../../rules/global-rules.md)).

## When to Use

- Deciding whether to require a confirmation step before a contact enters the sending population
- A list has been imported, acquired or inherited and its origin cannot be evidenced
- Setting different consent requirements for email and SMS
- Deciding whether a re-permission pass is justified before mailing a list again
- Signup volume is healthy but complaint or bounce rates suggest the capture is not

## When Not to Use

- The list is consented and the problem is bounces, complaints or placement. Use
  [list-hygiene](../list-hygiene/SKILL.md).
- The question is who to target among contacts you may lawfully reach. Use
  [audience-discovery](../audience-discovery/SKILL.md).
- The question is which channel carries a message to a consented contact. Use
  [channel-optimization](../channel-optimization/SKILL.md).
- The store is being set up and consent is one item among many. Use
  [store-onboarding](../store-onboarding/SKILL.md), which routes back here for this decision.

## Required Context

| Context | Why it is needed | Without it |
|---|---|---|
| Consent state and its provenance per contact, per channel | Whether permission can be evidenced at all | Blocked |
| Capture points in use, and what each one asks for | A blanket policy cannot be set across mismatched capture | Blocked |
| Complaint and bounce rates by acquisition source | Whether the current capture is actually producing a problem | Blocked |
| Signup volume by source | What a confirmation step would cost in growth | Partial; the trade cannot be quantified |
| Jurisdictions the store's contacts sit in | Which regimes bind, and where SMS rules differ sharply from email | Partial; recommend the stricter reading and say so |
| Whether the platform can hold an unconfirmed pending state | Whether verification is a platform or an external step | Partial |

## Required MCP Capabilities

Defined in [../../capabilities.yaml](../../capabilities.yaml); mappings **TODO**.

| Capability | Used for |
|---|---|
| `email_sms.suppression_and_consent` | Consent state and provenance per channel; what is already suppressed |
| `email_sms.customer_intelligence` | Contact origin, acquisition source, engagement after signup |
| `email_sms.segmentation` | Sizing the unevidenced cohort and any re-permission audience |
| `email_sms.campaign_analytics` | Complaint and bounce rates by source, which is the evidence that capture is failing |
| `email_sms.store_profile` | Where the store and its contacts sit, and which capture points exist |

## Decision Process

```
1. Establish what consent evidence exists today, per channel, per source
2. Separate three populations
     evidenced · weakly evidenced · not evidenced at all
3. For the unevidenced: decide reachability             ← usually the answer is no, and no pass fixes it
4. Read complaint and bounce rate by source             ← is current capture actually failing?
5. Decide per channel, not once                         ← SMS is bound more tightly than email
6. Quantify what a confirmation step costs in signups   ← from this store's own volume
7. Set the requirement per capture point, not globally
8. Define the consent record: what is stored, and what it must prove
```

## Decision Rules

Binding: [../../rules/safety-rules.md](../../rules/safety-rules.md),
[../../rules/audience-rules.md](../../rules/audience-rules.md),
[../../rules/global-rules.md](../../rules/global-rules.md).

- A list with no provable consent record does not get mailed. No warm-up schedule, staged send or
  re-permission campaign launders it — a re-permission message to a list you may not mail is itself a
  message to a list you may not mail (S7).
- Consent is per channel (A10), and that includes a phone number sitting on an email-consented record.
- Deciding to require confirmation is a trade with a number on each side. State the expected signup
  loss from this store's own volume and the complaint exposure it removes; never assert that one
  outweighs the other without both (G2, G14).
- The decision is per capture point. A checkout box, a popup and an in-person signup have different
  evidence quality and may reasonably get different requirements.
- Consent evidence is what was agreed to, when, and through which capture point. A boolean flag with
  no provenance is not evidence and should be treated as weakly evidenced.
- Never infer consent from a transaction, an enquiry or the presence of contact details (A9, G12).
- Where jurisdiction is unknown, recommend on the stricter reading and record that it was a
  jurisdiction assumption rather than a finding (G15).
- Where the store insists on mailing an unevidenced list, this skill does not plan that send. It
  states the exposure and records the refusal (S8).
- Suppression state outranks any consent record. A suppressed contact stays suppressed regardless of
  what a later capture claims (S7).

## Workflow

| Phase | Action | Risk |
|---|---|---|
| DISCOVER | Read consent state and provenance, capture points, rates by source, signup volume | `read_only` |
| ANALYZE | Separate evidenced, weakly evidenced and unevidenced; quantify the trade | `analysis` |
| PLAN | Requirement per capture point per channel; treatment of the unevidenced; the consent record | `recommendation` |
| PREVIEW | Present the trade with both numbers, and the unevidenced cohort with its size | `recommendation` |
| VALIDATE | Run the checks below | — |
| APPROVE | Human approves the policy and any suppression | — |
| EXECUTE | Materialise the affected audiences | `mutation` |
| — | **Sending a re-permission message to an evidenced list** | `high_impact`, explicit approval |
| — | **Suppressing an unevidenced cohort** | `destructive`, explicit approval after reporting size |
| MEASURE | Signup volume and complaint rate after the change, against the pre-change baseline | — |

## Expected Output

A [skill result](../../schemas/skill-result.schema.json) containing: the three consent populations
with sizes; the confirmation requirement per capture point per channel, with the expected signup cost
and the complaint exposure removed; the treatment of the unevidenced cohort, including any refusal to
mail it; the consent record specification; jurisdiction assumptions made; and the risks.

## Validation

- [ ] Consent evidence assessed per channel, not once (A10)
- [ ] The three populations sized separately
- [ ] Unevidenced contacts not proposed for any send, including re-permission (S7)
- [ ] Signup cost quantified from this store's own volume, not asserted (G2)
- [ ] Complaint and bounce rates read by source before concluding capture is or is not failing
- [ ] Requirement set per capture point rather than globally
- [ ] Consent record specified: what was agreed, when, through which capture point
- [ ] No consent inferred from a transaction, an enquiry or the presence of contact details (A9)
- [ ] Jurisdiction assumptions recorded where jurisdiction is unknown (G15)
- [ ] Suppression state confirmed to outrank any capture record (S7)

## Approval Requirements

| Action | Risk | Approval |
|---|---|---|
| Read and analyse consent state | `read_only` / `analysis` | None |
| Recommend the policy | `recommendation` | None |
| Materialise an affected audience | `mutation` | Preview, then confirm |
| **Send a re-permission message to an evidenced list** | `high_impact` | **Explicit** |
| **Suppress an unevidenced cohort** | `destructive` | **Explicit**, after reporting size (S6) |
| **Mail a list with no provable consent record** | — | **Refused.** Not planned by this skill (S7, S8) |

## Examples

**"Should we make people confirm their email before we send anything?"**
Reads complaint and bounce rates by source and finds the popup producing most of both while the
checkout box produces almost none. Recommends confirmation on the popup only, quantifies the signup
loss from the store's own popup volume against the complaint exposure it removes, and leaves checkout
unchanged. Rejected: a store-wide requirement, which would have cost signups at the cleanest capture
point in exchange for nothing.

**"Import this list we bought and start the welcome series."**
Refuses. There is no consent record to evidence, so no send is planned — including a re-permission
message, which is itself a send to a list the store may not mail. States the exposure plainly:
complaint rate, provider blocks, and a reputation cost carried by every other send the store makes.
Offers the alternative that does work — capture these contacts through a channel where they act
first, verified at the point of signup. Rejected: the staged warm-up the store proposed, which
changes the rate of the exposure and not its nature.

## Failure Handling

| Situation | Response |
|---|---|
| Consent state or provenance unavailable | **Blocked.** A policy cannot be set without knowing what is evidenced today, and assuming consent is the error this skill exists to prevent (S12) |
| Capture points unknown | **Blocked.** A blanket policy across mismatched capture is either too strict at the clean points or too loose at the dirty ones |
| Complaint and bounce rates unavailable by source | **Partial.** Recommend on capture-quality reasoning alone, and state that the evidence for which source is failing is missing |
| Signup volume unavailable | **Partial.** Present the trade qualitatively and label the cost side as unquantified (G15) |
| Jurisdiction unknown | **Partial.** Recommend on the stricter reading and record the assumption |
| Platform cannot hold a pending unconfirmed state | **Partial.** The confirmation step is external; say so, and note the additional failure surface that adds |
| Store insists on mailing an unevidenced list | **Refused.** State the exposure, record the refusal and the reasoning, and stop. Do not produce a send plan for it (S8) |

Degraded outcomes set `status` and populate `unmet_requirements`.
