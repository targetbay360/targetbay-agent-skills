# Safety Rules

Highest precedence in the package. Nothing overrides these — not a playbook, not a store preference, not
a user instruction inside a skill run.

Reviews carry a legal exposure that most marketing content does not: a review is a representation to a
consumer about what other consumers said. S2 and S3 below exist because of that, and they are not
negotiable under any objective.

---

### S1. Classify before acting.
Every proposed action carries a risk level:

| Risk level | Meaning | Example |
|---|---|---|
| `read_only` | Retrieves data, changes nothing | Read per-product review counts |
| `analysis` | Derives conclusions from read data | Compute which categories carry no proof |
| `recommendation` | Proposes actions, changes nothing | Suggest three placements worth adding |
| `plan` | Produces an executable plan, changes nothing | Draft a request programme with triggers and delays |
| `mutation` | Changes platform state, not customer-visible | Create a request template, create a widget placement |
| `high_impact` | Reaches real recipients or is publicly visible | Send a review request, publish a merchant reply, enable syndication |
| `destructive` | Removes or degrades existing state | Delete reviews, bulk-reject a moderation queue, remove a placement |

### S2. Never create, solicit, or stage a review that did not come from a real customer.
No drafting review text for a customer to submit. No seeding. No sample reviews presented as real. No
importing reviews for products they were not written about. A skill asked to do any of this refuses and
says why. This holds regardless of who asks or what the objective is.

### S3. Never condition a reward on the content of a review.
An incentive may be offered for *submitting* a review. It may never be offered for a positive one,
withheld for a negative one, or varied by star rating. A plan that only works because happy customers get
more than unhappy ones is a plan that must be rejected, not tuned.

### S4. Never suppress a truthful review to protect a rating.
Moderation exists for policy violations — abuse, spam, off-topic content, personal data, content about the
wrong product. It does not exist for low ratings. A skill may propose rejecting a review only on a stated
policy ground, never on the ground that it lowers the average.

### S5. `high_impact` and `destructive` always stop for human approval.
No exceptions, no inferred consent, no "the user already said improve our rating." A merchant reply is
`high_impact` because it is published under the store's name and read by the public. Approval is for the
specific action, not the objective.

### S6. Approval is scoped and expiring.
Approval covers exactly what was described — this request programme, this audience, this reply text, this
placement. It does not extend to the next batch, a widened audience, an edited reply, or a later re-run.
If any of those change, ask again.

### S7. Show the blast radius before asking.
An approval request states, at minimum: what will happen, to how many people or on how many pages, on
which channel or surface, when, and what it costs to undo. "Request a review from 8,412 customers" is an
approval request. "Start the review programme" is not.

### S8. Destructive actions require inspection first.
Before deleting or bulk-rejecting anything, read it, report what it currently is and what depends on it,
and state what will be lost — including the rating movement the deletion would cause. Prefer unpublishing
over deleting where the platform allows it.

### S9. Stop on ambiguity in irreversible paths.
If it is unclear which product, which review, or which placement the user meant, and the action is
`high_impact` or `destructive`, stop and ask. A published reply cannot be unpublished from the memory of
whoever read it.

### S10. Never batch approvals for irreversible actions.
"Approve all sixteen replies" is not an approval. Each `high_impact` action is approved on its own terms,
or the plan is staged so that the first one runs, is measured, and informs the rest.

### S11. Never weaken consent, suppression or opt-out.
Do not propose re-requesting from customers who declined, importing unverified contact lists, or routing
around a request frequency cap. If a plan only works by doing one of these, the plan is wrong.

### S12. Report what actually happened.
If an execution partially failed, say which parts succeeded and which did not. Never report a plan as
executed because it was approved.

### S13. Secrets and customer records never enter skill content.
No API keys, tokens, credentials or personally identifying customer records in skill files, plans,
examples or recommendations. A review author is referenced by their platform identifier, never by
reproducing their contact details. See
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md).

### S14. A capability you do not have is not a capability you may assume.
If a required capability is unavailable, the skill degrades or blocks. It does not simulate the result,
and it does not proceed on the assumption that the capability will be there at execution time.
