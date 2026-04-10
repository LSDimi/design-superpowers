# PROJECT_CONTEXT.md — Session Handoff Brief

> Generated 2026-04-08. Use this to onboard a new Claude session on the Tone DS Skills project.

## What This Project Is

A **Claude Code plugin** for the Talon.One design team containing two shared skills:

- **DS Producer** (`skills/ds-producer/SKILL.md`) — Full DS lifecycle: create, update, audit, document, version, publish Tone DS artifacts
- **DS Consumer** (`skills/ds-consumer/SKILL.md`) — Use Tone DS to design product features; never creates new components, requests from Producer
- **Shared foundation** (`skills/shared/`) — Token vocabulary, Figma file map, product context, design principles, governance model

Both skills are designed to be installed by the entire design team. Team has varying Claude Code experience.

## What Has Been Built (Completed)

### 1. Skills (Done)
- Both SKILL.md files are written, reviewed, and refined
- Shared context files (`tone-ds-context.md`, `design-principles.md`) cover Tone DS identity, governance, IA principles, anti-patterns, publishing cascade
- Cross-referencing is clean — Consumer references shared files, no duplication

### 2. Tone Lint Plugin Modifications (Done, needs deployment rethink)
Modified the existing Tone Lint Figma plugin to be agent-friendly:

**Files modified** (in `/tmp/figma-plugins/tone-lint/tone-lint/`):
- `src/plugin/controller.ts` — Added `sharedPluginData` writes after lint and audit scans
- `src/plugin/libraryKeys.ts` — NEW: loads library key map from `clientStorage` (replaces REST API)
- `src/app/components/AuditorPanel.tsx` — Removed token input, REST API calls (`fetchLibraryItems`, `buildKeyMaps`), progress bar. Auditor now works without a Figma API token.

**Agent scripts created** (in `tools/tone-lint-agent/`):
- `sync-libraries.js` — One-time: collects component/style keys from a Tone library file
- `store-keys.js` — Stores merged key map in `clientStorage`
- `read-lint-results.js` / `read-audit-results.js` — 3-line readers (~50 tokens each)

**Plugin builds clean:** `npm run build` succeeds, webpack output in `dist/`.

### 3. Plans Written
- `docs/superpowers/plans/2026-04-07-tone-ds-skills.md` — Original skills plan (executed)
- `docs/superpowers/plans/2026-04-08-headless-tone-lint.md` — Plugin bridge plan (executed, needs revision — see Open Question below)
- `docs/superpowers/plans/2026-04-08-plugin-integration.md` — MCP server plan (not started)

## Critical Discovery: `pluginData` vs `sharedPluginData`

**Problem found during testing:** `figma.root.getPluginData()` is plugin-scoped — only the plugin that wrote it can read it. The Figma MCP's `use_figma` tool runs as a different "plugin," so it gets `"getPluginData" is not a supported API`.

**Fix applied:** Switched to `figma.root.setSharedPluginData("tone_lint", "lint_results", ...)` which uses a cross-plugin namespace. Verified working end-to-end on test file `itFXHscn9JW5nZiE6t0auS`.

**All references updated:** controller.ts, reader scripts, both SKILL.md files, all use `sharedPluginData` with namespace `"tone_lint"`.

## Open Question: Plugin Deployment Architecture (ACTIVE — needs brainstorming)

This is where the session ended. The user raised a fundamental question:

> "Given the scope of our project, would these Figma plugins run natively when the Claude plugin is installed, or would they require some prior installation before agents can use them?"

