---
description: Design product features using an existing DS or design language — never creates new components
argument-hint: Optional description of the feature or screen to design
---

Invoke the `design` skill via the Skill tool to handle this request.

User request: $ARGUMENTS

Follow the skill's routing and maturity-detection procedure exactly. Never create new components — route any DS gaps to `/ds-make`. At L3 (Enterprise DS), the skill delegates to `ds-consumer`.
