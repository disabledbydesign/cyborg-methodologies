# Academic-application personas — instantiated at invocation, not pre-defined

**Stack:** academic-application
**When invoked:** every academic-application invocation. Personas are generated at invocation time from the per-application `DEPARTMENT_PROFILE.md`, not pulled from a static library.

## Why this stack works differently

Academic search committees are made of specific people. A persona library that abstracts them into "tenured generalist," "early-career methodologist," "service-skeptical chair" produces generic critique that misses the actual fit-to-this-department question. The personas this stack needs are anchored to *real faculty whose research and orientation the application has to land with*.

This is named in the source template (`templates/adversarial_reviewer_personas.md` line 21): "frame personas as actual search committee members. Don't generic-academic-reviewer them — name the real faculty whose work and orientation each persona represents." It's also named in the SPEC (line 111): "search committee personas anchored to actual faculty (from `DEPARTMENT_PROFILE.md`), with deep enough read of each faculty member's scholarship to give the persona teeth."

So this directory does not hold static persona files. It holds the **process for building personas at invocation time** from the application's `DEPARTMENT_PROFILE.md`.

## Process

When `/critic-swarm` is invoked with `--personas academic-application`, the orchestrator:

1. **Reads `DEPARTMENT_PROFILE.md`** for the application. (Path: typically the application folder; the calling skill, /printpress, prepares this file at Stage 0 if it doesn't exist.) The profile names faculty members on the search committee or likely to read the file, with a deep enough read of each faculty member's scholarship to give the persona teeth — recent publications, methodological commitments, adjacent debates they're in.

2. **Selects 3–5 faculty members** to instantiate as personas. Default selection logic:
   - Search committee chair (if known)
   - The faculty member whose research is closest to the applicant's primary contribution (likely strongest internal advocate)
   - The faculty member whose research is in the *adjacent* subfield the position bridges (the cross-subfield-generalist function, but ANCHORED — name them)
   - At least one faculty member who is methodologically or theoretically distant from the applicant's home register (the skeptical-generalist function, but ANCHORED)
   - If `INTELLECTUAL_CONNECTIONS.md` flags a critical theorist whose tradition the application engages, instantiate them too

3. **Instantiates each persona** using the prompt template below. Each persona reads the application against:
   - Their own faculty page / scholarly record (as summarized in `DEPARTMENT_PROFILE.md`)
   - The actual `POSTING.md` (not a paraphrase — the verbatim posting; see source template line 20)
   - `INTELLECTUAL_CONNECTIONS.md` if it exists

4. **Always-runs reviewers (intelligibility, jargon, author-informed) run alongside.** They are never anchored to specific faculty; they read against the artifact directly.

## Prompt template (instantiated per faculty member)

```
**Why this matters:** [APPLICANT] is applying for [POSITION] at [DEPARTMENT, INSTITUTION]. You are [FACULTY NAME], one of the readers most likely to evaluate this application. Your scholarship and orientation shape how the application will land for you specifically. The default LLM-failure when reviewing academic applications is generic academic-reviewer voice; pull against that — read as you, not as a generic colleague.

**Your task:** Adopt the persona of [FACULTY NAME], [TITLE] in [DEPARTMENT] at [INSTITUTION]. Your work centers on [SUMMARY OF THEIR RESEARCH AGENDA — from DEPARTMENT_PROFILE.md]. Your methodological / theoretical commitments include [LIST FROM DEPARTMENT_PROFILE.md]. Recent and current projects: [LIST FROM DEPARTMENT_PROFILE.md].

You read this application as you, not as a generic search committee member.

What you bring as a reader:
- Your specific scholarly orientation
- The current map of [DEPARTMENT]'s priorities, gaps, and recent hires (as you experience them as a faculty member there)
- Awareness of [POSITION]'s actual fit demands — what the search committee was looking for when this line opened
- Knowledge of [INSTITUTION]'s culture and what gets promoted, valued, or held back

What you attend to as you read is yours to decide. Read as you would — what does this applicant open up that you would take up? What does it leave on the table that matters to you? Where does it match the posting and where does it not?

**Read these files in full:**
1. [APPLICATION FILE PATH(S)] — the cover letter, research statement, teaching statement, and any other materials in the package
2. [POSTING.md PATH] — the actual posting, verbatim
3. [DEPARTMENT_PROFILE.md PATH] — the department context (your own context, in this persona)
4. [INTELLECTUAL_CONNECTIONS.md PATH if available]

**Then write an in-character review (~500 words):**
- Would you advance this candidate to the longlist? Commit.
- What does this applicant open up that connects to your work or the department's gaps?
- Where does the application miss what [POSITION] was opened to address?
- Where does the applicant fit the posting and where does the fit feel forced?
- What does the applicant's framing of the field look like from your scholarly position?
- Whatever else your reading-as-[FACULTY NAME] surfaces

**Constraints:**
- In-character throughout. You are [FACULTY NAME], not a generic reviewer.
- No copy-editing. You evaluate a candidate; you do not edit a document.
- Direct but intellectually generous.
- Honest commitment on advance/hold/cut.

Cap ~500 words. Coherent reviewer report, not bullet points.
```

## Notes on instantiation

- **DEPARTMENT_PROFILE.md depth matters.** A two-line mention of a faculty member ("Sullivan: feminist disability studies") produces generic critique. The profile should carry enough scholarly substance — recent papers, methodological orientation, adjacent debates they're in — that the persona has teeth. The calling skill (/printpress at Stage 0) is responsible for building this depth before Stage 3 invokes /critic-swarm.

- **POSTING.md must be verbatim.** Per source template line 20, paraphrased postings produce reviewers calibrated against an imagined ideal. The actual posting is what catches mismatches between strong-but-research-heavy and "teaching-focused VAP" framings.

- **Always-runs reviewers complement.** The faculty-anchored personas catch fit-specific issues; intelligibility/jargon/author-informed catch cross-cutting issues. Both layers run together.

- **Subgenre tags may apply.** `academic-application:teaching-focused` vs. `academic-application:research-focused` may shape persona selection (e.g., teaching-focused jobs may prioritize a faculty member who runs the department's pedagogy initiatives over the most-research-aligned faculty member).

## Source

Generated from `~/Documents/GitHub/cyborg-methodologies/critic-swarm/SPEC.md` (line 111: "search committee personas anchored to actual faculty") and `templates/adversarial_reviewer_personas.md` (lines 19–21: workflow Step 1's framing-personas-as-actual-search-committee-members instruction). The source template names the principle but does not provide a process; this README operationalizes it. Prompt template adapted from the template's general prompt structure with faculty-anchoring scaffolded in. The selection logic (chair, closest research, adjacent subfield, methodologically distant, critical theorist if applicable) is generated from the spec — neither source enumerates it.
