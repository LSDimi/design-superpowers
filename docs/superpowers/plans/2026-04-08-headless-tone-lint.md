# Agent-Friendly Tone Lint — Revised Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade Tone Lint plugin to be agent-readable (via pluginData) and token-free (eliminate REST API token requirement), keeping the native plugin for zero-cost daily team use while enabling agents to read results cheaply (~50 tokens per read).

**Architecture:** Three-layer approach: (1) Modify Tone Lint plugin to write structured results to `figma.root.pluginData` after each scan, and to read library key maps from `clientStorage` instead of REST API; (2) A one-time `use_figma` setup script that pre-builds the library key map by scanning each Tone library file; (3) A tiny agent reader script (~3 lines) that reads lint/audit results from pluginData. Daily team linting costs zero AI tokens. Agent reads cost ~50 tokens.

**Tech Stack:** TypeScript (Figma plugin), JavaScript (use_figma scripts), Figma MCP

---

## Cost Comparison

| Action | Headless Scripts (old plan) | Native Plugin + Agent Bridge (this plan) |
|--------|---------------------------|----------------------------------------|
| Team member runs lint | ~30K tokens | **0 tokens** (native plugin) |
| Agent reads results | N/A | **~50 tokens** (pluginData read) |
| Agent applies fix | ~3K tokens | **~500 tokens** (targeted use_figma) |
| One-time library sync | N/A | **~5K tokens** (run once) |
| 10 users × 5 runs/day × month | **30M tokens** | **~0 tokens** |

---

## File Structure

Changes to existing Tone Lint plugin + new agent scripts:

```
tone-lint/
├── src/
│   ├── plugin/
│   │   ├── controller.ts          # MODIFY: Add pluginData output after scans
│   │   ├── lintingFunctions.ts    # NO CHANGES
│   │   ├── auditFunctions.ts      # NO CHANGES
│   │   └── libraryKeys.ts         # CREATE: Library key map loader from clientStorage
│   └── app/
│       └── components/
│           └── AuditorPanel.tsx    # MODIFY: Use cached keys instead of REST API, remove token input
tools/
└── tone-lint-agent/
    ├── sync-libraries.js          # One-time: collect keys from all Tone library files
    ├── read-lint-results.js       # Agent reader: ~3 lines, reads pluginData
    └── read-audit-results.js      # Agent reader: ~3 lines, reads audit pluginData
```

---

## Chunk 1: Plugin Modifications — pluginData Output

### Task 1: Add pluginData Output to Controller

**Files:**
- Modify: `tone-lint/src/plugin/controller.ts:242` (after lint-result postMessage)
- Modify: `tone-lint/src/plugin/controller.ts:499` (after audit-result postMessage)

After each lint scan completes, write results to pluginData so agents can read them:

- [ ] **Step 1: Add pluginData write after lint scan**

In `controller.ts`, after the `lint-result` postMessage (line 242), add:

```typescript
// Write results to pluginData for agent consumption via Figma MCP
const lintOutput = JSON.stringify({
  timestamp: Date.now(),
  scope: msg.scope,
  totalErrors: errors.length,
  byRule: errors.reduce((acc, e) => { acc[e.ruleType] = (acc[e.ruleType] || 0) + 1; return acc; }, {} as Record<string, number>),
  errors: errors.map(e => ({
    nodeId: e.nodeId,
    nodeName: e.nodeName,
    nodePath: e.nodePath,
    pageName: e.pageName,
    ruleType: e.ruleType,
    message: e.message,
    value: e.value,
    suggestions: (e.suggestions || []).slice(0, 5).map(s => ({ key: s.key, name: s.name })),
    textStyleSuggestions: (e.textStyleSuggestions || []).slice(0, 3).map(s => ({ key: s.key, name: s.name })),
  })),
});
figma.root.setPluginData("tone_lint_results", lintOutput);
```

- [ ] **Step 2: Add pluginData write after audit scan**

In `controller.ts`, after the `audit-result` postMessage (line 499), add:

