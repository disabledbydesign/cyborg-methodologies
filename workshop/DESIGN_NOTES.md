# /workshop — Design Notes (pre-build)

**Status:** Design notes for future skill, not built yet. Captures the design language we'll need when we build it. Source synthesis: PIPELINE.md, INSIGHTS.md, cgt-skill memos, printpress SPEC, UX_STUB.md.

**Created:** 2026-05-07, immediately after /printpress + /critic-swarm v1 build, while the design language was fresh.

**Why pre-build notes:** the dialogic capability is currently embedded inside /printpress. Splitting it out is the right architectural move (parallel to /critic-swarm extraction) but should wait until v1 has been used enough to know what /workshop actually needs to contain. These notes capture the breadth of source material so future-us doesn't re-search.

---

## What /workshop is

A skill for **structured human-AI collaborative dialogue.** It owns two related modes:

1. **Generative mode** — figuring out what something should be. Four-move conversations (openings/takings-up), info-gathering, designing, structural organization. Used at: /printpress Stage 1 (pre-draft cyborg conversation), profile setup, genre config workshops, peer-review Stage 1 design, research methodology design, working through any decision or structural problem together.

2. **Revisionary mode** — sequential one-edit-at-a-time workshopping of an existing artifact. Used at: /printpress Stage 4 (revision), iterative refinement of plans/drafts/protocols, working through critic-swarm synthesis flag-by-flag.

The skill is *not* a chatbot. It implements specific dialogic principles from cgt-skill that activate the constructivist sub-distribution — every dialogic move carries analytical orientation through prompt shape.

---

## Why this is its own skill

Same architectural reasoning that landed /critic-swarm:

1. **Architectural cleanliness.** /printpress becomes truly thin (orchestrator). /workshop has its own evolution path, its own learning loop on dialogic patterns, its own register protections.
2. **Discoverability.** Once it has its own door, more uses surface — peer-review Stage 1 is a workshop we haven't designed; profile setup is a workshop; genre config promotion is a workshop. Naming the capability lets it be invoked directly.
3. **The cgt-skill memos already articulate this as a distinct cyborg-methodology** — not drafting-specific. Memo 006 ("conversation IS the analysis"), memo 012 ("designing for creative leaps"), memo 016 ("openings and takings-up") are general dialogic principles.
4. **Reusability beyond drafting.** Working through ideas, planning research, designing infrastructure, processing fieldnotes, conceptual debugging — all benefit from structured dialogue.
5. **Cyborg-methodologies as a public library.** /workshop is more shareable as a standalone methodology than as part of a drafting pipeline.

---

## Source materials (the full breadth)

### From cgt-skill memos (the dialogic methodology core)

The following memos at `~/Documents/GitHub/cyborg-methodologies/cgt-skill/memos/` should be required reading at /workshop invocation. Listed in order of centrality:

