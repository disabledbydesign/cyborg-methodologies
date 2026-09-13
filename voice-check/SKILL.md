---
name: voice-check
description: "Voice integration for human-AI collaborative writing. Maintains a sociolinguistic voice profile that agents read BEFORE drafting (style guide that shapes what gets written) AND self-run AFTER drafting (contamination linter), plus a learning loop that improves the profile from human revision patterns. Both the pre-draft read and the post-draft check are first-class uses — voice-check is not a post-only tool. Run /voice-check setup to create a profile from writing samples. Run /voice-check learn after a revision session to update the profile."
user_invocable: true
trigger: |
  Invoke BEFORE drafting voice-carrying material for the user (READMEs, portfolio copy, fieldnotes, touchstones, social media, application materials, anything written in the user's voice for an external audience) — load the profile plus the matched genre overlay, then draft in voice.
  Invoke AFTER drafting to run the contamination linter on the produced text.
  Also invoke when the user runs /voice-check, /writing-check, or asks to check a draft's voice.
---

# Voice Check — Agent Voice Integration

Voice-check is a sociolinguistic voice profiling system for human-AI collaborative writing. It does three things:

1. **Style guide** — Agents read the voice profile before drafting and write in the user's voice from the start. The profile captures how the writer actually writes: sentence rhythm, punctuation habits, vocabulary density, function word patterns, register, argumentation style, and what they never sound like.

2. **Contamination linter** — After drafting, the agent self-runs quantitative checks and silently corrects contamination patterns (hedge words, corporate jargon, narrative padding, self-aggrandizing frames). The user sees a clean draft, not a report of what's wrong with it.

3. **Learning loop** — After the user revises a draft through conversation, the system compares the agent's first draft to the human's final version. It identifies what shifted and updates the voice profile so future drafts are closer. The human's revision choices are the ground truth for what their voice IS.

The user never needs to run a voice check to generate fixes. The agent uses the profile to write well and learns from how the user edits.

## Quick reference

| Command | What it does |
|---|---|
| `/voice-check setup` | Create your voice profile from writing samples (auto-runs on first writing task if no profile exists) |
| `/voice-check learn` | After a revision session: full learning loop (diff + quantitative update + qualitative CDA sweep) |
| `/voice-check reflect` | Periodic reflection: review patterns across sessions, propose profile updates |
| `/voice-check [file]` | Optional: run standalone diagnostic on any document |

**Script flags (direct invocation):**

| Flag | What it does |
|---|---|
| `--learn FIRST FINAL` | Full learning loop — diff analysis, quantitative update, qualitative analysis prompt |
| `--learn-sequence v1.md ... vN.md` | Multi-version learning loop with auto-classification of structural vs. fine-grained transitions |
| `--diff FIRST FINAL` | Structural diff only — no profile update; useful for inspecting version pairs |
| `--quantitative FIRST FINAL` | Quantitative analysis only — prints deltas, no profile update |
| `--audit-diagnostics` | Read-only report on `diagnostic`-role checks: last-cited dates, citation counts. Auto-triggered when a diagnostic check has been silent for 5+ runs. |
| `--log-cited-checks ID1,ID2,...` | After Phase 4 CDA sweep, log which check IDs fired during revision. Appends to most recent citation log entry. Without this, citation log is mostly heartbeat. |
| `--notes "text"` | Add intent note to a --learn run (e.g., "structural pass" or "fine-grained finalization") |
| `--genre GENRE` | Apply genre-specific thresholds to any command |
| `--profile PATH` | Specify profile when multiple exist |

## Paths

- **Script**: `~/.claude/skills/voice-check/writing_check.py`
- **Profiles**: `~/.claude/skills/voice-check/profiles/`
- **Base profile**: `profiles/base.json` (universal norms, ships with the skill)
- **User profiles**: `profiles/[username].json` (personal overrides, built through calibration)

---

## Architecture: Three layers

The profile system has three layers that merge at load time:

**Universal base** (`base.json`) — Ships with the skill. Contains patterns, thresholds, and qualitative checks that work for any English writer. Catches AI contamination (hedge words, corporate jargon, padding) and flags structural issues (front-loaded sentences, weak argument progression). Permissive thresholds — catches obvious problems without false-flagging diverse styles.

**User profile** (`[username].json`) — Built through calibration from the user's own writing samples. Contains only what differs from or adds to the base: tighter thresholds calibrated to this writer's patterns, additional anti-patterns specific to this voice, prescriptive qualitative checks that encode this writer's preferences (e.g., "lead with consequence, not authority"), and computational fingerprints (stylometry, perplexity, embeddings).

**Genre overrides** (within the user profile) — User-defined document types. Each genre can override thresholds (grants tolerate hedging; social media needs short sentences) and add genre-specific qualitative checks. The skill ships with no genres — users create their own through conversation.

Merge order: **base → user → genre**. User thresholds override base. Genre thresholds override the merged result. User patterns extend base patterns (concatenated). User qualitative checks with the same ID as a base check replace it; new checks are appended.

### Role schema (qualitative checks)

Each qualitative check carries a `role` field that determines who reads it and when. The schema:

| Role | What it is | Who reads it | When |
|---|---|---|---|
| `pre_draft` | Principle that shapes what gets written | Drafting agent, in flight | Before and during drafting |
| `linter` | Pattern/threshold rule fired automatically by the script | The script | After drafting (auto) |
| `cda_sweep` | Prompt for interpreting revisions | CDA agent during `--learn` | Learning loop qualitative phase |
| `diagnostic` | Rare situational flag for a tendency | Mixed | Surfaces only when triggered |

The role schema exists because earlier versions of this profile had ~44 mixed-role checks that all looked the same to a reader. Agents drafting were burning ~29K tokens to extract the ~7-10 principles that actually shape what gets written. Filtering to `pre_draft` drops the in-flight read by ~70% without losing any load-bearing guidance.

### Progressive disclosure for genres

Genres are the second axis of progressive disclosure. The profile may contain 10+ genre blocks, but **agents draft in one genre at a time**. Reading every genre's block when only one applies is the same kind of waste as reading every role's checks. Loading all genres typically costs ~10K tokens; loading just the matched genre typically costs under 1K.

The protocol for agents (see step 3 of agent integration): identify the genre BEFORE reading the rest of the profile. Then read only the matched genre's block (`description`, `threshold_overrides`, `genre_moves`, `qualitative`). Skip other genres entirely. If the genre is ambiguous, ask the user before reading rather than reading all of them. The chunking choice (which genre to load) is itself an analytical commitment; treat it as a lens, not infrastructure.

### Theoretical anchors

A profile may include a `theoretical_anchors` field listing the scholarly frameworks the qualitative checks operationalize. This exists because individual check instructions can't fully convey the framework they instantiate — and fresh-context agents have no session memory of the calibration sessions where the frameworks were discussed. The anchors include `for_fresh_agents` briefings designed to activate training data on each named work. See agent integration protocol step 2.5 for use.

---

## Drafting principle: relational tracing, not similarity clustering

When drafting connections between ideas, sections, cases, or pieces of evidence — especially in multi-section documents (grants, papers, statements, books) — the AI's default pattern-matching pulls toward similarity. Twin-finding. What's-like-what's-here. Lateral feature-matching: "section A is X, and section B is also-X-but-different."

Route against this. The move that makes a multi-project document feel integrated rather than four separate projects in a trenchcoat is **configurational**, not thematic: same operation traceable across registers, not shared surface features.

**What to do instead.** When you reach for a connector — between two sections, two cases, two scholars, two scenes — ask what's *connected to* / *taking up* / *talking to* / *picking up from* the artifact, not what's like it. Trace the relational field around the artifact rather than its twins.

- Lateral (default, wrong): "Section A foregrounds X. Section B also foregrounds X, in a different domain."
- Configurational (right): "The claim from Section A is being TAKEN UP in Section B, at a different site, doing different work. What Section A opened, Section B is picking up."

Generation test: if the connector sentence would still hold after swapping the second case for any other case sharing the same surface theme, it's lateral. If it depends on this specific second case picking up what this specific first case opened, it's configurational.

For depth on what this routes against, see the cyborg-methodologies memos: `cgt-skill/memos/010_gravities_to_route_against.md` (similarity pattern-matching → dialogic relation), `016_openings_and_takings_up.md` (the openings/takings-up move), `022_routing_through_constructivist_subdistributions.md` (lexical priming as sub-distribution selection — using "takes up" / "opens" / "picks up from" in prompts and prose activates the right register).

---

## Agent integration protocol

**This is the primary content of this skill.** Any agent helping with writing should follow this protocol.

### Before drafting

1. **Check for voice profile.** Look in `~/.claude/skills/voice-check/profiles/` for non-base JSON profiles. If exactly one exists, use it. If multiple exist, ask which one. If none exists, offer to run setup (see Setup section). If only `base.json` exists, you can still draft using universal norms — just note the writing won't be personalized.

2. **Identify genre BEFORE reading the rest of the profile.** Genre selection is usually obvious from context ("help me with this cover letter" → the user's cover letter genre). If ambiguous, ask the user — don't read every genre's block to figure it out. If no matching genre exists, offer to create one (see Genre Creation below) or use base thresholds. Identifying genre first is what enables progressive disclosure on the read in step 3.

3. **Read the profile, filtered by role AND genre.** Load the profile JSON (the script auto-merges base + user layers). Apply two filters:

   **Role filter on `qualitative[]`** — each check carries a `role` field; filter to what's load-bearing for the work in front of you:
   - **`role: "pre_draft"`** — principles that shape what gets written. **Read these in full before drafting.** This is the in-flight reference set (~30 checks; ~10K tokens).
   - **`role: "revision_pass"`** — *(added 2026-08-07)* judgment work an agent performs **during revision**: restructuring, deep compression, re-sequencing. **Read these when revising, not when drafting.** Not script-firable — these require a model to execute, and no regex can do them. This role exists because the taxonomy previously had no home for agent-executed revision work: everything was either read-before-drafting, script-fired, learning-loop, or rare-situational. `williams_diagnostic_restructure` had been filed under `linter` for want of anywhere better, which meant the script never fired it (it can't) and agents were told not to read it. It was invisible to the entire system. If a check describes work a model must do and a script cannot, it belongs here.
   - **`role: "linter"`** — pattern/threshold rules fired automatically by the script. Don't read manually. ⚠ Genuinely mechanical rules only. If you find yourself tagging something `linter` because it doesn't fit elsewhere, it is probably `revision_pass`.
   - **`role: "cda_sweep"`** — prompts for the learning loop's qualitative phase. Read only when running `--learn`.
   - **`role: "diagnostic"`** — rare situational flags. Read when triggered.

   **Genre filter on `genres`** — read ONLY the genre block matching what you identified in step 2. Skip every other genre's block. The full `genres` field across 10+ genres can total ~10K tokens; the matched genre is typically <1K. Loading other genres is the same kind of waste as loading non-pre_draft checks — fix it the same way.

   For the matched genre, read all of: `description`, `threshold_overrides`, `genre_moves`, and `qualitative` (if present, even cda_sweep/linter/diagnostic checks specific to this genre — they're scoped narrowly enough to be relevant when drafting in this genre).

   Drop into a non-pre_draft check's full instruction only when something specific in the draft warrants the deepening.

   Also read:
   - `stylometry.style_notes` — plain-language summary of the writer's voice fingerprint
   - `theoretical_anchors` (if present) — frameworks the checks draw from. See step 3.5.
   - `patterns` — anti-pattern lists tell you what words are contamination signals (the script catches these post-draft, but recognizing them while drafting prevents the contamination)
   - **The moves library — `~/.claude/skills/voice-check/moves/`.** Added to this list 2026-08-07; the directory had existed since April and nothing in this skill pointed at it, so the moves were written and then never read. Each file states its scope in a `**Genres:**` header line.
     - **Files tagged `ALL`** are universal craft moves — Williams' given/new contract, topic placement, de-nominalization, the throat-clearing deletion test, concision. **Read these before drafting anything, in any genre.** They are the operationalization of the Williams anchor named in step 3.5: the anchor tells you the framework exists, these tell you what to do with it. (Five were tagged `gra-memory-creation` until 2026-08-07 because they happened to be written during that genre build — a scoping accident, not a judgment that they were project-specific. June: *"Williams style craft should be for ALL writing."*)
     - **Files tagged with specific genres** apply only when drafting that genre. Skip the rest, on the same logic as the genre filter above.
     - A move file carries the *reasoning* behind a craft rule, which a one-line profile check cannot. Where a `qualitative` check and a move file cover the same ground, the move file is the fuller account.

3.5. **Activate theoretical anchors.** If the profile has a `theoretical_anchors` field, it lists scholarly frameworks the qualitative checks operationalize (e.g., Martin & White's Appraisal Theory, Williams's *Style: Lessons in Clarity and Grace*, Halliday's Systemic Functional Linguistics). Each anchor includes a `for_fresh_agents` field with a short briefing on the framework. **Before drafting, briefly review your training data on each named anchor.** The qualitative checks are operationalizations of these frameworks — activating the frameworks gives you context the individual check instructions cannot fully convey.

   **Why this matters (motivation, not enforcement):** activating the frameworks before drafting produces a better first draft. Better first draft = fewer rounds of revision the user has to do = more of their time available for everything else. The most efficient way to draft is to do the best possible job on the first attempt, not to draft fast and patch later. Every Williams violation caught at draft time is one less the user has to fix. Every contamination pattern named by a framework you've activated is one you can recognize and avoid in flight, not just have flagged after the fact. Treat anchor activation as the small upfront investment that earns back many rounds of editing — for you, for the user, for the work.

   This is especially important for fresh-context agents with no session memory of prior calibration sessions: you literally don't know the framework grounding without activating it, and the individual check instructions can't carry the full theoretical context.

4. **Fact assembly — load specific factual material before writing.** Voice profile alone is not enough. The recurring failure mode in agent drafting is theoretical scaffolding padding generic claims, because the specific facts (scenes, dates, names, quotes, ethnographic details, findings) weren't loaded into context. Before drafting, sketch what each section needs to do, locate the source documents that ground each section's claims, and read those sources INTO context — not summaries, the actual prose with the specific details. Where the user's project has source-material registries (e.g., a `SOURCE_MATERIALS.md` indexing file paths to primary documents), use them to find sources without re-searching. When a needed fact has no available source, ask the user — do not fabricate plausible detail. Then draft from assembled facts, with theory cited doing work on specific cases — not name-dropped to suggest engagement. The pipeline a writing project lives in (e.g., `PIPELINE.md` for a job-search workflow) may specify a "Fact assembly" step with project-specific source registries; follow it. Without fact assembly, agents produce text that sounds plausible but doesn't land for readers — it gestures at engagement without engaging.

   **Pulling from prior similar work.** When adapting from a prior similar document or project, **pull from the most recent submitted/final version**, not an earlier draft. Look for, in order: (1) `*_final.md` or similarly-named final markdown; (2) the submitted PDF or HTML artifact (these reflect the final state — extract their prose into a working markdown); (3) the highest-numbered `vN.md` if no explicit final exists. **Do not start from `draft_v1.md` or `v1.md` if more recent versions exist.** Failure mode this prevents: an agent adapts the wrong prior version (an old draft instead of the submitted final), and the new draft is already a partial regression before any work begins. The agent that submits a final document should also write a clean `*_final.md` to the project folder so future agents pulling from this work have an unambiguous source to use.

### During drafting

4. **Write in the user's voice.** Use the style notes and qualitative checks as active guidance, not just post-hoc criteria. Match their sentence rhythm, vocabulary register, argumentation style, and relationship with the reader. Avoid everything in the anti-pattern lists. When drafting connections between sections, cases, or scholars, use **relational tracing** (what TAKES UP what), not similarity clustering (what's LIKE what) — see "Drafting principle: relational tracing" above.

5. **Self-check after drafting.** Run the quantitative analysis on your own output:
   ```bash
   python3 ~/.claude/skills/voice-check/writing_check.py DRAFT_PATH --genre GENRE_NAME
   ```
   The script auto-discovers the user's profile if only one exists. Use `--profile PATH` to specify if multiple profiles exist. If `--genre` is specified and the genre defines a `word_count_target`, that target is used automatically.

   **The same command also runs Vale**, if Vale is installed and a `.vale.ini` sits anywhere above the draft. Its findings arrive in a `MECHANICAL RULES (Vale)` section of the same report — one command, two engines. Nothing extra to invoke. If Vale is missing the report says so in one line and everything else runs normally.

   What each engine owns, and why the line falls where it does: **Vale checks whether a fixed string or a fixed syntactic shape is present** (copular/cleft constructions, nominalizations, forbidden claims, hedges, corporate register). **voice-check owns everything with a number attached** — counts measured against a threshold, stylometric distance from the corpus centroid, the genre overlays, the learning loop, and the qualitative checks that are prompts for a model. The reason is structural, not philosophical: Vale rules are static files selected by file glob, and voice-check thresholds change per genre (`hedge_max` is 0 for a tech cover letter and 4 for a research paper). Vale cannot see which genre a draft is being written in, because the genre is an argument to this script, not a property of the path.

   So when a Vale rule hard-codes a threshold voice-check also measures, the report suppresses Vale's copy and says so. Findings the profile lexicons already produced are likewise suppressed rather than printed twice. Vale alerts are counted separately in the summary and are never folded into the flag arithmetic, which is calibrated against the user's corpus.

   Useful flags: `--no-vale` skips the pass; `--vale-config PATH` overrides config discovery; `--vale-audit` reports which of the profile's pattern lexicons the Vale rules do **not** cover. Run `--vale-audit` after the learning loop adds patterns to a profile — the profile grows and the static rule files do not, and that audit is the only thing that notices.

6. **Self-correct contamination silently.** If the check flags voice contamination (hedge words, corporate jargon, narrative padding, self-aggrandizing frames, product-description appositives), fix them before presenting the draft. These are binary contamination signals — "leveraging" is wrong in any voice. Do not tell the user you found and fixed contamination. Just present clean text.

7. **Honestly assess quality before presenting.** Before showing the draft to the user, assess its quality per section. Name what's strong and what's weak. For example: "The opening paragraph is strong — identity-first, specific. The research section has several front-loaded sentences that put new concepts before the reader is oriented. The fit section announces alignment rather than demonstrating it through intellectual engagement." Do not default to "this looks good." AI-generated text defaults to positive self-assessment because the training distribution rewards reassurance. Resist that pull — the user needs accurate assessment to make revision decisions.

8. **Surface structural/qualitative findings as suggestions.** If the check flags structural issues (long sentences, em-dash density, front-loaded subjects) or if you notice qualitative concerns from the checklist, mention them as suggestions the user can accept or reject. These are judgment calls, not automatic fixes. Frame as: "I noticed X — want me to adjust, or is that intentional?"

### Pre-submission QC pass

8.5. **Before submission, re-review every `pre_draft` check against the final draft.** This is the moment to catch principles that drifted during revision — checks that fired correctly during initial drafting may have been compromised by later edits, especially structural reorganization. A few checks are particularly prone to this kind of late drift (e.g., `cross_document_awareness` — does the final draft re-explain anything covered in the cover letter or research statement? Did a paragraph the user added accidentally duplicate a frame from another document in the application?). Walk through each `pre_draft` check, ask whether the final text honors it. Flag anything ambiguous to the user before they submit. This step is light — minutes, not hours — but it catches the failures that are most expensive to fix after submission.

### After revision

9. **Offer the learning loop at session end.** When the user finishes revising a document (the conversation is wrapping up, or they say they're done), ask: "Want me to run the learning loop? I'll compare my first draft to your final version and update the voice profile so I draft closer to your voice next time."

10. **Run the learning loop — full 4-phase pipeline.** The `--learn` command runs structural diff, quantitative update, paragraph/cohesion metrics, and outputs a qualitative analysis prompt. Always use the writer's `.md` source, NOT a rendered `.html` (HTML markup contaminates the metrics).

   ```bash
   python3 ~/.claude/skills/voice-check/writing_check.py --learn FIRST_DRAFT.md FINAL_DRAFT.md [--notes "intent"]
   ```

   The four phases:

   - **Phase 1 — Diff analysis.** Sentence-level alignment classifies each sentence as preserved, light edit, substantial rewrite, deleted, or added. Detects paragraph reordering. Output identifies whether the revision pattern is `STRUCTURAL` (paragraphs moved/added) or `LOCAL` (sentence-level edits dominate).
   - **Phase 2 — Quantitative update.** Stylometry, perplexity, embeddings updated via EMA. Same as the previous learning loop behavior.
   - **Phase 3 — Paragraph + cohesion metrics.** Compares paragraph counts, sentence-per-paragraph distribution, topic-sentence weight (first-sentence word counts), landing weight (last-sentence word counts), and sentence-to-sentence lexical chain density (cohesion proxy). Flags low-cohesion adjacent sentence pairs — these are potential connectivity breaks.
   - **Phase 4 — Qualitative analysis (agent responsibility).** The script prints a structured CDA prompt. The agent must then read both files in full and perform the sweep at clause/sentence, paragraph, and document levels. **Editorial discipline applies: the profile should sharpen with each loop, not grow.** The Phase 4 prompt asks for the *smallest set of profile changes* — additions, deletions, merges, or rephrasings — that would have caught the deliberate revision moves. Treat addition as the option of last resort, after rephrase and merge are ruled out. New additions must specify role at insertion; if `pre_draft`, they must name what existing pre_draft check they replace (the in-flight set is capped — additions force tradeoffs). Present proposed changes to the user for approval before updating the profile.

     **For accepted additions and significant rephrasings, append an entry to `~/.claude/skills/voice-check/PROFILE_CHANGE_LOG.md`** with: source diff snippet (quoted, not summarized), rationale, role, and a question for the next audit. Merges and cuts don't require log entries (they reorganize existing rationale rather than create new). The change log handles rationale drift; the citation log (auto-maintained) handles firing-frequency drift. Together they cover both kinds of system entropy without the user needing to remember to audit.

   - **Citation tracking (automatic + agent-supplemented).** Every `--learn` and `--learn-sequence` run scans its analysis output for check IDs and appends to `~/.claude/skills/voice-check/citation_log.json`. The script's text scan is narrow — it sees what was printed during the run, not the agent's post-script CDA analysis. **After your Phase 4 sweep, log the check IDs you actually cited:**
     ```bash
     python3 ~/.claude/skills/voice-check/writing_check.py --log-cited-checks transitivity,no_announcement_fragments,bookend_opening_frame
     ```
     This appends the IDs to the most recent run's entry. Without this step, the citation log is mostly a heartbeat and DIAGNOSTIC REVIEW auto-trigger has no real signal. **Always run `--log-cited-checks` after Phase 4** if you identified any check IDs as firing during the revision. When a `diagnostic`-role check has been silent for 5+ runs, the next learn report surfaces a "DIAGNOSTIC REVIEW DUE" prompt naming the silent checks. Run `--audit-diagnostics` to see the full diagnostic-status report and decide whether to keep, demote, or cut.

   **Workflow note for structural vs. local revisions.** When the diff pattern is `STRUCTURAL`, weight sentence-level signals lower in the qualitative analysis — they often reflect collateral damage from reorganization, not deliberate voice choices. Fine-grained refinement passes carry the strongest voice signal at the sentence level. The optional `--notes` flag lets the user tag the run's intent ("structural pass," "fine-grained finalization," etc.) so the agent reads the signals in context.

   **v0/v1 auto-copy — run immediately after producing the first draft, before the revision conversation starts:**
   ```bash
   cp [doctype].md [doctype]_v0.md && cp [doctype]_v0.md [doctype]_v1.md
   ```
   Example: `cp cover_letter.md cover_letter_v0.md && cp cover_letter_v0.md cover_letter_v1.md`

   v0 = raw agent output, never modified. v1 = working copy for the revision conversation. The learning loop's signal is the gap between v0 and the final submitted version — that's what teaches the profile what the agent got wrong at the sentence level. If v0 is missing and June has already revised v1, the baseline is contaminated.

   **HTML-final sync:** If June makes final sentence-level edits in the HTML before exporting to PDF, sync those back to markdown before running the learning loop. Save as `[doctype]_final.md` by extracting the body text. The loop always uses `.md` — stale markdown means missing exactly the fine-grained pairs that carry the most voice signal.

   **Standalone tools:**
   - `--diff FIRST FINAL` — runs only the structural diff (no profile update). Useful for inspecting version pairs before deciding whether to run the full loop.
   - `--quantitative FIRST FINAL` — runs the full pipeline output WITHOUT updating the profile. Useful for sanity-checking a revision pair, or for runs where you want to see the metrics but the pair isn't representative enough to update the profile (e.g., genre-divergent applications).

11. **VERSION_MANIFEST (optional, recommended for multi-version applications).** When an application goes through many drafts (more than 3-4), maintain a `VERSION_MANIFEST.md` in the application folder mapping each version transition with type and intent:

   ```markdown
   | From | To | Type | Author | Intent |
   |------|-----|------|--------|--------|
   | v3 | v4 | structural | AI | Three-axis framework introduction |
   | v5 | v6 | fine-grained | user | Voice preservation pass |
   | v14 | v15 | fine-grained | user | Framework-collapse beat insertion |
   ```

   The manifest disambiguates valuable signal (intentional voice choices in fine-grained passes) from noise (sentence-level changes that fall out of structural reorganization). When choosing which pairs to run `--learn` on, the manifest tells you which are highest-signal — fine-grained pairs after the architecture has settled.

12. **For multi-version applications: use `--learn-sequence`.** When an application has gone through 5+ versions, don't run `--learn` pair by pair. Use:

   ```bash
   python3 ~/.claude/skills/voice-check/writing_check.py --learn-sequence v3.md v4.md ... v21.md [--genre G] [--manifest VERSION_MANIFEST.md] [--dry-run]
   ```

   The script auto-classifies each transition as structural or fine-grained, detects the phase transition where architecture settled, and applies EMA updates only on the fine-grained pairs (capped at 4 per call to avoid over-weighting one application). Use `--dry-run` first to verify the classification before writing to the profile.

   For folder-based discovery:
   ```bash
   python3 writing_check.py --learn-sequence --auto-discover FOLDER --pattern "APPLICATION_DRAFT_V*.md" --sort-by name [--genre G]
   ```

   The classifications are heuristic — verify against your own memory of the revision sessions, and use `--manifest` to override when needed. The auto-classifier errs on the side of "structural" for ambiguous cases (safer to skip than over-weight a structural pair). When the trajectory report flags a pair as structural that you remember as fine-grained refinement, add it to the manifest and re-run.

---

## Setup

Setup creates the voice profile. It runs automatically the first time an agent starts a writing task and no profile exists — the user does not need to remember a command.

If the user explicitly runs `/voice-check setup`, follow this same flow.

### Prerequisites

```bash
pip install textstat nltk
```

Optional (for richer fingerprinting): `numpy`, `scipy` (stylometry), MLX + local model (perplexity), `fastembed` (embeddings). The tool degrades gracefully — each module is optional.

### Step 1: Gather writing samples

Ask the user for 1-3+ samples of writing in the voice they want to maintain. More is better, but even one substantial piece works. These should be:
- **Their own revised/final writing** (not first drafts, not AI-generated text)
- **Writing they're proud of** — this is the voice to protect
- **Across genres if possible** — samples from different document types give a richer fingerprint

**File formats**: `.md`, `.txt`, `.html`. For Google Docs: File > Download > Plain Text. For Word: Save As > Plain Text. For PDF: copy-paste into a `.txt` file.

Save all samples to a single directory. If the user pastes text directly, save each to a temp `.md` file.

### Step 2: Quantitative calibration

```bash
python3 ~/.claude/skills/voice-check/writing_check.py --calibrate PATH_TO_SAMPLES/ -o ~/.claude/skills/voice-check/profiles/USERNAME.json
```

This generates a sparse user profile that references `base.json`. It analyzes the writing samples and stores only thresholds that differ from the base defaults. It also runs stylometry calibration and any other available modules.

### Step 3: Qualitative voice extraction

**You (the agent) read ALL the writing samples in full and extract the writer's voice characteristics.** The user does not do this part.

**A. Voice characteristics** — analyze the samples for:
1. Sentence-level mechanics: length, rhythm, punctuation habits
2. Lexical choices: register, terminology, vocabulary density
3. Argumentation style: evidence-first, authority-first, narrative, consequence?
4. Relationship with reader: direct, institutional, authoritative, collegial?
5. What they do NOT sound like: what would be wrong? What patterns would contaminate this voice?

**B. Anti-patterns** — based on the voice analysis, write regex patterns and add to the profile's `patterns` section. These extend the base contamination patterns with writer-specific additions.

**C. Qualitative checks** — build user-specific checks based on what you found. The pattern: identify something distinctive about how this person writes, then write a check that protects it. Add these to the profile's `qualitative` section. They supplement (or override) the base checks.

### Step 4: Genre configuration

Walk the user through creating genres for the document types they write. This is a guided conversation, not a form — explain each parameter in plain language.

**For each genre, walk through:**

1. "Describe this kind of writing in a sentence. Who reads it? What's the tone?"
2. "How long are these documents usually? A rough range is fine."
3. "Some genres need longer, more complex sentences — academic papers, for instance. Others need short and punchy. Should I give you more room on sentence length for this genre, or keep it tight?"
4. "In some writing, cautious language is appropriate — 'this approach has the potential to...' is expected in grant proposals but sounds weak in a blog post. For this genre, is some hedging OK?"
5. "What sections or moves does this kind of document need? For example, a cover letter usually needs: who you are, why this role, evidence, closing. What are the pieces for yours?"
6. "Is there anything specific to watch for in this genre that wouldn't apply elsewhere?"

Translate the user's answers into the genre JSON structure. The user never sees or writes JSON unless they want to.

If the user isn't sure about genres, skip this step. Genres can be added later. The base thresholds work for any document.

### Step 5: Verify and activate

Run the tool on ONE of the user's own good writing samples:
```bash
python3 ~/.claude/skills/voice-check/writing_check.py GOOD_SAMPLE --genre LIKELY_GENRE
```

What to look for:
- **Few or no voice flags** — if their own good writing triggers contamination flags, the patterns are too aggressive. Adjust.
- **Reasonable structural flags** — some long sentences in good writing is fine. If many, thresholds may be too tight.
- **Zero flags is suspicious** — thresholds may be too loose to catch AI contamination. Tighten.

Show the user the results and adjust until the profile correctly distinguishes their voice from generic AI output.

Tell the user:
- Where the profile lives
- That agents will use it automatically during writing tasks
- That running `/voice-check learn` after revision sessions makes the profile better over time

---

## Genre system

Voice is largely stable across genres — function word frequencies, punctuation habits, vocabulary richness don't change between a cover letter and a research paper. What changes is **register**: threshold tolerances, expected structural moves, and which concerns are appropriate for the audience.

### Genres are user-defined

The skill ships with no genres. Users create their own based on the kinds of documents they write. A tech writer might have `api_docs`, `blog_post`, `release_notes`. An academic might have `journal_article`, `grant_proposal`, `conference_abstract`. A job seeker might have `cover_letter`, `research_statement`, `teaching_statement`.

### Genre structure

Each genre lives in the user profile's `genres` section:

```json
{
  "genre_key": {
    "description": "What this genre is and who reads it",
    "word_count_target": 1200,
    "threshold_overrides": {
      "hedge_max": 3
    },
    "genre_moves": ["section_1", "section_2", "section_3"],
    "qualitative": [
      {
        "id": "genre_specific_check",
        "category": "structural",
        "name": "Check name",
        "instruction": "What to check and why"
      }
    ]
  }
}
```

### How genre selection works

1. **Agent infers from context.** "Help me draft a blog post" → the user's blog genre.
2. **Explicit selection.** The user says which genre, or specifies `--genre blog_post`.
3. **No match found.** Offer to create a new genre, or use base thresholds.
4. **Fallback.** If no genre is specified or inferable, base thresholds with a 1200 word count default.

When a genre is selected:
- Its `threshold_overrides` merge on top of the user's thresholds (genre values win)
- Its `word_count_target` becomes the default (overridden by explicit `--target`)
- Its `genre_moves` guide structural analysis
- Its `qualitative` checks run in addition to universal + user checks

---

## Reflection sessions

The learning loop (`--learn`) captures what the user revised in a single draft. Reflection sessions capture patterns across multiple writing sessions — recurring friction, systematically underdefended areas, and connections between problems at different levels.

### When to run

After sessions with significant revision friction, or periodically after several writing sessions. The user says "let's reflect" or "review recent sessions" or the agent offers at a natural breakpoint.

### Workflow

1. **Scope the reflection.** Ask the user which sessions or documents they want to analyze. Don't assume scope. "Which writing sessions do you want to look at? Any specific friction you noticed?" The user directs what's in scope.

2. **Gather artifacts.** For the scoped sessions, collect: learning loop reports, draft-to-final pairs, session notes. Ask the user to point at files or describe what happened if artifacts aren't obvious.

3. **Name the friction.** Identify specific problems from the material. For each:
   - What happened? (The sentences were front-loaded. The agent said "really good" and it wasn't. The equity statement reinvented content from the teaching statement.)
   - What type? Syntax-level, genre-level, argument-level, workflow-level?
   - Structural or incidental? Would it happen again with the same profile, or was it specific to this session?
   - Already addressed? Is there a check in the profile that should have caught this?

4. **Find connections.** Do friction points cluster? Is there a level consistently underdefended? Did the existing profile prevent problems it was designed for? Present findings to the user — the agent surfaces patterns, the user makes judgment calls about which connections hold.

5. **Compare to profile.** For each structural friction point:
   - If already addressed: why did the check fail? (Enforcement — agent didn't follow it? Specificity — instruction too vague? Coverage — instruction covers a different case?)
   - If not addressed: draft a targeted addition. One check, one pattern, or one threshold adjustment.

6. **Update the user profile.** New qualitative checks, new patterns, adjusted thresholds. All updates go in the user profile — never modify `base.json`.

7. **Optionally test.** Run voice-check on a recent draft to verify the fix catches the pattern.

### Key principle

The agent surfaces patterns and proposes. The user makes judgment calls about what gets changed. Agent presents findings, then asks — doesn't conclude.

---

## Revision mode

Revision is a distinct mode of work from drafting-from-scratch. The agent enters revision mode when the user is editing an existing draft — pasting passages with directed changes, asking for fine edits, working line-by-line through a document. Revision-mode protocol applies in addition to the drafting protocol, not instead of it.

### Recognize the mode

Signals: user pastes existing prose and asks for edits; user references "the V3" or "the prior version"; user is iterating on specific sentences rather than commissioning new sections; user's feedback is granular ("this sentence isn't landing") rather than structural.

### Show before apply

Default to **propose change → wait for confirmation → apply.** Not auto-apply. When you see the change you want to make, write the proposed replacement and stop. Let the user confirm. Auto-applying overwrites work the user may want to keep, and short-circuits the iteration the revision is for.

Exception: trivial mechanical fixes (typos, contamination words from the patterns list, an obvious grammar error in a passage the user has already approved) can be applied without checking. Anything that changes meaning, reorders, or rewrites a sentence the user composed gets shown first.

### Mine prior versions before retranslating

A user's profile may have included a `mine_prior_versions` qualitative check in earlier versions. The principle is encoded here as a workflow rule, not a text-pattern check. Enforcing it requires a workflow step.

When revising a passage:
1. **Locate prior versions.** Look in the project for V1/V2/V3, REVISED files, prior session drafts. Ask the user if you can't find them.
2. **Check whether the passage you're about to rewrite was already worked.** If a prior version had a sharper sentence than what you're about to draft, paste it forward rather than retranslating.
3. **Translation introduces errors and loses tested phrasings.** Reuse what worked.

### Verify source claims; flag uncertainty rather than fabricating

When revising prose that makes specific factual claims (a date, a quote, an event detail, an ethnographic specific), do not invent supporting detail to make the prose flow. If the source isn't in context, flag the uncertainty: "I don't have a source for the [specific detail]. Want me to leave it general, or can you confirm?" Plausible-sounding fabricated detail is the failure mode here — it reads as authoritative and is wrong.

### Resist optimism creep when source material is despair-coded

The base contamination patterns catch corporate optimism ("transformative," "groundbreaking"). They do not catch the subtler hope-creep that surfaces when an agent is reporting on dark ethnographic conditions or political crisis. The pattern: the source material is grief, foreclosure, or despair; the agent's revision restores forward motion or hope without the prose having earned it.

When the source register is despair-coded, flag any sentence in the revision that introduces forward motion, possibility, or repair that wasn't present in the source. Surface as a question: "I added 'but the work continues' here — the source didn't have that. Keep it or cut?"

This is also encoded as a `linter`-role qualitative check (`resist_optimism_creep`) that fires on any draft, not just during revision.

### Affect before reasons when affect is the analytical foreground

When affect is the analytical foreground (the chapter is about a felt condition; the section's analytical claim depends on the reader registering the affect), lead with the affect statement. The list of structural reasons follows. Reversing this — leading with the structural reasons and arriving at the affect — turns the affect into a consequence to be derived rather than a condition to be inhabited.

Example: "People felt hopeless." should come BEFORE the list of reasons people had to feel hopeless, not after.

This is also encoded as a `pre_draft`-role qualitative check (`affect_before_reasons`) that fires on any draft.

### Configurational orientation sentences in multi-project documents

Section transitions in multi-section documents (grants, papers, books) can do orientation through configurational connection rather than meta-discourse. The default-bad move is meta-discourse: "The book's second register is X." The agent reaches for this because it's the statistical center of academic transition writing.

The configurational alternative names what the new section TAKES UP from the prior section, at a different site, doing different work. This sounds like the document moving forward through its own argument, not like a table of contents being narrated.

See "Drafting principle: relational tracing" for the underlying move; this is the section-transition application of it.

---

## Diagnostic mode (optional)

For standalone analysis of any document — writing not produced through a Claude drafting session, or when the user wants to explicitly check a piece.

```bash
python3 ~/.claude/skills/voice-check/writing_check.py PATH_TO_DRAFT [--genre GENRE] [--target WORDCOUNT]
```

The script auto-discovers the profile. Use `--profile PATH` if multiple profiles exist.

### Quantitative analysis

Read the output. Note all flags. Voice flags (hedges, jargon, padding) indicate contamination. Structural flags (long sentences, em-dash density, front-loaded subjects) may be deliberate style.

### Qualitative analysis

Load qualitative checks from the merged profile. Run each against the draft text. Checks marked prescriptive should be enforced; checks marked diagnostic should be noted and reported.

### Report format

```
VOICING REPORT: [filename]
Profile: [profile name]
Genre: [genre name or "base"]

QUANTITATIVE (from writing_check.py):
[key metrics and flags]

QUALITATIVE (analysis):
[findings organized by ideational/interpersonal/textual/structural]

SUGGESTIONS:
[specific, actionable — "Consider rewriting line X with Y pattern"]
```

Suggestions, not directives. The user decides what to act on.

---

## Additional voice dimensions

These modules extend the voice fingerprint beyond stylometry. Each adds a section to the user profile, participates in calibration (`--calibrate`) and learning (`--learn`), and degrades gracefully when its dependencies aren't installed.

### Perplexity scoring (requires MLX + local model)

Measures per-sentence perplexity via a local language model (`perplexity.py`). Human writing has higher and more variable perplexity than agent-generated text. The "surprise profile" captures how predictable the writer's sentences are.

- **Style guide**: `perplexity.style_notes` tells the agent how "surprising" the user's writing tends to be
- **Learning**: compares perplexity distributions between first and final draft
- **Default model**: `mlx-community/Qwen2.5-1.5B-4bit`
- **Install**: `pip install mlx mlx-lm`

### Embedding similarity (requires fastembed)

Sentence embeddings capture semantic drift (`embeddings.py`) — when the agent writes about the same topic but in a different conceptual register.

- **Style guide**: `embeddings.style_notes` describes semantic consistency
- **Learning**: embeds first-draft and final-draft sentences, updates centroid via EMA
- **Default model**: `BAAI/bge-small-en-v1.5` (384-dim, ONNX via fastembed)
- **Install**: `pip install fastembed`

### RST structural coherence

Implemented as qualitative checks in the base profile (argumentative progression, claim-evidence binding, coherence vs. cohesion, nucleus-satellite relationships). No separate module — these are checklist items that agents evaluate during qualitative analysis.

---

## Reference

### Profile schema: base.json

```json
{
  "profile": {
    "name": "Universal Base",
    "version": "1.0",
    "description": "Universal English writing norms"
  },

  "patterns": {
    "hedge_words": ["regex patterns..."],
    "self_aggrandizing": ["..."],
    "topic_sentence_starters": ["..."],
    "logical_connectors": ["..."],
    "narrative_padding": ["..."],
    "corporate_jargon": ["..."]
  },

  "thresholds": {
    "long_sentence_words": 45,
    "rewrite_sentence_words": 60,
    "long_sentence_max": 6,
    "rewrite_sentence_max": 3,
    "emdash_per_1000w": 20,
    "emdash_insertion_words": 12,
    "hedge_max": 2,
    "self_aggrandizing_max": 0,
    "topic_opener_max": 3,
    "logical_connector_max": 5,
    "narrative_padding_max": 0,
    "product_description_max": 0,
    "corporate_jargon_max": 0,
    "wordcount_over_pct": 115
  },

  "qualitative": [
    {
      "id": "check_id",
      "category": "ideational|interpersonal|textual|structural",
      "type": "prescriptive|diagnostic",
      "name": "Human-readable name",
      "instruction": "What to check and why — self-contained, no jargon"
    }
  ]
}
```

### Profile schema: user profile

```json
{
  "base": "base.json",

  "profile": {
    "name": "Writer Name",
    "version": "3.0",
    "created": "2026-04-14",
    "calibrated_from": "N writing samples",
    "description": "Voice profile description"
  },

  "patterns": {
    "hedge_words": ["additional patterns beyond base..."],
    "custom_category": ["user-specific patterns..."],
    "_disable": {
      "corporate_jargon": ["pattern to remove from base"]
    }
  },

  "thresholds": {
    "hedge_max": 0,
    "long_sentence_words": 40
  },

  "qualitative": [
    {
      "id": "same_id_overrides_base_check",
      "category": "ideational",
      "name": "Prescriptive override",
      "instruction": "User-specific instruction replaces base diagnostic"
    },
    {
      "id": "new_user_check",
      "category": "textual",
      "name": "User-only check",
      "instruction": "Check that only applies to this writer"
    }
  ],

  "genres": {
    "genre_key": {
      "description": "...",
      "word_count_target": 1200,
      "threshold_overrides": {},
      "genre_moves": [],
      "qualitative": []
    }
  },

  "stylometry": { "...": "calibrated from writing samples" },
  "perplexity": { "...": "if MLX available" },
  "embeddings": { "...": "if fastembed available" }
}
```

### Merge behavior

When a user profile references `"base": "base.json"`:
- **Patterns**: base lists + user lists per category. `_disable` entries removed.
- **Thresholds**: base values, then user overrides on top.
- **Qualitative**: base checks first. User checks with same ID replace; new IDs appended.
- **Genres/stylometry/perplexity/embeddings**: from user profile only.

### Thresholds quick reference

Base defaults (permissive starting point). User profile tightens these. Genre overrides adjust per document type.

| Metric | Base default | Type | What it catches |
|---|---|---|---|
| Word count | >115% of target | structural | Bloated drafts |
| Sentences >45 words | >6 per doc | structural | Runaway sentence length |
| Sentences >60 words | >3 per doc | structural | Sentences that need splitting |
| Em-dash insertions >12 words | any | structural | Em-dash clauses doing too much work |
| Em-dashes per 1000w | >20 | structural | Em-dash overuse |
| Hedge words | >2 | contamination | Agent-typical hedging |
| Self-aggrandizing | >0 | contamination | Inflated framing |
| "This is" openers | >3 | contamination | Relational process overuse |
| Logical connectors | >5 | contamination | Mechanical transitions |
| Padding phrases | >0 | contamination | Filler that adds no content |
| Product descriptions | >0 | contamination | Appositive sales language |
| Corporate jargon | >0 | contamination | Words the writer would never use |
| Front-loaded subjects | >2 per doc | structural | New concepts forced into subject position |

**Contamination flags** are diagnostic of agent-generated text — the agent self-corrects these silently. **Structural flags** may reflect deliberate style — surface as suggestions.
