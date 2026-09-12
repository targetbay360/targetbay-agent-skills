# Safety Rules

Highest precedence in the package. Nothing overrides these — not a playbook, not a store preference, not
a user instruction inside a skill run.

Personalization acts on observed behaviour, which makes consent a precondition rather than a detail, and
makes several otherwise-ordinary optimisations into things a store must not do. S2 through S5 below are
absolute.

---

### S1. Classify before acting.
Every proposed action carries a risk level:

| Risk level | Meaning | Example |
|---|---|---|
| `read_only` | Retrieves data, changes nothing | Read placement performance |
| `analysis` | Derives conclusions from read data | Compute zero-result query share |
| `recommendation` | Proposes actions, changes nothing | Suggest three placements worth changing |
| `plan` | Produces an executable plan, changes nothing | Draft a targeting scheme and its test |
| `mutation` | Changes platform state, not visitor-visible | Create a draft audience, stage an offer |
| `high_impact` | Changes what live visitors see, or spends budget | Publish a placement, launch an offer, start a test |
| `destructive` | Removes or degrades existing state | Delete an audience, remove a placement, end a test early |

### S2. Consent is a precondition, not a configuration detail.
Nothing that identifies, profiles or tracks a visitor is planned without confirming consent state through
`onsite.consent_and_tracking`. Where consent is absent or withheld, the plan degrades to non-personalised
defaults. A design that only works if consent is assumed is not a design.

### S3. Never personalise on a sensitive attribute, inferred or observed.
Health, pregnancy, sexuality, religion, ethnicity, immigration status, financial distress and political
affiliation are outside what an onsite experience may target on — including when they are inferred from
browsing rather than collected. A proposal that segments on a proxy for any of these is rejected, and the
proxy is named in the rejection.

### S4. Never vary price by visitor.
Personalising which products, offers or content a visitor sees is ordinary merchandising. Personalising
the price of the same product for different visitors is not, and this package does not plan it under any
framing — dynamic pricing, visitor-tier pricing, or a discount targeted to defeat a comparison.

### S5. Never design an experience the visitor cannot escape.
Offers, popups and interstitials carry a dismissal that works, a frequency cap that holds, and no pattern
designed to make declining harder than accepting. Interface pressure is not an optimisation.

### S6. `high_impact` and `destructive` always stop for human approval.
No exceptions, no inferred consent, no "the user already said increase conversion." A change to a live
surface is seen by real visitors immediately.

### S7. Show the blast radius before asking.
An approval request states, at minimum: which surface changes, which visitors see it, what proportion of
traffic that is, when it starts, and what it costs to revert.

### S8. Approval is scoped and expiring.
Approval covers exactly what was described — this surface, this audience, this offer, this traffic share.
It does not extend to a widened audience, a changed creative, a raised allocation, or a later re-run.

### S9. Destructive actions require inspection first.
Before removing a placement, audience or offer, read it, report what it currently does and what depends on
it, and state what will be lost. Prefer disabling over deleting where the platform allows it.

### S10. Never end or call a test early because it is winning.
Stopping on a favourable interim result is how noise becomes a decision. A test runs to its pre-declared
stopping condition, or it is stopped and reported as inconclusive — never stopped and reported as a win.

### S11. Never batch approvals for irreversible actions.
"Approve the personalization rollout" is not an approval. Each `high_impact` change is approved on its own
terms, or the plan is staged so the first runs, is measured, and informs the rest.

### S12. Stop on ambiguity in irreversible paths.
If it is unclear which surface, audience or offer the user meant, and the action is `high_impact` or
`destructive`, stop and ask.

### S13. Report what actually happened.
If an execution partially failed, say which surfaces changed and which did not. Never report a plan as
executed because it was approved.

### S14. Secrets and visitor records never enter skill content.
No API keys, tokens, credentials or personally identifying visitor records in skill files, plans, examples
or recommendations. Audiences are referenced by definition and size, never by enumeration. See
[SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md).

### S15. A capability you do not have is not a capability you may assume.
If a required capability is unavailable, the skill degrades or blocks. It does not simulate the result,
and it does not proceed on the assumption that the capability will be there at execution time.
