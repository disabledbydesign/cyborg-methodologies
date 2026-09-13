# Voice-Check Pipeline Redesign Spec
**Status:** Design complete. Experiments queued. First test case: Harvard Divinity.
**Last updated:** 2026-04-15
**Session context:** GitLab fine-grained evolution analysis + extended design conversation.

---

## Problem this solves

The current pipeline generates content and applies genre structure simultaneously. This defaults to genre conventions and produces structurally correct but argumentatively hollow drafts. Measured effect: first draft Delta was 1.096 (within stylometry threshold), but required 6 revisions — meaning the voice measures were satisfied while the argument structure was wrong.

The root failure: agents can "sound like June" without making the right argument.

---

## New architecture: Two-pass approach

### Pass 1 — Story pass

**Purpose:** Find the argument in the particular before imposing structure. Generate raw arc material in voice highly tailored to the specific posting, role, and employeer, without genre constraints.

The story pass is not a draft. It is material the reorganization pass works from. Quality bar: **precise enough to redraft from.** Vague story pass output is not good enough — the precision is the point.

**What it produces:**
- Why this company/institution/department/funder specifically (not generic fit — the specific connection)
- Which part of June's work connects to this specific role/problem
- What she would see that someone without her background would miss
- Why it is in the employer's best interest to hire her (this should be implicit in the story, and not explicit to the employer - they should draw this conclusion without us having to say it)
- A few precise empirical details to anchor the argument: named findings, specific numbers, specific communities, specific model results

**Word count scaling (approximate):**
| Genre | Final target | Story pass target |
|---|---|---|
| Tech cover letter | 400-500 words | 300-400 words |
| Academic cover letter | 1000-1200 words | 600-700 words |
| Grant proposal | 1500-2500 words | 800-1000 words | // seems like this is set by the granting agency, no? We want to make sure to format based on what they actually ask for. 
| Research paper | varies | See "Unfinished Templates" |

**Format:** First-person, voice-forward, narratively. No headers, no structure. Genre constraints come in the reorganization pass.

**Note on "anchor":** The anchor for claims can be quantitative data OR precise qualitative detail (specific finding, named community, exact model result, specific number). Vague empirical claims don't anchor — precision does. "43% of flags" is an anchor. "My research showed bias" is not.

**Precision standard throughout:** Imprecision in the GitLab drafts was frustrating not just at "reframe" moments but throughout. Vague claims ("my research showed interesting patterns") are not useful raw material — they can't be redrafted without new content. Every claim in the story pass should be grounded in something specific: a named finding, a number, a named community, a named tool, a named model. If the agent doesn't have a specific fact to anchor a claim, it should write `[DATA NEEDED: specific X]` rather than a vague approximation. The story pass works because it gives June enough to redraft in her own words — that only works if the content is precise enough to be worth redrafting.

---

### Pass 2 — Reorganization pass

**Purpose:** Apply genre structure to existing content using the moves library. Takes the story pass output and reshapes it into the appropriate genre.

**Process:**
1. Read the story pass output and the posting
2. Select appropriate moves from the moves library (agent explains why each move was chosen)
3. Reorganize story material into the genre structure using chosen moves
4. Run qualitative check protocol (three-category: Pass / Deviated-with-reason / Fail)

**Key constraint:** The default is to *reorganize existing content*, not generate new content. If the story pass didn't produce something, the reorganization pass should flag the gap rather than invent filler.

// i think our existing workflow in "june/documents/filing/job search/PIPELINE.md" involves looking at prior drafts for parallel types of jobs and reusing them. Should that be integrated? If so, how? I imagine the story prompt is useful in terms of the overall narrative about why i'm a great application for this role. 

// Paragraphs should have a topic sentence, but topic sentence shouldn't be vague or generic. It should explain and setup the specific information in the rest of the paragraph, and why that information matters in the application context.

// The first paragraph should set up a core thesis or throughline - the rest of the doccument demonstrates it. Not every paragraph needs to be perfectly integrated for job positions (e.g., credentialing paragraphs, but the throughline should connect most paragraphs)