**The problem:**
- Tone Lint is a **Figma plugin** (runs in Figma's sandbox, installed in Figma)
- Our project is a **Claude Code plugin** (provides skills/tools, runs in terminal)
- These are **two completely separate installation surfaces** — a Claude Code plugin cannot auto-install Figma plugins
- Current architecture requires: (1) install Claude Code plugin, (2) separately install modified Tone Lint in Figma, (3) manually run Tone Lint before agent can read results

**This creates a dependency chain** that undermines the "just install and go" experience. The user wants deeper thinking on deployment strategy before continuing.

**Approaches to consider:**
1. **Require separate Tone Lint installation** — team already has it, but they'd need the modified version
2. **Agent runs lint headlessly via `use_figma`** — self-contained, but costs ~30K tokens per run (rejected earlier for cost)
3. **Lightweight headless lint** — port only critical rules as compact `use_figma` scripts, not the full 13-rule engine
4. **Agent writes + reads sharedPluginData** — agent runs lint logic headlessly, writes to sharedPluginData, subsequent reads are cheap (cached headless)
5. **Ship lint logic as `use_figma` snippets in the skill itself** — no plugin needed, agent IS the linter

**Key context for this decision:**
- The team already has Tone Lint installed today
- `lintingFunctions.ts` is 1,681 lines / 59KB — too large to run via `use_figma` (50K char limit)
- `auditFunctions.ts` is 223 lines / 7.3KB — small enough to run headlessly
- The `use_figma` tool has full Plugin API access including `findAll`, variable resolution, style inspection
- Token cost was a major concern from the user — 10 users x 5 runs/day x month = potential 30M tokens with headless approach

**Unanswered clarifying question:** How does the team currently deploy Tone Lint — org-wide or individual installs? Published to Community or internal distribution?

## Token Economics (Important to the user)

| Action | Cost |
|--------|------|
| Team runs Tone Lint natively | 0 tokens |
| Agent reads lint/audit results | ~50 tokens |
| Agent applies targeted fix | ~500 tokens |
| One-time library sync (all 13 libs) | ~5K tokens |
| Full headless lint run (rejected) | ~30K tokens |

The user explicitly flagged token cost as a concern: "this is a repetitive action from many users, which will eventually mean crazy spending."

## Known Tone Library File Keys

These are hardcoded in `AuditorPanel.tsx` and used by sync scripts:

| Library | File Key |
|---------|----------|
| Tone. Foundations | `Pn9sIWsLKN7gQKj1RkV75j` |
| Tone. Components | `rVLnzp5jPQee88ThJR81Ha` |
| Tone. Patterns | `H4A6DU7tCNJ7Qt4UwCuQy2` |
| Pricing Squad Patterns | `CsCMa8iqAGRpwOU9isrwxd` |
| Promotions Squad Patterns | `TCH0ed2xO5rOU6Ebnv6gB5` |
| Usability Squad Patterns | `Py2SqQuD8tJGYivKVGt9z2` |
| Legacy Library | `dqlNDxAO5JY0LliAPadihh` |
| W&N Squad Patterns | `9jD3iwOBezNKc3rFU7KNwY` |
| Rewards Squad Patterns | `2CpEj5cBBNICdWtCtCQYew` |
| Loyalty Squad Patterns | `JY1c1RNTYakochX5N5iZ8w` |
| Experiments Squad Patterns | `9a5SOlQphYDyKdvXa1RpfW` |
| Insights Squad Patterns | `o3m4IWJNh0sHD1Rea37Cg1` |
| Gamification Squad Patterns | `qGiniOnkCUIww81UKNUkSs` |

## Test File

`https://www.figma.com/design/itFXHscn9JW5nZiE6t0auS/Agentic-test--please-ignore` — used for end-to-end testing of the agent bridge.

## Verified Working (E2E tested on 2026-04-08)

1. `use_figma` can write to `sharedPluginData("tone_lint", ...)` on any file
2. `use_figma` can read from `sharedPluginData("tone_lint", ...)` — returns full JSON
3. `sync-libraries.js` collects real keys from Tone. Foundations (429 components, 91 styles)
4. Plugin builds clean with all modifications
5. `getPluginData` does NOT work from `use_figma` (plugin-scoped) — must use `sharedPluginData`

## File Structure

```
skills/
├── shared/
│   ├── tone-ds-context.md      # Tone DS identity, Figma file map, entities, tech stack
│   └── design-principles.md    # IA principles, governance, checklist, publishing cascade
├── ds-producer/
│   └── SKILL.md                # 7 workflows, Tone Lint integration, Shortcut, quality gates
└── ds-consumer/
    └── SKILL.md                # 5 workflows, hard rules, product awareness, UX framework
docs/superpowers/
├── plans/
│   ├── 2026-04-07-tone-ds-skills.md
│   ├── 2026-04-08-headless-tone-lint.md
│   └── 2026-04-08-plugin-integration.md
tools/
└── tone-lint-agent/
    ├── sync-libraries.js       # One-time: collect keys from library file
    ├── store-keys.js           # Store merged key map in clientStorage
    ├── read-lint-results.js    # Agent reader (~50 tokens)
    └── read-audit-results.js   # Agent reader (~50 tokens)
```

Modified plugin source (NOT in project dir — in `/tmp/figma-plugins/tone-lint/tone-lint/`):
```
src/plugin/controller.ts       # Modified: sharedPluginData writes, library key enrichment
src/plugin/libraryKeys.ts      # New: clientStorage-based key map loader
src/plugin/lintingFunctions.ts # Unchanged: 13 lint rules (1,681 lines)
src/plugin/auditFunctions.ts   # Unchanged: audit scanner (223 lines)
src/app/components/AuditorPanel.tsx  # Modified: removed token/REST, uses enriched results
```

## What Comes Next (after resolving deployment question)

1. **Resolve Figma plugin deployment strategy** — the open brainstorming question above
2. **Run full library sync** on all 13 Tone libraries (if plugin approach survives)
3. **Tone DS inspection via Figma MCP** — validate component/pattern names against real files
4. **Build data files** for the plugin (similar to ui-ux-pro-max CSV approach)
5. **Build MCP server** using `anthropic-skills:mcp-builder` (per plan 3)
6. **Add remaining Figma plugins** (user mentioned 1-2 more TBD)
7. **Test skills with real prompts** end-to-end

## Reference Resources

| Resource | Used For |
|----------|----------|
| `github.com/murphytrueman/design-system-ops` | DS operations patterns |
| `github.com/nextlevelbuilder/ui-ux-pro-max-skill` | Skill authoring patterns |
| `github.com/redongreen/uSpec` | DS documentation generation |
| `skillscheck.ai` | Skill quality evaluation |
| `impeccable.style` | Design system standards |
| `docs.talon.one` | Product context |
