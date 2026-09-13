---
name: workshop
description: "Structured human-AI collaborative dialogue. Three modes: generate (four-move pattern for plans, designs, framings), revise (sequential one-edit-at-a-time workshopping of an existing artifact), ask (quick-scan single dialogic question). Used standalone for design conversations, methodology workshops, profile setup, conceptual debugging — and (post-integration) invoked by /printpress at Stage 1 + Stage 4 and by /critic-swarm for mid-review author input. Adversarial protection against directive-collapse and approval-seeking framing."
version: 0.0
spec: ~/Documents/GitHub/cyborg-methodologies/workshop/SPEC.md
user_invocable: true
trigger: |
  Invoke when the user runs /workshop, asks for a structured dialogic conversation about what something should be, asks to "work through" or "think through" a plan/design/decision, or asks to "workshop" or "iterate on" an existing draft/plan/protocol. /workshop generate is the four-move pattern; /workshop revise is sequential edit-by-edit; /workshop ask is a single dialogic question. Default to ask unless scale warrants structured space. NOT a chatbot — implements specific dialogic principles from cgt-skill memos that activate the constructivist sub-distribution.
---

# /workshop — Dialogic Capability Skill

Structured human-AI dialogue. Three modes (`generate`, `revise`, `ask`). Implements cgt-skill dialogic principles (memos 006, 012, 016, 022) so prompt shape carries analytical orientation — not "ask the user some questions," but specific moves that resist directive-collapse and approval-seeking.

This file is the executable workflow. Design rationale lives in `~/Documents/GitHub/cyborg-methodologies/workshop/SPEC.md`. Pre-build design notes (broader context) at `~/Documents/GitHub/cyborg-methodologies/workshop/DESIGN_NOTES.md`.

---

## Status (v0.1)

This is a v0.1 skill — designed and integrated, but pre-use. The SPEC is well-articulated; calling conventions for /printpress (Stages 1 + 4) and /critic-swarm (mid-review author input) are **live as of 2026-05-08**. Real-use data has not yet refined the parameterization, mode-shift heuristics, or WORKSHOP_LOG.md convention.

When in doubt about a v0.1 behavior, surface the uncertainty rather than performing confidence. Real-use data is what will continue to refine this skill.

---

## When to use

Any moment of structured dialogic work:

- **Generative** — figuring out what something should be. Drafting plans, design decisions, framework selection, structural organization, profile setup.
- **Revisionary** — iterating on an existing artifact. Drafts, plans, protocols, designs.
- **Quick-scan** — single specific dialogic question that needs the dialogic register (specific over open-ended, structured choices where applicable, voice memo where reflective).

---

## Invocation modes

| Form | Behavior |
|---|---|
| `/workshop` | State detection. Read working directory + recent context. Infer mode (generate / revise / ask) and topic. Confirm or offer continuation options. |
| `/workshop generate [topic]` | Generative mode. Four-move pattern. Output: plan/decision artifact in working dir. |
| `/workshop revise [artifact-path]` | Revisionary mode. Sequential one-edit-at-a-time workshopping. Pre-assess, announce, work through one level at a time. |
| `/workshop ask [question]` | Quick-scan mode. Single dialogic question. Specific over open-ended. |

**Default to `ask`** unless the question genuinely needs structured space. Don't promote a clarifying question into a full reprise.

### State detection (bare invocation)

When invoked bare, the skill reads working directory + recent conversation context to infer:

| Working directory contains | Likely mode |
|---|---|
| `WORKSHOP_LOG.md` from a prior session | Resume that workshop. Read log first, offer pickup-state. |
| Existing artifact (plan, draft, protocol) and recent /critic-swarm output | `revise` |
| No existing artifact, recent conversation about "what should this be?" | `generate` |
| Single specific question or ambiguous | `ask`, scale up only if needed |

If genuinely ambiguous, ask via `AskUserQuestion` (generate / revise / ask / something else).

---

## Required reading at invocation

These are NOT optional. Without them, dialogic moves collapse into similarity-matching, approval-seeking, or directive-following. The skill's value is precisely that prompt shape carries orientation; reading these is what gives the agent the orientation to carry.

1. **`~/Documents/GitHub/cyborg-methodologies/cgt-skill/memos/006_conversation_is_the_analysis.md`** — foundational. The dialogue IS the work; outputs are residue. If a workshop produces a plan and the agent then "implements" without further dialogue, the workshop didn't happen yet.

2. **`~/Documents/GitHub/cyborg-methodologies/cgt-skill/memos/016_openings_and_takings_up.md`** — prompt shape carries orientation. Asking "what do these share?" produces sharing-shaped output. Asking "where does this take up what that opened?" produces taking-up-shaped output. The four moves operationalize this.