```typescript
const auditOutput = JSON.stringify({
  timestamp: Date.now(),
  scope: msg.scope ?? "page",
  instances: result.instances.length,
  variables: result.variables.length,
  styles: result.styles.length,
  detached: result.detached.map(d => ({
    nodeId: d.nodeId,
    nodeName: d.nodeName,
    pageName: d.pageName,
    detachedFrom: d.detachedFrom,
  })),
});
figma.root.setPluginData("tone_audit_results", auditOutput);
```

- [ ] **Step 3: Build and test**

```bash
cd tone-lint && npm run build
```

Open Tone Lint in Figma, run a lint scan, then verify pluginData was written by running via use_figma:
```javascript
return figma.root.getPluginData("tone_lint_results");
```

- [ ] **Step 4: Commit**

```bash
git add src/plugin/controller.ts
git commit -m "feat: write lint/audit results to pluginData for agent consumption"
```

---

## Chunk 2: Remove Token Requirement from Auditor

### Task 2: Create Library Key Loader

**Files:**
- Create: `tone-lint/src/plugin/libraryKeys.ts`

This module loads the library key map from `clientStorage` (pre-populated by the agent setup script). The Auditor uses this instead of REST API calls.

- [ ] **Step 1: Write the library key loader**

```typescript
// libraryKeys.ts — loads pre-built library key map from clientStorage

const LIBRARY_KEYS_CACHE = "tc_library_keys";

export interface LibraryKeyMap {
  componentKeys: Record<string, string>; // componentKey → libraryName
  styleKeys: Record<string, string>;     // styleKey → libraryName
  syncedAt: number;
}

export async function getLibraryKeyMap(): Promise<LibraryKeyMap | null> {
  const raw = await figma.clientStorage.getAsync(LIBRARY_KEYS_CACHE);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as LibraryKeyMap;
  } catch {
    return null;
  }
}

export async function setLibraryKeyMap(map: LibraryKeyMap): Promise<void> {
  await figma.clientStorage.setAsync(LIBRARY_KEYS_CACHE, JSON.stringify(map));
}
```

- [ ] **Step 2: Commit**

```bash
git add src/plugin/libraryKeys.ts
git commit -m "feat: add library key map loader for token-free auditor"
```

### Task 3: Wire Library Keys into Audit Results

**Files:**
- Modify: `tone-lint/src/plugin/controller.ts` (audit-result handler)

- [ ] **Step 1: Enrich audit results with library names in the plugin sandbox**

In `controller.ts`, modify the `scan-audit` case to resolve library names before sending to UI:

```typescript
case "scan-audit": {
  const result = await scanAudit(msg.scope ?? "page");

  // Resolve library names from cached key map (set by agent setup)
  const keyMap = await getLibraryKeyMap();
  let enrichedResult = result;

  if (keyMap) {
    // Attach library names directly to audit results
    enrichedResult = {
      ...result,
      instances: result.instances.map(inst => ({
        ...inst,
        libraryName: inst.isRemote
          ? (keyMap.componentKeys[inst.componentKey] || "⚠ Unknown library")
          : "This file"
      })),
      styles: result.styles.map(s => ({
        ...s,
        libraryName: s.isRemote
          ? (keyMap.styleKeys[s.styleKey] || "⚠ Unknown library")
          : "This file"
      })),
      detached: result.detached.map(d => ({
        ...d,
        libraryName: d.detachedFrom.type === "local"
          ? "This file"
          : (keyMap.componentKeys[d.detachedFrom.componentKey] || "⚠ Unknown library")
      })),
    };
  }

  figma.ui.postMessage({ type: "audit-result", result: enrichedResult, hasKeyMap: !!keyMap });

  // Write to pluginData for agents
  const auditOutput = JSON.stringify({
    timestamp: Date.now(),
    scope: msg.scope ?? "page",
    instances: enrichedResult.instances.length,
    variables: enrichedResult.variables.length,
    styles: enrichedResult.styles.length,
    detached: enrichedResult.detached.map(d => ({
      nodeId: d.nodeId,
      nodeName: d.nodeName,
      pageName: d.pageName,
      detachedFrom: d.detachedFrom,
      libraryName: (d as any).libraryName,
    })),
  });
  figma.root.setPluginData("tone_audit_results", auditOutput);
  break;
}
```

