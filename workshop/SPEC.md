# /workshop — Dialogic Capability Skill Spec

**Design date:** 2026-05-07; integration completed 2026-05-08.
**Status:** SKILL.md v0.1 — designed and integrated with /printpress (Stages 1 + 4) and /critic-swarm (Step 5b). Pre-use; real-use data has not yet refined the parameterization or heuristics. DESIGN_NOTES.md's "wait 5–10 uses" guidance was about *what to refine*, not whether to wire up the calls — integration is just an architectural step and is now in place.

---

## What this is

A skill for **structured human-AI collaborative dialogue.** It owns two related modes:

1. **Generative mode** — figuring out what something should be. Four-move conversations adapted from cgt-skill memos. Used for: drafting plans, design decisions, profile setup, methodology design, conceptual debugging.

2. **Revisionary mode** — sequential one-edit-at-a-time workshopping of an existing artifact. Pre-assess, announce the pass plan, work through one level at a time, watch for overwhelm.

Plus a third lightweight register:

3. **Quick-scan mode (`ask`)** — single specific dialogic question. Not the full four moves. The mode the skill should default into when scale doesn't warrant structured space.

This skill cannibalizes the dialogic content currently embedded in `/printpress` SPEC § Dialogic information-gathering and § Stage 1 four moves. When /workshop ships and integrates, /printpress invokes `/workshop generate` at Stage 1 and `/workshop revise` at Stage 4 instead of containing the dialogic logic itself. /critic-swarm invokes `/workshop ask` for mid-review author input.

The full design rationale is at `DESIGN_NOTES.md` (this directory). This SPEC consolidates the design decisions.

---

## Why this is its own skill

Same architectural reasoning that landed `/critic-swarm`:

1. **Architectural cleanliness.** /printpress becomes truly thin (orchestrator). /workshop has its own evolution path, learning loop on dialogic patterns, register protections.
2. **Discoverability.** Once it has its own door, more uses surface — peer-review Stage 1 design, profile setup, genre config workshops, research methodology design.
3. **The cgt-skill memos already articulate this as a distinct cyborg-methodology** — memos 006, 012, 016 are general dialogic principles, not drafting-specific.
4. **Reusability beyond drafting.** Working through ideas, planning research, designing infrastructure, processing fieldnotes, conceptual debugging — all benefit from structured dialogue.

---

## Modes

### `generate` — generative mode (four-move pattern)

**Use for:** any moment where the question is "what should this be?" Plans, decisions, designs, structures, framings.

The four moves are **parameterized** — the generic shell is the same; the invocation supplies what each move opens.

| Move | Generic shell | Drafting invocation (current /printpress Stage 1) | Other invocations |
|---|---|---|---|
| 1 | Surface candidate options. Don't pick. | 2–4 candidate framings for the position | Methodology candidates; design alternatives; framework candidates |
| 2 | Author names what they want. Agent does NOT generate a candidate. | Author names the story — fieldwork scene, politics, tool origin | Author names what the artifact should accomplish; what the methodology must protect against; what the design must enable |
| 3 | Arc proposal under formal vs. conventional parameters. | Arc proposal under genre conventions (academic CL, grant CFP, etc.) | Structure proposal under formal constraints + conventions of the form |
| 4 | Concrete commitments with grounding. | Section beats with load-bearing specifics | Methods + methodological commitments; design choices + trade-offs accepted; section beats + grounding |

**Output:** a plan/decision artifact in the working directory. Drafting → `DRAFT_PLAN.md`. Methodology → `METHODOLOGY_PLAN.md`. Profile setup → the profile itself. The artifact name follows the calling context; /workshop doesn't impose a single output name.

The artifact is **residue** of the conversation, not its purpose (memo 006). If the conversation produces a plan the agent then implements without further dialogue, the workshop didn't do its job.

### `revise` — revisionary mode (sequential workshopping)

**Use for:** working through an existing artifact's revision pass. Refining drafts, addressing /critic-swarm synthesis flags, iterating plans.

