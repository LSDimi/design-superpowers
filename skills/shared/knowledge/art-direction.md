# Art Direction & Imagery (L2)

> Loaded by /creative Moodboard Generator and Brand Architect, /design-review Visual Quality Inspector (imagery findings), /design when a deliverable includes photography, illustration, or generated imagery. Covers imagery meaning, photographic composition and lighting, sequencing, and production/handoff including AI image generation.

Photography and illustration are not decoration bolted onto a design — they are part of the designed artefact. Every image in a deliverable is a design decision that must survive the same scrutiny as a token or a component choice.

## The Meaning Equation

**Meaning = Form + Content + Context.** An image earns its place only when all three are deliberate:

| Term | Question | Example failure |
|------|----------|-----------------|
| **Form** | How is it made — lighting, composition, palette, technique? | Beautiful photo whose warm palette fights the product's cool UI |
| **Content** | What does it show — subject, action, moment? | Generic stock handshake that says nothing specific |
| **Context** | Where does it sit — placement, neighbors, caption, surface? | Right photo placed next to an unrelated image, creating an accidental story |

**Acceptance test for hero/campaign imagery:** articulate all three in one sentence each. If any answer is "it just looked good," the image is not done.

## Composition & Timing

- **The Decisive Moment** — meaning lives in the exact instant where gesture, event, and composition align. Select frames at the peak instant (mid-air, mid-gesture), not just before or after. In product imagery: show the moment of value delivery, not the aftermath.
- **The Gaze** — identify whose gaze the viewer follows; it dictates the power structure of a portrait. Subjects should read as active agents shaping the story, not passive specimens. Eye-line and posture signal agency.
- **Environmental framing** — placing a subject in their territory (workplace, landscape, community) anchors identity. Wide depth of field keeps the context sharp and meaningful.
- **Scale shifting** — a small subject against a vast environment makes the environment the true subject. Use for narrative tension and reward-on-inspection compositions.

## Lighting Recipes

| Recipe | Setup | Emotional register | Use for |
|--------|-------|--------------------|---------|
| **Chiaroscuro** | Single directional key at ~45°, minimal fill, deep shadow falloff, black negative space | Drama, mystery, focus | Editorial heroes, premium/craft brands, texture emphasis |
| **High-key separation** | Background lit separately ~2 stops brighter than key (4:1) | Clean, open, commercial | E-commerce product shots, catalog imagery |
| **Atmospheric glow** | Soft ambient sources, pastel blue/green hues, soft shadows, bokeh | Cozy, calm, safe | Wellness, night modes, ambient brand moments |
| **Long exposure** | ≥10s shutter with ND filters; motion renders as pure tonality | Meditative, serene | Landscape moods, abstract brand texture |

Match the lighting register to the theme statement from `creative-direction.md` — a "precise, confident, utilitarian" theme and a chiaroscuro hero contradict each other.

## Sequencing Logic

Images speak to each other through proximity and order. A person fishing placed next to a fish stall reads as cause and effect — whether you intended it or not.

- Treat adjacent images as one composition; storyboard galleries and image runs before filling slots.
- Build deliberate cause-effect or thematic rhythm across a sequence.
- Audit for accidental juxtapositions in review — the unintended story is a finding.

## Color as Structure

Color in imagery defines the world, not the decoration: mist, artificial light, and architectural lines form a coherent atmosphere; palette signals internal states and social meaning. Keep one photographic tension per palette, and keep atmosphere palettes consistent within a narrative sequence. Grade imagery toward the product palette's temperature — or document why it deliberately departs.

## Imagery Production & Handoff

When a deliverable needs imagery, offer the user the production path — never silently leave gray boxes.

**Capability ladder (graceful degradation):**
1. **Image-generation tooling available** (image-gen MCP, Figma "Make an image" / "Edit image" / Weave on AI-enabled plans): offer to generate or edit imagery as part of the deliverable. Ask before generating; label outputs AI-drafted.
2. **No raster generation available:** deliver an **image brief** (below) that a human, Figma AI, or an image model can execute, plus an SVG/CSS placeholder so layout review stays honest on spacing and contrast.
3. **Sourcing real photography:** recommend CC0/open-license libraries; keep a license/attribution manifest per asset; flag generic stock (handshakes, pointing-at-whiteboard) as a design smell.

**Image brief format** (also the prompt structure for image models). The promptable core (Subject through Color/mood) has a **hard cap of 60 words — count them before delivering**; under 30 leaves too much to the model, over 60 dilutes or truncates. Placement/Aspect/Target are handoff metadata outside the count:

```
Subject: <specific subject and action>
Style: <one art/photo movement + 1–2 modifiers>
Composition: <angle, lens (e.g. 35mm low-angle, 85mm portrait), framing, focal placement>
Lighting: <source, direction, quality — use the recipes above: chiaroscuro, high-key, rim light, golden hour>
Color/mood: <palette temperature, atmosphere>
Placement: <where it sits in the layout> · Aspect: <ratio> · Target: <resolution/format>
```

**Rules:**
- Never present AI-drafted or placeholder imagery as production-ready — label it in the deliverable.
- Placeholder services and doodle generators are fine during prototyping, clearly marked non-final.
- Real product UI beats abstract metaphor illustration on marketing surfaces; never fabricate fake product screenshots and pass them as real.

## Imagery Review Checklist

- [ ] Meaning Equation articulated for every hero/campaign image (form, content, context)
- [ ] Gaze and agency read as intended; no accidental power imbalance
- [ ] No accidental juxtaposition stories in image sequences
- [ ] Lighting register matches the theme statement
- [ ] Imagery palette coheres with (or deliberately contrasts) the product palette
- [ ] Text over images keeps consistent contrast (overlay/scrim per usability corpus)
- [ ] AI-generated and placeholder assets labeled; licenses recorded for sourced assets
- [ ] No generic-stock smell; no fabricated product screenshots

## L3 Lookup

When a finding needs principle backing, query with Grep:

- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/visual-styles.csv` — style recipes, photography, illustration, motion aesthetics
- `${CLAUDE_PLUGIN_ROOT}/skills/shared/data/psychological-principles.csv` — perception principles (gaze, canonical perspective, peripheral vision)

**Query pattern:** `Grep pattern="<keyword>" path="${CLAUDE_PLUGIN_ROOT}/skills/shared/data/<file>.csv"`
**Use sparingly:** query when a specific finding needs backing, not speculatively.
