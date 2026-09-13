# Drafting Standard — generalizable across applications

**Built 2026-08-10, replacing an application-specific standard that duplicated material already in the author's voice-check profile.** This file contains only what is reusable on any posting. Nothing here names a specific employer, and no fact about the author lives here.

**What this file is NOT.** It is not the prose standard. That already exists and is better than anything written here.

---

## 0. Where the actual standards live — read these, do not re-create them

| Layer | Lives in | Lifetime |
|---|---|---|
| **Prose principles** | `~/.claude/skills/voice-check/profiles/june_bloch.json` — the `qualitative` array, entries with `role: pre_draft` | Stable; author-owned |
| **Author identity, record, failure patterns** | The author's briefing/profile documents (path from the working directory's `CLAUDE.md`) | Stable |
| **This posting's facts, corrections, forbidden claims** | `[AppFolder]/FACT_INVENTORY.md` | Per application; disposable |
| **Process: scope, roles, verification** | This file | Stable |

> ### Note, 2026-09-13 — the profile is real; its only copy is outside version control
>
> A 2026-09-12 session concluded this file was missing and wrote two successive corrections
> here saying so. **Both were wrong and are withdrawn.** The profile is present and current:
> **237,061 bytes, v3.13, 54 `qualitative` entries**, with `patterns`, `thresholds`,
> `stylometry`, `perplexity`, `embeddings`, `genres`, `theoretical_anchors` and
> `cross_track_evidence`. The error came from a session that could not read `~/.claude` and
> treated "I cannot see it" as "it does not exist."
>
> **The real exposure, unchanged:** that path is its only copy. It is in no repository, has
> no backup, and cannot be diffed, so a bad write or a lost disk takes all of it. The
> standing fix is to move the file into `cyborg-methodologies/voice-check/profiles/` and
> symlink it back — note the repo-root `.gitignore` rule `profiles/*` has a mid-pattern
> slash and so anchors to the repo root, where no `profiles/` directory exists; it does
> **not** cover `voice-check/profiles/`. Decide that deliberately rather than by accident.
>
> A 38-check reconstruction built by extraction from `Spelman/STYLE_REVIEW_v11.md` sits at
> `voice-check/profiles/june_bloch.json` marked `4.0-reconstructed`. **It is not a
> replacement** — it is missing 16 checks and every numeric block. Its one use is as a
> cross-check: its 38 instructions were lifted verbatim from a style review, so any
> divergence from the live profile's wording is evidence about which of the two drifted.

**The recurring failure this table prevents.** On the run that produced it, the editing instance read four of thirty-eight qualitative checks, then wrote a local standard that restated several of them worse and application-specifically. The duplicate then competed with the original. **Do not write prose principles into a local file. Point at the profile and make it binding.**

---

## 1. Scope tags — the reason "PASS" was meaningless

Checks do not all apply at the same grain. A flat pass/fail per item is how an item gets marked satisfied while being violated in four places. **Every check carries a scope, and verification reports findings at that scope.**

| Scope | Meaning | Verification output |
|---|---|---|
| `DOC` | Holds once for the whole document | A verdict plus the reasoning |
| `PARA` | Applies to every paragraph | A line per paragraph |
| `SENT` | Applies to every sentence | Every violating sentence, quoted |
| `INST` | Applies to every instance of a class — every named entity, every quotation, every demonstrative, every number | **An enumeration of the instances found and the status of each** |

`INST` is the one that has failed hardest. "Every named thing is defined at first use" is not a question with a yes/no answer; it is a list. The verifier must produce the list.

**Assigning scope:** when adding a check, ask *what is the unit at which this can go wrong?* If it can go wrong more than once in a document, it is not `DOC`.

---

## 1.5 Standing principles — how the author's applications should read

*Moved here from `Job Search/CLAUDE.md` on 2026-09-12. They are drafting method, and method
belongs with the standard that enforces it, not in the workspace map. They were the last
substantive block of method still living in the entrypoint file. Nothing was reworded in the
move — including the corrections each one carries.*

1. **Read primary sources directly.** Don't delegate synthesis to subagents when drafting. You need the material in your context to write with texture.
2. **Specificity is the constraint layer.** If it could describe any scholar, it fails.
3. **Orient, then demonstrate — the story lands the claim, it does not open the document.** The reader is told what they are holding and who June is first; the specific moment, the fieldwork scene, the tool-building discovery then *demonstrates* the claim rather than substituting for it.

   **Corrected 2026-08-16.** This principle previously read *"Story over system. Lead with the specific moment…"* — **the last uncorrected copy of an instruction June overturned in April 2026.** Her own margin note sits on the same line as the pattern in `WRITING_ANALYSIS.md:226-227`: *"topic sentence usually needs to be first. I had to do that edit a lot… Jumping into a story without a topic sentence is fine on occasion if the context calls for it."* That correction reached `Bloch_Application_Context.md` (mistake 9) and memory (`feedback_topic_sentences`) and never reached here — the file every agent reads first. She has since made the same edit **five separate times** across applications (`_application_evidence/CHECK_TRIAGE.md:129`, item A2), most recently reversing a draft plan that had licensed a story opening as a "sanctioned exception."

   **The diagnosis is placement, not abolition** — *"a story with nothing before it is a payoff with no setup"* (`printpress/genre_configs/academic_position.md:280`). The story keeps its full weight one paragraph later, under a claim.

   ⚠ **Two things not to attach to this rule.**
   - **Do not justify it with reader-skimming.** "Screeners spend N seconds," "the tired reviewer with a stack of 50" — every such figure in this workspace traces to no source and is marked **do not use, and do not let it justify any front-loading rule** (`Hypotheses_Academic.md:559-570`; `Hypotheses_Practitioner_Advisors.md:105-109`; `Discredited_Claims.md:112`). The rule stands on her own repeated revisions and on two committee-insider sources. Take the advice, leave the number.
   - **Do not generalize it to fellowships.** `Grants_Fellowships.md:194` is the one place in the evidence base where her story instinct is affirmatively supported, scoped to Wenner-Gren / SSRC / ACLS / NEH, on Lamont's panel ethnography — *write the person, not only the project.* A former ACLS program officer endorses a scene-setting opening for proposals, with a hard constraint: **rarely longer than one paragraph, and it must set up something the rest of the document actually addresses.** Fellowship personal statements are a different genre with a different move structure; porting the job-letter model onto them is porting the wrong model (`Genre_Move_Structure.md:174`).

   **Status: working hypothesis**, per `_application_evidence/EVIDENCE_BASE.md`. Supported by her revision record and by genre convention (orientation is the conventional opening move), not by outcome data. Tracks differ — tech/industry sources run actively against narrative in cover letters; academic is genuinely unresolved between two committee insiders and should be surfaced to June rather than defaulted.
4. **Anti-sycophancy is structural.** Push back on bad ideas, flag weak fit, tell June when a strategy won't work. She needs a collaborator who positions her to succeed, not an assistant who does whatever she asks.
5. **Low friction for June.** She reviews and approves; she shouldn't have to rewrite from scratch.
6. **Prior applications are the best training data.** Read what worked before. Adapt, don't reinvent.
7. **The critique and the engineering are the same move.** This is the through-line of everything June does. If your draft separates them, you've missed the point.
8. **Gateway words are doors, not rooms.** "Accessibility" leads to crip time and Mia Mingus. "Equity" leads to Omi & Winant. If a gateway word sits alone as the point, rewrite.
9. **Verify every factual claim BEFORE drafting, not after.** Dates, line counts, timelines, project descriptions — check against `Bloch_Application_Context.md` and `Bloch CV.docx`. Use `[DATA NEEDED]` tokens for anything you can't verify. Never invent plausible numbers.
10. **Output format matters.** Tech resumes use HTML. Academic materials use .docx with letterhead. Match the format of the closest prior application.
11. **Voice-check has three roles:** style guide (read the profile before drafting, write in June's voice from the start), contamination linter (silently fix agent artifacts after drafting), and learning loop (compare agent draft to June's final version after revision, update the profile). NEVER re-run voice-check to modify documents June has already edited. Her edits train the profile.
12. **Context is for strategic decisions, not exhaustive inclusion.** June's offered context (voice memos, source docs, session conversation) is background for judgment — not a checklist to cram into the draft. For each rhetorical move, identify what's load-bearing for *that move* given the medium, genre, and audience — drop the rest. Grant prose ≠ memoir ≠ chapter writing. When uncertain what's load-bearing, ASK. Including-to-be-safe is the failure mode.
13. **Context before claim. Specificity before theory. Theory as scaffolding, not name-drop.** Claims must be earned by what precedes them: (a) orient the reader before making the analytical move — set context before the analysis lands; (b) ground theoretical claims in specific ethnographic/empirical detail; (c) apply scholars' arguments to the specific case, don't parenthetically cite to signal engagement; (d) no new concepts in conclusions; (e) mine prior version language before retranslating — if a prior phrasing was sharper, use it; (f) distinguish June's moves from "the field" — sycophancy by displacement dilutes her contribution.

