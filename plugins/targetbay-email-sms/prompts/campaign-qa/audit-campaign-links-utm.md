---
title: Check Every Link Before Sending
summary: Mistargeted, untracked or unverifiable links in one campaign, with a send verdict.
skill: email-quality-auditor
---
Using TargetBay Email & SMS (`email-quality-auditor` skill), check every link in my campaign [CAMPAIGN NAME] before it goes out.

For each link give: visible text, destination as configured, UTM tracking parameters as read from the template and whether they're consistent, and whether a linked product is in stock at the price shown.

Also check the opt-out link and any personalised link's empty-data fallback.

Return:
- verdict: PASS, WARN or BLOCK
- each finding with its cost and fix
- links you cannot verify, named individually

Analysis only: change nothing.
