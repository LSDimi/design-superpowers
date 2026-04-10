# UX Heuristics (L2)

> Loaded by /design-review UX Critic, /design Layout Composer. Use for heuristic evaluation and cognitive load assessment.

## Nielsen's 10 Heuristics

| # | Heuristic | Definition | Do | Don't | Severity |
|---|-----------|------------|----|-------|----------|
| 1 | Visibility of System Status | System always keeps users informed about what's happening. | Show progress indicators, loading states, success/error feedback. | Leave users guessing after actions; no feedback on long operations. | Critical |
| 2 | Match Between System and Real World | Use language and concepts familiar to the user. | Use plain language; align mental models to real-world metaphors. | Use internal jargon, database field names, or engineering terms in UI. | Critical |
| 3 | User Control and Freedom | Users need a clearly marked emergency exit from unintended states. | Provide Undo, Cancel, Back; never trap users in a flow. | Force completion of a flow; make destructive actions irreversible. | Critical |
| 4 | Consistency and Standards | Users shouldn't wonder if different words, situations, or actions mean the same thing. | Follow platform conventions; use the same patterns for same actions. | Use different labels for identical actions; invent novel interaction patterns without cause. | High |
| 5 | Error Prevention | Prevent problems from occurring in the first place. | Disable invalid options; confirm destructive actions; validate inline. | Show errors only after submission; allow obviously invalid input. | Critical |
| 6 | Recognition Over Recall | Minimize memory load by making options visible. | Show options rather than requiring users to remember commands. | Require memorizing codes, IDs, or sequences to complete tasks. | High |
| 7 | Flexibility and Efficiency | Allow experts to speed up interactions. | Provide shortcuts, bulk actions, keyboard navigation. | Force all users through the beginner path; no power-user affordances. | High |
| 8 | Aesthetic and Minimalist Design | Every extra unit of information competes with relevant information. | Show only what's needed for the current task. | Display rarely-needed info alongside critical info; cluttered dashboards. | High |
| 9 | Help Users Recognize, Diagnose, and Recover from Errors | Error messages should be plain language and suggest a solution. | Explain what went wrong and how to fix it; use plain language. | Show raw error codes; blame the user; offer no recovery path. | Critical |
| 10 | Help and Documentation | Sometimes users need help; provide it where needed. | Contextual tooltips, inline guidance, progressive disclosure of help. | Require users to leave the task to find a manual. | Medium |

## Cognitive Load Framework

Three types of cognitive load affect usability:

| Type | Description | Design lever |
|------|-------------|-------------|
| **Intrinsic** | Complexity inherent to the task itself | Can't eliminate; simplify where possible via IA and chunking |
| **Extraneous** | Load imposed by poor design — clutter, unclear hierarchy | Eliminate via clean layout, clear labels, reduced noise |
| **Germane** | Load that builds useful mental models | Optimize via consistent patterns, progressive disclosure |

**Measuring extraneous load:**
- Count decision points per screen (target ≤3 primary decisions per view)
- Count words on screen excluding content (fewer = better)
- Run a 5-second test: what is the user supposed to do? If unclear → extraneous load too high

## IA Principles

- **Discoverability:** Users can find features without being told. Navigation labels match user vocabulary.
- **Findability:** Search works for things users know exist. Browsing works for exploration.
- **Scanability:** Users can get value without reading everything. Hierarchy, bold labels, and grouping carry the load.
- **Predictability:** Clicking X always does the same thing. No surprising context-dependent behavior.

## Severity Rubric

| Level | Name | Definition | Action required |
|-------|------|------------|-----------------|
| **P0** | Blocker | Prevents task completion; causes data loss or security risk | Fix before release |
| **P1** | Major | Causes significant confusion or repeated error; workaround exists but painful | Fix in current sprint |
| **P2** | Minor | Sub-optimal; users can complete task but with friction | Fix in next sprint |
| **P3** | Cosmetic | Aesthetic or polish issue; no functional impact | Backlog |

## Evaluation Output Format

When reporting findings, use this table format:

| # | Heuristic | Location | Issue | Severity | Suggestion |
|---|-----------|----------|-------|----------|------------|
| 1 | Error Prevention (#5) | Bulk delete modal | No confirmation of how many records will be deleted | P1 | Show count: "Delete 47 campaigns?" |
| 2 | Visibility of Status (#1) | Export CSV button | No loading state; button appears frozen during 5s export | P0 | Add spinner + "Exporting…" label |

Group findings by severity (P0 first). Include a summary count at the top: `Found: 2 P0, 3 P1, 5 P2, 2 P3`.

## L3 Lookup

When you need a deeper reference during evaluation, query these CSVs with Grep:

- `skills/shared/data/psychological-principles.csv` — cognitive + perceptual principles
- `skills/shared/data/ecommerce-usability.csv` — forms, checkout, search patterns
- `skills/shared/data/usability-homepage.csv` — homepage, nav, filtering patterns
- `skills/shared/data/design-principles.csv` — classic design frameworks

**Query pattern:** `Grep pattern="<keyword>" path="skills/shared/data/<file>.csv"`
**Use sparingly:** Query only when a specific finding needs backing, not speculatively.