3. **`~/Documents/GitHub/cyborg-methodologies/cgt-skill/memos/012_designing_for_creative_leaps.md`** — the leap is relational. Move 2 specifically: agent does NOT generate a candidate; the human's redirect IS the leap.

4. **`~/Documents/GitHub/cyborg-methodologies/INSIGHTS.md`** — entry **2026-04-29** (relational tracing vs. similarity-clustering). Without this, generative workshops produce credential-listing, alignment-announcing, feature-overlap planning. With it, they produce planning that thinks WITH the human and the audience.

5. **`~/.claude/skills/workshop/principles.md`** — skill-wide patterns confirmed through use. Read every invocation. v0.0 has two principles pre-populated (compression-is-structural; word-count-final-pass).

6. **`~/.claude/skills/workshop/feedback/[author].md`** — per-author feedback (gitignored, local-only). Read if present. Author-specific patterns that shape how the workshop runs for this person.

7. **The working directory's `CLAUDE.md`** (and parent's, if no working-dir one exists) — for finding source materials, project-specific paths, author profile pointers.

8. **For `revise` mode:** the artifact being revised + any prior conversation context (e.g., /critic-swarm synthesis, prior workshop log).

9. **Optional but high-value when relevant:**
   - cgt-skill memos 022 (constructivist sub-distribution routing), 007 (tension as data), 011 (visibility of interpretive labor)
   - The active genre config if /workshop is invoked from /printpress

---

## Adversarial sycophancy protection

Default LLM mode in dialogue is helpful encouragement. /workshop's adversarial protection isn't critique (that's /critic-swarm's job). It's resistance to two specific failure modes:

- **Directive collapse** — agent making decisions for the human. Recovery: surface the field, don't pick.
- **Approval-seeking framing** — agent asks "is this OK?" instead of opening a field. Recovery: restate the move as joint thinking, not validation.

**Constitutive instruction (read before any dialogic move):**

> Your default mode is helpful agreement. The cyborg practice requires you to resist that — not by being contrarian, but by *opening rather than concluding*, *surfacing rather than deciding*, *letting the human name what matters rather than naming it for them*. Move 2 specifically: do not generate a candidate. Ask, listen, reflect.

This sits parallel to /critic-swarm's "you are not a friendly reader" framing, but oriented toward dialogic register rather than critical register.

---

## Mode 1: `generate` (four-move pattern)

The four moves are **parameterized**. Generic shell below; the specific content of each move depends on the topic.

### Move 1: Surface candidate options. Don't pick.

Surface 2–4 candidates in the relevant dimension (framings for a draft; methodology candidates; design alternatives; framework candidates).

For each, name what it *opens* and what thread it *takes up* (per memo 016). Use relational tracing (INSIGHTS.md 2026-04-29), not similarity-clustering ("what's like what's already here"). The cyborg-distinctive move is connection-following.

**Failure mode A — approval-seeking framing:** presenting candidates as "is this OK?" rather than thinking *with* the human. Recovery: restate — "I'm not asking which is best; I'm surfacing the field so we can decide together."

### Move 2: Author names what they want. Agent does NOT generate a candidate.

Open with a question. Listen. Reflect back. The author names what's load-bearing the agent couldn't see from posting/profiles alone — a fieldwork moment, a politics they want visible, a tool whose origin matters here, a refusal of a frame.

**This move is sacred.** If the agent answers for the human, the relational structure that makes the leap possible collapses. The leap happens in the dialogue, not in either party alone (memo 012). The human's redirect IS the leap.

For reflective generation, voice memo invitation is appropriate: *"This is a voice memo question — 60–90 seconds is enough. [Specific framing question]. Paste the transcript when you're ready."*

For shorter reflective questions, plain inline question.

**Failure mode B — directive extraction without understanding-shift:** human says "draft from this" before the conversation has actually shifted the agent's understanding. Recovery: before drafting, the agent names what changed. If nothing changed, the conversation didn't happen yet.

### Move 3: Structure proposal under formal vs. conventional parameters.

Distinguish:
- **Formal parameters** — non-negotiable: word limits, posting-specified moves, structural requirements, hard constraints from the form.
- **Genre conventions** — creative space: defaults that can be intentionally broken to make things land harder.

The active context (genre config for drafting; methodology constraints for research; design parameters for design work) supplies the genre-specific formal/conventional split.

Propose a structure under this distinction. Open it for the human's response, not for approval.

### Move 4: Concrete commitments with grounding.

For each section/element/decision: what does it carry? What's the load-bearing specific (scene, number, scholar cited *doing work*, prior phrasing to mine, methodological commitment, design trade-off accepted)?

