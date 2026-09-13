# Genre config: other (meta-config)

**Sources:** printpress SKILL.md (cross-genre Stages, learning loop surfaces, "other" accumulation), printpress SPEC § Genres + § Learning loops Tier 2 ("other" promotion), Job Search CLAUDE.md (file-finding via working-dir CLAUDE.md)
**Updated:** 2026-05-07
**Status:** v1 — meta-config; not a workflow per se

---

## What this is

`other` is the genre `/printpress` lands on when invocation doesn't match the four named genres (`academic_position`, `non_academic_application`, `grant_fellowship`, `peer_review`). This file is a **meta-config**: it tells the skill how to *handle* unknown genres by deriving a temporary working config in conversation with the author.

Most of the cross-genre defaults from `SKILL.md` apply directly — Stages 0, 1, 2, 4, 4.5, 5 use the cross-genre frame, scaled by the formal parameters of the artifact. What's genre-specific in the four named configs (required Stage 0 files, Stage 3 swarm composition, Stage 5 save conventions) gets derived through Stage 0 conversation with the author rather than read from this file.

---

## When this genre applies

- The author invoked `/printpress` and the artifact doesn't match the four named genres (e.g., a teaching dossier intro, a public-facing op-ed, a workshop materials packet, a foundation cold-outreach email, a sabbatical report, a tenure dossier, an obituary, a podcast pitch, a syllabus statement, a manifesto)
- The author invoked `/printpress other` explicitly
- State detection (per SKILL.md § Invocation) finds an artifact that doesn't fit existing genre patterns

If the artifact looks like it might fit a named genre, ask before defaulting to `other` — a borderline academic-statement-of-purpose is closer to `academic_position` even if the structure is unusual.

---

## Stage 0: Data-in (genre-specific)

Stage 0 is where the meta-config does its work. Use the dialogic capability (per SKILL.md § Cross-cutting capabilities) — usually quick-scan, occasionally deep dialogic if the artifact is novel and high-stakes.

### Surface the dialogic question to the author

Open with a structured set of options. Use AskUserQuestion (per UX_STUB § UX principles):

> What kind of artifact is this?
> - **An existing genre under an unusual name** — pick from `academic_position`, `non_academic_application`, `grant_fellowship`, `peer_review`. Skill switches to that genre config.
> - **A genuinely new genre.** Skill builds a temporary working config in conversation. Logged for promotion candidate review (per SKILL.md § Learning loop surfaces).
> - **A one-off** — use the cross-genre defaults from SKILL.md, no new config logged.

If the author picks an existing genre → switch to that config; this file's work is done.

If the author picks a one-off or new genre → continue below.

### If author names a new genre or one-off, surface the structural questions

Five questions, asked one at a time (one-thing-at-a-time, per UX_STUB § UX principles):

1. **What is this artifact?** Genre name, document type, length, format. ("A 2-page foundation cold-outreach letter," "a 30-page tenure dossier intro," "a 600-word op-ed for *Truthout*.")
2. **Who reads it?** Specific reader / panel / audience. Reviewer composition for Stage 3 derives from this answer.
3. **What's the formal structure?** Word/character limits, required sections, required content elements. Like APPLICATION_STRUCTURE.md for grants — what's non-negotiable formal parameter, what's creative space.
4. **Where do source materials live?** Existing drafts, source docs, voice-final priors of similar work the author has done before, briefing context. Same file-finding protocol as the named genres (working-dir CLAUDE.md → parent → ask).

   **Content accuracy gate (for content work about a specific project or repo):** If the artifact's content depends on factual accuracy about a project — what it does, what it found, what design decisions were made — Stage 0 is not complete until the primary source materials for that project have been *read*, not inferred. Do not proceed to Stage 1 on likely/probable content. Read the fieldnotes, design logs, or session records that are the source of truth. What was actually built, decided, or found may differ substantially from what seems likely from summaries. This is especially critical for social media and public-facing content where overclaiming is both easy and damaging.
5. **What's the closest matching genre we have?** Even if it's not a fit, the closest named genre tells us which conventions to lean against and which to break. ("Closer to grant_fellowship than academic_position because the audience is a panel, but the prompts aren't structured.")

**Output:** capture answers in `[ProjectFolder]/DRAFT_PLAN.md` under a "Working genre definition" section. This becomes the temporary working config for this invocation.

### What this Stage 0 produces

A temporary working config that names:
- Required Stage 0 files (POSTING-equivalent, source materials registry, prior-work lookup)
- Reviewer composition for Stage 3 (who reads it; what personas instantiate)
- Formal/conventional parameters for Move 3 (formal structure, conventions to work with or against)
- Save / tracker conventions for Stage 5 (where the final artifact lives, what gets archived, what reminders trigger)

Most of these will be light — `other` invocations are typically lower-stakes than named genres or are one-offs. Don't over-engineer.

### Append to other_log.md (always)

After Stage 0, append an entry to `~/.claude/skills/printpress/other_log.md`:

