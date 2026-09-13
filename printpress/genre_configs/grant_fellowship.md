# Genre config: grant_fellowship

**Sources:** PIPELINE.md (`../PIPELINE.md`, esp. Steps 0 verbatim CFP capture, 0.5 fact assembly, 1.5 form-prompt allocation, 3 the question they haven't asked (PIPELINE Step 3), 4 Fellowship/AI welfare audience calibration, 5.7 adversarial reviewer pass, 6 save), Bloch_Application_Context.md (seven common drafting mistakes, voice characteristics), critic-swarm personas at `~/.claude/skills/critic-swarm/personas/grant_fellowship/`, printpress SPEC (Genre splitting note on deferred ea_grant / humanist_fellowship split), printpress SKILL.md (cross-genre Stages, voice-check tag mapping), Job Search CLAUDE.md (funder profiles, opening-payoff intros)
**Updated:** 2026-05-07
**Status:** v1 — built ahead of first use; refine after first invocation

---

## When this genre applies

Grants and fellowships with a **review panel** (not a hiring manager, not a search committee). The application is structured as a CFP / RFP with prompts, word limits, and a panel composed of program officers + subject-area scholars + (often) external reviewers. Tracks include:

- **Effective-altruist grants (EA)** — SFF (Survival and Flourishing Fund), LTFF (Long-Term Future Fund), Coefficient Giving, Open Phil where applicable. Reviewer culture: technical, impact-focused, longtermist register, often quantitative-evaluative.
- **Humanist fellowships** — Wenner-Gren, Hunt, ACLS, NEH, Spencer, Mellon postdocs, Schomburg, AAUW, Fulbright. Reviewer culture: subject-area scholars, methodological-rigor-focused, scholarly register.
- **STEM/research grants reviewed by humanists or hybrid panels** — NSF SBE, some NIH cultural-research lines, foundation grants for interdisciplinary work.
- **Arts and tech-adjacent grants** — Mozilla Foundation, Knight Foundation, Rita Allen, Sloan tech-and-society lines.
- **AI safety fellowships** — Anthropic AI Safety Fellows, Constellation Astra, MATS, fellowships hosted at AI labs but reviewed by **panels** (not by hiring managers). **Edge case** — see Genre boundary below.

Hallmarks: structured form with explicit prompts (Q1, Q2, Q3 — each with its own word limit), panel review (multiple readers), funder mission and review culture as load-bearing context (a project that's strong for one funder reads as adjacent for another), deliverables and timeline expected, often a budget, often a project description distinct from the applicant's broader research program.

**Subgenre variation visible in v1 (deferred split — see Subgenre notes):**
- **EA-flavored** (SFF, LTFF, Coefficient) — voice-check tag `ea_grant`. Technical / impact-focused. Lead with the finding before the theory. Quantified deliverables. Less narrative, more empirical.
- **Humanist** (Wenner-Gren, ACLS, NEH, Spencer) — voice-check tag `humanist_fellowship`. Subject-area scholars. Methodological depth. Narrative scholarly register. Theoretical stakes load-bearing.
- **Hybrid** (Mellon tech-and-society, Mozilla, Sloan) — register depends on panel composition. Confirm at Stage 0.

**Genre boundary:**
- Academic positions → `academic_position` (committee review of cover letter + RS/TS/DS, not a structured form)
- Industry roles at AI labs reviewed by hiring managers → `non_academic_application`
- Anthropic Fellows / Constellation Astra (panel-reviewed fellowships hosted at industry orgs) → **this genre** (`grant_fellowship`), because reviewer composition is a panel of researchers, not a hiring manager. Voice-check tag is `ea_grant` per the EA register, even though the host is industry. (See `project_anthropic_fellows.md` memory; Anthropic Fellows app at `Anthropic Fellows/` is the in-house reference.)
- Cold-outreach grants without a structured form → use `other`; this config assumes prompts and panel.

---

## Stage 0: Data-in (genre-specific)

**Find paths via the file-finding protocol** (printpress SPEC, "Where the skill finds local files").

### Required file load

| File | Source | If missing |
|---|---|---|
| `[AppFolder]/POSTING.md` | The CFP / RFP, **complete unedited text**. WebSearch → WebFetch → save | Create before proceeding. Cannot draft without this. |
| `[AppFolder]/APPLICATION_STRUCTURE.md` | **Verbatim prompts and word limits**, captured exactly as written, NOT paraphrased | **Create before drafting** — grants are heavily prompt-driven; paraphrasing introduces drift the agent then drafts toward (PIPELINE.md Step 0). |
| **Funder profile** — `_funder_profiles/[FUNDER].md` | Working-dir convention (June: `Job Search/_funder_profiles/`) | **Write before drafting if missing.** Per Job Search CLAUDE.md mandatory reading: "Grants/fellowships … if no profile exists, write it before drafting." |
| Agent briefing | Path from working CLAUDE.md | Ask author |
| Voice document | Path from working CLAUDE.md | Ask author |
| Application context | Path from working CLAUDE.md | Ask author |
| Reframe Opportunity Brief (when relevant) | June: `agent_briefs/Bloch_Reframe_Opportunity_Brief.md` | Ask author |
| Voice-final priors (2–3 closest by track) | Track lookup table — see PIPELINE.md Step 0 | Ask author |
| Publications deep read (research statements / project descriptions) | June: `/Users/june/Documents/GitHub/profile/PUBLICATIONS_DEEP_READ.md` | Ask author |

### APPLICATION_STRUCTURE.md content

**Capture verbatim. Why verbatim matters** (PIPELINE.md Step 0): reviewers grade against the prompt as written. "Describe your research in 500 words" and "Describe how your research advances the field's most important questions in 500 words" call for different documents. Paraphrasing during capture introduces drift that the agent then drafts toward.

For each prompt:
- Exact wording (copy-paste, do not summarize)
- Word / character limit
- Formatting rules (Markdown allowed? Specific header structure?)
- Attachment requirements (CV format, supplementary documents, letters of support)
- Any explicit guidance to applicants from the funder

For grant-specific structural elements:
- Budget format (line items, indirect costs allowed?)
- Deliverable timeline expectations (1-year, 2-year, 5-year arc)
- Reporting requirements
- Dissemination expectations

### Funder profile content

If `_funder_profiles/[FUNDER].md` doesn't exist, build it before drafting. Per `project_grant_tracking.md` memory and Job Search CLAUDE.md. The funder profile feeds Stage 1 framings, Stage 2 register calibration, and Stage 3 program-officer persona anchoring. Capture:

- **Mission as stated** — verbatim from the funder's site
- **Review culture** — Stage 1 vs. Stage 2 (panel) review process, what kinds of applications get advanced at Stage 1, who reviews at Stage 2
- **Recent grantees** — what they funded last 2–3 cycles. This is the strongest signal for what the funder treats as legible-as-fit.

⚠ **Split what you know three ways, and mark inference as inference.** *Added 2026-09-12
from the Rustin fork, which carries a guard this config lacked.*

- **Published facts** — the funder's own stated criteria, guidelines, eligibility pages.
- **Relationship records** — prior correspondence, feedback, conversations.
- **Inference** — patterns you read off the award record.

**Recent grants are strong evidence of what the funder has treated as legible. They do not
create an unpublished rule.** An agent reading the "strongest signal" line above without this
guard will invent a criterion out of a pattern and then draft against it — which reads to a
panel as confident misunderstanding of their own programme.
- **Funding rate** — % of applications funded (when published)
- **Anti-patterns** — kinds of applications the funder regularly cuts (when documented in their site, blog, or program officer talks)
- **Panel composition** — when known. EA grants often disclose review panels publicly; humanist fellowships less so.
- **Deadline cadence** — annual, rolling, biannual; for rolling deadlines, verify the posting is live (per Job Search CLAUDE.md session-start rule)
- **Decision dates** — typically funder-published; feeds calendar reminders at Stage 5

**Confirm voice-check `--genre` tag at Stage 0.** Funder profile + posting register usually answers `ea_grant` vs. `humanist_fellowship`. If unclear (hybrid panels, novel funders), ask the author. Tag selection prevents genre-adaptive shifts from contaminating the user voice baseline.

### Voice-final prior selection

Same protocol as `academic_position.md`. Highlights:
1. `VERSION_LOG.md` if it exists; last submitted row is voice-final.
2. Otherwise: highest `_final.md` / `_voicefinal.md` in folder.
3. `Materials Archive/` entries via `save_materials.py` are canonical.

**Track-specific closest-match lookup** (from PIPELINE.md Step 0):
- Anthropology fellowship → `Wenner-Gren Hunt Fellowship/`
- AI/tech grants → `SFF/`, `LTFF/`, `Coefficient Giving/`
- AI welfare/safety fellowship → `Anthropic Fellows/`, `Constellation Astra/`
- Spencer / education humanities → `Spencer/` (when one exists)
- ACLS / NEH humanist → adapt from Wenner-Gren if no closer

### Fact assembly: FACT_INVENTORY.md

Same operation as academic_position. Per PIPELINE.md Step 0.5. Grant-specific notes:

- **Section-by-prompt fact assembly.** Grants are prompt-driven; sketch what each prompt's answer needs to do, then assemble facts per prompt. Don't write a generic project description and split it across the questions — draft each answer to its prompt (PIPELINE.md Step 4).
- **Quantified deliverables** where they exist or can be honestly committed to. EA-grant register expects them; humanist register tolerates qualitative outcomes but rewards specific timelines (chapter drafts, manuscript milestones, fieldwork seasons).
- **Reframe positioning** depends on funder type (per Reframe Opportunity Brief if it exists):
  - **AI welfare grants (SFF, LTFF, Coefficient)** — substrate framing. "Ethnic studies + affect theory = decades of tools for what gets counted as capable of feeling." Recognition and Sentience as theoretical scaffolding. Reframe as the operationalization. (See `project_ai_welfare_funding.md`, `project_sff_ichange_arc.md`.)
  - **Humanist fellowships (Wenner-Gren, ACLS, NEH)** — methodological-stakes framing. The fieldwork, the ethnography, the book project. Reframe usually NOT load-bearing for humanist apps — don't force tech work into humanist arcs. (Per `project_wennergren_state.md`: theoretical core is recognition+sensoria, temporal violence, survival architectures — the book project, not the engine.)
- **Pause-as-method handling** (per `feedback_pause_as_method.md`) — for the THPO / Pvlvcekolv work specifically: years between THPO objection and *Current Anthropology* article are method, NOT absence. Don't frame as "no writing time." Bloch methodological commitment.
- **Fieldwork duration** (per `feedback_fieldwork_duration.md`) — Pvlvcekolv fieldwork is "over a decade," NEVER "fifteen years." Recurring error in source docs that keeps getting re-introduced.

### Pull-from-prior priority

Same as academic_position. Pull from `*_final.md` (or extracted-from-PDF) of closest prior, not v1.md.

### Enforcement checkpoint

Before drafting each prompt's answer, name (in writing or note): (a) which prior materials loaded, (b) what each gave you, (c) which briefing sections at full depth, (d) which prompt's exact wording you're answering. If you cannot answer all four, you skipped Stage 0 — go back.

---

## Stage 1: Pre-draft cyborg conversation (genre-specific)

The four moves come from printpress SPEC Stage 1.

### Pre-conversation gate: analytical mode

Same as academic_position — read INSIGHTS.md 2026-04-29 BEFORE Stage 1.

**Why this matters for grants specifically:** the failure mode for grant applications is "paying lip service to the funder's framework without substantive uptake" (see Stage 4 anti-patterns). Similarity-clustering from posting language to candidate experience produces the "I match your mission" register that screeners cut at Stage 1. Relational tracing — what the candidate's work *opens up* for the funder's actual problem — produces the substantive-uptake register that advances.

### Move 0: Fit evaluation (PIPELINE Step 1) — runs before Move 1

- **Direct matches**: requirements / mission elements June meets with existing work
- **Bridgeable gaps**: gaps with credible bridge
- **Real gaps**: what the funder is asking for that her work doesn't address
- **Verdict**: Strong / Decent / Weak

**If Weak: STOP. Tell the author.** Drafting weak-fit grants wastes time at high opportunity cost — grant deadlines are typically annual or biannual, so a wasted application means a year+ delay on that funder.

### Move 1: Candidate framings

Surface 2–4 framings. For each:

- **What June's work opens up** for this funder's mission. Forms: convergence (the funder's recent grants are moving toward questions her work addresses), thread-uptake (their conversation is running a thread her work continues), productive tension (her work disagrees-interestingly with a funded direction).
- **What thread her work picks up** in the funder's recent grantees / mission statements / program-officer talks.
- **candidate for the question they haven't asked for this funder type** (PIPELINE Step 3):
  - **AI welfare (SFF, LTFF, Coefficient)** — measurement framework constitutively forecloses what it can perceive; what gets recognized as capable of feeling, by what epistemic regime, under what material conditions
  - **Humanist anthropology (Wenner-Gren, ACLS)** — Indigenous knowledge doesn't supplement Western categories, it replaces them; recognition + sensoria as one process; temporal violence as method
  - **Education humanities (Spencer)** — output format IS the bias; "did this student cheat?" as signal not violation; structural conditions of pedagogy under fascism
  - **Trans studies / genocide studies (specialized funders)** — the Genocide Convention's exclusion of gender groups IS the mechanism of non-recognition

Don't pick yet. Present the field. Move 1 opens; Move 2 takes up.

### Move 2: Author names the story

**The agent does NOT generate a candidate here.** Open with a question, listen, reflect back. For grants, the load-bearing thing the agent couldn't see from posting/profiles is often:

- The fieldwork moment that anchors the project (the question-they-haven't-asked move's bird-that-isn't-a-bird, Pvlvcekolv moth, the cemetery, the Penobscot painting)
- The methodological commitment that makes the project this project (CBPR with specific community, autoethnography under specific conditions, digital ethnography of a specific movement)
- A politics she wants visible in the proposal but might be coached out by genre conventions
- A refusal of a frame the funder's posting language wants to impose (e.g., "applicant's research project" boilerplate that flattens the relational/community accountability)

Failure mode: agent answers for the author. Recovery: ask.

### Move 3: Arc proposal under genre conventions and formal parameters

**Formal parameters (non-negotiable):** the prompts as written, exact word limits per section, formatting rules, attachment requirements. The arc must respect them — the form IS the document structure.

**Grant/fellowship conventions to work with or against:**

- **Opening paragraphs set up a specific payoff the rest of the doc delivers, not a generic summary.** Per `feedback_payoff_setup_intros.md` (memory). Applies to all high-stakes drafting; especially load-bearing for grants where reviewers commit to a Stage 1 yes/no fast.
- **EA-flavored conventions** (`ea_grant`):
  - Lead with the finding / contribution before the theory. EA-adjacent reviewers expect empirical clarity early.
  - Quantified deliverables, theory of change, concrete timeline.
  - Readability for non-specialist reviewers within the technical-impact register.
  - Avoid: literature-review parallelism, scholarly-density opener, theoretical-architecture sections without immediate empirical grounding.
- **Humanist-flavored conventions** (`humanist_fellowship`):
  - Open with methodological stakes / theoretical question, ground in fieldwork or empirical anchor.
  - Methodological depth is expected; subject-area scholars read for it.
  - Project description distinct from a research statement — focused, specific, deliverable-shaped (chapters, articles, fieldwork seasons).
  - Avoid: the EA register (compresses the theoretical work humanist reviewers grade for).

### Allocation table (grants use form-prompt rows)

For grant-style structured forms, allocation rows are **the form's prompts** (Q1, Q2, Q3) — not separate documents. Each story / concept / finding gets its full treatment in ONE answer; other answers reference it briefly. Pull the prompt list from `APPLICATION_STRUCTURE.md`.

| Prompt (verbatim, with word limit) | Full treatment of [story/concept] | Brief reference to [other story/concept] |
|---|---|---|
| Q1: [verbatim, NN words] | [main story for this prompt] | [other concepts referenced] |
| Q2: [verbatim, NN words] | [main story for this prompt] | [other concepts referenced] |
| ... | ... | ... |

Same anti-redundancy logic as academic apps; different unit. Build BEFORE drafting any answer.

### Move 4: Section beats and load-bearing specifics

From FACT_INVENTORY and the allocation-by-prompt table, name what each prompt's answer carries. Which scenes, which numbers, which scholars cited *doing work* not name-dropped, which prior phrasings to mine.

### Funder landscape research (analog of PIPELINE Step 3.7) — feeds Moves 1 + Stage 3 swarm

For grants, the relational-tracing analog is: who funds what, in what conversation, and where does the project enter that conversation.

1. Recent grantees (last 2–3 cycles) — what kinds of projects, what register, what scope
2. Recent program-officer talks / blog posts / public statements about the funder's evolving direction
3. For panel-disclosed funders (often EA grants): identify panel members, their public work, where June's project enters their conversation
4. Funder's relationship to other funders — sometimes co-funded, sometimes positioned-against; informs register

**Output:**
- Update `_funder_profiles/[FUNDER].md` with anything surfaced
- Optionally `[AppFolder]/INTELLECTUAL_CONNECTIONS.md` for panel-disclosed funders or where review-panel members are scholars in conversation with June's work (rare for grants — common for fellowships)

### DRAFT_PLAN.md output

Save to `[AppFolder]/DRAFT_PLAN.md` using `templates/DRAFT_PLAN_TEMPLATE.md`. Captures: arc, openings/uptakes, the question-they-haven't-asked reframe, allocation-by-prompt table, what we're deliberately NOT doing, swarm composition decision, conversation notes.

**Failure modes to watch for** (same as academic_position): approval-seeking framing; directive extraction without understanding-shift.

**When to skip legitimately:** very short LOI / preliminary inquiry under 300 words. Even then, name the arc in one sentence before drafting.

---

## Stage 2: Drafting (genre-specific)

Draft from `DRAFT_PLAN.md`. Step 2 executes the plan.

### Read the actual posting and prompts before writing a sentence

Re-read `POSTING.md` and `APPLICATION_STRUCTURE.md`. Each prompt has its own answer, in its own word limit, addressing what that prompt actually asks. **Don't write a generic project description and split it.**

For grants especially: posting-specific instructions ("address how this work advances X funder's commitment to Y") set required moves. Ignoring them weakens the application even if the rest is strong.

### Audience calibration (PIPELINE Step 4)

| Bucket | Posture |
|---|---|
| **EA-flavored grants** (`ea_grant`) | Empirical, concrete deliverables, theory of change. EA-adjacent audiences need the finding before the theory. Reframe = the operationalization gap (between critical theorists who don't build and CS researchers using insufficient metrics). Quantified scope where honest. Less narrative density, more deliverable shape. |
| **Humanist fellowships** (`humanist_fellowship`) | Scholarly but narrative. Opening sentence is everything — it decides whether they keep reading (PIPELINE Step 4.5). Methodological stakes upfront. Fieldwork or ethnographic anchor early. Theoretical contribution explicit. Don't compress academic register that's load-bearing — humanist reviewers grade for it. |
| **Hybrid panels** (Mellon tech-and-society, Mozilla, Sloan) | Confirm panel composition. Often a code-switching arc: open in the register the panel-chair reads in, expand to the register the subject-area reviewers read in. |

### Voice-check tag mapping

Per printpress SKILL.md Stage 2 table, confirmed at Stage 0:

| Subgenre | voice-check `--genre` tag |
|---|---|
| SFF, LTFF, Coefficient (EA grants) | `ea_grant` |
| Wenner-Gren, ACLS, NEH (humanist fellowships) | `humanist_fellowship` |
| Anthropic Fellows, Constellation Astra | `ea_grant` (research lab fellowship register) |
| Hybrid (Mellon tech-and-society, Mozilla) | Confirm at Stage 0; usually `ea_grant` for tech-leaning, `humanist_fellowship` for humanities-leaning |

**v2 split candidate** (deferred, per printpress SPEC § Genres): `ea_grant` and `humanist_fellowship` should eventually become two `/printpress` genres to match voice-check's existing tag distinction. The two have meaningfully different reviewer cultures (technical/impact-focused vs. subject-area scholars). Personas need stack-appropriate framings for each. v1 keeps as one genre; tag is selected per-application.

### Word count targets

| Document type | Target |
|---|---|
| Grant abstract | per form requirements |
| Project narrative / research plan | per form requirements (commonly 5–10 pages, 2500–5000 words for fellowships; 1500–3000 words for shorter grants) |
| Personal statement (when separate) | per form (300–800 words common) |
| Budget justification | per form (typically short — 250–500 words) |
| Letters of support | not drafted by /printpress (request from author's collaborators) |

These are targets for the *final* document, not for the assembly or handoff. Grant and fellowship prompts make the final cap non-negotiable, but they do not decide who performs structural selection. Capture genuine evidentiary abundance, record the actual ratio, show the full assembly to the author for KEEP / DROP / UNSURE marking, and then choose an AI-proposed, author-led, or hybrid route. A provisional 50–75% over figure may orient new material but is not a command; a provisional ~1.2 × handoff is an experiment, not a guarantee of quality.

### Cutting swarm composition (Stage 2 — only when the post-marking route includes AI cutting)

If this route is chosen, core readers are **program-officer**, **author-informed**, and **subfield-specialist**. They receive the author's marks and produce a reversible handoff plus diff. The subfield-specialist remains important because a generic cut can remove the field-specific texture that makes a proposal legible to its panel.

**Briefing difference from Stage 3:** for the cutting swarm, brief subfield-specialist across the **2–3 subfields most relevant to this specific proposal** (from `INTELLECTUAL_CONNECTIONS.md` or the project's own framing), instructed to hold all of them at once rather than reading through only the single primary subfield the way the base persona (`critic-swarm/personas/grant_fellowship/subfield-specialist.md`) is normally scoped. Same base file, broader briefing — don't fork a new persona file for this.

Optional (long project narratives only): **critical-theorist**, generalized the same way if used — the base file's "anchor to a real scholar" instruction (per this genre config's Stage 3 section) is fine for Stage 3's live-reader depth, but if pulled into the cutting swarm it should run generalized or as a couple of theorists, not one named scholar's idiosyncratic take, for the same reason the academic department-reader stays composite.

Excluded: intelligibility, jargon (stay Stage 3/4).

### Voice-check during drafting

Same protocol as academic_position. Pre-draft: read voice profile, select `--genre` tag (`ea_grant` or `humanist_fellowship`). In-flight: write in voice. Post-draft: self-run quantitative check, silently fix contamination, surface structural findings as suggestions. Williams's *Style* applies continuously.

### What the 2026-08 research established — read before drafting

*Added 2026-08-09. Restated here rather than only referenced, because Stage 2 dispatches cold subagents that see only their brief. **Put these in the brief.** Full sourcing: `_application_evidence/` (esp. `Hypotheses_Grants_NIH_NSF.md`, `Hypotheses_Humanities_Fellowships.md`) and the `humanist_fellowship` / `ea_grant` blocks of the voice profile.*

**Status rule:** funder-published criteria are **facts**. Everything else here is **hypothesis** — panel research and reviewer testimony, never a measure of what makes a proposal succeed.

**Who is being cited below, and why they count** — you have no context on these names, so here it is once:
- **Lamont** — sociologist who observed twelve real funding panels and interviewed 81 panelists within hours or days of their deliberations, across five national competitions **including ACLS and SSRC**. The only ethnography of academic panel judgment that exists, and two of the competitions she studied are ones June applies to. Fieldwork is c. 2000, which is the main caveat.
- **Roche** — a named scholar who served on an ACLS selection panel and published a first-person account with vote counts and panel composition. One of only two such accounts in existence for humanities fellowships.
- **Rosati** — both a National Humanities Center fellow and a member of its selection committee. The other of the two.
- **Fang & Casadevall**, **Pier et al.**, **Mayo et al.**, **Snell** — researchers who studied grant peer review quantitatively: reviewer agreement, score reliability, and how much of an outcome is determined by which reviewers happened to be assigned. All US/Canadian biomedical or federal contexts. ⚠ **Transfer to humanities fellowships is unargued** — those are large structured panels with numeric scoring; June's funders mostly are not. Use the shapes, not the numbers.
- **The ERC interview study** — 22 interviews with European Research Council panel reviewers about how they actually decide under time pressure.
- **NIGMS** — a US National Institutes of Health institute; the guidance cited is its own program office correcting how its reviewers were scoring.

1. **⚠ CAPTURE THE FUNDER'S PUBLISHED EVALUATION CRITERIA VERBATIM AT STAGE 0.** This was the pipeline's largest gap. Required *materials* were being captured; the *criteria the work is scored against* were not. **Where a funder publishes criteria they outrank everything in this config** — they are the rubric, stated by the people deciding. Carry them into the allocation, the Stage 2 brief, and the Stage 3 swarm (critic-swarm permits exactly one scoped lens to map an artifact against named external criteria; fold it into the program-officer persona). Two things this catches: criteria a funder does **not** use — ACLS publishes clarity, intellectual/social significance, quality, and feasibility, and does **not** list originality, so a proposal optimized for originality is optimized for an axis they don't score — and criteria that **favour June and would otherwise go unclaimed**, e.g. ACLS instructing reviewers to weigh the record "taking into account relative advantages or constraints on resources over the course of the applicant's career," the only such instruction across seven programs surveyed. **Write into that criterion; don't hope a reviewer applies it unprompted.** Where a funder publishes none, record the absence — it predicts a more idiosyncratic review.

2. **⚠ ACLS runs two sequential stages with different readers.** Per an internal ACLS document quoted in Lamont: applicants are **prescreened by two scholars in their own field** (anthropology and archaeology are both named prescreening fields), and those scores **eliminate about 50% of all proposals**. Survivors go in groups of ~60 to **four panels of five or six** mixed-discipline scholars. → The first gate is a same-field specialist, not the interdisciplinary panel. A first-person ACLS panelist account records a strong application dying because one same-field panelist objected and everyone deferred — at ACLS that risk sits at the *front*. **The proposal must clear a specialist before it ever meets a generalist.** ⚠ Lamont's fieldwork is c. 2000 — verify against current ACLS materials.

3. **You are judged against your neighbours, not an absolute standard.** Three independent sources: Lamont ("panelists adopt a nonlinear approach… they compare proposals according to shared characteristics"), the ERC interview study ("calibration devices" — reviewers adjust to the quality of the given set), and an NSF panelist describing rankings nudged on the board by whoever recalls the cluster. **Legibility to whoever else is in your pile matters more than absolute merit.**

4. **Excellence and diversity are additive, and the action is at the margin.** Lamont: "contra popular debates… not alternatives; they are additive considerations," with panelists competing over "which of several different types of diversity will push an A− or B+ proposal above the line — and very few proposals are pure As." **And the diversity evaluators report caring most about is institutional** — "ensuring that funding not be restricted to scholars in only a few fields or at top universities." That is the axis June sits on.

5. **Jargon eliminates, and framework-first framing is a named failure.** Roche (ACLS panelist): jargon "immediately led to elimination"; at finalist stage the panel is "almost looking for excuses to eliminate"; and the named failure is a topic with no thesis, specifically *"externally plugging categories into a topic as opposed to letting the topic or the evidence drive the categories."* → The framework must emerge from the material, not be laid over it. Relevant to how Reframe-adjacent work gets framed.

6. **The proposal needs someone in the room able to advocate for it.** Rosati (NHC fellow and selection committee member): a discipline-internal proposal needs a particular person seated, and whether they are is luck. Lamont names the norm that makes this decisive — panelists defer "to the expertise of colleagues." Converges with the department-composition rule on the academic side.

7. **Innovation is penalized past a threshold.** Lamont, from panel observation: *"innovators are often penalized if they go too far in breaking boundaries, even if by doing so they redefine conventions."* Plus homophily — evaluators "often define excellence as what speaks most to me, which is often akin to what is most like me." And Roche's singleton: work positioned as **correcting** its field is more exposed than work positioned as **opening** something, because the specialist who would be corrected is in the room.

8. **Reduce the count of criticizable surfaces.** NIGMS had to issue guidance because reviewers "arrive at overall impact scores by comparing the NUMBER of weaknesses and strengths… rather than balancing the importance." → A defensible small claim may outperform a large one with an exposed flank. (US federal panels — transfer unargued.)

9. **Assignment is a substantial share of the outcome.** Only two or three people read any application carefully; the top-ranked project would have missed the cutoff 9–35% of the time depending which pair drew it; and the randomness concentrates in the **competitive middle**, where most applicants sit. Reviewer influence scales *inversely with the payline* — the tighter the money, the more one reader's idiosyncrasy decides.

10. **Structural shift that favours June: four of eight programs surveyed have removed reference letters entirely.** ACLS this cycle accepts **no letters and no writing sample** — "reviewers will consider your proposal itself as a sample of your writing," so three pages carry everything. Verify per program; this is recent and moving.

11. **NEH requires footnoted acknowledgement of inserted AI-generated text.** A formatting-and-attribution requirement, not a philosophical one. LTFF and Coefficient have no findable published policy — check the live form.

### The seven common drafting mistakes (Bloch_Application_Context.md)

Check during drafting. Grant-specific notes:

1. Treating academic and tech work as separate tracks → **for hybrid grants this is critical**; the project IS the integration.
2. "Non-traditional" framing → flag.
3. Precarity as backstory rather than design condition → load-bearing for fellowship personal statements.
4. Softening political language → never. "Police state," "genocide," "ruthlessly exploitative" stay.
5. Separating disability from design → load-bearing.
6. The "journey" or "pivot" frame → flag. The project is structurally produced, not chosen as a career-shape.
7. Calling Reframe a chatbot → never. Engine, 312 modules.

### Anti-generic test

If a sentence could describe any scholar with comparable training applying for this grant, delete it. Specificity is the constraint layer.

### Sentence-level rules (Bloch_Application_Context.md)

Especially load-bearing for grants:
- Rule 4 (tools by what they REPLACE) — for project descriptions
- Rule 6 (categorical modality) — humanist fellowship reviewers expect committed claims in evidenced sections
- Rule 8 (constructivist framing — knowledge from practice, not "I discovered") — load-bearing for both fellowship personal statements and EA grant impact framing
- Rule 9 (topic sentence first, story demonstrates) — opening paragraphs set up the payoff
- Rule 3 (no self-aggrandizing frames) — let facts carry weight; both EA and humanist registers are allergic to "groundbreaking" prose

### Never invent numbers

Same as academic_position. Use `[DATA NEEDED]`. Reframe timeline (~November 2025) and Pvlvcekolv fieldwork ("over a decade," NOT "fifteen years") are recurring inflation/error points. Verify against source.

### Format

Per Job Search CLAUDE.md "Document generation and templates": grants typically render as PDF or paste-into-portal text. `.md` source is the canonical form for the voice-check learning loop. Match format requirements named in the funder's portal.

---

## Stage 3: Reviewer swarm (invoke /critic-swarm)

### Pre-swarm: reader takeaway audit (PIPELINE Step 4.7)

Write `[AppFolder]/READER_TAKEAWAYS.md` — 5–8 things the panel should know about June and the project by the end. Distributed across: who June is, what the project is, why it's fundable by THIS funder specifically, what becomes newly possible (or known) if funded, what's the deliverable shape.

Read each prompt's answer against the takeaways.

### Persona stack

**Stack name:** `grant_fellowship` (per `~/.claude/skills/critic-swarm/personas/grant_fellowship/`).

Personas in the stack:
- **Program officer / Stage-1 screener** (`program-officer.md`) — pattern-recognizes fit fast. Stage 1 decision + panel ranking estimate. Anchored to the funder's review culture from `_funder_profiles/[FUNDER].md`. The highest-leverage check for grant work — most applications die at Stage 1.
- **Subfield specialist** (`subfield-specialist.md`) — Stage 2 panelist anchored to the project's subject-area conversation. For AI welfare grants: an AI safety researcher or operationalized-ethics scholar. For humanist fellowships: a scholar in the subfield (NAIS, transgender studies, archaeology of the Native South, etc.).
- **Critical theorist** (`critical-theorist.md`) — checks substantive uptake of theoretical scholars. For June's work, this is critical because Reframe-engaged scholars (Wynter, Spillers, Hartman, Benjamin, Mingus, Yosso) are operationalized, not personal-tradition — the persona catches over-claim or under-claim of theoretical relationship (per `Bloch_Application_Context.md` "Scholarly Traditions").

Anchor program-officer to the funder's specific Stage-1 review culture (from funder profile). Anchor subfield-specialist to a real scholar in the project's conversation (from INTELLECTUAL_CONNECTIONS or built ad-hoc). Anchor critical-theorist to one of the theoretical scholars June engages.

### Context passed to /critic-swarm

- The draft (full application, all answers)
- `POSTING.md` and `APPLICATION_STRUCTURE.md` — verbatim, the actual CFP and prompts
- `_funder_profiles/[FUNDER].md` — for program-officer anchoring
- `INTELLECTUAL_CONNECTIONS.md` if it exists — for subfield-specialist anchoring
- Author profile path (if set up)

### Always-runs reviewers

Intelligibility, jargon (venue-aware — humanist fellowships tolerate scholarly density, EA grants don't), author-informed (profile-gated). These run inside /critic-swarm regardless of stack.

### Synthesis output

Cut list first → convergent flags → threading → specialty insights → mechanical flags.

### Adversarial reviewer history note

Per PIPELINE.md Step 5.7 history: this stack was first used 2026-04-25 on Wenner-Gren (5 personas; surfaced AI dominance, theoretical density, Pvlvcekolv-Muscogee handling as convergent flags). The pattern that emerged: convergent flags from grant_fellowship stack are usually about *theoretical handling*, not prose-level issues. Prose-level fixes are mechanical; theoretical-handling fixes go to Stage 4 sequential workshopping.

---

## Stage 4: Revision (genre-specific)

### Sequential workshopping

Same protocol as academic_position — ONE revision at a time. Address convergent flags first; specialty insights second; mechanical flags last.

**Exception: structural revisions integrating substantive new content** — e.g., Wenner-Gren's V4–V8 theoretical-core consolidation (per `project_wennergren_state.md`). Batch the integration; preserve prior version as checkpoint.

**Content first, word counts later.** Lock content first.

### Drafting & revision principles

Apply continuously. Same list as academic_position; grant-specific notes:
- **Less is more** — humanist fellowship panelists tolerate density but reward what earns its weight. Strip what's not load-bearing for the project.
- **Skeleton paring under conceptual overload** — per `feedback_skeleton_paring.md`. When the agent is conceptually overloaded, surface clusters, propose 3–4 distinct cores with pros/cons, recommend with honest pushback. Don't inline-edit toward parsimony.
- **Strategic, not exhaustive** — per `feedback_strategic_not_exhaustive.md`. June's offered context (voice memos, source docs) is background for judgment, not a checklist to cram in. Especially load-bearing for humanist fellowships where the cram-everything failure mode produces conceptually incoherent V5-style drafts.

### Address convergent flags from /critic-swarm first

For grants, convergent flags often surface:
- Over-promising (scope outruns the funded period)
- Under-claiming on impact (humanist self-effacement that hurts EA-grant reads, or EA-flatness that hurts humanist reads)
- Theoretical-handling: scholars cited as parenthetical signal rather than doing work; concepts named without grounded empirical case
- Mismatched register (EA project written in humanist register, or vice versa)

### Anti-patterns specific to grants

- **Paying lip service to the funder's framework without substantive uptake.** "Your funder values X, my work does X" — generates the screener's "adjacent, not fit" cut.
- **Underclaiming on impact.** Humanist register sometimes hedges what the work makes possible; EA reviewers read the hedge as scope-uncertainty.
- **Failing to commit to a deliverable timeline.** Both EA and humanist panels expect to see what's done by month 6, year 1, year 2. Without commitment, scope reads as aspirational.
- **Pause-as-method misframed as absence** (per `feedback_pause_as_method.md`) — for Pvlvcekolv work specifically.
- **Cram-everything in opening paragraphs.** The opening sets up the payoff; if it's a summary of everything, no payoff lands.

### Logging to LEARNING_LOG.md

After Stage 3 synthesis is addressed, log to `[AppFolder]/LEARNING_LOG.md`. Tag each learning as `genre-specific` or `potentially-generalizable`.

---

## Stage 4.5: Pre-save QC verification

Same checklist as printpress SKILL.md Stage 4.5. Grant-specific verification:
- [ ] **Each prompt answered specifically** — no generic-document-split-across-prompts
- [ ] **Word limits met** for each prompt (within posting's exact specification, not 10% over)
- [ ] **Posting-specific moves addressed** — any "describe how…" or "discuss…" clause has its move in the answer
- [ ] **Funder mission legibility** — does this read as belonging to THIS funder, or as adjacent
- [ ] **Deliverables and timeline committed** — not aspirational
- [ ] **Theoretical handling** — scholars cited doing work, not parenthetical signal; substantive uptake of funder's framework
- [ ] **Reframe described as engine, not chatbot** (when Reframe is in scope)
- [ ] **Pvlvcekolv fieldwork as "over a decade," NOT "fifteen years"**

---

## Stage 4.6: Requirements Compliance Gate

Before declaring materials ready, run the cross-genre **Requirements Compliance Gate** (printpress SKILL.md § Stage 4.6): re-fetch the live posting/form, diff against `APPLICATION_STRUCTURE.md`, and verify every required document, limit, prompt/section/field, and submission convention is met. Grants especially: confirm milestones / budget / duration / deliverables requirements (these get added mid-cycle and hide in prose). Any unmet or changed requirement blocks "ready" — the author can override explicitly. Backstop to the Stage 0 Submission Requirements Ledger.

---

## Stage 5: Save + post-submission

### Mechanical cleanup

Same protocol as academic_position. Haiku subagent on the final `.md`. Per PIPELINE.md Step 5.9.

### Save protocol

1. Save draft(s) to the application folder
2. Ensure `DRAFT_PLAN.md` is in the folder
3. **Append a row to `[AppFolder]/VERSION_LOG.md`** — `From | To | Type | Author | Notes`
4. **After submission, save `*_final.md`** for each section / answer
5. Save/update `APPLICATION_CHECKLIST.md`
6. Update `Applications_Tracker.md` and grant tracking (per `project_grant_tracking.md`)
7. Archive: `python3 save_materials.py <file> "<app_name>" --doc <type> --track grant`

### Voice-check learn pass

Same protocol — `LEARNING_LOOP_PROCEDURE.md`. Use the genre tag confirmed at Stage 0:
- Single-pair: `python3 writing_check.py --learn FIRST.md FINAL.md --genre ea_grant` (or `humanist_fellowship`)
- Multi-version: `--learn-sequence --auto-discover . --pattern "..." --manifest VERSION_LOG.md --genre ea_grant`
- Always `.md`, never `.html`
- Always specify `--genre`

The Wenner-Gren multi-version arc (22 versions) is the canonical multi-version case for grant_fellowship; per `project_voicecheck_track2_done.md`, that CDA sweep is complete and integrated into voice-check profile v3.4 / v3.10.

### Post-submission workflow

Operational logic (June-specific):
1. Update `Applications_Tracker.md` — status → "Submitted," date and materials
2. Archive: `save_materials.py`
3. **Calendar reminder for grant decision date** — typically funder-published; create Google Calendar event for the published decision window. Per `project_grant_tracking.md`. Drafts only — never send without author approval.
4. **Follow-up cadence: usually no follow-up needed** — funders communicate on their own timeline (per PIPELINE.md post-submission section). Exceptions: if a funder publishes a "no-news-by-date X" rule and the date passes, draft a status-check email for author approval.
5. When interview / panel discussion scheduled (rare for grants; common for fellowships at decision-final stage): tracker, INTERVIEW_PREP.md, research panel members.
6. After decision (funded or not): update tracker, debrief, log feedback if funder provides it. Funded → grant management workflow (out of /printpress scope).

### Skill-global writes

After Stage 5:
- Update this genre config with refinements
- Periodic genre review per printpress SPEC: every 3rd–5th use, surface at Stage 0
- Watch for the deferred ea_grant / humanist_fellowship split signal (see Subgenre notes)
- Tagged-generalizable learnings from `LEARNING_LOG.md` feed cross-genre principles

---

## Subgenre notes (for future)

`grant_fellowship` v1 spans:
- **EA-flavored** (SFF, LTFF, Coefficient, Anthropic Fellows, Constellation Astra) — `ea_grant`
- **Humanist** (Wenner-Gren, ACLS, NEH, Spencer, Mellon) — `humanist_fellowship`
- **Hybrid** (Mellon tech-and-society, Mozilla, Sloan) — tag confirmed per application

**Deferred split (decision pending):** Per printpress SPEC § Genres, `grant_fellowship` is held as one genre with two voice-check tags pending the periodic review trigger. The two have meaningfully different reviewer cultures:
- **EA-flavored:** technical/impact-focused, longtermist register, often quantitative-evaluative, deliverable-shape over narrative
- **Humanist:** subject-area scholars, methodological-rigor-focused, scholarly density expected, theoretical contribution load-bearing

Personas need stack-appropriate framings for each — design work for a focused session, not mechanical rename. Signals that would trigger the split:
- Recurring swarm composition differences that subgenre tags don't resolve cleanly (e.g., critical-theorist persona reads differently against an EA application than a humanist one)
- Author-informed reviewer flags conflicts between subtypes (e.g., humanist self-effacement coded as appropriate by EA persona but as overclaim by humanist persona)
- Genre config accumulates contradictions on register/scope/deliverable expectations

When signals point to a split, design with the author. June has flagged this as deferred (per memory `project_voicecheck_v310.md` and printpress SPEC); hold for now.

**Subgenre auto-detection candidates (for v2):** funder name lookup against a registry of known funders by subgenre, posting language ("longtermist," "EA-aligned," "operationalized impact" → ea_grant; "scholarly contribution," "fieldwork," "methodology" → humanist_fellowship), `_funder_profiles/[FUNDER].md` subgenre tag. v1: ask the author at Stage 0 if not obvious.

---

## Learning loop notes

[Empty for v1 — populated through use.]

**v1 inferences requiring confirmation after first use:**
- Critical-theorist persona anchoring to specific Reframe-engaged scholars vs. personal-tradition scholars (per `Bloch_Application_Context.md` distinction). Confirm after first sweep.
- Convergent-flag pattern (theoretical handling > prose-level for grant_fellowship) — sourced from Wenner-Gren V4 history. Confirm or refine after second multi-version sweep.
- Anti-pattern list (lip-service-to-funder, underclaim-on-impact, undercommitted-deliverables) — sourced from grant-review general knowledge + Wenner-Gren convergent flags. Refine with each new application.
- Decision-date calendar protocol — funder-published dates; refine if June's actual workflow uses different cadence.
