# Visual Quality (L2)

> Loaded by /design-review Visual Quality Inspector, /map-design Visual Parser. Covers alignment, spacing, rhythm, balance, hierarchy verification, and inspection checklist.

## Alignment Rules

**Edge alignment** — elements sharing a visual relationship should share an edge. Left-aligned text in a column? All labels align left. Card grid? All cards align top.

**Center alignment** — use for single centered elements (hero heading, empty state), not for multi-element columns. Center-aligned body copy is hard to read.

**Baseline alignment** — for mixed type sizes or icon+text pairs, align to the text baseline, not the bounding box top. A 12px label next to a 16px label aligned by bounding box will look off by ~2px.

**Alignment tolerance:** 0px. There is no "close enough." Off-by-1px misalignment is visible in screenshots and fails QA. Use a grid, use auto-layout (Figma), or use CSS Flexbox — do not eyeball.

**Grid alignment vs. visual alignment:** Sometimes strict grid alignment creates optical misalignment (e.g., rounded icons look smaller than flat ones at the same bounding box). Apply optical adjustment only when the math-correct position looks wrong — document the exception.

## Spacing Consistency

**Rule 1:** Only use values from the spacing token scale. No `13px`, `22px`, `37px`. If a design uses an off-scale value, either adjust to the nearest token or question the layout.

**Rule 2:** Consistent spacing across identical components. If two cards have different internal padding, one is wrong.

**Rule 3:** Proximity = relationship. Elements that belong together have smaller gaps between them than elements that belong to different groups. This is Gestalt's law of proximity — the primary tool for grouping without lines or boxes.

**How to audit spacing:**
1. Select two components of the same type and compare padding values — they must match.
2. Check that section gaps are larger than component-internal gaps.
3. Verify form fields: label-to-input gap should be consistent across all fields.

## Visual Rhythm

Rhythm is the repetition of visual elements at consistent intervals. It creates order and makes scanning easier.

**Horizontal rhythm** — consistent column alignment, consistent left margin for all body text, consistent icon sizes in a list.

**Vertical rhythm** — consistent `line-height` and `margin-bottom` (or `gap`) between stacked elements. Vertical rhythm is what makes a page feel "settled."

**How to detect broken rhythm:**
- Turn the screen to grayscale — irregular spacing becomes obvious without color distraction.
- Squint at the page — if your eye catches on a gap, the rhythm is broken there.

**Density consistency:** Components at the same hierarchy level should have the same padding scale. A dense data table next to an airy card breaks rhythm — they should be from the same density mode.

## Balance

**Symmetrical balance** — both halves of the composition carry equal visual weight. Default for enterprise/B2B UIs. Safe, structured, formal.

**Asymmetrical balance** — one side is heavier but balanced by contrast, white space, or color on the other. More dynamic; works well with strong hero sections or single focal points.

**Visual weight factors:**
- Larger elements are heavier.
- Darker elements are heavier than lighter ones.
- High-chroma colors are heavier than muted ones.
- Irregular shapes draw more attention than regular ones.
- Isolated elements have higher weight (white space amplifies focus).

**Common imbalance:** A heavy CTA button on the right of a form, with no balancing weight on the left — eye jumps to the button before reading the form. Fix: increase form label prominence or add visual anchor on left.

## Hierarchy Verification

Three quick tests to verify hierarchy without tools:

| Test | How to do it | What it reveals |
|------|-------------|----------------|
| **Squint test** | Defocus your eyes or squint at the screen | Only the top 1–2 hierarchy levels remain visible; if nothing stands out → no clear hierarchy |
| **3-second test** | Look at the screen for 3 seconds, look away. What did you see? | Whatever the user noticed first is the actual hierarchy — compare to intended hierarchy |
| **Grayscale test** | Remove all color (Figma: Desaturate; browser: `filter: grayscale(1)`) | Hierarchy must survive without color; if it collapses → over-reliance on color alone |

After each test, compare result to design intent. If the test-revealed hierarchy doesn't match the intended hierarchy, adjust size, weight, or color contrast accordingly.

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|-------------|---------|-----|
| **Fake alignment** — visually close but not on the grid | Visible in hi-res; fails pixel-level QA | Use Figma auto-layout or CSS flexbox; measure, don't eyeball |
| **Inconsistent border radii** — `4px` on some components, `6px` on others, `8px` on yet others | Feels unfinished; breaks visual language | Define 1–3 radius tokens and apply strictly |
| **Mixed icon stroke widths** — 1.5px strokes next to 2px strokes | Icons feel mismatched in the same view | Use one icon set with one stroke weight per project; `1.5px` or `2px`, not both |
| **Inconsistent shadow styles** — various box-shadows not from a token scale | Depth levels are arbitrary; no clear elevation story | Define elevation tokens: `shadow-sm`, `shadow-md`, `shadow-lg` |
| **Color for grouping without proximity** — colored backgrounds instead of spatial grouping | Adds visual noise; fails in grayscale | Use proximity and whitespace as primary grouping; color is secondary |