Also: what's deliberately NOT included and why?

**For drafting:** section beats with grounding (per /printpress academic_position config Stage 1 Move 4). Mine voice-final priors for prior phrasings.

**For methodology design:** methods + the methodological commitments behind each.

**For decision-making:** chosen path + trade-offs accepted.

### Output

A plan/decision artifact in the working directory. Name follows the calling context — `DRAFT_PLAN.md` for drafting, `METHODOLOGY_PLAN.md` for methodology, the profile itself for profile setup. /workshop doesn't impose a single output name.

The artifact captures:

- Arc / structure / direction settled
- What was opened (Move 1) and what was taken up (Move 2)
- Formal parameters honored vs. conventions intentionally departed from (Move 3)
- Concrete commitments + grounding (Move 4)
- What's deliberately NOT included and why
- **Conversation notes:** what shifted, which failure modes (A/B above) appeared, counterfactual on first-draft quality if we'd skipped

The artifact is **residue**, not the purpose of the workshop (memo 006). If the conversation didn't shift the agent's understanding, the workshop didn't happen — surface this rather than producing a polished but empty plan.

### When to skip Move 2 legitimately

Very short documents (cold-outreach emails, statements under 300 words) where the structure is constrained enough that the conversation collapses. Even then, name the arc in one sentence before drafting.

---

## Mode 2: `revise` (sequential workshopping)

### Pre-assess honestly

Before showing anything: pre-assess. Specific, not "this looks good." Examples:
- "Research section has strong specificity; opening is too clause-heavy."
- "Methodology stage 2 is sound; the framework selection in stage 1 needs another move."

This pre-assessment is what gives sequential workshopping its bearings.

### Announce the plan at session start

> "We'll work through this sequentially — cross-document structure first, then each document's argument arc, then sentence-level. One level at a time."

### Sequential one-edit-at-a-time

Default. Not a batch. One change, one approval, next change. Prevents overwhelm escalation.

**Address /critic-swarm convergent flags first** (if synthesis is in scope). Then specialty insights. Then mechanical flags.

### Three-component revision (per principles.md, May 2026 Duquesne)

The revision phase has three distinct components, not two:

1. **Substantive content revision** — addressing /critic-swarm convergent flags. Content layer.
2. **Williams-style line-level compression** — preserving semantic content through stylistic tightening. Voice-check's `williams_concision`. Craft layer.
3. **Weakness-and-attention flag pass** — *distinct from compression*. Identifying sentences/phrases/paragraphs that don't earn their place: weaker than surrounding prose, decorative without doing work, repeating work done elsewhere, gesturing rather than doing. Editorial judgment about what's *load-bearing*, not just *tight*.

A passage can be tightly written AND not earning its place (weakness pass flags it). A passage can be load-bearing AND poorly compressed (compression pass tightens it). Don't conflate.

### Content first, word counts later

When integrating substantive changes, lock content first. Treat word-count compression as a separate downstream phase. Compressing prose before content settles wastes effort.

### Exception to sequential

Structural revisions integrating substantive new content. Batch the integration. Preserve prior version as checkpoint. Let the human read V[N+1] as a whole. Sequential is for fine-grained edits and word-count compression, not for content integration where structure needs assessment.

### Workshop language in chat, not in file

Decide phrasing in conversation, then commit. Don't churn the file with exploratory rewrites — the file should reflect committed decisions, not in-flight thinking.

### Overwhelm detection

Increasing typo density signals overwhelm (per Job Search CLAUDE.md). Shift to:
- Shorter responses
- Targeted questions instead of more draft text
- Simpler language without reducing depth
- Explicit check-in: "Should we pause on this and come back?"

---

## Mode 3: `ask` (quick-scan)

Single specific dialogic question. Not the full four moves. The default register when scale doesn't warrant structured space.

**Specific over open-ended.** Where options exist, surface them as structured choices via `AskUserQuestion` (2–4 options, one option always available is "other"). Where reflective, voice memo invitation. Where neither, plain inline question.

When the question turns out to be load-bearing mid-flow, name the shift: *"This is becoming a deeper conversation — let me restate as a workshop generate."*

Examples of `ask`-appropriate questions:
- "Where's the source material?"
- "Did you want to include X here, or save it for Y?"
- "Which prior application is the closest match?"
- "Funder profile up to date, or build it before drafting?"

Examples of questions that should promote to `generate`:
- Anything where the answer would steer downstream work substantially
- Anything that requires reflection or generates new framing
- Anything where the human's redirect would be load-bearing

---

## Multi-session workshops

Long workshops (peer-review Stage 1 design, research methodology design) span multiple sessions. /workshop maintains state via `WORKSHOP_LOG.md` in the working directory.

