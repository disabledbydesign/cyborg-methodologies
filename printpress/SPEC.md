# /printpress — Drafting Workflow Skill Spec

**Design date:** 2026-05-07  
**Status:** Design spec — not yet built. Invocation syntax unspecified. Multi-document applications unspecified. See "What's NOT in this spec yet" for the build gaps.

---

## What this is

A full invokable drafting pipeline. Genre-parameterized. Owns the full cycle: data-in → pre-draft conversation → draft → reviewer swarm → synthesis → revised draft.

This skill cannibalizes and replaces PIPELINE.md as the execution entry point. Invoking `/printpress` runs the full workflow — fit eval, Hakope's Question, cyborg conversation, draft, reviewer swarm, synthesis. PIPELINE.md's execution logic moves INTO the skill's genre configs. PIPELINE.md becomes the documentation layer — the WHY behind each step — valuable to keep as prose explanation, but agents follow the skill, not the doc.

Voice-check (`~/.claude/skills/voice-check/`) and the adversarial reviewer (currently `templates/adversarial_reviewer_personas.md`) are components of this skill, not separate workflows.

---

## Genres

Five genre configurations. Genre determines: data-in sources, swarm composition, and what the pre-draft conversation focuses on.

| Genre | Description | Voice-check tag mapping |
|---|---|---|
| `academic_position` | Academic job applications. Absorbs PIPELINE.md logic into the genre config. | `academic_position` (1:1) |
| `non_academic_application` | Industry, tech, nonprofit, govt, EdTech, EA orgs. | Per-application: `tech_position` for industry; voice-check needs new tags (`nonprofit_position`, etc.) for others. Genre config asks or infers. |
| `grant_fellowship` | Any grant or fellowship with a review panel. | `ea_grant` (SFF, LTFF, Coefficient) OR `humanist_fellowship` (Wenner-Gren, ACLS, NEH). Planned split into two genres deferred — see note below. |
| `peer_review` | Journal articles, book chapters, manuscripts. | `peer_review` (new — voice-check adds when first profile is built). |
| `other` | Unknown genre — ask the author. Learning loop tracks accumulation. | Asks the author or infers per invocation. |

**Planned genre split (deferred):** `grant_fellowship` should split into `ea_grant` and `humanist_fellowship` to match voice-check's existing tag distinction. The two have meaningfully different reviewer cultures (technical/impact-focused vs. subject-area scholars). Personas need stack-appropriate framings for each, which is design work for a focused session — not mechanical rename. v1 keeps `grant_fellowship` as one genre with the voice-check tag selected per-application.

---

## Dialogic information-gathering (cross-cutting capability)

*The model here is adapted from cgt-skill's dialogic memos (memo 006, 012, 016) — "the conversation is the analysis," "designing for creative leaps," and "openings and takings-up." See `~/Documents/GitHub/cyborg-methodologies/cgt-skill/memos/`.*

The skill uses dialogue to gather information whenever it needs to — not just in Stage 1. Stage 1 is the most structured use (the four moves), but the same dialogic mode is available across the workflow:

- **Stage 0**: when source material isn't retrievable (peer_review fieldnotes, "other" genre context), ask
- **Stage 1**: structured four-move conversation (most extensive use)
- **Stage 3** (via /critic-swarm): a critic might surface a point where more author input is needed — a story from experience, a fact only the author has, a clarification on what's load-bearing. The skill dispatches a small dialogic ask back to the author, then resumes review
- **Stage 4 revision**: workshopping is itself dialogic — sequential one-edit-at-a-time conversation
- **Profile setup**: voice memo questions to extract author profile

### Three principles (from cgt-skill)

**1. The conversation IS the work, not preparation for it.**  
The dialogue isn't a means of gathering information that then feeds drafting — the dialogue is where the structure of the document gets constructed. DRAFT_PLAN.md is residue of the conversation, not its purpose. If the conversation produces a plan that the agent then "implements" without further dialogue, the conversation didn't do its job.

**2. Openings and takings-up — the dialogic structure to use.**  
The four moves of Stage 1 (and any dialogic ask elsewhere) are openings and takings-up:  
- Move 1 *opens* candidate framings  
- Move 2 *takes up* one of those openings (or names a different one entirely)  
- Move 3 *opens* arc possibilities under genre conventions  
- Move 4 *takes up* by getting specific about beats  

