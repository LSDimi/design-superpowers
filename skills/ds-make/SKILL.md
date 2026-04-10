---
name: ds-make
description: Use when creating, updating, versioning, or deprecating design system tokens, components, or patterns. Activates for /ds-make, "new component", "add token", "create a variant", "update a component", "bump version", "deprecate X", "semver", "scaffold design system", "token naming", "breaking change".
---

# /ds-make — DS Creation & Lifecycle

Router for DS creation and lifecycle sub-agents. At L3 (Tone/Enterprise), delegates to `skills/ds-producer/SKILL.md` workflows.

## Maturity Detection

Follow `skills/shared/maturity-detection.md`. Run detection before routing.

- **L0 (Greenfield):** Scaffold a new DS from scratch. Requires DESIGN.md as input. If none exists, redirect: "Run /creative first to establish a design language, then /map-design to generate DESIGN.md."
- **L1 (DESIGN.md exists):** Scaffold a DS using DESIGN.md tokens as the source of truth. Token Architect reads DESIGN.md and formalizes it.
- **L2 (DS exists):** Extend the existing DS. Load `.ds-context.md` for library keys and token collections before acting.
- **L3 (Tone/Enterprise):** Delegate to `skills/ds-producer/SKILL.md`. Use the sub-agents below only for exploration/planning; final execution goes through ds-producer workflows.

Always announce the detected level before routing.

## Always Load

- `skills/shared/knowledge/core-principles.md` (L1 — always)
- `skills/shared/knowledge/governance.md` (L2 — always for DS work)

## Sub-Agent Router

| Trigger | Sub-Agent |
|---------|-----------|
| "token", "variable", "color scale", "spacing scale", "naming", "tier" | Token Architect |
| "component", "new <X>", "variant", "api", "props", "compound" | Component Builder |
| "deprecate", "remove", "sunset", "retire", "clean up" | Deprecation Planner |
| "version", "bump", "semver", "breaking change", "changelog", "release" | Version Advisor |

If the request spans multiple areas (e.g., "new component + version bump"), run Token Architect → Component Builder first, then Version Advisor at the end.

---

## Sub-Agent: Token Architect

**Load additionally:** `skills/shared/knowledge/token-architecture.md`

**Optional L3 query:** `Grep pattern="<keyword>" path="skills/shared/data/design-principles.csv"` for principle backing on naming or structural decisions.

**L3 delegation:** If maturity is L3, delegate to **ds-producer Workflow 1 (New Component / Foundation)** for token creation within Tone, or **Workflow 2 (Update Existing Component)** for token amendments. Use this sub-agent for planning and naming only.

### Ask first

1. What category of token? (color, spacing, typography, radius, effect, dimension)
2. Which tier? (Primitive — raw values; Semantic — purpose-bound; Component — scoped to one component)
3. Are these net-new tokens or updates to existing ones?

### Workflow

1. Confirm the **3-tier model** applies: Primitive → Semantic → Component. Verify the user is not trying to bind primitives directly to components (flag if so).
2. Draft **token names** using the `<category>.<property>.<role>.<state>.<size>` convention from `token-architecture.md`. Show examples before finalizing.
3. For **color tokens**: verify primitive scale exists; if not, prompt to run /creative → Palette Architect first.
4. For **semantic tokens**: map from primitives explicitly — show the binding. Confirm dark mode counterpart if applicable.
5. For **component tokens**: scope to the component namespace. Confirm no semantic token already covers the need (avoid redundancy).
6. Check against anti-patterns from `token-architecture.md`: no primitives tied directly to components, no bypassing the semantic layer, no magic numbers.
7. Output the token set as a structured table.

### Output format

```
## Token Proposal — <Category>

### Primitives (if new)
| Token Name | Value | Notes |
...

### Semantic Bindings
| Semantic Token | → Primitive | Dark Mode |
...

### Component Tokens (if applicable)
| Token Name | → Semantic | Scope |
...
```

Flag any anti-patterns detected. Offer to pass to Component Builder if this is part of a new component.

---

## Sub-Agent: Component Builder

**Load additionally:** `skills/shared/knowledge/component-patterns.md`

**Optional L3 query:** `Grep pattern="<component type>" path="skills/shared/data/design-principles.csv"` for relevant composition or API principles.

**L3 delegation:** If maturity is L3, delegate to **ds-producer Workflow 1 (New Component)** for building in Tone, or **Workflow 2 (Update Existing Component)** for modifications. Use this sub-agent for design API planning only.

### Ask first

1. What is the component name and purpose? (one sentence)
2. What variants are needed? (list by dimension: size, intent, state, layout)
3. Is this a new component or an update to an existing one?
4. Any existing component in the DS it should relate to or extend?

### Workflow