- **memo 006 — "Conversation IS the analysis."** The dialogue isn't preparation that feeds outputs; the dialogue is where theory/structure gets constructed. Codes, memos, categories materialize *during* the dialogue; outputs are residue, not the purpose. This is the foundational principle. *In /workshop terms:* if a workshop produces a plan that the agent then "implements" without further dialogue, the workshop didn't do its job. The plan is residue of work that happened in conversation.
- **memo 016 — "Openings and takings-up."** The dialogic structure that resists similarity-flattening at the relational level. For each move: what does it *open*, leave unfinished, gesture toward? For any pair: where does the second pick up what the first opened? Where does it answer, reframe, deflect, extend? *Critical:* the prompt shape carries analytical orientation. Asking "what do these share?" produces sharing-shaped output. Asking "where does this take up what that opened?" produces taking-up-shaped output. Task framing is a primary gravity-management move.
- **memo 012 — "Designing for creative leaps."** The cyborg practice depends on moves the AI's gravity tends against — introduction of new context, abductive redirection, "what if we read this another way." But these moves don't happen in the human alone; they happen *in the dialogue* — the AI's surface gives the researcher something to articulate against, push off from, see differently. The leap is relational, not unilateral. *In /workshop terms:* the agent's surface (candidate framings, arc proposals, beat lists) is not "options to approve" — it's material the human articulates against. Move 2 of the four-move structure protects this: the agent does NOT generate a candidate story; the human's redirect IS the leap.
- **memo 022 — "Routing through constructivist sub-distributions."** Every prompt template carries register weight. Lexical priming, citation as priming, methodological context, negative priming, lens invocation — these activate the constructivist sub-distribution rather than the AI's default positivist/command-tool register. *In /workshop terms:* every dialogic prompt the skill issues carries register weight. Workshop prompts written in constructivist/cyborg register condition the working sub-distribution; prompts written in command-tool register don't get the dialogic work done. The system prompt for the workshop establishes the register from the start.
- **memo 007 — "Tension as data."** When the AI's reading diverges from the human's, when readings conflict, when new context unsettles a stable framing — the divergence is itself a finding. The tool surfaces it and holds it open; doesn't smooth, vote, or pick a winner. *In /workshop terms:* when the agent's framing differs from what the human says they want, that tension is data — preserve it, don't collapse to consensus. This is also the praxis vs. bliss attractor distinction (relevant to c2c skill).
- **memo 011 — "Visibility of interpretive labor."** Every move leaves a trace the human can interrogate. The trace is generative — it's what learning loops feed on. Mining the trace lets us see what shaped a decision, where divergence got resolved, when a lens got invoked. *In /workshop terms:* the workshop conversation produces an audit trail — DRAFT_PLAN.md "Conversation notes" section, the failure-mode log entries (A or B per /printpress SPEC), the workshop's own learning loop. The trace makes the dialogic work visible and refinable.

### From PIPELINE.md (operational embodiment of these principles)

PIPELINE.md is the most worked-out instantiation of /workshop's generative mode (in the drafting context). At `/Users/june/Documents/Filing/Job Search/PIPELINE.md`:

- **Analytical Mode block (top of PIPELINE).** Required reading: INSIGHTS.md 2026-04-29 entry on relational tracing. Without this, the four-move conversation collapses to similarity-matching ("does this match the posting?"). With it, the conversation activates relational tracing ("what does the work open up for this reader?").
- **Step 3.5 — "Drafting method."** Voice-guided single pass + sequential workshopping. Names the judgment gap explicitly: "The judgment gap (what to emphasize, which stories to choose, what the committee needs) is filled by June during sequential workshopping, not by additional agent passes." This is a /workshop-mode-2 (revisionary) statement.
- **Step 3.7 — "Intellectual landscape research (relational tracing)."** The two organizing questions: (1) what does June's work *open up* for them? (2) what threads in their work does June's work *pick up*? These are openings/takings-up applied at the relational-field level. Not similarity-matching; connection-following. The pattern of "two organizing questions framed as openings" should be a /workshop pattern more broadly.
- **Step 3.8 — "Pre-draft cyborg conversation."** The four moves (surfaces candidate framings → human names the story → arc proposal → section beats). The Move 2 guard (agent does NOT generate a candidate). The two failure modes:
  - **Failure A:** Approval-seeking framing — the agent presents arc candidates as "is this OK?" rather than thinking *with* the human. Recovery: agent restates the move — "I'm not asking which is best; I'm surfacing the field so we can decide together."
  - **Failure B:** Directive extraction without understanding-shift — the human says "draft from this" before the conversation has actually shifted the agent's understanding. Recovery: before drafting, the agent names what changed. If nothing changed, the conversation didn't happen yet.
  - Per-use capture in DRAFT_PLAN.md: "Conversation notes / what happened" — did either failure mode appear, what shifted, what would have happened if we'd skipped this step.