```
## [Date] — [Artifact name / project folder]
- **Author-named genre:** [from question 1]
- **Reader / audience:** [from question 2]
- **Formal structure:** [summary from question 3]
- **Closest matching named genre:** [from question 5]
- **Working config decisions:** [brief — what was non-default]
- **Outcome (filled in at Stage 5):** [success / friction / promotion candidate]
```

This feeds the **3rd+ "other" invocation promotion question** at Stage 0 of future invocations (per SKILL.md § Learning loop surfaces). The skill reads `other_log.md` at every `other` invocation and surfaces accumulation patterns.

### Promotion question surface (3rd+ use)

Per SKILL.md § Learning loop surfaces:

> "You've used `other` N times. Looking at the log, these uses look like [description — derived from clustering on author-named-genre + reader-audience]. Should we add this as a named genre? (Design conversation with you, ~30 minutes.)"

Don't wait for the author to initiate — surface the question. The author decides whether to promote. If yes: design the genre config together; the working config from this invocation becomes the v1 of the new genre. If no: continue with `other`.

---

## Stage 1: Pre-draft cyborg conversation (cross-genre defaults, scaled)

Same four moves as the cross-genre frame (printpress SKILL.md Stage 1 / SPEC Stage 1). Scale by the formal parameters of the artifact:

- **Short artifacts (cold-outreach email, op-ed, brief statement)**: very brief Stage 1. Surface the field briefly even if the author moves fast through it; capture even a 4-line DRAFT_PLAN.md so the structural decision is on the page (per SPEC § Stage 1 "When to skip legitimately").
- **Long-form artifacts (tenure dossier, sabbatical report, manifesto)**: full four-move conversation. May benefit from voice memo invitation in Move 2 (deep dialogic).

The four-move pattern (Move 1 surfaces 2–4 candidate framings, Move 2 author names the story with NO agent candidate, Move 3 arc proposal under conventions, Move 4 section beats with grounding) holds across artifact types. The genre-specific framings are derived from Stage 0 conversation — what does the audience read for, what's the closest matching genre's conventions to lean on or break.

**INSIGHTS.md relational-tracing read still required.** Same as named genres — without it, Stage 1 collapses to similarity-clustering.

**candidate for the question they haven't asked:** ask the author whether the artifact has a Hakope-Question move. Some genres do (op-eds, manifestos, cold-outreach for novel partnerships); some don't (sabbatical reports, dossiers documenting completed work). Don't force it; the author's "no, this is documentation" is a legitimate answer.

**Output:** `DRAFT_PLAN.md` in the project folder. Same template (`templates/DRAFT_PLAN_TEMPLATE.md`) as named genres.

---

## Stage 2: Drafting (cross-genre defaults)

Same as printpress SKILL.md Stage 2. Voice-check active throughout.

**Voice-check tag mapping for `other`:** ask the author what the closest existing tag is (`academic_position`, `tech_position`, `ea_grant`, `humanist_fellowship`, `peer_review` once it exists), or note that no tag fits and use the user voice baseline without a genre overlay. For `other`, the genre overlay risk is contamination from the wrong genre's register; defaulting to "no overlay" is safer than picking an arbitrary tag.

**Williams's *Style*** applies continuously regardless of genre.

**The seven common drafting mistakes** apply across all of June's writing — check during drafting, not just at QC. Per `Bloch_Application_Context.md`. (For other authors using this config: substitute the author's drafting-mistakes list if one exists.)

---

## Stage 3: Reviewer swarm — derived swarm composition

Stage 3 swarm composition is **derived from Stage 0 conversation**, not a fixed stack.

### Calling /critic-swarm with explicit personas

/critic-swarm gets passed `--personas p1,p2,p3` as an explicit list rather than a stack name. The personas are specified in DRAFT_PLAN.md "Working genre definition" section (Stage 0 question 2 — who reads this).

For most `other` invocations, the persona list is small (2–4 personas) and may pull from the named-genre persona libraries:
- A primary-audience reader anchored to whoever Stage 0 named (a foundation officer, a reader of the target publication, a colleague reviewing a workshop packet)
- An always-runs reviewer set (intelligibility, jargon, author-informed) — these run regardless

Sometimes a fully novel persona is needed (e.g., for an op-ed: a reader of the target publication, calibrated to its political/editorial register). Build the persona prompt in conversation with the author, anchored to a specific real reader where possible.

### Author profile

Same as named genres — author profile path passed if set up; author-informed reviewer runs in /critic-swarm.

### Synthesis output

Same format — cut list first → convergent flags → threading → specialty insights → mechanical flags.

---

## Stage 4: Revision (cross-genre defaults)

Same as printpress SKILL.md Stage 4. Sequential workshopping. ONE edit at a time.

Voice-check active throughout revision.

Drafting & revision principles (Williams, less-is-more, action verbs, stress position, etc.) apply continuously.

Overwhelm detection same as named genres.

---

## Stage 4.5: Pre-save QC verification

Same checklist as printpress SKILL.md Stage 4.5. Customize verification items per the working config (e.g., for an op-ed: "fits the target publication's register and length"; for a dossier: "documentation is comprehensive across the review period").

---

## Stage 4.6: Requirements Compliance Gate

