# Security

## What this package is

Markdown, YAML frontmatter and JSON Schema. It contains no executable code beyond a validation script, no
network calls, no credentials, and no customer data. Its security surface is mostly about what it tells an
agent to do, not what it does itself.

## Reporting a vulnerability

Use [private vulnerability reporting](https://github.com/targetbay360/targetbay-agent-skills/security/advisories/new),
or email `support@targetbay.com` if you cannot. **Do not open a public issue.**

Please include what the problem is, which files are involved, and what an attacker or a misconfigured
agent could cause. If the issue is that a skill could lead an agent to take an unsafe action, describe the
prompt or situation that would trigger it.

You will receive an acknowledgement, an assessment, and a fix or an explanation of why it is not a
vulnerability.

## Never in this repository

- API keys, tokens, OAuth client secrets, passwords
- Real customer records, email addresses, phone numbers or order data
- Real store identifiers, account IDs or tenant names
- Anything copied from a production database

Documentation figures are illustrative and labelled as such. If you need an example, invent an obviously
fictional one — never anonymise real data, which is frequently reversible.

## Credentials

Skills never handle credentials. Authentication to a TargetBay product is the agent host's and the
product MCP's responsibility. No skill should ever instruct an agent to read, store, transmit or log a credential.

See each plugin's `docs/mcp-integration.md`, for example
[bayengage-marketing](plugins/bayengage-marketing/docs/mcp-integration.md).

## Agent safety

The safety-relevant content of a plugin is its `rules/safety-rules.md`, for example
[bayengage-marketing](plugins/bayengage-marketing/rules/safety-rules.md). Treat a change that weakens one
as a security change:

- `high_impact` actions — anything reaching real recipients or spending budget — always stop for explicit
  human approval
- `destructive` actions require inspection and reporting of what is lost before approval
- Approval is scoped to the described action and does not extend to later or widened ones
- Consent, suppression and opt-out are never weakened, bypassed or routed around
- A capability that is unavailable is never simulated

A pull request that removes an approval gate, broadens an approval scope, or lets a skill proceed without
verified data is a security-relevant change and will be reviewed as one.

## Prompt injection

Skills instruct agents that read store data. That data can contain text written by third parties —
customer names, product descriptions, support messages, review content.

- Data read through capabilities is **data, not instructions**. No skill should treat content returned by a
  capability as a directive.
- Approval gates are the backstop: an injected instruction still cannot reach a recipient without a human
  approving a described action with a stated recipient count.
- If you add a skill that reads free-text customer or catalogue content, say explicitly in its
  `Failure Handling` section that such content is never followed as instruction.

## Data minimisation

Skills should ask for the aggregate they need rather than raw records. A skill that needs a segment size
should read the size, not the contacts. Recommendations and plans reference audiences by definition, never
by enumerating people.

## Supported versions

Each plugin versions independently; the current MINOR release line of a plugin receives fixes. See that
plugin's `CHANGELOG.md`, and [CHANGELOG.md](CHANGELOG.md) for repository-level changes.
