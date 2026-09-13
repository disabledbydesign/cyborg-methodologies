# Genre config: academic_position

**Sources:** PIPELINE.md (primary, `../PIPELINE.md`), Bloch_Application_Context.md (drafting mistakes, `/Users/june/Documents/Filing/Job Search/Bloch_Application_Context.md`)
**Updated:** 2026-05-07
**Status:** v1 — initial extraction from PIPELINE.md

---

## When this genre applies

Academic faculty job applications: tenure-track at R1, R2, SLAC, and HSI institutions; visiting assistant professorships; lectureships and adjunct lines where materials follow academic-CL conventions; postdocs hosted in academic departments; open-rank searches.

Hallmarks: review by a search committee (not HR or a panel of program officers), an audience expecting full scholarly register, materials in `.docx` (not HTML), letterhead format, departmental rather than HR routing. The required set may include a cover letter, research statement, teaching statement, equity/diversity statement, writing sample, syllabi, CV, and references. `/printpress` drafts the in-scope narrative documents. Academic CVs and all reference lists are author-handled compliance items. If an application requires a résumé instead, it enters drafting unless the author explicitly takes it over.

**Subgenre variation already visible in v1 (don't split yet, but track):**
- R1 research-focused (Emory-type) — RS-heavy, scholarly density, lead disciplinary credentials
- Teaching-focused VAP / lectureship (LMU WGS, Hamilton WGS, Berkeley Anthro Lecturer) — TS-heavy, pedagogical voice, course-design specifics
- Religious studies / interdisciplinary (Harvard Divinity AI Religion) — register-bridging, theology-engaged
- NAIS / Indigenous studies — relational register, Indigenous methodologies foreground

These have meaningfully different swarm composition needs (research-heavy vs. teaching-pedagogy-heavy reviewer mix). Per printpress SPEC's "Genre splitting" guidance, hold as one genre with subgenre tags pending the periodic review trigger.

**Genre boundary:**
- Grants and fellowships → `grant_fellowship` (review panels, prompt-driven forms)
- Industry / nonprofit / EdTech / EA-org → `non_academic_application` (HR routing, ATS)
- Edge cases (Anthropic Fellows, AI safety fellowships at academic homes) — ask the author; default to whichever genre matches the *reviewer composition*, not the host institution.

---

## Stage 0: Data-in (genre-specific)

**Find paths via the file-finding protocol (printpress SPEC, "Where the skill finds local files"):** working directory `CLAUDE.md` → parent `CLAUDE.md` → author profile → ask. PIPELINE.md is documentation, not data; the skill points to it for human-readable rationale but reads paths from CLAUDE.md.

### Required file load (per PIPELINE Step 0)

| File | Source | If missing |
|---|---|---|
| `[AppFolder]/POSTING.md` | WebSearch → WebFetch → save **complete unedited posting text** | Create before proceeding. Cannot draft without this. |
| `[AppFolder]/APPLICATION_STRUCTURE.md` | **Submission Requirements Ledger** — every required document (+format/limit), prompt/section/field, submission method, deadline, and owner: `DRAFT`, `AUTHOR-HANDLED`, or `PORTAL` | **Always create.** Academic CVs and all references are `AUTHOR-HANDLED`: track them for compliance but do not draft them. A required résumé enters `DRAFT` unless the author explicitly takes it over. Only `DRAFT` rows become Stage 1 allocation targets and Stage 2 hard constraints. |
| Agent briefing | Path from working CLAUDE.md (June: `/Users/june/Documents/GitHub/profile/JUNE_BLOCH_AGENT_BRIEFING.md`) | Ask author for the briefing path |
| Voice document | Path from working CLAUDE.md (June: `/Users/june/Documents/GitHub/disabled_by_design/voice/VOICE_DOCUMENT.md`) | Ask author |
| Application context | Path from working CLAUDE.md (June: `Bloch_Application_Context.md`) | Ask author |
| Voice-final priors (2–3 closest matches) | Track lookup table — see PIPELINE.md Step 0 ("Briefing scope by document type" + track-specific closest-match lookup) | Ask author for closest prior application by track |

**Briefing scope is document-type-specific. Don't read the full briefing for every doc.** Reference PIPELINE.md Step 0 for the two scope tables (sections to read at full depth per document type; closest-prior-match lookup by track). Those tables are local data; this config points to them.

### Voice-final prior selection (PIPELINE Step 0, "How to find the right version")

Don't make the author pick. Pick correctly:

1. Read `VERSION_LOG.md` if it exists — last submitted row, or highest `fine-grained` version with `Author: June` or `June+AI`, is voice-final.
2. Otherwise: take highest `_final.md` / `_voicefinal.md` / `_v[N].md` in folder. Ignore agent-only intermediate drafts (typically v1–v3 in multi-version arcs).
3. If `Materials Archive/` has an entry via `save_materials.py`, that's canonical.

**Why structurally, not just found:** AI default picks longest-or-newest, which surfaces agent intermediate drafts the author rejected. Voice-final versions are ground truth; intermediate drafts re-introduce patterns already edited out.

### Pull-from-prior priority (PIPELINE Step 0.5, "Pulling from prior similar applications")

When a closely-related prior exists, pull from its FINAL state:
1. `*_final.md` in prior folder
2. Submitted PDF/HTML — extract prose into temporary `final_extracted.md`, pull from that
3. Highest `vN.md` if no explicit final
4. Only fall back to early drafts if none of the above exist

### Enforcement checkpoint (PIPELINE Step 0)

Before drafting each in-scope narrative document, name in writing or in a note: (a) which prior materials loaded, (b) what each gave you (voice model / story bank / structure model / arc model), (c) which briefing sections read at full depth. If you cannot answer all three, you skipped Stage 0 — go back.

### Fact assembly: FACT_INVENTORY.md (PIPELINE Step 0.5)

Academic applications need fact assembly *before* drafting. The failure this prevents: drafting from theoretical understanding, padding generic claims with theory citations, because specific factual material (scenes, dates, quotes, ethnographic detail, findings) wasn't loaded into context first. Theory padding sounds plausible; reviewers don't read it as load-bearing.

**Operation:**
1. Sketch what each section needs to do (opening, story, evidence, fit, conclusion). For each, name the kind of grounding required: scene, date, name, quote, finding, number, ethnographic detail.
2. Locate source documents per the source registries in PIPELINE Step 0.5 (R&S source materials, agent briefing, publications deep read, CV, prior application folders, the application's own folder).
3. **Read sources INTO context.** Not summaries. The actual prose and specific details. Use `pages` parameter for PDFs over 10 pages.
4. Assemble `[AppFolder]/FACT_INVENTORY.md` with: per-section facts, source paths, `[DATA NEEDED]` tokens for gaps requiring author input.
5. **Use the inventory to verify and bound the draft.** Do not mistake its compressed rows for the evidence at the scale where an interpretive claim is earned.

### Evidence-to-claims bridge — optional, triggered by complexity

For research-intensive or interdisciplinary applications, major identity, research, and methodological claims may need a bridge between the fact inventory and the plan. Create `EVIDENCE_TO_CLAIMS.md` (or a functionally equivalent section) for those claims with:

- rich source evidence;
- the interpretive move;
- the narrowest candidate claim;
- what the evidence does not establish;
- possible document use.

Do not require this for every CV fact or straightforward teaching instance. The inventory remains the accuracy ledger; the bridge makes the reasoning inspectable.

**Never fabricate plausible details.** The cost of asking is one line; the cost of inventing is the application carrying claims that won't survive author or committee scrutiny. The seven common drafting mistakes (in `Bloch_Application_Context.md`) inform what facts to verify — especially mistake #2 ("non-traditional" — verify she IS traditional in her field) and the timeline-inflation pattern around tool-building start dates.

### Source registries (June-specific paths; resolve via working CLAUDE.md)

For book-relevant work and recurrent applications, PIPELINE Step 0.5 lists specific source paths under `~/Documents/GitHub/recognition_sentience/` and `~/Documents/GitHub/profile/`. Read those when drafting research statements that touch the book project.

---

## Stage 1: Pre-draft cyborg conversation (genre-specific)

The four moves come from printpress SPEC Stage 1. This section names the genre-specific framings, gates, and outputs. **The conversation IS the work, not preparation for it** — DRAFT_PLAN.md is residue, not purpose. If the conversation didn't change the agent's understanding, it didn't happen yet.

### Pre-conversation gate: analytical mode (PIPELINE top, INSIGHTS.md)

Before any move, read `~/Documents/GitHub/cyborg-methodologies/INSIGHTS.md`, the 2026-04-29 entry on "Pattern-matching as relational tracing, not similarity-clustering."

**Why this is required, not optional:** AI default is similarity-clustering ("what's like what's already here") — produces credential-listing letters with confrontational alignment-announcing frames. The cyborg-distinctive move is connection-following: what conversation gets staged, what opens up, what threads get picked up. Skipping INSIGHTS.md collapses Stage 1 into feature-overlap planning. Self-check: can you articulate the difference in one sentence? If not, go back.

### Move 0: Fit evaluation (PIPELINE Step 1) — runs before Move 1

Write a fit assessment, save at top of draft or in app folder:

- **Direct matches**: requirements June meets with existing experience
- **Bridgeable gaps**: gaps she can credibly bridge, plus the bridge
- **Real gaps**: what the role asks for that she doesn't have
- **Verdict**: Strong / Decent / Weak

**If Weak: STOP. Tell the author. Do not draft.** Recommend a better-fit alternative. Drafting weak-fit applications is wasted effort and trains the system on misalignment.

### Move 1: Candidate framings (printpress SPEC Stage 1 Move 1, contextualized)

Surface 2–4 framings for the academic position. For each, name:
- **What June's work opens up** for this department's intellectual conversation (not "skills she brings" — what becomes newly possible if she's part of it). Forms: convergence, thread-uptake, productive tension, surprising opening (per PIPELINE Step 3.7).
- **What thread her work picks up** in the department's existing conversation. Not "we both care about X" — "they're asking [specific question]; her [specific work] is one way that question gets answered."
- **candidate for the question they haven't asked for this application**: what framework is this field/institution treating as given, that her work reveals as the problem?

Examples per PIPELINE Step 3 (note the research-register vs application-register table there):
- AI: the measurement framework constitutively forecloses what it can perceive
- Assessment: the output format IS the bias (binary classification is the bird that isn't a bird)
- NAIS/archaeology: Indigenous knowledge doesn't supplement Western categories — it replaces them
- Teaching: "did this student cheat?" → cheating is signal, not violation
- Trans studies: the Genocide Convention's exclusion of gender groups IS the mechanism of non-recognition

Don't pick yet. Present the field. Move 1 opens; Move 2 takes up.

### Move 2: Author names the story (printpress SPEC Stage 1 Move 2)

**The agent does NOT generate a candidate here.** Open with a question, listen, reflect back. The author names what's load-bearing the agent couldn't see from posting/profiles alone — a fieldwork moment, a politics she wants visible, a tool whose origin matters here, a refusal of a frame. For academic applications, this is often a fieldwork scene (the question-they-haven't-asked move, the moth moment, the Penobscot painting, the cemetery), a tool-origin scene (Autograder's first deployment, Reframe's framework-suppression detection), or a structural-conditions scene (the strike, the Cabrillo conditions).

Failure mode: if the agent answers for the author, it's collapsing the relation. Recovery: ask. The author's redirect IS the leap.

### Move 3: Arc proposal under genre conventions (printpress SPEC Stage 1 Move 3, academic-CL gravity)

Distinguish formal parameters (non-negotiable: word limits, required address-this-clause moves in the posting, attachment requirements) from genre conventions (creative space — academic CL has reading defaults that can be intentionally broken to make things land harder).

**Academic CL conventions to work with or against:**
- Opening paragraph signaling fit + scholarly identity within first 4–6 sentences
- Research / teaching / service tripartite structure (or four with equity)
- "I am applying for…" boilerplate is genre-default; departure is allowed if the opening earns it
- Closing references statement and availability for interview
- Density is fine — committees expect it. Don't artificially compress to a tech register.

**Anti-pattern to flag at this move:** confrontational alignment-announcing. "Your department was created to upend X. I have been upending X." Don't tell the committee what they believe. Write into the conversation they're already having; let them recognize their own values in the work. (PIPELINE Step 3.7 anti-pattern; PIPELINE Step 4.5 collaborative register check.)

### Allocation table (PIPELINE Step 1.5) — settle within Move 3 for multi-doc applications

Academic applications typically require CL + RS + TS + DS. **The cover letter is the BRAID** — it weaves strands from the other documents into a new argument at their intersection, not a miniature version of each. Each concept/story/example gets ONE full treatment in one document; others reference it briefly.

Build the allocation table BEFORE drafting any document. PIPELINE.md Step 1.5 has a starting template with rows for Pvlvcekolv moth moment, Autograder bias finding, normative gravity, emergency flex weeks, survival architecture, "Ethnic Studies is a Strike," beaded arrow story, identity/positionality. **Customize per application** — don't reuse the template wholesale. The table prevents the redundancy spiral (normative gravity re-explained 4 times, Autograder described in every doc).

For grant-style structured forms, rows become the form's prompts (Q1, Q2, Q3) rather than separate documents. (Same anti-redundancy logic; different unit. Academic apps rarely use this variant — it's listed for completeness.)

### Identity architecture and project selection — when the record has several strands

Before drafting, distinguish:

- the established scholarly core;
- a current extension or method;
- an independent present research program where applicable;
- the proposed institutional expansion;
- candidate comparisons that remain hypotheses rather than identity claims.

Then distinguish **content abundance** from **program abundance**. Content abundance supplies scenes, evidence, and prose for the long assembly. Program abundance is a set of possible projects or futures and must be selected in Stage 1. Record the candidate reservoir, selected packet strands, longer horizon, and deliberate exclusions. Do not send every credible project into Stage 2 and expect prose cutting to make a coherent research program.

### Move 4: Section beats and load-bearing specifics (printpress SPEC Stage 1 Move 4)

From FACT_INVENTORY.md, any claim bridge, and the allocation table, name what each section carries. Which scenes, which numbers, which scholars cited *doing work* not name-dropped, which prior phrasings to mine from voice-final priors. What is deliberately NOT included and why. Extract unresolved author comments into the plan's decision/source-retrieval queue; a comment never enters prose merely because it lives in a working document.

### Intellectual landscape research (PIPELINE Step 3.7) — feeds Moves 1 + Stage 3 swarm

**Required reading first:** `~/Documents/GitHub/cyborg-methodologies/INSIGHTS.md` (relational tracing). Skipping this collapses 3.7 into similarity-clustering — agent surfaces feature-overlap candidates because it never did the relational tracing that gives it material to think with.

**The two organizing questions:**
1. What does June's work *open up* for them? (What becomes newly possible in their conversation if she's part of it.)
2. What threads in their work does her work *pick up*? (Where does her work join a conversation already underway?)

Same operation in two directions. Both questions matter — together they map the relational field, not the feature overlap.

Relational tracing is not limited to faculty. Where the work requires it, map four interlocutor groups: community knowledge-producers; scholarly traditions; students and collaborators; and institutional/departmental communities. For each major paragraph or strand, ask: who besides the applicant acts, whose question or practice changes the inquiry, what conversation is being entered, and what distinct contribution does the applicant make? This is how the packet presents participation in a discourse rather than a lone individual surrounded by names.

**Operation for academic positions:**
1. Identify search committee chair + 3–5 faculty whose work is closest to June's intellectual conversations (not just keyword-matching the CV).
2. Use Semantic Scholar / department websites / training data for recent publications and research focus.
3. For each relevant faculty member, work the two questions. Forms the relational tracing can take: convergence, thread-uptake, productive tension, surprising opening. Not every faculty member will have a meaningful relation — don't force it. Forced similarity-matching is what produces credential-listing letters.
4. Note department gaps as "what conversation are they not yet having that her work could start" — not "what skill do they lack."
5. Note recent hires and direction of travel.

**Output two documents:**

- **`[AppFolder]/DEPARTMENT_PROFILE.md`** — the research itself: faculty, gaps, structural questions, recent hires. Used by Stage 3 swarm to anchor personas.
- **`[AppFolder]/INTELLECTUAL_CONNECTIONS.md`** — a brief for the author, written as intellectual introduction, not fit justification. For each relevant person/team: what they work on, what structural question they're asking, what threads of theirs the author's work picks up, what her work opens up. The author keeps and reads this; she may follow up on the work herself.

**How this shapes the draft:** The letter thinks in a register that recognizes the department's questions. Don't quote faculty websites. Don't announce "your department values X and I do X." Faculty research is input to the register, not content in the letter. Impressionistic and gestural — evoking shared intellectual terrain, not citing it.

### DRAFT_PLAN.md output (printpress SPEC Stage 1)

Save to `[AppFolder]/DRAFT_PLAN.md` using `templates/DRAFT_PLAN_TEMPLATE.md`. Captures: arc, openings/uptakes, the question-they-haven't-asked reframe, section beats with grounding, allocation table, identity architecture and project selection where relevant, unresolved-comment queue, what we're deliberately NOT doing, swarm composition, and conversation notes. It also records that the author sees the full assembly and supplies selection input before any autonomous cut. Granular `KEEP / DROP / UNSURE` marking is the default; after seeing a multi-document packet whose scale makes marking itself a cutting assignment, the author may explicitly choose the reversible proposition-level merge described in printpress Stage 2. The selection route remains an experiment.

**Failure modes to watch for** (PIPELINE Step 3.8 learning-loop section):
- *Approval-seeking framing*: agent presents arcs as "is this OK?" rather than thinking with the author. Recovery: restate the move — surfacing the field for joint decision, not asking for approval.
- *Directive extraction without understanding-shift*: author says "draft from this" before the conversation actually shifted the agent's understanding. Recovery: name what changed before drafting. If nothing changed, the conversation didn't happen.

**When to skip legitimately:** very short documents (cold-outreach emails, statements under 300 words) where structure is constrained enough that the conversation collapses. Even then, name the arc in one sentence before drafting.

---

## Stage 2: Drafting (genre-specific)

Draft from `DRAFT_PLAN.md`. Step 2 executes the plan; it does not re-plan. If structural decisions arise that aren't in DRAFT_PLAN.md, surface them in conversation before deciding solo.

### Read the actual posting before writing a sentence (PIPELINE Step 4)

Re-read POSTING.md and APPLICATION_STRUCTURE.md (if present). The document responds to:
- The exact prompts/questions as written (for grants/structured apps; rare for academic but happens)
- Posting-specific instructions ("address how your teaching advances X department's commitment to Y" — that clause sets a required move; ignoring it weakens the application even if the rest is strong)
- Word/character limits per section
- Required content elements named explicitly (research plan, specific population, methodology, named partnerships, named outcomes)

**The failure this prevents:** a high-quality generic version of the document type that doesn't answer what the posting asked. Reviewers grade against the prompt; a beautifully-written non-response loses to a competent direct response.

### Audience calibration (PIPELINE Step 4) — Academic bucket

Academic apps use the **Academic** calibration:
- Lead with disciplinary credentials.
- Reframe = research project, not a product.
- Full scholarly register. Dense is fine.
- Don't shift to tech register; don't compress academic jargon that's load-bearing.

(Other PIPELINE Step 4 buckets — Fellowship, Tech, AI welfare, EdTech — apply to other genres; reference PIPELINE.md if the application straddles. For straddling cases, ask the author rather than guess.)

### Word count targets (PIPELINE Step 3.5)

| Document | Target |
|---|---|
| Cover letter | ~1,200 words (open-rank may be longer) |
| Research statement | ~2,000 words |
| Teaching statement | ~1,200 words |
| Equity / diversity statement | ~900 words |

These are targets for the *final* document, not for the assembly or the author handoff. Capture genuine abundance—provisionally around 1.6× where a real target exists—then show the complete assembly to the author. The default selection input is keep / drop / unsure marking. For a multi-document packet, the author may instead explicitly authorize the reversible proposition-level merge in printpress Stage 2 after seeing the full scale; unmarked material remains `UNSURE`. Then choose an inspectable selection route. The provisional ~1.2× handoff is an experiment intended to leave room for author additions, not a requirement and not evidence that AI cutting is sufficiently good.

### Cutting swarm composition (Stage 2 — only when the post-marking route includes AI cutting)

**Deliberately not the same as Stage 3's persona stack.** Stage 3 anchors 3–5 personas to specific, real, named faculty from `DEPARTMENT_PROFILE.md` (per `critic-swarm/personas/academic_position/README.md`) — that's the right design for a live quality review with you present to weigh individually-textured reactions, but too narrow and too heavy for an autonomous cutting pass: any single named faculty member's specific tastes could wrongly drive what gets cut, and five separate dispatches is more than cutting needs.

If this route is chosen, core readers are: **one composite department-reader persona**—briefed with the department's stated commitments and the documented range of faculty concerns—plus **author-informed**. They receive `ASSEMBLY_MARKS.md`. Their output is a proposed handoff plus diff; it cannot delete `KEEP` material or treat `UNSURE` as permission.

Optional (RS/dossier-length documents, where a single composite reader's judgment is thin relative to the document's length): a second composite department-reader dispatch, briefed the same way, for cross-check.

Excluded: intelligibility, jargon (stay Stage 3/4).

### Voice-check during drafting (printpress SPEC Stage 2)

Voice-check runs throughout, not just before/after. **The pre-draft work is where agents consistently under-execute.** See printpress SKILL.md § Stage 2 for the full HOW. For academic_position specifically:

- **Read the profile with the Read tool, not python extraction.** Read `stylometry.style_notes` and `qualitative.checks` filtered to `pre_draft` role in full text; do not truncate or summarize. Read `genres.academic_position` in full (description, threshold_overrides, genre_moves, qualitative checks specific to this genre).
- **Voice-final priors are SOURCE prose, not comparators.** Per Stage 0 § "Pull-from-prior priority": when a closely-related voice-final prior exists (a submitted CL/RS/TS from the same track), read it in full and identify which sentences, paragraphs, and section beats will be adapted into the current document. **Drafting an academic_position document is primarily adaptation of voice-final prior prose; new prose is written only for genuinely new material.** The agent-shaped-prose failure mode is what happens when this step is skipped.
- **Begin Stage 2 by listing in DRAFT_PLAN.md** (or in chat if DRAFT_PLAN.md is already locked) which specific prior passages map to which sections — author name, file path, paragraph identifier. Without this list, the default move is to compose from scratch and produce agent-shaped prose that passes the contamination linter but doesn't sound like the author.

Write in voice from the start.

Williams's *Style: Lessons in Clarity and Grace* applies continuously (encoded in profile as `williams_concision`, `patterns.wordy_phrases`). Especially load-bearing during compression: most "I can't cut more without losing meaning" moments are verb-to-nominalization conversions, redundant qualifiers, or relative-clause sprawl that can tighten to verb forms.

Self-run quantitative check after each substantive draft. **Silently fix contamination** (hedges, jargon, padding, self-aggrandizing frames). **Surface structural/qualitative findings as suggestions**, not corrections. Don't run voice-check on documents the author has already edited — her edits are ground truth and train the profile.

### What the 2026-08 research established — read before drafting

*Added 2026-08-09. Restated here rather than only referenced, because Stage 2 dispatches cold subagents that see only their brief. **Put these in the brief.** Full sourcing: `_application_evidence/` and the `academic_position` / `cover_letter` blocks of the voice profile.*

**The status rule, first.** Every item below is **convention** (what readers have been exposed to) or **hypothesis** (untested testimony) — never finding. **No study anywhere measures whether application-document quality affects shortlisting.** Two independent searches confirmed the void. Carry the status; a frequency is never an efficacy claim.

**Who is being cited below, and why they count** — you have no context on these names, so here it is once:
- **Wang (2023)** — analysed 100 teaching philosophy statements written by faculty who *won* university teaching awards. Outcome-selected corpus; the strongest genre evidence available.
- **Lamont** — sociologist who observed twelve real funding panels and interviewed 81 panelists within days of their deliberations, including at ACLS. The only ethnography of academic panel judgment that exists.
- **Tardy** — applied linguist whose book studies when departures from genre convention read as skilled versus as error.
- **Roche** and **Rosati** — the only two named people who have written first-person accounts of serving on humanities fellowship selection committees. Roche served on an ACLS panel; Rosati was both a National Humanities Center fellow and a member of its selection committee.
- **Williams-Jones** — a named academic who has served on more than a dozen hiring committees and was hiring at the time of writing.
- **Kelsky** — the most prescriptive advice writer in this space, roughly eleven search committees, some chaired. **She also sells application editing, and much of the circulating advice online originates with her** — so agreement with Kelsky elsewhere is usually just Kelsky again, not corroboration. Never treat her as a tiebreaker against a committee member.
- **Bhatia** — the linguist whose analysis of application letters is the origin of most move-structure work on this genre.

1. **The part of the letter that makes the case — what genre analysts call the *argument move* — is where letters fail, and it is the whole game.** Three independent corpora converge: writers produce every expected element, then write an argument that restates the previous one and never ties specific capacities to what the posting actually asked for. Checkable form — *background → what that does for them → why this, why now.* Applicants do "background" near-universally and "what that does for them" about a fifth of the time. **Check every capacity named against something this posting literally asks for.** Readers do not infer.

2. **"Generic" means unresponsive to THIS situation, not formally conventional.** A completely standard structure is non-generic if every move does work only this application requires; an invented structure is still generic if it doesn't. Test each sentence: could it appear in a letter to a different department?

3. **Ordering is free — structural variation is inside this genre, not a departure from it.** Bhatia said so; multiple corpora found reordering with no loss of communicative purpose. Only the request and close have a stable position (together, at the end).

4. **How much the letter must explain is a function of the department, not of taste.** If several people there share June's subfield, they translate her significance for the room and the letter can be spare. If she'd be the only one, **the letter carries the vouching itself.** Answer this in `DEPARTMENT_PROFILE.md` (PIPELINE Step 3.7 "Local reading conditions") before drafting.

5. **Absence gets read even where presence doesn't.** A letter with no mention of collaboration, student supervision, or committee service reads as "loner, not a team player" (Williams-Jones, 12+ committees). Independently mirrored in tech hiring, where one source discounts letter *content* but treats letter *absence* as lack of effort.

6. **Teaching statements have a measured skeleton.** From 100 statements by faculty who *won* teaching awards (Wang 2023): describe teacher actions (99/100) → generalize beliefs and principles (98/100) → **justify the reasoning behind the actions (86/100)**. Mean **704 words**. What award-winners rarely do: **express commitment or passion — 13 of 100**; showcase their own accomplishments — 29; narrate their own path — 42. The centre of gravity is the classroom and the reasoning, not the autobiography.

7. **Submit exactly what is requested.** Berkeley eliminated 76% of applicants on a single document; one district states in policy that unrequested extras will not be considered. Where a search publishes a screening rubric, **it outranks everything in this config.**

8. **Deviation is priced by standing, and this is the go/no-go on any unusual structure.** Tardy: assessors judge norm-breaking as transgressive where peers judge it innovative, and *"it is typically only the students who have already demonstrated such mastery who are granted the opportunity to innovate."* Lamont, from panel observation: *"innovators are often penalized if they go too far in breaking boundaries."* Kelsky prescribes a "business card" opening with no accomplishments — which forbids a story-first opening outright. **Do not resolve this by default. Surface it to June.** The likely diagnosis of why story-first hasn't felt right is *placement*: a story with nothing before it is a payoff with no setup. A short payoff-setup paragraph first fixes it, and small-and-motivated is what expert genre-bending actually looks like.

9. **Between-search variance is enormous — read this before applying 1–8 as rules.** Six documented contradictions among sources who all have real committee standing: two R1s where one reads letters first and the other never until finalist stage; length guidance spanning one to four pages; naming specific faculty advised by *Chronicle* guidance and forbidden by a UNC chairs' panel. **No single rule survives it.** Confident advice about academic letters describes one committee's practice.

10. **Three fabricated screening statistics — never repeat, and check origination.** "75% ATS auto-rejection" → a 2012 vendor product launch. "10–20 seconds per application" → cited to a Berkeley page that doesn't contain it. "30 seconds on the research paragraph" → Kelsky 2017, no citation, contradicted by a source saying materials get 5–30 *minutes*. **There is no established reading-time figure.** And repetition is not corroboration: one committee member's page-count guidance turned out to hyperlink Kelsky.

11. **Hard gate for California community colleges.** June's anthropology PhD clears the Anthropology minimum qualification. It does **not** clear Ethnic Studies or Religious Studies — those need a board-granted equivalency, **not portable between districts**. Applied by HR before any faculty member reads. Check at Stage 0; it is go/no-go.

### The seven common drafting mistakes (Bloch_Application_Context.md)

Check during drafting, not just at QC. One-line each; full descriptions in `Bloch_Application_Context.md`:

1. Treating academic and tech work as separate tracks
2. "Non-traditional" framing (flattens her credentials)
3. Precarity as backstory rather than design condition
4. Softening political language ("concerning developments" for "police state")
5. Separating disability from design
6. The "journey" or "pivot" frame
7. Calling Reframe a chatbot

These are flagged on every academic_position draft. The author-informed reviewer in Stage 3 catches them as failure patterns; agents drafting should catch them upstream.

### Anti-generic test (PIPELINE Step 4 rule 1)

If a sentence could describe any scholar with a PhD and some tech experience, delete it. Specificity is the constraint layer.

### Sentence-level rules (Bloch_Application_Context.md "Sentence-Level Writing Rules")

Ten rules from CDA of UB application revision (April 2026), encoded in voice-check profile and discoverable there. Flagged here so drafting agents know they exist; full list lives in `Bloch_Application_Context.md`. Especially load-bearing for academic_position: rule 8 (constructivist framing — knowledge from practice, not "I discovered"), rule 4 (tools by what they REPLACE, not abstract description), rule 6 (categorical modality for evidenced claims).

### Never invent numbers (PIPELINE Step 3.5)

If you don't have evaluation scores, publication counts, or dates, use `[DATA NEEDED]` tokens. Inventing plausible numbers is the highest-risk failure mode — a committee that catches inflated numbers will distrust the entire application. The Reframe timeline (tool-building started ~November 2025) is a recurring inflation point — verify against `Bloch CV.docx` and `Bloch_Application_Context.md`.

### Format (PIPELINE Step 4)

Academic narrative documents: `.md` draft → becomes `.docx` with letterhead. Final documents use HTML templates (per working-dir CLAUDE.md, "Document generation and templates"). Match format of closest prior application. Academic CVs and reference lists are author-handled.

---

## Stage 3: Reviewer swarm (invoke /critic-swarm)

### Pre-swarm: reader takeaway audit (PIPELINE Step 4.7)

Before invoking the swarm, write `[AppFolder]/READER_TAKEAWAYS.md` — 5–8 things the reader should know about the author by the end of this document, distributed across identity, scholarly contribution, teaching, fit. Then read the draft against the list:

1. Does each takeaway land? If essential but only implicit, surface it.
2. Does anything in the document NOT serve a takeaway? Candidates for cut.
3. Are takeaways in the right weight? Buried high-priority needs to move forward; over-weighted low-priority needs to compress.
4. Is structural balance right for the genre? Teaching-focused VAP letter where teaching only appears in the last 25% has a balance problem.

This is the editorial pass that answers "what should I cut?" non-arbitrarily. Save the list — useful for the learning loop and for future similar applications.

### Persona stack

**Stack name:** `academic_position` (per /critic-swarm SPEC).

Personas anchored to actual faculty from `DEPARTMENT_PROFILE.md`. The agent prepares deep-enough reads of each faculty member's scholarship to give the persona teeth, then passes that context to /critic-swarm.

### Context passed to /critic-swarm

- The draft(s) (file paths)
- `POSTING.md` — verbatim, the actual posting (not a description). Critical: feed personas the actual posting so they catch where the document mismatches what was asked for, not just what an ideal reader would flag (PIPELINE Step 5.7).
- `DEPARTMENT_PROFILE.md` — for faculty-anchored personas
- `INTELLECTUAL_CONNECTIONS.md` — for relational-tracing context
- The application folder path — for any per-application context the swarm might want
- Author profile path (if set up) — for the author-informed reviewer

### Always-runs reviewers

Intelligibility, jargon (venue-aware, interdisciplinary if applicable), author-informed (profile-gated). These run regardless of stack — handled by /critic-swarm. /printpress doesn't specify these; just ensures the author profile path is set up or skipped.

### Synthesis output (handled by /critic-swarm)

Cut list first → convergent flags (3+ reviewers) → threading suggestions → specialty insights → mechanical flags. /printpress passes synthesis to Stage 4.

---

## Stage 4: Revision (genre-specific)

### Sequential workshopping (PIPELINE Step 5.5)

ONE revision at a time. Not four full documents. Not a batch. One change, one approval, next change. Prevents overwhelm escalation.

**Exception: structural revisions integrating substantive new content** (a new theoretical move, a structural reframe, new domain material). Batch the integration — preserve prior version as checkpoint, let the author read V[N+1] as a whole. Sequential one-at-a-time is for fine-grained edits and word-count compression.

**Content first, word counts later** (PIPELINE Step 5.5). Lock content first; treat compression as separate downstream phase. Compressing prose before content settles wastes effort — author will likely cut other things or restructure on read-through.

### Drafting & revision principles (printpress SPEC Stage 4)

Apply continuously, not as final-pass checklist:
- **Less is more.** Removing material that isn't necessary — even when good — often makes the draft stronger.
- **Strategic, not exhaustive.** Author's context is input for judgment about what's load-bearing, not a checklist to cram in.
- **Action verbs with clear agents.** Convert nominalizations to verbs; make actors explicit.
- **New information after the verb, not in the noun phrase.** Stress position at sentence end.
- **Simplify sentence structure for complex ideas.** Embedded clause chains usually mean an idea wants to split.
- **Reader orientation at section boundaries.** New sections need a sentence orienting where you are in the argument.
- **Workshop language in chat, not in file.** Decide phrasing in conversation, then commit; don't churn the file with exploratory rewrites.

For academic_position specifically:
- Word-count compression after content lock.
- **Never cut political directness.** "Police state," "genocide," "ruthlessly exploitative" stay. Framing/placement may shift; content does not soften.
- **Never invent numbers.** Use `[DATA NEEDED]` over plausible fabrication.
- **Don't re-run voice-check to modify documents the author has already edited.** Her edits train the profile; running voice-check on her edits would revert them.

### Address convergent flags from /critic-swarm first

Convergent flags (3+ reviewers) are load-bearing-but-at-risk pieces. Address them before specialty insights or mechanical flags. Specialty insights (single-reviewer) are held for consideration — don't average them away into the convergent set, but don't auto-fix either.

### Overwhelm detection (printpress SPEC Stage 4)

Increasing typo density signals overwhelm. Shift to:
- Shorter responses
- Targeted questions instead of more draft text
- Simpler language without reducing depth
- Explicit check-in: "Should we pause on this and come back?"

### Logging to LEARNING_LOG.md (printpress SPEC Tier 1)

After Stage 3 synthesis is addressed, log to `[AppFolder]/LEARNING_LOG.md`: what convergent flags surfaced, which persona prompts produced sharp critique vs. shallow, what spec refinements would help. Tag each learning as `genre-specific` or `potentially-generalizable` (printpress SPEC cross-genre generalization).

---

## Stage 4.6: Requirements Compliance Gate

Before declaring materials ready, run the cross-genre **Requirements Compliance Gate** (printpress SKILL.md § Stage 4.6): re-fetch the live posting/form, diff against `APPLICATION_STRUCTURE.md`, and verify every required document, limit, prompt/section/field, and submission convention is met. Any unmet or changed requirement blocks "ready" — the author can override explicitly. Backstop to the Stage 0 Submission Requirements Ledger.

---

## Stage 5: Save + post-submission

### Mechanical cleanup (PIPELINE Step 5.9)

After the author's final edits, dispatch a haiku subagent on the final `.md` (NOT `.html` — see `feedback_voicecheck_html_workflow.md`). Subagent prompt template at PIPELINE Step 5.9. Catches typos, double spaces, em-dash inconsistency, missing serial commas, doubled words, malformed markdown. Does NOT do voice/structural/register/clarity changes.

Apply flagged corrections one at a time with `Edit`, verifying each — author's text is ground truth, haiku can flag false positives. Don't show the report to the author unless something is genuinely ambiguous.

### Save protocol (PIPELINE Step 6)

1. Save draft(s) to the application folder.
2. Ensure `DRAFT_PLAN.md` is in the folder. The "Conversation notes / what happened" section is filled in before save (per-use learning capture).
3. **Append a row to `[AppFolder]/VERSION_LOG.md`** — one row per transition, copy `templates/VERSION_LOG_TEMPLATE.md` if the file doesn't exist. Columns: `From | To | Type (structural/fine-grained) | Author (AI/June/June+AI) | Notes`. Notes column: one sentence on what *the pass was trying to do* + word-count delta. The voice-check learning loop reads this directly via `--manifest VERSION_LOG.md`.
4. **After submission, save `*_final.md`.** The markdown text of the final document lives in the folder as `*_final.md` (e.g., `COVER_LETTER_final.md`). Don't leave only HTML/PDF — those are render artifacts; the markdown is source. Future agents adapting from this application need an unambiguous source.
5. Save/update `[AppFolder]/APPLICATION_CHECKLIST.md` — done vs. needs-author-review.
6. Update `Applications_Tracker.md` status (per working-dir CLAUDE.md).

### Voice-check learn pass (PIPELINE Step 7)

Don't improvise — follow `LEARNING_LOOP_PROCEDURE.md` (canonical procedure: prerequisites, version manifest construction, genre stylometry bootstrap, sequence-mode invocation; mechanical script-running and qualitative CDA work belong in *separate sessions*).

Quick reference:
- **Single-pair** (one agent draft → one final): `python3 writing_check.py --learn FIRST.md FINAL.md --genre academic_position [--notes "..."]`
- **Multi-version** (5+ revision drafts): `python3 writing_check.py --learn-sequence --auto-discover . --pattern "..." --manifest VERSION_LOG.md --genre academic_position`
- Always use `.md` source, never `.html`
- Always specify `--genre` to prevent genre-adaptive shifts from contaminating the user voice baseline

**What this is NOT:** an excuse to re-edit docs the author has already revised. Her edits are ground truth. The loop learns FROM her edits to produce better first drafts next time.

### Post-submission workflow (PIPELINE post-submission section)

Operational logic — author-specific (June's job-search workflow), reference PIPELINE.md for full procedures:
1. Update `Applications_Tracker.md` — status → "Submitted," record date and materials sent.
2. Archive materials: `python3 save_materials.py <file> "<app_name>" --doc <type> --track <track>`.
3. If author is excited about the position, generate interview prep doc from `templates/interview_prep_template.md`.
4. Calendar reminders (Gmail MCP + Google Calendar): **4–6 weeks for academic** (academic searches are slow). Drafts only — never send without author approval.
5. Follow-up cadence — academic: 4–6 weeks if no confirmation. Templates in `templates/follow_up_emails.md`.
6. When interview scheduled: update tracker, generate `[AppFolder]/INTERVIEW_PREP.md`, research institution/team/interviewers (Semantic Scholar + WebSearch), read most similar prior interview prep, identify gaps to be honest about and prepare framings.
7. After interview: thank-you within 24 hours, fill debrief in interview prep doc, log interviewers and key themes, set 2-week follow-up reminder.
8. Offer: research salary norms for discipline; negotiate course load, startup funds, research support.

### Skill-global writes (printpress SPEC Tier 2)

After Stage 5:
- Update `~/.claude/skills/printpress/genre_configs/academic_position.md` with refinements (this file). Periodic genre review per printpress SPEC: every 3rd–5th use, surface at Stage 0: "You've used academic_position N times since the last review. Shall we do a quick genre config update? (5 minutes, can skip.)"
- Tagged-generalizable learnings from Stage 4 LEARNING_LOG.md feed cross-genre principles per printpress SPEC.

---

## Subgenre notes (for future)

`academic_position` v1 spans:
- R1 research-focused (Emory, U Buffalo AI Society)
- Teaching-focused VAP / lectureship (LMU WGS, Hamilton WGS, Berkeley Anthro Lecturer, UCSC CRES)
- Religious studies / interdisciplinary (Harvard Divinity AI Religion)
- NAIS / Indigenous studies — relational register foreground

These have meaningfully different swarm composition needs. Research-focused applications want a swarm anchored more heavily in the candidate's research-area faculty; teaching-focused VAPs want a swarm with pedagogy-oriented faculty + a teaching-letter reader who reads for course design and student-facing voice; religious studies / interdisciplinary apps need register-bridging readers (theology + STS + Indigenous studies depending on the angle).

Per printpress SPEC's "Genre splitting" guidance: hold as one genre with subgenre tags pending the periodic review trigger. When recurring swarm composition differences accumulate that subgenre tags don't resolve cleanly, design a split with the author.

Subgenre auto-detection candidates (for v2): posting language ("primarily a teaching position," "tenure-track research-active," "interdisciplinary across religious studies and…"), required document weighting (RS-heavy vs. TS-heavy), institutional type (R1 vs. SLAC vs. HSI). v1: ask the author at Move 3 if not obvious.

---

## Learning loop notes

[Empty for v1 — populated through use. Genre config refinements come from periodic genre review per printpress SPEC. First refinement candidate: subgenre tagging once recurring composition differences accumulate.]