## Craft & Anti-Slop Tells

What separates competent from crafted — and the signature "tells" that mark AI-generated design. Screen for these before shipping.

**Craft moves (do):**
- **Design read first.** Before any pixels, state a one-line read: *page kind · audience · vibe · design-system/aesthetic family*. Everything downstream defends against it.
- **Restraint:** one accent color per surface, used consistently; off-black/off-white instead of pure #000/#fff; a single locked corner-radius system.
- **Tinted depth:** shadows tinted toward the background hue (never pure black), offset more vertically than horizontally, on a fixed elevation scale. As elevation rises, blur grows but opacity *drops* — heavier and lighter, not heavier and darker. In dark mode, prefer tonal elevation (a lighter surface tone per level, as in Material 3) over shadows, which barely register on dark surfaces; reserve shadows/scrims for elements needing extra separation (dialogs, FABs).
- **Shadow language follows the style family.** Each aesthetic has its own depth grammar — Swiss: none; neubrutalism: hard offset, zero blur; glassmorphism/Frutiger Aero: translucency and specular gloss, not fuzzy drops; neumorphism: dual light+dark extrusion (with its documented contrast failures). Mixing grammars (a soft blurred shadow on a neubrutalist card) is a craft failure. Recipes: `visual-styles.csv`.
- **Whitespace first:** start over-spaced and remove; tighten within a group, loosen between groups so proximity carries meaning.
- **Separate without borders** where possible (spacing / background shift / soft shadow); use a card only when elevation communicates real hierarchy.
- **Design every state:** loading (skeleton matching final shape, not a generic spinner), empty (composed, shows how to populate), error (inline for forms, toast for transient), plus tactile active feedback.
- **Layout variety:** each section a distinct layout family; grid cell count = item count with real visual variation.

**Generative "tells" (avoid — these cheapen otherwise good work):**
- Three identical equal-width feature cards; the same section template repeated down the page; mathematically perfect padding with no rhythm.
- Placeholder identity: generic names (John Doe), startup-slop names (Acme, Nexus, SmartFlow), filler verbs (Elevate, Seamless, Unleash, Next-Gen).
- Decoration noise: section-number eyebrows (`001 · Capabilities`), version labels in a marketing hero (`BETA`), scroll cues (`↓ scroll`), status dots before every item, poetic labels (`Field notes`).
- Fabrication: div-based fake product screenshots, fake-precise numbers (92%, 4.1×) not backed by real data or marked mock, overlaid pills/photo-credit captions on images.
- Emoji used as UI icons; hand-rolled SVG icon paths; mixed icon families; em-dash used as a decorative flourish in UI copy.
- Neon/outer glows, oversaturated accents, gradient-text headers, AI-purple by default.

**Context overrides aesthetic:** trust-, accessibility-, and safety-critical domains beat style (no heavy motion in accessibility-critical apps, no AI-purple in fintech, no dark-by-default for wellness/beauty).

## Inspection Checklist

Run before marking a screen ready for review:

- [ ] Every text element uses a type scale token (no ad-hoc font sizes)
- [ ] Every spacing value is on the token scale
- [ ] All components of the same type have identical internal spacing
- [ ] Icon sizes are consistent within the same context (all 16px or all 20px in a list)
- [ ] All border radii are from the token scale
- [ ] All shadows are from the elevation token scale
- [ ] Squint test passes — primary action is visually dominant
- [ ] Grayscale test passes — hierarchy is legible without color
- [ ] All left edges in a column are aligned (0px tolerance)
- [ ] Component spacing follows proximity principle (related = closer, unrelated = farther)

## L3 Lookup

When you need a deeper reference during evaluation, query these CSVs with Grep:

- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv` — cognitive + perceptual principles
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/usability.csv` — homepage, navigation, forms, commerce, feedback, trust patterns
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/design-principles.csv` — classic design frameworks
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/visual-styles.csv` — named style recipes, photography, illustration, motion aesthetics

**Query pattern:** `Grep pattern="<keyword>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/<file>.csv"`
**Use sparingly:** Query only when a specific finding needs backing, not speculatively.
