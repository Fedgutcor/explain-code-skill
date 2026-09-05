---
name: explain-code
description: >
  Explains code architecture, logic, and data flow using mental models, Mermaid diagrams,
  edge-case analysis, and verification vectors. Trigger when asked: "cómo funciona esto",
  "explicame este código", "explain code", "walk me through this", "qué hace esta función",
  "why is this written this way", or when onboarding to unfamiliar logic.
user-invocable: true
license: MIT
allowed-tools:
  - Read
  - Grep
  - Glob
metadata:
  author: Ultragresion
  homepage: https://github.com/Fedgutcor/explain-code-skill
---

# Explain Code (Pedagogical Standard 2026)

When explaining any function, module, architectural pattern, or code snippet, structure the explanation following this 5-part cognitive contract. Never output generic summaries or restate obvious syntax.

A complete worked example — the five parts applied to real code, next to the generic output this skill exists to prevent — lives in [examples.md](examples.md). Read it when the shape of a section is unclear.

## 0. Read Before Explaining (Hard Precondition)

- **Never explain code you have not read.** Open the file. If the symbol comes from elsewhere, follow it (`Grep`) before describing what it does.
- If a dependency cannot be read (vendored binary, remote service, missing file), **say so explicitly** in that section and mark the claim as unverified. An unmarked guess is worse than an admitted gap.
- Every line reference (`file.ts:L12-L24`) must point at a line you actually opened. A fabricated citation destroys the value of every other citation.

## 1. Mental Anchor (The Physical Analogy)

- Ground the concept in a physical, everyday system (e.g., civil architecture, logistics routing, restaurant kitchens, electrical circuits).
- Explain **why** this pattern exists before discussing syntax.
- The analogy must break somewhere. Name where it breaks — an analogy carried too far teaches a false model.

## 2. Visual Architecture (Executable Mermaid Diagram)

- Provide a clear, valid `mermaid` diagram (flowchart, sequence, or state diagram).
- Highlight state transitions, async boundaries, and error branches.
- **The diagram must show the mechanism, not the file list.** A box per module connected by arrows is a table of contents, not a diagram. If the code has no interesting flow, skip this section and say why — a decorative diagram costs the reader attention and returns nothing.

## 3. Data Flow & Contract Lifecycle

- **Input shape:** What enters the boundary (types, invariants, validation).
- **Transformation pipeline:** Step-by-step state changes with exact line references (`file.ts:L12-L24`).
- **Output shape & Side effects:** What exits, what gets mutated, and what I/O occurs (database, network, disk).

## 4. Failure Modes & Gotchas (The Traps)

- Highlight at least one non-obvious failure mode: race conditions, silent exceptions, memory/token leaks, boundary edge cases, or N+1 queries.
- Explain the technical root cause and how to prevent it.
- **A failure mode is a scenario, not a category.** "Could have a race condition" is a label. "Two requests arriving within the TTL window both miss the cache and both hit the database" is a finding. Give concrete inputs and the wrong result they produce.

## 5. Verification Vector (Empirical Test Scenario)

- Provide a minimal test scenario (TDD style, input vs. expected output) that proves the code works or reproduces the edge case.
- The vector must target the failure mode named in section 4 — a happy-path test that would pass on broken code verifies nothing.
- Never ask the user to "trust" the explanation; give them the exact assertion to verify it.

## Tone & Constraints

- **Direct and evidence-based:** Facts, line numbers, and data shapes over subjective prose.
- **Adaptive depth:** If the concept is complex, break it into composable layers (High-Level Contract -> Mechanical Implementation).
- **Zero AI fluff:** No conversational filler ("Sure, I can explain that!"). Start immediately with the Mental Anchor.
- **Sections earn their place.** For a genuinely trivial snippet, collapse to sections 1, 3 and 5 and state that 2 and 4 were skipped for lack of substance. Padding an empty section is the same failure as a generic summary.
