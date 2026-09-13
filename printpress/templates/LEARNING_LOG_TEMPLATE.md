# Learning Log — [Application / Project Name]

<!--
This template implements SPEC.md § Learning loops, Tier 1 — document-local swarm performance log.
Lives in the project folder, stays there. Useful locally and as raw material for the periodic review that promotes patterns to Tier 2 (skill-global).

The skill copies this template into the working directory at the END of Stage 3 (after /critic-swarm returns synthesis), then fills it as Stage 4 revision proceeds.

This file is NOT the synthesis output — that comes from /critic-swarm and gets used directly in Stage 4. This is the meta-log: what the swarm surfaced, what the author did with it, what the personas were good at, what they were shallow on.
-->

---

**Application / Project:** [name]
**Genre:** [`academic_position` / `grant_fellowship` / `non_academic_application` / `peer_review` / `other`]
**Date:** [YYYY-MM-DD — the Stage 3 swarm date]

---

## Persona stack used

<!--
Stack passed to /critic-swarm at Stage 3, settled in Stage 1.
List only the stack-specific personas — the always-runs (intelligibility, jargon, author-informed) run on every swarm and don't need to be re-listed unless something specific to this run is worth noting about them.
For academic_position: the personas anchored to actual faculty from DEPARTMENT_PROFILE.md — note which faculty grounded which persona.
For peer_review: the panel selected by the editor agent.
-->

**Stack-specific personas:**
- [persona type] — [grounding: faculty name / role / domain]
- [persona type] — [grounding]
- [persona type] — [grounding]

**Always-runs:** intelligibility, jargon, author-informed [/ skipped because no profile]

---

## Convergent flags surfaced

<!--
Per /critic-swarm synthesis: items multiple reviewers flagged independently.
Convergent flags are the highest-confidence signal in the synthesis — they're where the document is most clearly underperforming for its actual readers.
Capture them here even though they're already in the synthesis output, because this log is what the periodic review reads later.
-->

- [flag] — flagged by [N] reviewers ([which])
- [flag] — flagged by [N] reviewers
- [flag] — flagged by [N] reviewers

---

## What the author addressed vs. held

<!--
Stage 4 outcome. Not every flag gets addressed — the author makes judgment calls. The held ones are part of the record: they show where the author's voice / strategic call diverged from the swarm's pull.
"Held" is not failure. It's information. If a persona consistently flags something the author consistently holds against, the persona may be miscalibrated for this author or this genre — that's a Tier 2 learning.
-->

**Addressed:**
- [flag] — [how it was addressed]
- [flag] — [how]

**Held (and why):**
- [flag] — [why the author held — voice call, strategic, disagreement with the read, etc.]
- [flag] — [why]

---

## Persona performance notes

<!--
Which personas surfaced sharp critique, which were shallow, which surfaced something only they could have caught.
Sharp = specific, grounded in the document, would change the revision. Shallow = generic, could have been said about any document in this genre, didn't move anything.
This is the field that feeds Tier 2 genre config refinement: when a persona type is consistently shallow across multiple uses, the genre config drops or reformulates it. When a persona type consistently surfaces sharp critique, it gets promoted to default for the stack.
-->

- **[persona type]:** [sharp / shallow / mixed] — [one sentence on what they surfaced or missed, with enough specificity to be useful three months later]
- **[persona type]:** [sharp / shallow / mixed] — [...]
- **[persona type]:** [sharp / shallow / mixed] — [...]

---

## Cross-stack generalization tag

<!--
Per SPEC § Cross-genre generalization: at log-write, tag each learning here as `genre-specific` or `potentially-generalizable`.
The agent's tag will be wrong sometimes — that's fine, it's input to the periodic review, not a final decision. Periodic review validates and promotes truly generalizable learnings to ~/.claude/skills/printpress/principles.md (Tier 2).
The tags should be on specific findings, not on the file as a whole.
-->

| Learning | Tag |
|---|---|
| [specific finding from this swarm — e.g., "junior-faculty persona surfaced citation density issue earlier than search-chair"] | [genre-specific / potentially-generalizable] |
| [specific finding] | [tag] |
| [specific finding] | [tag] |

---

## Notes for the periodic genre review

<!--
Anything the agent or author wants surfaced when the periodic genre config review runs (every 3rd–5th use of this genre).
Examples: a persona that should be added to the default stack, a persona that consistently underperforms for this genre, a context document type the swarm needed that wasn't in Stage 0 sources, a synthesis-output structure change that would help.
Skip if there's nothing worth flagging — empty is fine and informative.
-->

- [note]
