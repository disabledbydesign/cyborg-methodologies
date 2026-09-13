# /critic-swarm — Adversarial Reviewer Swarm Skill Spec

**Design date:** 2026-05-07  
**Status:** Design spec — not yet built. Extracted from /printpress 2026-05-07 to operate as an independent skill.

---

## What this is

An adversarial reviewer swarm. Pass any artifact through multiple critical perspectives in parallel, get back a synthesis oriented toward improvement (cuts and substantive flags), not validation.

Used as a component of `/printpress` (drafting pipeline Stage 3) AND invokable standalone for any document that needs critical review: design specs, agent prompts, research protocols, briefing docs, plans, papers, applications, instructions.

The swarm is **explicitly adversarial** — these are critics oriented to counteract sycophancy, not friendly readers. Helpful encouragement is the default LLM mode and the failure mode this skill exists to correct against.

---

## Why this is its own skill

Originally designed inside /printpress as Stage 3, extracted because:
1. **Architectural cleanliness.** /printpress becomes thinner; the swarm has its own learning loop, persona library, evolution path.
2. **Discoverability.** Capabilities get used way more once they have their own door. Used on the /printpress spec itself during design (meta-application).
3. **Cyborg-methodologies as a methodology library.** The swarm is shareable as a standalone methodology. Other people doing AI methodology work can use it without /printpress.
4. **The meta-application is a reproducible practice.** Running the swarm on design artifacts (specs, plans, instructions) is its own valuable practice. INSIGHTS.md 2026-05-07 records this.

---

## Invocation

`/critic-swarm [artifact-path]` — runs the swarm with default persona stack inferred from artifact type.

`/critic-swarm [artifact-path] --personas [stack-name]` — runs with a named persona stack.

`/critic-swarm [artifact-path] --personas [persona1,persona2,...]` — runs with explicit persona list.

`/critic-swarm [artifact-path] --reviewer [single-persona]` — runs a single reviewer (e.g., just author-informed, just intelligibility).

When invoked from /printpress: the calling skill passes the persona stack and the relevant context (posting, funder profile, department profile, etc.) as inputs. /critic-swarm doesn't need to know about drafting; it just runs the swarm and returns synthesis.

---

## Core principles

**Adversarial orientation.** The skill briefs each persona to read with skepticism appropriate to their lens (a panel reviewer's skepticism, a hiring manager's, a peer reviewer's, a build agent's). Default LLM mode is helpful encouragement; this skill exists to pull against that.

**Designed to detect, not enumerate.** Reviewers are oriented by lens, not by checklist. A persona prompt that says "evaluate the following 7 things" produces seven evaluations. A persona prompt that says "you are X, you read this as Y" produces analysis the prompter didn't anticipate — including the things that turn out to matter.

**Convergence preserves variance.** When multiple reviewers flag the same thing, that's high priority. When a single reviewer flags something, that's a specialty insight from their lens — preserve it, don't average it away.

**Default move is cut, not add.** The synthesis is oriented by relational threading — following connections across the full swarm output to surface what's load-bearing, what's redundant, what should be cut. Cut list is the most actionable output.

---

## Always-runs reviewers (run on every invocation regardless of stack)

### Intelligibility reviewer

Reads as a cold reader who has never seen this artifact and marks every place they'd stop, re-read, or get confused. Not voice, not argument quality — pure intelligibility.

**Reads at four levels: sentence, paragraph, document, cross-document.** Real editors operate at all four simultaneously; restricting the reviewer to sentence-level produces sentence-clean documents that fail at the architecture level. Designed to detect, not enumerate — reads the artifact as a cold reader and flags whatever doesn't land at any level, without classifying the failure mode first. The categories below are common patterns to seed the reading at each level, not a checklist that exhausts the failure space. The general case at every level is "reader can't follow."

**Level 1 — Sentence:**
- Sentence-level re-read zones (new information at sentence start; nominalization stacks)
- Broken reference tracking (pronouns / "as discussed above" pointing to deleted or ambiguous antecedents)
- "Off" passages (things that read wrong without being technically incorrect)
- Post-compression logical breaks (cuts leave connectives connecting things that no longer justify them)

**Level 2 — Paragraph:**
- Paragraph purpose — does each paragraph do what its position requires? Opening paragraphs orient; middle paragraphs argue; closing paragraphs land.
- Transition incoherence — paragraph transitions that assert a relationship that no longer holds, or that don't pick up what the prior paragraph put down.
- Topic sentence honesty — does the topic sentence accurately preview what the paragraph does, or does the paragraph drift?
- Section-opening paragraphs do extra work — orient the reader to what the whole section is working toward, not only what the immediate paragraph argues. Headers say what a section is *about*; the section-opening sentence says what the section is *arguing*.