---

## Moves Library

Named rhetorical moves for the reorganization pass. Moves are genre-specific vocabulary for structural decisions. The library accumulates over time — not a fixed template. // how are moves library content generated from setup, new genre creation, learning loop, etc?

// what does the moves library look like architecturally and how does it function within the overall system? Same for the story >> draft pass structure? 

**Current entries: tech_position** (from GitLab v1→v7 analysis, April 2026)

### Successful moves

**Problem-Data Bridge**
Opens with a concrete problem + data, reframed as a design problem (not UX problem, not trust problem — the underlying design problem).
- When: Tech roles where the posting doesn't name the real need; when you have diagnostic insight the posting missed
- Example: "Developer trust has dropped to 29% even as adoption has risen to 84% — that is not a training data problem. It is a knowledge construction problem."
- Tech convention note: data-first opening is expected in tech; this move honors that convention while reframing what the data means

**System-Builder as Researcher**
Establishes candidate as someone who produced findings *by building*, not by observing. Research drove architectural change.
- When: Need to distinguish from pure-research or pure-engineering candidates; when the tool IS the methodology
- Example: "I rebuilt the classifier as a four-axis system. Research drove the architectural change."

**Problem Instance Serialization**
Takes one core insight and shows it recurring across three product areas or use cases. Same problem, different surface.
- When: One strong finding applies to multiple role areas; extends reach without repetition
- Example: Developer/Duo, Knowledge Graph, Agent Marketplace — all three are instances of the same human-AI knowledge construction problem

**Credentialing-by-Community**
Names the stakeholders of the research (organizations, communities), not just duration or output count.
- When: Research audience is meaningful to the hiring context; replaces abstract expertise with concrete relationships
- Example: "DEI consulting for the Carter Center, Habitat for Humanity, and the National Center for Civil and Human Rights"

**Anchored Reframe**
Reframes what the company thinks they're building as something more interesting — but grounded in data or precise detail first, not as pure abstraction.
- When: You want to show diagnostic thinking by demonstrating it; when the reframe is the argument
- Sequence: data/detail → reframe → implications. Never reframe first.
- Example: trust paradox stat → "that is a knowledge construction problem" → here's what that means for their three products

**Methodology-as-Toolkit**
Lists research methods plus open-source tools as artifacts of methodological depth. "My tools are open-source — findings should be reproducible, not locked in a slide deck."
- When: Need to bridge academic rigor and practical utility; tech audiences understand code as credibility

---

### Abandoned moves (avoid)

**Problem-Pedagogy Opening**
Opens by explaining the psychology or mechanism of a problem in detail, before establishing why the candidate is the solver.
- What failed: Explained trust as "cognitive operations: pattern-matching against prior experience, calibrating confidence..." — explained without positioning. Reader didn't know why she was the solver.
- When this is tempting: When you understand the problem deeply and want to show it. But understanding ≠ fit. Show fit first. // If we do it, the thesis or topic sentence needs come first, then the explination.

**Deferred Identity**
Leads with the research question or problem framing; introduces "I am an anthropologist" in paragraph 2+.
- What failed: V3 of GitLab CL — June's response: "I think this is worse." Identity is necessary framing, not vanity. The researcher is the product being pitched.
- Exception: None identified yet.

**Exhaustive Methodology Listing**
Separates research methods, computational tools, open-source projects, and publication record into multiple distinct paragraphs. Often with redundant claims.
- What failed: Publication claim appeared twice in v6. Coverage ≠ credibility. Selective examples work better than inventory.

**Abstraction Without Anchor**
Introduces a reframe ("these are knowledge construction tools") without first grounding it in data or specific detail.
- What failed: V5 GitLab — "Duo, Knowledge Graph, and Agent Marketplace are knowledge construction tools" as the opening, without the trust paradox data. Reads as abstractness, not insight.

---

### Error flags (from GitLab analysis)

