# Genre config: peer_review (STUB — DO NOT RUN)

**Sources:** printpress SPEC § "What's NOT in this spec yet" (peer_review Stage 1 hard build blocker), printpress SKILL.md § Build status v1, critic-swarm peer_review personas at `~/.claude/skills/critic-swarm/personas/peer_review/` (editor-agent, source-validator, README.md), workshop DESIGN_NOTES at `~/Documents/GitHub/cyborg-methodologies/workshop/DESIGN_NOTES.md` (peer-review Stage 1 design as a workshop-not-yet-built)
**Updated:** 2026-05-07
**Status:** STUB — Stage 1 design conversation required before this genre is run.

---

## ⚠️ Hard build blocker

Per printpress SKILL.md § Build status (v1):

> "Hard build blocker: peer_review Stage 1 not yet specified. Do NOT run /printpress for peer_review without a design conversation with the author."

Per SPEC § What's NOT in this spec yet:

> "Peer-review Stage 1 — STILL A HARD BUILD BLOCKER. We designed peer_review's Stage 3 (editor agent + source validator + reviewers) but NOT Stage 1 (the cyborg conversation for a research article). The Stage 1 conversation for peer_review is structurally different from an application (no posting, no fit eval, different framing for the question-they-haven't-asked move, source material varies)."

**Agents: do not invoke `/printpress` for peer_review until the design conversation has happened and this stub is replaced with a full config.** If the author asks for peer_review work before then, surface the build blocker and offer one of these instead:
- `/critic-swarm` directly on a draft (review-only, no drafting pipeline) — peer_review personas exist (editor-agent, source-validator, scholar-anchored reviewers per README) and that path is unblocked
- A scoped Stage 1 design conversation with the author — the conversation that this config needs as a prerequisite

---

## What peer_review is (when it exists)

Drafting research articles, book chapters, and manuscripts for academic publication. Reviewer = journal editor + 2–3 scholar-peers + (in some cases) a source-validator. Voice-check tag = `peer_review` (new — voice-check adds when first profile is built).

Genre boundary:
- Application materials → other genres
- Public-facing writing (op-eds, public scholarship) → `other`
- Book proposals → likely `peer_review` subgenre OR `grant_fellowship` depending on press review culture; decided in design conversation

---

## Stages 0, 2, 3, 4, 5 — sketches (for design context)

These are sketches to inform the Stage 1 design conversation, not executable workflow.

### Stage 0 — Data-in (sketched)

Source material is the artifact's hard problem. Per SPEC § Stage 0:

> "Ask the author: where is the source material? (fieldnotes, data, prior drafts, source PDFs — these aren't retrievable without their input.) Also: target venue guidelines, special issue call or CFP if applicable. Save venue guidelines verbatim."

Likely required:
- The article / chapter / manuscript draft (or notes if pre-draft)
- Source materials registry — fieldnotes, data files, PDFs of cited works, prior drafts
- Target venue + venue guidelines (saved verbatim)
- Bibliography (separate from prose if possible — feeds editor-agent panel selection)
- Any prior peer review feedback if this is a revision

### Stage 2 — Drafting (sketched)

Voice-check active throughout. `--genre peer_review` once the tag exists.