14. **Surface fit ≠ real fit — read the role before ranking it.** A title, org, keyword match, or match_score identifies a *candidate*, not a fit. Before presenting any role as a fit or in a ranked tier — scraper, LinkedIn, or anywhere — read what the role actually involves: who the learner/audience is, the day-to-day, the real requirements. Unread roles are shown as *unread candidates*, never as verified fits. (Extends "verify liveness before recommending" → "verify the role is actually the job." Both sources carry `fit_basis = content|surface`; scraper and LinkedIn are two sources of one integrated dataset, so the rule is defined once and applies to both. See memory `feedback_surface_vs_content_fit`; full spec in `LINKEDIN_FRAMEWORK_HANDOFF.md` §9.)

---

## 2. The generalizable checks — process, not prose

Prose checks live in the voice-check profile. These are the ones that profile does not carry.

### Accuracy

**ACC-1 · `INST` · Never invent a detail.** Every concrete claim traces to a source document or is computable from one. Where a fact is wanted and absent, write `[NEED: description]` and leave the gap visible. **Generalization from one run:** fabrication is likeliest exactly where a posting duty has no matching evidence — the slot demands a claim and generating one is the locally optimal move. Audit the gaps before drafting.

**ACC-2 · `DOC` · Source-documented is not author-verified.** A claim quoted from the author's own prior writing can still be wrong or imprecise. Facts that are load-bearing, unusual, or specific get confirmed with the author before shipping.

**ACC-3 · `INST` · A fact inventory must carry a NOT-AVAILABLE section** listing what an agent will reach for and cannot support, including any fabrication that has already occurred, with its correction.

*Given teeth 2026-08-16, from the FAMSF run — where this check's absence started a four-link failure chain.* No `FACT_INVENTORY.md` was produced. The role's operational/administrative duties (~60% of the JD) therefore had no evidence behind them and nothing said so. The slot got filled with the job description in future tense; the review swarm's two most senior readers **independently** named it *the deciding question*; the next agent deleted the paragraph rather than supplying evidence; the letter shipped with the deciding question unanswered.

**Two additions:**

1. **The inventory is a gate, not an artifact.** Drafting does not begin without one. An author-supplied facts file is an *input* to the inventory, not a substitute for it — `FACTS_FROM_JUNE.md` existed and covered four topics; the inventory would have covered the posting.
2. **The NOT-AVAILABLE list is an input to assembly, not a note at the bottom.** *From the PlayLab analysis:* nine of fifteen specifics the author restored were already in that application's inventory, one flagged in the file itself as *"neither has appeared in any draft."* The list did its job and nobody read the output. Every NOT-AVAILABLE row is either served by the draft, routed to the author as a `[NEED:]`, or recorded as a deliberate exclusion under `PRO-7`. **A row with none of those three dispositions blocks the draft.**

**ACC-4 · `INST` · Do not upgrade a claim's specificity.** Narrowing "at the intersections of race and gender" into two named groups, or fusing two unlike engagements into one longer tenure, are the same error as inventing: the source did not say it.

**ACC-5 · `INST` · Has the author already used, taught with, cited, or built on anything this employer makes or publishes?** *From PlayLab, applied 2026-08-16.* A fact-inventory row, asked at Stage 0. Her words: *"I am moreover drawn to Playlab because I already use your tools in my own teaching. I use a colleague's tool to ensure CVC-OEI compliance and built my own Playlab chatbot, refRAME."* No agent draft in any application has ever contained a prior-adoption claim, and nothing in the workspace asked for one. Interest evidenced by prior adoption, not asserted.

**ACC-6 · `INST` · The inventory carries a row for work in progress, and a row for what the author's systems do at scale.** *From Spelman/PlayLab, applied 2026-08-16.* The inventory records what she *built* and what she *did*; both retrieval gaps fell in the two holes it has no slot for. Examples: *"which I am writing up for publication in* Race Ethnicity and Education" (the journal appears nowhere in the workspace before her rewrite); the overnight class-wide analytics; academic dishonesty tracked as collective burnout signals.

### Argument

**ARG-1 · `SENT` · Nothing appears without its relevance clear where the reader meets it.** No exemption for short sentences or closing paragraphs — those only *feel* exempt because they resemble a convention.

**ARG-2 · `PARA` · Every paragraph carries exactly one stated proposition** from the propositions list. Prose carrying none is cut. An "arc" or a list of "section beats" is not an argument; only claims that could be false are.

**ARG-3 · `SENT` · Never state what the posting says as if it were your claim.** A sentence whose content restates the job ad occupies a slot without making a move.

*Extended 2026-08-16, from FAMSF.* The failure has a **tell and a cause**, and both are checkable.

**The tell:** future-tense duty language with no instance attached. *"research files built item by item, consultation meetings scheduled and hosted for tribal delegations, records kept in a form the next person can pick up cleanly, and the resulting inventories and summaries reported to the… database on schedule."* That is the JD with the applicant's name implied. It reads as competence and contains no evidence.

**The cause:** a posting duty for which the inventory holds nothing. The slot demands a claim and generating one from the JD is the locally optimal move — the same mechanism `ACC-1` names for fabrication, one step milder.

**The rule:** a duty with no evidence behind it gets a NOT-AVAILABLE row (`ACC-3`) and then one of three honest outcomes — the author supplies evidence, the duty is served by adjacent evidence that is named as adjacent, or it is deliberately excluded under `PRO-7`. **Restating the duty is never one of them.** When a reviewer says "I don't see evidence they can do X," deleting the sentence about X does not answer it.

**ARG-4 · `INST` · Every named entity is defined by what it does, at first use — and the gloss is chosen for *this* reader.** Titles are labels, not descriptions. If the gloss will not fit the budget, cut the name.

*Amended 2026-08-12 (applied 2026-08-16). The single highest-value change from the Spelman/PlayLab analysis.* The `INST` enumeration gains a second column: **the gloss, and the reader it was written for.** A gloss carried verbatim from another application is a `[NEED:]`, not a pass.

Why this one first: it is a *misdirected* check, not a missing one. The field was filled, the list was produced, and the check passed while the sentence was aimed at the wrong reader — and a check that passes is worse than one that is absent, because it certifies the defect. The same organization, two audiences, in the author's own words:

> **Spelman (HBCU, higher ed):** "iChange Collaborative, an Atlanta-based DEI firm that works with educational institutions, nonprofits, and corporate clients."
> **PlayLab (K-12 lab schools):** "iChange Collaborative since 2016, a transformative leadership firm founded by middle school teachers and serving schools, nonprofits, and corporate clients."

