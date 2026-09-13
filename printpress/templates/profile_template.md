# Author profile — [Name]

<!--
This template implements SPEC.md § "Where the skill finds local files" (priority 3 — skill profile) and UX_STUB.md § "Profile format (author-informed reviewer)."

The skill copies this template into ~/.claude/skills/printpress/profiles/[author].md during profile setup. The profile is read by /critic-swarm's author-informed reviewer at Stage 3, and by /printpress at Stage 0 to locate source documents.

Profiles are NOT committed to git (see init.sh — profiles/ is gitignored at install time). They contain personal context about the author's work and failure modes that should stay local.

Build path: manual fill, OR bootstrap from documents (point the skill at PDFs, CVs, research statements; agent extracts a draft for review). See UX_STUB.md profile setup flow for the three-question voice memo extraction.

v2 note (per SPEC and UX_STUB): if a semantic memory architecture (MemPalace or equivalent) holds the author's publications and contributions, the author-informed reviewer should query that instead. The flat file is a v1 approximation — don't over-engineer expecting to replace it.
-->

**Last updated:** [YYYY-MM-DD]

---

## Key contributions

<!--
What this author has done that tends to get undersold when someone else describes their work.
Specific, not generic. "Works on AI ethics" is not a contribution; "named a specific structural pattern in [domain] that prior literature treated as individual variation" is.
2–4 items. The author-informed reviewer reads this to flag drafts that under-claim what's actually been done.

UX_STUB question 1: "What are your 2–3 most important contributions — the things that most often get undersold when someone else describes your work?"
-->

- [contribution — what was done, why it matters, what it cuts against]
- [contribution]
- [contribution]

---

## Key projects

<!--
Current and recent work, with brief descriptions and source paths if they exist.
The author-informed reviewer reads this to ground its critique in what the author is actually working on, not just what the draft mentions.
Source paths matter: the skill uses them at Stage 0 (data-in) to load specific factual material.
-->

- **[Project name]** — [1–2 sentence description, what it does, current status]
  - Sources: [path/to/source/doc.md], [path/to/another.pdf]
- **[Project name]** — [...]
  - Sources: [...]

---

## Failure patterns

<!--
What goes wrong in this author's drafts. The author-informed reviewer uses this to predict where THIS draft might be failing.
Examples of failure pattern types: ADHD-pattern issues (forgetting to include something, frontloading the wrong claim), compression casualties (specific things that get cut that shouldn't), voice contamination signatures (corporate register, hedging, narrative padding the author doesn't write but agents introduce), genre-specific traps (this author keeps making this same mistake on grant narratives).
Be specific. "Sometimes too long" is useless; "tends to bury the analytical contribution under fieldwork detail in the opening; the move only lands if the contribution comes first" is useful.

UX_STUB question 2: "What goes wrong in your drafts? Patterns you notice, things that get cut that shouldn't, things you forget to include."
-->

- [pattern — describe it specifically enough that an agent could recognize it in a draft]
- [pattern]
- [pattern]

---

## Source documents

<!--
Paths to fuller briefing docs. These get read by the author-informed reviewer at Stage 3, alongside the draft, to give the persona the depth it needs.
Don't list every file the author has written — list the documents that an agent would need to read to understand the author's work and voice well enough to critique a draft as if it were a longtime collaborator.
Common entries: agent briefing doc, voice document, publications portfolio, deep-read of publications, research-statement-archive, primary CV.

UX_STUB question 3: "Is there a document that describes your work in detail — a CV, a research statement, a bio?"
-->

- [path/to/agent_briefing.md] — [what it is]
- [path/to/voice_document.md] — [what it is]
- [path/to/publications_deep_read.md] — [what it is]
- [path/to/CV.docx] — [what it is]

---

## Notes for the agent

<!--
Anything else an agent reading this profile cold needs to know to do good work for this author. Examples:
- Naming conventions the author uses for their projects (initials, codenames, internal vs. public names)
- Voice-check profile location if it differs from the default discovery path
- Working-directory CLAUDE.md path if the file structure is unusual
- Sensitive context (e.g., a topic that requires care when surfacing in drafts — see SPEC.md examples re: process-as-method, pause-as-method)

Skip if there's nothing worth flagging.
-->

- [note]