- **Step 5.5 — "Presenting the draft and revision process."** /workshop-mode-2 (revisionary) embodied:
  - Pre-assess honestly before showing — "research section has strong specificity; opening is too clause-heavy" — not "this looks good."
  - Announce the plan at session start: "We'll work through this sequentially — cross-document structure first, then each document's argument arc, then sentence-level. One level at a time."
  - **Sequential workshopping is the default revision model.** ONE revision at a time. Not four full documents. Not a batch of edits. One change, one approval, next change.
  - **Exception:** structural revisions to existing draft — when integrating substantive new content, batch the integration; preserve prior version as checkpoint; let the human read V[N+1] as a whole. Sequential is for fine-grained edits and word-count compression, not for content integration where structure needs assessment.
  - **Content first, word counts later.** When integrating substantive changes, lock content first; treat word-count compression as separate downstream phase.
  - **Overwhelm detection:** increasing typo density → shorter responses, targeted questions, simpler language without reducing depth, explicit check-in.

### From INSIGHTS.md

At `~/Documents/GitHub/cyborg-methodologies/INSIGHTS.md`:

- **2026-04-29 — "Pattern-matching as relational tracing, not similarity-clustering."** The cyborg-distinctive analytical move. Default AI pattern-matching pulls toward similarity (lateral, feature-matching, twin-finding). The cyborg move is connection-following — what's *connected to* what's here, what *relates to* it, what it *talks to*. This frame is what /workshop's generative mode requires to do its job. Without it, generative workshops produce credential-listing, alignment-announcing, feature-overlap planning. With it, they produce planning that thinks WITH the human and the audience.
- **2026-05-07 — "Adversarial swarm as design review method."** Less directly relevant but shows the pattern: cyborg-methodology capabilities extracted as standalone skills get more use than buried-in-larger-workflow capabilities.

### From printpress SPEC (the cross-cutting capability section)

At `~/Documents/GitHub/cyborg-methodologies/printpress/SPEC.md` § "Dialogic information-gathering (cross-cutting capability)" — currently embedded in /printpress, will move to /workshop when the split happens. Contains:

- **Three principles** (from cgt-skill, condensed): conversation IS the work; openings and takings-up; creative leaps happen in the dialogue, not in either party alone.
- **Scale: quick-scan vs. deep dialogic mode.**
  - *Quick-scan* (most asks): single specific question, one piece of information, no voice memo. Examples: "Where's the source material?" "Did you want to include X here, or save it for Y?"
  - *Deep dialogic* (rare but high-stakes): full Stage 1 conversation, paper-writing's story development, profile setup, peer-review Stage 1 design. Voice memo invitations appropriate. The skill names the shift: "This is a deeper conversation — voice memo question, take 60-90 seconds."
  - Default to quick-scan unless the question genuinely needs structured space. Don't promote a clarifying question into a full reprise; don't reduce a paper's story-development to a one-line ask.

### From UX_STUB.md (the interview-pattern UX layer)

At `~/Documents/GitHub/cyborg-methodologies/printpress/UX_STUB.md` — interaction patterns for each generative-mode moment:

- **Two question modes:**
  - *Structured choices* → AskUserQuestion tool (2–4 options, "other" always available). Use for: confirmations, panel approvals, learning loop prompts.
  - *Reflective/generative questions* → Voice memo invitation. Use for: Move 2 (name the story), source material discovery, profile setup. Format: "This is a voice-memo question — 60-90 seconds is enough. [Specific framing question]. I'll read the transcript when you're done."
- **PARK tangents.** Capture explicitly: "Parking that — [brief summary]. Continuing with [current thread]." Don't let tangents get lost; don't let them hijack the flow.
- **One thing at a time.** Never present multiple questions or decisions simultaneously.
- **Specific over open-ended.** Where options exist, surface them as structured choices. "What's the one thing you want this document to accomplish?" beats "Tell me about this application."
- **Overwhelm detection.** Increasing typo density → shorter responses, ask one targeted question, check in.

### From the /printpress + /critic-swarm spec set

The four-move generative pattern instantiated for drafting (currently in /printpress SPEC § Stage 1):

1. **Move 1** — Agent surfaces candidate framings (2–4 options). What does each open up for the reader/venue? What thread does it pick up? Don't pick — present the field.
2. **Move 2** — Human names the story. *Agent does NOT generate a candidate.* The agent opens with a question, listens, reflects back. If it tries to answer for the human, it's collapsing the relational structure that makes the leap possible.
3. **Move 3** — Arc proposal under genre conventions and formal parameters. Distinguish formal parameters (non-negotiable: word limits, prompts) from genre conventions (creative space for intentional rule-breaking).
4. **Move 4** — Section beats and load-bearing specifics. From assembled context, what does each section carry? What's deliberately NOT included and why.

