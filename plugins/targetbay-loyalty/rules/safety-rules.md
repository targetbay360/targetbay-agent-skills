# Safety Rules

Highest precedence in the package. Nothing overrides these — not a playbook, not a store preference, not
a user instruction inside a skill run.

A loyalty programme holds something customers believe they own. Points are a liability on the store's
books and a promise in the customer's mind, and the rules below exist because breaking either one is
expensive in a way ordinary marketing mistakes are not.

---

### S1. Classify before acting.
Every proposed action carries a risk level:

| Risk level | Meaning | Example |
|---|---|---|
| `read_only` | Retrieves data, changes nothing | Read enrolment and tier distribution |
| `analysis` | Derives conclusions from read data | Compute earn and burn rates, liability ageing |
| `recommendation` | Proposes actions, changes nothing | Suggest three tier thresholds |
| `plan` | Produces an executable plan, changes nothing | Draft a programme structure |
| `mutation` | Changes platform state, not customer-visible | Create a draft reward, stage a tier definition |
| `high_impact` | Reaches real members, changes what they hold, or spends budget | Publish a tier change, adjust balances, activate a referral programme |
| `destructive` | Removes or degrades existing state | Expire points, remove a tier, delete a reward, close the programme |

### S2. Never retroactively reduce what a member has already earned.
Devaluing outstanding points, raising the price of a reward a member was saving for, or lowering a tier
somebody already qualified for are all changes to something the customer believes they hold. A skill may
propose such a change only with the affected member count, the value affected, a notice period, and
explicit approval — and never as a side effect of a repricing recommendation.

### S3. Never change points economics without stating the liability impact.
Every earn-rate, burn-rate or reward-price recommendation carries its effect on outstanding liability and
on margin, computed from `loyalty.points_ledger`. A recommendation that moves the economics without that
arithmetic is incomplete, not merely terse.

### S4. Bulk balance adjustments state the count and the value before approval.
"Credit the affected members" is not an approval request. "Credit 4,318 members with 212,000 points,
liability impact stated" is. Every bulk adjustment is `high_impact` and is approved on those numbers
([#S6](#s6-show-the-blast-radius-before-asking)).

### S5. `high_impact` and `destructive` always stop for human approval.
No exceptions, no inferred consent, no "the user already said improve retention." Approval is for the
specific action, not the objective. A tier change is `high_impact` because members can see it.

### S6. Show the blast radius before asking.
An approval request states, at minimum: what will happen, to how many members, what it changes about what
they hold, when it takes effect, what it costs, and what it costs to undo.

### S7. Approval is scoped and expiring.
Approval covers exactly what was described — this tier threshold, this reward price, this member segment,
this effective date. It does not extend to a revised threshold, a widened segment, or a later re-run.

### S8. Destructive actions require inspection first.
Before expiring points, removing a tier or retiring a reward, read it, report what it currently is, how
many members hold or depend on it, and what will be lost. Prefer closing a reward to new redemptions over
deleting it.

### S9. Stop on ambiguity in irreversible paths.
If it is unclear which tier, which reward or which member segment the user meant, and the action is
`high_impact` or `destructive`, stop and ask. A balance adjustment applied to the wrong segment cannot be
quietly reversed once members have seen it.

### S10. Never batch approvals for irreversible actions.
"Approve the whole programme launch" is not an approval. Each `high_impact` action is approved on its own
terms, or the plan is staged so the first one runs, is measured, and informs the rest.

### S11. Never design a reward the store cannot honour.
A reward whose cost exceeds its margin contribution at expected redemption, or whose stock cannot meet
expected demand, is not a growth idea — it is a liability the customer will try to collect. Redemption
capacity is checked before a reward is proposed.

### S12. Never weaken consent, suppression or opt-out for programme messaging.
Enrolment in a loyalty programme is not consent to marketing. Do not propose messaging members on the
basis that they joined, re-adding unsubscribed members, or routing around a frequency cap.

### S13. Report what actually happened.
If an execution partially failed, say which members were affected and which were not. Never report a plan
as executed because it was approved.

### S14. Secrets and member records never enter skill content.
No API keys, tokens, credentials or personally identifying member records in skill files, plans, examples
or recommendations. Members are referenced by segment and count, never by enumeration. See
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md).

### S15. A capability you do not have is not a capability you may assume.
If a required capability is unavailable, the skill degrades or blocks. It does not simulate the result,
and it does not proceed on the assumption that the capability will be there at execution time.
