# Design Principles & Governance

> Governance content moved to `skills/shared/knowledge/governance.md`. This file retains only IA principles and anti-patterns for backward compatibility with ds-producer and ds-consumer references.

## Information Architecture Principles

1. **Conciseness over completeness** — Show only what's relevant at each step. Do not clutter with tangential information.
2. **Single-surface preference** — Avoid multi-page flows and double-drawers. Keep interactions on one surface when possible.
3. **Progressive disclosure** — Start with essentials, reveal complexity on demand.
4. **Efficient navigation** — Every click must earn its place. Minimize steps to accomplish tasks.

## Anti-Patterns to Prevent

| Anti-Pattern | Problem | Solution |
|-------------|---------|----------|
| Multi-page sprawl | Simple CRUD split across 3+ pages | Single-surface with sections/tabs/progressive disclosure |
| Double-drawers | Drawer opening another drawer | Inline expansion, modal for confirmation, or navigate to detail page |
| Information overload | All entity attributes shown everywhere | Only attributes relevant to current task/step |
| Inconsistent patterns | Different list/detail patterns for similar entities | Reuse DS Patterns (L1) |
| Context loss | Navigation loses place or unsaved state | Preserve context, inline editing, auto-save |
| Overextended flows | Asking for info that could be defaulted | Smart defaults, optional fields collapsed |

---

> For governance model, contribution process, versioning, deprecation, consumption rules, publishing cascade, and checklist — see `skills/shared/knowledge/governance.md`.

## Governance Model

### Decision-Making & Modes
- **Democratized contributions:** Whole team proposes ideas/requests. 1-2 designated approvers merge changes.
- **Prioritization:** Impact/effort ratio, attentive to reusability and scale.
- **Two operational modes:**
  - **Expand** — Add new elements, variants, patterns to meet emerging needs
  - **Contract** — Reduce complexity, merge elements under single structures, endorse reusability

### Contribution Process
1. **Discovery** — Explore need, research existing solutions, validate with team
2. **Acceptance Criteria** — Define and get approval before building
3. **Build** — Create/update artifact on Figma branch
4. **Peer Review** — 4-eye principle (async, on Figma branches):
   - Minor changes: 1 reviewer
   - Standard changes: 2 reviewers
   - Major refactors: whole team
5. **Approve & Merge** — 1-2 designated approvers

### Versioning (Semver)
- **Major** — New structure triggers override loss when files accept updates
- **Minor** — New variants, additive changes, no override loss
- **Patch** — Bug fixes, token adjustments, cosmetic

### Deprecation
1. Run analytics to assess usage
2. Remove from related files/patterns
3. Delete the component

### Communication Cadence
Regular meetings (weekly/bi-weekly): Refinement, Retro, Demo, Governance, Handoff, Office Hours, Vision. Analytics reports every Monday (per Squad + global).

### Cross-Squad Conflicts
Resolve via Expand → Contract: create multiple variants (or separate components) first, then review if cases can converge into one scalable component.

### Exceptions
Breaking DS rules is ONLY acceptable during DS Producer discovery and iteration (new components/updates). No other exceptions.

## Consumption Rules

- **Mandatory:** Use DS components. Never detach. Always use latest library version.
- **No overrides** by Consumers (except copy/text content).
- **All components** are responsive, accessible, support dark mode and zoom levels.
- **Swappable areas** (modals, drawers, etc.) use unpublished microcomponents to enforce allowed swaps.
- **No temporary workarounds** — when something new is needed, Consumer creates a ticket for Producers.
- **Pre-handoff:** Run DS lint (`{{governance.lint.tool}}`) → designer does UX review → handoff to engineering.

## DS Governance Checklist

### All Artifact Types (Component, Foundation, Icon, Pattern)

**Branch Organization:**
- Name aligned across component/Figma page/Shortcut ticket
- Branch name mentions Shortcut story ID
- Branch name mentions version (from Notion changelog)

**Foundations (Lint Plugin):**
- DS colors, typography (components not text styles), icons, effects/elevations, radius, stroke, spacing applied
- No unnecessary hidden background

**Structure:**
- Simple — no unnecessary grouping, layers, nested components
- Hidden objects only if part of state changes
- Child elements resize with container ("fill" width where applicable)
- No min size assigned; max width set if applicable

**Properties and Layers:**
- Micro component names: "_" prefix, no version mention
- Meaningful layer and property names
- Properties in logical, intuitive order
- Correct property switching (no size jumps/unexpected shifts)
- No property conflicts; no client names

**Test:**
- Frames at different scales (paste into separate frame, adjust in Appearance)
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
- DS components used
- DS spacing applied
- Modals use copies from project library

## Publishing Cascade Order

Changes propagate upward. See DS Producer Workflow 5 for the full cascade procedure.

```
Foundations → Components → Patterns (L1) → Squad Patterns (L2) → Final files
```