Before declaring materials ready, run the cross-genre **Requirements Compliance Gate** (printpress SKILL.md § Stage 4.6): re-fetch the live posting/form, diff against `APPLICATION_STRUCTURE.md`, and verify every required document, limit, prompt/section/field, and submission convention is met. Any unmet or changed requirement blocks "ready" — the author can override explicitly. Backstop to the Stage 0 Submission Requirements Ledger.

---

## Stage 5: Save + post-submission

### Mechanical cleanup

Same as named genres — haiku subagent on the final `.md`. Per PIPELINE.md Step 5.9 (or equivalent if working dir's CLAUDE.md points elsewhere).

### Save protocol

Use the cross-genre defaults from printpress SKILL.md Stage 5. Customize per Stage 0's save-convention answer:
1. Save draft(s) to the project folder
2. Ensure `DRAFT_PLAN.md` is in the folder
3. Append a row to `[ProjectFolder]/VERSION_LOG.md` — `From | To | Type | Author | Notes`
4. Save `*_final.md` after the artifact is finalized
5. Save/update a project checklist if the working config indicated one
6. Update any tracker named in Stage 0 (per working-dir CLAUDE.md conventions)

### Voice-check learn pass

Run only if a voice-check `--genre` tag was confirmed at Stage 0. If no tag fits, skip the genre-tagged learn pass; running without `--genre` risks contaminating the user voice baseline. Per `LEARNING_LOOP_PROCEDURE.md` and printpress SKILL.md § Stage 5.

### Update other_log.md (Stage 5 outcome field)

Append the outcome to the entry created at Stage 0:
- **Success / friction / promotion candidate**
- One-line note on what worked or didn't in the working config

This feeds the periodic review trigger.

---

## Learning loop surface — promotion to named genre

Per SKILL.md § Learning loop surfaces and SPEC § Learning loops Tier 2:

**Trigger:** 3rd+ use of `other` in `other_log.md`.

**Process:**
1. At Stage 0 of the 3rd+ `other` invocation, the skill reads `other_log.md` and clusters entries by author-named-genre + reader-audience.
2. If a cluster of 2+ similar uses exists, surface the promotion question:

   > "You've used `other` for [genre name] N times. Looking at the log, these are similar enough that we could promote to a named genre. Should we design the config? (~30 minutes.)"

3. If the author says yes:
   - Design the genre config together; this is its own workshop (akin to peer_review Stage 1 design — the workshop skill, when built, will own this conversation).
   - The working config from the current invocation becomes the v1 of the new genre.
   - New genre config saved to `~/.claude/skills/printpress/genre_configs/[new_genre].md`.
   - `other_log.md` entries that were the cluster get archived to a "Promoted" section with a pointer to the new config.

4. If the author says no:
   - Continue with `other` for this invocation.
   - Note the rejection in `other_log.md` so the prompt doesn't re-fire on every invocation.

---

## Don't do this

- **Don't pick a named genre on the author's behalf when the artifact is borderline.** Ask. The cost of asking is one structured question; the cost of defaulting to the wrong genre is the workflow pulling the artifact toward conventions that don't fit it.
- **Don't skip the `other_log.md` append.** The promotion mechanism only works if the log has data. Even for one-off invocations, the entry (with "outcome: one-off, no promotion needed") is what makes future invocations smarter.
- **Don't over-engineer the working config.** Most `other` invocations are lighter than named genres and shouldn't carry the full Stage 0 / Stage 3 ceremony. Scale by what the artifact actually needs.
- **Don't run voice-check `--learn` without a confirmed `--genre` tag.** Contamination risk. Skip the learn pass for `other` invocations where no tag fits.

---

## Subgenre notes (for future)

`other` is itself a meta-config; subgenres emerge through promotion to named genres rather than internal subgenre-tagging. Patterns to watch for in `other_log.md` accumulation:

- **Public-facing writing** (op-eds, public scholarship, interviews) — likely a future named genre with its own Stage 1 framings
- **Pedagogical artifacts** (syllabi, teaching dossier intros, workshop packets) — could be a `pedagogy` genre or a subgenre of `academic_position`
- **Cold-outreach / partnership letters** — could promote to `cold_outreach` or fold into `non_academic_application`
- **Self-narration documents** (sabbatical reports, tenure dossiers, biosketches) — different reader, different conventions; could be a `self_narration` genre

The periodic genre review (every 3rd–5th use of any genre, per SKILL.md) reads `other_log.md` even when not directly invoked, surfacing promotion candidates the author may not have noticed.

---

## Learning loop notes

[Empty for v1 — populated through use.]

**v1 inferences requiring confirmation:**
- Five Stage 0 questions as the right structural frame (artifact / reader / structure / sources / closest match) — sourced from spec; refine after first 2–3 uses.
- Voice-check tag default to "no overlay" when no fit — sourced from contamination-risk reasoning, not from observed practice. Confirm with first `other` invocation that has unclear tag fit.
- Promotion threshold of 2+ similar entries (not 3+) — softer than the 3+ rule for surfacing the prompt, because the design conversation can decide whether 2 is enough. Refine after first promotion candidate.