The drafting register is **scholarly-density-expected** (more so than humanist_fellowship — peer reviewers grade for methodological depth and engagement with the field's conversations). Williams's *Style* applies but the registers conventions of academic prose dominate.

### Stage 3 — Reviewer swarm (designed; this part is unblocked)

**Stack name:** `peer_review` (per `~/.claude/skills/critic-swarm/personas/peer_review/`).

Per /critic-swarm peer_review README:
1. **Editor agent runs first** (`editor-agent.md`) — proposes 3–4 specific scholars as reviewers, drawn from the article's bibliography, recent journal contributors, and scholars in direct conversation with the article's subject. Output: panel proposal with rationale.
2. **Author confirms or overrides** — they may know reasons (conflict, prior bad-faith reads, professional history) the editor cannot see. Their final list is what gets instantiated.
3. **Source validator runs in parallel** (`source-validator.md`) — does not depend on panel composition; checks claim-evidence fit.
4. **Always-runs reviewers run in parallel** — intelligibility, jargon, author-informed.
5. **Each confirmed subject-area reviewer instantiated** using the prompt template in the README, anchored to the specific scholar's work, methodological orientation, and recent publications.

Stage 3 is the most-built component of peer_review. The Stage 1 design conversation needs to ensure Stage 0 → Stage 1 → Stage 2 produce a draft that Stage 3 can meaningfully review.

### Stage 4 — Revision (sketched)

Sequential workshopping. Address editor agent's overall recommendation first; convergent flags from scholar-anchored reviewers second; source-validator findings third (often mechanical-but-substantive — claim-evidence gaps); always-runs flags last.

Voice-check active throughout revision.

### Stage 5 — Save (sketched)

- Save `*_final.md` of the manuscript
- Append VERSION_LOG.md row
- Calendar reminders for **revision deadlines** (journals typically give 30/60/90 days for revisions; major-revision timeline matters)
- Archive to a journal-submission archive (location decided per author's working-dir CLAUDE.md — for June, this is likely under research/ or recognition_sentience/, not Job Search/Materials Archive/)
- Voice-check learn pass with `--genre peer_review` once the tag exists

---

## Open design questions for Stage 1

These are the questions the Stage 1 design conversation needs to answer. Drawn from /critic-swarm peer_review README, printpress SPEC § What's NOT in this spec yet, and the workshop DESIGN_NOTES.md mention of "peer-review Stage 1 design — IS a workshop we haven't designed yet."

1. **Story development pre-draft.** Articles often start from a research insight, a fieldwork moment, or a theoretical puzzle that hasn't yet found its argument. The Stage 1 conversation needs to surface what the article is *about* in a way that's structurally different from "what does this position invite?" An application has a posting; an article has only the source material and the author's developing sense of the contribution. How does the four-move pattern adapt?

2. **No posting / no fit eval / different framing for the question-they-haven't-asked move.** What replaces these scaffolding moves? Per SPEC: "no posting, no fit eval, different framing for the question-they-haven't-asked move." Candidates:
   - "What's the contribution?" replaces fit eval (Move 0 analog).
   - "What's the audience this article enters?" replaces audience-derived swarm composition.
   - The question-they-haven't-asked move still applies — what framework does the field treat as given that this article reveals as the problem? — but the framing is article-internal, not application-external.

3. **Source material is variable.** Different articles draw on different combinations of fieldnotes, archival material, theoretical sources, prior drafts, data files, interview transcripts, ethnographic detail. Stage 0 source-loading varies more than for applications. Does Stage 1 begin with a source-material conversation before any framing surfacing?

4. **Argument arc vs. application arc.** Article arc has its own conventions (introduction sets up the problem and contribution; body builds argument with empirical/theoretical scaffolding; conclusion opens to broader stakes). The four-move pattern (opens / takes-up / arc-proposal / beats) maps differently to these conventions than to application arcs.

5. **Voice memo register.** Per SPEC § Dialogic information-gathering, peer_review Stage 1 is one of the explicit "deep dialogic" cases. Voice memo invitations are appropriate — but for what specifically? Story development? Contribution articulation? Field positioning? The Stage 1 design needs to identify the genuinely-generative voice memo questions.

6. **Revision-mode entry.** Many peer_review invocations will be revision-mode (post-editor-decision, addressing reviewer feedback). Stage 1 looks different when the article exists and the question is "how do we address these reviews?" vs. when the article is pre-draft. Both need design.

7. **Editor agent integration.** The editor agent in /critic-swarm is currently designed for Stage 3 (selecting reviewers from bibliography). Could it also play a role at Stage 1 — surfacing the article's contribution from the bibliography it's already in conversation with? The design conversation should consider whether Stage 1 and Stage 3 share a component.

8. **Subgenre handling.** "Article" vs. "book chapter" vs. "manuscript review" vs. "book proposal" may be sub-genres of peer_review with meaningfully different Stage 1 conventions. The design needs to decide whether to handle as one genre with subgenre tags (like academic_position's R1/SLAC/HSI variation) or split.

---

## When to do the Stage 1 design

Per workshop DESIGN_NOTES.md, peer_review Stage 1 design is one of the workshops the `/workshop` skill (deferred build) is intended to own — a generative four-move conversation about what peer_review's Stage 1 should be. When `/workshop` is built, this design becomes one of its first invocations.

Until then: the design happens in a focused session with the author. June has flagged this as post-FFS work (per printpress SPEC § Build order).

When the design is done, replace this stub with a full config matching the structure of `academic_position.md` and `grant_fellowship.md`.
