---
name: ds-manage
description: Use for DS operations — publishing cascades, adoption analytics, documentation generation, health and drift monitoring. Activates for /ds-manage, "publish", "release cascade", "adoption report", "generate docs", "uspec", "check health", "library drift", "detached components", "DS audit".
---

# /ds-manage — DS Operations

Router for ongoing design system management. Handles publishing, analytics, documentation, and health monitoring. At L3 (Enterprise), Publisher and Health Monitor integrate with DS lint via the configured Figma adapter.

## Maturity Detection

Follow `skills/shared/maturity-detection.md`. Run detection before routing.

**Manage commands require L2 at minimum** — a design system must exist. At L0 or L1, politely redirect:

> "DS manage operations require an existing design system (L2+). It looks like this project doesn't have one yet. Run `/ds-make` to create one, or `/creative` → `/map-design` to establish a design language first."

- **L2 (DS exists):** Full operations available using governance.md rules and manual checklists.
- **L3 (Enterprise DS):** Full operations + DS lint integration via configured Figma adapter (see `skills/shared/figma-adapter.md`) for Publisher and Health Monitor. Library analytics available for Analytics Reporter.

Always announce the detected level before routing.

## Always Load

- `skills/shared/knowledge/core-principles.md` (L1 — always)
- `skills/shared/knowledge/governance.md` (L2 — always for manage operations)

## Sub-Agent Router

| Trigger | Sub-Agent |
|---------|-----------|
| "publish", "release", "cascade", "ship" | Publisher |
| "adoption", "usage", "metrics", "report", "analytics", "Monday report" | Analytics Reporter |
| "document", "uspec", "property table", "demo area", "spec", "generate docs" | Documentation Generator |
| "health", "drift", "detached", "audit", "compliance check", "lint" | Health Monitor |

If a request implies a multi-step operation, suggest the appropriate chain (see Workflow Chains below).

## Workflow Chains

Two common multi-sub-agent chains:

1. **Pre-release chain** (before any publish): Health Monitor → Documentation Generator → Publisher
   - Run Health Monitor first to catch blockers before documentation effort.
   - Confirm all documentation is current before triggering the cascade.
   - Publisher executes only after both pass.

2. **Weekly ops chain** (recurring team cadence): Analytics Reporter → Health Monitor → (optional) Deprecation Planner from /ds-make
   - Review adoption trends first.
   - Health Monitor flags any new drift or detached instances introduced since last week.
   - If Health Monitor finds legacy usage growing, trigger /ds-make Deprecation Planner.

---

## Sub-Agent: Publisher

**Load additionally:** None — `governance.md` (already loaded) contains the full publishing cascade rules.

**At L3:** Use the configured Figma adapter to run DS lint before publishing (see `skills/shared/figma-adapter.md`). Lint violations are blocking — do not proceed until resolved.

### Ask first

1. What artifact is being published? (component, foundation, pattern, squad pattern)
2. What is the current version being released?
3. Are there known downstream dependents? (list them or confirm "run discovery")

### Workflow

1. **Pre-publish gate**: Verify the artifact passes all quality gates from `governance.md`:
   - [ ] Governance checklist — all applicable items pass
   - [ ] DS lint — no violations (L3: read via configured Figma adapter using `{{governance.lint.tool}}`)
   - [ ] Multi-scale test complete
   - [ ] Dark mode tested
   - [ ] Demo area present (property table + behavioral guidelines)
   - [ ] No old library connections
   - [ ] Branch conflicts resolved
   - If any gate fails, stop. Do not proceed with the cascade until resolved.

2. **Cascade planning**: Per the cascade order from `governance.md`:
   `Foundations → Components → Patterns (L1) → Squad Patterns (L2) → Final files`
   Map the artifact to its cascade level. List all dependent artifacts at each downstream level.

3. **Execute cascade level by level**:
   - Publish the current artifact at its level
   - For each downstream level: update dependents with upstream changes → QA (governance checklist) → publish only after QA passes
   - NEVER publish a dependent before its upstream is published and QA'd
   - If QA fails at any level: stop the cascade, create a blocking note, fix before continuing

4. **Changelog**: Write cascading changelog entries for all affected artifacts in the standard format from `governance.md`.

5. **Shortcut**: Update all related tickets with status + version tags.

### Output format

```
## Publish Plan — <Artifact Name> v<X.Y.Z>

### Pre-Publish Gate
| Check | Status |
|-------|--------|
| Governance checklist | PASS / FAIL |
| DS lint (L3) | PASS / FAIL / N/A |
...

### Cascade Map
Level 1 — Foundations: <artifact> ✓
Level 2 — Components: <list>
Level 3 — Patterns: <list>
...

### Changelog Entries
[formatted entries per artifact]

### Blockers
<any failing gates or dependencies — empty if clean>
```

---

## Sub-Agent: Analytics Reporter

**Load additionally:** None.

**At L3:** Library analytics are available. Track adoption across all libraries declared in `{{figma.libraries}}` from `.ds-context.md`. Compare DS library usage vs. non-DS usage.

### Ask first

1. What time window? (this week / this month / since last report)
2. Scope: all teams, or a specific squad?
3. Any specific component or library to focus on?

### Workflow

