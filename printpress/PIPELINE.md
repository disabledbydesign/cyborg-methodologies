# Application Drafting Pipeline

> **Status note (2026-05-07):** PIPELINE.md is now documentation, not the executable workflow. To draft an application, invoke `/printpress` (a genre-parameterized skill at `~/.claude/skills/printpress/SKILL.md`). The genre configs at `~/.claude/skills/printpress/genre_configs/[genre].md` reference this document by step number for local data (source registries, track lookup tables, the seven common drafting mistakes) — those references depend on the section numbering staying stable, so the structure here is preserved. PIPELINE.md remains canonical for the steps it documents and June still actively edits it; read it when you need the rationale or examples behind a workflow step.

**For any agent starting a new application draft.** Read this, then follow the steps. No complex prompts needed — June just says: `Draft [Application Name]` or `Next application` and you check the tracker.

---

## Analytical mode (read first — sets how you read everything else)

**`~/Documents/GitHub/cyborg-methodologies/INSIGHTS.md`** — read the 2026-04-29 entry, "Pattern-matching as relational tracing, not similarity-clustering," BEFORE the five required-reading documents below.

**Why this is here, not in Step 3.7:** INSIGHTS.md sets the analytical mode for everything that follows — fit evaluation, fact assembly, intellectual landscape, draft plan, drafting. The default AI move (similarity-clustering — "what's June's work like in their conversation?") produces credential-listing letters, alignment-announcing framings, and feature-overlap planning. The cyborg-distinctive move (relational tracing — "what conversation gets staged, what opens up, what gets taken up?") produces planning that thinks WITH June and the audience rather than matching FROM June TO them. Buried in Step 3.7, this requirement gets skipped any time planning happens from a different door (a draft-plan conversation, a fit eval, an intellectual-landscape sketch). Hoisted here, it conditions every step.

**Self-check before proceeding:** Can you articulate the difference between similarity-clustering and relational-tracing in one sentence? If not, go back to INSIGHTS.md.

---

## Before you write a single word

**Read these five documents. The detail is the constraint layer.**

1. **The posting — and its prescribed structure.** Check the application folder for `POSTING.md`. If none exists, WebSearch → WebFetch → save the **complete, unedited posting text** as `[AppFolder]/POSTING.md`. You cannot draft without this.

   **Capture the prescribed structure verbatim, separately if needed.** For grants, fellowships, and any application with a structured form (Q1/Q2/Q3 with specific prompts, word limits, formatting requirements), save those questions/parameters/instructions exactly as written — verbatim, not paraphrased — as `[AppFolder]/APPLICATION_STRUCTURE.md` (or as a clearly-labeled section within POSTING.md). Include: each prompt's exact wording, word/character limits, formatting rules, attachment requirements, and any explicit guidance to applicants.

**⚠⚠ CAPTURE THE FUNDER'S PUBLISHED EVALUATION CRITERIA, VERBATIM — added 2026-08-09. This was the largest gap in the pipeline.**

Required *materials* were being captured; the *criteria the work is scored against* were not. Those are different things. Where a funder publishes its evaluation criteria — or its instructions to reviewers, or a scoring rubric — **those outrank every general heuristic in this pipeline.** They are the actual standard, stated by the people deciding, for this specific competition.

Capture them **verbatim** into `APPLICATION_STRUCTURE.md` under a heading of their own, and carry them into three places: the Stage 1 allocation (does the plan address each criterion?), the Stage 2 subagent brief (a cold drafting agent sees only its brief), and the Stage 3 swarm (`/critic-swarm` permits exactly one scoped lens to map the artifact against named external criteria — see its SKILL.md carve-out; fold it into the program-officer persona).

Two things this catches that nothing else does:
- **Criteria a funder does NOT use.** ACLS publishes clarity, intellectual/social significance, quality, and feasibility (training, past experience, plan of work) — and does **not** list originality. A proposal optimized for originality is optimized for an axis that funder does not score.
- **Criteria that favour the applicant and would otherwise go unclaimed.** ACLS instructs reviewers to weigh the record "taking into account relative advantages or constraints on resources… over the course of the applicant's career" — the only such instruction found across seven programs surveyed. Write *into* a criterion like that rather than hoping a reviewer applies it unprompted.

⚠ Guards. **Do not invent criteria** — where a funder publishes none, record that absence, which is itself information about how idiosyncratic the review will be. And **do not treat criteria-mapping as sufficient**: panel ethnography (Lamont) finds panelists routinely decide on grounds beyond the formal criteria — diversity considerations, "elegance," and how a proposal compares to the batch it landed in. The criteria are a floor, not the whole reading.

**⚠ Also capture any AI-use disclosure requirement — added 2026-08-08, and this is a real gap the pipeline has been carrying.** A sweep of funder and employer policies found that where disclosure rules exist, they govern **provenance of substance, not register** — nobody draws the line at "sounds polished," and June's practice (AI-assisted drafting with heavy human revision) sits inside every policy located, including the strict ones. But some are *procedural* and will fail an application if missed:

- **NEH requires footnoted acknowledgement of inserted AI-generated text.** That is a formatting-and-attribution requirement, not a philosophical one, and it was nowhere in this pipeline until now.
- **AI Now** required an AI-tool disclosure at the bottom of the cover letter (June has already encountered this one).
- **LTFF and Coefficient Giving have no findable published policy** — check the live form rather than assuming.

Capture the exact wording into `APPLICATION_STRUCTURE.md` alongside the other requirements, and carry it into the Stage 4.6 compliance gate. Treat a disclosure requirement exactly like a word limit: a hard, checkable submission condition. Full policy survey: `_application_evidence/Hypotheses_Post_AI.md`.

   **Why verbatim matters:** Reviewers grade against the prompt as written. "Describe your research in 500 words" and "Describe how your research advances the field's most important questions in 500 words" call for different documents. Paraphrasing the prompt during capture introduces drift that the agent then drafts toward. Same applies to academic positions with specific instructions ("address how your work advances X department's commitment to Y" — those clauses are draft-shaping, not boilerplate).