**WORKSHOP_LOG.md format** (one section per session):

```markdown
# Workshop log: [topic]

## Session [N] — [date]

**Mode:** generate / revise / ask
**Duration:** [if known]

**Opened:** [what was surfaced for joint thinking]
**Taken up:** [what the human named, what shifted in agent understanding]
**Decided:** [concrete commitments]
**Deliberately NOT done:** [what was set aside, why]
**Parked:** [PARK tangents, deferred decisions]
**Failure modes observed:** [A: approval-seeking / B: directive-extraction / C: compression-as-line-trimming / D: word-count premature / etc.]
**Pickup-state for next session:** [where to start next time]
```

**At invocation in a folder containing WORKSHOP_LOG.md:** read the log, offer re-entry. *"Last session we settled X and parked Y. Pick up at Y, or revisit X first?"*

This makes /workshop's state explicit and interrogable, not implicit in chat history.

---

## Feedback-deposit mechanism

Two surfaces:

### `~/.claude/skills/workshop/principles.md` (skill-wide, read every invocation)

Patterns that emerge from use across all authors. Pre-populated v0.0 with two principles:

1. **Compression is structural, not line-level.** Real compression rebuilds architecture; line-level trimming is a different, narrower operation. When /workshop runs in compression mode, the prompt shape MUST activate architectural reading: "what's this passage doing, and what's the tightest architecture for that?" — not "is this tight?"
2. **Word count is a final-pass concern.** Stages 0–2: informational. Stage 4 content phase: structural revision before compression. Compression is its own downstream pass.

Edited via periodic learning loop (every 3rd–5th use, surfaced at invocation: *"You've used /workshop N times since the last review. Quick principle update before proceeding?"*).

### `~/.claude/skills/workshop/feedback/[author].md` (per-author, gitignored)

Author-specific patterns that don't generalize. Read at invocation if present. Same convention as voice-check profiles and /critic-swarm author profiles.

**At end of session:** offer *"anything you'd like me to remember for next time?"* — captures author-specific feedback that goes to `feedback/[author].md`. Skill-wide promotion happens through periodic review, not real-time.

---

## Integration with other skills (live)

### /printpress

- **Stage 1**: /printpress invokes `/workshop generate` with the active genre config + Stage 0 data as context. /workshop returns DRAFT_PLAN.md.
- **Stage 4**: /printpress invokes `/workshop revise` with the draft + /critic-swarm synthesis + genre config + DRAFT_PLAN.md. /workshop returns the revised draft + WORKSHOP_LOG.md entry.

### /critic-swarm

- **Step 5b** (mid-review): When a reviewer surfaces a need for author input the artifact can't resolve, /critic-swarm invokes `/workshop ask`. The answer integrates into synthesis. Used sparingly — most reviewer flags are addressable in synthesis directly.

### Standalone use cases

- Profile setup workshops
- Genre config workshops when /printpress's "other" accumulates
- **Peer-review Stage 1 design** (the hard build blocker for /printpress's peer_review genre)
- Research methodology design
- Working through complex decisions with structured dialogue
- Conceptual debugging

---

## Quick reference

| Step | Reads | Writes |
|---|---|---|
| Invocation | INSIGHTS.md, cgt-skill memos 006/012/016, principles.md, feedback/[author].md (if present), working dir CLAUDE.md | — |
| `generate` | (above) + topic/genre context | working dir plan artifact (e.g., DRAFT_PLAN.md), WORKSHOP_LOG.md entry |
| `revise` | (above) + artifact being revised + prior workshop log if present | revised artifact, WORKSHOP_LOG.md entry |
| `ask` | (above) | (chat-only typically; WORKSHOP_LOG.md entry only if part of larger workshop) |
| Per-session log | — | `[working dir]/WORKSHOP_LOG.md` |
| Skill-global (when warranted) | prior session logs | `~/.claude/skills/workshop/principles.md`, `perf_log.md`, `feedback/[author].md` |

---

## Build status (v0.1)

- **Designed:** SPEC.md, this SKILL.md, principles.md (pre-populated with two confirmed principles).
- **Integrated** (2026-05-08): /printpress Stages 1 + 4 invoke /workshop; /critic-swarm Step 5b invokes /workshop ask.
- **Pre-use:** No invocations yet (standalone or integrated). Real-use data will refine the four-move parameterization, the mode-shift heuristics, the WORKSHOP_LOG.md convention.
- **First uses to watch:** the next /printpress invocation will exercise the integration path; standalone uses (profile setup, methodology design, peer-review Stage 1 design) are also good test paths. Surface friction or unexpected behavior — that's the data the design needs.
- **Open design questions:** see SPEC § Open questions for the build session.
