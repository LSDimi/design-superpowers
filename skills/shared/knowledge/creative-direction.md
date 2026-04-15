# Creative Direction (L2)

> Loaded by /creative sub-agents. Covers configurable dials, moodboard method, theme statements, and translation to tokens.

## Configurable Dials

Four dials shape the output of every creative exploration. Users set them explicitly or implicitly through word choice. Default to the middle value unless cues suggest otherwise.

| Dial | Low | Mid | High | Read from user as |
|------|-----|-----|------|-------------------|
| **Creativity** | Safe — familiar patterns, minimal risk | Balanced | Bold — unconventional, provokes reaction | "clean/professional" → safe; "unexpected/fresh" → bold |
| **Density** | Airy — lots of whitespace, few elements per view | Balanced | Packed — high information density, compact spacing | "breathable/minimal" → airy; "data-rich/dashboard" → packed |
| **Variance** | Uniform — one visual style, tightly consistent | Balanced | Playful — deliberate variation in size, color, texture | "enterprise/serious" → uniform; "expressive/brand-forward" → playful |
| **Motion** | Static — no animation by default | Balanced | Kinetic — motion is a primary communication tool | "accessible/fast" → static; "engaging/dynamic" → kinetic |

**How to apply:** State the dial settings before proposing any direction. Example: "Treating this as: Creativity=Balanced, Density=Packed, Variance=Uniform, Motion=Static."

## Moodboard Method

A structured approach to extract signal from references before generating anything.

### Step 1 — Gather references (5–7 sources)
Sources can include: existing product UIs, brand identities, physical products, editorial layouts, art movements, architecture. Aim for variety — at least 2 outside the direct category.

### Step 2 — Extract traits (3–5 per reference)
For each reference, name specific observable traits — not vague adjectives. Use:
- **Visual traits:** color temperature, contrast ratio, stroke weight, spatial density
- **Structural traits:** grid type, hierarchy levels, rhythm
- **Emotional traits:** what feeling does it trigger? (max 1–2 per reference)

### Step 3 — Cluster and synthesize
Group traits that appear in ≥2 references. Discard unique traits. The cluster that survives is the design signal.

### Step 4 — Write the theme statement
Synthesize the cluster into a single theme statement (see template below). Everything downstream — palette, type, motion — should be defensible against this statement.

## Theme Statement Template

Format: `<adjective> + <adjective> + <noun>`

- The adjectives describe feeling and character.
- The noun names a world or domain the design inhabits.
- Together they give the design a point of view.

**Examples:**
- `precise, confident, utilitarian` — B2B ops tool
- `warm, layered, editorial` — content-first consumer app
- `sharp, minimal, instrument` — developer tooling
- `playful, structured, workshop` — educational product

**Test:** Can you reject a design decision because it violates this statement? If yes, the statement is strong. If everything passes, it's too vague — tighten it.

## Translation to Tokens

The theme statement drives token decisions. Apply in order:

| Theme dimension | Token category | Decision rule |
|-----------------|---------------|---------------|
| Adjective 1 (character) | Color palette — hue, saturation | "Confident" → higher chroma brand color; "Restrained" → desaturated neutrals |
| Adjective 2 (feeling) | Typography — weight, letter-spacing | "Warm" → humanist sans, looser tracking; "Precise" → geometric, tighter |
| Noun (world) | Spacing rhythm + radius | "Instrument" → tight 4px grid, 0–2px radius; "Workshop" → 8px grid, generous radius |
| Creativity dial | Variance in scale steps | Safe → fewer, closer steps; Bold → wider range, more contrast |
| Motion dial | Duration + easing type | Static → 0ms transitions; Kinetic → spring physics, 200–500ms |

Work through each row before opening color theory or typography files. Anchor every choice to the theme.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|-------------|--------------|-----|
| **Reference collage** — combining 7 references without synthesis | Produces contradiction, not direction | Complete Step 3 (cluster) before generating anything |
| **Skipping the theme statement** | Decisions lack a shared rationale; reviews become subjective | Always write the statement even if it feels obvious |
| **Overfitting to one reference** | Derivative, not original | Require at least one reference outside the direct category |
| **Dial drift** — changing dials mid-exploration without announcing | Inconsistent output; confuses stakeholders | Restate dials at the start of each new sub-agent call |
| **Adjective inflation** — "modern, clean, bold, friendly, professional" (5+ adjectives) | No point of view | Cap at 3 adjectives; force ranking if there are more |

## L3 Lookup

When you need a deeper reference during evaluation, query these CSVs with Grep:

- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv` — cognitive + perceptual principles
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/ecommerce-usability.csv` — forms, checkout, search patterns
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/usability-homepage.csv` — homepage, nav, filtering patterns
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/design-principles.csv` — classic design frameworks

**Query pattern:** `Grep pattern="<keyword>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/<file>.csv"`
**Use sparingly:** Query only when a specific finding needs backing, not speculatively.
