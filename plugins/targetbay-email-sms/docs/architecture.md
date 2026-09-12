# Architecture

## The layering

```
┌──────────────────────────────────────────────┐
│ AI Agent host                                │  loads skills, matches intent
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Email & SMS Marketing Skills       │  ← this package
│   skills · rules · knowledge · playbooks     │     HOW to decide
└──────────────────┬───────────────────────────┘
                   ▼  declares required capabilities
┌──────────────────────────────────────────────┐
│ TargetBay Email & SMS MCP                                │  ← separate repository
│   tools and resources                        │     WHAT can be done
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│ TargetBay Email & SMS platform                           │  data and execution
└──────────────────────────────────────────────┘
```

The boundary is the point of the package. Skills reason; the MCP acts. Neither reimplements the other, and
both version independently.

## What lives where

| Concern | Owner | Example |
|---|---|---|
| Reading a customer, creating a campaign, sending | **TargetBay Email & SMS MCP** | The capability to create a segment |
| Which customers to target | **Skills** | Deciding that first-time buyers need their own journey |
| What is never acceptable | **Rules** | Never personalise on unverified data |
| Why something works | **Knowledge** | Why the first-to-second purchase transition matters |
| Vertical defaults | **Playbooks** | Beauty stores lead with replenishment |
| Consent, suppression, hard caps | **TargetBay Email & SMS platform** | Enforcement, not restatement |

If a question is "can the platform do X?", it belongs to the MCP. If it is "should we do X, for whom, and
in what order?", it belongs here.

## The four internal layers

```
skills/      objective → decisions → plan → execution sequence
   │  cites
   ├─▶ rules/        constraints that bind every skill
   ├─▶ knowledge/    durable marketing theory
   └─▶ playbooks/    vertical overlays that adjust defaults
```

Skills link to the other three by relative path. Nothing is copy-pasted between them: a constraint
restated in fourteen skills drifts in fourteen directions.

## Composition

Skills delegate to other skills through `metadata.targetbay.composes` in the frontmatter. The graph is
validated to stay
acyclic, and `audience-discovery` sits at the bottom of it — every targeting question routes through one
implementation. See [../skills/README.md](../skills/README.md) for the current graph.

Composition is conceptual: a composing skill defers a decision to another skill's reasoning. It is not a
function call, and this package defines no runtime.

## Execution lifecycle

Every skill that can eventually change platform state moves through these phases. A skill declares how far
it is permitted to go with `targetbay.execution_mode`.

```
DISCOVER   read the store's actual state                         read_only
   ↓
ANALYZE    derive conclusions from what was read                 analysis
   ↓
PLAN       produce a concrete, reviewable plan                   plan
   ↓
PREVIEW    show exactly what will change, and to how many        plan
   ↓
VALIDATE   run the skill's own checks                            plan
   ↓
APPROVE    a human decides                                       —
   ↓
EXECUTE    apply through TargetBay Email & SMS MCP                           mutation / high_impact
   ↓
VERIFY     confirm what was created matches what was approved    read_only
   ↓
MEASURE    read the outcome against the stated expectation       read_only
   ↓
OPTIMIZE   feed the result into the next decision                —
```

Phases are not optional steps to be skipped when the answer seems obvious. PREVIEW and APPROVE exist
precisely for the cases where the agent is confident and wrong.

## Risk classification

| Level | Meaning | Approval |
|---|---|---|
| `read_only` | Retrieves data, changes nothing | None |
| `analysis` | Derives conclusions from read data | None |
| `recommendation` | Proposes actions, changes nothing | None |
| `plan` | Produces an executable plan, changes nothing | None |
| `mutation` | Changes platform state, not customer-visible | Preview, then confirm |
| `high_impact` | Reaches real recipients or spends budget | **Explicit, per action** |
| `destructive` | Removes or degrades existing state | **Explicit, after inspection** |

A skill's `targetbay.risk_level` declares the highest class it can reach. The binding rules are in
[../rules/safety-rules.md](../rules/safety-rules.md).

## Execution modes

| Mode | The skill may |
|---|---|
| `analyze_only` | Read and analyse. Nothing else |
| `recommend_only` | Also propose actions, without planning execution |
| `plan_then_execute` | Also produce an executable plan, and execute it after approval |
| `execute_with_approval` | Execute within an approved scope, stopping at each `high_impact` step |

## Contracts

Four JSON Schemas define the machine-readable surface:

| Schema | Defines |
|---|---|
| [skill.schema.json](../schemas/skill.schema.json) | Skill frontmatter |
| [recommendation.schema.json](../schemas/recommendation.schema.json) | How a proposal is stated, with its evidence |
| [workflow.schema.json](../schemas/workflow.schema.json) | An automation or sequence plan |
| [skill-result.schema.json](../schemas/skill-result.schema.json) | What a skill returns, including partial and blocked |

`blocked` and `partial` are first-class results. A skill that cannot get the data it needs says so rather
than filling the gap.

## Capabilities

Skills declare abstract capability identifiers — `email_sms.customer_intelligence`, not a tool name. The
registry is [../capabilities.yaml](../capabilities.yaml) and the mapping to real MCP tools is **TODO**.
See [mcp-integration.md](mcp-integration.md) for why this indirection exists.

## Vendor neutrality

The package is Markdown, YAML frontmatter and JSON Schema. No runtime, no host-specific behaviour, no
dependency on a particular agent framework.

Every skill conforms to the [Agent Skills specification](https://agentskills.io/specification), which any
host implementing that format loads unmodified. The specification closes the top level of the frontmatter
to six fields and its reference validator rejects the rest, so everything this package adds — display
name, version, category, required capabilities, composition, risk level, execution mode, status — lives
under `metadata` as `targetbay.*` string values. A host that does not read them simply sees a skill with
a `name` and a `description`, which is the whole point.

`tests/validate.py` runs that reference validator in its `spec` group, so conformance is a test rather
than a claim.