The prompt shape carries analytical orientation. Asking "what does this framing open up for the reader?" produces opening-shaped output. Asking "do these match the posting?" produces match-shaped output. The skill should default to opening-shaped questions and let the author's takings-up do the convergent work.

**3. Creative leaps happen in the dialogue, not in either party alone.**  
The agent's surface (candidate framings, arc proposals) gives the author something to articulate against. The leap — the actual story for this document, the right opening, the structural move that makes everything land — emerges relationally. This is why Move 2's guard matters: if the agent answers for the author, it's collapsing the relation. The author's redirect IS the leap, made possible by the agent's surface.

### Scale: quick-scan vs. deep dialogic mode

The capability has two registers, and the skill is transparent about which it's in.

**Quick-scan** (most asks): a single specific question, one piece of information needed. No voice memo, no structured moves. Examples: "Where's the source material?" "Is the funder profile up to date?" "Did you want to include the Autograder finding here, or save it for the equity statement?"

**Deep dialogic** (rare but high-stakes): full Stage 1 conversation, paper-writing's story development, profile setup, peer_review Stage 1 design. Voice memo invitations are appropriate here. The conversation has its own time and structure. The skill names the shift: "This is a deeper conversation — voice memo question, take 60-90 seconds."

Default to quick-scan unless the question genuinely needs structured space. Don't promote a clarifying question into a full Stage 1 reprise; don't reduce a paper's story-development to a one-line ask.

### Interview pattern

Per UX_STUB.md: structured choices via AskUserQuestion, voice memo invitations for reflective/generative questions, one thing at a time, PARK tangents, specific over open-ended.

---

## Where the skill finds local files

The skill is universal; user data is local. The skill finds local files via this priority:

1. **Working directory `CLAUDE.md`** — the primary mechanism. The skill reads any `CLAUDE.md` it finds in the directory it's invoked from for: where applications/archives live, where source materials are kept, where prior versions are stored, where templates are, where the author's briefing doc lives. Project-level CLAUDE.mds are already a Claude Code convention; this skill reads them like any other agent would.
2. **Parent directory `CLAUDE.md`** — if the working dir doesn't have one, walk up one level. Useful when invoked from inside a specific application folder where the parent (e.g., the job search root) holds the structure.
3. **Skill profile** (`~/.claude/skills/critic-swarm/profiles/[author].md`) — for author-specific source documents (briefing, CV, application context). See the Author-informed reviewer in /critic-swarm.
4. **Ask the author** — if none of the above answer the question. Quick-scan dialogic mode (see Dialogic information-gathering above).

**The skill should NOT maintain its own user-paths config file.** Directory-level CLAUDE.md is already where this kind of "where things are" information belongs. Don't create a parallel system. If a user wants the skill to know where their applications archive lives, they add it to their working directory's CLAUDE.md.

---

## Workflow

### Stage 0: Data-in

Assemble what the full pipeline needs before anything else runs. Genre-specific sources; generic structure (what facts does the draft need?).

**All application genres:** for track-specific prior-application lookup (which prior application to pull as a voice model), the skill reads CLAUDE.md in the working directory or its parent for the track lookup table or paths to it (per the file-finding priority above). The data is local; the skill is universal. PIPELINE.md is documentation, not data.

**`academic_position`**  
Posting (`POSTING.md`), department profile (`DEPARTMENT_PROFILE.md`), intellectual connections (`INTELLECTUAL_CONNECTIONS.md`), funder/department profile, voice-final priors (see PIPELINE.md track lookup). If any are missing, create them before proceeding.

**`grant_fellowship`**  
Call for proposals (verbatim — save as `POSTING.md` or `APPLICATION_STRUCTURE.md`), funder profile (`_funder_profiles/[FUNDER].md` — create if absent), prior applications from same track.

**`non_academic_application`**  
Posting (`POSTING.md`), company/org profile (`COMPANY_PROFILE.md`), voice-final priors (see PIPELINE.md track lookup).