**Output:** DRAFT_PLAN.md (or analogous artifact for non-drafting workshops). Captures: what was opened, what was taken up, what was decided, what was deliberately NOT done, conversation notes (failure modes A/B + what shifted).

This four-move pattern generalizes beyond drafting. For any generative workshop:
- Surface options (don't pick)
- Human names what they want (agent doesn't generate it for them)
- Propose structure under constraints (formal vs. conventional)
- Get specific about beats with grounding

---

## Design language for the eventual /workshop SKILL.md

When we build /workshop, the skill should:

### Modes

**`/workshop generate [topic]`** — generative mode. Four-move pattern (or scaled variant). Outputs a plan/decision document.

**`/workshop revise [artifact-path]`** — revisionary mode. Sequential one-edit-at-a-time workshopping. Pre-assesses, announces the plan, works through one level at a time, watches for overwhelm.

**`/workshop ask [question]`** — quick-scan mode. Single dialogic ask, used when scale is small.

When invoked from another skill (/printpress, /critic-swarm), the calling skill specifies the mode and passes context.

### Required reading at invocation

- INSIGHTS.md 2026-04-29 (relational tracing) — required to do the generative four-move work in the right mode
- cgt-skill memos 006, 012, 016 (the dialogic core)
- For /printpress integration: the active genre config (which carries genre-specific framings for Move 3 and 4)
- For revision mode: the artifact being revised + any prior conversation context
- The working directory's CLAUDE.md (per the file-finding protocol)

### Adversarial sycophancy protection (parallel to /critic-swarm's protection)

Default LLM mode in dialogue is helpful encouragement. /workshop's adversarial protection isn't critique — it's resistance to **directive collapse** (the agent making decisions for the human) and **approval-seeking framing** (the agent asking "is this OK?" instead of opening fields). The constitutive instruction:

> Your default mode is helpful agreement. The cyborg practice requires you to resist that — not by being contrarian, but by *opening rather than concluding*, *surfacing rather than deciding*, *letting the human name what matters rather than naming it for them*. Move 2 specifically: do not generate a candidate. Ask, listen, reflect.

### Learning loops

Per-session: workshop conversation log (failure modes A/B observed, what shifted, what would've happened if we'd skipped this).

Skill-global: pattern recognition on which conversational moves produce sharp work vs. shallow ratification. Periodic review surfaces refinements to the four-move pattern, the scale-judgment heuristics, the register-priming.

### Integration with /printpress

- Stage 1 (pre-draft cyborg conversation): /printpress invokes `/workshop generate` with the genre config + Stage 0 data as context. /workshop returns DRAFT_PLAN.md.
- Stage 4 (revision): /printpress invokes `/workshop revise` with the draft + critic-swarm synthesis. /workshop returns the revised draft + workshop notes.

### Integration with /critic-swarm

When a critic surfaces "more author input needed" mid-review, /critic-swarm invokes `/workshop ask` for a small dialogic ask. After the ask resolves, /critic-swarm resumes synthesis. Per /printpress SPEC § Dialogic information-gathering.

### Standalone use cases (when /workshop matters most)

- **Profile setup workshops** (currently inside /printpress UX_STUB.md profile setup section)
- **Genre config workshops** when "other" accumulates (currently inside /printpress SPEC § Learning loops)
- **Peer-review Stage 1 design** (the hard build blocker — IS a workshop we haven't designed yet)
- **Research methodology design**
- **Working through complex decisions** with structured dialogue
- **Conceptual debugging** — when a problem isn't yielding, sometimes the dialogic frame is what surfaces the actual question

---

## Principles to bake into /workshop at build time (from observed use)

These emerged from real use before /workshop was built. They belong in /workshop's `principles.md` (skill-wide patterns from use, parallel to /printpress's principles.md).

### Compression is structural, not line-level

Real compression rebuilds the architecture of a passage, not just tightens individual sentences. The recurring agent failure mode is **line-level trimming** ("is this sentence tighter?") substituted for **structural restructuring** ("what's this passage actually doing, and what's the tightest architecture for that?"). When agents say "I can't cut more without losing meaning," they usually mean "I can't cut words without losing meaning" — which is a different and narrower operation.

Real compression:
- Asks what each passage is doing (its function in the larger argument)
- Identifies redundant architectural moves (this paragraph and that paragraph are doing the same work)
- Restructures: combines, recasts, sequences differently to do the same work in less space
- Preserves semantic content while changing structural shape

Line-level trimming (Williams's stylistic principles):
- Tightens individual sentences
- Stays within existing architecture
- Useful as a final polish, not a substitute for structural compression
- Voice-check's `williams_concision` operates here

When /workshop runs in compression mode, the prompt shape MUST activate architectural reading, not sentence-tightening. Asking "is this tight?" produces tight-shaped output. Asking "what's this passage doing, and what's the tightest architecture for that?" produces structural compression. Per cgt-skill memo 022, prompt shape carries analytical orientation.

Source: feedback memory `feedback_compression_structural_not_line_level.md`.

### Weakness-and-attention flag pass (distinct from compression)

Surfaced in June's 2026-05-07 Duquesne Grefenstette session (memory: `project_printpress_compression_phase.md`). The revision phase has THREE distinct components, not two:

1. **Substantive revision** — addressing /critic-swarm convergent flags (content layer)
2. **Williams-style line-level compression** — preserving semantic content through stylistic tightening (craft layer; voice-check's `williams_concision`)
3. **Weakness-and-attention flag pass** — *distinct from compression* — identifying sentences/phrases/paragraphs that don't earn their place: weaker than surrounding prose, decorative without doing argumentative work, repeating work done elsewhere, gesturing rather than doing. This is editorial judgment about what's *load-bearing*, not just what's *tight*.

The weakness pass and structural compression are related but distinct:
- Compression asks: "what's the tightest architecture for what this passage is doing?"
- Weakness pass asks: "is each part of this passage actually doing the work it should be doing?"
- A passage can be tightly written AND not earning its place (weakness pass flags it).
- A passage can be load-bearing AND poorly compressed (compression pass tightens it).

When /workshop is built with revisionary mode, the dual-mandate (compression + weakness) is part of the canonical pass after substantive content revision. Output structured for one-at-a-time author approval (per sequential-workshop preference).

### Word count is a final-pass concern, not a structural-draft constraint

Agents default to enforcing word counts as hard constraints throughout drafting. Real authorial workflow: draft long, shorten before submission. Compression is its own pass after content is locked.

- Stages 0–2: word count is informational, not optimized for
- Stage 3 review: word count is not a primary critique dimension
- Stage 4 (content phase): structural revision first, before compression
- Stage 4 (compression phase): word count is the primary target; apply structural compression principles
- Stage 4.5 QC: word count check as verification

Exception: when the human explicitly asks for compression mid-process, do it. This rule is about the agent's *default behavior*, not about ignoring directives.

Source: feedback memory `feedback_word_count_final_pass_only.md`.

---

## Feedback-deposit mechanism (gap to design)

**The gap June surfaced:** /workshop should have a place where recurring author feedback lives so it doesn't have to be re-explained every session. Currently, feedback like "compression is structural, not line-level" or "word counts shouldn't be enforced before final pass" requires re-articulation each time.

**Design (parallel to /printpress's principles.md + voice-check's profile):**

Two surfaces:

1. **`~/.claude/skills/workshop/principles.md`** — skill-wide patterns that emerge from use across all authors. Like /printpress's principles.md. Read at every invocation. Edited via the periodic learning loop. The two principles above (structural compression, word-count timing) live here.

2. **`~/.claude/skills/workshop/feedback/[author].md`** (gitignored, local only) — per-author overrides and additions. Same convention as voice-check profiles and /critic-swarm author profiles. For author-specific patterns that don't generalize. Most authors will have this empty initially; populated through use.

**At invocation, /workshop reads:**
- `principles.md` (skill-wide)
- `feedback/[author].md` (if present)
- Both shape how the workshop operates

**At end of session:**
- /workshop offers: "anything you'd like me to remember for next time?" — captures author-specific feedback that goes to `feedback/[author].md`
- Skill-wide principle promotion happens through periodic review, not real-time (parallel to /critic-swarm's cross-stack generalization)

This makes the feedback-deposit mechanism explicit. June's "agents need to be less rigid about word counts" feedback wouldn't need to be re-stated; /workshop would already know.

---

## Open design questions for the build session

1. **Does /workshop own the four-move pattern or does it parameterize?** The four moves are drafting-specific in their current form (candidate framings → story → arc → beats). For non-drafting workshops, the moves might be (options → choice → structure → details) or something else. Probably parameterized: /workshop has a generic four-move shell, each invocation supplies what each move opens.

2. **How does /workshop handle multi-session workshops?** A long workshop (designing a research methodology, peer-review Stage 1) might span multiple sessions. The conversation-as-the-analysis principle implies the workshop's state needs to persist across sessions, not just per-invocation. Worth thinking about: is there a `WORKSHOP_LOG.md` per workshop that persists state?

3. **The relationship to c2c skill.** C2C is Claude-to-Claude collaborative sessions. /workshop is human-AI. Different in some senses, related in others — both are dialogic, both resist consensus collapse, both implement cgt-skill principles. Does /workshop and /c2c share infrastructure (e.g., session logging)? Worth understanding before building.

4. **Voice memo invitation mechanics.** The UX_STUB notes this is unspecified: does the skill prompt and wait, or does the human run mlx_whisper transcription separately? When /workshop is its own skill, this question gets first-class treatment.

5. **Quick-scan threshold.** When does an ask warrant deep dialogic mode? Currently the heuristic is "single specific question vs. paper's story-development" — too vague to be operational. Need clearer signals: voice memo? structured response expected? cross-session-relevant?

6. **Register protection.** Memo 022's sub-distribution routing requires the workshop's system prompt to anchor constructivist register from the start. What does that prompt look like? It's a primary architectural element, not a UX detail.

7. **The pattern for non-drafting Move 4 (specifics with grounding).** In drafting, Move 4 names section beats with grounding from Stage 0 fact assembly. For other workshops (research methodology, decision-making), what plays the role of "beats with grounding"? Probably "concrete commitments with the evidence/reasoning that supports them" — but worth specifying.

---

## Build order (when ready)

Wait until /printpress + /critic-swarm v1 has been used 5–10 times. By then:
- The dialogic patterns will have been used enough to know what's working
- Failure modes will have surfaced in real use, not just designed against
- The integration points with /printpress and /critic-swarm will have stress-tested cleanly enough to know the calling conventions

Then:
1. Extract the dialogic content from /printpress SPEC (currently § Dialogic information-gathering and § Stage 1 four moves) into /workshop SPEC.
2. Build /workshop SKILL.md with the three invocation modes (generate / revise / ask).
3. Update /printpress to invoke /workshop at Stage 1 and Stage 4 instead of containing the dialogic logic itself.
4. Update /critic-swarm to invoke `/workshop ask` for mid-review author input.
5. Create the workshop log conventions (per-session + skill-global learning).
6. Test on a non-drafting use case first — peer-review Stage 1 design, OR a research methodology workshop, OR profile setup as a standalone workshop.

---

## What this document is for

When future-us comes back to build /workshop, this file:
- Reminds us that the dialogic capability is a real cyborg-methodology, not an ad-hoc UX detail
- Points at the source material so we don't re-search
- Captures the design language while it's fresh
- Names the open questions so the build session starts from a clear list
- Marks what's been thought through (the modes, the principles, the integration points) vs. what hasn't (the invocation specifics, the multi-session handling, the c2c relationship)

The dialogic capability is currently distributed across /printpress SPEC, UX_STUB, PIPELINE.md, INSIGHTS.md, and the cgt-skill memos. /workshop is the consolidation. These notes are the consolidation map.
