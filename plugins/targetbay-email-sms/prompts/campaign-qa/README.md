# Campaign QA prompts

Checks to run on a built campaign, SMS or test before anything reaches a customer. Each prompt routes to one skill in this plugin.

| Prompt | What you get | Skill |
|---|---|---|
| [Check Every Link Before Sending](audit-campaign-links-utm.md) | Mistargeted, untracked or unverifiable links in one campaign, with a send verdict. | [`email-quality-auditor`](../../skills/email-quality-auditor/SKILL.md) |
| [Make My Email Readable for Everyone](audit-email-accessibility.md) | An accessibility check on alt text, contrast, link text and reading order, with must-fix items. | [`email-render-qa`](../../skills/email-render-qa/SKILL.md) |
| [Check Logo, Hero and CTA on Mobile](check-image-size-and-cta-placement.md) | Whether my logo, hero image and main call to action hold up on phones and with images off. | [`email-render-qa`](../../skills/email-render-qa/SKILL.md) |
| [Find Deliverability Risks Hiding in Segments](audit-segment-deliverability-risks.md) | Where bounces, complaints and never-engaged contacts concentrate, with a suppression and sunset plan. | [`list-hygiene`](../../skills/list-hygiene/SKILL.md) |
| [Clear My SMS Messages Before Sending](audit-sms-compliance.md) | A PASS, WARN or BLOCK verdict on an SMS campaign or automation covering consent, opt-out and timing. | [`email-quality-auditor`](../../skills/email-quality-auditor/SKILL.md) |
| [Check Opt-Out and Sender Details](check-email-opt-out-and-sender-details.md) | Whether an email's unsubscribe link, sender identity and footer meet commercial email law. | [`email-quality-auditor`](../../skills/email-quality-auditor/SKILL.md) |
| [Confirm the Send Time Fits This Audience](check-send-time-fit.md) | Whether a campaign's send time and time zone suit its audience, bounded by quiet hours. | [`send-time-optimization`](../../skills/send-time-optimization/SKILL.md) |
| [Prove My SMS Consent Holds Up](check-sms-opt-in-compliance.md) | Whether every texted contact's consent is evidenced by capture point, and what to do with the rest. | [`consent-verification`](../../skills/consent-verification/SKILL.md) |
| [Gate Generated SMS Copy for Restricted Content](check-sms-restricted-content.md) | Sign-off rules that stop restricted topics and unsupported claims in generated SMS before it goes out. | [`ai-content-governance`](../../skills/ai-content-governance/SKILL.md) |
| [Tighten an SMS That Reads Like Spam](evaluate-sms-quality.md) | Length, spam-signal and clarity fixes for one SMS, plus what to fix versus test. | [`content-optimization`](../../skills/content-optimization/SKILL.md) |
| [Is This Campaign Ready to Send?](pre-send-checklist.md) | One PASS, WARN or BLOCK verdict covering audience, consent, content, offer, links and collisions. | [`email-quality-auditor`](../../skills/email-quality-auditor/SKILL.md) |
| [Check My A/B Test Before It Runs](validate-ab-test-setup.md) | Whether a test's setup, sample size and decision rule can actually produce an answer. | [`ab-testing`](../../skills/ab-testing/SKILL.md) |
