# Benchmark — design-superpowers v1.0.0 vs. popular AI-design skills (2026-07)

_All competitor data verified 2026-07-13/14 by direct repo/site inspection (star counts via GitHub API, CSV row counts by download-and-parse of the competitors' own public files). Comparisons are factual, not promotional; every library below is genuinely good at its job — the jobs differ._

## The field

| Dimension | **design-superpowers v1.0** | **impeccable.style** (pbakaus) | **taste-skill** (Leonxlnx) | **ui-ux-pro-max** (nextlevelbuilder) |
|---|---|---|---|---|
| Form | 6 command routers → 27 sub-agents, 4-layer knowledge | 1 skill, 23 commands + deterministic CLI detector | 13 flat SKILL.md files | 7 bundled skills + BM25 CSV search CLI |
| Primary job | **Run the full design practice**: direction → DS → product design → review → governance | Make AI-generated *code* look designed; catch slop in CI | Anti-slop taste for landing/marketing pages | Style/palette/font *catalog* + design-brief generator for code output |
| Audience | Design teams (varying AI experience) | Developers shipping UI code | Solo builders, vibe-coders | Developers across 19 AI tools |
| Adoption (verified) | New (v1.0, this week) | ~46k stars, Apache-2.0 | ~63k stars in 5 months, MIT | ~105k stars, 57k npm DL/mo, MIT (mixed sub-licenses) |

## Capability matrix (verified, not claimed)

| Capability | **design-superpowers v1.0** | **impeccable.style** (pbakaus) | **taste-skill** (Leonxlnx) | **ui-ux-pro-max** (nextlevelbuilder) |
|---|---|---|---|---|
| Project-maturity adaptation (greenfield → enterprise) | ✅ L0–L3 detection changes every command's behavior | ❌ | ❌ | ❌ |
| Figma integration (read/write, live node review) | ✅ via PluginOS peer plugin, graceful degradation | ❌ none | ❌ none | ❌ none |
| DS lifecycle: tokens, versioning, deprecation, publish cascade, adoption analytics | ✅ /ds-make + /ds-manage + L3 producer/consumer | ❌ (extract only) | ❌ | ❌ |
| Review of *existing* designs (severity-graded findings vs static checklist) | ✅ 5-lens /design-review, live Figma node reads | ✅ code/audit + critique (code/browser only) | Partial (redesign audit protocol) | ❌ (pre-delivery self-checklist) |
| Named style recipes **with when-to-avoid caveats** | ✅ 29, each caveated | Partial (anti-patterns, not style recipes) | Partial (3 style skills, banned-cliché list) | ✅ 84 styles (breadth winner), anti-patterns per style |
| Industry/audience → style/type/palette correlations with evidence-confidence + cultural caveats | ✅ 15 rows, confidence-annotated | ❌ | Partial (brief→DS routing table) | ✅ 161-row reasoning engine (no confidence/cultural annotation) |
| Font awareness of the **user's actual machine** + Figma | ✅ inventory scan + [installed]/[figma]/[needs-install] marks + deterministic class→font resolver | ❌ | ❌ | ❌ (static Google Fonts catalog, 1,923 rows — catalog winner, no machine scan) |
| Brand strategy (principles layer above named typologies) | ✅ two-layer brand-design.md + Brand Architect | ❌ (PRODUCT.md voice context) | ❌ (brandkit generator) | Partial (bundled brand templates) |
| Photography/art direction (lighting recipes, image briefs, AI-image handoff) | ✅ first-class L2 domain | ❌ | Partial (imagegen prompt skills) | Partial (image-gen via bundled skill) |
| Published eval evidence | ✅ 300+ scenario evals, results in-repo | ❌ | ❌ | ❌ |
| Deterministic CI-runnable linting | ❌ (via DS lint tools at L3) | ✅ **46-rule detector, no LLM — unique** | ❌ | Partial (CSV validation CI) |
| Live in-browser variant → source diff | ❌ | ✅ **`live` mode — unique** | ❌ | ❌ |
| Multi-harness distribution (Cursor/Codex/Gemini...) | ❌ Claude Code only | ✅ 12 harnesses | ✅ semi-universal SKILL.md | ✅ 19-tool CLI installer |
| Code scaffolding depth (per-stack implementation data) | Partial (React/ArkUI conventions) | ✅ code-first | ✅ code-first | ✅ 21 stack CSVs |

## Honest read

**Where the others are ahead:** distribution and adoption (all three are massively installed; we're at v1.0), multi-harness reach, and code-output ergonomics — impeccable's non-LLM CI detector and `live` HMR mode are mechanics nobody else has; ui-ux-pro-max's catalogs are the broadest raw data; taste-skill's banned-cliché list is the sharpest anti-slop prose in the field.

**Where design-superpowers is alone:** it's the only one built for the *design practice* rather than the code output — the only one that knows whether you're greenfield or governing an enterprise DS and behaves differently; the only one that touches Figma at all (read AND write); the only one with DS lifecycle/governance semantics; the only one that checks what fonts you actually have; the only one with a brand-strategy layer above templates; and the only one that ships its own eval evidence.

**Fair one-liner:** the other three make AI *output* look designed; design-superpowers makes AI *work like a design team*.

## Method note
Star counts are gameable and time-boxed; npm downloads and forks are harder to fake. All row counts parsed from live files, not READMEs (two of three repos had stale README numbers). This document should be re-verified before reuse after 2026-Q3.