**`peer_review`**  
Ask the author: where is the source material? (fieldnotes, data, prior drafts, source PDFs — these aren't retrievable without their input.) Also: target venue guidelines, special issue call or CFP if applicable. Save venue guidelines verbatim.

**`other`**  
Ask the author: what is this document, who reads it, where is the source material? Their answers become the working genre definition for this invocation and get logged to `~/.claude/skills/printpress/other_log.md` (see Learning loops, Tier 2).

> **v2 design question (deferred):** what's the right memory architecture integration for the `other_log` accumulation, profile data, and learning loop history? Candidates: Kintsugi, MemPalace, Karpathy's system. Research lives in `~/Documents/GitHub/research/` and `~/Documents/GitHub/relational-memory-architecture/`. v1 uses flat markdown files; the right v2 answer requires reviewing those repos. Don't pick a system without that review.
---

### Stage 1: Pre-draft cyborg conversation

*Generalizes PIPELINE.md Step 3.8 across genres. The most structured use of a capability that runs throughout — see "Dialogic information-gathering" below.*

The conversation has four moves. The first, third, and fourth are agent-opens-author-redirects. **The second is different — the agent asks, the author speaks, the agent listens.**

**Move 1 — Agent surfaces candidate framings** (2–4 options)  
For each: what does the author's work open up for this reader/venue? What thread does it pick up (relational tracing — connection-following, not feature-matching, per `~/Documents/GitHub/cyborg-methodologies/INSIGHTS.md` 2026-04-29)? What is the Hakope's Question candidate for this context? Present the field — don't pick one yet.

> **Build requirement:** the SKILL.md must instruct agents to read INSIGHTS.md before doing relational tracing. A cold agent without that context will default to feature-matching. The skill should also briefly gloss the term inline so a reader following the skill can follow it, but the deeper reading is required.

**Move 2 — Author names the story** *(agent does NOT generate a candidate here)*  
The agent opens with a question, not a draft: something like "given those options, what's the story you actually want this document to tell?" The author's answer names what's load-bearing that the agent couldn't see from the context alone — a fieldwork moment, a politics they want visible, a refusal of a frame the field wants to impose, a tool whose origin matters here. The agent listens and reflects back. If it tries to answer for them, it's doing Stage 2 early.

**Move 3 — Arc proposal under genre conventions and formal parameters**  
Two different things to handle, not one. Distinguish them.

*Formal parameters (non-negotiable):* a grant's specific prompts, word limits, required sections, structural requirements named in the application itself. These are followed exactly. The arc must respect them.

*Genre conventions (creative space):* reading defaults the genre carries (academic CL norms, fellowship statement gravity, peer_review intro shape). These can be intentionally broken to make things land harder, sparingly. Voice-check has rule-breaking moves of its own. The judgment call: when does a deliberate break sharpen impact, and when does it fight the reader?

The author redirects on what's overweighted, missing, or needs to land earlier/later — within formal parameters, with genre conventions as material to work with rather than rules to follow.
**Move 4 — Section beats and load-bearing specifics**  
From Stage 0 data: what does each section carry? Which scenes, numbers, scholars cited doing work (not name-dropped), prior phrasings to mine. What is deliberately NOT included and why.

**Stage 1 also settles swarm composition:** the question "who actually reads this?" is answered here, not in Stage 3. The cyborg conversation establishes who the reader is; Stage 3 operationalizes that answer into personas. If swarm composition isn't clear by the end of Stage 1, surface the question explicitly before moving to Stage 2.

**Output:** `DRAFT_PLAN.md` in the application/project folder (use `templates/DRAFT_PLAN_TEMPLATE.md`). It captures the arc, openings/uptakes, question-they-have-not-asked reframe, section beats with grounding, swarm composition, and deliberate exclusions. When complexity triggers them, it also records the claim bridge, identity architecture, project selection, and unresolved-comment queue. It distinguishes `DRAFT`, `AUTHOR-HANDLED`, and `PORTAL` requirements so compliance does not silently expand drafting scope.

---

### Stage 2: Draft

From `DRAFT_PLAN.md`. Genre register from the swarm-composition answer.

**Voice-check runs throughout drafting and revision** — not just before/after. The voice profile is read pre-draft (style guide that shapes what gets written), the agent self-runs voice-check after each substantive draft to catch contamination, and contamination is silently fixed during drafting without surfacing to the author. Williams's *Style* principles (in profile as `williams_concision`) apply continuously. Voice-check is also active in Stage 4 revisions — every workshopping edit gets the same treatment.

Execution of the plan, not re-planning. Structural decisions not in `DRAFT_PLAN.md` → surface in conversation before deciding solo (using the dialogic capability, scaled appropriately — usually small).

Stage 2 produces a complete long-form `*_ASSEMBLY_v0.md` before structural selection. Abundance means distinct evidence, scenes, or argumentative paths—not padding—and the actual ratio is recorded rather than enforced. The author sees the full assembly and marks `KEEP / DROP / UNSURE` in a separate decision layer before any autonomous cut.

After marking, the author and agent choose an inspectable route: AI-proposed reversible cut with diff; author-led selection with local Williams-style compression; or hybrid. Preserve the assembly in every route. A handoff near 1.2 times the final limit is a provisional experiment, not a target or proof that AI cutting is good enough. Record assembly, handoff, and final sizes; restored material; rejected cuts; author additions; and observed quality losses or gains.

Reference lists are always author-handled. Academic CVs are author-handled. A required résumé enters drafting unless the author explicitly takes it over.

---

### Stage 3: Reviewer swarm — invokes `/critic-swarm`

Stage 3 invokes the standalone `/critic-swarm` skill on the author-informed handoff, consulting the assembly marks. The handoff may still run over target depending on the selected route. /printpress doesn't own the swarm logic — that lives in `/critic-swarm`'s SPEC.md (`~/.claude/skills/critic-swarm/SPEC.md`). What /printpress owns at Stage 3 is **selecting the right persona stack for this genre and passing the right context.**

**Composition settled in Stage 1.** /printpress determines who reads this document during the cyborg conversation; Stage 3 passes that answer to /critic-swarm as a persona stack.

#### Genre → persona stack mapping

| Genre | Stack passed to /critic-swarm | Genre-specific context |
|---|---|---|
| `academic_position` | `academic_position` | `DEPARTMENT_PROFILE.md`, `POSTING.md`, `INTELLECTUAL_CONNECTIONS.md` |
| `grant_fellowship` | `grant_fellowship` | Funder profile, panel composition, CFP |
| `non_academic_application` | `non_academic_application` | `POSTING.md`, `COMPANY_PROFILE.md`, ATS context |
| `peer_review` | `peer_review` | Article + target journal + bibliography + source materials |
| `other` | author-named (from Stage 1) + intelligibility + jargon | Whatever Stage 1 surfaced |

For `academic_position` specifically: the personas anchor to actual faculty from `DEPARTMENT_PROFILE.md` — /printpress prepares this context (a deep enough read of each faculty member's scholarship to give the persona teeth) and passes it to /critic-swarm.

For `peer_review`: /critic-swarm's editor agent runs first to select reviewers from the article's bibliography + journal contributors. Show the author the panel before launching.

#### What /critic-swarm always runs (regardless of genre)

The intelligibility reviewer, jargon reviewer, and author-informed reviewer (profile-gated) run on every invocation. /printpress doesn't need to specify these — they're the always-runs reviewers in `/critic-swarm`'s spec. /printpress just needs to ensure the author profile path is set up (or skipped) before invoking.

#### Synthesis output

/critic-swarm returns the synthesis (cut list first, then convergent flags, threading, specialty insights, mechanical flags). /printpress passes this synthesis to Stage 4 (Revision).

⚠️ **Stage 1 (pre-draft conversation) not yet specified for peer_review.** See build order — do not implement peer_review genre without a design conversation with the author.

---

### Stage 4: Revision

The author reviews synthesis → sequential workshopping (one edit at a time) → revised draft. Overwhelm detection: increasing typo density = shift to shorter responses, targeted questions, simpler language without reducing depth.

#### Drafting & revision principles

The principles that guide both Stage 2 drafting and Stage 4 revision. Some are encoded in voice-check (`williams_concision`, `patterns.wordy_phrases`); some live here. The skill applies them throughout, not as a final-pass checklist.

- **Less is more.** Removing material that isn't necessary — even when it's good — often makes the draft stronger. Word-count compression isn't a constraint to work around; it's a forcing function for clarity. Cut what doesn't earn its weight.
- **Strategic, not exhaustive.** When the author provides tons of context, that's input for judgment about what's load-bearing — not a checklist to cram in. The point is to enhance THIS draft for THIS reader, not to include everything.
- **Action verbs with clear agents.** Convert nominalizations to verbs ("the analysis demonstrates" → "we demonstrate"). Make the actors explicit. Williams's principle: characters as subjects, actions as verbs.
- **New information after the verb, not in the noun phrase.** Old/anchor information at the start of the sentence; new/landing information at the end (stress position). New information buried in a leading noun phrase is cognitively expensive.
- **Simplify sentence structure for complex ideas.** Complex ideas in simple sentences land harder than complex ideas in complex sentences. Embedded clause chains usually mean an idea wants to be split.
- **Reader orientation at section boundaries.** New sections and paragraphs need a sentence that orients the reader to where they are in the argument. Don't drop them into the middle of a thought.
- **Workshop language in the chat, not in the file.** When the author and agent are deciding how to phrase something, work it out in conversation first, then commit to the document. Don't churn the file with exploratory rewrites.

These are working principles, not a complete list. If voice-check or PIPELINE.md has refinements that should live here, surface them.

---

### Stage 4.5: Pre-save QC verification (light)

Before save, run a brief verification pass that the continuous checks distributed across Stages 2–4 actually happened. Not a re-do — a confirmation. Stages 2 and 3 already addressed each item during flow; this is the integration checkpoint.

**Verification checklist:**
- [ ] Anti-generic — every sentence specific to this author and this position
- [ ] Common drafting mistakes (per genre config) — none surface in the final draft
- [ ] The question they haven't asked (renamed 2026-08-09 from "Hakope's Question") — present explicitly or structurally, and framed as contribution rather than correction (for genres where it applies)
- [ ] Factual claims verified against source documents — no fabricated numbers or descriptions
- [ ] Genre effectiveness — works as the genre it claims to be (PIPELINE Step 4.5)
- [ ] 30-second scan — what does a skimming reader take away? Is it specific, not generic?
- [ ] Dual-audience check (if applicable) — works for both/all camps the document is addressing
- [ ] Reader takeaways — each item from `READER_TAKEAWAYS.md` (Stage 4.7 / PIPELINE Step 4.7) actually lands in the final

If any item fails: address it before save. The discrete checkpoint catches integration issues that continuous checks during flow don't surface (e.g., a takeaway that was in scope at draft-time but got cut during compression and nobody noticed).

If everything passes: proceed to Stage 5.

---

### Stage 5: Save + learning loops

After the author's final edits:
1. Mechanical cleanup — haiku subagent per PIPELINE.md Step 5.9 (see that step for the full subagent prompt template)
2. Save `*_final.md` — canonical source for future agents adapting from this work
3. Append row to `VERSION_LOG.md` — format per `templates/VERSION_LOG_TEMPLATE.md`
4. Voice-check learn pass — the author's revision choices are ground truth. Flag selection logic: if `VERSION_LOG.md` has multiple revision versions, use `--learn-sequence --manifest VERSION_LOG.md` for the full revision arc; if only first draft + final exist, use `--learn FIRST.md FINAL.md`. Per PIPELINE.md Step 7 / `LEARNING_LOOP_PROCEDURE.md`.
5. Write to skill-global genre config (see Learning loops, Tier 2 below)

---

## Standalone review = invoke `/critic-swarm` directly

For reviewing a draft without running the full pipeline (e.g., a contractor's draft, an existing near-final document, a sanity-check), invoke `/critic-swarm` directly rather than going through /printpress. The swarm skill handles standalone use cases.

This is part of why /critic-swarm is its own skill — review-without-drafting has its own door.

---

## Learning loops

Two tiers. Only Tier 2 actually improves the skill across sessions. Tier 1 is project documentation — useful locally, not expected to compound globally.

### Tier 1: Document-local (project documentation)

These logs live in the project folder and stay there. They're useful for that project and as raw material for periodic review, but they don't automatically feed the skill.

| What | Writes to | When |
|---|---|---|
| Pre-draft conversation quality | `DRAFT_PLAN.md` ("Conversation notes") | End of Stage 1 |
| Swarm performance | `LEARNING_LOG.md` in project folder | End of Stage 3 |
| Version transitions | `VERSION_LOG.md` | Each save |

### Tier 2: Skill-global (actually improves the skill)

These files live in the skill directory. **The skill reads them at Stage 0 on invocation.** They represent what was learned across all prior uses.

| What | Reads at | Writes at | Location |
|---|---|---|---|
| Genre config refinements | Stage 0 | After Stage 5 | `~/.claude/skills/printpress/genre_configs/[genre].md` |
| "Other" genre accumulation | Stage 0 | End of any "other" invocation | `~/.claude/skills/printpress/other_log.md` |

**Genre config files** contain: default swarm composition for this genre (updated from Tier 1 LEARNING_LOG.md patterns), what persona types produced sharp critique, what consistently failed. If no genre config file exists for a genre, the spec defaults apply.

**"Other" accumulation:** log each "other" invocation with document type, who read it, what swarm was used. **If this is the 3rd or later "other" invocation, surface the proposal at Stage 0 before proceeding:** "You've used 'other' N times. These uses look like [description] — should we add this as a genre?" The author and agent design the genre config together. The author decides whether to promote. Don't wait for the author to initiate this — they may not remember.

**Periodic genre config review:** after every 3rd–5th use of a genre, **open Stage 0 with a flag:** "You've used [genre] N times since the last review. Shall we do a quick genre config update before proceeding? (5 minutes, can skip.)" Log the review date in the genre config file when it runs. Don't rely on the author to initiate — they may forget.

#### Cross-genre generalization (C + D combined, learning-loop driven)

Some learnings are skill-wide, not genre-specific. Two surfaces feed the generalization signal:

**At log-write (background signal):** when writing to a genre's `LEARNING_LOG.md`, the agent tags each learning as `genre-specific` or `potentially-generalizable`. The tagging is a meta-cognitive judgment that will be wrong sometimes — that's fine, it's input to the loop, not a final decision.

**In synthesis (in-context surfacing):** when /critic-swarm spots a pattern in the current run that might apply across genres, it flags it in the synthesis output: "This persona-grounding move worked here; might be worth applying to other genres." The author sees it and decides whether to promote.

**Periodic generalization review:** as part of the periodic genre config review (above), the skill also reads tagged-generalizable learnings from across genres and surfaces candidate skill-wide principles to the author for confirmation. Confirmed principles get written to a skill-global `~/.claude/skills/printpress/principles.md` (and similar for /critic-swarm). The system self-corrects: tags that turn out to be genre-specific stay there; truly generalizable ones get promoted.

This is the learning loop's job — the agent doesn't need to be right at tag-time; the periodic review validates and promotes.

#### Genre splitting (when one genre needs to become two)

Two complementary mechanisms:

**Subgenre tags within a genre (lightweight).** When a genre starts spanning meaningfully different cases (e.g., `academic_position:teaching-focused` vs. `academic_position:research-focused`), use subgenre tags rather than splitting. Same workflow, different default stacks per subgenre. The genre config holds the subgenre-selection logic (auto-detect from posting language, or ask).

**Periodic genre review surfaces the split question.** When the periodic genre config review runs (above), it explicitly asks: "Is this still one genre, or has it become two?" Signals to look for: recurring swarm composition differences that subgenre tags don't resolve cleanly, author-informed reviewer flags conflicts between subtypes, the genre config has accumulated contradictions. If signals point to a split, design it together with the author.

**Future option (D):** heterogeneity signal in synthesis (every swarm synthesis notes whether the composition felt right). Not in v1 — adds per-session overhead and the periodic review aggregates this signal naturally. Reconsider for v2 if the periodic review is missing splits that should have happened earlier.

---

## Relationship to PIPELINE.md

PIPELINE.md logic that moves INTO the `academic_position` genre config during the build:
- Fit evaluation (PIPELINE Step 1)
- The question they haven't asked, PIPELINE Step 3 (renamed 2026-08-09 from "Hakope's Question touchstone"; the move was also narrowed from corrective to additive — see that step for why)
- Allocation table for multi-document applications (PIPELINE Step 1.5)
- ATS pass (PIPELINE Step 4.4)
- Audience calibration by track (PIPELINE Step 4)
- Post-submission workflow (PIPELINE Steps 6–8)
- All source-doc reading requirements and the enforcement checkpoint

**What stays in PIPELINE.md (not moved into the skill):**
- The *explanatory prose* — the WHY behind each step. Why fit eval matters, why Hakope's Question is the touchstone, why prior materials are loaded structurally not just found. This is documentation for humans reading the file, not workflow for agents executing it.
- The track lookup table — this is local data (June's specific application archive structure), referenced via working directory CLAUDE.md per the file-finding protocol above.
- Long-form rationale for the seven common drafting mistakes, the briefing scope tables, and the analytical mode setup. These are reference content; the skill points to them when needed.
- Anything about the specific job search workflow (post-submission tracker updates, follow-up cadence, calendar integration) that's June-specific operational logic, not generic drafting workflow.

The split is: **executable workflow → skill; documentation, rationale, and author-specific operational data → PIPELINE.md.** When a contradiction appears (the skill says one thing, PIPELINE says another), the skill wins for execution; PIPELINE wins for explaining why.

PIPELINE.md is the authoritative reference *during the build* — the genre config is built from it, not from memory. After the build, PIPELINE.md stays as a human-readable explanation of why each step exists.

The adversarial reviewer template (`templates/adversarial_reviewer_personas.md`) becomes the persona library for `/critic-swarm`. Organized under `~/.claude/skills/critic-swarm/personas/` by stack (per `/critic-swarm`'s spec). /printpress doesn't own personas directly — it specifies which stack to invoke.
---

## What's NOT in this spec yet

Resolved design decisions (formerly gaps):

- **Invocation syntax** — DECIDED: invoke as `/printpress` with no arguments; if no genre context is available, the skill asks the author. No need to specify genre upfront.
- **Multi-document applications** — for `academic_position`, multi-doc logic (allocation tables, CL-as-braid, cross-doc structure) moves from PIPELINE.md Step 1.5 into the `academic_position` genre config. This is part of the PIPELINE cannibalization, not a separate gap. Handled during the genre config build.

Remaining gaps (need resolution before building):

- **Peer-review Stage 1** — ⚠️ STILL A HARD BUILD BLOCKER. We designed peer_review's Stage 3 (editor agent + source validator + reviewers) but NOT Stage 1 (the cyborg conversation for a research article). The Stage 1 conversation for peer_review is structurally different from an application (no posting, no fit eval, different Hakope framing, source material varies). **Do not build peer_review genre without that design conversation.** v1 build scope: `academic_position` + `grant_fellowship` only.
- **Folder structure creation** — does the skill create the application folder and standard files, or assume they exist? Build-time decision; low stakes either way. Perhaps it asks to create the folder if it doesn't already exist? But default to using the one that exists. In practice im going to call the skill in an environment with trackers adn things like that, for job applications - and project directories for papers. 
- **Genre config init** — `genre_configs/` and `other_log.md` need to exist before first invocation. An install/init step is needed.
- **Author profile format** — specced in `UX_STUB.md`. v1: manual markdown file + optional bootstrap from documents (PDFs, CVs, research statements → agent extracts draft profile for review). v2: query MemPalace or equivalent memory architecture instead of a flat file. Don't over-engineer v1 expecting to replace it.
- **Calendar integration** — PIPELINE.md post-submission creates deadline/follow-up reminders. Not scoped here.

---

## Build order (when ready — post-FFS May 2026)

**v1 scope: `academic_position` + `grant_fellowship` only.**  
Peer-review requires a design conversation before building. `non_academic_application` and `other` can be added after v1 is stable.

1. `genre_configs/` directory with stub files for v1 genres + `other_log.md` (init step)
2. Persona library → `personas/` organized by genre (from `templates/adversarial_reviewer_personas.md`)
3. Swarm invocation logic (parallel subagents, main-agent synthesis)
4. Stage 0 data-in templates for `academic_position` + `grant_fellowship`
5. Pre-draft conversation scaffolding (Stage 1) — with Move 2 guard explicit
6. Tier 2 learning loop read/write plumbing
7. Build `academic_position` genre config by absorbing PIPELINE.md logic (fit eval, Hakope's Question, allocation tables, ATS, audience calibration, post-submission). PIPELINE.md becomes documentation after.
8. ⚠️ Peer-review Stage 1 design conversation with the author → then add peer_review genre
