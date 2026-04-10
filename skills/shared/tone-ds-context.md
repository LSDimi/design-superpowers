# Tone DS Context

Shared context for all Tone DS skills. Both DS Producer and DS Consumer reference this file.

## Project Context File

This file serves as the `.ds-context.md` equivalent for Tone DS. When /map-design or /ds-manage detect Tone specifically, they load this file for L3 context. Projects on other design systems should maintain their own `.ds-context.md` at the repo root with similar structure.

## Tone DS Identity

Tone is Talon.One's design system. It provides foundations, components, patterns, and squad patterns organized across dedicated Figma files.

## Token Architecture

Three tiers:
- **Primitive** — Raw values (color scales, spacing units, type scales)
- **Semantic** — Purpose-mapped (e.g. `color.text.primary`, `spacing.gap.md`)
- **Component** — Scoped to specific components (e.g. `button.padding.lg`)

## Figma File Map

| File | Key | Purpose |
|------|-----|---------|
| Foundations | `Pn9sIWsLKN7gQKj1RkV75j` | Primitive + semantic tokens, shared styles |
| Components | `rVLnzp5jPQee88ThJR81Ha` | Component library with variants |
| Components Demo | `Lwxy3Us24a0UoTqQEdpbev` | Showcases, behavioral guidelines, property tables |
| Patterns (L1) | `H4A6DU7tCNJ7Qt4UwCuQy2` | Cross-component compositions |
| Squad Patterns (L2) | `qGiniOnkCUIww81UKNUkSs` | Domain-specific patterns (e.g. Gamification) |
| Checklist | `QCQcWpr372QodwEhZF1qbM` | Governance checklists per artifact type |
| Final files | Per-feature | Where DS Consumer works (e.g. `26niLy8kJmmrGIH9XFRo9c`) |

## Talon.One Product Context

Talon.One is an API-first Promotion Engine and Loyalty Platform. Primary UI: **Campaign Manager** (business users). Developer interfaces: Integration API, Management API.

### Core Entities

| Entity | Definition | Design Relevance |
|--------|-----------|-----------------|
| Application | Connected integration point (storefront, app, POS) | App switcher, scoping |
| Campaign | Rule container with budget, schedule, states (Draft/Active/Inactive/Expired) | Primary object for UI |
| Rule | Conditions → Effects logic | Rule Builder (most complex UI) |
| Effect | Outcome: setDiscount, addFreeItem, addLoyaltyPoints, createCoupon, etc. | Effect picker/configurator |
| Customer Profile | Persistent user record with attributes and loyalty balances | Profile explorer |
| Customer Session | Shopping cart/checkout interaction | Session history tables |
| Audience/Segment | Reusable customer groups for targeting | Query-builder pattern |
| Coupon | Promotional codes (unique/generic) | Bulk management tables |
| Referral Code | Shareable codes triggering referral effects | Distribution management |
| Loyalty Program | Cross-application points/tiers system | Tier ladder, points ledger |
| Achievement | Customer milestone/recognition | Progress indicators |
| Attribute | Custom extensible property on any entity | Schema editor |
| Giveaway | Promotional distribution pool | Pool management |
| Store | Physical or virtual retail location | Location context |
| Collection | Named value lists for rule conditions | List management |
| Webhook | Outbound event notifications | Subscription config |

### Terminology Rules

Always use Talon.One terms: Campaign (not "promotion"), Application (not "project"), Effect (not "action"), Profile (not "user record"), Session (not "cart"), Ruleset (not "rule group").

## Tech Stack

- **Design:** Figma — inspect via Figma MCP
- **Code:** React, ArkUI, Zag.js
- **Documentation:** uSpec (generates specs from Figma via MCP)
- **Project management:** Shortcut (tickets, changelogs, comments)
- **Figma plugins:** Tone Lint (validation + audit), Library Analytics (adoption metrics), Prostar (property tables)

## Interaction Pattern

Before executing any non-trivial task, ask 2-3 targeted questions to:
1. Clarify scope (which components/pages/patterns?)
2. Confirm constraints (existing patterns to follow, breakpoints, states?)
3. Validate intent (new creation vs. iteration on existing?)

Skip questions when the prompt is specific and unambiguous, context is fully provided, or task is a simple lookup.