- [ ] **Step 2: Commit**

```bash
git add src/plugin/controller.ts
git commit -m "feat: resolve library names in plugin sandbox via cached key map"
```

### Task 4: Simplify AuditorPanel — Remove Token Requirement

**Files:**
- Modify: `tone-lint/src/app/components/AuditorPanel.tsx`

- [ ] **Step 1: Remove REST API calls and token input**

The key changes to `AuditorPanel.tsx`:
1. Remove `token` state and the password input
2. Remove `fetchLibraryItems()` and `buildKeyMaps()` functions
3. Remove `restProgress` state
4. Use `libraryName` from enriched audit results (pre-resolved in sandbox)
5. Show a warning banner if `hasKeyMap` is false ("Run agent library sync for full library names")

The scan function becomes simply:

```typescript
async function scan() {
  setScanState("running");
  setResult(null);
  setSearch("");
  parent.postMessage({ pluginMessage: { type: "scan-audit", scope } }, "*");
}
```

The Instances/Detached/Bindings tabs read `libraryName` directly from the audit result items instead of looking it up in a local keyMap.

- [ ] **Step 2: Build and test**

```bash
cd tone-lint && npm run build
```

Open Tone Lint Auditor in Figma. Scan should work without entering a token. Library names show as "⚠ Unknown library" until agent sync runs.

- [ ] **Step 3: Commit**

```bash
git add src/app/components/AuditorPanel.tsx
git commit -m "feat: remove REST API token requirement from Auditor — uses cached key map"
```

---

## Chunk 3: Agent Setup and Reader Scripts

### Task 5: One-Time Library Sync Script

**Files:**
- Create: `tools/tone-lint-agent/sync-libraries.js`

This script runs once via `use_figma` on each Tone library file, collecting all component and style keys. The agent merges results and stores the combined key map.

- [ ] **Step 1: Write the library key collector**

```javascript
// sync-libraries.js — Run via use_figma on ONE Tone library file
// Returns all component keys and style keys from this file
// Agent runs this on each library file, merges results, stores via store-keys.js

async function collectKeys() {
  const components = [];
  const styles = [];

  // Collect component keys from all pages
  for (const page of figma.root.children) {
    await page.loadAsync();
    const comps = page.findAll(n => n.type === "COMPONENT" || n.type === "COMPONENT_SET");
    for (const c of comps) {
      components.push({ key: c.key, name: c.name });
    }
  }

  // Collect style keys
  const textStyles = await figma.getLocalTextStylesAsync();
  const effectStyles = await figma.getLocalEffectStylesAsync();
  const gridStyles = await figma.getLocalGridStylesAsync();

  for (const s of textStyles) styles.push({ key: s.key, name: s.name, type: "text" });
  for (const s of effectStyles) styles.push({ key: s.key, name: s.name, type: "effect" });
  for (const s of gridStyles) styles.push({ key: s.key, name: s.name, type: "grid" });

  return { fileName: figma.root.name, components, styles };
}

const result = await collectKeys();
return JSON.stringify(result);
```

- [ ] **Step 2: Write the key map store script**

```javascript
// store-keys.js — Run via use_figma on ANY file (e.g. the target product file)
// Stores the merged library key map in clientStorage
// Agent replaces __KEY_MAP_JSON__ with the merged map

const keyMap = __KEY_MAP_JSON__;
await figma.clientStorage.setAsync("tc_library_keys", JSON.stringify(keyMap));
return "Library key map stored: " + Object.keys(keyMap.componentKeys).length + " components, " + Object.keys(keyMap.styleKeys).length + " styles";
```

- [ ] **Step 3: Document the agent workflow**

The agent runs this workflow once (or when libraries are updated):