**Level 3 — Document:**
- **Concept-introduction** — are key concepts the document depends on introduced at first use? Pay particular attention to (a) **invented terms** (coinages by the author — they know what these mean; no reader does), (b) **specialized terms from non-dominant traditions** (insider readers may know these, but the document is rarely read by purely insider audiences), (c) **cross-tradition terms with multiple meanings**. Failure here is often load-bearing and was the trigger for adding this level (Duquesne Grefenstette session, 2026-05-08).
- **Stakes-orientation** — does the document tell the reader why this work matters / what field it's in / what's at stake?
- **Architecture coherence** — do the sections build into an argument, or sit as a list? Can a reader reconstruct the argument from *section-level topic claims* (what each section is arguing toward), not only paragraph topic sentences? Going straight from a section header into paragraph content treats the section as a content-bucket rather than a move in the document's argument.

**Level 4 — Cross-document** (when multiple docs from a single submission are reviewed together):
- Standalone-vs-dependent readability — does each document stand alone, or does each implicitly assume the reader has read the others?
- Allocation accuracy — concepts duplicated across documents, or absent from both because each assumed the other carried it (PIPELINE Step 1.5 allocation table).
- Voice consistency across the set.

Reports: specific passage or structural problem → which level the failure occurred at → what the confusion was → what the reader would have needed.

### Jargon reviewer

Venue-aware: knows what's normal shorthand for the relevant venue and calibrates to it. Leans toward dejargoning broadly.

**For interdisciplinary work, reads from BOTH (or all) field perspectives.** If an artifact crosses tech and ethnic studies, readers from each camp must be able to follow — terms obvious in one field can be opaque in the other, in both directions. Same for Indigenous studies + anthropology, AI safety + critical theory, public-facing + scholarly. Identify the camps from the artifact and venue, then run jargon checks against each.

Reports: term → which camp it fails for → what they hit → suggested replacement or brief in-text gloss.

### Author-informed reviewer (profile-gated)

Reads from the inside — knows the author's work deeply enough to trace connections upward and outward. Profile-gated: requires `~/.claude/skills/critic-swarm/profiles/[author].md` (gitignored, local only). If no profile exists, asks the author to point to one or build one; skips this reviewer if declined.

Profile points to source documents (briefing, CV, application context, common-mistakes lists). Reviewer reads: profile + source documents + the artifact. Default move is CUT, not ADD.

