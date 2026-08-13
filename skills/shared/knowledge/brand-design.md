# Brand Design (L2)

> Loaded by /creative Brand Architect, and Moodboard Generator on brand-level briefs. Organized in two layers: **Layer 1 — universal brand-design principles** that govern every engagement, then **Layer 2 — named typologies** with tighter application definitions. Generic principles always outrank stylistic expression; a named model is applied *within* them, never instead of them.

## Layer 1 — Universal Principles

### Distinctive assets ≠ differentiation
Non-verbal cues (color, shape, logo, character, sound, packaging) trigger brand recall independent of the name. They build *fame*, not meaning — distinctiveness (being recognized) is a different job from differentiation (being preferred).

- Audit assets on the **fame × uniqueness grid**: Core (high/high — protect and scale), Shared cues (famous but generic — sharpen or you're advertising the category), Emergers (unique but unknown — invest), Non-assets (retire).
- Assets bind strongest when paired with specific buying/use contexts — design the pairing, not just the asset.
- **Anti-pattern:** redesigning a high-fame asset for aesthetic reasons. Recognition built over years erodes in one refresh; a Refresh Strategist "retire" verdict on a Core asset needs business evidence, not taste.

### Consistency builds mental availability
Mental availability — the probability a buyer recalls the brand at a buying moment — is built by repeated, undistorted exposure to the same cues. Most tested brand assets (~85%) are not attributable to their brand; repetition, not novelty, closes that gap.

- Keep the fixed cues fixed across campaigns, surfaces, and time; vary the message, not the identity.
- **Anti-pattern:** campaign-by-campaign creative reinvention that drops the fixed cues in favor of novelty.

### Promise must match product truth
Brand promise is aspirational (belonging, identity, meaning); product truth is what the product actually delivers. Design carries the emotional register — but if the visual/verbal system writes checks the product can't cash, the brand reads as hollow on first use.

- Verify each aspirational design element against a deliverable product behavior.
- **Anti-pattern:** lofty imagery + lofty copy over an unchanged mediocre experience.

### Equity pillars as a critique lens
Every touchpoint either reinforces or dilutes one of the five equity pillars (loyalty, awareness, perceived quality, associations, proprietary assets — Aaker). In critique, ask of any element: *which pillar does this serve?*

- Recognition (aided) and recall (unaided) are distinct design targets: lockup clarity serves recognition; category framing and positioning serve recall.

### Flexibility with coherence
Identity systems flex across touchpoints by fixing a core (grid, mark logic, color system) and varying the surface. The fixed/variable ratio is a deliberate design decision.

- Every flexible system = named fixed elements + named variable elements. If you can't list both, the system is ungoverned.
- **Anti-pattern:** "flex without governance" — unbounded variation degrades into inconsistency indistinguishable from off-brand use.

### Voice–visual alignment
Verbal personality and visual identity must express the same attributes. Map tone words ("confident, warm, precise") to visual attributes (contrast, roundness, saturation) and check they point the same direction — a playful voice over severe minimalist visuals reads as two brands.

- **Anti-pattern:** verbal and visual identity documented and governed by separate teams with no shared attribute vocabulary.

## Layer 2 — Named Typologies

### Brand archetypes (12)
Use as a shorthand for register, not a horoscope — pick one primary (max one secondary), then translate:

| Archetype | Typography direction | Palette | Imagery register |
|-----------|---------------------|---------|------------------|
| Innocent | Rounded simple sans | Pastels, white, soft pink | Minimal, negative space |
| Sage | Structured serif | Navy, deep green, neutrals | Restrained, editorial |
| Explorer | Bold sans | Earth tones | Outdoor, wide-open, action |
| Hero | Geometric bold sans | High-contrast red/orange/electric blue | Dynamic action |
| Outlaw | Distressed/rough display | Clashing, dark + acid | Raw texture, rebellion |
| Magician | Geometric, mystical marks | Deep purple, gradients, light | Transformation |
| Lover | Italic/script accents | Rich reds, pinks | Sensual texture, soft light |
| Jester | Playful casual | Saturated multicolor | Whimsical, unconventional |
| Everyman | Approachable, unadorned | Muted blue, soft green | Relatable people, warm settings |
| Caregiver | Rounded friendly | Pale blue, warm pink | Generous whitespace, gentle |
| Ruler | High-end serif | Black, gold, deep tones, metallics | Symmetrical, formal |
| Creator | Expressive, varied | Diverse multicolor | Asymmetric, process-revealing |

Quick grouping — Stability: Innocent/Sage/Explorer · Change: Outlaw/Magician/Hero · Belonging: Lover/Jester/Everyman · Order: Caregiver/Ruler/Creator.

### Brand architecture (4 types)
| Type | Model | Choose when |
|------|-------|-------------|
| Branded house | One master brand, descriptive products (Google) | High audience/category overlap; consistency beats segment nuance |
| House of brands | Independent brands, invisible parent (P&G) | Categories/audiences diverge widely; acquisitions carry standalone equity |
| Endorsed | Sub-brands backed by visible parent (Marriott lines) | Adjacent-category expansion that borrows parent trust |
| Hybrid | Mixed rules per unit (Microsoft) | Only with documented, governed per-unit rules — else it collapses |

Decision axes: category distance · growth strategy (organic vs acquisitive) · audience diversity. Always state the rule for naming the *next* product.

### Identity-system types
- **Static/monolithic** — one fixed logo and palette everywhere. Dependable, rigid.
- **Flexible system** — bounded, governed variation: fixed core + deliberately variable elements. The practical enterprise default.
- **Dynamic/generative** — algorithmic variation from a rule-set (MIT Media Lab's 7×7 grid → ~40,000 marks). Highest expressiveness, highest governance cost.

### Practice philosophies
Different organizational needs call for different practice models (exemplified by how the major identity practices position themselves). Name the working philosophy in one line before proposing visuals — it disciplines every downstream choice.

| Organizational need | Philosophy | Practice emphasis |
|---------------------|-----------|-------------------|
| Iconic identity for a cultural/institution-grade client | **Identity-first** (Pentagram model) | Partner-led craft; the mark and system carry the story |
| Business transformation across sonic, motion, visual | **Transformation-first** (Landor model) | Brand as a change program; every surface in scope |
| Strategy that must land emotionally | **Meaning-first** (Mucho model) | Translate strategy into emotional visual systems |
| Regulated/complex org drowning in messaging | **Simplicity-first** (Siegel+Gale model) | Message simplification before any styling |
| Org whose culture must change, not just its look | **Point-of-view-first** (Wolff Olins model) | Brand as organizational-change lever |
| Brand as belief + behavior, not communication | **Belief-first** (Collins model) | What we believe (internal) + how we behave (external), via story, symbol, responsive system |

### Identity audit lens (Kapferer prism)
Six facets: Physique, Personality, Culture, Relationship, Reflection, Self-image. Audit whether the visual system covers all six — most over-index on Physique (the look) and leave Culture and Self-image unexpressed.

## Brand → Product Bridge

- **Tokens are the translation layer.** Brand guidelines land in product as design tokens (W3C Design Tokens format is now standard; semantic token layer + swappable brand "skins" serves house-of-brands/hybrid architectures from one codebase).
- **Dynamic identities enter product UI as parameterized tokens** (gradient-generation rules, variable-font axis ranges), not fixed hex values — the generative core runs inside the token pipeline.
- The concrete mapping (brand color → functional palette roles, logo clear-space → spacing tokens, voice → motion register + imagery direction) is the Brand Architect's **translation contract** — see `/creative` Brand Architect workflow.

## L3 Lookup

- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv` — association and persuasion backing (limbic decisions, social proof, anecdotes)
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/visual-styles.csv` — style recipes once the brand register is chosen
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/design-principles.csv` — SUCCES rows for message stickiness
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/style-contexts.csv` — industry/audience → style, typography, palette correlations

**Query pattern:** `Grep pattern="<keyword>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/<file>.csv"`
**Use sparingly:** query when a specific finding needs backing, not speculatively.
