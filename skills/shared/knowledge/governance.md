# Design System Governance (L2)

> Loaded by /ds-make, /ds-manage, /design-review sub-agents. Covers contribution, versioning, deprecation, publishing cascade, consumption rules, and the QA checklist.

## Governance Model

### Decision-Making & Modes

- **Democratized contributions:** Whole team proposes ideas/requests. 1-2 designated approvers merge changes.
- **Prioritization:** Impact/effort ratio, attentive to reusability and scale.
- **Two operational modes:**
  - **Expand** — Add new elements, variants, patterns to meet emerging needs
  - **Contract** — Reduce complexity, merge elements under single structures, endorse reusability

### Cross-Squad Conflicts

Resolve via Expand → Contract: create multiple variants (or separate components) first, then review if cases can converge into one scalable component.

### Exceptions

Breaking DS rules is ONLY acceptable during DS Producer discovery and iteration (new components/updates). No other exceptions.

## Contribution Process

1. **Discovery** — Explore need, research existing solutions, validate with team
2. **Acceptance Criteria** — Define and get approval before building
3. **Build** — Create/update artifact on Figma branch
4. **Peer Review** — 4-eye principle (async, on Figma branches):
   - Minor changes: 1 reviewer
   - Standard changes: 2 reviewers
   - Major refactors: whole team
5. **Approve & Merge** — 1-2 designated approvers

## Versioning (Semver)

| Bump | When | Impact |
|------|------|--------|
| **Major** | New structure that causes override loss when files accept updates | Breaking — notify all consumers |
| **Minor** | New variants, additive changes, no override loss | Additive — safe to accept |
| **Patch** | Bug fixes, token adjustments, cosmetic changes | Safe — auto-accept recommended |

**Branch naming convention:** `<story-id>/<component-name>-v<version>` — name must be aligned across component, Figma page, and Shortcut ticket.

## Deprecation

1. Run analytics to assess usage across all library consumers
2. Remove from related files and patterns (unlink dependencies first)
3. Notify consumers with migration path (minimum 1 sprint lead time for Major)
4. Delete the component after migration window

## Consumption Rules

- **Mandatory:** Use DS components. Never detach. Always use the latest library version.
- **No overrides** by Consumers (except copy/text content).
- **All components** are responsive, accessible, support dark mode and zoom levels.
- **Swappable areas** (modals, drawers, etc.) use unpublished microcomponents to enforce allowed swaps.
- **No temporary workarounds** — when something new is needed, Consumer creates a ticket for Producers.
- **Pre-handoff:** Run DS lint (`{{governance.lint.tool}}`) → designer does UX review → handoff to engineering.

## Publishing Cascade

Changes must propagate upward in order. Each level must pass QA before the next level publishes.

```
Foundations → Components → Patterns (L1) → Squad Patterns (L2) → Final files
```

**QA gate per level:** Validate tokens/overrides, run DS lint, check dark mode, verify in demo area before promoting to next level.

## DS Governance Checklist

Use this during /ds-manage Publisher and /design-review DS Compliance Checker workflows.

### All Artifact Types (Component, Foundation, Icon, Pattern)

**Branch Organization:**
- Name aligned across component, Figma page, and Shortcut ticket
- Branch name mentions Shortcut story ID
- Branch name mentions version (from Notion changelog)

**Foundations (Lint Plugin):**
- DS colors, typography (components not text styles), icons, effects/elevations, radius, stroke, spacing applied
- No unnecessary hidden background layers

**Structure:**
- Simple — no unnecessary grouping, layers, or nested components
- Hidden objects only if part of state changes
- Child elements resize with container ("fill" width where applicable)
- No min size assigned; max width set if applicable

**Properties and Layers:**
- Micro component names: `_` prefix, no version mention
- Meaningful layer and property names
- Properties in logical, intuitive order
- Correct property switching (no size jumps or unexpected shifts)
- No property conflicts; no client names

**Test:**
- Frames tested at different scales (paste into separate frame, adjust in Appearance)
- Dark mode applied to test frames

**Demo Area:**
- Property table generated (Prostar plugin)
- Overflow behavior explained if applicable
- Max width described if applicable
- Component version removed from frame names
- Link to Component Master file added

**Publishing:**
- No old libraries connected
- Branch conflicts resolved

### Pattern-Specific Additions

- DS components used throughout (no detached instances)
- DS spacing tokens applied (no ad-hoc values)
- Modals use copies from project library (not external file instances)

## Communication Cadence

Regular meetings (weekly/bi-weekly): Refinement, Retro, Demo, Governance, Handoff, Office Hours, Vision. Analytics reports every Monday (per Squad + global).
