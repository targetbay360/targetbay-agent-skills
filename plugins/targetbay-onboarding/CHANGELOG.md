# Changelog

All notable changes to TargetBay Onboarding Skills are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this package adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-12

First release. Four skills forming one pipeline, a capability registry, the rules and knowledge they
cite, and the schema for the derived store context they all read.

This is a `0.x` line because no TargetBay MCP surface has been inspected yet. Every capability in
[capabilities.yaml](capabilities.yaml) maps to `TODO`, which means the skills can plan but cannot
execute. Skill reasoning is expected to be stable; capability identifiers may still change as the real
MCP is mapped.

### Added

- **Four skills forming a pipeline**, not a catalogue. [`context-audit`](skills/context-audit/SKILL.md)
  (analysis) sits at the bottom of the graph and establishes what is known;
  [`onboarding-intake`](skills/onboarding-intake/SKILL.md) (mutation) asks only what the platform cannot
  observe; [`onboarding-blueprint`](skills/onboarding-blueprint/SKILL.md) (plan) sequences all four
  products across ninety days; [`onboarding-provisioning`](skills/onboarding-provisioning/SKILL.md)
  (high_impact) builds the approved plan as drafts and stops. The risk level climbs at each step so a
  reviewer can disagree with the facts before the plan is built on them, and with the plan before
  anything is created.

- **A cross-product plugin, because the validator requires one.** A plugin's capability identifiers may
  not span namespaces, and `composes:` may only name skills in the same plugin. An onboarding skill that
  needs `reviews.*`, `loyalty.*` and `onsite.*` alongside `email_sms.*` therefore cannot live in any
  product plugin. The `onboarding.*` namespace declares four orchestration capabilities rather than a
  fifth copy of the fifty-five product ones.

- **[`contact-ownership-rules.md`](rules/contact-ownership-rules.md), answering the marketplace's
  unreconciled-contact problem.** TargetBay Email & SMS, Reviews and Loyalty can each decide,
  independently and correctly, to contact the same customer. X1 puts the contact budget on the platform
  rather than in each product; X2 assigns each lifecycle moment exactly one owner; X3 records why onsite
  personalization is structurally exempt; X5 and X6 answer the open dispatch questions recorded in the
  Loyalty and Reviews integration docs; X7 makes a stated aggregate a condition of approval. X9 states
  the residual dependency: none of this is *enforceable* without a unified cross-product frequency and
  consent view from the MCP, and where that view does not exist the budget is labelled provisional rather
  than claimed as enforced.

- **[`sequencing-rules.md`](rules/sequencing-rules.md).** Capture before consumption, because a review
  trigger armed on day sixty cannot ask about a day-ten order. Reversible before irreversible.
  Preconditions stated as observations, never as dates.

- **[`context-pack.schema.json`](schemas/context-pack.schema.json).** The derived store context every
  skill reads. Its load-bearing type is `derivedValue`: a quantity plus its basis — derived, provisional,
  stated or absent — its sample size and its evidence. A `derived` value must carry an `n` and evidence;
  a `provisional` or `absent` value must name the observation that would replace it; an `absent` value's
  `value` must be null. This makes global rules G3 and G14 a schema constraint rather than author
  discipline, which matters most for the zero-history store where every instinct is to fill the gap.

- **Rule anchors chosen to survive.** `sequencing-rules.md` uses the `SQ` prefix rather than `Q`, because
  `onboarding-intake`'s twelve intake questions are already `Q1`-`Q12` and
  `context-pack.schema.json` encodes their answers as `intake:Q3` — one plugin cannot have two meanings
  for `Q1`. `global-rules.md` keeps the same tail numbering as the other four plugins (`G15` declare what
  you could not check, `G16` prefer reversible steps first) so an author moving between plugins is not
  surprised.

- **Two knowledge documents.**
  [`evidence-and-provenance.md`](knowledge/evidence-and-provenance.md) covers the four bases and what a
  store with no history can honestly be given;
  [`onboarding-sequence.md`](knowledge/onboarding-sequence.md) covers why ordering decides the outcome.

### Known gaps

- **No MCP mapping.** All four capabilities are `TODO`. The nine questions that mapping must settle are
  listed at the bottom of [docs/mcp-integration.md](docs/mcp-integration.md).
- **`onboarding.provisioning` is unverified.** No TargetBay write surface has been inspected. Until one
  is, `onboarding-provisioning` degrades to producing a build checklist rather than creating anything.
- **The contact budget is not enforceable from here.** The rules decide ownership; enforcement needs a
  unified frequency and consent view from the platform. See X9.
- **No vertical playbooks.** Onboarding reads the detected vertical from the store context and applies
  the Email & SMS playbooks. Whether the other three products need their own overlays is an open
  question, and inventing five of them without evidence would be the error this marketplace avoids
  elsewhere.
- **A fifth copy of the shared layer.** `global-rules.md`, `safety-rules.md` and three schemas are now
  duplicated five times across the marketplace. Extracting a shared layer is tracked at the repository
  root and is deliberately not coupled to this release.
