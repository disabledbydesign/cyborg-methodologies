# /printpress — Skill-Wide Principles

<!--
This file implements SPEC.md § Cross-genre generalization (C + D combined).
It holds learnings that have been confirmed across multiple applications and multiple genres — patterns that turned out to be generalizable, not genre-specific.

The skill reads this file at Stage 0 on invocation (alongside the matched genre config). Principles here apply across all genres.

Promotion path:
1. At Stage 3 / log-write, the agent tags learnings in a project's LEARNING_LOG.md as `genre-specific` or `potentially-generalizable`.
2. /critic-swarm's synthesis output flags in-context patterns that might apply across genres.
3. The periodic genre-config review (every 3rd–5th use of a genre) reads tagged-generalizable learnings from across genres and surfaces candidates to the author for confirmation.
4. Confirmed candidates get written here, with provenance (which stacks they were observed in, when promoted).
5. Tags that turn out to be genre-specific stay in their genre config; truly generalizable ones get promoted.

The system self-corrects: the agent doesn't need to be right at tag-time, the periodic review validates and promotes.

Initial state: empty. As the skill is used and patterns get confirmed, entries accumulate here.
-->

---

## How entries get written here

After a periodic genre review surfaces a candidate principle and the author confirms it:

- Add an entry under "Confirmed principles" with: pattern name, plain-language statement of the pattern, stacks observed in (genres + specific applications), the date of promotion.
- If the principle replaces or refines a check that lives in a genre config or in voice-check, note the supersession explicitly.
- If the principle is operationalized in a tool (a voice-check qualitative check, a Stage 4.5 verification item, a persona-stack default), link to where it lives.

Entries should be specific enough that an agent reading this cold could recognize the pattern in a draft. "Be specific" is not a principle. "When the author provides extensive context, treat it as input for judgment about what's load-bearing for THIS draft, not as a checklist to include" is.

---

## Confirmed principles

<!--
Initial state: none. Entries get added as the periodic review confirms them.
Format per entry:

### [Pattern name]

**Statement:** [the principle, in plain language, specific enough to recognize]

**Stacks observed in:** [genre]:[application name], [genre]:[application name], ...

**Promoted to skill-wide on:** [YYYY-MM-DD]

**Operationalized as:** [where the principle lives if it's encoded somewhere — voice-check check ID, genre config field, Stage 4.5 verification item, persona-stack default. Or "applies as cross-cutting principle, not encoded in tooling."]

**Notes:** [anything else — e.g., subtleties, exceptions, related principles]

---
-->

### References handling — out of scope for agents

**Statement:** When drafting any application materials, do not surface references as something to confirm, strategize about, or flag in checklists. References are the author's domain — they have the rolodex and judgment for which referees fit which application. Bringing references concern up creates friction without value.

**Stacks observed in:** `academic_position` across multiple applications (recurring correction); applies to `grant_fellowship` and `non_academic_application` by extension.

**Promoted to skill-wide on:** 2026-05-07

**Operationalized as:** cross-cutting principle. Read at Stage 0 invocation alongside the genre config. Applies to checklist generation, DRAFT_PLAN.md fields, and any "open questions" the skill might surface.

**Notes:**
- If a posting requires reference contact info as part of the materials list, note that the materials list includes it — but don't add reference selection to the agent's scope.
- If the author surfaces a reference question themselves, engage normally; otherwise leave it alone.
- Source: `feedback_references_handling.md` in author memory (Duquesne Grefenstette session, 2026-05-07).

---

---

## Candidate principles (under observation)

<!--
Patterns that have been tagged `potentially-generalizable` in one or more LEARNING_LOG.md files but haven't been confirmed across enough stacks yet. Listed here as a watch-list for the next periodic review.

Each candidate: pattern name, where first observed, why it might be generalizable.
This section is the input to the next periodic review — it's where tagged-generalizable learnings sit between project-local logging and skill-wide promotion.
-->

*(None yet.)*

---

## Demoted candidates

<!--
Patterns that were tagged `potentially-generalizable` but, on review, turned out to be genre-specific or context-specific. Logged here so the same pattern doesn't keep getting re-promoted from a different stack.
The demotion record is part of the system's self-correction.
-->

*(None yet.)*
