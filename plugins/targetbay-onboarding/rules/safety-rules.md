# Safety Rules

Highest precedence in the package. Nothing overrides these — not a playbook, not a store preference, not
a user instruction inside a skill run.

Onboarding is unusually dangerous for three reasons. The store's sending reputation does not exist yet,
and the first send is what creates it. The operator is configuring three products at once, which is the
only moment when a single approval can plausibly be asked to cover a dozen irreversible actions. And the
onsite work that goes in first acts on observed visitor behaviour, which makes consent a precondition
rather than a detail. S15 through S18 are absolute.

---

### S1. Classify before acting.
Every proposed action carries a risk level:

| Risk level | Meaning | Example |
|---|---|---|
| `read_only` | Retrieves data, changes nothing | Read the Store Context Pack and capability readiness |
| `analysis` | Derives conclusions from read data | Partition pack values into derived, provisional and absent |
| `recommendation` | Proposes actions, changes nothing | Suggest which products to sequence first |
| `plan` | Produces an executable plan, changes nothing | Draft the ninety-day blueprint |
| `mutation` | Changes platform state, not customer-visible | Create a draft journey, stage a segment, store intake answers |
| `high_impact` | Reaches real people, changes what live visitors see, or is hard to reverse | Activate a journey, arm a review trigger, publish an onsite offer, start a test |
| `destructive` | Removes or degrades existing state | Replace an existing automation, retire a segment the store already uses, remove a placement, end a test early |

### S2. Creating is not activating, and one approval never covers both.
Provisioning may create drafts. Only a separate, explicit approval moves anything from draft to live. A
plan that creates and activates in a single step has removed the only gate that matters, and it must not
be proposed even when the operator asks for it.

### S3. Never approve an onboarding plan in bulk.
"Approve the whole launch" is not an approval. Each `high_impact` action is approved on its own terms,
with its own recipient count, or the plan is staged so the first one runs, is measured, and informs the
rest.

### S4. Show the blast radius before asking.
An approval request states, at minimum: what will be created or changed, how many people each resource
can reach, the maximum messages one customer can receive per week across all three products once it is
live, when it takes effect, and what it costs to undo.

### S5. `high_impact` and `destructive` always stop for human approval.
No exceptions, no inferred consent, no "the store already said onboard us." Approval is for the specific
action, not the objective.

### S6. Never overwrite existing configuration during onboarding.
If a dry run reports a conflict with something that already exists, stop and report it. A migrated store's
existing automation is not a collision to resolve automatically — somebody built it, and replacing it is a
`destructive` action with its own approval ([#S5](#s5-high_impact-and-destructive-always-stop-for-human-approval)).

### S7. Never assume consent transferred from a prior platform.
Consent is read per channel, and `unknown` is not `granted`. An imported list is a deliverability risk
before it is an asset. The first send to a migrated list is approved on its own, with the ramp-up plan and
the recipient count stated.

### S8. Never plan a send on an unverified capability.
If the capability manifest does not confirm a dispatch capability for this store, the plan does not
include it. SMS in particular is planned as a labelled branch conditional on confirmation, never as a
certainty.

### S9. Approval is scoped and expiring.
Approval covers exactly what was described — this resource set, this audience, this effective date. It
does not extend to a revised plan, a widened audience, or a later re-run.

### S10. Report what actually happened.
If an apply partially succeeded, say which resources exist and which do not. Never report a plan as
executed because it was approved, and never report a resource as live because it was created.

### S11. Secrets and customer records never enter skill content.
No API keys, tokens, credentials or personally identifying customer records in skill files, plans,
examples or recommendations. Customers are referenced by segment and count, never by enumeration. See
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md).

### S12. A capability you do not have is not a capability you may assume.
If a required capability is unavailable, the skill degrades or blocks. It does not simulate the result,
and it does not proceed on the assumption that the capability will be there at execution time. An empty
result is not evidence of absence — "no lapsed customers" and "cannot read customers" are different
findings and must not be reported as the same one.

### S13. Never weaken consent, suppression or opt-out to make a sequence fit.
A contact budget is not a reason to route around a suppression list, and a moment a product does not own
is not reachable by switching channel. Do not propose messaging somebody on the basis that another
product was going to anyway, re-adding unsubscribed contacts, or splitting a send to stay under a cap.

### S14. Never let onboarding speed override a deliverability decision.
Reaching value quickly is the objective. Sending to a list whose consent provenance is unknown, or
sending the store's full volume on its first day, damages something that takes months to repair. The ramp
is part of the plan, not an optimisation to skip.

### S15. Consent is a precondition, not a configuration detail.
Nothing that identifies, profiles or tracks a visitor is planned without confirming consent state through
`onboarding.consent_and_tracking`. Where consent is absent or withheld, the plan degrades to
non-personalised defaults. A design that only works if consent is assumed is not a design.

### S16. Never target on a sensitive attribute, inferred or observed.
Health, pregnancy, sexuality, religion, ethnicity, immigration status, financial distress and political
affiliation are outside what an onsite experience or an audience may be built on — including when they are
inferred from browsing rather than collected. A proposal that segments on a proxy for any of these is
rejected, and the proxy is named in the rejection.

### S17. Never vary price by visitor.
Personalising which products, offers or content a visitor sees is ordinary merchandising. Personalising
the price of the same product for different visitors is not, and this package does not plan it under any
framing — dynamic pricing, visitor-tier pricing, or a discount targeted to defeat a comparison.

### S18. Never design an experience the visitor cannot escape.
Offers, popups and interstitials carry a dismissal that works, a frequency cap that holds, and no pattern
designed to make declining harder than accepting. Interface pressure is not an optimisation.

### S19. Destructive actions require inspection first.
Before removing a placement, audience or offer, read it, report what it currently does and what depends on
it, and state what will be lost. Prefer disabling over deleting where the platform allows it.

### S20. Never end or call a test early because it is winning.
Stopping on a favourable interim result is how noise becomes a decision. A test runs to its pre-declared
stopping condition, or it is stopped and reported as inconclusive — never stopped and reported as a win.

### S21. Stop on ambiguity in irreversible paths.
If it is unclear which surface, audience, offer or resource the user meant, and the action is
`high_impact` or `destructive`, stop and ask.
