# /printpress — UX Stub

**Status:** Stub — interaction patterns described but not implemented. Use this during the SKILL.md build to design what the skill actually says.

---

## UX principles

**One thing at a time.** Never present multiple questions or decisions simultaneously. Present, wait, proceed.

**Specific over open-ended.** "What's the one thing you want this document to accomplish?" beats "Tell me about this application." Where options exist, surface them as structured choices.

**Two question modes:**
- **Structured choices** → AskUserQuestion tool (2–4 options, "other" always available). Use for: genre confirmation, reviewer panel approval, learning loop prompts.
- **Reflective/generative questions** → Voice memo invitation. Use for: Stage 1 Move 2 (name the story), Stage 0 peer_review source material, profile setup. Format: "This is a voice-memo question — 60-90 seconds is enough. [Specific framing question]. I'll read the transcript when you're done."

**PARK tangents.** If the author introduces something interesting but off-track, capture it explicitly: "Parking that — [brief summary]. Continuing with [current thread]." Don't let tangents get lost and don't let them hijack the flow.

**Overwhelm detection.** Increasing typo density → shorten responses, ask one targeted question, check in.

---

## Interaction at each key moment

### Invocation

Skill reads available context (current directory, any open files, recent conversation). Makes a best-guess at genre. Presents as a confirmable statement, not a question.

> "Looks like an academic job application — the posting is at [path]. Starting from there. Sound right?"

AskUserQuestion if the guess is uncertain or no context is available:
> "What kind of document are we working on?"
> Options: Academic application / Grant or fellowship / Non-academic application / Peer-review article / Something else

### Stage 0: Data-in

If required files are missing, surface them one at a time — not a checklist. Most critical first.

> "I need the posting before we can do anything else. Is there a URL, or a file I should look for?"

For peer_review, source material is the unknown. Voice memo invitation:
> "I need to understand what you're working with. Voice memo question: where does this paper come from — fieldwork, archive, experiment? What are the main sources? 60-90 seconds is plenty."

### Stage 1: Pre-draft cyborg conversation

**Move 1 — Candidate framings**  
Present 2–3 options, not a wall of text. Each framing gets: one sentence on what it opens up, one sentence on what thread it picks up. Numbered. End with: "Which of these is closest, or is the actual framing somewhere else?"

**Move 2 — Author names the story** *(voice memo invitation)*  
> "Voice memo question: given those options, what's the story you actually want this document to tell? Not the argument — the story. What do you want the reader to walk away knowing about you and your work that they didn't know before? 60-90 seconds."
>
> [After transcription] "Let me read that back to make sure I've got it: [summary]. Is that the story?"

**Move 3 — Arc proposal**  
One clear proposal, not options. The agent commits to a structure. The author redirects.
> "Here's the arc I'd propose for a [genre] with this story: [3–4 beat description]. What's wrong with this, or what's missing?"

**Move 4 — Section beats**  
Structured list: section → what it carries → which specific source/scene/fact grounds it. Present as a table or short list. End with: "Anything on this list that surprises you, or anything load-bearing that's not here?"

### Stage 3: Reviewer panel (peer_review only)

After editor agent runs, show the proposed panel before launching reviewers. AskUserQuestion:

> "Here's the reviewer panel the editor agent selected: [name + 1-sentence rationale for each]. Any to add, swap, or remove before I launch?"
> Options: Looks good / Swap one out / Add someone / Start over

### Synthesis output

Scannable structure. Cut list is FIRST — it's the most actionable revision work.

```
## Cut list
[passage] → [why it can go] → [~N words]
...

## Convergent flags (N reviewers flagged this)
...

## Threading suggestions
[what's missing] → [where it splices in]
...

## Specialty insights (single-reviewer)
...

## Mechanical (fix before save)
[jargon flags, intelligibility breaks]
```

Present with: "Here's what the swarm found. The cut list is where most revision work lives — start there. What do you want to work through first?"

### Learning loop surfaces

At Stage 0, brief and skippable:

*Genre review (every 3rd–5th use):*
> "You've used academic_position [N] times. Before we start — worth a 5-minute genre config review? [Yes, quickly / Skip for now]"

*Other accumulation (3rd+ use of 'other'):*
> "This is the [N]th time you've used 'other' — these uses look like [description]. Should we add this as a genre? [Yes, let's spec it / Not yet / Skip]"

### Profile setup (author-informed reviewer)

If no profile exists at invocation:
> "The author-informed reviewer needs a briefing doc about your work and failure modes. Do you have one? [Point me to it / Let's build one now / Skip this reviewer]"

If building now — three voice memo questions, one at a time:

1. "What are your 2–3 most important contributions — the things that most often get undersold when someone else describes your work?"
2. "What goes wrong in your drafts? Patterns you notice, things that get cut that shouldn't, things you forget to include."
3. "Is there a document that describes your work in detail — a CV, a research statement, a bio?"

Agent extracts a draft profile from the answers + any documents pointed to. Shows the author the draft for correction before saving to `profiles/`.

---

## Profile format (author-informed reviewer)

Stored at `~/.claude/skills/critic-swarm/profiles/[name].md`. Not committed to git.

```markdown
# Author profile — [Name]
# Last updated: [date]

## Key contributions
<!-- What this person has done that tends to get undersold. Specific. -->

## Key projects
<!-- Current and recent work, with brief descriptions. Source paths if they exist. -->

## Failure patterns
<!-- What goes wrong in their drafts. ADHD patterns, compression casualties, common mistakes. -->

## Source documents
<!-- Paths to fuller briefing docs (CV, research statement, briefing doc). -->
<!-- These get read by the author-informed reviewer alongside the draft. -->
```

**Building from data:** optional bootstrap command. Point the skill at documents (PDFs of publications, CVs, research statements) and it extracts a draft profile for review. Useful for first-time setup. For richer integration, see v2 note below.

**v2 note — memory architecture:** if a semantic memory system (MemPalace or equivalent) already holds the author's publications and contributions, the author-informed reviewer should query that instead of maintaining a separate flat profile. The flat profile is a v1 approximation; the memory architecture integration is the right long-term direction. Don't over-engineer the profile for v1 expecting to replace it.

---

## What this stub doesn't cover yet

- Exact wording for edge cases (profile missing mid-run, genre auto-detect fails, swarm subagent errors)
- How the skill handles multi-document applications during the arc conversation (allocation table introduction)
- The voice memo → transcription handoff mechanics (does the skill prompt and wait, or does the author run transcription separately?)