1. **Data source**: At L3, reference `output/latest_library_instances.csv` or ask user to run `FIGMA_TOKEN=xxx npm run build`. At L2, ask user to provide usage data (CSV, spreadsheet, or manual estimates).
2. **Adoption rate**: Calculate DS component instances vs. non-DS instances per team. Key metric: `ds_instances / (ds_instances + non_ds_instances) × 100 = adoption %`.
3. **Trend analysis**: Compare against prior period if data available. Flag regressions (teams moving away from the DS) and bright spots (teams increasing adoption).
4. **Component breakdown**: Top 10 most used components. Top 5 least used (flag for deprecation consideration).
5. **Legacy hotspots**: Which files or teams have the highest legacy instance counts? These are migration priorities.
6. **Recommendations**: Based on trends, recommend actions — deprecation candidates, migration sprints, team outreach.

### Output format

```
## Adoption Report — <Period>

### Summary
Overall adoption: X%  (↑/↓ from last period: Y%)

### By Team
| Team | DS Library | Non-DS | Adoption % | Trend |
...

### Top Components
| Component | Instances | Trend |
...

### Legacy Hotspots
| File / Team | Legacy Count | Priority |
...

### Recommendations
1. ...
2. ...
```

---

## Sub-Agent: Documentation Generator

**Load additionally:** `skills/shared/knowledge/documentation.md`

**Optional L3 query:** Not applicable for documentation generation.

### Ask first

1. Which component or pattern needs documentation?
2. Which spec types are needed? (minimum: API spec + anatomy + component properties; full set adds: color annotation, structure, screen reader, motion)
3. Is there an existing Figma file key for this component, or should I work from a description?

### Workflow

1. **Fetch the component**: If a Figma file key is available, use `use_figma` to retrieve the component structure and existing properties. If not, work from user-provided description.
2. **Apply uSpec templates** from `documentation.md`:
   - **API spec** — all props, types, defaults, descriptions
   - **Anatomy** — component parts labeled with names and roles
   - **Component properties** — variant matrix with Prostar-compatible format
   - Add color annotation, structure spec, screen reader spec, motion spec as requested
3. **Property table**: Generate in Prostar-compatible format — name, type, default, description, example. Flag any props that are undocumented or have unclear defaults.
4. **Demo area structure**: Overview → Usage guidance → Variants grid → States → Accessibility notes → Do/Don't examples. Confirm the structure with user before writing.
5. **Coverage check**: Run the documentation coverage checklist from `documentation.md` — flag any missing sections.
6. **Anti-pattern check**: No undocumented props, no missing "when to use", no examples without context.

### Output format

Documentation output follows uSpec format from `documentation.md`. Deliver as structured markdown sections the user can paste into Figma or a documentation platform. Confirm with user before finalizing.

```
## Documentation — <ComponentName>

### API Spec
| Prop | Type | Default | Description |
...

### Anatomy
<labeled parts list>

### When to Use / When Not to Use
...

### Variants
...

### States
...

### Accessibility
...
```

---

## Sub-Agent: Health Monitor

**Load additionally:** None — `governance.md` (already loaded) contains the governance checklist and cascade rules.

**At L3:** Read DS lint results via the configured Figma adapter (see `skills/shared/figma-adapter.md`). If using PluginOS, call `run_operation("lint_styles", {scope: "page"})`, `run_operation("lint_detached", {scope: "page"})`, and `run_operation("lint_naming", {scope: "page"})` for a full inventory of lint violations, detached components, and naming issues.

**At L2:** Run governance checklist manually using rules from `governance.md`. Ask user to provide screen exports or Figma links for inspection.

### Ask first

1. What is the scope? (full file / specific page / selection)
2. What is the Figma file key? (required for L3 lint reads)
3. Any specific concern — drift, detached components, token compliance, legacy usage?

### Workflow

1. **L3 path**:
   - Read lint results via configured Figma adapter (PluginOS: `run_operation("lint_styles")` + `run_operation("lint_detached")`)
   - Read audit results via configured Figma adapter (PluginOS: `run_operation("lint_naming")`)
   - Parse results: group violations by rule type (fill, stroke, spacing, textStyle, instanceOverride, naming — see `skills/ds-producer/SKILL.md` for full rule table).
   - Classify each finding by severity: P0 (lint violation blocking publish), P1 (deviation from governance), P2 (minor inconsistency), P3 (cosmetic/naming).

2. **L2 path**:
   - Walk the governance checklist from `governance.md` against the described or provided designs.
   - Check: token binding, component source library, override presence, naming conventions.
   - Classify findings with the same P0–P3 severity rubric.

3. **Drift analysis**: Compare finding counts vs. last known health check (if data available). Flag regressions.

4. **Remediation plan**: For each P0/P1 finding, provide a specific fix instruction. Group P2/P3 as a batch for a future cleanup sprint.

5. **Summary**: Overall health score (P0 count = blockers; P1 count = major debt; P2/P3 = cosmetic backlog).

### Output format

```
## Health Report — <File / Scope>

### Summary
P0 Blockers: X  |  P1 Major: Y  |  P2 Minor: Z  |  P3 Cosmetic: W

### Findings
| # | Rule / Check | Location | Issue | Severity | Fix |
...

### Remediation Plan
**P0 (fix before next publish):**
1. ...

**P1 (schedule for next sprint):**
1. ...

**P2/P3 (cosmetic backlog):**
<batch note>
```

Offer to feed P0 findings into the Publisher pre-publish gate, or route complex deprecation cases to /ds-make Deprecation Planner.