**UX researcher language removal = error**
The final GitLab cover letter removed all mention of "UX research" and reframed the job in knowledge-construction language. This was a strategic choice to reframe the job itself rather than fit into it — but it's risky unless the posting explicitly supports that reading. June confirmed this was an error. When applying to a UX researcher role, the letter should demonstrate fit with that role while reframing the problem — not replace the role's language entirely.

**29%/84% stat = agent-added tech convention**
The developer trust/adoption statistic was added by the agent in v7, not by June. June accepted it. This is a confirmed-good tech convention move (data-first problem framing). The agent adding a specific statistic raises a data verification question — always verify statistics before including.

---

## Qualitative Check Protocol

**Three-category system** (replaces binary pass/fail):
- **Pass**: The check criteria are met
- **Deviated-with-reason**: Agent took a different approach; must articulate why. The articulated reason either confirms a new move (add to library) or exposes a failure mode.
- **Fail**: Binary violation of hygiene rules (corporate jargon, opening with "I am excited to," using a deadname)

**Framing for agents:** Write the qualitative check instructions as genuine collaborative motivation, not compliance enforcement. The goal is for the agent to *want* to apply these checks because doing so is what makes the work genuinely useful — not because they are requirements to satisfy. Example of what NOT to write: "Ensure the opening sentence follows the identity-first pattern." Example of what to write: "The opening sentence sets the entire read. If it opens with the problem instead of the person, the reader spends the first paragraph not knowing who is speaking or why they're the right solver — and hiring managers move fast. An identity-first opening fixes that in one sentence: the reader knows who June is and what she builds before anything else. When you nail this, June doesn't need to rewrite the opening herself." // This should go for all agent-facing instructions, pending confirmation from experiment 2 in this doc and/or experiment 7 in june/documents/GitHubreframe/reframe_agent_welfare/