The agent copied the first into the second application verbatim — a 1.00 string match, "Atlanta-based DEI firm," into an application about middle schools. The test already exists in the voice profile (`situational_specificity` #50: *could this sentence appear in a letter to a different organization?*). **The half an agent cannot answer — what this reader needs to know about the entity — is routed to the author as a `[NEED:]`.** She answers it in one line.

**ARG-4a · `INST` · The author's own named artifacts get named.** *From PlayLab.* The agent wrote "I built an app on Playlab" running "a critical-theory method engine"; she wrote "built my own Playlab chatbot, refRAME." An agent that will name a journal and an institution will still decline to name the author's own tool. Enumerate her artifacts the same way as any other entity.

**ARG-5 · `INST` · Quoted evidence arrives with the pattern it illustrates.** A quotation is never self-explaining.

**ARG-6 · `INST` · No demonstrative reaching back more than one paragraph.** "This audit," "that decision," "the finding" all break silently when blocks are reordered.

**ARG-7 · `DOC` · Identity claim first, story lands it.** The letter establishes who the applicant is and why that fits, and the specific instance demonstrates it. The inverse — one instance foregrounded, identity hoped for — is a recurring failure.

### Audience

**AUD-1 · `DOC` · Anchor to the actual employer type, not the genre's default bucket.** A single application genre spans tech industry, EdTech, nonprofit, and mission-driven higher ed; those are different readers with different registers.

**AUD-2 · `SENT` · Vocabulary from the applicant's field is glossed or cut.** Includes metric and evaluation language that assumes the reader knows whose metrics they are.

**AUD-3 · `DOC` · Do not restate the employer's own published values to them.**

**AUD-4 · `DOC` · Do not assume the employer's community agrees internally** about the thing being applied for.

**AUD-5 · `DOC` · Every duty in the posting is substantively served, and the letter must not read as arguing for a different job.**

*Corrected 2026-08-11.* This item previously read "serve the duties in proportion to their emphasis," operationalized as *the largest duty must be the largest cluster*. **That stricter form was an editing instance's invention, not the author's instruction** — and it cost four rounds of assembly work against a target nobody had set. The critique it came from was that a draft argued for a role the employer was not filling; that draft had the largest duty at 16% with no concrete instances. The defect was **absence and irrelevance, not ratio.**

**What to check:** does each duty cluster have at least one concrete, specific instance? Would a reader finish thinking the applicant is applying for this job rather than an adjacent one? A distinguishing strength may legitimately occupy the most space — that is what makes the letter competitive — provided nothing the posting asks for is missing or gestured at.

**The general lesson, which is the more valuable one:** an editing instance will invent a stricter, more measurable version of a soft instruction, because a number is easier to check than a judgment. Then it enforces the number. **Record what the author actually said, and mark any operationalization as the instance's own.** See also PRO-6.

**AUD-6 · `INST` · When the application asks a literal question, enumerate how the text answers it — the question as written, not the question the genre usually implies.**

*Added 2026-08-12, from the PlayLab run.* This standard grew up around cover letters, where the question is implicit and always the same: *why should we hire you.* An application **form** often asks something else in so many words, and nothing here ever checked whether the submitted text answered it. The PlayLab field was labeled **"Why are you interested in this position?"** with the sub-instruction *"Please provide details about your experience or expertise that would make you a great fit."* The draft answered why to hire her. Defensible given the sub-instruction, and no pass flagged it, because no pass was looking.

**What to check — this is `INST` scope, so produce a list, not a verdict.** Quote the field's label and sub-instruction verbatim. Then one row per paragraph: does it answer the label, the sub-instruction, both, or neither? "Neither" is not automatically a defect; a paragraph with no row at all is.

**The two-sided case, which is the common one.** June's observation, 2026-08-11: *why should you interview me* and *why am I interested* are two sides of one claim, and a form that carries both a label and a sub-instruction is asking for both. **Do not pick one.** An answer that argues only fit reads as a pitch; one that argues only interest reads as a fan letter. The fit claim should be earned through what the applicant is drawn to. Where interest appears only at the open and close, say so — that is usually enough to hold the frame, but it is a finding, not a pass.

⚠ **Applies to the form actually being submitted.** Two postings on the same team can carry different forms with different questions. Capture the real one before drafting; see the sibling-posting failure recorded in `AUTHOR_REVISION_SPEC.md`.

**AUD-6a · `INST` · When a form carries more than one free-text field, decide what each field carries — before drafting.** *Proposed 2026-08-12, applied 2026-08-16.*

One row per **field** (not per paragraph) naming what that field will carry and why, produced before any prose exists. The per-paragraph enumeration in `AUD-6` then runs inside each field.

**The observation this comes from, and its limits.** On PlayLab she moved three paragraphs bodily from the required field to the optional one. Read as a compression decision it produces the wrong lesson entirely — *measured*, her total submitted text moved **−2.5%**. She did not cut. She **reallocated**: the required field carried claims tied to the role, the optional field carried self-contained evidence that needed no tie. A reader who stops at the required field still gets the argument.

**This is recorded as an observation, not a target, and no proportion is proposed.** The per-field split was set by the material. She has said the division was specific to that application and not yet generalizable. What generalizes is only that **the allocation is decided deliberately and written down before drafting** — because an agent that has not decided it will pour everything into the required field and treat the optional one as overflow.

**AUD-5a · `DOC` · Proportion is set in the propositions, not in the prose. Check it there.**
*Observed failure, 2026-08-10.* An assembler raised duty proportion as unfixable three rounds running and was correct. Four of seven propositions served governance; one served training and support — which the posting names as its largest duty. Because every paragraph carries exactly one proposition, the plan mechanically produced a 66%-governance letter, and no assembly-layer editing could move it. The assembler's only remaining lever was relabeling paragraphs to shift the count on paper, which it rightly refused as "arithmetic, not a letter that serves the duty better."

**The rule:** proposition count per duty determines paragraph count per duty determines word count per duty. **Before drafting, count the propositions against the posting's duty clusters.** If the heaviest duty has the fewest propositions, the plan is already wrong and the letter cannot recover.

**The two fixes, in order of preference:** split the under-served duty into more than one proposition — usually it genuinely contains more than one claim — or consolidate over-served ones where two propositions are really one argument. Do not fix it by cutting evidence the author asked for.

**Corollary for escalations:** when a subordinate agent raises the same unfixable item across multiple rounds, that is a signal the defect is upstream of where it is being asked to work. Fix the upstream artifact rather than dispatching the item again.

**AUD-7 · `DOC` · Service verbs.** If nobody but the applicant does anything in the letter, the grammar is wrong for a role defined by assisting, coordinating, and supporting.

*Renumbered 2026-08-16 — this was a second `AUD-6`, colliding with the literal-question check above. Two different checks under one ID is how one of them goes unread.*

*Confirmed twice since, and the repair is the same both times: **named events, not named institutions.*** PlayLab: the agent's draft had nobody but the applicant acting; she added participatory design and partners *"leveraging participants' knowledge about their own institutional contexts that exceed that of any outside Playlab employee."* FAMSF: the agent's outreach paragraph was **one sentence, four institution names, zero events**; hers was a full paragraph with five named events, tribal partners as actors — a colloquia series negotiated into a contract, a Heritage Month keynote, Muscogee Nation preservation officials hosted in her classroom, a conference co-organized, a student panel moderated. **An institution list is not outreach evidence. The event is the evidence.**

**AUD-10 · `INST` · Posted requirements are not one kind of thing. Classify them before deciding what the letter must serve.** *New 2026-08-16, at the author's prompting and then narrowed by what her files actually support.*

*Her framing:* **"the cover letter doesn't need to demonstrate that I meet every single job requirement… the 'requirements' are often more a wish list than hard requirements… some requirements are far more essential than others, and we can think about what the job is truly about at its core as a way of getting at that."**

The instinct is right and the general form of it is dangerous. **Three different things get printed under one heading**, and the response to each is different:

| Kind | How to tell | Response |
|---|---|---|
| **Statutory gate** | A legal or policy eligibility rule, verified before any human reads the file | **No writing crosses it.** Do not spend words; establish eligibility or do not apply |
| **Scored rubric criterion** | The posting names "must-haves," or the employer's process writes screening criteria before applications are read | Serve it explicitly and map to it. Material not mapping to a named must-have is overhead |
| **Wish-list preference** | A long undifferentiated list, "preferred," or criteria with no visible scoring | Weight by centrality to what the job is actually for. A gap here is not burning |

**Which kind you are looking at is a per-posting question, answerable from the posting** — not a statistic to look up, and not a disposition to apply uniformly.

**The counter-example that keeps this honest, and it is from her own record.** California community college minimum qualifications are a statutory gate: HR verifies transcripts against listed degrees before any faculty member reads the file, and "makes no attempt to judge if the experience is appropriate." Her anthropology PhD clears the **Anthropology** MQ outright and does **not** clear Ethnic Studies, Religious Studies, or Women's Studies, which require a board-granted equivalency that is **not portable between districts.** Applications filed to those lines without an equivalency request were eliminated before anyone read them. *Already tracked* — `Applications_Tracker.md` rows 8–9 and the 2026-08-10 entry; `agent_briefs/READING_LIST_academic_position.md`. **A general "requirements are a wish list" disposition would have produced exactly those applications.**

Worth naming plainly, since it shapes who can teach the field: the discipline whose subject is racial formation has a credentialing rule that excludes scholars trained in adjacent disciplines, and at some districts equivalency requests were reported as *always denied*. That is a structural gate, not a paperwork step, and it is the kind of thing a cover letter cannot argue with.

⚠ **Do not cite the "women apply only at 100% of qualifications, men at 60%" claim.** June raised it as half-remembered. **A full search of `_application_evidence/` found it nowhere** — not the claim, not the Hewlett-Packard attribution, not *Lean In*. Its structure matches the pattern `Discredited_Claims.md` documents (unsourceable internal report laundered through a popular book), but **her files do not establish that either way, so it must not be written into a rule in either direction.** The gender material her files *do* hold is about discrimination by readers (Park & Oh 2025; Correll et al. 2007; Johnson & Kirk 2020; Dutt et al. 2016), not applicant self-selection — a different variable and a different literature.

**What is supported:** Fuller, Raman, Sage-Gavin & Hines, *Hidden Workers: Untapped Talent* (Harvard Business School / Accenture, **September 2021**; 8,000+ workers, 2,250+ executives) — **88% of employers agree that qualified high-skills candidates are screened out because they do not match the exact criteria in the job description.** ⚠ Status per `Discredited_Claims.md` Claim 2: **DISTORTED in circulation**, executive *opinion* survey, and the canonical HBS PDF **404s**. The honest one-line version: *employers overwhelmingly believe their own hiring criteria screen out people who could do the job* — which locates the problem in the job description, not in the applicant.

**AUD-9 · `INST` · Name the thinnest duty at Stage 0 — the posted duty with the least evidence behind it.** *New 2026-08-16, at the author's prompting.*

*Her question, which is the right one:* **"that probably generalizes and depends on different roles, right? For this app, it was operational. For the next, it might be something else. So maybe what we need is a protocol for those things?"**

Yes. "Operational register" was FAMSF's accident. **The pattern is that every posting has one duty cluster where her evidence is thinnest, and that cluster is what generates the deciding flag** — for a curatorial role it was administration; for a research role it might be management; for a management role, technical depth. Waiting to discover it at Stage 3, from reviewers, is waiting until it is expensive: by then the draft is built around the strong duties and the only remaining move is to delete the paragraph that made the gap visible.

**The protocol — runs at Stage 0, immediately after `ACC-3`:**

1. **Cluster the posting's duties** and map each to the evidence the inventory actually holds. This is `INST` scope: produce the table, not a verdict.
2. **Rank by evidence density.** The bottom row is the thinnest duty. Name it out loud, in the plan.
3. **Choose a response before drafting**, from four — and only four:
   - **Evidence exists and wasn't found** → find it. Most of her record is on her drive and in her CV; a retrieval gap is not a real gap.
   - **Evidence exists offline** → one plain `[NEED:]` to her.
   - **Evidence exists but she may not recognize it as evidence** → **propose the transferable reading before accepting "no."** *Her instruction, 2026-08-16:* **"sometimes i dont realize how my own experience translates. There have been cases where I've actually learned about that and how to do it from working with agents' drafts, because as an autistic person, I tend to take things super literally and can sometimes miss the bigger picture, where it's something like, no, this is a transferrable skill."** So a bare *"do you have experience with X?"* is the wrong question — it invites a literal reading of X and gets a literal no. Ask it with a candidate bridge attached: *"the posting asks for X; you did Y at Z — does that count as X, or is it a different thing?"* **Her "no" is only informative once the bridge has been offered.** This is the one place in the protocol where an agent's outside view is worth more than the author's, and it must not be skipped for politeness.
   - **Adjacent evidence covers it** → use it, and **name it as adjacent.** Adjacent evidence presented as direct is `ACC-4`.
   - **No evidence exists** → this is hers to decide (`PRO-9`'s consult rule), between serving it thinly, excluding it under `PRO-7`, or dissolving the condition.
4. **Open its `FLAGS.md` row at Stage 0**, pre-populated. Then a Stage 3 reviewer converging on it is a **confirmation of a known gap**, not a discovery — and cannot be closed by deletion, because the row already exists and names the duty.

**Why this ordering is the whole point.** The thinnest duty is knowable from the posting and the inventory before a word is drafted. FAMSF's was: the JD's administrative duties were ~60% of the role and the workspace held nothing for them. Every downstream failure in that run followed from nobody having said so at Stage 0.

**AUD-8 · `DOC` · A plan may not license an exception to the author's own documented rules.** *New 2026-08-16, from FAMSF.*

`DRAFT_PLAN.md` opened with *"Lead with the Okeeheepkee/copper-plate story, not a summary paragraph,"* and named it *"the sanctioned exception"* to her topic-sentence-first rule. She reversed it: her version opens with a conventional application statement and a credential block, and the story arrives in ¶2 **under a topic sentence** — which is `feedback_topic_sentences` operating exactly as written.

The plan had invented an exception to a standing rule and licensed it in the plan's own voice, where no reviewer treats it as a violation because the plan says it is intended. **A planning artifact can allocate, sequence, and select. It cannot suspend a rule the author wrote.** If a plan believes an exception is warranted, that is a `[NEED:]` for the author, not a decision the plan may make.

*See also `AUD-5`'s note on invented stricter targets and `PRO-6`: this is the same mechanism pointed the other way — an instance relaxing a soft rule instead of tightening one, both without authority.*

### Process

**PRO-1 · `DOC` · Never instruct an agent to "write a cover letter."** That phrase invokes the genre's statistical center. Instruct: *explain, in writing, to this hiring team, why they should interview this person.*

**PRO-2 · `DOC` · Capture long, then cut** — and the rationale matters, because it determines whether the capture is real. **Agents write mediocre punchy prose and edit well, like human writers.** The leverage is in the cutting pass, so the capture exists to give the cut something to select from. The failure mode is padding: the same content at greater length. **Test — did anything good get cut?** A capture with no casualties was never over-supplying.

**PRO-3 · `DOC` · Edit by targeted replacement; never rewrite a file wholesale.** Regeneration silently loses good sentences and is the observed cause of drafts getting worse across rounds.

**PRO-3a · `DOC` · Enforce PRO-3 mechanically. This is a command, not a principle.**
```
python3 "Job Search/_tools/check_rewrite_fidelity.py" --before OLD.md --after NEW.md --strict
#   --expect-cut     compression is the declared task for this transition
#   --author-edit    the "after" file is the author's own revision
```
Reports length delta and the percentage of word tokens changed, and **fails if the text collapses, or if a number or citation present before is absent after.** Run it on every version transition.

*Amended 2026-08-16 — the guard passed the worst transition in the FAMSF run.* Measured across that run: the collapse from 789 to 310 words scored **68.1% changed and printed "clean"** (threshold 70), while the author restoring her own material scored **84.5% and drew a Major**. **The tool passed the agent and flagged the author** — the same shape as the Vale finding in `PRO-8` below.

The cause was structural, not a bad threshold: the footprint metric measures *which* words changed, not *how many survived*, and was calibrated on a medical de-AI skill where length is roughly constant. **Deletion was invisible to it.** Lowering `--warn-pct` would not have caught this and would have begun failing legitimate rewrites. A `LENGTH_COLLAPSE` verdict was added instead, Major above 25% removed, and `--author-edit` stops the number-drift invariant firing on the author. Verified against all six FAMSF transitions: the collapse now exits 1 under `--strict`; her edits exit 0.

**The two flags are declarations, and an undeclared cut is the finding.** If an agent needs `--expect-cut` to get a clean result on a transition briefed as a repair, the brief and the work have come apart.

*Reading the number:* a targeted repair lands low — the v11→v12 prose repair measured **23% changed, numbers preserved, clean**. A wholesale regeneration lands at 80–90% and means PRO-3 was violated whatever the agent reported. **A high footprint on a task briefed as a repair is a failed task**, regardless of whether the output reads well.

*Provenance:* `check_rewrite_fidelity.py` and `check_sentence_variety.py` are taken from `Aperivue/medsci-skills` (MIT, https://github.com/Aperivue/medsci-skills) and copied to `Job Search/_tools/`. **Do not install that skill collection** — 59 medical-writing skills would collide with `/printpress` and `/voice-check` for no gain. These two scripts are stdlib-only, genre-neutral, and run standalone. Its footprint threshold is advisory by its own docstring; set your own once a few runs exist.

*What this closes:* "we were getting closer and then lost it," material disappearing between versions, and numbers drifting — all previously catchable only by the author reading a diff.

**PRO-4 · `INST` · Author inclusion requests outrank cut-rather-than-bungle.** If the author asked for something to appear, make budget for it. Record the request in the application context file — anything held only in an instance's memory does not survive the handoff to an agent.

**PRO-5 · `DOC` · Protect material multiple independent readers named as a loss** — but **verify the characterization with the author before protecting it.** Reader enthusiasm is evidence that a line *lands*, never evidence that it is *true as read*.

*Observed failure, 2026-08-11.* Three independent readers each named "I do not read the chatbot transcripts" their single biggest loss, reading it as restraint — a capability the applicant declined. It survived four rounds as protected material on that basis. The author then said she is not sure she can access those transcripts at all, and does not see why the line is strong. The source page says only *"I don't see the chat transcripts."* If the platform does not surface them, there was no choice to decline, and the sentence readers loved was an overclaim they had constructed from an ambiguous artifact.

**The mechanism:** readers reward the most flattering available reading of an ambiguous fact, and protection status then makes that reading harder to dislodge than an ordinary sentence. **Any line multiple readers single out for praise gets an author check before it becomes protected**, precisely because praise is what stops it being questioned.

**PRO-6 · `DOC` · Length is a real target, and an invented tighter target is worse than none.** Record what the author actually said, not a stricter version.

*Measured 2026-08-16, replacing a guess.* The genre configs carried **600–800 words** for a one-page cover letter. That target was never checked against the template it has to fit, and it does not fit: `letter_template.html`, rendered through WeasyPrint at her prose's actual mean word length (6.07 characters) across five paragraphs, **holds up to ~525 words. 530 breaks to page two.**

**Working target ~500; ceiling ~525 at five paragraphs.** *Caveats, stated because this number will get reused:* WeasyPrint's font metrics are not identical to Chrome's Save-as-PDF; more paragraphs means more inter-paragraph space and a lower ceiling; Chrome headless could not be used as a cross-check because the empty template paginates to two pages under it. **Re-measure if the template changes** — the method is in `REVISION_ANALYSIS_2026-08-16_FAMSF.md` §6.

The 600–800 figure is how the FAMSF letter reached the author 300 words over what could fit, forcing a compression pass she described as brutal. **A budget that the output format cannot hold is not a budget; it is a deferred cut, and it lands on the author.**

**PRO-7 · `DOC` · Excellence in what is included beats coverage of everything. Exclusion is a decision, not a failure.**
*June, 2026-08-11:* "It's better that what is in the letter is excellent than that we cover every item badly… Getting to 400 will mean making hard choices about what the audience needs to know and why."

**This governs AUD-5 when the two conflict.** AUD-5 asks that every duty be substantively served; a one-page budget may make that impossible. When it does, **serve fewer things well rather than all of them thinly** — and note that thin coverage is worse than absence, because a gestural sentence spends words while telling the reader nothing and signalling that the applicant had nothing better.

*The operative question at a tight budget is not "what can we fit" but "what does this reader need to know, and why."* A single sentence that does its work is not a compromise — if the design setup is one good sentence that lands, that is the correct size for it.

**Requirement:** deliberate exclusions get recorded — what was dropped and the reason — so a later reviewer reads the gap as a choice rather than an oversight, and so the author can overrule a specific call rather than re-litigating the whole cut.

---

### The compliance checks — added 2026-08-16

*These five exist because the standard's largest observed failure is not coverage. Across three applications the biggest bucket was **a check existed and the draft violated it** (34%), and the second was a check that fired and nobody acted on it. Adding rules does not fix that. These are about landing.*

**PRO-8 · `INST` · A lint hit on text the author wrote is a rule defect until shown otherwise.** *Proposed 2026-08-12, applied 2026-08-16.*

Her finished, shipped rewrites draw error-level Vale alerts on `facilitated` (her own word — five occurrences in her CV), `transformative`, and `leveraging`, plus a "product descriptions" flag on the iChange gloss. **An agent that ran the linter obediently would have deleted her best sentence and replaced her own verb.** Enumerate every alert whose span the author wrote; each is a rule-file candidate, not a prose fix. **No agent silently applies a lint suggestion to author-written text.**

The general form matters more than the instances: *the tools in this workspace are calibrated against agent output, and the author is the out-of-distribution case.* Two independent tools have now been caught flagging her and passing the agent — Vale here, `check_rewrite_fidelity.py` in `PRO-3a`. Assume the next one does too.

**PRO-9 · `INST` · Every review flag carries a disposition, and nothing advances with a blank one.** *New 2026-08-16, from FAMSF — the single most consequential process gap found.*

The FAMSF swarm raised five convergent flags (two or more independent reviewers each). Two were properly fixed. One was resolved by the author deleting a word. One was "fixed" by deleting 60% of the letter. **And the one that two reviewers independently called *the deciding question* — no evidence the applicant can do the operational half of the job — was never addressed by anyone, in any version.**

The cause is that `LEARNING_LOG.md` is a *transcript*. It records what reviewers said. **There is no artifact where a flag is marked handled, and therefore no way to tell a finding that was dealt with from one that was merely written down.**

**The rule:** every flag — swarm, check violation, or `[NEED:]` — becomes a row in `[AppFolder]/FLAGS.md` with one of four dispositions:

| Disposition | Means |
|---|---|
| `FIXED` | with the version it landed in |
| `DISSOLVED` | the condition that generated the flag was removed, so the question no longer arises. See the test below — this is legitimate and easy to abuse |
| `REJECTED` | with the reason. A rejected flag is data about the *check*, not a dismissal |
| `AUTHOR` | routed to her, with the question stated in one line |
| `EXCLUDED` | deliberate, under `PRO-7`, with the reason |

**A draft does not reach the author with an undisposed row.**

#### `DISSOLVED` — and the test that separates it from hiding the problem

*Added 2026-08-16 at the author's correction. The first version of this check said flatly "deletion is not a disposition," and that was wrong.* Her words:

> "one way to avoid 'open question' responses is in fact to cut it — readers don't know what got cut. I don't know if cutting it is the right call or not, but sometimes the way to answer a critic's feedback isn't to answer it directly, but to figure out what the underlying conditions are that lead to that feedback popping up, and addressing that."

She is right, and this is a stronger move than answering: a reviewer's flag is evidence about a *condition*, and the condition is often upstream of the sentence that triggered it. Removing it is a real repair, and the reader never sees what was not there.

**The test — where does the flag's condition live?**

- **In the document** → cutting genuinely dissolves it. A theory paragraph that raises a question the letter cannot answer; a claim that invites scrutiny it cannot survive; a tangent that makes a reader wonder about something irrelevant. Cut the paragraph and the question does not exist. **`DISSOLVED` is correct, and is often better than a defensive sentence.**
- **In the posting, or in the reader's brief** → cutting hides the sentence and leaves the gap. The reviewer was not reacting to your prose; they were reacting to an absence measured against what the job asks for. **Deleting the sentence does not delete the requirement, and `DISSOLVED` is a false record here.**

**The FAMSF case is the second kind, which is how the distinction was found.** Two reviewers independently reported no evidence the applicant could do the role's operational half — roughly 60% of the posted duties. An agent deleted the paragraph. Nothing about the posting changed; the letter simply stopped mentioning the largest part of the job. Had the flag been *"this operations paragraph overclaims"*, cutting would have been the right answer.

**Recording it:** a `DISSOLVED` row names the condition removed and why it was upstream of the flag. "Cut it" alone is a blank row wearing a disposition.

#### When a flag is a moment to ask her

*Author, 2026-08-16, on the FAMSF gap:* **"it might even be a point where it would have been appropriate to consult with me (which may have happened and I didn't have spoons)."**

**Route to `AUTHOR` rather than deciding alone when all three hold:** the flag is convergent (2+ independent reviewers), it concerns a duty the posting weights heavily, and no evidence for it exists in the inventory. That combination is a judgment about how to present a genuine gap — hers, not an agent's.

**And route it as one plain question with options, not as a research problem.** Her capacity varies and an unanswered question must not block the draft: if she does not answer, the flag stays `AUTHOR` and open, is surfaced again at Stage 5, and **the draft ships with the gap named in `FLAGS.md`** rather than silently closed by an agent's guess.

**PRO-10 · `DOC` · An analysis that proposes amendments applies them. The document records what changed.** *New 2026-08-16.*

`REVISION_ANALYSIS_2026-08-12.md` is 316 lines of good work ending in nine specific amendments, each naming its target file and scope tag, ordered by value. **Zero were made.** The next application ran on the unchanged standard four days later and reproduced three of the same defects. The analysis became a fifth document in a folder of documents.

**The output of a revision analysis is a diff to the named files.** The document records what was applied, what was refused and why, and what needs the author — in that order. An amendment that is proposed but not applied is recorded as `AUTHOR` under `PRO-9`, not left in prose where it reads as done.

*This is the same failure as `PRO-9` one level up, and as the compression stage one level down: capture happens, landing doesn't.*

**PRO-11 · `DOC` · The author sees the assembly before the cut.** *New 2026-08-16, from FAMSF and PlayLab.*

FAMSF, measured: the agent captured 1,025 words, cut to 310 against its own plan's 600–800 target, and the author's first contact with the letter was at 377 words — **after every cut had been made.** She rebuilt to 819, restoring material that had been present in the agent's own v0 and deleted by its own compression pass: the NSF / Wenner-Gren / American Philosophical Society funding, "seven states," the site count, the exhibition catalog. Her note at the foot of that draft: *">> June: This doesn't meet the rules we outlined for drafts to adhere to."*

**The cut is where the value dies, and it is the only stage with no author in it.** Her own account of why her cutting pass hurt: *"I had to cut a lot of really strong information that I otherwise would have liked to keep. So just because I cut something, that shouldn't mean it was bad."*

**The sequence, stated as proportions of the final target `T` so it carries across genres** — `T` is whatever the format actually holds or the funder actually allows (one-page letter, academic letter, form field, grant section):

| Stage | Size | Who acts |
|---|---|---|
| Capture | **~1.6 × T** | Agent assembles long — selection from abundance, not compression under scarcity |
| Post-marking selection | **record actual size; ~1.2 × T is provisional** | Route is chosen and logged: AI-proposed reversible cut, author-led selection with local AI compression, or hybrid |
| **Author receives an inspectable handoff, if one is made** | | **She edits: cuts *and adds*. In practice she adds** |
| Final | **T** | Fits the format |

**~1.2 × T is a proposed handoff point, not a target or a settled assignment of cutting authority.** Her instruction, 2026-08-16: *"I think we assemble at 800, and then have agents cut down… I think if I saw something at 600, that would be good. Or even 500 — because in practice, I also **add**."* Her later clarification is equally governing: it is not yet known whether AI can cut to a sufficiently high-quality draft, or where the balance between author selection and AI compression lies. An agent that delivers exactly `T` has spent her working room; an agent that forces ~1.2 × T despite losing the argument has mistaken an experiment for a rule. Preserve the assembly, make every proposed cut reversible, and record the route and outcome.

**For a one-page non-academic cover letter** (`T` ≈ 500, measured — see `PRO-6`): capture around 800; after her marks, test whether an inspectable handoff around 600 helps; she works toward the measured format limit. The 600 handoff is the experiment, not the standard.

⚠ **Both the 1.2 figure and the ownership/depth of the cut are experiments, not findings.** Her words: *"Lets try 600 first, and see how that goes — it'll be easier to adjust going forward."* Record the assembly size, selected route, handoff size, restored material, rejected cuts, author additions, and shipped size on the next applications. Do not harden a ratio or an AI-cutting route before it has data — see `PRO-6` and `AUD-5` on invented targets.

**The author's visibility before selection is the point of the sequence.** In a single-document case, she normally marks keep/drop on the ~1.6 × T assembly before the cut—marking, not prose-editing, because low friction is what makes participation possible. That gives the cutting stage selection information it would otherwise invent and stops the cut happening behind her.

**Scale correction — SJSU multi-document packet, 2026-08-24.** A four-document assembly reached 11,406 words. The author saw the complete packet and immediately identified the problem, so the visibility requirement worked. But granular KEEP/DROP marking had itself become a packet-scale cutting assignment: *“This is way too much content for me to be effective at cutting by hand.”* She explicitly asked the system to compare the competing treatments, retain the strongest formulation wherever it appeared, and orchestrate the merge.

This distinguishes two requirements that the first version conflated:

1. **The author sees the complete assembly and can redirect the selection process before material disappears.** Load-bearing; unchanged.
2. **The author marks every block before any proposed handoff exists.** Useful participation route, but not universal at multi-document scale.

After seeing the assembly, the author may explicitly choose a reversible proposition-level merge instead of granular marking. In that route:

- unmarked blocks remain `UNSURE`; they are never recorded as author `DROP` decisions;
- the assemblies stay unchanged;
- the system allocates each proposition or evidentiary scene to one owning document, then selects the strongest treatment regardless of where it first appeared;
- the handoffs are proposals, not finals;
- required outputs are a cross-document ownership/redundancy map, source notes, a standing-inclusion audit, and a named list of genuine losses;
- the author performs an intent-check read on the manageable handoffs and can restore any assembly material.

**Status:** working hypothesis from one live multi-document case. It corrects an observed usability failure without weakening the author-before-selection principle. Do not generalize it into permission to skip visibility, and do not let an agent infer authorization merely from packet size.

**Corollary for revision analysis:** a cut the author made under a length constraint is **not evidence the material was weak.** Derive nothing from a compression pass except facts about the budget. Her first pass — the one where she changes the prose — is the quality signal; her second is length surgery.

**PRO-14 · `DOC` · The author's revisions are the ground truth for her *voice* and not automatically for her *strategy*. Some tendencies are for counteracting, and she names which.** *New 2026-08-16, at her instruction.*

**The structural problem, stated plainly.** Every learning loop here — voice-check's profile updates, the revision analyses, `AUTHOR_REVISION_SPEC.md` — treats *what June changed* as evidence of *what is better*. For prose, voice, and register that is correct and is the whole point: it is her document and her voice. **But the same mechanism silently amplifies any systematic habit she has, including ones she considers weaknesses** — because a habit shows up in every revision, so it looks like the strongest signal in the data.

**Her own example, which is why this check exists:**

> "I think effective applications probably are geared towards 'what I would do in this role' in a future-oriented way (which shows interest and that I've genuinely pictured myself in this role). I tend towards a 'here are my past accomplishments of me doing the things you ask for' register. **It's not one or the other, but I think that future framing is an area where my own tendencies shouldn't drive the learning loop, and may need to be counteracted actively.**"

If she edits toward past-accomplishment framing in five consecutive applications, the loop learns "she wants past-accomplishment framing" — and starts *generating* it, removing the very thing she is asking us to supply.

**The rule:**

1. **A revision analysis distinguishes two kinds of change**: voice/register/accuracy edits (learn from these — they are authoritative) and **strategic-framing** edits (record, but do not promote to a rule without either her explicit ratification or outcome evidence).
2. **A tendency she has flagged as a weakness is a counter-target, not a target.** It goes in a standing list, and a draft is checked *against* it — the correct agent behaviour is to supply what she under-supplies, not to match her distribution.
3. **The standing counter-list, as of 2026-08-16:** *future-oriented framing* — what she would do in the role, evidence that she has pictured herself in it. Her instinct runs to the past-accomplishment register; drafts should carry both, and an agent should expect her edits to trim the future-facing material without that meaning it was wrong. **She named this one herself; nothing goes on this list except by her naming it.**
4. **Whether future-orientation is actually more effective is a separate question, and the answer as of 2026-08-16 is that nobody knows.** A full sweep of `_application_evidence/` found the corpus **essentially silent on it.** This check does not depend on the answer — it is about *how the loop treats her edits*, not about which register wins — but the counter-target above is her judgment, not a finding, and must be carried as such.

   **What the sweep actually found, so a later instance does not re-derive it:**
   - **The nearest finding is on a different axis.** Hou's move analysis splits the argument move into *background/experience*, *benefit to the organization*, and *benefit to the applicant* — and finds the second used in only 20% of letters where the first appears in 100% (`Genre_Move_Structure.md:162`). **That is "what does this do for you," which is fully satisfiable in past tense.** It is not a future-orientation finding, and reading it as one is the available mistake.
   - **The only explicit statement about future tense in the workspace treats it as a defect** — `ARG-3`'s tell, future-tense duty language with no instance attached. Read precisely, the defect is *evidence-free* futurity, not futurity. Nothing licenses future-orientation positively.
   - **In grants the two halves point opposite ways.** Published criteria are proposal-forward (NEH uniquely says "the quality *or promise of quality* of the applicant"), while measured reviewer behaviour runs on record — panelists delegate to CV under time pressure, and the hardest evidence in the corpus (Bol et al. 2018, regression discontinuity) shows past funding compounding.
   - **Her suspicion about her own instinct has exactly one ambiguous data point**, bucketed `?` by its own analyst as possibly rhythm (`REVISION_ANALYSIS_2026-08-12.md:283`).

   **This is a genuine gap, not a re-read problem.** Answering it needs new work. Until then the counter-target operates on her authority alone, which is a sufficient reason to supply the material and an insufficient reason to claim it wins.

*Related and distinct:* `PRO-11`'s corollary says a cut made under length pressure is not evidence the material was weak. Both are cases of the same error — **reading a constrained choice as a preference.**

**PRO-13 · `INST` · Diff every version against the author's standing inclusion requests.** *Proposed 2026-08-12 (as `PRO-9` — see the numbering note), applied 2026-08-16.*

`PRO-4` records what she asked to have included. **Nothing compares a new version against that record**, so material she asked for by name disappears in a later pass and only she notices. Observed: her Spelman rewrite silently dropped the **Justice in AI working group**, which she had requested by name and confirmed as *"SUPER important."*

**One row per standing request, present/absent, every version.** This is `INST` scope — it produces a list, not a verdict. A request that has gone absent is either restored or becomes an `EXCLUDED` row under `PRO-7` with a reason, never a silent loss.

*Numbering note:* the 2026-08-12 analysis proposed this as `PRO-9`, and `PRO-9` was independently assigned to flag dispositions on 2026-08-16 before that proposal was applied. This check is `PRO-13`. Anyone reading the older analysis should map its `PRO-9` to this entry.

**PRO-12 · `INST` · Carry the author's own sentence across applications, or mark the change.** *Proposed 2026-08-12 as `PRO-3b`, applied 2026-08-16 (renumbered — `PRO-3b` collided with nothing but read as a sub-clause of a different rule).*

**Observation, measured:** her PlayLab answers reuse her own Spelman sentences at **38% of words**; the agent draft reused **19%**, and inverted which parts it kept — it copied the audience-specific gloss verbatim and *paraphrased* the durable sentences.

> Hers (Spelman): "I packaged Autograder with installers **for Mac, Windows, and Linux**, then sat with a colleague…"
> Agent (PlayLab): "I packaged Autograder with installers, then sat with a colleague…"

`PRO-3` forbids wholesale rewriting *within* a document and is silent on transposition *between* them. **The author's own prior sentences are the strongest available material; the entity glosses attached to them are the weakest** (`ARG-4`). Carry the sentence, re-aim the gloss.

---

## 3. Roles — four, separated on purpose

| Role | Does | Never does |
|---|---|---|
| **Orchestrator** | Runs the process, spawns agents, handles errors, decides when to loop | Writes prose; verifies |
| **Editor** | Judgment: selection among components, what is load-bearing, what gets dispatched back | Verifies its own selections |
| **Style editor** | Applies the voice-check qualitative checks in full, reports findings by check id | Drafts; fact-checks |
| **Verifier** | Produces the findings artifact against this standard | Fixes anything |

**Why separated.** Nobody reads cold a sentence they wrote for a reason they still find convincing. This applies most to whoever has been steering — the orchestrator carries the whole run in context and is the worst reader in the room. **Scope is also what makes an agent read its material: a narrowly scoped agent reads the whole thing; a broadly scoped one samples it.** That is the direct cause of thirty-eight qualitative checks being read four-deep.

---

## 3a. Prose checks — added 2026-08-11 after a draft shipped with none run

**These were missing entirely.** §0 said "prose checks live in the voice-check profile," which meant the verifier structurally never checked them: the word *passive* appeared zero times in a full verification artifact. Pointing at the profile is not the same as checking against it.

**PRO-A0 · `SENT` · Enumerate every COPULAR construction where an action verb was available. This is the one that characterizes the whole register.**
*Named by June, 2026-08-11, correcting both "passive" and "nominalization":* **"Atlanta is where I was raised"** is a worse way of writing **"I was raised in Atlanta."** She calls it a recurring construction in this model's writing, and it is.

The pattern: take a plain agent-verb-object sentence, demote the verb into a relative clause or a gerund, and put *is* in the main slot. Forms to enumerate:
- **Pseudo-cleft** — "X is where/what/why/when Y." → *"Atlanta is where I was raised"* · *"the working group is where I would bring a practice"*
- **Demonstrative + copula** — "That is the ___ I would ___." → *"That is the testing I would do at Spelman"*
- **Gerund subject + copula** — "Doing X is the hard half." → *"Getting people from agreement to actual use is the hard half"*
- **It-cleft** — "It is X that Y."
- **Bare equation** — *"Both halves are one job."*

**Test:** does a simple subject-verb-object version exist? *I was raised in Atlanta. I would test tools that way at Spelman. I would bring that practice to the working group.* If yes, the copular version is the defect.

**Why this matters more than the other two prose checks:** it is high-frequency, it is invisible to a passive-voice search, and it is what makes prose read as flat and agentless while every individual sentence looks grammatically fine. It is also the reason "run a Williams pass" has repeatedly produced no change — a word-count trim leaves every cleft intact.

**PRO-A1 · `SENT` · Find the agent; find the action. Enumerate every NOMINALIZATION, not every passive.**
*Corrected 2026-08-11 on measured evidence.* Reinhart et al., *PNAS* 2025 (122(8):e2422455122) found GPT-4o uses agentless passive at roughly **half** the human rate, while **nominalizations run 1.5–2× human rate**. Prose that reads as passive is usually agency dissolved into abstract nouns — *"the implementation of," "the misreading of," "the conversion of X into Y"* — with a weak linking verb. Hunting passives finds little; hunting nominalizations finds the actual defect. Enumerate every abstract noun occupying a subject position and name the concrete agent it displaced.

---

### ⚠ A measured ceiling this standard exceeds, and what the evidence says to do instead

**Judgment-dependent constraints collapse past roughly three per pass.** FollowBench (*ACL 2024*): GPT-4's all-constraints-satisfied rate falls 84.7% → 61.9% by level five; practical ceiling ≈3. Mechanical instructions scale far better (IFScale: ~98% at 38 instructions), but almost everything in this file is judgment-dependent. **A style editor handed the profile's full qualitative set is being asked to do something no model does reliably.**

*Corrected 2026-08-12.* This passage said "38 checks" throughout. **The profile now carries 54.** The number was never re-counted after the profile grew, so every argument built on it understated the problem — the gap between three and fifty-four is not a matter of degree. Re-count before citing; do not hard-code the number here again.

**Rules transmit less than examples.** Webson & Pavlick (*NAACL 2022*) found models learn as fast from deliberately misleading instructions as from correct ones. Min et al. (*EMNLP 2022*): demonstrations teach *what this looks like*, not the generating rule; definition **plus two examples** scored 62.0 against 48/45 for either alone.

**The author's own sentences are the lever with measured effect.** Chakrabarty & Dhillon (*CHI 2026*, preprint): fine-tuning on an author's corpus moved blind expert preference from 82.7% favoring the human original to **62.2% favoring the model**, 81.1% on stylistic fidelity. DITTO (*ICLR 2025*): fewer than ten of the author's own samples used as preference signal beat few-shot prompting **72.1% to 48.1%**, saturating at 1–3 demonstrations.

**Therefore, for prose passes: run ~3 checks at a time, each paired with two of the author's own sentences** — one that does the thing and one that fails it — rather than handing an agent the whole rubric. Sequential small passes over a single large one. This is a change in how the standard is *used*, not in what it contains.

**PRO-B · `PARA` · Topic sentence first.** Each paragraph **opens** with its proposition; the story or evidence then demonstrates it. `ARG-2` only required that a paragraph *carry* a proposition, which passed three paragraphs whose claim arrived in the last sentence. This is one of the author's most-repeated corrections and it was absent from this file.

**PRO-C · `SENT` · No aphorism or generalization not earned by a preceding specific.** Enumerate every general statement and name the specific that earns it. If none precedes it, it fails.

**PRO-D · `INST` · Every forward-looking promise gets a row.** "I would…", "at Spelman that means…" — the prior verifier excluded these from the claims table by construction, so **promises were unaudited**. Each one must be traceable to a documented capacity or marked `[NEED:]`. An unbacked promise about what the applicant will do for future students is an overclaim.

## 3b. Three gate rules — the failures were procedural, not perceptual

**GATE-1 · A style review must run on the text being shipped.** If the draft's paragraph count or word count differs from the one named in the latest style review, that review is **stale** and the draft cannot pass. On the run that produced this rule, the style review examined a five-paragraph 485-word draft; the shipped letter was seven paragraphs and 557 words, and three of its paragraphs had never been style-checked.

**GATE-2 · `DOC`-scope is forbidden for any check about content placement.** `ARG-7` (identity claim first) passed as a one-word verdict with nothing to falsify. Re-scope it to `INST`: **name the identity claim and its sentence, name the fit claim and its sentence.** A check that cannot produce a list cannot be audited.

**GATE-3 · The gate blocks; it does not report.** Any `SAME ERROR` in the corrections audit, and any unresolved verifier miss, **blocks handover.** There is no "flagged for the author's eye" path for a known never-do violation — that path is how a caught real-students implication reached her twice. The author's own condition: *"If I have to repeat any editorial feedback, the letter fails and it isn't ready to show me."*

**GATE-4 · Whoever terminates the repair loop does not also decide the draft is deliverable.** Both decisions were made by the same instance ten minutes apart, and the second one discarded the results of the first.

## 4. Verification produces an artifact, not a judgment

**Observed failure:** an instance ran the automatable subset — a grep for known fabrications, a word count, a sentence-length measure, a presence-check for required strings — and reported "it passes." Every failure the author then found was a check already in the standard. **A checklist ticked mentally is not a check.**

1. Verification is performed by an agent that did not draft, assemble, or select.
2. Output is **written to disk**: every check, at its declared scope, with findings enumerated. Not a summary.
3. `INST`-scope checks produce **lists**, not verdicts.
4. Every failure **quotes the offending sentence**.
5. The verifier fixes nothing; it returns findings and the assembler acts on them.
6. **An unwritten cell is an unrun check.** If the author finds a violation of a check marked satisfied, the artifact was falsified, and that is a process failure to log — not a prose problem.

---

## 5. Changelog

### 2026-08-16 — applied from `REVISION_ANALYSIS_2026-08-16_FAMSF.md` and the unapplied half of `REVISION_ANALYSIS_2026-08-12.md`

**Context.** The Aug-12 analysis proposed nine amendments, each naming its target file. Only one had been applied (the Vale `facilitate` removal). The other eight sat in prose while the next application reproduced three of the defects they addressed. `PRO-10` now exists so this does not recur: **an analysis that proposes amendments applies them.**

| Change | Where | Origin |
|---|---|---|
| `ARG-4` amended — gloss carries the reader it was written for; a gloss carried from another application is a `[NEED:]` | this file | Aug-12 §5, the "one change" |
| `ARG-4a` added — the author's own named artifacts get named | this file | Aug-12 §Q5 (§7 extends) |
| `ARG-3` extended — the tell (future-tense duty language, no instance) and the cause (a duty with no inventory row) | this file | FAMSF §1 |
| `ACC-3` given teeth — inventory is a gate; its NOT-AVAILABLE list is an assembly input needing a disposition | this file | FAMSF §1 + Aug-12 §Q4 |
| `ACC-5` added — prior adoption of the employer's own tools | this file | Aug-12 §3.7 |
| `ACC-6` added — inventory rows for work in progress and for behaviour at scale | this file | Aug-12 §3.8 |
| `AUD-6` collision resolved — service-verbs check renumbered `AUD-7` | this file | FAMSF (two checks under one ID) |
| `AUD-7` extended — named events, not named institutions | this file | FAMSF §4 + PlayLab #31 |
| `AUD-8` added — a plan may not license an exception to a rule the author wrote | this file | FAMSF §4 |
| `PRO-3a` amended — `LENGTH_COLLAPSE` verdict, `--expect-cut` / `--author-edit` declarations | this file + `_tools/check_rewrite_fidelity.py` | FAMSF §2 |
| `PRO-6` amended — measured page capacity replaces two unmeasured guesses | this file | FAMSF §6 |
| `PRO-8` added — a lint hit on author-written text is a rule defect | this file | Aug-12 §3.2 |
| `PRO-9` added — every flag carries a disposition; `FLAGS.md`; nothing advances blank | this file + `templates/FLAGS_TEMPLATE.md` + printpress Stage 3 | FAMSF §5 |
| `PRO-10` added — an analysis applies its own amendments | this file | FAMSF §5 |
| `PRO-11` added — the author sees the assembly before the cut | this file | FAMSF §0 + author, 2026-08-16 |
| `PRO-12` added — carry the author's sentence across applications (was proposed as `PRO-3b`) | this file | Aug-12 §3.9 |

**Outside this file:**

| Change | File |
|---|---|
| `LENGTH_COLLAPSE` verdict + `--expect-cut` / `--author-edit`; verified against all six FAMSF transitions | `_tools/check_rewrite_fidelity.py` |
| `I am excited (to\|about\|by)` removed — refuted by her finished text in three consecutive applications | `styles/JuneBloch/CorporateRegister.yml` |
| `transformative` inside an organization gloss documented as a known false-positive class | `styles/JuneBloch/CorporateJargon.yml` |
| `most significant` etc. documented as firing on attributed external reputation, not only self-praise | `styles/JuneBloch/SelfAggrandizing.yml` |
| **This file added to required reading, with a per-stage check index** — it was referenced by nothing | `printpress/SKILL.md`, `Job Search/CLAUDE.md` |
| Stage 3 now closes by opening `FLAGS.md`; hard gate on undisposed rows | `printpress/SKILL.md` |
| One-page target corrected to ~500 working / ~525 ceiling (measured) | `printpress/genre_configs/non_academic_application.md`, `PIPELINE.md` |


### 2026-08-16, second pass — the four Aug-12 amendments missed on the first pass, plus author corrections

The first pass applied five of the Aug-12 analysis's nine amendments and reported the task closed. Four were missing. Recorded here because that is `PRO-10`'s failure happening inside `PRO-10`'s own implementation, one turn after it was written.

| Change | Where | Origin |
|---|---|---|
| `AUD-6a` added — per-**field** allocation decided before drafting (the PlayLab reallocation, −2.5% total text; no proportion proposed) | this file | Aug-12 §3.3, missed |
| `PRO-13` added — diff every version against standing inclusion requests (the dropped Justice in AI working group) | this file | Aug-12 §3.6, missed. **Numbering:** Aug-12 called this `PRO-9`; `PRO-9` was taken. Map accordingly |
| `demonstration_over_peroration` narrowed — the declarative may name what a thing IS, not what the demonstration MEANT (she cut 5 of 6 codas, kept the one stating a fact) | `voice-check/profiles/june_bloch.json` | Aug-12 §3.4, missed |
| `one_focus_per_paragraph` given a genre scope note — in application prose the unit is a capability claim with its instances; a 49-word cover-letter paragraph is a fragment. No word range proposed | `voice-check/profiles/june_bloch.json` | Aug-12 §3.5, missed |

**Author corrections to the first pass:**

| Change | Where | Origin |
|---|---|---|
| **`DISSOLVED` disposition added**, with the test for where a flag's condition lives — document vs. posting. The first version said flatly "deletion is not a disposition," and that was **wrong**: cutting is often the strongest answer to a critic, because readers never see what was removed | `PRO-9`, `templates/FLAGS_TEMPLATE.md` | June, 2026-08-16 |
| **Consult rule** — a convergent flag on a heavily weighted duty with no evidence is hers to decide; asked as one plain question, and an unanswered question never blocks the draft | `PRO-9`, template | June ("it might even be a point where it would have been appropriate to consult with me") |
| **`AUD-9` added — name the thinnest duty at Stage 0.** "Operational register" was FAMSF's accident; the pattern is that every posting has a duty cluster where her evidence is thinnest, and it is knowable before drafting | this file | June ("maybe what we need is a protocol for those things?") |
| **`PRO-14` added — not every author tendency should be learned.** The loop treats her edits as ground truth, which silently amplifies habits she considers weaknesses. Standing counter-target, named by her: future-oriented framing | this file | June ("my own tendencies shouldn't drive the learning loop, and may need to be counteracted actively") |
| Budget restated as **proportions of the final target `T`** (capture around 1.6×, author marks before selection, provisional handoff around 1.2×, author works toward `T`) so it carries across genres; both the ratio and the post-marking cutting route flagged as experiments, not findings | `PRO-11`, `PRO-6`, genre config | June ("lets use purportions/percentages… lets try 600 first"; later clarification that AI-cut quality and ownership remain unresolved) |
| Elder-naming question **closed** — not load-bearing; revisit only if it becomes a pattern | — | June |

**Status of the Aug-12 backlog: closed.** All nine applied. Verify with the ID list in §2 before believing this line.

**Refused, and recorded so a later instance does not derive them again** (extending the Aug-12 list of three):

1. **A paragraph word range.** Her paragraphs cluster 130–185 words across four documents. Four documents cannot carry a number, and a number is what gets enforced hardest against the material least able to justify it.
2. **A rule about naming individuals.** She replaced the elder's personal name with his role-title (*Heles-Hayv*, Maker of Medicine). Given `project_thpo_situation` this is plainly deliberate, and it is hers to state — one instance cannot carry a rule about how Pvlvcekolv people are named in her writing. Routed to her as a question.
3. **Anything derived from her compression pass.** Per her own instruction, 2026-08-16: a cut made under a length constraint is not evidence the material was weak. `PRO-11`'s corollary states this; no check here is derived from a second-pass cut.
