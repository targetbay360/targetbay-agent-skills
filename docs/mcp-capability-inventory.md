# MCP Capability Inventory — Phase 0 worksheet

Every skill in this marketplace declares abstract capabilities, and every one of them currently maps to
`mcp_tools: TODO`. A TargetBay MCP exists and reportedly reads and writes across all three products, but
its surface has never been inspected from this repository. Until it is, no skill here can execute — they
can only plan.

Answering the questions below is what unblocks everything else.

**Do not guess.** A tool name invented here becomes confident, wrong documentation in four packages — the
exact failure the marketplace's own rules prohibit. An honest "the platform cannot do this" is more
useful than a plausible tool name.

## Where the answers go

**Straight into the registries**, not into this file. `plugins/<plugin>/capabilities.yaml` is the single
source of truth for what a capability is and what satisfies it, and it is the only place
`tests/validate.py` can police the answers. Transcribing the capability list into a worksheet and then
copying it back is two lists that drift.

| Registry | Capabilities | Flagged unverified |
|---|---|---|
| [`targetbay-email-sms`](../plugins/targetbay-email-sms/capabilities.yaml) | 18 | 2 |
| [`targetbay-reviews`](../plugins/targetbay-reviews/capabilities.yaml) | 14 | 1 |
| [`targetbay-loyalty`](../plugins/targetbay-loyalty/capabilities.yaml) | 14 | 1 |
| [`targetbay-onboarding`](../plugins/targetbay-onboarding/capabilities.yaml) | 15 | 1 |

That is 61 capabilities. For each one, fill in:

| Field | What goes in it |
|---|---|
| `mcp_tools` | The exact tool or resource names that satisfy it, with their binding arguments — `targetbay_query(dataset=customers)`, not a bare tool name that serves thirty capabilities. |
| `notes` | Required if you leave `mcp_tools: TODO` — say why. `tests/validate.py` enforces this as soon as any capability in that registry is mapped, so "not mapped yet" cannot quietly become "nobody looked". |

Record the shape of what each tool returns, and the OAuth scope it needs, in that plugin's
`docs/mcp-integration.md` — it carries a TODO list this work closes, plus the open questions below
stated per plugin.

The 4.2.0 email quality layer narrowed part of this for `targetbay-email-sms`: which unconfirmed
capability shapes block which of its newest skills, and what contract each would need, is written up in
[mcp-capability-gap-analysis.md](mcp-capability-gap-analysis.md). It also records the one capability
that was refused rather than invented — inbox placement — and why.

The rows that matter most are the ones each plugin's `docs/mcp-integration.md` lists under **Mapping
status** as open questions: capabilities this repository already suspects may not exist, or may belong
to the commerce platform rather than to TargetBay. Nine of the 60 carry such a question —
three in `targetbay-email-sms`, two in each of the others.

## The three answers that change the plan

1. **Does a write surface exist** for segments, journeys, templates, review triggers, loyalty
   configuration and onsite placements? If not, provisioning degrades to emitting a build checklist and
   the onboarding pipeline stops at an approved plan. Everything before that point is unaffected, which
   is why it is sequenced first.
2. **Are creation and activation separate operations?** If a single call creates and activates, the gate
   separating `mutation` from `high_impact` cannot be enforced by the host and has to be enforced by
   convention instead — a materially weaker position worth knowing about early.
3. **Is there a unified cross-product view of frequency and consent for one customer?** Without it the
   contact budget in an onboarding blueprint is a plan rather than an enforcement, and the blueprint has
   to say so on its face.

The remaining questions are per-plugin and live with their plugin — see each
`plugins/<plugin>/docs/mcp-integration.md`, whose TODO list this work closes. The onboarding plugin's
list is the longest, because it is the only one that needs all three products at once, plus every onsite
read and write:
[plugins/targetbay-onboarding/docs/mcp-integration.md](../plugins/targetbay-onboarding/docs/mcp-integration.md).

## The manual baseline

Capture this while the inspection is happening, because every later phase is measured against it and it
cannot be reconstructed afterwards.

| Question | Answer |
|---|---|
| How long does onboarding one store take today, end to end? | |
| How much of that is a person reading the store's admin UI? | |
| What gets configured for essentially every store, regardless of what the store is? | |
| What gets configured only when someone notices a reason? | |
| Where does onboarding most often stall? | |

The third row is the one that matters most: it is the list this project exists to replace with decisions.
