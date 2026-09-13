# Genre config: non_academic_application

**Sources:** PIPELINE.md (`../PIPELINE.md`, esp. Steps 0, 0.5, 3.7 industry/tech variant, 3.5 word counts, 4 audience calibration, 4.4 ATS pass, 4.5 register, 5.5 sequential workshopping, 6 save, post-submission), Bloch_Application_Context.md (seven common drafting mistakes, voice characteristics), critic-swarm personas at `~/.claude/skills/critic-swarm/personas/non_academic_application/`, Job Search CLAUDE.md (HTML templates, knowledge-construction frame), printpress SKILL.md (cross-genre Stages, voice-check tag mapping)
**Updated:** 2026-05-07
**Status:** v1 — built ahead of first use; refine after first invocation

---

## When this genre applies

Non-academic role applications where the reviewer is a hiring manager / recruiter / panel of program staff (not a search committee or peer-review panel) and the application typically routes through an HR portal or ATS rather than a department/program email. Tracks include:

- **Tech / industry** — software, ML, research, product, engineering roles at companies (GitLab, Netflix, etc.)
- **EdTech** — Turnitin, ETS, Coursera, Canvas/Instructure, edtech startups
- **AI safety / AI welfare industry** — Anthropic non-fellowship roles, OpenAI policy/safety, Conjecture, etc. (For *fellowships* hosted at AI labs, see `grant_fellowship.md` — distinguish by reviewer composition, not host institution.)
- **Nonprofit / policy / civic tech** — research orgs, EA-adjacent orgs reviewed by hiring managers (not grant panels), think tanks
- **Government** — federal, state, local civic-tech and research roles

Hallmarks: review by a hiring manager (the person the role reports to or works alongside), application routed through an ATS (Greenhouse, Lever, Workday, iCIMS, Taleo, BambooHR, SmartRecruiters, JazzHR, Ashby), document set is **resume + cover letter** (not CV + research statement), final output as **HTML** (per Job Search CLAUDE.md "Document generation and templates" — `resume_template.html`, `letter_template.html`).