1. **Determine hierarchy level**: Primitive, Component, Pattern, or Template (from `component-patterns.md` composition hierarchy). Confirm with user.
2. **Design the variant matrix**: For each variant dimension (size, intent, etc.), decide: boolean prop, enum prop, or separate component. Apply decision tree from `component-patterns.md`.
3. **Define the component API**: Props list with name, type, default, description. Apply naming conventions: PascalCase component names, camelCase props, action verbs for handlers (`onSelect`, `onChange`).
4. **Identify slot patterns**: What parts of the component are composable? Define slot names.
5. **List required states**: Default, hover, focus, pressed, disabled, loading, error, empty — which apply?
6. **Responsiveness**: Fluid or fixed? Which breakpoints need specific treatment?
7. **Validate against governance**: Check contribution process rules from `governance.md` — does this require a new ticket? A peer review?
8. Output as a structured spec.

### Output format

```
## Component Spec — <ComponentName>

**Hierarchy:** <Primitive / Component / Pattern>
**Purpose:** <one line>

### Variant Matrix
| Dimension | Type | Values |
...

### Props API
| Prop | Type | Default | Description |
...

### States
<list of applicable states>

### Slots
<list of composable slots, if any>

### Governance Note
<any contribution process steps triggered per governance.md>
```

Offer to pass to Version Advisor if this is an update with semver implications.

---

## Sub-Agent: Deprecation Planner

**Load additionally:** None — `governance.md` is already loaded.

**Optional L3 query:** Not applicable for deprecation planning.

**L3 delegation:** If maturity is L3, delegate to **ds-producer Workflow 6 (Deprecation)**. Use this sub-agent for impact analysis and planning only.

### Ask first

1. Which component, token, or pattern is being deprecated?
2. Is there a replacement? If yes, what is it?
3. Do you have usage data (per-squad, per-file counts), or should we estimate scope?

### Workflow

1. **Impact analysis**: Identify all files, patterns, squad libraries, and templates that reference the artifact. If usage data is available (from Analytics Reporter or Library Analytics CLI), summarize it. If not, request it.
2. **Migration path**: Define the replacement clearly. Draft a migration note: "Replace `<deprecated>` with `<replacement>` — key differences: ...".
3. **Communication plan**: Per `governance.md` deprecation rules — governance meeting announcement, Shortcut ticket, changelog entry, team notification.
4. **Staged removal plan**:
   - Phase 1: Mark deprecated in the library (annotation + deprecation flag)
   - Phase 2: Notify all consuming teams with migration guide
   - Phase 3: Remove from library after confirmed migration (or agreed sunset date)
5. **Verification**: After removal, plan a Tone Lint (L3) or governance checklist run (L2) across affected files to confirm clean removal.
6. Output the full deprecation plan.

### Output format

```
## Deprecation Plan — <Artifact Name>

**Replacement:** <name or "no replacement — remove with prejudice">
**Affected files:** <count or list>

### Migration Note
<Replace X with Y. Key differences: ...>

### Staged Removal
Phase 1 — <date/sprint>: ...
Phase 2 — <date/sprint>: ...
Phase 3 — <date/sprint>: ...

### Communication Checklist
- [ ] Governance meeting announcement
- [ ] Shortcut ticket created
- [ ] Changelog entry written
- [ ] Teams notified

### Post-Removal Verification
<Lint / checklist plan>
```

---

## Sub-Agent: Version Advisor

**Load additionally:** None — `governance.md` is already loaded (contains semver rules).

**Optional L3 query:** Not applicable.

**L3 delegation:** If maturity is L3, delegate to **ds-producer Workflow 2 (Update Existing Component)** step 9 (Version) and **Workflow 5 (Publishing)**. Use this sub-agent for semver decision-making only.

### Ask first

1. What changed? (list the specific modifications)
2. What is the current version?
3. Does this change affect consuming teams' overrides, auto-layout, or text bindings?

### Workflow

1. **Classify the change** using semver rules from `governance.md`:
   - **Major** — Structure change that causes override loss on update acceptance (e.g., layer restructure, removed props, renamed variants that break instances)
   - **Minor** — New variants, additive changes, no override loss
   - **Patch** — Bug fixes, token adjustments, cosmetic corrections
2. **Check for hidden breaking changes**: Does the change affect auto-layout fill behavior? Does it rename a required prop? Does it restructure a slot? These are Major even if they seem Minor.
3. **Draft the changelog entry** in the standard format:
   ```
   ## [Component Name] v[X.Y.Z] — [Date]
   ### [Added|Changed|Fixed|Deprecated|Removed]
   - <Description>
   - Shortcut: [SC-XXXXX]
   ```
4. **Cascade check**: Per `governance.md` publishing cascade — does this version bump trigger updates in Patterns, Squad Libraries, or Final Files? List them.
5. **Communication**: Who needs to be notified? (Component consumers, squad leads, design leads for Major)
6. Recommend the final version number with justification.

### Output format

```
## Version Decision — <Component Name>

**Current version:** X.Y.Z
**Recommended bump:** X.Y.Z → X.Y.Z (Major / Minor / Patch)
**Reason:** <one sentence>

### Changelog Entry
[formatted entry]

### Cascade Impact
<list of downstream artifacts that need updating>

### Notification Required
<list of teams/roles for Major; "standard release notes" for Minor/Patch>
```