2. **Agent briefing**: `/Users/june/Documents/GitHub/profile/JUNE_BLOCH_AGENT_BRIEFING.md` (662 lines). Read the sections relevant to what you're drafting — use the scope table below. You don't need every section for every document.
3. **Voice document**: `/Users/june/Documents/GitHub/disabled_by_design/voice/VOICE_DOCUMENT.md` (625 lines)
4. **Application context**: `/Users/june/Documents/Filing/Job Search/Bloch_Application_Context.md` (quick-ref with 7 common mistakes)
5. **Prior materials — structurally delivered, not just found.** For EACH document type you're drafting, load 2-3 prior versions and explain to yourself what each provides:

   **Briefing scope by document type** (read relevant sections at full depth; skim others for context only):

   | Document type | Priority briefing sections | Skim only |
   |---|---|---|
   | Cover letter | Identity & positionality, Research programs (all), Portfolio overview, Voice | Detailed project descriptions (Reframe internals, Autograder architecture) |
   | Research statement | Research programs (all), Publications, Detailed project descriptions | Teaching, Service |
   | Teaching statement | Teaching, Student stories, Accessibility/disability, Autograder (pedagogical use) | Detailed Reframe architecture, Publications list |
   | Equity/diversity | Identity & positionality, Disability/accessibility, Teaching, Student stories | Detailed project descriptions, Publications list |
   | Tech cover letter | Portfolio overview, Autograder (technical), Reframe (technical), Skills | Extended research narratives, Teaching |
   | Grant/fellowship | Research programs (relevant), Budget/timeline, Portfolio overview | Teaching, Service |

   | Document type | Load these (by application track) | What they give you |
   |---|---|---|
   | Cover letter | Closest prior + one from a different track | **Voice model** (how June writes this genre), **arc model** (how she braids strands) |
   | Research statement | Emory RS, UB RS v4 | **Concept architecture** (how she organizes research programs), **story bank** |
   | Teaching statement | UB TS v5, base 2024-2025 TS (`2024-2025/Bloch Teaching Statement.docx` via graphify-out) | **Voice model** (bell hooks paragraph, student stories), **structure model** |
   | Equity/diversity | UB ES v4, UCLA diversity, Cornell diversity | **Voice model**, **story bank** (arrow, cemetery, Penobscot painting, student petitions) |

   **Write FROM these materials, not from the briefing doc's description of June's work.** Reorganize rather than regenerate. The least revision of pre-existing material while still communicating the arc, the better. The briefing doc tells you WHAT June does; the prior materials show you HOW SHE WRITES ABOUT IT. The difference is texture, humor, pacing, specificity — everything that makes the output not generic.

   **Enforcement checkpoint:** Before you begin drafting each in-scope narrative document, name (in your thinking or in a note): (a) which prior materials you loaded, (b) what each gave you (voice model, story bank, structure model, arc model), (c) which briefing sections you read at full depth. If you cannot answer all three, you skipped this step — go back. Reference lists are always author-handled, and academic CVs default to author-handled. A résumé enters drafting when the application requires one unless June explicitly takes it over.

   Track-specific closest-match lookup:
   - R1 NAIS academic → `Emory/` or `U Buffalo AI Society/`
   - WGS VAP / Women's & Gender Studies → `LMU WGS VAP/` or `Hamilton WGS VAP/`
   - Teaching-focused lecturer → `Berkeley Anthro Lecturer/` or `UCSC CRES Lecturer/`
   - Religious Studies / AI & Religion → `Harvard Divinity AI Religion/`
   - Tech/industry → `Netflix/` or `GitLab/`
   - AI ethics/safety fellowship → `Anthropic Fellows/` or `Constellation Astra/`
   - EdTech → `VictoryXR/`, `ETS Research Scientist Equity/`, or `Turnitin/`
   - AI welfare/safety → `Anthropic Fellows/`
   - Grant/fellowship (anthropology) → `Wenner-Gren Hunt Fellowship/`
   - Grant (AI/tech) → `SFF/`, `LTFF/`, `Coefficient Giving/`

   **How to find the right version inside the folder** (don't make June pick — pick correctly):
   1. Check `VERSION_LOG.md` if it exists — the last row marked submitted (or the highest version with type `fine-grained` and `Author: June` or `June+AI`) is the voice-final version.
   2. Otherwise: `ls` the folder, take the highest-numbered version with `_final`, `_voicefinal`, or `_v[N].md` (latest N) — June's convention. Ignore agent-only intermediate drafts (typically v1–v3 in multi-version arcs).
   3. If `Materials Archive/` has an entry for this app via `python3 save_materials.py`, that's the canonical submitted version.

   **Why this matters:** "find the closest prior application" produces uneven first drafts because agents pick whatever's longest or most recent rather than what June actually shipped. June's voice-final versions are ground truth; intermediate agent drafts are training data she's already rejected. Reading from agent drafts re-introduces patterns she edited out.

**Also read when relevant:**
- Research statements: `/Users/june/Documents/GitHub/profile/PUBLICATIONS_DEEP_READ.md`
- Teaching statements: `synthesis/Bloch_Teaching_Portfolio.md`
- Diversity statements: `synthesis/Bloch_Service_and_Diversity.md`
- Reframe-heavy apps: `agent_briefs/Bloch_Reframe_Opportunity_Brief.md`
- Voicing parameters: `VOICING_PARAMETERS.md` (CDA-based voice specification)

---

## Step 0.5: Fact assembly (before fit eval, before drafting)

*Added 2026-04-25 after Wenner-Gren V5–V7 friction. The recurring failure mode this prevents: agents draft from theoretical understanding, padding generic claims with theory citations, because the specific factual material (scenes, dates, quotes, ethnographic detail, specific findings) wasn't loaded into context first. Result: "monuments are sensory infrastructure" without the specific affective regime; "coalition expanded the sensorium" without TallBear's specific contribution; "the diary moved through registers" without the Deputy AG releasing the scan online and the court's failed takedown. Theory padding sounds plausible but doesn't land for reviewers.*

**The discipline: assemble the specific facts the draft will need BEFORE drafting begins.**

1. **Sketch what each section needs to do.** Section by section (opening, story, evidence, fit, conclusion), name the kind of grounding the section needs: a scene, a date, a name, a quote, a specific finding, a number, an ethnographic detail. List them.

2. **Locate source documents for each grounding need.** Cross-reference these source registries:
   - **`/Users/june/Documents/GitHub/recognition_sentience/SOURCE_MATERIALS.md`** — R&S book chapter sources, with file paths verified
   - **`/Users/june/Documents/GitHub/recognition_sentience/PER_DOMAIN_TEMPORAL_FLESH.md`** — chapter-domain ethnographic flesh
   - **`/Users/june/Documents/GitHub/recognition_sentience/PARKED_SPECIFICS.md`** — pending verifications and chapter-level details
   - **`/Users/june/Documents/GitHub/profile/JUNE_BLOCH_AGENT_BRIEFING.md`** — identity, story, research programs
   - **`/Users/june/Documents/GitHub/profile/PUBLICATIONS_DEEP_READ.md`** — per-article analysis with content hooks
   - **`/Users/june/Documents/Filing/Job Search/Bloch CV.docx`** — source of record for dates, titles, affiliations
   - **`/Users/june/Documents/Filing/Job Search/Bloch_Application_Context.md`** — consolidated drafting facts
   - **Prior application folders** (`Emory/`, `Netflix/`, etc.) — voice-tested phrasings worth mining
   - **The application's own folder** — POSTING.md, prior version drafts, INTELLECTUAL_CONNECTIONS.md if it exists
   - For book-relevant work, the `recognition_sentience/` directory's per-domain docs and original source PDFs (e.g., `/Users/june/Downloads/The Second Battle of Charlottesville.pdf`, `/Users/june/Library/CloudStorage/.../Weelaunee Research/2025 WGS South Conference/Bloch WGS South Pres v3.pdf`)

3. **Read the sources INTO context.** Not summaries. The actual prose and specific details. If a PDF is more than 10 pages, use the `pages` parameter to read the most relevant sections. The goal is having the specific quote, the specific date, the specific scene available — not paraphrased through a summary layer.

4. **Assemble a working fact inventory** in the application folder as `FACT_INVENTORY.md` (or as a section in `APPLICATION_CHECKLIST.md`). For each section of the draft, list:
   - The specific facts/quotes/scenes that will ground it
   - The source path for each (so future agents can find it without re-searching)
   - Any `[DATA NEEDED]` gaps where June's input is required (a fieldnote detail, a quote you don't have, a date you can't verify)

5. **THEN draft.** From the assembled facts, not from theoretical scaffolding. Theory cited should be doing work on a specific case — not name-dropped to suggest engagement.

**Anti-pattern this prevents:** writing "Anti-trans law is constitutive, not just prohibitive" without the specific mechanism that demonstrates it (the Convention's Holocaust framing decentering homosexual victims; HRT's slow-time becoming on the legal-administrative clock). Or writing "The diary traveled across registers" without the Deputy AG, the RICO motion, the online scan release, the court's failed takedown. Generic theory + missing specifics reads as padding.

**When source docs don't yet exist:** if the section needs a fact you don't have, ask June. Don't fabricate plausible details. The cost of asking is a one-line message; the cost of inventing detail is the application carrying claims that won't survive June's read or a reviewer's scrutiny.

**Cross-reference convention:** when you discover a new source path that future drafts will need (e.g., a new PDF, a new fieldnote file), add it to `SOURCE_MATERIALS.md` (for R&S material) or to the relevant `_funder_profiles/` or application-folder doc. Don't let path discovery be redone every session.

**Pulling from prior similar applications — pull the FINAL version, not an old draft.** When a new application has a closely-related prior application (same role type, same kind of fellowship, same audience), the closest prior application is often the best starting material. **Pull from the most recent submitted/final version**, in this priority order:

1. `*_final.md` or similarly-named final markdown in the prior application folder
2. The submitted PDF or HTML artifact (`Bloch CL.pdf`, `Bloch_Application_*.pdf`, `*_final.html`) — these reflect the actual final state. **Extract their prose into a temporary `final_extracted.md`** and pull from that
3. The highest-numbered `vN.md` if no explicit final exists
4. Only if none of the above exist, fall back to `draft_v1.md` or earlier drafts

**Failure mode caught 2026-05-06 (Hamilton WGS VAP):** drafting agent for Hamilton pulled from an old version of the closest prior application (LMU WGS VAP) instead of LMU's final state. Hamilton's draft v1 was a partial regression from the start. The fix is upstream of voice-check — load the right source, not patch the bad draft afterward.

**When you submit, write a clean `*_final.md`.** After June approves the final document and it's submitted, save the final markdown text (the `.md` source, not the rendered HTML or PDF) to the application folder as `*_final.md`. Future agents pulling from this application will then have an unambiguous source to reference. Don't leave only an HTML or PDF as the canonical record — those are render artifacts; the markdown is the source.

---

## Step 1: Fit evaluation (before drafting)

Write a short fit assessment and save it at the top of your draft or in the app folder:

- **Direct matches**: What requirements does June meet with existing experience?
- **Bridgeable gaps**: What can she credibly bridge? What's the bridge?
- **Real gaps**: What does the role ask for that she doesn't have?
- **Fit verdict**: Strong / Decent / Weak

If weak: STOP. Tell June. Don't draft.

---

## Step 1.5: Allocation table (multi-document applications only)

If the application requires 2+ documents (cover letter + research statement, etc.), create an allocation table BEFORE drafting anything. Each concept, story, and example gets ONE full treatment in one document. Other documents reference it briefly.

| Concept/Story | Full treatment in | Brief reference in |
|---|---|---|
| Pvlvcekolv moth moment | Cover letter (origin story) | Research statement (theoretical architecture) |
| Autograder bias finding | Research statement (full technical) | Cover letter (summary), equity (implication) |
| Normative gravity | Research statement (theorized) | Others use the term, don't re-explain |
| Emergency flex weeks | Teaching statement (primary) | Equity (brief reference) |
| Survival architecture | Research statement (theorize) | Teaching (apply), cover letter (use term) |
| Ethnic Studies is a Strike | Teaching statement (full section) | Cover letter (brief) |
| Identity/positionality | Equity statement (primary) | — |
| Beaded arrow story | Equity statement | — |

This table prevents the redundancy spiral (normative gravity re-explained 4 times, Autograder described in every doc). Customize for each application — the table above is a starting template based on the UB experience.

**The cover letter is the BRAID** — it weaves strands from the other documents into a new argument at their intersection, not a miniature version of each. Each strand gets its full treatment elsewhere; the cover letter is where they meet.

**For grants and structured-form applications**, the same allocation discipline applies, but the rows are the form's prompts (Q1, Q2, Q3) rather than separate documents. Each story/concept/finding gets its full treatment in ONE answer; other answers reference it briefly. Pull the prompt list from `APPLICATION_STRUCTURE.md` (captured in Step 0) and build the allocation table against those questions. The Pvlvcekolv moth moment goes in full in (say) the "describe your background" prompt; the "describe your fit" prompt references it without re-telling. Same anti-redundancy logic, different unit.

---

## Step 2: "Why This Position" note

3 sentences max, placed at the top of your draft:
- What about THIS position connects to June's specific work?
- Which research program or tool is most relevant?
- What would she bring that the posting implicitly needs but doesn't name?

---

## Step 3: The question they haven't asked

**Find the question this employer, department, or funder hasn't thought to ask — and say what you would contribute to it.** Additive, collaborative, positioned as joining.

> ### ⚠ RENAMED AND NARROWED 2026-08-09 — read this if you are looking for "Hakope's Question"
>
> This step was called **"Hakope's Question touchstone"** and asked: *"What framework is this field/institution treating as given, and how does June's work reveal that the framework itself is the problem?"*
>
> **That is a different move from the one this step is for, and the difference matters.** June (2026-08-09), on catching the conflation: *"I conflated both, but the first one is more effective for the context."*
>
> - **What this step now asks** — surface the question they haven't reached, and offer what you'd bring to it. *"Here's the kind of contribution I can make as part of your team."* **Additive. Collaborative. Positioned as joining.**
> - **What the old wording asked** — reveal that their framework is the problem. **Corrective. Positioned as verdict.**
>
> **Why the change.** The 2026-08 evidence sweeps found that work positioned as *correcting* a field is substantially more exposed than work positioned as *opening* something — because the specialist who would be corrected is in the room, and at ACLS is structurally the first reader (two same-field prescreeners eliminate ~50% of proposals before any panel sees them). Mark Roche, an ACLS panelist, watched a strong application die because one same-field panelist objected and everyone deferred, with no hostility involved. Add Lamont's panel-observation finding that "innovators are often penalized if they go too far in breaking boundaries," and Tardy's that assessors judge norm-breaking as transgressive where peers judge it innovative — with standing gating which reading you get. June applies without institutional affiliation.
>
> **The additive version is also better supported.** "What I'd contribute to the question you haven't asked" *is* the argument move — specifically the element the genre research finds almost everyone skips. In the one corpus that split it out, applicants supplied "background" near-universally and "what that does for them" about a fifth of the time. This step is that missing element, worked at the level of the intellectual problem rather than the job description.
>
> **The name was retired here, not the move.** "Hakope's Question" carries the corrective version's charge, because that is what it means in the research context where it originated — and correctly so there. Keep the name for research writing. In applications, use the plain description above.
>
> **Where the original lives, and it is worth reading for research work:** `~/Documents/GitHub/research/ai-welfare/touchstones/FOLLOW_THE_HEADMANS_QUESTION_TOUCHSTONE.md`. ⚠ **Name collision:** "the headman's question" and "Hakope's Question" are the same thing — the touchstone is titled for the role, the move inside it named for the person. Searching "Hakope" alone misses it, which is how it stayed invisible through fifteen invocations. Also: `~/Documents/GitHub/cyborg-methodologies/hakopes-question/`, and activation research at `~/Documents/GitHub/research/compression-research/touchstone_activation_findings/`, which classifies the move as reachable by a fresh agent with **the moth image as the retrieval hook** — if the operation feels abstract, the concrete image is what makes it available. That research measures activation *in a reading instance*; it says nothing about application outcomes.

### What to actually do

Before drafting, answer both halves:

1. **What is the question this employer, department, or funder hasn't reached yet?** Not the question their posting asks — the one their own work is heading toward and hasn't named. This comes out of the Step 3.7 research; you cannot answer it from the posting alone.

2. **What would June contribute to it, as part of their team?** Concrete and specific: what she'd build, study, teach, or open up that they currently can't. This is the half that carries the move — an insight without a contribution attached is an observation about them, not an offer.

**The test.** Read your answer back. Does it sound like *"you've missed something"* or like *"here's what I'd bring to what you're already doing"*? If the first, rewrite it. The intellectual content can be identical; the relationship to the reader is what changes, and the reader deciding is often the specialist whose work is implicated.

**Anti-pattern**, and it is already flagged at Step 3.7: don't tell them what they believe. *"Your department was created to upend X, and I have been upending X"* announces a verdict on their self-understanding. Write into the conversation they are already having.

**The origin, for context.** The move descends from a moment in June's fieldwork: *"Well, did you ever consider that it isn't a bird?"* — Hakope (Maker of Medicine), responding to her queer theory paper on Mississippian figures. The figures weren't gendered birds at all. They were genderless moths, and the entire academic debate shared an unexamined premise. **In research writing that is the whole move and it should stay that way** — see the touchstone linked above. **In applications, the useful part is the opening it creates, not the verdict it delivers.**

**Where the move already operates in June's work** — these are the *research-register* versions, stated as verdicts because that is correct in research writing. **For an application, convert each into what it opens up for this specific reader**, and lead with the contribution rather than the correction:

| The research-register version (verdict) | What it becomes in an application (offer) |
|---|---|
| In AI: the measurement framework constitutively forecloses what it can perceive | "Here is what your evaluation could see that it currently can't, and how I'd build toward it" |
| In assessment: the output format IS the bias — binary classification is the bird that isn't a bird | "Here is a question about your assessment tooling nobody is asking, and what I'd contribute to answering it" |
| In NAIS/archaeology: Indigenous knowledge doesn't supplement Western categories — it replaces them | "Here is the collaboration your community-engaged work makes possible, and what a decade of CBPR brings to it" |
| In teaching: "did this student cheat?" → cheating is signal, not violation | "Here is what your academic-integrity data could tell you about your curriculum, and how I'd read it" |
| In trans studies: the Genocide Convention's exclusion of gender groups IS the mechanism of non-recognition | "Here is the legal-recognition question your program is already circling, and what I'd bring to it" |

Same intellectual content in both columns. The right-hand column is what goes in an application.

---

### How this move holds up against the 2026-08 research — assessed 2026-08-09

June asked whether the touchstone survives contact with what the evidence sweeps found. It does, with one framing constraint that changes its exposure substantially. Sourcing: `_application_evidence/`.

**It passes the single named failure mode that a real ACLS panelist supplied.** Mark Roche, who served on an ACLS selection panel and published a first-person account, names the killer as *"externally plugging categories into a topic as opposed to letting the topic or the evidence drive the categories."* Hakope's Question is the inverse of that — the moths were moths; the reframe came *from* the evidence. This is the strongest thing in the research's favour, and it is not incidental: it is the failure mode a person who sat on the panel chose to name.

**It is also the strongest available version of what the genre research demands.** Two independent literatures converged on "generic" meaning *unresponsive to this particular situation* rather than formally conventional. A reframe that only this material could produce is maximally situated. And Michèle Lamont — the sociologist who observed twelve real funding panels — found that the diversity evaluators report caring about most is disciplinary and institutional: "ensuring that funding not be restricted to scholars in only a few fields or at top universities." A cross-cutting reframe can read as exactly that.

**Three findings cut the other way, and they compound.**

- **Roche's sharpest observation:** he watched a strong application die because one same-field panelist objected and everyone deferred — no hostility, "legitimate intellectual differences." The implication he draws is that work positioned as **correcting** its field is more exposed than work positioned as **opening** something, because the specialist who would be corrected is in the room.
- **Lamont, from panel observation:** *"innovators are often penalized if they go too far in breaking boundaries, even if by doing so they redefine conventions."* Plus homophily — evaluators "often define excellence as what speaks most to me, which is often akin to what is most like me."
- **Christine Tardy** (applied linguist studying when departures from convention read as skilled versus as error): assessors judge norm-breaking as transgressive where peers judge it innovative, and *"it is typically only the students who have already demonstrated such mastery who are granted the opportunity to innovate."* Standing gates which reading you get — and June applies without institutional affiliation.

**And at ACLS specifically the exposure is structural.** Per an internal ACLS document quoted in Lamont, applicants are **prescreened by two scholars in their own field**, whose scores eliminate about half the pool, before any interdisciplinary panel sees the proposal. A move that unsettles a debate goes *first* to the people whose debate it is.

**The conclusion is a framing rule, not a go/no-go.**

The same intellectual content is substantially less exposed positioned as **opening** — *"this suggests a different question"* — than positioned as **correcting** — *"the field has assumed X and is wrong."* Identical claim; different relationship to the specialist reading it first.

This converges with an anti-pattern already in this pipeline at Step 3.7: *don't tell the committee what they believe.* The research supplies the mechanism behind that instinct and extends it — the risk is not the reframe itself, it is whether the reframe is delivered as a verdict on a field or as an opening within it.

**Status:** the supporting evidence is testimony and panel ethnography — hypothesis, never finding. No study measures whether reframing moves affect application outcomes. What is solid is the *asymmetry* between opening and correcting, which two independent sources reached.

Name the specific framework-reframe for THIS application. It goes in the cover letter or application essay.

---

## Step 3.5: Drafting method

**Default: Voice-guided single pass from a shared plan + sequential workshopping with June.**

The drafting agent works from three inputs: (1) the shared plan built in Step 3.8 (`DRAFT_PLAN.md`), (2) the voice-final priors loaded in Step 0, and (3) the voice profile. The plan supplies the arc and beats; the priors supply the voice model and story bank; the profile supplies the live style guide.

Before drafting, read June's voice profile (`~/.claude/skills/voice-check/profiles/june_bloch.json`) — the `stylometry.style_notes`, `qualitative` checks, the active genre's description, and the anti-pattern lists. Select the genre (e.g., `academic_position`, `tech_position`, `ea_grant`, `humanist_fellowship`). Write in her voice from the start.

**Apply Williams's *Style: Lessons in Clarity and Grace* throughout drafting and revision.** The voice profile catches contamination patterns; Williams catches structural prose problems the profile doesn't. Core principles: characters as subjects, actions as verbs (not nominalizations); old information at the start of sentences, new information at the end (cohesion); cut metadiscourse ("I argue that," "It is important to note"); cut redundant pairs and categories; replace phrases with words ("in light of the fact that" → "because"); end sentences on the most important information (stress position). Williams is especially load-bearing during word-count compression — most "I can't cut more without losing meaning" moments are actually places where verb-to-nominalization conversions, redundant qualifiers, or relative-clause sprawl can be tightened to verb forms. Added 2026-05-05 after LMU CL compression session.

Draft the complete long-form assembly before selecting to the target. Use the allocation table, prior materials, and the voice profile as active guidance; abundance must mean additional evidence, scenes, or argumentative paths, not padded versions of the same content. Show the assembly to June before any autonomous cut. Granular KEEP / DROP / UNSURE marking is the default selection input. At multi-document scale, after seeing the full packet, she may explicitly authorize the reversible proposition-level merge in `PRO-11` instead; unmarked material remains `UNSURE`, the assemblies stay preserved, and the system supplies a cross-document ownership map, source notes, standing-inclusion audit, and named genuine losses. Then choose and record an inspectable route: AI-proposed reversible cut with a diff, author-led selection with local AI compression, hybrid, or the explicitly authorized packet synthesis. The provisional ~1.2 × `T` handoff in `PRO-11` is an experiment, not a requirement, and the quality of AI cutting remains an open question. After the content architecture settles, self-run the quantitative check and silently fix agent contamination (hedges, jargon, padding, self-aggrandizing frames). Surface structural/qualitative findings as suggestions, not corrections.

This pipeline is designed to produce innovative, specifically tailored materials — documents that resist normative gravity by drawing surprising connections between June's work and each position, shifting enough from standard genre conventions to catch a reader's attention without working against her. The voice profile is what prevents that creative shift from drifting into agent-voice contamination.

Then present to June for sequential revision — one edit at a time, back-and-forth. The judgment gap (what to emphasize, which stories to choose, what the committee needs) is filled by June during sequential workshopping, not by additional agent passes.

**Target word counts:**
- Cover letter: ~1,200 words (open-rank may be longer)
- Research statement: ~2,000 words
- Teaching statement: ~1,200 words
- Equity/diversity statement: ~900 words
- Non-academic cover letter (tech/nonprofit/museum/general staff roles): **~500 words working target, ~525 hard ceiling at five paragraphs** — one page on `letter_template.html`. **Measured 2026-08-16**, superseding two unmeasured figures. The original "~600–800" was asserted, never sourced, and produced a FAMSF letter no one-page letterhead could hold; the 2026-08-13 correction to "~350–450" was a reaction to that and ran ~50–150 words tighter than the template actually holds, which spends real content for nothing. What was measured: `letter_template.html` through WeasyPrint at June's prose's mean word length, five paragraphs — 525 fits, 530 breaks. Corroborated by her own FAMSF letter converging at 492 words on one page. More paragraphs lowers the ceiling; re-measure if the template changes (method: `_application_evidence/REVISION_ANALYSIS_2026-08-16_FAMSF.md` §6). Capture still runs long (~800) so Stage 3–4 select from abundance — and per `DRAFTING_STANDARD.md` `PRO-11`, June marks keep/drop on the assembly *before* the cut.
- Grant abstract: per form requirements

**Never use placeholder numbers.** If you don't have evaluation scores, publication counts, or dates, use `[DATA NEEDED]` tokens. Inventing plausible numbers is the highest-risk failure mode — a committee that catches inflated numbers will distrust the entire application.

**Optional: Multi-pass for structural complexity.** If the document requires complex cross-referencing or the agent is struggling to hold the full argument, break into: (1) structured outline with key claims and story placements, (2) full draft from the outline. This is a fallback, not the default.

---

## Step 3.7: Intellectual landscape research (relational tracing)

*The goal is not "demonstrate fit." The goal is to enter their intellectual conversation.*

**Required reading first:** `~/Documents/GitHub/cyborg-methodologies/INSIGHTS.md` (the 2026-04-29 entry, "Pattern-matching as relational tracing").

**Why this is required, not optional:** AI default pattern-matching pulls toward similarity — *what's like what's already here*. Lateral, feature-matching, twin-finding. The cyborg-distinctive analytical move is different: connection-following. Not "which faculty share keywords with June" but "what conversation is this department actually having, and where in it does June's work belong." For position research, this is the difference between a credential-match list (which produces a confrontational alignment-announcing letter) and a relational map (which produces a letter that thinks alongside the reader). The framing changes what you notice. Read INSIGHTS.md before you do this step, not after.

**The two questions that organize the research:**
1. **What does June's work *open up* for them?** Not what skills she brings — what becomes newly possible in their conversation if she's part of it. What questions can they now ask that they couldn't before? What method becomes available? What blockage gets unblocked?
2. **What threads in their work does June's work *pick up*?** Their department/team is already in some intellectual conversation — what threads is it running, and where does June's work join one already underway? Not "we both care about X" but "they're asking [specific question]; June's [specific work] is one way that question gets answered."

These are the same operation in two directions. Both questions matter — together they map the relational field, not the feature overlap.

**For academic positions:**
1. Identify faculty in the department — especially the search committee chair and 3–5 faculty whose work is closest to June's intellectual conversations (not just keyword-matching her CV).
2. Use Semantic Scholar, training data, or department websites to find their recent publications and research focus.
3. For each relevant faculty member, work the two questions. Forms the relational tracing can take:
   - **Convergence**: Their direction of travel moves toward questions June is already answering (or vice versa). Example: a CS theorist whose career moved from efficient architectures to responsible computing is on a trajectory toward questions June's work addresses empirically.
   - **Thread-uptake**: They're working on the same problem from a different disciplinary entry point. June's work picks up a thread they're running and continues it from her angle.
   - **Productive tension**: Their work and June's disagree in an interesting way — the kind of disagreement that would make a good seminar conversation. Tension is a relation, not a mismatch.
   - **Surprising openings**: Sometimes the strongest move is one neither side is currently making but that becomes obvious when their conversations meet. Flag these — they're often the most valuable.

   Not every faculty member will have a meaningful relation. That's fine — don't force it. Forcing similarity-matching is what produces credential-listing letters.
4. Note where the department has gaps June could fill — but frame as "what conversation are they not yet having that her work could start" rather than "what skill do they lack."
5. Note recent hires and direction of travel.

**For industry/tech positions:**
1. Surface what you know about the company from training data — products, public technical challenges, recent blog posts, engineering culture.
2. Identify the specific team or product the role serves.
3. Apply the two questions: what does June's work open up for their product/problem? what threads in their engineering or research conversation does her work pick up?

**For policy/research orgs specifically (AI Now, DAIR, Data & Society, think tanks, advocacy orgs with a developed intellectual position):** The company profile must include two additional required outputs — without these, the draft will describe the org accurately but generically, and the letter could be sent to any peer org with minimal edits:

- **Vocabulary extraction**: List 3–5 key terms the org uses in their public writing that don't appear in June's typical register. These are the terms the draft should use rather than substituting June's coined terms. The draft enters their vocabulary; it doesn't describe their work in June's vocabulary.
- **Gap analysis**: What does their structural/critical analysis open but not yet answer affirmatively? Where is their roadmap underdeveloped — what are they calling for but haven't built? This is the sharpest differentiating argument. It names what June's work answers that they can't yet do. "We're aligned" is not a gap argument; "you've named the problem; I've been building toward the answer" is.

The test: *could this letter be sent to a peer org (e.g., DAIR instead of AI Now) with minimal edits?* If yes, the tailoring failed. A properly tailored letter names at least one specific publication and uses the org's vocabulary. See `non_academic_application.md` Stage 0 and `DRAFT_PLAN_TEMPLATE.md` Tailoring anchors section.

**Output TWO documents** in the application folder:

1. **`DEPARTMENT_PROFILE.md`** (or `COMPANY_PROFILE.md`) — the research itself. Faculty, gaps, structural questions, recent hires. **Plus a "Local reading conditions" section — added 2026-08-09, see below.**
2. **`INTELLECTUAL_CONNECTIONS.md`** — a brief for June explaining, for each relevant person/team: what they work on, what structural question they're asking, and (the relational answer) what threads of theirs June's work picks up and what her work opens up for them. **This is a document June keeps and reads.** She wants to learn about these people's theories. Write it as an intellectual introduction, not a fit justification. She will evaluate whether the connections hold and may follow up with the work herself.

**How this shapes the draft:** The letter should think in a register that recognizes the department's questions. Don't quote faculty websites. Don't announce "your department values X and I do X." Instead, write in a way that a reader from that department recognizes as already being in their conversation. The faculty research is input to the register, not content in the letter. It's impressionistic and gestural — evoking the shared intellectual terrain, not citing it.

**Anti-pattern (similarity-clustering version):** "Your department was created to upend X. I have been upending X for Y years." This tells the committee what they believe and announces a match. Feature-matching with a confrontational frame.

---

### Local reading conditions — added 2026-08-09

**Why this section exists.** Four independent literatures converged on one finding during the 2026-08 sweeps: **applications are evaluated relationally — against whatever cluster they land in, by whoever happens to be in the room, through that person's disciplinary lens — not against an absolute standard.** Lamont observed it in panel ethnography ("panelists adopt a nonlinear approach... they compare proposals according to shared characteristics"); the ERC interview study named it "calibration devices"; an NSF panelist described rankings nudged on the board by whoever recalled the neighbouring proposals; and Christine Tardy — an applied linguist whose book studies when departures from genre convention read as skilled rather than as error — supplies the theory: tolerance for difference is a property of the **local** group, not the discipline. (Michèle Lamont is the sociologist who observed twelve real funding panels and interviewed 81 panelists; the ERC study interviewed 22 European Research Council reviewers about how they decide under time pressure. Names given once here because a cold agent has no context on them.) Full sourcing: `_application_evidence/`.

The consequence is that several drafting decisions have **no general answer** and only a per-application one. `DEPARTMENT_PROFILE.md` / `COMPANY_PROFILE.md` is where they get answered, because it is the only artifact that is already per-application. Answer these in writing; leave anything unknown marked unknown rather than guessed.

1. **Does anyone here share June's subfield?** If several people do, they will translate her significance for the room and the letter can be spare. If she would be the only one, nobody can do that translation and **the letter must carry the vouching itself.** This reframes interdisciplinarity from "look more focused" to "this room has nobody who can vouch for this work." (Berkeley career guidance; converges with Rosati — a discipline-internal proposal needs a particular person seated, and whether they are is luck.)

2. **Is there a published screening rubric, or a stated review criterion?** Some searches publish one; some funders publish reviewer instructions. Where they exist they outrank every general heuristic in this pipeline. Berkeley eliminated 76% of applicants on one document. ACLS instructs reviewers to weigh the record "taking into account relative advantages or constraints on resources over the course of the applicant's career" — a criterion worth writing *into* the framing rather than hoping a reviewer applies unprompted.

3. **Does this employer score blind?** Organizations that strip identifying information before scoring generally say so. If blind: the letter can only work on content and reasoning — naming a contact or leaning on affiliation is stripped or flags as defeating the process. If not blind: relational and institutional signal is available. See the `blind_scoring_check` in the voice profile.

4. **What cluster will this be compared against?** Not "how good is it" but "who else is in this pile." Where the posting names a field, a specialization, or a cohort, that is the comparison set.

5. **What symbolic capital does June have *in the eyes of these specific evaluators*?** (Tardy's question, and the one this pipeline has never asked.) Symbolic capital is reader-relative, not a property of the CV — the same record reads differently to a department that knows her work than to one that does not. Ask it about *these* readers.

6. **What is the risk of deviation here, for her specifically?** Tardy: "it is typically only the students who have already demonstrated such mastery who are granted the opportunity to innovate," and readers in an assessor role judge norm-breaking as transgressive where a peer would judge it innovative. Lamont, from panel observation: "innovators are often penalized if they go too far in breaking boundaries." **Deviation is not equally affordable across applications, and this is where that gets decided** — not at drafting time by taste.

**Where this lands.** Answers 1, 4, and 5 shape how much the letter must explain versus assume. Answer 2 outranks general guidance. Answer 3 determines what the letter may contain at all. Answer 6 is the go/no-go on any unusual structure. Carry all six into the Stage 2 subagent brief — a cold drafting agent sees only its brief, so a condition not written there does not exist for the agent writing the prose.

**The relational-tracing version of the same move:** Write into the conversation the department is already having, in a register that picks up its threads. The reader arrives at "this person belongs here" through the texture of the thinking — not because the letter announces it.

---

## Step 3.8: Pre-draft cyborg conversation

**Prerequisite gate: Step 3.7 must be done first.** This step is the *conversation* layer; Step 3.7 is the *research* layer. Doing 3.8 without 3.7 collapses the conversation into similarity-clustering — the agent surfaces "candidate framings" that are feature-overlaps between June's work and the position, because it never did the relational tracing that gives it material to think with. Failure mode caught 2026-05-07 (Duquesne Grefenstette session): agent skipped 3.7, jumped to 3.8, surfaced four similarity-clustered "frames" (more-CST-similar, parallel-traditions, less-CST-similar). June redirected — the actual frame was a staged conversation grounded in shared epistemic-from-below commitment across traditions, which the agent could only see *after* being pointed back to INSIGHTS.md. The fix: the analytical-mode reading (INSIGHTS.md) was hoisted to the top of the pipeline, AND this gate was added to make the 3.7→3.8 chain explicit.

*Added 2026-05-06. The drafting friction the pipeline kept hitting: agent does fact assembly, fit eval, intellectual landscape, then drafts solo from a structure it picked. June reads, redirects, edits heavily — sometimes restructures wholesale. The structural decisions that determine whether a draft is strong (arc, what story it tells, what's load-bearing, what to leave out) were happening at the drafting agent's choice and getting overturned at June's read. This step moves those decisions earlier, into a conversation, before drafting.*

**The principle:** Strong first drafts come from a strong shared plan. The plan is built in conversation, not handed off as a directive. The agent surfaces what it sees from the prior steps; June redirects, names the story she wants told, identifies what the document needs to do. The conversation is the artifact; the captured plan is what we built together.

**Required reading reminder:** INSIGHTS.md (per Step 3.7). The conversation IS where relational tracing becomes operative — what June's work opens up for them, what threads it picks up. The agent has done the research; the conversation is where the agent and June together decide which connections are load-bearing for THIS document.

**The conversation has roughly four moves. The agent opens each; June redirects.**

1. **What the agent sees from 3.7**: surface 2–4 candidate framings the position invites. For each: the relational opening (what June's work makes newly possible there), the thread it picks up (what conversation it joins), and the candidate for the question they haven't asked (Step 3). Don't pick one yet — present the field.
2. **What June actually wants to communicate**: she names the story. This is where the agent learns what's load-bearing that wasn't visible from the posting alone — a fieldwork moment that anchors everything, a politics she wants made visible, a tool whose origin matters here, a refusal of a frame the field wants to impose.
3. **Arc proposal under genre conventions**: agent proposes the structure that carries June's story under the genre's reading conventions (academic CL, fellowship statement, tech CL, grant abstract — each has its own gravity). June redirects on what's missing, what's overweighted, what needs to land earlier or later.
4. **Section beats and load-bearing specifics**: from the fact inventory (Step 0.5), name what each section carries. Which scenes, which numbers, which scholars cited *doing work* not name-dropped, which prior phrasings to mine from voice-final priors.

**Output:** `DRAFT_PLAN.md` in the application folder, using `templates/DRAFT_PLAN_TEMPLATE.md`. Captures the shared plan: arc, openings/uptakes, the question-they-haven't-asked reframe, section beats with grounding, allocation (multi-doc), what we're deliberately NOT doing.

**Anti-patterns:**
- **Don't present DRAFT_PLAN.md as a fait accompli for June to approve.** The conversation is where the plan is built. The file captures what we built; it doesn't replace the building.
- **Don't extract a directive then draft solo.** If the conversation didn't change the agent's understanding — if the draft would have been the same without it — the conversation didn't happen.
- **Don't use this to multiply checkboxes.** The two questions (opens up / picks up) need real answers, not "[ ] relational tracing applied." If the answer is generic, the agent didn't do Step 3.7 deeply enough — go back.
- **Don't skip when June says "just draft it."** That's a signal that the position is high-confidence and feels familiar — but the cost of a weak first draft is high in editing time, which is the whole point of this step. Surface the field briefly even if June moves fast through it; capture even a 4-line DRAFT_PLAN.md so the structural decision is on the page.

**When to skip (legitimately):** very short documents (cold-outreach emails, short statements under 300 words) where structure is constrained enough that the conversation collapses to "send the draft." Even then, name the arc in one sentence before drafting.

**Why a conversation, not a solo step:** The structure-and-story decisions that make first drafts strong require June's judgment about what the committee/funder/team needs to walk away with — judgment that depends on her field knowledge and her own intentions for the document. The agent can surface options; June names the story. Drafting from a shared plan produces drafts that don't need wholesale restructure on her read.

### Learning loop: watch for these failure modes

This step is new (May 2026) and neither side has muscle memory for it yet. Two failure modes are likely until the practice settles. Notice them in real time, name them when they happen, and capture both in DRAFT_PLAN.md (under "Conversation notes / what happened") so we can refine the practice across uses.

**Failure mode A — Approval-seeking framing.** The agent presents arc candidates as if asking June "is this OK?" rather than thinking with her about which connections are load-bearing. Symptom: agent's framing makes June feel she's being asked to approve drafts of drafts rather than co-author the plan. Recovery: agent restates the move — "I'm not asking which is best; I'm surfacing the field so we can decide together what this document needs to do." The two organizing questions (opens up / picks up) are conversational prompts, not approval gates.

**Failure mode B — Directive extraction without understanding-shift.** June reads the agent's surface and says "draft from this" before the conversation has actually shifted the agent's understanding. Symptom: the draft that emerges is what the agent would have written without the conversation. The conversation became overhead instead of work. Recovery: before drafting, the agent names what changed — "Here's what I now understand differently from before this conversation." If nothing changed, the conversation didn't happen yet. Sometimes June's "draft from this" is correct (the agent's surface was already aligned with what she wants); sometimes it's a signal that she's tired or the position feels familiar enough to skip the work. The agent's job is to notice which one.

**Per-use capture.** In `DRAFT_PLAN.md`, under "Conversation notes / what happened":
- Did either failure mode appear? Which? How was it addressed (or was it)?
- What in the conversation actually shifted the agent's understanding? Name the specific moment.
- What would have happened if we'd skipped this step (counterfactual on first-draft quality)?

**Aggregate review (after 3–5 uses).** Read across `DRAFT_PLAN.md` files in completed applications. Look for: which failure mode is more common, what conversational moves recover from each, whether the step is producing stronger first drafts (compare first-draft-survival rate to pre-Step-3.8 baseline). Update Step 3.8 based on the patterns. Log the review at `agent_briefs/step_3_8_learning_log.md` (create on first review).

**Why a learning loop here specifically:** Step 3.8 is the intervention point with the highest leverage on first-draft quality (the whole reason it was added). If it isn't working as designed, the cost is invisible — drafts come out and get edited, and we don't notice the redesign isn't doing its job. Naming the failure modes makes them detectable. Without this, the step quietly degrades into a procedural pre-draft conversation that doesn't actually shift the planning.

---

## Step 4: Draft

**Draft each in-scope narrative document from DRAFT_PLAN.md** (Step 3.8). The arc, openings/uptakes, the question-they-haven't-asked reframe, section beats, and load-bearing specifics are already settled in conversation with June. Step 4 is execution of the plan, not re-planning. If you find yourself making structural decisions that aren't in DRAFT_PLAN.md, stop — go back to Step 3.8 and surface them in conversation. Drafting is the place where prose-level voice and the plan's beats become specific sentences, not the place where arc choices are made. Reference lists and academic CVs stay in the requirements ledger for compliance but do not become printpress drafting targets. A required résumé is in scope unless June explicitly takes it over.

**Draft for the actual posting, not for a template.** Before writing a sentence, re-read the posting (POSTING.md) and the prescribed structure (APPLICATION_STRUCTURE.md if it exists). The document you produce should respond to:
- **The exact prompts/questions as written** (for grants, fellowships, structured applications). Q1 has its own answer, in its own word limit, addressing what Q1 actually asks. Don't write a generic research statement and split it across the questions; draft each answer to its prompt.
- **Posting-specific instructions** for academic positions ("address how your teaching advances X department's commitment to Y" — that clause sets a required move; ignoring it weakens the application even if the rest is strong).
- **Word/character limits per section** (not just total). If Q1 caps at 300 words and Q2 at 800, those are different drafts with different scopes — not one essay redistributed.
- **Required content elements** the posting names explicitly (a research plan, a specific population, a methodology, named partnerships, named outcomes).

The default failure mode this prevents: agent drafts a high-quality generic version of the document type ("a strong cover letter," "a strong research statement") that doesn't actually answer what the posting asked. Reviewers grade against the prompt; a beautifully-written non-response loses to a competent direct response. For grants especially, the form IS the document structure.

**Format by track:**
- Academic narrative documents: .md draft (will become .docx with letterhead). Cover letter, possibly RS/TS/DS/Institutional Excellence statement. CVs and reference lists are author-handled.
- Tech/non-academic: .md draft (will become .html). Cover letter plus a résumé when the application requires one, unless June explicitly takes over the résumé.
- Fellowship/grant: .md draft matching the application form structure.

**The rules:**
1. Anti-generic test: If a sentence could describe any scholar with a PhD and some tech experience, delete it.
2. Seven mistakes (memorize): no separate tracks, no "non-traditional," no precarity-as-backstory, no softened politics, no disability/design separation, no "journey"/"pivot," no "chatbot."
3. Voice: Direct, funny, politically sharp, stories first, concrete not abstract, names tensions without resolving them. NOT: tech-optimist, corporate, startup pitch, self-help, inspiration porn, both-sides.
4. Concise and precise. Not self-aggrandizing. Not cheesy. Let the facts carry the weight. "I built a 312-module engine that detected its own framework suppression" beats "my groundbreaking paradigm-shifting AI system."
5. Deadname rule: Always L. June Bloch narratively. Published citations use published name.
6. Cross-references mandatory: If you can't point to a source document for a claim, you might be hallucinating.
7. **Source facts before writing, don't verify after.** Read `Bloch_Application_Context.md`, `Bloch CV.docx`, and any relevant source documents (evaluation logs, experiment data) INTO your context before drafting — so that facts, dates, and numbers are drawn from sources rather than generated and then checked. The difference matters: verification catches hallucinations after you've written them. Sourcing prevents them. If you don't have a source for a number, use `[DATA NEEDED]` — never generate a plausible number.

**Audience calibration:**
- Academic: Lead with disciplinary credentials. Reframe = research project. Full scholarly register. Dense is fine.
- Fellowship: Lead with the A/B/C gap (critical humanist who actually builds). Narrative but scholarly.
- Tech: Resume format. Reframe = the operationalization gap. **Register shift**: shorter sentences, less theoretical density, map findings onto THEIR product/problem. "The system's design determines what users can perceive" not "constitutively forecloses." Em-dashes for casual directness are OK. Avoid: academic literature-review parallelism, standalone concept definitions, theoretical architecture sections. The voicing parameters (sentence-level rules, no hedging, constructivist framing, tools by what they replace) apply equally — but the register is cleaner, more direct, less layered.
- AI welfare: Recognition and Sentience book. Ethnic studies + affect theory = decades of tools for "what gets counted as capable of feeling."
- EdTech: Lead with the Autograder finding (output format as activation function for bias). This is the concrete differentiator. Describe Autograder by what it REPLACES in the instructor's workflow, not by its technical architecture. Connect to THEIR assessment product.

---

## Step 4.4: ATS pass (non-academic resumes)

*Added 2026-05-06. **Substantially corrected 2026-08-07 — see the evidence note at the end of this step.** For any application where the resume goes through an Applicant Tracking System.*

⚠ **Read this before running the step.** The original version of Step 4.4 was written on the premise that ATS software drops strong candidates by auto-rejecting résumés on content, keywords, or formatting. **That premise is not supported by any vendor's technical documentation, and the statistics behind it trace to recruiting-vendor marketing.** No vendor documents automatic rejection based on résumé content. Greenhouse's auto-reject fires exclusively on answers to application-form questions; Workday's A–D grades are prioritization, and Workday's own docs say C and D candidates still get hired.

**What the step is actually for:** ensuring the résumé arrives *intact and legible* rather than as a profile with blank fields sitting low in a review queue, and catching mechanical faults (image-only PDF, unaccepted file type, oversized file) that silently strip content. That is a real problem worth a dedicated pass. It is not the same problem as "the machine will reject me," and the difference changes what the pass should recommend.

The one documented auto-rejection mechanism acts on **structured fields derived from work history** — employers configuring screens on employment gaps — not on keywords or formatting.

**Trigger:** Any non-academic, non-fellowship, non-grant position. The default for industry, EdTech, nonprofit, government, NGO, think-tank, AI safety/welfare industry, EA-org employment, science journalism, civic tech, and corporate research roles — most of these route through Greenhouse, Lever, Workday, iCIMS, Taleo, BambooHR, SmartRecruiters, JazzHR, Ashby, or similar. If the application URL goes to an HR portal rather than a department/program email, assume ATS.

**Skip for:** academic positions (committees read directly), fellowships (review panels), grants (review panels), and email-only applications where June emails materials to a named individual. If unsure, check the posting URL — `boards.greenhouse.io`, `jobs.lever.co`, `myworkdayjobs.com`, etc. are dead giveaways.

### Step 4.4-PRE — Text-layer verification gate (ALL tracks, no exceptions)

*Added 2026-09-12. **Runs on every submitted PDF, including academic, fellowship, and grant submissions** — the "Skip for" list above governs the keyword/subagent pass only, not this gate.*

**Everything else in Step 4.4 reasons about the `.md` / `.html` source. This gate reads the rendered artifact's text layer — what a parser, a screen reader, and a recruiter's Cmd-F actually receive.** The two are not the same document, and the difference is invisible until you look.

```
python3 check_pdf_textlayer.py "[App Folder]/Bloch CL.pdf" ["...Resume.pdf" ...]
# --show prints the first 30 lines in parser reading order
```

Exit 1 = at least one BLOCK finding. **Do not present an application as ready to submit with an open BLOCK.**

**What it catches, and why each one was added:**

1. **Flattened PDFs (`Producer: ... Quartz PDFContext`).** A Chrome-rendered PDF re-saved through macOS Preview or the system print dialog rasterizes the text. The file looks perfect, is 10–30× larger, and contains **seven characters** of extractable text (", Ph.D." — the one span in a different font). A 2026-09-12 sweep found **sixteen** such application documents, including AI Now, DAIR, Netflix, PEN America (résumé), Anthropic Institute, and FAMSF on the ATS-routed side, and nine academic letters besides (where the cost is searchability and screen-reader access, not parsing). Good exports read `Producer: Skia/PDF`. **Chrome's own "Save as PDF" destination — never "Print Using System Dialog…".**
2. **Letter-spacing shatter.** CSS `letter-spacing` above ~0.08em at 7–8pt makes Chrome emit each glyph as a separate positioned token; extraction yields `E D U C AT I O N`. This hit the résumé **section headers** — the one place where Greenhouse's documented "unclear section structure" parse failure actually bites, since the parser has no `Education` string to match. Threshold measured by rendering the real templates headless across 0.03–0.14em: clean at ≤0.08em, shattered at ≥0.10em. All print rules in `resume_template.html`, `letter_template.html`, `cv_template.html`, `letterhead.html`, and `portfolio_template.html` were set to **0.06em** on 2026-09-12 — below the measured ceiling, for margin against font-metric differences between machines. **Any new tracked rule that prints must stay at or below 0.06em**; UI chrome (toolbar, modal, buttons) is exempt because it never prints. Verified after the change: zero shattered lines in all three rendered templates.
3. **File size over 2.5 MB** — the Greenhouse parse ceiling already documented in item 7 below. Nothing checked it before.
4. **Bare LinkedIn handle** with no `linkedin.com/in/` URL for the field extractor.

**This gate is mechanical and cheap. It is not the ATS pass** — it does not touch keywords, framing, or content, and it carries none of the vendor-marketing premises the evidence note at the end of this step dismantles. It answers exactly one question: did the document that left this workspace still contain its own words?

---

**Operation:** Dispatch a subagent to run the ATS pass. Don't auto-edit — surface flags for June to review and decide.

**Subagent prompt template** (use `Agent` tool, `subagent_type: general-purpose`, foreground unless drafting more in parallel):

```
You are running an ATS (Applicant Tracking System) compatibility pass on a resume.

Be precise about the risk, because the common framing is wrong and will distort your recommendations. No vendor documents automatic rejection based on résumé content, parsing, or keyword score. Auto-reject, where it exists, fires on answers to application-form questions — never on the résumé itself. Ranking systems change *review order*, not eligibility.

The failure you are guarding against is that the résumé **arrives as a profile with blank fields and lands low in a queue**, or that a mechanical fault silently strips its content. Do not write as though a machine is about to reject the document.

Inputs:
- Posting: [path to POSTING.md]
- Resume: [path to resume .md or .html]
- Cover letter (optional, for keyword cross-check): [path]
- Role type: [tech / edtech / nonprofit / govt / industry research / etc. — informs what counts as a relevant keyword]

Check for and report:

1. **Keyword coverage** — Read the posting's required and preferred qualifications. List the keywords (skills, tools, methodologies, frameworks, certifications, domain terms specific to the role type) and report which are present in the resume verbatim, which are present as synonyms (flag the gap — ATS keyword-matching is often literal), and which are absent. Do NOT recommend keyword stuffing — recommend honest additions where June genuinely has the experience but the resume doesn't currently surface it. For nonprofit/govt/policy roles, keyword conventions differ from tech (e.g., "stakeholder engagement," "theory of change," "Section 508," "FOIA," "logic model") — calibrate to the role type.

2. **Section header parsing** — Greenhouse names "unclear section structures" among its documented parse-failure causes, so recognizable headers do matter. Flag genuinely opaque section names ("What I've Built," "How I Work"). But **no vendor publishes an approved header vocabulary** — the specific list previously given here was sourced to nothing. Keep the instruction; drop the implied authority. ⚠ **The claim that "HTML resumes with semantic tags often parse better than .docx" was false and has been removed** — see item 7.

3. **Date format — DO NOT FLAG DURATION PHRASING. This item previously said the opposite and was wrong.** The prior instruction told agents to flag relative durations ("3 years") as a defect. The best available evidence points the other way: Kristal, Nicks, Gloor & Hauser (*Nature Human Behaviour*, 2023) — preregistered UK field experiment, **9,022 real applications** — found that listing **years worked instead of employment dates raised callbacks ~8% for applicants without gaps and ~15% for applicants with gaps**, by making accumulated experience salient rather than making a gap computable.

   The parser consideration runs the other way: "3 years" gives a date parser no date to extract. But that cost is speculative — no vendor documents a penalty for missing dates, parse failure degrades to manual entry rather than rejection, and the largest published parser evaluation (13,100 real résumés) found date fields are the *best*-extracted field class at F1 0.984, i.e. the least fragile part of the parse when dates are present at all.

   **Neither format is a defect.** A hybrid — explicit ranges for parseability plus a duration cue where a gap would otherwise be conspicuous — satisfies both. Surface it to June as a deliberate choice; never silently strip a duration. Still worth flagging: genuinely missing end dates and internally inconsistent formatting.

4. **Format issues that hurt parsing** — text in images, text in headers/footers (often ignored), tables that disrupt linear parse, columns that cross-thread, special characters that may render as unicode garbage, multi-column layouts that the parser linearizes incorrectly.

5. **Keyword density — and there is a measured ceiling.** ⚠ **The former claim here, that "top-tier ATS systems weight early-document keywords more," was unsourceable and has been removed.** Every locatable source for positional keyword weighting was vendor marketing; no vendor technical documentation describes it; and the two documented scoring mechanisms point the other way (Workday HiredScore grades on overall résumé-to-JD match with no positional component, and the peer-reviewed ranking work uses whole-document cosine similarity, position-invariant by construction). "Top-tier ATS" is not a defined category.

   What *is* evidenced: returns to added keywords are **non-monotonic**. In the one peer-reviewed study of embedding-based résumé ranking (Samadi, Banerjee & Nilizadeh, BlackboxNLP 2021 — a research prototype, not a deployed commercial system), 20 added bigrams improved rank by ~30 positions out of 100 while 50 improved it by only ~28. **Flag over-integration as well as gaps.** The anti-stuffing rule this step already carried is independently vindicated.

6. **Title alignment** — does the candidate's recent title use language the posting recognizes? Flag if there's a translation gap (e.g., posting wants "Machine Learning Engineer," resume says "Researcher"; or posting wants "Program Officer," resume says "Project Lead"). For interdisciplinary candidates like June, title-translation is often the highest-leverage fix.

7. **File format and size — two hard blockers, one of them new.**
   - ⚠ **Never submit .html.** Greenhouse's supported-file-types documentation lists ".doc, .docx, .pdf, .rtf, .txt" — **HTML is not accepted at all and the upload fails outright**, not gracefully. This matters because June's canonical résumé workflow is `resume_template.html`. **That workflow is fine: HTML is the authoring and editing format; the submitted artifact is always the rendered PDF.** The prior version of this step actively recommended HTML as parsing *better* than .docx, which is the one claim here capable of breaking an application.
   - ⚠ **File size: Greenhouse accepts uploads up to 100 MB but cannot parse anything over 2.5 MB.** A file uploads cleanly, looks successful, and silently fails to parse. Nothing else in the pipeline checks this. Flag anything over 2.5 MB.
   - Image-only / scanned PDFs: **supported hazard**, five independent vendor docs converge — but "dead" overstates it. The file still uploads and stays human-viewable; the recruiter gets blank fields, not a rejection.
   - Text-layer PDF, DOCX, RTF, TXT are all accepted.

Output a single markdown report at [app folder]/ATS_REPORT.md with:
- High-priority flags (would leave the document illegible, unparsed, or unsubmittable — **not** "would cause rejection")
- Medium-priority flags (worth addressing)
- Honest-additions list (keywords June plausibly has experience with that should be made visible)
- Format/parse issues with specific line/section references

Do NOT auto-edit the resume. June decides which flags to address.
```

**After the pass:** Read ATS_REPORT.md. Surface the high-priority flags to June with a one-line summary per flag. She decides what to act on. Honest additions are the most common useful output — keywords she has experience with that the resume doesn't currently surface, often because of title/role-language mismatch between her interdisciplinary trajectory and the posting's domain conventions.

**Why a subagent rather than inline:** ATS pattern-matching is mechanical and the agent doing the QC pass shouldn't be split between voice/structural review and parser-compatibility review. The two require different reading modes.

**Track-specific note:** For nonprofit/policy/govt roles, the keyword library is different from tech — pass the role type explicitly so the subagent calibrates. For positions that bridge sectors (e.g., AI safety nonprofit, civic tech research), name both registers in the role-type input so the subagent checks both keyword conventions.

---

### Evidence note — 2026-08-07

Every factual claim in the original Step 4.4 was asserted with no source, in the single topic area most saturated by recruiting-vendor marketing. It was adjudicated claim-by-claim against vendor technical documentation and the research literature. Full findings, with sources: `_application_evidence/Tech_Industry.md` (Part One). Myth provenance: `_application_evidence/Discredited_Claims.md`.

**Removed as unsupported:**
- The auto-rejection frame ("before any human reads it," "would likely cause ATS rejection") — contradicted by every vendor whose technical documentation could be reached.
- Positional keyword weighting — unsourceable, and inconsistent with every documented scoring mechanism.
- HTML parsing better than .docx — contradicted; HTML is not an accepted upload type at all.

**Reversed:**
- Date format. The step told agents to flag the exact representation that a preregistered field experiment with 9,022 real applications found *improves* callbacks, most for applicants with employment gaps. This is the correction with the clearest evidence behind it and it had been running against June for three months.

**Added:**
- The 2.5 MB parse ceiling — real, documented, trivially avoidable, previously unchecked.
- The keyword ceiling (non-monotonic returns).

**Retained because they held up:** multi-column layouts, tables, text in images, header/footer text, image-only PDFs, anti-stuffing, title alignment.

**For context on how much this step can matter at all:** in the best-studied experiment on résumé quality and callbacks (Bertrand & Mullainathan 2004), a substantially stronger résumé produced a 30% relative callback improvement from a base of 8.8% — for white applicants; the same improvement produced nothing statistically distinguishable from zero for Black applicants. That study is from a low-wage 2004 labor market and its effect sizes do not transfer to the roles June applies to. The transferable point is only qualitative: document-level improvement has measurable but bounded returns, and the returns are demographically conditional. Run this step to keep the document legible. Do not run it expecting it to decide an outcome.

---

## Step 4.5: Genre check (before QC)

> **Provenance flag added 2026-08-07.** The four-track register guidance below (academic / fellowship / grant / industry) is **practitioner judgment derived from June's own drafting experience, not from research.** The 2026-08 evidence sweep searched for studies on register, tone, and audience calibration by sector and found none — this is a genuine gap in the literature, not a gap in the search. The guidance is retained because it encodes real accumulated experience and nothing contradicts it. It is flagged rather than rewritten because replacing asserted claims with differently-asserted claims would be no improvement. Treat it as a working heuristic, not a finding. The one adjacent thing the sweep *did* establish: no peer-reviewed field experiment has ever manipulated cover-letter content and measured callbacks, so nobody knows what register does. See `_application_evidence/Cross_Track.md` §3.

*Added 2026-04-11 based on Experiment 7 findings on context weight and genre effectiveness.*

**Genre awareness:** Before QC, verify the draft works as the genre it claims to be, not just as a well-written document about June.

1. **Who reads this, and how?** A search committee member on their 150th app skims differently than a program officer evaluating a cold proposal. Name the reader.
2. **The 30-second scan test:** If the reader gives this 30 seconds, what do they walk away knowing? If the answer is "that this person is qualified" — too generic. If the answer is "that this person has a specific finding/insight that changes how we think about the problem" — effective.
3. **Register calibration:**
   - Academic: Full scholarly voice. Lead with disciplinary credentials. Dense is fine — they expect it.
   - Fellowship: Scholarly but narrative. The opening sentence is everything — it decides whether they keep reading.
   - Grant: Empirical, concrete deliverables, theory of change. EA-adjacent audiences need the finding before the theory.
   - Industry/tech: Shorter, more direct. Map findings onto THEIR product/problem. Avoid: "constitutively forecloses," "probabilistic architectures." Use: "the system's design determines what users can perceive."
   - Cold outreach: SHORT. The first email should make them want the full proposal, not BE the full proposal.
4. **Dual-audience check:** If the position reports to multiple units (e.g., Engineering + Arts & Sciences), does the draft work for both audiences? The strongest letters balance specificity with accessibility.
5. **Collaborative register check:** Does the letter think alongside the reader, or present credentials at them? The reader should arrive at "this person belongs here" through the texture of the thinking — not because the letter announces it. Specific anti-patterns to catch:
   - **Confrontational alignment-announcing:** "Your department was created to upend X. I have been upending X." Don't tell the committee what they believe. Let them recognize their own values in the work.
   - **Credential-listing as argument:** Listing qualifications is not the same as making a case. The case is: here is how this specific work changes how we think about this specific problem.
   - **"I match your mission" construction:** Any sentence that could be paraphrased as "you want X and I have X" is announcing fit rather than demonstrating it.

**Why this matters (from Experiment 7):** Genre is an output format — it has its own normative gravity. The model pulls toward "what a good cover letter looks like" and positional specificity is costly within the genre. Context delivery conditions (how the briefing is framed, scoped, and connected to the task) determine whether the model produces something that works WITHIN the genre while preserving what makes June distinctive — or whether it produces a generic letter or a brilliant essay that isn't quite a letter. The pipeline's existing structure (fit evaluation, Hakope's Question, task scoping) already functions as a structural context delivery intervention. This step makes the genre dimension explicit.

---

## Step 4.7: Reader takeaway audit

*Added 2026-05-05 from LMU WGS VAP session — emerged from a word-count compression where the operative editorial question turned out to be "what should the reader know about June by the end of this letter?"*

**Before QC, write a short list answering: "What should the reader know about June by the end of this document?"** Aim for 5–8 things, distributed across identity, scholarly contribution, teaching, and fit. Then read the draft against the list and ask:

1. **Does each thing on the list land?** If a takeaway is essential but only implicit, the document needs to surface it.
2. **Does anything in the document NOT serve the list?** Paragraphs that don't map to a takeaway are candidates for compression or cutting — even if individually well-written.
3. **Are takeaways in the right weight?** A high-priority takeaway buried at the end may need to move forward; a low-priority takeaway taking up two paragraphs may need to be one.
4. **Is the structural balance right for the genre?** A teaching-focused VAP letter where teaching only appears in the last 25% has a balance problem the takeaway audit will surface.

This is the editorial pass that answers "what should I cut?" non-arbitrarily. Word-count compression without a takeaway list cuts what's easiest; compression with a takeaway list cuts what's not load-bearing for what the reader needs to walk away with.

**Save the list** in the application folder (e.g., `READER_TAKEAWAYS.md` or as a section in `APPLICATION_CHECKLIST.md`) — useful for the learning loop and for future similar applications.

---

## Step 5: QC checklist (run before saving)

If you followed the voice-guided drafting process (Step 3.5), the voice profile already handled most of the voice and CDA checks during drafting and self-correction. This checklist catches what the skill doesn't cover and verifies the document works as a whole.

**Handled by the voice profile** (verify these were addressed, don't re-run manually):
- [ ] 8 voice characteristics (in profile's qualitative checks)
- [ ] Anti-patterns / contamination (silently corrected during drafting)
- [ ] Corporate jargon (caught by profile's `patterns.corporate_jargon`)
- [ ] CDA qualitative checks — transitivity, concept scope, constructivist epistemology, referential strategy, argumentation topoi, genre moves, narrative structure, etc. (all in profile)

**Supplementary checks** (not covered by the skill — run these manually):
- [ ] Anti-generic: Every sentence specific to June? If it could describe any scholar with a PhD and some tech experience, delete it.
- [ ] 7 common drafting mistakes (from Application Context doc)
- [ ] The question they haven't asked (Step 3) — present, and framed as contribution rather than correction?
- [ ] **Factual verification pass**: Every factual claim (dates, numbers, project details, institutional names, publication venues) checked against source documents. Deep engagement with context can produce confident extrapolation — vivid details that feel right but extend beyond what the briefing actually states. Verify, don't trust.
- [ ] **Genre effectiveness**: Does this work as the genre it claims to be? Does it shift enough from the standard to catch attention without working against June? (see Step 4.5)
- [ ] **30-second scan**: What does a skimming reader take away? Does the document resist normative gravity — or could it have been written by any applicant?

---

## Step 5.5: Presenting the draft and revision process

**Before showing June any draft, assess it honestly.** Name what's strong and what's rough. Not "this looks good" — that sets expectations the draft may not meet and creates overwhelm when she encounters problems she wasn't prepared for. Instead: "The research section has strong specificity. The opening is too clause-heavy. The teaching and equity statements overlap in three places. I want to take you through one level at a time."

**At the start of any drafting/revision session, announce the plan:** "We'll work through this sequentially — cross-document structure first, then each document's argument arc, then sentence-level. One level at a time." This prevents the simultaneity overwhelm of trying to fix sentence-level, document-level, and cross-document problems all at once.

**Sequential workshopping** is the default revision model. Present June with ONE revision at a time. Not four full documents. Not a batch of edits. One change, one approval, next change. This prevents the overwhelm escalation loop.

**Exception: structural revisions to an existing draft.** When the task is integrating substantive new content (a new theoretical move, a structural reframe, new domain material) into an existing draft, batch the integration — preserve the prior version as a checkpoint and let June read through V[N+1] as a whole. Sequential one-at-a-time is the model for fine-grained edits and word-count compression, not for content integration where she needs to assess structure across the document.

**Content first, word counts later.** When integrating substantive changes, lock the content first; treat word-count compression as a separate downstream phase. Flagging that a section is over budget is useful as a notice, but compressing the prose before content is settled wastes effort — June will likely cut other things or restructure on read-through. Compression is a sequential one-at-a-time task that comes after content is approved. (Established 2026-04-25 during Wenner-Gren V4 integration.)

**Overwhelm detection**: When June's messages show increasing typo density, shift to:
- Shorter responses
- Targeted questions instead of more draft text
- Simpler language without reducing depth
- Explicit check-in: "Should we pause on this and come back?"

**Post-draft committee simulation** (recommended for academic): Run perspective reads from simulated committee positions (engineering faculty, humanities faculty, department chair, skeptic). Report strengths, concerns, and what's missing from each perspective. This is a QC check, not full research — the pre-draft simulation (Step 3.7) does the deep research.

---

## Step 5.7: Adversarial reviewer pass (substantive applications, before saving)

For substantive applications — anything where reviewer panel composition matters — run a multi-persona adversarial reviewer pass before finalizing. Spec at `templates/adversarial_reviewer_personas.md`.

1. Identify the funder's likely panel composition (use `_funder_profiles/[FUNDER].md`) OR for academic positions, the actual search committee (`DEPARTMENT_PROFILE.md`)
2. Select 3–5 reviewer personas from the library matching that panel
3. **Feed personas the actual posting** (`POSTING.md`) — not just a description of the funder/department. Mock reviewers calibrated against an *imagined* posting catch what an ideal reader would flag; mock reviewers reading the *actual* posting catch where the document mismatches what was actually asked for. For academic positions, frame the personas explicitly as members of the actual search committee reading the actual posting and the application together — this surfaces fit-to-posting mismatches the funder-profile-only frame misses.
4. Launch personas in parallel as background subagents — each gets the application file + posting + persona prompt + (funder profile or department profile)
5. Synthesize: convergent flags (3+ reviewers) are high-priority; divergent flags are specialty insights worth holding

Personas should be oriented by lens, not checklist. Trust them to surface what they notice.

After each pass, log to `LEARNING_LOG.md` in the application folder: what convergent flags surfaced, which persona prompts produced sharp critique vs. shallow, what spec refinements would help.

*First used 2026-04-25 on Wenner-Gren (5 personas; surfaced AI dominance, theoretical density, Pvlvcekolv-Muscogee handling as convergent flags). Used 5+ times as of 2026-05-06 — promotion to standalone skill is queued (see Future Enhancements).*

---

## Step 5.9: Mechanical cleanup (after June's final edits, before save)

*Added 2026-05-06. Voice-check catches contamination patterns; Williams's principles catch structural prose problems. Neither catches the small mechanical issues — typos, double spaces, inconsistent dash usage, missing serial commas where June uses them, stray punctuation — that accumulate across many revision passes. This step is a final mechanical sweep on June's converged version.*

**When this runs:** AFTER June has finished sequential workshopping (Step 5.5) and the document has converged on a final. NOT during drafting. NOT on the agent's first draft. Running it earlier wastes effort because June will continue editing.

**What it does NOT do:** voice changes, structural changes, register changes, word choice changes for clarity. Those belong upstream. This is mechanical only.

**Operation:** Dispatch a haiku subagent on the final .md (NOT .html — see `feedback_voicecheck_html_workflow.md`).

**Subagent prompt template** (use `Agent` tool, `subagent_type: general-purpose`, `model: haiku`):

```
You are doing a final mechanical cleanup on a finished document. June Bloch wrote and edited this; her voice and structure are correct. You are NOT editing for voice, register, or clarity. You are catching mechanical issues only.

Input: [path to .md file]

Check for:
1. Typos and obvious spelling errors
2. Double spaces, missing spaces after punctuation
3. Inconsistent em-dash usage (June uses —, not -- or –, except inside code blocks)
4. Missing serial commas in lists where June uses them (her pattern: she uses serial commas)
5. Inconsistent quote style (June uses straight quotes in .md, curly quotes are fine if already converted)
6. Stray punctuation, doubled words ("the the"), broken sentence fragments from incomplete edits
7. Markdown formatting issues (broken links, unclosed bold/italic, malformed headers)

Output: a list of proposed corrections with line numbers and before/after. Do NOT auto-edit. Format:

Line N: "before text" → "after text" — [reason]

If no issues found, report "No mechanical issues found."

Do NOT flag style choices, voice patterns, sentence structure, or word choice. Those are not your concern.
```

**After the pass:** Read the report. If it's empty, proceed to save. If there are flagged items, apply them with `Edit` (one at a time, verifying each — June's text is ground truth and the haiku subagent can flag false positives). Don't show the report to June unless something is genuinely ambiguous; she's already done her editing.

**Why haiku, not inline:** Mechanical sweeps benefit from a different reading mode than voice/structural review. Haiku is fast, cheap, and good at this kind of pattern-matching. Saving the main agent's context for the substantive work.

---

## Step 6: Save and update

1. Save draft(s) to the application folder
2. **Save `DRAFT_PLAN.md` (from Step 3.8)** to the application folder if not already there. The plan is part of the application's history and an input to the Step 3.8 aggregate review. The "Conversation notes / what happened" section should be filled in before save — that's the per-use learning capture.
3. **Append a row to `VERSION_LOG.md`** — one row per transition (when you save vN+1, append a row classifying the move from vN). Columns: `From | To | Type (structural/fine-grained) | Author (AI/June/June+AI) | Notes`. Copy `templates/VERSION_LOG_TEMPLATE.md` if the file doesn't exist. The Notes column is what makes the log useful three weeks later — write one sentence on what *the pass was trying to do* + wc delta, not just what changed. The voice-check learning loop reads this directly via `--manifest VERSION_LOG.md`, replacing post-hoc reconstruction. (Why this matters: WG had 22 versions with intent reconstructed retrospectively from session logs. Forward-looking logging keeps signal that decays over time. Column format must match `writing_check.py`'s parser — From/To/Type/Author/Notes.)
4. **After June submits, save a clean `*_final.md`.** Once the application is submitted, the markdown text of the final document needs to live in the folder as `*_final.md` (e.g., `COVER_LETTER_final.md`, `RESEARCH_STATEMENT_final.md`). Without this, future agents adapting from this application have to reverse-extract from PDF or HTML, which is error-prone. The `_final.md` is the canonical source-of-record for the submitted text. If the final was assembled from a `*_v23.md` or similar, copy that to `*_final.md` (don't just leave the version-numbered file as the final — the name `_final.md` is the marker). For artifact files (PDF, HTML rendered output), keep them too — they're useful for sharing — but the `.md` is the source.
5. Save/update `APPLICATION_CHECKLIST.md` in the folder
6. Note what's done vs. what needs June's review
7. Update `Applications_Tracker.md` status if needed

---

## Step 7: Post-submission learning loop (after June submits)

After an application is submitted and June's final versions are available, run the voice-check learning loop to update the voice profile. This is how the system improves over time — June's revision choices are ground truth for what her voice IS.

**Don't improvise — follow the canonical procedure.** See `LEARNING_LOOP_PROCEDURE.md` (this dir) for the full workflow: prerequisites, version manifest construction, genre stylometry bootstrap, sequence-mode invocation, and the rule that mechanical script-running and qualitative CDA work belong in *separate sessions*. The procedure is the authoritative reference; this section just summarizes when and why.

**Quick reference:**
- **Single-pair applications** (one agent draft → one final): `python3 writing_check.py --learn FIRST.md FINAL.md --genre G [--notes "..."]`
- **Multi-version applications** (5+ revision drafts): point at `VERSION_LOG.md` (built incrementally during drafting per Step 6) — `python3 writing_check.py --learn-sequence --auto-discover . --pattern "..." --manifest VERSION_LOG.md --genre G`. If only `VERSION_MANIFEST.md` exists (older convention), use that instead.
- **Always** use the `.md` source, never `.html`
- **Always** specify `--genre` if the application has a known genre register (humanist_fellowship, ea_grant, academic_position, tech_position, etc.) — this prevents genre-adaptive shifts from contaminating the user voice baseline

**What runs:** diff analysis (sentence-level change classification + paragraph reorder detection), quantitative update (stylometry/perplexity/embeddings via EMA, decomposed by genre vs. voice if `--genre` is set), paragraph + cohesion metrics, and a printed qualitative analysis prompt for the agent to follow up on in a fresh session.

**Important — v0 convention:** Immediately after producing the first agent draft, save it as `[doctype]_v0.md` in the application folder (e.g., `cover_letter_v0.md`, `research_statement_v0.md`) **before** the revision conversation starts. This is the baseline for the learning loop. If June touches v1 before v0 is saved separately, the baseline drifts — the loop trains on June-already-revised→final instead of agent-raw→final, which is the signal that teaches the profile what the agent got wrong. Never rename or overwrite v0 once saved.

**When to stop:** When agent first drafts require primarily structural/content revision (not sentence-level voice fixes), the profile has converged. Keep running the loop but expect diminishing returns.

**What this is NOT:** This is not an excuse to re-edit docs June has already revised. Her edits are ground truth. The loop learns FROM her edits to produce better first drafts next time.

---

## Step 8: Pipeline reflection (periodic)

After significant revision sessions, friction, or a cluster of applications, run the reflection workflow at `REFLECTION_WORKFLOW.md`. It reviews where friction happened, identifies structural vs. incidental problems, compares to current pipeline state, and makes targeted fixes. This is how the pipeline improves over time — the voice-check learning loop (Step 7) learns from individual draft revisions; the reflection workflow learns from session-level patterns.

---

## Post-submission workflow

### When an application is submitted
1. Update `Applications_Tracker.md` — status → "Submitted," record date and materials sent
2. Archive key materials: `python3 save_materials.py <file> "<app_name>" --doc <type> --track <track>`
3. If June is excited about the position, generate an interview prep doc from `templates/interview_prep_template.md`
4. Create a follow-up calendar reminder (Gmail MCP + Google Calendar): 2 weeks for tech, 4-6 weeks for academic

### Following up
- **Academic**: 4-6 weeks after submission if no confirmation. Academic searches are slow.
- **Tech**: 2 weeks. If no response after 2 check-ins, move on.
- **Fellowships**: Usually no follow-up needed — they communicate on their own timeline.
- Use templates in `templates/follow_up_emails.md`
- **Gmail MCP**: Search prior correspondence, check for confirmation, draft follow-ups. Always draft — never send without June's approval.

### When an interview is scheduled
1. Update `Applications_Tracker.md` — status → "Interview Scheduled," add date
2. Generate interview prep: `templates/interview_prep_template.md` → save as `[AppFolder]/INTERVIEW_PREP.md`
3. Research the institution/team/interviewers — publications, recent hires, department news (Semantic Scholar + WebSearch)
4. Read most similar prior interview prep (Netflix `KEY_INFO_AND_PREP_NOTES.md` is the gold standard)
5. Identify gaps to be honest about and prepare framings

### After an interview
1. Send thank-you within 24 hours (`templates/follow_up_emails.md`)
2. Fill in the debrief section of the interview prep doc
3. Update `Applications_Tracker.md` — log interview, interviewers, key themes
4. Set a 2-week follow-up reminder if no response

### When an offer arrives
1. Update tracker — status → "Offer"
2. Research salary/benefits norms:
   - Academic: discipline averages; negotiate course load, startup funds, research support
   - Tech: salary bands (levels.fyi, Glassdoor); negotiate equity, remote policy, research budget
   - Fellowship: stipend usually fixed; negotiate institutional affiliations, publication policies, timeline
3. Draft counter-offer talking points if needed
4. If declining, use the decline template in `templates/follow_up_emails.md`

---

## The one-line prompt

After clearing context, June just types:

```
Draft [Application Name from tracker]
```

or

```
Next application
```

The agent reads this file, checks `Applications_Tracker.md` for the next undrafted application by deadline priority, and follows the steps above.

---

## Future enhancements (parking lot)

*Items identified but not yet built. Tracked here so they don't disappear. Promote to a step or skill when the trigger condition is met.*

- **Adversarial reviewer → incorporated into `/printpress`** (Step 5.7 currently). Not promoting standalone. The adversarial reviewer is Stage 3 of the `/printpress` generalized drafting pipeline — designed 2026-05-07. Spec at `~/.claude/skills/printpress/SPEC.md`. Persona library will move to `~/.claude/skills/printpress/personas/`. Build post-FFS. Memory: `project_printpress_skill.md`.
- **ATS pass → standalone skill** (Step 4.4 currently). Currently a subagent dispatch with the prompt inline in PIPELINE.md. If used 3+ times and the prompt stabilizes, promote to `~/.claude/skills/ats-check/` so the prompt template lives in the skill rather than the pipeline.
- **Research-paper story pass.** The pipeline serves applications. June's research-paper drafting needs the same story-first treatment but with different genre conventions (argument structure, methods exposition, lit review as conversation). The "argument memo" framing didn't survive contact with practice — it's normatively gravity-laden. When June starts a research paper, scope a parallel pipeline for that genre. See `project_voicecheck_pipeline_redesign.md`.
- **Pre-draft conversation A/B test** (Experiment 3 from pipeline-redesign-spec). Once Step 3.8 has been used on 3–5 applications, compare drafts produced from a cyborg-conversation plan vs. drafts produced from solo agent planning. Measure: how much of the first draft survives June's read. Validates whether the new step does what it's designed to do.
- **Voice-check signal-priority manifest column.** `--learn-sequence` currently uses even-sampling across fine-grained pairs; should prefer high-signal pairs from manifest annotation. See `project_voicecheck_track2_done.md` item 4.
- **Voice-check `--auto-discover` exclusion of VERSION_MANIFEST.md.** Small fix; manifest currently gets globbed as a spurious version when in the same dir.
- **Other-genre voice-check overlays.** `tech_position` and `ea_grant` have qualitative overlays. `humanist_fellowship` has stylometry but no qualitative overlay. `academic_position`, `teaching_statement`, `research_statement` overlays don't exist. Each needs the learning-loop CDA-sweep treatment.
- **`VOICING_PARAMETERS.md` ↔ voice-check profile cross-references.** Neither doc currently references the other.

---

## Current queue

**`Applications_Tracker.md` is authoritative.** Check it for current status, deadlines, and queue priority. `resources/PRIORITIES.md` is the master schedule with constraint context (FFS window, etc.).
