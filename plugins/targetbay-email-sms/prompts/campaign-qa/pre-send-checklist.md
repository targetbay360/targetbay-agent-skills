---
title: Is This Campaign Ready to Send?
summary: One PASS, WARN or BLOCK verdict covering audience, consent, content, offer, links and collisions.
skill: email-quality-auditor
---
Using TargetBay Email & SMS (`email-quality-auditor` skill), run the full pre-send check on [CAMPAIGN NAME].

Sweep the resolved audience and exclusions, consent and suppression, recent contact for these people, personalisation fallbacks, links, opt-out, offer terms as stated versus configured, product stock and price, rendering, collisions with other sends and automations, and my sending programme's current health.

Return:
- verdict: PASS, WARN or BLOCK, blocking condition first
- resolved audience size
- each finding with cost and fix
- what I'm accepting if I send on WARN
- checks you couldn't run, named individually

Analysis only: change nothing.