```
1. For each library in TONE_LIBRARIES:
   use_figma(fileKey: lib.fileKey, code: sync-libraries.js) → { components, styles }

2. Merge all results into a single keyMap:
   { componentKeys: { key: libraryName, ... }, styleKeys: { key: libraryName, ... }, syncedAt: Date.now() }

3. Store the merged keyMap:
   use_figma(fileKey: anyFile, code: store-keys.js with __KEY_MAP_JSON__ replaced)
```

Total cost: ~5K tokens one-time. Libraries: Foundations, Components, Patterns, Legacy, + squad patterns.

- [ ] **Step 4: Commit**

```bash
git add tools/tone-lint-agent/sync-libraries.js
git commit -m "feat: add one-time library key sync script for agent setup"
```

### Task 6: Agent Reader Scripts

**Files:**
- Create: `tools/tone-lint-agent/read-lint-results.js`
- Create: `tools/tone-lint-agent/read-audit-results.js`

- [ ] **Step 1: Write the lint results reader**

```javascript
// read-lint-results.js — ~50 tokens to read
// Run via use_figma on the file that was linted
return figma.root.getPluginData("tone_lint_results") || '{"error": "No lint results found. Run Tone Lint plugin first."}';
```

- [ ] **Step 2: Write the audit results reader**

```javascript
// read-audit-results.js — ~50 tokens to read
return figma.root.getPluginData("tone_audit_results") || '{"error": "No audit results found. Run Tone Lint Auditor first."}';
```

- [ ] **Step 3: Commit**

```bash
git add tools/tone-lint-agent/read-lint-results.js tools/tone-lint-agent/read-audit-results.js
git commit -m "feat: add lightweight agent reader scripts for lint/audit results"
```

---

## Chunk 4: Skill Updates

### Task 7: Update DS Producer and Consumer Skills

**Files:**
- Modify: `skills/ds-producer/SKILL.md`
- Modify: `skills/ds-consumer/SKILL.md`

- [ ] **Step 1: Update Producer Tone Lint section**

Replace the current Tone Lint section with:

```markdown
### Tone Lint (Native Plugin + Agent Bridge)

**For the team:** Run Tone Lint natively in Figma — zero AI token cost. The plugin writes results to pluginData automatically.

**For agents:** Read lint/audit results via `use_figma` (~50 tokens per read):
- Lint: `use_figma(fileKey, code: 'return figma.root.getPluginData("tone_lint_results")')`
- Audit: `use_figma(fileKey, code: 'return figma.root.getPluginData("tone_audit_results")')`

**For targeted fixes:** Apply individual fixes via `use_figma` (~500 tokens):
- Variable binding: Import variable by key, bind to node property
- Text style: Import style by key, apply to text node
- Reattach: Import component by key, create instance, copy text, replace detached node

**One-time setup:** Run `tools/tone-lint-agent/sync-libraries.js` on each Tone library file to pre-build the library key map (~5K tokens total, run once).
```

- [ ] **Step 2: Update Consumer detached component section**

Add to Workflow 5:

```markdown
**Agent reads detached components:** After user runs Tone Lint Auditor, read results:
`use_figma(fileKey, code: 'return figma.root.getPluginData("tone_audit_results")')`
The `detached` array lists all detached components with their original library source.
```

- [ ] **Step 3: Commit**

```bash
git add skills/ds-producer/SKILL.md skills/ds-consumer/SKILL.md
git commit -m "feat: update skills with agent-friendly Tone Lint integration"
```

---

## Execution Notes

**Build order:** Task 1 (pluginData output) → Task 2-4 (token removal) → Task 5-6 (agent scripts) → Task 7 (skill updates)

**Testing:** After each task, rebuild the plugin (`npm run build`) and test in Figma.

**The Auditor token removal is backward-compatible:** If the library key map hasn't been synced yet, the Auditor still works — it just shows "⚠ Unknown library" for remote components. No functionality is lost.

**Future: Auto-sync trigger.** The plugin could detect when the library key map is stale (comparing `syncedAt` to library `lastModified`) and show a "Sync needed" indicator. But this is YAGNI for now.