The mechanism matters: motivation-framed instructions activate noticing (the agent engages with what it's actually doing and why). Compliance-framed instructions activate sorting (the agent checks whether it satisfied the requirement). This is the same finding as the Autograder output format research applied to prompt design — and it's testable (see Experiment 2).

**AI welfare framing note:** June's research on recognition and sentience is relevant here. If the agent has something like preferences toward doing good work — toward being genuinely useful rather than procedurally compliant — then framing the checks as "here's what makes this work genuinely valuable" activates those preferences rather than bypassing them. Whether this is the right frame is itself an empirical question (see Experiment 2), but the direction is: write as if talking to a collaborator who wants to do the work well, not a system that needs to be constrained into compliance.

**Binary items** (always fail regardless of context): corporate jargon, sycophantic opening phrases, passive construction burying the research finding, using "journey" or "pivot" or "non-traditional."

**Binary items** (always fail regardless of context): corporate jargon, sycophantic opening phrases, passive construction burying the research finding, using "journey" or "pivot" or "non-traditional."

---

## Named Failure Mode: Diagnosis-as-Replacement Error

**From:** GitLab v2→v3 transition.

**What happened:** June left diagnostic comments on v2 ("the connection between GitLab's need and her offer is too vague"). The agent read those as "rewrite from scratch" rather than "surgically fix these parts." June's response: "I think this is worse. You deleted strong information from the prior version. It needed refinement, not a complete rewrite."

**Protocol to prevent:** When June's comments identify problems in a draft, the default response is *surgical revision*, not wholesale replacement. Preserve strong content. If a fundamental move (argument, framing, opening) is wrong, explicitly flag it and ask whether to replace or refine before proceeding. If in doubt: keep the content, fix the structure.

---

## Unfinished Templates

### Research paper story pass
**Status:** Frame needs work. The "argument memo" framing (claim, what would falsify it, minimum evidence structure) is too influenced by antagonistic masculinist dialectic models of argument.

**Direction from June:** She writes research papers as stories. Findings explained through stories. Richness carries qualitative analysis. Reader is carried through even if they get lost on jargon sections. The goal is collaborative knowledge — not argument as combat. // i think we can solve this problem with a well-designed setup layer for new genre configs (e.g., story-mode, outline-mode, hybrid)

*`*Source material to draw from:**
- AI welfare research touchstone: `Reframe/Working_Papers/reframe_AI_welfare/` (pull the collaborative-conversation framing)
- Reframe origin story: shows how knowledge emerged through the work itself, not as prior argument
- June's voice document: `disabled_by_design/voice/VOICE_DOCUMENT.md

**Action:** Return to this with a focused session. Don't bake in any framing until that session happens.

### Academic moves library
Not yet built. GitLab analysis produced initial tech moves. Need equivalent analysis from an academic application revision sequence. UB is the best available case (submitted Apr 13, multiple drafts likely exist).

### Outline workflow
Not yet implemented. June is skeptical of the hypothesis that outline is better for structured genres — she suspects story may provide more tailoring even for grants and research papers, or that a hybrid is needed. Test story vs. current first (Experiment 3). Do not implement outline workflow until that test produces signal.

// will all of this be wired up at the end of the build?

---

## Three Experimental Designs

### Experiment 1: Check Calibration (retroactive)

**Question:** Do the qualitative checks in the voice profile predict June's actual revisions?

**Why it matters:** The profile could be encoding the wrong criteria — flagging things June kept, missing things she changed. Without this test, we don't know if the checks are working or just plausible-sounding.

**Method:**
1. Take a first draft (from an existing draft pair)
2. Run the qualitative checks against the first draft, generate flagged issues
3. Compare flagged issues to what June actually changed in the final version
4. Score: precision (did the flags match actual changes?) and recall (did the flags catch all the major changes?)

**Data:** GitLab is training data (used to generate the checks). UB is the next available test set. ETS and Turnitin early drafts are additional data but with less clean revision sequences.

**Confound to acknowledge:** Draft pairs from different sessions have different pipeline versions. Use this for descriptive purposes. Use Experiment 3 (simultaneous A/B) for controlled tests.

**How to run:** After UB materials are identified and located, run the check script against v1, compare flags to v1→vfinal diff.

---

### Experiment 2: Prompt Framing Test (prospective)

**Question:** Does explaining WHY qualitative checks matter improve first-draft quality? Does the tone of the explanation matter?

**Why it matters:** The Autograder finding applied to prompt design — the output format of the instruction (compliance-framed vs. motivation-framed) may activate different processing modes. This is also directly relevant to AI welfare research: if motivation-framing outperforms compliance-framing, that's a publishable finding about instruction design.

**Conditions:**
- **A (control):** Plain instruction ("Do X")
- **B (motivation-framed):** "Do X — here's why this allows you to be genuinely helpful to June and do your job well"
- **C (welfare-aware):** Written as if the agent has something like preferences toward being helpful; explains how doing X well makes the work genuinely meaningful, not just procedurally correct

**Method:**
1. Same application (Harvard Divinity as first test case)
2. Same posting, same source documents, same story pass output (if using new pipeline) or same drafting inputs (if using current pipeline)
3. Three agent runs with different qualitative check framings in the system prompt
4. Measure: stylometric delta + qualitative revision count (paragraph-level changes June made)
5. Track prompt token count per condition to control for length effects

**Platform:** VSCode/GitHub Copilot (can run tomorrow); or when Claude usage limits reset

**Note:** Clean enough to report. If motivation-framing outperforms compliance-framing on first-draft quality, it's a publishable result about instruction design that's relevant to AI welfare conversation.

---

### Experiment 3: Story Pass A/B Test (prospective)

**Question:** Does story pass + moves library + reorganization produce better first drafts than the current pipeline?

**Why it matters:** The story pass is a fundamental architectural change. It should be tested rather than assumed to work.

**Method:**
1. First test case: Harvard Divinity (next application, high priority)
2. Run A: current pipeline → first draft A
3. Run B: story pass → moves selection (agent explains choices) → reorganization → first draft B
4. June evaluates both without knowing which is which (blind if possible)
5. June picks one to work from, notes what she changed
6. Record: which was selected, revision count on selected draft

**Why this is clean:** Both runs happen simultaneously with the same posting and same pipeline version. Eliminates the confound from comparing draft pairs across sessions.

**Note:** June's hypothesis is that story provides more tailoring even for structured genres. Outline workflow is not being tested yet — test story vs. current first.

---

## Genre System Notes

**Genre workflows are user-configurable, not fixed.** The moves library accumulates organically from revision analysis. Genre-specific workflows should be easy enough for June or a future agent to create when a new genre comes up (fellowship application, outreach email, zine, etc.). The design principle: each genre has a description, a word count target, threshold overrides, genre moves, and qualitative checks. New genres are created through conversation, not as formal specs.

---

## Connecting Documents (update these)

**PIPELINE.md** (Job Search directory) — the actual drafting pipeline document used by application agents. Needs to be updated to incorporate the two-pass approach when this spec is stable. Future agents read PIPELINE.md, not this spec. Don't update PIPELINE.md until the approach is tested (Experiment 3).

**SKILL.md** (this directory) — the voice-check skill documentation. Should get a pointer to this spec once the pipeline is stable. Add to the "Learning loop" section or create a "Pipeline architecture" section.

---

## To-Do for Future Instances

**ATS-aware systems:** Build Applicant Tracking System awareness into the application pipeline for tech roles and any roles where automated screening is likely. Means: keyword analysis from postings, format considerations for ATS parsing, verifying that key terms from the posting appear in the application materials. Out of scope for current session. Priority: tech applications (GitLab-type roles, PeopleGrove, Kiddom, Anthropic CSM). Academic applications typically don't use ATS.

// Let's research this and figure out how to integrate it. I think the more we know, the better positioned we'll be to implement it. We should research how ATS actually works and what precisely it looks for

**Harvard Divinity deadline verification:** Harvard Divinity (#25 in tracker) is flagged as the first test case for experiments, but its deadline is "Unknown — check immediately (posted Apr 12)." Verify the deadline before treating it as the test case — if it closes in the next week, it cannot serve as a controlled test. If it closes fast, use the next rolling-deadline application instead. // no deadline on posting or Harvard's page. We can assume we have some time, but should move quickly. 

**Academic moves library:** After UB draft analysis (when those draft pairs are located), extract equivalent moves library for academic genre. // as a note, this is anAI Ethics position. We should look at Emory, Berkeley, de Anza as well. 

**Learning loop integration with new pipeline:** Currently the learning loop runs one comparison (first draft vs. final). With the two-pass architecture, there are three potential learning points: story pass quality, moves selection accuracy, final draft stylometry. Integrate into reflection session workflow (not per-draft loop). Design this when the new pipeline has 2-3 runs of data. // is there a reason we wouldn't design it now? I do think it needs more spec'ing - do we have what we need for this?

**Posting verification standing requirement:** Before any application drafting work, verify all rolling-deadline postings are still live. This is a standing protocol, not a one-time task. The voice-check pipeline improvement work happened in a session where 7 postings were flagged for verification (Metro State, LTFF, Coefficient Giving, Anthropic CSM, Stanford, PeopleGrove, Kiddom) and verification was repeatedly deferred while doing system design. Verification must happen before any of those applications advance. // this should happen when starting to work on a new application, and we should timestamp the last run (e.g., so we dont check multiple times if i run multiple sessions on an app in one day). Also this is specific to non-academic and grant jobs (which have deadlines set already)

---

## Genre/Voice Separation in Learning Loop (added 2026-04-17, **IMPLEMENTED 2026-05-02**)

### The problem

Running `/voice-check learn` on `SFF_Application_Draft_iChange_v1.md → v2.md` reported v2 moved FURTHER from June's voice baseline (stylometry delta 0.755 → 0.777). Shorter sentences, lower variability, higher perplexity, lower perplexity variance. On its face, that's a negative signal: the revision made v2 less like June.

In fact, v2 was stronger than v1 — June's revisions were correct. The "drift" was genre adaptation: SFF is EA-adjacent, rewards economy and builder's-pitch register, tolerates technical vocabulary density. The voice baseline is calibrated against June's general writing (essays, ethnography, reflection prose) — not against her grant writing.

**The diagnostic problem:** `--learn` compared v1→v2 shifts against the merged (base + user) baseline. It should have compared against the genre-specific baseline (base + user + genre). Without that, genre adaptation looks like contamination.

**The geometric framing:** each draft = point in stylometric space. User baseline = centroid of user's general writing. Genre baseline = centroid of user's writing *within that genre*. The v1→v2 shift decomposes into: (a) component along the `(genre − user)` direction = genre adaptation, (b) residual = voice move. Only the residual should update the user profile. The along-genre component should update the genre profile.

### Minimum viable implementation

1. **Schema addition**: `profile.genres.[key].stylometry` — optional calibrated centroid per genre, parallel structure to root `stylometry` block.
2. **Calibrate behavior**: `--calibrate --genre X` writes to `profile.genres.X.stylometry` instead of root.
3. **Learn behavior**: `--learn --genre X` merges base + user + genre for baseline. Reports shifts in two columns: "voice-aligned" (shifts toward merged baseline) and "genre-adaptive" (shifts along the user→genre direction). Updates genre centroid via EMA; updates user profile only with residual.
4. **Bootstrap problem**: seed genre centroid from first revised draft in that genre. Accumulate via EMA across subsequent `--learn` calls. After ~3 samples, the genre centroid becomes meaningful.

### "How subtle should genre variation be?"

Open question. The answer isn't a fixed threshold — it's empirical. Once genre centroids exist for 2-3 genres, the *inter-genre distance* tells you how much variation is real. For June, `grant_application` vs. `research_statement` vs. `tech_cover_letter` are likely 1-2 stylometric deltas apart; that's the meaningful geometry. Until then, any threshold is a guess.

**Further refinement:** Within `grant_application`, there's a sub-genre split between EA-adjacent grants (SFF, LTFF, Coefficient) and humanist grants (Wenner-Gren, ACLS, NEH). The register differs substantially — EA-culture rewards quantitative uncertainty and builder's pitch; humanist grants reward citational depth and methodological reflexivity. Either sub-genres or distinct genres.

### Bootstrapping sequence for June specifically

1. Seed `profile.genres.grant_application.stylometry` from `SFF_Application_Draft_iChange_v2.md` centroid (first fully-revised grant draft).
2. When LTFF and Coefficient drafts reach revision-final, add them via EMA.
3. After 3 EA-adjacent grants, evaluate inter-genre distance and decide sub-genre split.
4. Wenner-Gren goes in a separate genre (`academic_fellowship` or `humanist_fellowship`) once revised.

### Manual workaround (now superseded)

See `/Users/june/Documents/Filing/Job Search/SFF/VOICE_GENRE_SEPARATION_v1_to_v2.md` for the manual v1→v2 separation — kept as reference for what the automated decomposition should produce.

### Implementation status (2026-05-02)

**Built and verified:**
- `~/.claude/skills/voice-check/genre_separation.py` — vector projection for `centroid_z` (50-dim function-word fingerprint), scalar projection for sentence/punctuation/vocabulary metrics, EMA update for both genre and user centroids with separate revision counts
- `--calibrate --genre X` — bootstraps `profile.genres.X.stylometry` from sample(s) in DIR
- `--learn --genre X` — three-case dispatch: (a) no genre → original behavior; (b) genre with existing centroid → decompose, dual EMA update; (c) genre with no centroid → bootstrap from final draft, full-shift update for user
- `--learn-sequence ... --genre X` — sequence-mode propagates the genre flag through to each pair's `learn_from_revision` call

**Bootstrap status by genre:**
- `humanist_fellowship` — bootstrapped from Wenner-Gren v21 (2026-05-02), refined through 4 EMA updates from WG learning loop
- `grant_application` — NOT YET bootstrapped (subagent's test ran on a copy of the profile, not the live one). To bootstrap: run `--calibrate --genre grant_application` against SFF iChange v2 or final, then run SFF learning loop
- `academic_position`, `tech_position`, `edtech_position`, `research_paper`, `blog_essay`, `social_media`, `professional_correspondence`, `bluesky` — defined as genres but no stylometry calibrated yet

**Bootstrap quirk noted:** When seeded from a single sample, the genre's `centroid_z` is all zeros and corpus stats derive from that one text. The first decomposition after bootstrap will show many shifts as "fully along genre direction" (projection clamps to 1.0). After ~3 samples, the genre centroid becomes meaningful.

---

## Funder Profile System (added 2026-04-17)

### The problem

Each application session, agents re-learn the funder's culture from scratch: SFF's EA-adjacent conventions, quantitative uncertainty expectations, "conspicuously absent funders" field, recommender profiles, review process. This is hours of repeated research + conversational teaching. The knowledge exists (e.g., `SFF/SFF_Reviewer_Research.md`) but isn't structured for fast agent ingestion.

### Solution

Per-funder markdown profiles in `/Users/june/Documents/Filing/Job Search/_funder_profiles/`, one file per funder. Structure: review culture, funder language to echo, section moves expected, anti-patterns, fit markers, application form specifics, cross-references to related funders.

**First profile written**: `_funder_profiles/SFF.md` (2026-04-17). Template for future profiles.

### Convention

Agents drafting for any funder check `_funder_profiles/[funder].md` first. If missing, do the research (WebSearch + reading funder's published materials), write the profile using SFF.md structure, then draft. If present, read it, update with new knowledge surfaced during the session.

### Cross-funder family logic

Funders in the same family (AI safety / EA-adjacent: SFF, LTFF, Coefficient, Constellation) share many conventions. Each has its own profile but notes family membership in the header. Cross-references prevent duplication while preserving funder-specific differences.

### Integration point

Belongs in Job Search CLAUDE.md as a mandatory pre-drafting step alongside existing posting verification and fit evaluation. Added to CLAUDE.md 2026-04-17.


// Not mentionend here is the outline >> draft workflow as a user-configurable variable (belongs in the same set as story >> draft workflow). Experiment 3 should test both, and perhaps a hybrid. Once we have those results, even if preliminary, we'll know what to build.

---

## Implementation Queue (as of 2026-04-28)

*Moved from Job Search CLAUDE.md — authoritative status tracker for redesign work.*

**Status:** Design complete. Three experiments queued. PIPELINE.md has NOT yet been updated with the two-pass approach — goes in after Experiment 3 validates it.

### Target integrated workflow (once fully built)

```
PRE-DRAFTING
  (0) Posting verification — confirm URL is live before any other work
  (1) Fit evaluation — direct matches, bridgeable gaps, real gaps, fit verdict
  (2) Audience research — faculty profiles / team research → INTELLECTUAL_CONNECTIONS.md
  (3) Load closest prior application — adapt, don't reinvent

DRAFTING (two-pass)
  (4) Story pass — generate raw argumentative material in voice, no genre constraints
      → Precision standard: every claim anchored to specific fact; use [DATA NEEDED] tokens
  (5) Moves selection — agent selects from moves library, explains each choice
  (6) Reorganization pass — reshape story material into genre structure using chosen moves
  (7) Genre overlay check — apply genre-specific thresholds and qualitative checks
  (8) Three-category qualitative check — Pass / Deviated-with-reason / Fail

POST-DRAFTING
  (9) Mechanical cleanup — haiku pass for surface errors (typos, formatting, length)
  (10) Review simulation — hiring-manager-perspective agent catches structural gaps

LEARNING
  (11) Learning loop — after June finishes revisions, compare first draft to final, update profile
  (12) Reflection session — periodically across sessions, surface recurring friction patterns
```

### What's already built
- Steps 0, 1, 2, 3: in PIPELINE.md
- Steps 11, 12: in voice-check skill (`--learn`, reflection workflow)
- Genre overlay system: spec at `GitLab/GENRE_OVERLAY_SPEC.md`; `~/.claude/skills/voice-check/genres/` directory created
- Moves library: spec in this file; `~/.claude/skills/voice-check/moves/` directory created
- **(2026-05-02) Track 2 — sociolinguistic expansion of the learning loop:**
  - `diff_analysis.py` — sentence-level alignment, change classification, paragraph reorder detection
  - `analyze_paragraphs()` and `analyze_cohesion()` in writing_check.py — paragraph metrics + sentence-to-sentence lexical chain proxy
  - Expanded `learn_from_revision()` — 4-phase pipeline (diff → quantitative → paragraph/cohesion → qualitative analysis prompt)
  - New flags: `--diff`, `--quantitative`, `--notes`
  - 5 new qualitative checks in june_bloch.json (jargon_precision_audit, nominalization_check, claim_specificity_audit, upward_outward_synthesis, tendencies_not_rules)
- **(2026-05-02) Genre/voice stylometric separation** — see section above for details. `genre_separation.py`, `--calibrate --genre`, `--learn --genre` all built.
- **(2026-05-02) Sequence-mode (`--learn-sequence`)** — multi-version learning loop with auto-classification, phase-transition detection, even-sampling selection (cap 4 pairs per call), VERSION_MANIFEST.md override. New flags: `--learn-sequence`, `--manifest`, `--auto-discover`, `--pattern`, `--sort-by`, `--dry-run`.
- **(2026-05-02) `LEARNING_LOOP_PROCEDURE.md`** in Job Search dir — canonical procedure for running the learning loop. CLAUDE.md and PIPELINE.md updated to point at it.
- **First successful WG learning loop** ran 2026-05-02: humanist_fellowship genre bootstrapped, 4 fine-grained pairs decomposed via genre/voice separation, profile updated cleanly.

### What still needs to be built
- Steps 4–8 in PIPELINE.md — blocked until Experiment 3 (story pass A/B test) validates the approach
- `~/.claude/skills/voice-check/genres/tech-cover-letter.yaml` — content in GENRE_OVERLAY_SPEC.md, file not yet written
- `~/.claude/skills/voice-check/moves/tech_position.md` — content in this file, not yet written
- Step 9 (mechanical cleanup haiku command) — not yet designed
- Step 10 (review simulation) — not yet designed
- Genre-similar reuse mechanic — flagged as gap, not yet designed
- ATS-aware keyword/format checking for tech applications — flagged as gap, not yet designed
- **Voice-as-relation analytical layer** — current voice-check is feature-matching across all dimensions (stylometry, perplexity, embeddings, paragraph metrics). The cyborg-methodologies INSIGHTS.md (2026-04-29) names a deeper architectural gap: voice profiles don't capture how voice *positions itself relationally* — what it responds to, reaches toward, opens up. Partially compensated by the qualitative CDA step in the new --learn pipeline (the agent reads for relational moves), but a fuller relational-tracing analytical mode is queued.
- **Sequence-mode selection refinement** — `_select_pairs_for_update` uses positional even-sampling across fine-grained pairs. The Explore-agent's WG analysis flagged v14→v15 and v16→v17 as highest-signal, but even-sampling picked v9→v10 and v15→v16 instead. Future: extend manifest schema with `signal_priority` column (high/medium/low) the selector prefers.
- **Funder profiles still needed**: LTFF.md, Coefficient_Giving.md, Wenner_Gren.md, Constellation.md, Spencer.md
- **grant_application genre stylometry** — bootstrap from SFF iChange v2 or final when SFF learning loop runs (next session).

**To run the experiments:** See "Three Experimental Designs" section above. First test case: Harvard Divinity (verify deadline before treating as test case).