**Subgenre variation visible in v1 (don't split yet, but track):**
- Tech / engineering — knowledge-construction framing for AI/ML roles (per `feedback_knowledge_construction_frame.md`); concrete tool-shipping evidence
- EdTech — lead with Autograder bias finding (per `feedback_autograder_differentiator.md`); pedagogical voice subordinate to product framing
- AI welfare industry — Recognition & Sentience theoretical scaffold + Reframe; bridges to `grant_fellowship` framing on measurement-foreclosure via the question-they-haven't-asked move (PIPELINE Step 3)
- Nonprofit / policy — different keyword conventions (theory of change, stakeholder engagement, FOIA, Section 508); voice-check needs `nonprofit_position` tag eventually

These have meaningfully different swarm composition needs (engineering manager vs. EdTech product reader vs. AI welfare research lead vs. nonprofit ED). Per printpress SPEC's "Genre splitting" guidance, hold as one genre with subgenre tags pending the periodic review trigger.

**Genre boundary:**
- Academic positions → `academic_position` (committee review, .docx + letterhead, scholarly register)
- Grants and fellowships → `grant_fellowship` (review panels, prompt-driven forms, even when hosted at industry orgs)
- Edge cases (Anthropic Fellows, Constellation Astra, AI safety fellowships at labs) — default to whichever genre matches the **reviewer composition**, not the host institution. If unsure, ask the author.

---

## Stage 0: Data-in (genre-specific)

**Find paths via the file-finding protocol** (printpress SPEC, "Where the skill finds local files"): working directory `CLAUDE.md` → parent `CLAUDE.md` → author profile → ask. PIPELINE.md now lives beside this file in the skill (`../PIPELINE.md`) and is **executable reference** — these configs cite its steps by number for instructions you must follow. Read the step a citation names.

### Required file load

| File | Source | If missing |
|---|---|---|
| `[AppFolder]/POSTING.md` | WebSearch → WebFetch → save **complete unedited posting text** | Create before proceeding. Cannot draft without this. |
| `[AppFolder]/COMPANY_PROFILE.md` | Web research + Stage 1 (see below) | Create before drafting; corresponds to academic_position's DEPARTMENT_PROFILE.md |
| `[AppFolder]/INTELLECTUAL_CONNECTIONS.md` | Output of relational-tracing (Stage 1 below) — for AI/research/edtech roles where intellectual fit matters; skipped for pure operational roles | Create at Stage 1 |
| Agent briefing | Path from working CLAUDE.md (June: `/Users/june/Documents/GitHub/profile/JUNE_BLOCH_AGENT_BRIEFING.md`) | Ask author |
| Voice document | Path from working CLAUDE.md (June: `/Users/june/Documents/GitHub/disabled_by_design/voice/VOICE_DOCUMENT.md`) | Ask author |
| Application context | Path from working CLAUDE.md (June: `Bloch_Application_Context.md`) | Ask author |
| Reframe Opportunity Brief (when relevant) | June: `agent_briefs/Bloch_Reframe_Opportunity_Brief.md` | Ask author |
| Voice-final priors (2–3 closest matches by track) | Track lookup table — see PIPELINE.md Step 0 ("track-specific closest-match lookup") | Ask author for closest prior application by track |

**Briefing scope is document-type-specific.** For non-academic CLs and resumes, PIPELINE.md Step 0 says: read Portfolio overview, Autograder (technical), Reframe (technical), Skills at full depth; skim extended research narratives and Teaching. Don't pull the full briefing for every doc.

### Voice-final prior selection

Same protocol as `academic_position.md` — see that file. Highlights:
1. Read `VERSION_LOG.md` if it exists; last submitted row is voice-final.
2. Otherwise: highest `_final.md` / `_voicefinal.md` / `_v[N].md`. Ignore agent-only intermediate drafts.
3. `Materials Archive/` entries via `save_materials.py` are canonical.

**Track-specific closest-match lookup** (from PIPELINE.md Step 0):
- Tech / industry → `Netflix/` or `GitLab/`
- EdTech → `VictoryXR/`, `ETS Research Scientist Equity/`, `Turnitin/`
- AI welfare/safety industry → `Anthropic Fellows/` (note: Fellows is borderline; pull voice not arc if applying to non-fellowship Anthropic role)
- Nonprofit / civic tech / policy — no June-specific prior yet; use closest tech-prior + adapt register

### COMPANY_PROFILE.md content

Built before Stage 1. The non-academic equivalent of DEPARTMENT_PROFILE.md. Per relational tracing (INSIGHTS.md 2026-04-29), the goal is to enter their conversation, not match keywords. Capture:

- **Company size and stage** — startup / scale-up / public / nonprofit / agency. Different reading registers; different what-counts-as-evidence.
- **Mission / values as stated** — pulled verbatim from their site (careers page, about page, blog). Verbatim matters because the document responds to the conversation they say they're having, not what an outsider summarizes.
- **Recent news / funding / shipping** — last 6–12 months. New round, new product, new policy posture, public technical writeups, layoffs/restructuring. Posture shifts under conditions; a profile from 18 months ago misreads the moment.
- **Products / services** — what the company actually makes. For tech, what the team specifically owns. For nonprofits, programs and theory of change.
- **Hiring-team identifiable members** — when findable. CTO, head of [function], engineering manager for the team, ED for nonprofits. LinkedIn + company blog + conference talks. Not always findable; don't fabricate.
- **Public technical / programmatic writing** — engineering blog, research pubs, white papers. This is the equivalent of faculty publications for relational tracing.
- **Glassdoor / public-record red flags** — recurring patterns in reviews (toxic management, layoff cycles, exploitative comp). Inform fit eval, not the draft itself.

**Vocabulary extraction (required for policy/research orgs):** List 3–5 key terms from the org's own published writing that don't appear in June's typical register. Example: AI Now uses "extractive," "austerity tool," "used on us," "corporate capture," "frontline expertise" — these are not the same as June's "normative gravity" or "community knowledge." The draft should enter their vocabulary, not just introduce June's. Failure mode: describing their work in June's language instead of theirs produces a letter that reads as "adjacent to their work" rather than "inside their conversation."

**Gap analysis (required for policy/research orgs with a developed critique):** What does their structural/critical analysis open but not yet answer affirmatively? Where is their roadmap underdeveloped — what alternative architecture or method are they calling for but haven't built? This is the sharpest differentiating argument for orgs with a strong critique but underdeveloped affirmative vision. Capture this explicitly so the draft can make the argument: "you've named the problem; I've been building toward the answer." AI Now case: they document extractive AI at the structural level but have no model for what community-controlled, non-extractive AI looks like architecturally — June has been building it.

**Output:** `[AppFolder]/COMPANY_PROFILE.md`. The Stage 3 swarm reads this to anchor the hiring-manager and culture-fit-reader personas.

### Fact assembly: FACT_INVENTORY.md

Same operation as `academic_position.md` — see PIPELINE.md Step 0.5. Non-academic-specific notes:

- **Map projects to role responsibilities, not to research programs.** The resume / CL is organized by what the candidate has shipped or run, not by intellectual genealogy. For each posting requirement, name the project that demonstrates it.
- **ATS-relevant keyword shortlist** — pull 8–15 role-defining keywords from the posting (skills, tools, methodologies, domain terms). These feed both the draft and the Stage 3 ATS-compatibility reviewer.
- **Quantified outcomes where they exist.** Tech and nonprofit registers value numbers (lines of code, scale, throughput, dollar amount, % impact, N students/users). For June: 312 modules, 160K+ lines, 76 frameworks, 7 disciplines, 10+ courses, ~$37,556 external funding. ⚠ **Two entries removed 2026-08-16.** *"6+ model families"* is **retired and partly disconfirmed** (`feedback_autograder_differentiator.md`) — the current, verified claim is **architecture-general across Gemma and Qwen including 72B**, with the cross-family claim still marked preliminary. *"15+ years CBPR"* conflicts with `feedback_fieldwork_duration.md`: Pvlvcekolv fieldwork is **"over a decade," never a specific count** (career *research* experience is a separate claim, and "sixteen years" is June-confirmed for that). Both sat inside a list headed *never invent* — a verified-numbers list is exactly where a retired number does the most damage. **Verify against `Bloch_Application_Context.md` / `Bloch CV.docx` — never invent.**
- **Reframe positioning** — per `Bloch_Reframe_Opportunity_Brief.md` if it exists. Tech audience needs the operationalization framing ("the gap between critical theorists who don't build and CS researchers who use insufficient metrics"); EdTech audience needs the bias-mechanism framing — **disclosure-to-deficit conversion, with quantization/compute-justice as the load-bearing mechanism** (⚠ NOT "output format as activation function for bias," retired June 2026 and a GATE-3 blocker — see the EdTech row below); AI welfare needs the substrate framing ("ethnic studies + affect theory = decades of tools for what gets counted as capable of feeling").

### Pull-from-prior priority

Same as academic_position. Pull from `*_final.md` (or extracted-from-PDF) of closest prior, not v1.md. The Hamilton-pulled-from-old-LMU-instead-of-final failure mode (PIPELINE.md Step 0.5, May 2026) applies equally here.

### Enforcement checkpoint

Before drafting each document, name (in writing or in a note): (a) which prior materials loaded, (b) what each gave you (voice / story bank / structure / arc), (c) which briefing sections read at full depth, (d) which posting keywords surfaced from FACT_INVENTORY. If you cannot answer all four, you skipped Stage 0 — go back.

---

## Stage 1: Pre-draft cyborg conversation (genre-specific)

The four moves come from printpress SPEC Stage 1. This section names genre-specific framings, gates, outputs.

### North star principle — state this before any other Stage 1 work

**The goal of every application is for the reader to finish thinking: "we can't afford not to hire her" — not stated, demonstrated implicitly.**

The mechanism is the mutual-opening approach (INSIGHTS.md 2026-04-29): identify what the hiring entity is opening and taking up in their work; identify what the author is opening and taking up in hers; find where those trajectories meet. The fit question should be unambiguous after reading — a reader should never finish wondering "why this candidate, for this role, at this org?"

**Hard pre-draft gate.** Before drafting anything — before Move 0, before Move 1 — answer these two questions in writing:

1. What is this organization reaching toward? What problems, threads, openings define their current work?
2. What is June reaching toward? What is she building toward, what threads is she pursuing?

Then: where do those trajectories meet? Name the intersection in one or two sentences. Not adjacent domains — the specific convergence point: what becomes possible *at the meeting point* that wasn't possible from either trajectory alone.

**This gate is not satisfiable by restating the concept.** "Both work on AI accountability" is similarity-clustering dressed as an intersection. A real intersection names something specific that wasn't visible before you held the two trajectories together. If you can't name a real intersection, the fit verdict from Move 0 should be reconsidered before any drafting begins.

This principle is cross-genre — it applies equally to `academic_position` and `grant_fellowship`. It lives here because non-academic postings (bullet-list qualifications against bullet-list skills) make the similarity-clustering default especially strong and especially easy to miss.

### Pre-conversation gate: analytical mode

Read INSIGHTS.md 2026-04-29 entry on relational tracing vs. similarity-clustering BEFORE Stage 1. Self-check: can you articulate the difference in one sentence? Then apply the hard gate above before proceeding.

**Why this matters even more for non-academic apps:** the posting register itself invites similarity-clustering (bullet-list "qualifications" against bullet-list "candidate skills"). The risk of producing a credential-listing letter is higher here than in academic apps. Relational tracing answers "what does June's work *open up* for this team's actual problem?" — which is what a hiring manager actually reads for, even when the posting was written like a checklist.

### Move 0: Fit evaluation (PIPELINE Step 1) — runs before Move 1

- **Direct matches**: posting requirements June meets with shipped work
- **Bridgeable gaps**: gaps with a credible bridge (transferable skill, adjacent project, specific learning trajectory)
- **Real gaps**: things she doesn't have and can't credibly bridge in this application
- **Verdict**: Strong / Decent / Weak

**If Weak: STOP. Tell the author. Do not draft.** Recommend a better-fit alternative. Tech/EdTech rolling deadlines mean wasted draft time also has opportunity cost — applications-that-could-have-been-better-targeted close while a weak-fit draft is being polished. (Per Job Search CLAUDE.md session-start rule and `feedback_verify_rolling_deadlines.md`.)

### Move 1: Candidate framings (printpress SPEC Stage 1 Move 1, contextualized)

Surface 2–4 framings for the non-academic position. For each:

- **What June's work opens up for this team** — what becomes newly possible if she's part of it. Forms: convergence, thread-uptake, productive tension, surprising opening (PIPELINE Step 3.7's industry-position variant). NOT "skills she brings" — what becomes newly possible.
- **What thread her work picks up** in their public technical/programmatic conversation. Their engineering blog, research output, recent public writing.
- **candidate for the question they haven't asked for this audience** — drawn from PIPELINE Step 3:
  - **Tech / AI** — the measurement framework constitutively forecloses what it can perceive
  - **EdTech / assessment** — the output format IS the bias (binary classification is the bird that isn't a bird)
  - **AI welfare** — what gets recognized as capable of feeling, by what epistemic regime
  - **Nonprofit / civic tech** — variable by mission; often a structural-conditions framing (the conditions that make the problem appear unsolvable are the design parameter)

Don't pick yet. Present the field. Move 1 opens; Move 2 takes up.

### Move 2: Author names the story

**The agent does NOT generate a candidate here.** Open with a question, listen, reflect back. For non-academic apps, the load-bearing thing the agent couldn't see from posting/profiles is often:

- A specific tool-origin scene (Autograder's first deployment, Reframe's framework-suppression detection, the Canvas evaluation crisis that produced EvalEye)
- The structural conditions that produced the build (Cabrillo conditions, post-non-renewal, contingent employment + survival architecture)
- A refusal of a frame the role's posting wants to impose ("we want a non-traditional candidate" — June is traditional in her field, novel in tech because of orientation)

Failure mode: agent answers for the author; collapses the relation. Recovery: ask. The author's redirect IS the leap.

### Move 3: Arc proposal under genre conventions and formal parameters

**Formal parameters (non-negotiable):** posting-specified moves ("describe a project where you…"), word/character limits, attachment requirements, portal field constraints (some portals enforce 4000-character cover letter caps, etc.).

**Non-academic CL conventions to work with or against:**
- **Lead with the deliverable framing, not disciplinary credentials.** This is the inverse of academic_position. The first 2–3 sentences should say what June has built / done that's relevant to this role, in this team's register, before any "I am a [X] applying for [Y]" boilerplate.
- **Compress academic jargon that's not load-bearing.** "Constitutively forecloses" → "the system's design determines what users can perceive." (PIPELINE Step 4 audience calibration, Tech bucket.) Note: compress jargon, don't compress *politics*. "Police state," "genocide," "ruthlessly exploitative" stay (per Bloch voice characteristics; `feedback_political_directness_tension.md`).
- **Knowledge-construction frame for tech apps** (per `feedback_knowledge_construction_frame.md`). Frame the work as collaborative human-AI knowledge creation, not as ethics/trust/bias-mitigation. The Autograder and Reframe stories are about what becomes knowable when the system is designed differently — that's the frame that landed for GitLab.
- **Em-dashes for casual directness are OK** (PIPELINE Step 4 Tech bucket). Academic letters tend toward semicolon-and-clause-chain register; tech letters can pivot mid-sentence with em-dashes.
- **Closing**: invite the conversation, name the next step. Less "available for interview at your convenience" than "happy to walk through any of this — June at [email]."

**Anti-pattern to flag at this move:** "non-traditional path" or "career pivot" framing. June is traditional in her field, novel in tech because of orientation (per drafting mistake #2 and #6). Don't write the document around her trajectory shape; write it around the work.

### Allocation table

For non-academic applications, the document set is typically two: **resume + cover letter**. Allocation is simpler than academic (no RS/TS/DS), but the cover letter is still the BRAID — it weaves the resume's bullets into a connected argument at their intersection. Build a brief allocation table in DRAFT_PLAN.md:

| Concept/Story | Full treatment in | Brief reference in |
|---|---|---|
| Autograder bias finding | Cover letter (story) | Resume (one-line) |
| Reframe technical depth | Resume (project entry) | Cover letter (gestural) |
| [Project most relevant to role] | Cover letter (story) | Resume (full entry) |
| [Other portfolio projects] | Resume (entries) | (not in CL) |

**Customize per application.** For grant-style structured applications routed through HR portals (sometimes the case for AI welfare industry roles), allocation rows are form prompts.

### Move 4: Section beats and load-bearing specifics

From FACT_INVENTORY and the allocation table, name what each section carries. For non-academic apps:

- **Resume bullets**: which projects, with what quantified outcomes (modules, lines, scale, model families tested, students taught). Verb-led ("Built," "Designed," "Shipped," "Led"). Williams's principle: characters as subjects, actions as verbs.
- **CL paragraphs**: opening (deliverable framing), middle (story demonstrating the Hakope reframe + project specifics), bridge (what June's work opens up for this team), close (invitation to talk).

### Intellectual landscape research (PIPELINE Step 3.7) — feeds Moves 1 + Stage 3 swarm

For non-academic positions where intellectual fit matters (research roles, AI welfare roles, EdTech roles where the team has public technical writing):

1. Surface what's known about the company from training data + recent web search — products, public technical challenges, blog posts, engineering culture.
2. Identify the specific team or product the role serves.
3. Apply the two questions: what does June's work open up for their product/problem? what threads in their engineering or research conversation does her work pick up?
4. For findable hiring team members: skim their public technical writing. Anchor culture-fit-reader and hiring-manager personas in Stage 3 to specific people where possible.

**Output two documents** (or one merged for ops-heavy roles):
- `[AppFolder]/COMPANY_PROFILE.md` — what kind of org, what the team does, public posture (already created in Stage 0)
- `[AppFolder]/INTELLECTUAL_CONNECTIONS.md` — for each relevant team / public author: what they work on, what threads of theirs June's work picks up, what her work opens up. Author-readable doc.

For pure operational / non-research roles, INTELLECTUAL_CONNECTIONS may collapse to a paragraph or be skipped. Don't force it.

### DRAFT_PLAN.md output

Save to `[AppFolder]/DRAFT_PLAN.md` using `templates/DRAFT_PLAN_TEMPLATE.md`. Captures: arc, openings/uptakes, the question-they-haven't-asked reframe, section beats with grounding, allocation table, what we're deliberately NOT doing, swarm composition decision, conversation notes.

**Failure modes to watch for** (same as academic_position): approval-seeking framing; directive extraction without understanding-shift.

**When to skip legitimately:** very short cover letters under 300 words, cold-outreach emails. Even then, name the arc in one sentence before drafting.

---

## Stage 2: Drafting (genre-specific)

Draft from `DRAFT_PLAN.md`. Step 2 executes the plan; it does not re-plan.

### Read the actual posting before writing a sentence

Re-read POSTING.md and any APPLICATION_STRUCTURE.md. The document responds to:
- Required content elements named explicitly in the posting
- Word/character limits per section (some portals cap CL at 2000-4000 chars)
- Posting-specific instructions ("address how you have…")

Reviewers (and ATS keyword search) grade against the posting; a beautifully-written non-response loses to a competent direct response.

### Audience calibration (PIPELINE Step 4)

| Bucket | Posture |
|---|---|
| **Tech / industry** | Lead with deliverable framing. Compress academic jargon (not politics). Knowledge-construction frame. Reframe = the operationalization gap. Em-dashes OK. Map findings onto THEIR product/problem. Avoid: "constitutively forecloses," "probabilistic architectures," literature-review parallelism, theoretical architecture sections. Use: "the system's design determines what users can perceive." |
| **AI welfare industry** | Recognition and Sentience as framework, not paper. "Ethnic studies + affect theory = decades of tools for what gets counted as capable of feeling." Bridges to grant_fellowship register (less compression of theory than tech bucket) but ends with concrete deliverable framing. |
| **EdTech** | Lead with the Autograder finding — **disclosure-to-deficit conversion**: a binary wellbeing classifier reads a student *disclosing* structural hardship or disability as an at-risk flag, turning rigorous intersectional work into a deficit verdict. Load-bearing mechanism is **compute-justice / quantization** — the compression that lets a model run on the cheap hardware under-resourced schools can afford pushes contained sub-threshold false positives over the actionable threshold and re-pathologizes AAVE/ESL registers the full-precision model cleared. Harm is bidirectional. Theory: *"there is no neutral format — bias surfaces differently across surfaces."* Per `feedback_autograder_differentiator.md`. Describe Autograder by what it REPLACES in the instructor's workflow, not by technical architecture. Connect to THEIR assessment / teaching product. |

⚠ **Corrected 2026-08-16 — this row previously instructed the opposite, and the contradiction was live.** It said *"Lead with the Autograder finding (output format as activation function for bias),"* citing `feedback_autograder_differentiator.md` — **the very memory that retires that phrasing.** That memory (rewritten June 2026 through the SSRC verification pass) marks *"output format is the activation function for bias," "generative observation eliminates the disparity entirely," "replicated across 6+ model families,"* and *"43% of flags the model contradicted itself"* as **RETIRED and partly DISCONFIRMED — do not use.**

**And `activation function` is a GATE-3 blocker in `styles/JuneBloch/ForbiddenClaims.yml`** — it blocks handover, correctly. So an agent following this row wrote a draft that could not ship, on every EdTech application, and the failure surfaced only at QC. Verified still firing on two prior letters (`Turnitin/cover_letter_v2.md`, `GitLab/cover_letter_v6.md`).

*The general form, worth more than the instance:* a retirement that reaches the memory and the linter but not the genre config produces a workflow that **instructs the error and then blocks it**. When retiring a claim, grep every consumer — see `DRAFTING_STANDARD.md` `PRO-10`.
| **Nonprofit / civic tech / policy** | Different keyword library (theory of change, stakeholder engagement, Section 508, FOIA, logic model). Less tool-shipping, more program-and-outcome register. Lead with the population served + the structural-conditions framing that produced the work. |

For applications that straddle buckets, ask the author rather than guess.

### Voice-check tag mapping

Per printpress SKILL.md Stage 2 table:

| Subgenre | voice-check `--genre` tag |
|---|---|
| Tech / industry | `tech_position` |
| EdTech | `tech_position` (no separate tag yet — same register; flag for v2 if EdTech-specific patterns accumulate) |
| AI welfare industry | `tech_position` for industry roles; `ea_grant` for fellowship-adjacent (decided per application) |
| Nonprofit / policy | **No tag yet — needs new `nonprofit_position` voice-check tag.** v1 inference: confirm with author at Stage 0 whether to use `tech_position` as closest available or build the tag. (Per printpress SKILL.md Stage 2 table note.) |

### Word count targets

| Document | Target |
|---|---|
| Non-academic cover letter (tech/nonprofit/museum/general staff) | **~500 words working target, ~525 hard ceiling at five paragraphs** — one page on `letter_template.html`. **Measured 2026-08-16**, superseding two guesses in a row. |

**The length figure has now been wrong in both directions; read this before changing it again.** The original "~600–800 words" was unsourced assertion, and it produced a FAMSF museum-staff letter no one-page letterhead could hold. The 2026-08-13 correction to "~350–450" was a reaction to that failure and was also unmeasured — roughly 50–150 words *tighter* than the template actually holds, which spends real content for nothing.

**What was actually measured (2026-08-16):** `letter_template.html` rendered through WeasyPrint at June's own prose's mean word length (6.07 characters), five paragraphs — **one page holds up to ~525 words; 530 breaks to page two.** Independently corroborated: her own FAMSF letter converged at **492 words** on one page after she cut it by hand.

*Caveats, because this number will get reused:* WeasyPrint's font metrics are not identical to Chrome's Save-as-PDF; more paragraphs means more inter-paragraph space and a lower ceiling; Chrome headless is not a usable cross-check here (the empty template paginates to two pages under it). **Re-measure if the template changes** — method in `_application_evidence/REVISION_ANALYSIS_2026-08-16_FAMSF.md` §6.

**The sizes are proportions of the final target `T`, not fixed numbers** — so the same discipline carries to academic letters, grant sections, and form fields where `T` differs. Per `DRAFTING_STANDARD.md` `PRO-11`:

| Stage | Size | For this genre (`T` ≈ 500) |
|---|---|---|
| Capture | record actual; ~1.6 × T is provisional | often around 800 words when the material supports it |
| Author marks | full assembly | KEEP / DROP / UNSURE before selection |
| Post-marking handoff, if made | record actual; ~1.2 × T is provisional | around 600 is one experiment, not a requirement |
| June edits (cuts **and adds**) | → T | ~500 words, one page |

**The author sees the assembly before any selection pass.** After marking, choose an AI-proposed reversible cut, author-led selection with local AI compression, or a hybrid. A handoff near 1.2 × `T` may leave useful room for additions, but both the ratio and AI-cut quality are unresolved experiments. Record what she receives, restores, rejects, adds, and ships rather than hardening the route.

Marking is not prose-editing. Unmarked material remains `UNSURE`, not permission to delete.
| Resume | one page if early-career-targeted; two pages OK for senior/research roles. June's portfolio depth often warrants two pages |
| Application essay (where required, e.g., EA-org screens) | per posting; usually 250–500 words per prompt |
| Screening-question / short-answer response (HR follow-up, portal free-text, "a short paragraph") | per posting; typically 150–250 words |

These are targets for the *final* document, not the assembly or handoff. Per printpress Stage 2, capture genuine evidentiary abundance and record the actual ratio. The provisional 50–75% over figure can orient a new-material capture but cannot override coherence, ported voice-final prose, or a thin evidence base. The author marks the assembly before any autonomous selection; the later route is chosen rather than assumed.

#### Three ways the capture pass fails — all observed, all preventable (added 2026-07-29, PEN America screening-question session)

The "capture long, then cut" rule was already in this config and was violated anyway, three times in one session, each time by a different route. The rule alone does not bind; these are the specific holes to close.

**1. A length stated in the prompt is a FINAL target, never a drafting target.** When the posting or requester names a length — "a short paragraph," "250 words max," "brief response" — that number governs the submitted artifact. The capture must still contain the setup, stakes, evidence, and connective tissue needed to make a real selection. Record the actual ratio rather than forcing 1.5–1.75×.

**2. Small artifacts do not automatically exempt the capture logic.** A short response can still need alternate framings or evidence because one wrong framing consumes the whole piece. Scale the artifact and marking interface to the decision; do not create ceremony where no selection question exists.

**3. A padded capture is not a capture.** The subtlest failure and the hardest to self-detect: the agent complies with "write long," but writes the final draft it has already converged on *plus filler* — added clauses, restatements, softening transitions. That is inflation, not over-supply. A genuine capture contains more **material**: distinct beats, additional evidence, alternate framings and openings that may not survive, connective tissue that explains rather than asserts.

**Two checkable tests (run both on your own cut) — they catch different fakes.**

*Test 1 — what kind of thing got cut?*
- Mostly words *inside* sentences → the capture was padded. The abundance was fake and the cut selected from nothing.
- Mostly whole sentences, beats, or paragraphs — including discarding an entire framing in favor of a better one → the capture was genuine.

*Test 2 — did anything good get cut?* (June, 2026-07-29; the stronger test.) A genuine capture contains novel content and beats that do **not** survive: an alternate opening, a second line of evidence, an argument that turns out not to fit this reader. If everything in the capture reached the final, the capture was never over-supplying — it was the final draft written out long, and it will pass Test 1 while still having failed. **A capture with no casualties is a failed capture**, regardless of its word count.

**Required output of every AI cutting dispatch, when that route is chosen:** a reversible handoff, a diff, the list of what was cut and why, and a named list of genuine losses. An empty losses list is evidence to inspect—not automatic proof that the capture failed.

**Why a separate AI cutting dispatch matters when that route is chosen.** An agent that already holds the final shape tends to generate toward its own destination. Preserve the cold assembly, obtain author marks, then give a separate cutting reader the assembly plus those marks. Author-led and hybrid routes do not require a fictional autonomous cutting stage.

### Cutting swarm composition (Stage 2 — only when the post-marking route includes AI cutting)

If this route is chosen, core readers are **hiring-manager** and **author-informed**. Optional for longer documents: **culture-fit-reader**. Give each reader the author's marks. Exclude **ats-compatibility**, **intelligibility**, and **jargon** from structural selection; they remain Stage 3/4 checks.

Each included persona runs `cut_reader.md`'s three-pass procedure in character — reading and judging load-bearing-ness as that specific reader would, not as a generic voice. Anchor hiring-manager and culture-fit-reader the same way Stage 3 does (specific identifiable people from `COMPANY_PROFILE.md` where possible).

### Voice-check during drafting

Same protocol as academic_position. Pre-draft: read voice profile, select `--genre` tag. In-flight: write in voice. **Post-draft is TWO passes — the linter alone is NOT the check:**

1. **Quantitative linter** — self-run `writing_check.py DRAFT --genre [tag] --profile [profile]`. Silently fix contamination (hedges, corporate jargon, padding). This is regex/stylometry only: it counts em-dashes and flags long sentences, but CANNOT judge whether a topic sentence *makes a move or announces one*, whether a claim is *demonstrated or merely asserted*, or whether specifics ground the theory.
2. **Qualitative pass (agent-applied) — mandatory, not optional.** Read the draft back against the merged profile's qualitative checks (global `pre_draft` + this genre's `qualitative`). Enforce prescriptive checks; note diagnostic ones. Surface findings as suggestions the author accepts/rejects. Per voice-check SKILL.md the linter "is not a positive voice match — passing it does not mean the prose sounds like the author wrote it." The qualitative pass is where you verify it actually does. **Failure mode (2026-07-06): agent ran the linter, declared post-draft done, skipped the qualitative pass. Do not stop at the linter.**

Williams's *Style* applies continuously.

### What the 2026-08 research established — read before drafting

*Added 2026-08-09. Restated here rather than only referenced, because Stage 2 dispatches cold subagents that see only their brief. **Put these in the brief.** Full sourcing: `_application_evidence/` and the `cover_letter` / `tech_position` / `nonprofit_position` blocks of the voice profile.*

**Status rule:** every item is **convention** or **hypothesis**, never finding. **No study measures whether cover-letter quality affects callbacks** in any sector. Carry the status.

**Who is being cited below, and why they count** — you have no context on these names:
- **Judd Kessler** — an economist at Wharton who studies hiring and co-authored one of the two rigorous studies this evidence base relies on. The quotation below is him describing his *own* change in behaviour as a reader of applications.
- **Linos (2018)** — a randomised recruitment experiment published in a public-administration journal, testing how job-ad framing affects who applies.
- **Verhaest et al. (2018)** — a field experiment sending paired applications from equally and over-qualified candidates to real job openings.
- **NPEU agreements** — collective bargaining contracts at two national advocacy nonprofits. Not testimony: binding, public contract language describing how those organisations are *obliged* to run hiring.
- **Alison Green** — writes the long-running workplace advice column *Ask a Manager*; the funnel described is her own hiring practice, stated in her own words.

1. **The part of the letter that makes the case — what genre analysts call the *argument move* — is where letters fail.** Writers produce every expected element, then write an argument that restates the previous one and never ties specific capacities to what the posting asked for. Form: *background → what that does for them → why this, why now.* Almost everyone does the first and skips the second. Readers do not infer.

2. **"Generic" means unresponsive to THIS situation, not conventional.** Test each sentence: could it appear in a letter to a different company?

3. **⚠ Ask FIRST: does this employer score blind?** Organizations that strip identifying information before scoring generally say so — EA-adjacent orgs openly, some tech companies, a growing number of nonprofits. **If blind:** the letter can only work on content and reasoning; naming a contact or leaning on affiliation is stripped or flags as defeating the process. One organization dropped cover letters entirely because applicants were using them to leak identity past the blind. **If not blind:** relational signal is available — and June's only interview to date came through exactly that channel. **This determines what the letter can contain, before a word is written.**

4. **Sector may be the wrong cut.** Three independent agents proposed better divisions than industry-vs-nonprofit: by **organization size**, and by **whether the employer scores blind**. Nothing found supports treating nonprofit as a distinct track. If a distinction is needed, use one of those.

5. **Mission-fit language is folk knowledge, and the evidence runs sideways.** The heavily-cited nonprofit "mission attachment" research is about *retention of people already hired*, not selection — routinely mis-cited. Linos (2018, *JPART*) found career and personal-benefit framing roughly **three times** more effective than public-service-mission framing at generating applications, "particularly effective for people of color and women." That's about who applies, not how they're judged — but the sector's confidence in mission framing is not evidence-based. **Do not declare passion. Name the specific campaign or program** — the thing that shows you read past the About page.

6. **Competent prose stopped being a signal.** Judd Kessler (Wharton), on his own behavior: *"I used to get really good cover letters, and be like, oh, I should really talk to this person… and now I don't."* His mechanism: the letter didn't get worse, it **stopped discriminating** — a signal everyone can send isn't a signal. This runs on what readers *assume* about production cost, so a better tool doesn't fix it. **Put weight on what stayed expensive:** specific verifiable content, actual record, situated knowledge nobody else could supply.

7. **The channel may matter more than the document.** Employers facing volume are abandoning inbound postings rather than reading harder — one publication pulled its ad within 12 hours of 400+ applications and hired through outreach. Application volume roughly doubled 2022–25 while applications *per recruiter* rose 412%, because recruiters per organization fell 56% — **the gap is layoffs, not AI.**

8. **Overqualification: the folk wisdom is contradicted where measured.** Overqualified candidates were **19% more likely** to be directly invited to interview (Verhaest et al. 2018); overeducation is a *smaller* signal problem than unemployment. Untested at doctoral level. The reader's inference is still real — June needs a genuine felt answer to "why this role," not a diplomatic one.

9. **Mechanics that silently break an application** (see PIPELINE Step 4.4, corrected 2026-08-07 after being wrong for three months): **never upload .html** — Greenhouse doesn't accept it and the upload fails outright, so `resume_template.html` is an authoring format and the submitted artifact is always the rendered PDF. **Files over 2.5 MB upload cleanly and never parse.** **Do not flag duration phrasing ("3 years") as a defect** — a preregistered field experiment with 9,022 real applications found that format *raises* callbacks ~8%, ~15% for applicants with gaps. Multi-column layouts, tables, and image-only PDFs are real hazards; **auto-rejection on résumé content is not** — no vendor documents it.

10. **Capture any AI-use disclosure requirement at Stage 0.** Where policies exist they govern *provenance of substance, not register* — June's practice sits inside every one located — but some are procedural and failing them is a hard fail. AI Now required disclosure at the bottom of the cover letter.

11. **Two fabricated statistics — never repeat.** "75% of résumés auto-rejected by ATS" → a 2012 product launch by a vendor that folded in 2013. "Recruiters spend 6 seconds" → a résumé-rewriting company's own unpublished n=30 study. The real figure from a recruiter's disclosed data: **median read 1 minute 40**, with screening accuracy near chance (κ=0.13, 53%). A third figure, "~55 seconds per portfolio," is currently forming the same way — do not adopt it.

### The seven common drafting mistakes (Bloch_Application_Context.md)

Critical for non-academic apps; mistakes #1, #2, #6, #7 are higher-leverage here than for academic:

1. Treating academic and tech work as separate tracks → **especially load-bearing**. One practice, different media.
2. "Non-traditional" framing → **especially load-bearing for tech apps**. June is traditional in her field; the novelty is *orientation*, not credentials.
3. Precarity as backstory rather than design condition
4. Softening political language
5. Separating disability from design
6. The "journey" or "pivot" frame → **especially load-bearing**. Don't write the arc around a career-shape; write it around the work.
7. Calling Reframe a chatbot → **never describe it as a chatbot in any application**. Engine, 312 modules, 5-stage Generative Irresolution workflow.

### Anti-generic test

If a sentence could describe any candidate with a PhD and some tech experience, delete it. Specificity is the constraint layer.

### Sentence-level rules (Bloch_Application_Context.md)

The 10 rules apply equally here. Especially load-bearing for non-academic: rule 4 (tools by what they REPLACE), rule 6 (categorical modality), rule 8 (constructivist framing — knowledge from practice, not "I discovered"), rule 3 (no self-aggrandizing frames — let facts carry weight; tech audiences are register-allergic to "groundbreaking paradigm-shifting" prose).

### Never invent numbers

Same as academic_position. Use `[DATA NEEDED]` over plausible fabrication. The Reframe timeline (tool-building started ~November 2025 — NOT "two years," NOT "since 2024") is a recurring inflation point. Verify against `Bloch_Application_Context.md` and `Bloch CV.docx` before drafting.

### Format

Per Job Search CLAUDE.md "Document generation and templates":
- Cover letter: `.md` draft → renders to **HTML via `letter_template.html`** (NOT .docx with letterhead — that's academic_position)
- Resume: `.md` draft → renders to **HTML via `resume_template.html`**
- Final delivery format depends on portal: HTML-rendered-to-PDF, .docx, or paste-into-portal-text-field. Match format of closest prior application.

Voice-check learning loop reads the `.md`, never the rendered HTML (per `feedback_voicecheck_html_workflow.md`). Always preserve the `.md` source.

---

## Stage 3: Reviewer swarm (invoke /critic-swarm)

### Pre-swarm: reader takeaway audit (PIPELINE Step 4.7)

Write `[AppFolder]/READER_TAKEAWAYS.md` — 5–8 things the reader should know about the candidate by the end of the package. Distributed across: capability evidence, role-fit specificity, what's distinctive (the bias finding, the engine, the orientation), and (if intellectually-relevant) what the candidate's work opens up for the team.

Read the draft against the list:
1. Does each takeaway land?
2. Does anything in the document NOT serve a takeaway? Candidates for cut.
3. Are takeaways in the right weight? Buried high-priority needs to move forward.
4. Is structural balance right? A research-role CL where research only appears in the last 25% has a balance problem.

### Persona stack

**Stack name:** `non_academic_application` (per `~/.claude/skills/critic-swarm/personas/non_academic_application/`).

Personas in the stack:
- **Hiring manager** (`hiring-manager.md`) — the primary reader who decides whether the candidate moves to interview. Reads pragmatic, time-pressured, candidate-comparative. Day-30/day-90 imagination. Bias toward reasons to cut (because reading a stack).
- **Culture-fit reader** (`culture-fit-reader.md`) — reads for whether the candidate would work well with the team / org culture. Anchor to COMPANY_PROFILE.md for stated values; flag culture-fit register that's actually exclusionary-coded (well-known anti-pattern).
- **ATS-compatibility reviewer** (`ats-compatibility.md`) — gate-check. Will the document make it through to a human? Mechanical, checklist-form (the one persona where checklist is appropriate). See PIPELINE.md Step 4.4 ATS subagent and the ats-compatibility persona file for the operationalized check.

Anchor hiring-manager and culture-fit-reader to specific identifiable people from COMPANY_PROFILE.md where possible. Anchor to roles otherwise.

### Context passed to /critic-swarm

- The draft(s) — resume + cover letter file paths (in their delivery format for ATS reviewer; .md for hiring-manager and culture-fit)
- `POSTING.md` — verbatim, the actual posting
- `COMPANY_PROFILE.md` — for culture-fit and hiring-manager anchoring
- Author profile path (if set up)
- Role type — passed to ATS reviewer for keyword library calibration (tech / edtech / nonprofit / govt / industry research)

### Always-runs reviewers

Intelligibility, jargon (venue-aware — the jargon reviewer for tech contexts checks academic jargon that doesn't translate, not the inverse), author-informed (profile-gated). These run inside /critic-swarm regardless of stack.

### ATS report handling (PIPELINE Step 4.4)

The ATS reviewer outputs to `[AppFolder]/ATS_REPORT.md` with high-priority flags, medium-priority flags, honest-additions list (keywords June plausibly has experience with that the resume doesn't currently surface), and format/parse issues.

**Triage in Stage 4** (revision): high-priority flags address first; honest-additions get author review (don't auto-add — June decides). Format flags fix mechanically. Don't keyword-stuff; integrate honestly where the experience exists. (Per PIPELINE.md Step 4.4 and the ats-compatibility persona file.)

### Synthesis output

Cut list first → convergent flags → threading suggestions → specialty insights → mechanical/ATS flags. /printpress passes synthesis to Stage 4.

---

## Stage 4: Revision (genre-specific)

### Sequential workshopping

Same protocol as academic_position — ONE revision at a time. Address convergent flags first; specialty insights second; ATS/mechanical flags last (mechanical fixes can batch).

**Exception: structural revisions integrating substantive new content** (a new project framing, a structural reframe of the CL opening). Batch the integration; preserve prior version as checkpoint.

**Content first, word counts later.** Lock content first. Compression as separate downstream phase. Non-academic CLs at 350–450 words leave far less room for redundancy than academic CLs — but compression discipline still belongs after content settles.

### Drafting & revision principles (printpress SPEC Stage 4)

Apply continuously. Same list as academic_position; non-academic-specific notes:
- **Less is more** is especially load-bearing — tech readers will not finish a 1200-word CL.
- **Action verbs with clear agents** matters even more in resume bullets. Williams principle: characters as subjects, actions as verbs.
- **Workshop language in chat, not in file** — don't churn the draft with exploratory rewrites.

For non-academic-specific:
- **Never cut political directness.** Tech-register compression is for jargon, not for politics. "Police state," "genocide," "ruthlessly exploitative" stay.
- **Never invent numbers.** Use `[DATA NEEDED]`.
- **Don't re-run voice-check on docs the author has edited.**

### Address ATS report

Triage flags from ATS reviewer:
- **High-priority** (would cause rejection / low-rank): address before save. Often title-translation gaps and missing posting keywords the candidate plausibly has experience with but didn't surface.
- **Medium-priority**: discuss with author; address what she chooses.
- **Honest-additions**: author review only. Never auto-add keywords; she decides.
- **Format/parse**: fix mechanically (linear-parse layout, standard headers, parseable date format, removing text-in-images).

### Overwhelm detection

Same as academic_position. Increasing typo density → shorter responses, targeted questions, simpler language, explicit check-in.

### Logging to LEARNING_LOG.md

After Stage 3 synthesis is addressed, log to `[AppFolder]/LEARNING_LOG.md`: which convergent flags surfaced, which persona prompts produced sharp critique vs. shallow, what spec refinements would help. Tag each learning as `genre-specific` or `potentially-generalizable`.

---

## Stage 4.5: Pre-save QC verification

Same checklist as printpress SKILL.md Stage 4.5. Non-academic-specific verification:
- [ ] **ATS report addressed** — high-priority flags resolved or explicitly held with author
- [ ] **Title-translation legible** — does the candidate's recent title use language the posting recognizes?
- [ ] **Format check** — final delivery matches portal requirements (HTML-rendered PDF, .docx, paste-text)
- [ ] **Text layer verified** — `python3 ~/.claude/skills/printpress/tools/check_pdf_textlayer.py "[App Folder]/*.pdf"` exits 0. A flattened PDF looks perfect and contains six extractable characters; nothing else in this workflow reads the rendered artifact.
- [ ] **Commitment matrix clean** — `COMMITMENT_MATRIX.md` cross-artifact audit run; no document, résumé line, or portal field contradicts another
- [ ] **Knowledge-construction frame** (for tech apps) — frame is collaborative knowledge creation, not ethics-mitigation register
- [ ] **Reframe described as engine, not chatbot**
- [ ] **No "non-traditional" or "pivot" framing**
- [ ] **Tailoring specificity (policy/research orgs):** Does the draft reference at least one specific org publication or stated argument by name? Does it use at least 2–3 vocabulary terms from the org's own writing (not June's coined terms)? Does it make the gap argument — not just alignment, but what June's work adds to what they can't yet do?

---

## Stage 4.6: Requirements Compliance Gate

Before declaring materials ready, run the cross-genre **Requirements Compliance Gate** (printpress SKILL.md § Stage 4.6): re-fetch the live posting/form, diff against `APPLICATION_STRUCTURE.md`, and verify every required document, limit, prompt/section/field, and submission convention is met. Non-academic especially: portal character caps, required screening questions, attachment/format constraints the posting prose doesn't foreground. Any unmet or changed requirement blocks "ready" — the author can override explicitly. Backstop to the Stage 0 Submission Requirements Ledger.

---

## Stage 5: Save + post-submission

### Mechanical cleanup

Same protocol as academic_position. Haiku subagent on the final `.md` (NOT `.html` — render artifacts contaminate metrics, per `feedback_voicecheck_html_workflow.md`). Per PIPELINE.md Step 5.9. Catches typos, double spaces, em-dash inconsistency, doubled words, malformed markdown. Does NOT do voice/structural changes.

### Save protocol

1. Save draft(s) to the application folder (`.md` source)
2. Render `.html` final via templates (`letter_template.html`, `resume_template.html`)
3. Ensure `DRAFT_PLAN.md` is in the folder; "Conversation notes" section filled in
4. **Append a row to `[AppFolder]/VERSION_LOG.md`** — `From | To | Type | Author | Notes` (per `templates/VERSION_LOG_TEMPLATE.md`)
5. **After submission, save `*_final.md`.** Markdown source, not HTML/PDF.
6. Save/update `APPLICATION_CHECKLIST.md` — done vs. needs-author-review
7. Update `Applications_Tracker.md` status
8. Archive: `python3 save_materials.py <file> "<app_name>" --doc <type> --track <track>`

### Voice-check learn pass

Same protocol — see `LEARNING_LOOP_PROCEDURE.md`.
- Single-pair: `python3 writing_check.py --learn FIRST.md FINAL.md --genre tech_position`
- Multi-version: `--learn-sequence --auto-discover . --pattern "..." --manifest VERSION_LOG.md --genre tech_position`
- Always `.md`, never `.html`
- Always specify `--genre`

### Post-submission workflow

Operational logic (June-specific; reference PIPELINE.md post-submission):
1. Update `Applications_Tracker.md` — status → "Submitted," date and materials.
2. Archive: `save_materials.py`.
3. If author is excited about the role, generate interview prep doc (`templates/interview_prep_template.md`).
4. **Calendar reminders: 1–2 weeks for tech (NOT 4–6 like academic).** Tech timelines are faster; rolling postings can close in days. Per PIPELINE.md post-submission section. Drafts only — never send without author approval.
5. **Follow-up cadence: 2 weeks for tech.** If no response after 2 check-ins, move on. (Compare academic: 4–6 weeks.)
6. When interview scheduled: tracker, INTERVIEW_PREP.md, research team/interviewers (Semantic Scholar for research roles + WebSearch + LinkedIn), prepare framings.
7. After interview: thank-you within 24h, debrief, log interviewers, 2-week follow-up reminder.
8. Offer: research salary norms (levels.fyi, Glassdoor); negotiate equity, remote policy, research budget.

### Skill-global writes

After Stage 5:
- Update `~/.claude/skills/printpress/genre_configs/non_academic_application.md` (this file) with refinements.
- Periodic genre review per printpress SPEC: every 3rd–5th use, surface at Stage 0.
- Tagged-generalizable learnings from `LEARNING_LOG.md` feed cross-genre principles.

---

## Subgenre notes (for future)

`non_academic_application` v1 spans:
- Tech / industry (engineering, ML, research roles)
- EdTech (Turnitin, ETS, Canvas/Instructure, edtech startups)
- AI welfare industry (Anthropic non-fellowship roles, OpenAI safety, etc.)
- Nonprofit / civic tech / policy (different keyword library)

Subgenre auto-detection candidates (for v2): posting URL host (`boards.greenhouse.io` etc. → ATS-routed; nonprofit ATS hosts vs. tech ATS hosts), posting language ("ship," "scale," "infrastructure" vs. "stakeholder," "theory of change," "logic model"), explicit org-type tagging in COMPANY_PROFILE.

Recurring swarm composition differences not yet resolved by single stack:
- AI welfare industry roles often need an additional research-lead persona anchored in published lab work
- Nonprofit roles benefit from an ED / program officer persona instead of generic hiring manager
- EdTech apps can use a product-manager persona (the person who'd integrate June's pedagogical insights into product roadmap)

These are subgenre-tag candidates for v2. v1: ask the author at Move 3 if not obvious.

**Voice-check tag gap: `nonprofit_position`** — voice-check has no overlay yet. Per printpress SPEC § Genres table, this requires a new tag and CDA-sweep treatment when the first nonprofit application is drafted. v1 fallback: use `tech_position` and flag the contamination risk to the author.

---

## Learning loop notes

### AI Now Program Associate (2026-05-25) — tailoring failure

**What failed:** COMPANY_PROFILE.md was thoroughly researched (AI Now's specific vocabulary, austerity-mechanism analysis, gap in their affirmative vision) but none of it made it into the draft. Nine versions passed through the pipeline; not one referenced a specific AI Now publication or used their vocabulary ("extractive," "austerity," "corporate capture"). The letter described AI Now at the level of "you work on AI and communities" — interchangeable with DAIR, Data & Society, or any peer org.

**Root cause:** The research was treated as background orientation rather than drafting source material. The pipeline asked "what threads does June's work pick up?" but accepted a generic answer ("they document how AI gets deployed on communities"). The enforcement mechanism was missing — no gate requiring named publications + org vocabulary in the draft plan before drafting.

**What v10 fixed:** Opens with *Artificial Power* (2025) by name; uses "austerity tool," "extractive deployment model," "frontline workers," "concentrating decision-making in vendors"; makes the gap argument explicitly ("what your structural analysis opens but doesn't yet answer"). The "I synthesize fast" language — dropped in v6 compression, a direct execution signal for this role — was also restored from v5.

**Cross-stack generalization:** Any application to an org with a developed public intellectual position (AI Now, DAIR, Data & Society, EFF, academic departments with named research programs) should pass the specificity test: could this letter be sent to a peer org with minimal edits? If yes, it's not tailored.

**System changes made (2026-05-25):**
- `DRAFT_PLAN_TEMPLATE.md`: Added "Tailoring anchors" section (vocabulary, named publication + argument, gap)
- `non_academic_application.md` Stage 0: Added vocabulary extraction + gap analysis to COMPANY_PROFILE.md requirements
- `non_academic_application.md` Stage 4.5: Added tailoring-specificity QC check

**v1 inferences requiring confirmation after first use:**
- Knowledge-construction frame as default for tech apps (sourced from one positive datapoint, GitLab CL, per `feedback_knowledge_construction_frame.md`). Confirm or refine after second tech app.
- 1–2 week follow-up cadence for tech (vs. 4–6 academic) — sourced from PIPELINE.md post-submission and tech-norm general knowledge. Confirm against author's actual experience.
- ATS report triage protocol (high-priority before save, honest-additions to author) — sourced from ats-compatibility persona + Job Search CLAUDE.md MCP-tools rule on never-auto-send. Refine after first ATS report return.
- Subgenre-specific reading patterns (EdTech leads with Autograder finding; AI welfare leads with R&S substrate) — sourced from `feedback_autograder_differentiator.md` and Anthropic Fellows positioning. Confirm after second EdTech and second AI welfare app.