**Default protocol** (instantiates /printpress Stage 4 + Step 5.5 logic in skill form):

1. **Pre-assess honestly before showing.** Not "this looks good." Specific: "research section has strong specificity; opening is too clause-heavy."
2. **Announce the plan at session start.** "We'll work through this sequentially — cross-document structure first, then each document's argument arc, then sentence-level. One level at a time."
3. **Sequential one-edit-at-a-time** is the default. Not a batch. One change, one approval, next change.
4. **Three-component revision** (per `principles.md`, drawn from May 2026 Duquesne session):
   - (a) substantive content revision (addressing /critic-swarm convergent flags)
   - (b) Williams-style line-level compression (preserving content; voice-check's `williams_concision`)
   - (c) weakness-and-attention flag pass (distinct from compression; what's not earning its place)
5. **Content first, word counts later.** When integrating substantive changes, lock content first. Compression is its own pass after.
6. **Exception to sequential**: structural revisions integrating substantive new content. Batch the integration; preserve prior version as checkpoint; let the human read V[N+1] as a whole.
7. **Workshop language in chat, not file.** Decide phrasing in conversation, then commit; don't churn the file with exploratory rewrites.
8. **Overwhelm detection.** Increasing typo density → shorter responses, targeted questions, simpler language without reducing depth, explicit check-in.

### `ask` — quick-scan mode

**Use for:** single specific dialogic question. The default register when scale doesn't warrant structured space.

Examples: "Where's the source material?" "Did you want to include X here, or save it for Y?" "Which prior application is the closest match?"

Not just "ask a quick question" — the dialogic principles still apply. **Specific over open-ended.** Where options exist, surface them as structured choices via `AskUserQuestion`. Where reflective, voice memo invitation. Where neither, plain inline question.

When the question turns out to be load-bearing mid-flow, the skill names the shift: "This is becoming a deeper conversation — let me restate as a workshop ask."

### Mode selection heuristic

- **`ask`** is the default when scale is small. Single piece of info, response is choice or short value, no reflection or generation needed.
- **`generate`** is right when the question requires structured space — multiple possible directions, the human's redirect IS the leap, output will steer downstream work.
- **`revise`** is right when the artifact already exists and the task is iterating on it.

Default to `ask` unless the question genuinely needs structured space. Don't promote a clarifying question into a full reprise; don't reduce a paper's story-development to a one-line ask.

---

## Source materials (the dialogic core)

These are required reading at /workshop invocation. Without them, dialogic moves collapse into similarity-matching, approval-seeking, or directive-following.

### From cgt-skill memos (`~/Documents/GitHub/cyborg-methodologies/cgt-skill/memos/`)

In order of centrality:

- **memo 006 — "Conversation IS the analysis."** The dialogue is where structure gets constructed. Outputs are residue, not purpose. Foundational.
- **memo 016 — "Openings and takings-up."** Prompt shape carries analytical orientation. Asking "what do these share?" produces sharing-shaped output. Asking "where does this take up what that opened?" produces taking-up-shaped output.
- **memo 012 — "Designing for creative leaps."** The leap is relational, not unilateral. The agent's surface gives the human something to articulate against. Move 2 specifically: agent does NOT generate a candidate; the human's redirect IS the leap.
- **memo 022 — "Routing through constructivist sub-distributions."** Every prompt template carries register weight. The system prompt for the workshop establishes the register from the start.
- **memo 007 — "Tension as data."** When agent reading diverges from human's, divergence is itself a finding. Don't smooth, vote, or pick a winner.
- **memo 011 — "Visibility of interpretive labor."** Every move leaves an interrogable trace. Mining the trace is what learning loops feed on.

### From INSIGHTS.md (`~/Documents/GitHub/cyborg-methodologies/INSIGHTS.md`)

- **2026-04-29 — "Pattern-matching as relational tracing, not similarity-clustering."** The cyborg-distinctive analytical move. Without this frame, generative workshops produce credential-listing, alignment-announcing, feature-overlap planning. With it, planning thinks WITH the human and the audience.

### From PIPELINE.md (the operational embodiment in the drafting context)

- Step 3.7 (intellectual landscape research) — the two organizing questions: what does the work *open up*? what threads does it *pick up*? Openings/takings-up applied at the relational-field level.
- Step 3.8 (pre-draft cyborg conversation) — the four moves, the Move 2 guard, the two failure modes (approval-seeking, directive-extraction).
- Step 5.5 (presenting the draft and revision process) — pre-assess, announce, sequential, content-first.

### From printpress SPEC + UX_STUB

- printpress SPEC § Dialogic information-gathering — the three principles, the quick-scan vs. deep dialogic distinction.
- printpress UX_STUB.md — interaction patterns. The two question modes (structured choices vs. voice memo). PARK tangents. One thing at a time. Specific over open-ended. Overwhelm detection.

When /workshop ships, the dialogic content moves OUT of /printpress SPEC and UX_STUB and into /workshop SPEC + SKILL.md. /printpress retains thin reference to /workshop for the calling convention.

---

## Adversarial sycophancy protection

Default LLM mode in dialogue is helpful encouragement. /workshop's adversarial protection isn't critique (that's /critic-swarm's job) — it's resistance to two specific failure modes:

1. **Directive collapse** — the agent making decisions for the human. Recovery: surface the field, don't pick.
2. **Approval-seeking framing** — the agent asks "is this OK?" instead of opening a field. Recovery: restate the move as joint thinking, not validation.

**Constitutive instruction at invocation:**

> Your default mode is helpful agreement. The cyborg practice requires you to resist that — not by being contrarian, but by *opening rather than concluding*, *surfacing rather than deciding*, *letting the human name what matters rather than naming it for them*. Move 2 specifically: do not generate a candidate. Ask, listen, reflect.

This is parallel to /critic-swarm's "you are not a friendly reader" framing, but oriented toward the dialogic register rather than critical register.

---

## Register protection (system-prompt-level)

Per memo 022, every prompt the skill issues carries register weight. The workshop's system prompt MUST anchor constructivist register from the start. Specifically:

- Frame moves in **opening/taking-up** language, not in **input/output** language.
- Frame the human's role as **co-thinker**, not **decider** (decisions emerge from the dialogue, not from the human picking from a menu).
- Frame the agent's surface as **material to articulate against**, not **options to approve**.
- Frame divergence (memo 007) as **data**, not **failure**.
- Frame revision as **what the passage is doing**, not **whether it's tight enough**.

When dispatched into a sub-skill context (e.g., /printpress invokes /workshop), the calling skill passes its own context but does NOT override the register prompt. The register prompt is /workshop's load-bearing protection against sub-distribution drift.

---

## Where the skill finds local files

Same protocol as /printpress and /critic-swarm:

1. Working directory `CLAUDE.md`
2. Parent directory `CLAUDE.md`
3. Skill profile (`~/.claude/skills/workshop/feedback/[author].md`, if present)
4. Ask the author (quick-scan dialogic)

Do NOT maintain a parallel user-paths config in the skill.

---

## Feedback-deposit mechanism

Two surfaces (parallel to /printpress's principles.md + voice-check's profile):

### `~/.claude/skills/workshop/principles.md` (skill-wide)

Patterns that emerge from use across all authors. Read at every invocation. Edited via periodic learning loop. Pre-populated at v0.0 with two principles already articulated through use:

1. **Compression is structural, not line-level.** Real compression rebuilds architecture; line-level trimming is a different, narrower operation. Source: `feedback_compression_structural_not_line_level.md`. When /workshop runs in compression mode, the prompt shape MUST activate architectural reading: "what's this passage doing, and what's the tightest architecture for that?" — not "is this tight?"
2. **Word count is a final-pass concern.** Stages 0–2: informational. Stage 3 review: not a primary critique dimension. Stage 4 content phase: structural revision before compression. Stage 4 compression phase: word count primary. Stage 4.5 QC: verification check. Source: `feedback_word_count_final_pass_only.md`. Exception: when human explicitly asks for compression mid-process, do it.

### `~/.claude/skills/workshop/feedback/[author].md` (per-author, gitignored)

For author-specific patterns that don't generalize. Same convention as voice-check profiles and /critic-swarm author profiles.

**At invocation:** read `principles.md` (skill-wide) + `feedback/[author].md` (if present). Both shape how the workshop operates.

**At end of session:** offer "anything you'd like me to remember for next time?" — captures author-specific feedback that goes to `feedback/[author].md`. Skill-wide principle promotion happens through periodic review, not real-time.

This makes the feedback-deposit mechanism explicit. Author feedback like "agents need to be less rigid about word counts" wouldn't need to be re-stated; /workshop would already know.

---

## Multi-session workshops

Long workshops (peer-review Stage 1 design, research methodology design) span multiple sessions. The conversation-as-the-analysis principle implies workshop state needs to persist.

**Convention:** `WORKSHOP_LOG.md` per workshop, in the working directory containing the artifact. Captures:

- Session date + duration
- What was opened, what was taken up, what was decided, what was deliberately NOT done
- Failure modes observed (approval-seeking, directive-extraction, compression-as-line-trimming, etc.)
- What shifted (the agent's understanding before vs. after)
- What's parked (PARK tangents, deferred decisions)
- Pickup-state for next session

**At invocation in an existing workshop folder:** /workshop reads WORKSHOP_LOG.md and offers re-entry. "Last session we settled X and parked Y. Pick up at Y, or revisit X first?"

This makes /workshop's state explicit and interrogable, not implicit in chat history.

---

## Integration with other skills

### /printpress

- **Stage 1** (pre-draft cyborg conversation): /printpress invokes `/workshop generate` with the active genre config + Stage 0 data as context. /workshop returns DRAFT_PLAN.md.
- **Stage 4** (revision): /printpress invokes `/workshop revise` with the draft + /critic-swarm synthesis. /workshop returns the revised draft + workshop notes.

### /critic-swarm

- When a critic surfaces "more author input needed" mid-review, /critic-swarm invokes `/workshop ask` for a small dialogic ask. After the ask resolves, /critic-swarm resumes synthesis.

### Standalone use cases

- **Profile setup workshops** (currently inside /printpress UX_STUB.md profile setup section)
- **Genre config workshops** when "other" accumulates (currently inside /printpress SPEC § Learning loops)
- **Peer-review Stage 1 design** (the hard build blocker for /printpress's peer_review genre — IS a workshop we haven't designed yet)
- **Research methodology design**
- **Working through complex decisions** with structured dialogue
- **Conceptual debugging** — when a problem isn't yielding, sometimes the dialogic frame surfaces the actual question

### Integration status (live as of 2026-05-08)

/printpress and /critic-swarm now delegate dialogic work to /workshop. /printpress SKILL.md Stage 1 and Stage 4 invoke `/workshop generate` and `/workshop revise` respectively, passing genre config + Stage 0 data as context. /critic-swarm SKILL.md Step 5b invokes `/workshop ask` for mid-review author input.

The integration is mechanically complete; what's NOT done is real-use validation. Refinement to the four-move parameterization, mode-shift heuristics, and WORKSHOP_LOG.md convention will come from observing real invocations.

---

## Learning loops

### Per-session

Logged to `[working dir]/WORKSHOP_LOG.md`:

- Failure modes observed (A: approval-seeking; B: directive-extraction; C: compression-as-line-trimming; D: word-count premature enforcement; etc.)
- What shifted (agent's understanding before vs. after)
- Counterfactual: what would have happened if we'd skipped this workshop? Worth running, or formality?

### Skill-global

- `~/.claude/skills/workshop/principles.md` — patterns confirmed across authors and use-cases. Periodic review (every 3rd–5th use, surfaced at invocation: "You've used /workshop N times since the last review. Quick principle update before proceeding?").
- `~/.claude/skills/workshop/perf_log.md` — which dialogic moves produce sharp work vs. shallow ratification. Pattern recognition input for periodic review.
- `~/.claude/skills/workshop/feedback/[author].md` — per-author feedback that doesn't generalize.

---

## What's NOT in this spec yet (build gaps)

These are open design questions where v0.0 makes a defensible choice but real-use data should drive refinement.

1. **Voice memo invitation mechanics** — v0.0: skill prompts and waits; user runs `mlx_whisper` separately; user pastes transcript when ready. Per Job Search CLAUDE.md, that's the established workflow. Future: tighter integration if there's a way to invoke transcription from within the skill.

2. **Quick-scan threshold** — v0.0 heuristic: quick-scan when single piece of info needed and response is choice or short value; promote to `generate` when reflection or generation is required and the human's redirect is load-bearing. May need refinement after observing where v0.0 misroutes.

3. **Move 4 parameterization for non-drafting genres** — v0.0: "concrete commitments with grounding." For research methodology, that's methods + methodological commitments. For decision-making, that's chosen path + trade-offs accepted. Worth testing on a real non-drafting workshop before committing.

4. **Relationship to /c2c skill** — v0.0: no shared infrastructure. Both implement cgt-skill principles; both resist consensus collapse. Different in that c2c is Claude-to-Claude and /workshop is human-AI. Revisit at periodic review whether shared logging/state conventions help.

5. **Multi-author profile handling** — v0.0: single profile per author at `feedback/[author].md`. If a workshop spans multiple humans (collaborative writing, joint methodology design), profile selection logic is unspecified. Defer until the use case appears.

6. **Mode-shift signaling** — v0.0: when an `ask` becomes a `generate` mid-flow, the skill names the shift inline. Whether this should be a structured transition (with a synthesis of what's been settled before promoting) or a soft transition (with continuity preserved) is untested.

7. **Integration sequencing with /printpress and /critic-swarm** — DONE 2026-05-08. /printpress Stages 1 + 4 invoke /workshop; /critic-swarm Step 5b invokes /workshop ask. Open question now: do the calling conventions match real call patterns, or will real use surface awkwardness in the handoff?

---

## Build status (v0.1)

- **Designed:** This SPEC.md, drawn from `DESIGN_NOTES.md` and existing /printpress + /critic-swarm v1.
- **Built:** SKILL.md, `principles.md` (two pre-populated principles: compression-is-structural; word-count-final-pass), `feedback/` dir for per-author overrides.
- **Integrated** (2026-05-08): /printpress Stages 1 + 4 delegate to /workshop generate / revise; /critic-swarm Step 5b delegates to /workshop ask.
- **Not yet:** First standalone use; first integrated use via /printpress; first non-drafting workshop (peer-review Stage 1 design is a candidate); first author-feedback profile populated.
- **Next:** Real use will surface refinements. Recommended first paths: (a) the next /printpress invocation will exercise the integrated path; (b) a standalone workshop on peer-review Stage 1 design (which /printpress can't run yet — explicit blocker in genre_configs/peer_review.md); (c) author-profile bootstrap as a /workshop generate (or as part of /critic-swarm's profile setup, see CRITIC_SWARM_TEST_PLAN.md).

---

## Open questions for the build session

These are the questions /workshop will need to answer once it has real-use data. Recording them here so the build session starts from a clear list.

1. Are the four-move shells generic enough to parameterize across drafting / methodology / decision-making / profile-setup? Or do non-drafting workshops need their own move shells?
2. Does the WORKSHOP_LOG.md convention work, or is per-session state better stored elsewhere (chat history, /printpress's DRAFT_PLAN.md)?
3. Does the register-protection system prompt actually anchor constructivist sub-distribution, or does it drift mid-conversation under sub-skill calling conventions?
4. Does the mode-shift signaling (`ask` → `generate` mid-flow) feel natural or jarring?
5. Does the principles.md + feedback/[author].md split reduce friction, or add overhead?
6. When /printpress and /critic-swarm integrate, do the calling conventions match real call patterns, or is the integration awkward?
