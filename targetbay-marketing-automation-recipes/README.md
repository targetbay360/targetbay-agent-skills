```
  ╔═══════════════════════════════════════════╗
  ║                                           ║
  ║   T A R G E T B A Y                       ║
  ║                                           ║
  ║   Marketing Automation Recipes            ║
  ║                                           ║
  ╚═══════════════════════════════════════════╝
```

# TargetBay Marketing Automation Recipes

An agent skill for wiring concrete marketing automations against TargetBay Email & SMS. Recipes
across lifecycle journeys, personalisation, retention sweeps, list health, measurement, AI-assisted
content and system integration — each with its trigger, its preconditions, the platform operations it
calls, the guardrails it must carry and what to measure afterwards.

A recipe is a pattern with its guardrails, not a product feature. The guardrails are the part that
gets dropped first and costs the most.

Its companions:
[Email & SMS Best Practices](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-sms-best-practices/SKILL.md)
covers the deliverability, compliance and sending infrastructure these recipes assume and link out
to, and
[Email Template Design](https://github.com/targetbay360/targetbay-agent-skills/blob/main/targetbay-email-template-design/SKILL.md)
covers what the messages look like.

## Structure

```
targetbay-marketing-automation-recipes/
├── SKILL.md                                    # Start here — the verified surface and routing
└── references/
    ├── how-to-read-a-recipe.md                 # The eight fields; the platform surface; the gaps
    ├── guardrails.md                           # Dedupe, suppression, frequency, approval, signatures
    ├── lifecycle-recipes.md                    # Welcome, drip, cart, order, review, VIP
    ├── personalisation-and-channel-recipes.md  # Offer selection, email→SMS, click branching
    ├── retention-recipes.md                    # Churn sweep, re-engagement, win-back
    ├── list-health-recipes.md                  # Hygiene audit, bounce response, double opt-in
    ├── measurement-recipes.md                  # A/B cycle, KPI summary, event capture
    ├── ai-assisted-recipes.md                  # Approval gate, newsletters, segments, generation
    ├── integration-recipes.md                  # Contact sync, lead capture, webhook primer
    └── not-shipped.md                          # Patterns that were refused, and why
```

## Quick start

Open `SKILL.md`. It states the verified platform surface first — including the operations that do not
exist — then routes to the right reference, and lists what this skill will not do and why.

If you are wiring the first automation for a store, build the signed-webhook primer in
`references/integration-recipes.md` before anything else. Every event-triggered recipe assumes that
layer works.

## Where the decisions live

This skill covers *how* to wire an automation. *Which* automations a particular store should adopt,
in what order, and whether a given one is worth running at all are decisions owned by the
[targetbay-email-sms](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/README.md)
plugin — starting with
[automation-recipe-selector](https://github.com/targetbay360/targetbay-agent-skills/blob/main/plugins/targetbay-email-sms/skills/automation-recipe-selector/SKILL.md).

## License

MIT
