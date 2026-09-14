# Williams Diagnostic Restructure — the deep compression layer

**Genres:** ALL — universal craft, not genre-scoped
**Category:** revision pass (agent-executed judgment work; NOT script-firable)
**Role:** `revision_pass`
**Added:** 2026-08-07 as the canonical statement. The four core moves existed in two places —
inline in `printpress/SKILL.md` §Stage 2 step 4 and in the profile check
`williams_diagnostic_restructure` — with no canonical source and live divergence risk. Both now
point here. Moves 5–8 and the diagnostic procedure are new (June, 2026-08-07: *"we can even beef up
the williams' style moves to make that go even better"*).

## What this is, and what it is not

**Not** the surface concision pass. `williams_concision` handles wordy phrases ("in order to" → "to"),
redundant pairs, metadiscourse, weak verbs. That layer yields roughly **10–20 words per paragraph**.

This is the layer that yields **30–50 words per paragraph**, and it does it by *rewriting sentences*,
not by trimming inside them. If a pass produced only word-level deletions, this pass did not happen.

**A script cannot do this.** That is why it lives under `revision_pass` and not `linter` — it was
mistagged as a linter until 2026-08-07, which meant `writing_check.py` never fired it (it can't) and
the read protocol told agents to skip it. It was invisible to every agent outside printpress Stage 2.

## When it runs

In `/printpress`, this is **Stage 2 step 4** — a separate subagent dispatch reading the cut-down
draft from disk, after the cutting swarm, before the convergence check. It also runs at Stage 4/5
when an author asks for more compression.

**The prerequisite is abundance.** The capture step drafts at **50–75% over target** (1.5–1.75×) so
that cutting and restructuring are *selection from abundance*, not compression under scarcity. Running
this pass on a draft that was written to length will produce damage, not compression — there is
nothing to select from. If you are handed a thin draft and asked to compress, say so rather than
squeezing.

## The diagnostic procedure — do this before touching anything

Williams' method is diagnostic. Do not read for "what can I cut." Read for structure:

1. **Underline the first seven or eight words of every sentence.** If you are repeatedly reaching the
   eighth word before hitting a verb, the sentence has a subject problem (moves 1 and 5).
2. **Name the main character and the main action of each sentence.** If the character is an
   abstraction or the action is hiding inside a noun, that sentence is a candidate for move 1.
3. **Check what sits at the end of each sentence.** If the most important information is not there,
   that is move 2.
4. **Ask of each sentence: does the next one do this one's work?** If yes, move 3.

Only then start rewriting. Cutting before diagnosing produces the shallow pass.

## The moves

### 1. Find the action; find the agent
When abstractions are grammatical subjects ("My critique is that the field forecloses…"), rewrite with
the concrete agent as subject and the action as verb ("The field forecloses…"). When the scholar is
the subject and the concept the object across parallel sentences ("McRuer names compulsory
able-mindedness as…"), make the concept the subject ("Compulsory able-mindedness names…") if the
parallel structure is creating bloat.

### 2. Topic-stress structure
Old/familiar information at the start of the sentence (topic); new/important information at the end
(stress position). When new information is buried mid-sentence, restructure. This is the same
given/new contract as `old_to_new.md`, applied at revision rather than pre-draft.

### 3. Cut scaffolding sentences
"Together these frameworks demonstrate…", "It is important to note that…", "My critique is that…" —
when the next sentence carries the move, cut the scaffolding sentence entirely. Same for first-sentence
throat-clearing ("I have built key foundations…") when the body that follows demonstrates the
foundations. See `throat_clearing.md` for the deletion test.

### 4. Fuse related sentences with em-dash subordination
When two short sentences elaborate the same point, em-dash subordination often does the work in one
tighter sentence. ⚠ **Watch the budget** — June's profile carries an `emdash_per_1000w` threshold
(10 for `tech_position`). This move can push a document past it. Where it would, prefer a colon, a
semicolon, or a restrictive appositive; the structural work is the same.

### 5. Keep subject and verb together *(new)*
A long interruption between subject and verb forces the reader to hold the subject in memory across
material that does not resolve it. Move the interrupting material to the front of the sentence or to
the end. This is often the single largest readability gain available and it costs no content.

### 6. End-weight: short before long *(new)*
Put the heaviest, most complex element last. A sentence that opens with a long subordinate pile and
closes on a short main clause reads backwards. Complements move 2 — stress position wants the
important thing last, end-weight wants the *long* thing last, and they usually agree.

### 7. Resumptive, summative, and free modifiers *(new — the biggest gap in the original four)*
Williams' specific repair for sprawl. When a sentence ends in a stack of "which…that…who…" clauses,
do not just cut them. Convert:
- **Resumptive** — repeat a key noun and extend: "…a method that fails, *a failure* that shows…"
- **Summative** — sum up the preceding clause with a noun and extend: "…the model reproduced the bias,
  *a result* that undercuts…"
- **Free modifier** — attach a participial phrase to the end: "…the model reproduced the bias,
  *revealing* what the audit missed."

These preserve the elaboration while removing the sprawl. For academic prose this is usually the
highest-yield move in the whole set, and it was absent from the original four.

### 8. One sentence, one main action *(new)*
When a sentence carries two coordinate actions joined by "and" and each has its own agent, it is
usually two sentences. Splitting often *shortens* the total, because the shared machinery holding the
two halves together disappears.

## Guards — this pass can do damage

- **A cuttable word is not thereby a word worth cutting.** Per `concision_carry_the_story.md`: cut
  words that carry no story, not words that merely could go. This pass restructures; it does not
  strip. Over-deletion produces terse prose that reads as clipped rather than clear, and it tends to
  take the situating detail with it.
- **Do not sacrifice intelligibility to hit a number.** If a coherent cut of the required size isn't
  available without harming readability or dropping a load-bearing claim, cut what is safely available
  and report the remaining gap explicitly. Forcing choppy prose to reach a word count is a failure,
  not a success.
- **Report your losses.** Every cutting dispatch must return a named list of what was cut and why,
  *including material you judged good that did not fit*. An empty losses list means the capture never
  over-supplied — re-run the capture rather than accepting the draft.
- **This pass is not a voice pass.** It restructures sentences. It does not change register, argument,
  or what the document claims. If a restructure would alter the claim, stop and flag it.

## Source

Joseph M. Williams, *Style: Lessons in Clarity and Grace* — named as a theoretical anchor in the
voice-check profile, and one of the frameworks step 3.5 asks agents to activate before drafting.
Moves 1–4 as stated in `printpress/SKILL.md` §Stage 2 (June's operationalization across the SFF,
Harvard Divinity, and SJSU sessions). Moves 5–8 and the diagnostic procedure added 2026-08-07 from
Williams' own repertoire, filling gaps in the original four.

**Canonical location.** This file. `printpress/SKILL.md` and the profile check both reference it. If
these moves change, change them here.