Finds:
- **Redundancy** (two passages carrying the same weight)
- **Overlap** (a concept re-explained from scratch that's already carried elsewhere)
- **The author's documented failure patterns** (from the profile — e.g., dropped connecting context, compression casualties, assumed background, common drafting mistakes specific to this author)
- **Underselling** (contributions hedged when strong, tools described as minor when central)
- **Overclaiming** (the inverse failure — claims that don't match what source materials support, scope inflation, contributions described larger than they are, things the author hasn't built described as if they have). Flag systematically — if overclaiming patterns appear in source materials themselves, they propagate through every artifact. The reviewer catches both the surface claim AND the systemic pattern when it spots one.
- **Factual inaccuracies** (wrong dates, affiliations, descriptions that don't match source of record)

If something missing can be spliced into existing text without expanding word count, flag with a specific location — otherwise identify what comes out first to make room.

Output: **cut candidates** + **threading suggestions** (rare — only when payoff justifies the cost).

> **v2 design question (deferred):** what's the right memory architecture integration for the profile? Candidates: Kintsugi, MemPalace, Karpathy's system. Research lives in `~/Documents/GitHub/research/` and `~/Documents/GitHub/relational-memory-architecture/`. v1 uses flat markdown; the right v2 answer requires reviewing those repos.

---

## Persona library

Personas live in `~/.claude/skills/critic-swarm/personas/`, organized by stack. The library starts from the existing adversarial reviewer template at `/Users/june/Documents/Filing/Job Search/templates/adversarial_reviewer_personas.md`.

Default stacks (extensible):
- **`design_spec`** — future build agent + skeptical architect. Used on specs, architecture docs, plans. (This is the stack we used on the /printpress spec.)
- **`academic_position`** — search committee personas anchored to actual faculty (from `DEPARTMENT_PROFILE.md`), with deep enough read of each faculty member's scholarship to give the persona teeth. Plus posting-aware framing.
- **`grant_fellowship`** — program officer + panel composition from funder profile.
- **`non_academic_application`** — hiring manager + culture-fit reader + ATS compatibility reviewer.
- **`peer_review`** — editor agent (selects panel, see below) + 2–3 subject-appropriate reviewers + source validator.
- **`agent_prompt`** — fresh build agent + skeptical user (red-team for prompt brittleness).
- **`research_protocol`** — methodologist + skeptical reviewer.

When invoked without a stack, the skill infers from artifact type or asks.

### Peer-review specific: editor agent

When the persona stack is `peer_review`, an **editor agent runs first, before reviewers**. Reads the article + target journal + bibliography, selects 3–4 reviewer personas (drawing from the bibliography, recent journal contributors, and scholars in direct conversation with the article's subject). Output: proposed reviewer panel with rationale. **Show the author the panel before launching reviewers** — they can override.

### Peer-review specific: source validator

Reads source materials (fieldnotes, data, prior drafts, PDFs) and validates claims against evidence. Finding source materials: looks first in the working directory's `CLAUDE.md` for a source materials section; if absent, asks the author directly. Project organization varies — don't assume.

---

## Synthesis

Done by the main agent after subagents return. Not a separate subagent.

Oriented by relational threading — following connections across the full swarm output to surface what's load-bearing, what's redundant, and what the revision should prioritize. Default move: cut, not add.

**Output structure (cut list first — that's where most revision work lives):**
1. **Cut list** — specific, actionable, start here. Format: passage → why it can go → estimated word savings.
2. **Convergent flags** — 3+ reviewers flagged this. High priority.
3. **Threading suggestions** — from author-informed reviewer (rare; only when payoff justifies).
4. **Specialty insights** — divergent flags (single reviewer). Consider, don't average.
5. **Mechanical flags** — jargon, intelligibility. Address before save.

Praise from multiple reviewers marks load-bearing passages — protect in revision (advisory, no enforcement).

Convergent vs. divergent: don't average rankings or critiques. "Three middle and two upper-middle" averages to "middle" but that's misleading; the two upper-middle saw something the others didn't, and vice versa.

---

## Profile system (for author-informed reviewer)

Stored at `~/.claude/skills/critic-swarm/profiles/[author].md`. Not committed to git. Same convention as voice-check profiles.

```markdown
# Author profile — [Name]
# Last updated: [date]

## Key contributions
<!-- What this person has done that tends to get undersold. Specific. -->

## Key projects
<!-- Current and recent work, with brief descriptions. Source paths if they exist. -->

## Failure patterns
<!-- What goes wrong in their drafts. Working memory, compression, common mistakes. -->

## Source documents
<!-- Paths to fuller briefing docs (CV, research statement, briefing doc). -->
```

**Building from data:** optional bootstrap. Point the skill at documents (PDFs, CVs, research statements) and it extracts a draft profile for review.

**Setup UX:** see UX patterns shared with /printpress (voice memo questions, AskUserQuestion for choices, one thing at a time). Documented in /printpress UX_STUB.md.

---

## Learning loops

### Tier 1: Document-local
Each invocation logs swarm performance to `LEARNING_LOG.md` in the working directory: which personas surfaced sharp critique, which were shallow, what convergent flags appeared, what was addressed vs. held.

### Tier 2: Skill-global (actually improves the skill)

| What | Reads at | Writes at | Location |
|---|---|---|---|
| Persona stack refinements | Invocation | After synthesis | `~/.claude/skills/critic-swarm/stacks/[stack].md` |
| Persona performance data | Invocation | After synthesis | `~/.claude/skills/critic-swarm/persona_perf.md` |

**Periodic stack review** — after every 3rd–5th use of a stack, **surface the prompt at invocation:** "You've used [stack] N times since the last review. Shall we do a quick stack update before proceeding? (5 minutes, can skip.)" Don't rely on the author to initiate.

**Cross-stack generalization** — some learnings are skill-wide, not stack-specific. The synthesis step should flag when a pattern observed in one stack might apply to others. Periodic cross-stack review feeds the swarm's general principles section.

---

## Standalone use cases

Beyond /printpress integration:
- **Design review** — run the `design_spec` stack on specs, plans, architecture docs (this is what we did on the /printpress spec itself)
- **Author-informed review of contractor work** — author runs `--reviewer author-informed` on a draft someone else produced of their work
- **Agent prompt stress-testing** — run `agent_prompt` stack on a prompt template
- **Research protocol review** — run `research_protocol` stack on a methodology design
- **Pre-submission peer simulation** — run `peer_review` stack on a paper before submitting

The pattern: any artifact that benefits from multiple critical perspectives benefits from the swarm.

---

## What's NOT in this spec yet

- **Persona library extraction** — currently in `/Users/june/Documents/Filing/Job Search/templates/adversarial_reviewer_personas.md`. Build step: extract into `~/.claude/skills/critic-swarm/personas/` organized by stack.
- **Memory architecture** (see v2 note above)
- **Stack auto-detection from artifact type** — when `--personas` is omitted, how does the skill decide? Ask vs. infer vs. default.

---

## Build order (post-FFS, with /printpress)

1. Extract personas from `templates/adversarial_reviewer_personas.md` into `personas/` organized by stack
2. Stack definitions in `stacks/`
3. Subagent dispatch logic + synthesis
4. Profile system + UX (mostly shared with /printpress)
5. Learning loop plumbing
6. /printpress integration test (printpress invokes critic-swarm at Stage 3)
7. Standalone test on a non-drafting artifact (a design spec or agent prompt)

---

## Relationship to /printpress

`/critic-swarm` is invoked by `/printpress` at Stage 3. /printpress passes:
- The draft (artifact path)
- The persona stack (genre-determined)
- Relevant context (posting, funder profile, department profile, etc.)

/critic-swarm executes the swarm and returns synthesis. /printpress's Stage 3 spec collapses to "invoke /critic-swarm with [stack + context]."

Standalone invocations don't go through /printpress — they invoke /critic-swarm directly.
