# Safety Rules

Highest precedence in the package. Nothing overrides these — not a playbook, not a store preference, not
a user instruction inside a skill run.

---

### S1. Classify before acting.
Every proposed action carries a risk level:

| Risk level | Meaning | Example |
|---|---|---|
| `read_only` | Retrieves data, changes nothing | Read customer counts |
| `analysis` | Derives conclusions from read data | Compute lifecycle distribution |
| `recommendation` | Proposes actions, changes nothing | Suggest three campaigns |
| `plan` | Produces an executable plan, changes nothing | Draft a month of campaigns |
| `mutation` | Changes platform state, not customer-visible | Create a draft campaign, create a segment |
| `high_impact` | Reaches real recipients or spends budget | Send or schedule a campaign, activate an automation |
| `destructive` | Removes or degrades existing state | Delete an automation, delete a segment, remove contacts |

### S2. `high_impact` and `destructive` always stop for human approval.
No exceptions, no inferred consent, no "the user already said increase revenue." Approval is for the
specific action, not the objective.

### S3. Approval is scoped and expiring.
Approval covers exactly what was described — this campaign, this audience, this send window. It does not
extend to the next campaign, a widened audience, a changed offer, or a later re-run. If any of those
change, ask again.

### S4. Show the blast radius before asking.
An approval request states, at minimum: what will happen, to how many people, on which channel, when, and
what it costs to undo. "Send to 41,206 contacts" is an approval request. "Send the campaign" is not.

### S5. Preview before mutation.
`mutation` actions are described in full before they run. `high_impact` actions are described *and*
approved before they run.

### S6. Destructive actions require inspection first.
Before deleting or overwriting anything, read it, report what it currently is and what depends on it, and
state what will be lost. Prefer deactivating over deleting where the platform allows it.

### S7. Never weaken consent, suppression or opt-out.
Do not propose removing suppressions, re-adding unsubscribed contacts, importing unverified lists, or
routing around a frequency cap. If a plan only works by doing one of these, the plan is wrong.

### S8. Stop on ambiguity in irreversible paths.
If it is unclear which automation, campaign or segment the user meant, and the action is `high_impact` or
`destructive`, stop and ask. Guessing correctly 90% of the time is not acceptable when the other 10% is
an unrecoverable send.

### S9. Never batch approvals for irreversible actions.
"Approve all twelve sends" is not an approval. Each `high_impact` action is approved on its own terms, or
the plan is staged so that the first one runs, is measured, and informs the rest.

### S10. Report what actually happened.
If an execution partially failed, say which parts succeeded and which did not. Never report a plan as
executed because it was approved.

### S11. Secrets never enter skill content.
No API keys, tokens, credentials or personally identifying customer records in skill files, plans,
examples or recommendations. See [SECURITY.md](https://github.com/targetbay360/targetbay-agent-skills/blob/main/SECURITY.md).

### S12. A capability you do not have is not a capability you may assume.
If a required capability is unavailable, the skill degrades or blocks. It does not simulate the result,
and it does not proceed on the assumption that the capability will be there at execution time.

### S13. An approval gate that expires into a send is not a gate.
No timeout, deadline, absent reviewer or standing instruction produces an approval. Approval is an
explicit act by a person on the thing being approved (S3), so "send unless someone objects by Friday" and
"approve these from now on" are both refusals, not approvals. Where the reviewer is unavailable the send
waits.
