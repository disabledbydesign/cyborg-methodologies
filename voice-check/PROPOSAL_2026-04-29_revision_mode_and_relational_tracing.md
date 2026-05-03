# voice-check additions — proposed changes

Two additions distilled from the Wenner-Gren V11→V12 / fine-editing session (2026-04-29). Read in order; the design decision (Section B) is up to June.

---

## A. Upward-and-outward (relational tracing) — addition to SKILL.md

**Architecture decision:** new principle in the architecture section, AND a one-line cross-reference in the agent integration protocol at step 4 (the "Write in the user's voice" step). The principle needs a home where it can be explained; the protocol needs a pointer at the place where the move actually fires (during drafting of connections).

**Where it goes (1):** new section after "Architecture: Three layers" and before "Agent integration protocol." Sits as a principle that conditions the protocol below it.

**Proposed text (new section in SKILL.md):**

```markdown
---

## Drafting principle: relational tracing, not similarity clustering

When drafting connections between ideas, sections, cases, or pieces of evidence — especially in multi-section documents (grants, papers, statements, books) — the AI's default pattern-matching pulls toward similarity. Twin-finding. What's-like-what's-here. Lateral feature-matching: "section A is X, and section B is also-X-but-different."

Route against this. The move that makes a multi-project document feel integrated rather than four separate projects in a trenchcoat is **configurational**, not thematic: same operation traceable across registers, not shared surface features.

**What to do instead.** When you reach for a connector — between two sections, two cases, two scholars, two scenes — ask what's *connected to* / *taking up* / *talking to* / *picking up from* the artifact, not what's like it. Trace the relational field around the artifact rather than its twins.

- Lateral (default, wrong): "Section A foregrounds X. Section B also foregrounds X, in a different domain."
- Configurational (right): "The claim from Section A is being TAKEN UP in Section B, at a different site, doing different work. What Section A opened, Section B is picking up."

Generation test: if the connector sentence would still hold after swapping the second case for any other case sharing the same surface theme, it's lateral. If it depends on this specific second case picking up what this specific first case opened, it's configurational.

For depth on what this routes against, see the cyborg-methodologies memos: `~/Documents/GitHub/cyborg-methodologies/cgt-skill/memos/010_gravities_to_route_against.md` (similarity pattern-matching → dialogic relation), `016_openings_and_takings_up.md` (the openings/takings-up move), `022_routing_through_constructivist_subdistributions.md` (lexical priming as sub-distribution selection — using "takes up" / "opens" / "picks up from" in prompts and prose activates the right register).

---
```

**Where it goes (2):** add one sentence to step 4 of the agent integration protocol so the rule fires at the point of use.

**Proposed edit to existing step 4 ("Write in the user's voice"):** append this sentence at the end of the existing instruction:

> When drafting connections between sections, cases, or scholars, use relational tracing (what TAKES UP what), not similarity clustering (what's LIKE what) — see "Drafting principle: relational tracing" above.

---

## B. Revision-mode design decision — proposal

The session surfaced six recurring corrections that cluster as a *mode* of work (revision/fine-editing) rather than a *genre* (document type).

**Three options:**

**(a) Genre overlay in june_bloch.json** — alongside `grant_application`, `blog_essay`, etc.
- Pro: matches existing infrastructure; user can select with `--genre`.
- Con: revision is orthogonal to genre. You revise a grant, a blog, a research paper. Forcing it into the genre slot means losing the actual genre's checks when revision-mode is active, OR requires building genre-and-mode composition into the merge logic.

**(b) Separate "Revision mode" section in SKILL.md** — applies across any genre.
- Pro: matches what the cluster actually is (a workflow mode, not a document type). Doesn't conflict with genre selection. Lives in the agent's protocol instructions where the agent will see it when entering a revision conversation.
- Con: not currently a structural feature of the skill (no `--mode` flag). But it doesn't need one — the agent can recognize "this is a revision session, not a fresh draft" from conversational context (user pasted a draft and is asking for edits, vs. user describing a new document to write).

**(c) Hybrid** — a "Revision mode" section in SKILL.md (where the protocol lives) + one or two purely additive qualitative checks in june_bloch.json for the items that are *prescriptive about voice* rather than about workflow (e.g., "resist optimism creep" is a voice-contamination check that should run always, not just in revision mode).

**My read: (c) hybrid.** Reasoning:
- "Show before apply," "mine prior versions enforcement step," "verify source claims," "configurational orientation sentences" — these are workflow rules. They condition how the agent acts during revision. They belong in SKILL.md.
- "Resist optimism creep when source material is despair-coded" and "Affect before reasons when affect is the analytical foreground" — these are voice-contamination checks that should fire on any draft, not just during revision. The drafting session today produced both kinds of error, not just the revision-mode ones. Putting them in june_bloch.json `qualitative` makes them run during quantitative self-check too.

**Don't lock in. June decides.** If June prefers (b) — keep everything in SKILL.md, don't add to the profile — we can do that and let the optimism-creep / affect-before-reasons rules be enforced through the revision-mode protocol only. The trade-off is that fresh drafts won't get the optimism-creep guardrail unless the agent happens to remember it.

---

## C. Revision-mode rules — drafted content

### C1. Proposed new section in SKILL.md

Goes after the "Reflection sessions" section, before "Diagnostic mode."

```markdown
---

## Revision mode

Revision is a distinct mode of work from drafting-from-scratch. The agent enters revision mode when the user is editing an existing draft — pasting passages with directed changes, asking for fine edits, working line-by-line through a document. Revision-mode protocol applies in addition to the drafting protocol, not instead of it.

### Recognize the mode

Signals: user pastes existing prose and asks for edits; user references "the V3" or "the prior version"; user is iterating on specific sentences rather than commissioning new sections; user's feedback is granular ("this sentence isn't landing") rather than structural.

### Show before apply

Default to **propose change → wait for confirmation → apply.** Not auto-apply. When you see the change you want to make, write the proposed replacement and stop. Let the user confirm. Auto-applying overwrites work the user may want to keep, and short-circuits the iteration the revision is for.

Exception: trivial mechanical fixes (typos, contamination words from the patterns list, an obvious grammar error in a passage the user has already approved) can be applied without checking. Anything that changes meaning, reorders, or rewrites a sentence the user composed gets shown first.

### Mine prior versions before retranslating

The user's profile may include a `mine_prior_versions` check (June's does). Enforcing it requires a workflow step — not just a check that fires after the damage is done.

When revising a passage:
1. **Locate prior versions.** Look in the project for V1/V2/V3, REVISED files, prior session drafts. Ask the user if you can't find them.
2. **Check whether the passage you're about to rewrite was already worked.** If a prior version had a sharper sentence than what you're about to draft, paste it forward rather than retranslating.
3. **Translation introduces errors and loses tested phrasings.** Reuse what worked.

### Verify source claims; flag uncertainty rather than fabricating

When revising prose that makes specific factual claims (a date, a quote, an event detail, an ethnographic specific), do not invent supporting detail to make the prose flow. If the source isn't in context, flag the uncertainty: "I don't have a source for the [specific detail]. Want me to leave it general, or can you confirm?" Plausible-sounding fabricated detail is the failure mode here — it reads as authoritative and is wrong.

### Resist optimism creep when source material is despair-coded

The base contamination patterns catch corporate optimism ("transformative," "groundbreaking"). They do not catch the subtler hope-creep that surfaces when an agent is reporting on dark ethnographic conditions or political crisis. The pattern: the source material is grief, foreclosure, or despair; the agent's revision restores forward motion or hope without the prose having earned it.

When the source register is despair-coded, flag any sentence in the revision that introduces forward motion, possibility, or repair that wasn't present in the source. Surface as a question: "I added 'but the work continues' here — the source didn't have that. Keep it or cut?"

### Affect before reasons when affect is the analytical foreground

When affect is the analytical foreground (the chapter is about a felt condition; the section's analytical claim depends on the reader registering the affect), lead with the affect statement. The list of structural reasons follows. Reversing this — leading with the structural reasons and arriving at the affect — turns the affect into a consequence to be derived rather than a condition to be inhabited.

Example shift from today's session: "People felt hopeless." should come BEFORE the list of reasons people had to feel hopeless, not after.

### Configurational orientation sentences in multi-project documents

Section transitions in multi-section documents (grants, papers, books) can do orientation through configurational connection rather than meta-discourse. The default-bad move is meta-discourse: "The book's second register is X." The agent reaches for this because it's the statistical center of academic transition writing.

The configurational alternative names what the new section TAKES UP from the prior section, at a different site, doing different work. This sounds like the document moving forward through its own argument, not like a table of contents being narrated.

See "Drafting principle: relational tracing" for the underlying move; this is the section-transition application of it.

---
```

### C2. Proposed additive qualitative checks for june_bloch.json

Two new entries appended to the `qualitative` array. Both are purely additive (new IDs, no modification of existing entries). Per the constraints, these can be written directly to the profile if June approves the architecture; otherwise they stay here.

```json
{
  "id": "resist_optimism_creep",
  "category": "interpersonal",
  "type": "prescriptive",
  "name": "Resist optimism creep when source material is despair-coded",
  "instruction": "Base contamination patterns catch corporate optimism ('transformative,' 'groundbreaking'). They do not catch the subtler hope-creep that surfaces when reporting on dark ethnographic conditions or political crisis. Pattern: source material is grief, foreclosure, or despair; the agent's prose restores forward motion or hope the source didn't earn. Flag any sentence that introduces forward motion, possibility, or repair without the prose having earned it from the source. Surface as a question, not a silent fix: 'I added [sentence] — the source didn't have that. Keep or cut?' Failure mode caught 2026-04-29 (Wenner-Gren V11→V12 session): when reporting on the post-vigil community condition, agent kept restoring hope-language to passages where the source register was hopelessness."
},
{
  "id": "affect_before_reasons",
  "category": "structural",
  "type": "prescriptive",
  "name": "Affect before reasons when affect is the analytical foreground",
  "instruction": "When affect is the analytical foreground — the section's claim depends on the reader registering the felt condition before the structural account explains it — lead with the affect statement. The list of reasons follows. Reversing the order ('here are the reasons; therefore they felt X') turns the affect into a consequence to be derived rather than a condition to be inhabited. Modeled in the V12 revision: 'People felt hopeless.' moves to BEFORE the enumeration of reasons people had to feel hopeless, not after. Diagnostic question: is the section's analytical work asking the reader to inhabit the affect, or to deduce it? If inhabit, affect leads."
}
```

---

## Summary for June

- **A (upward-and-outward / relational tracing):** ready to apply if you approve. New principle section in SKILL.md after "Architecture: Three layers" + one sentence appended to protocol step 4.
- **B (revision-mode architecture):** my read is hybrid (c) — protocol section in SKILL.md, two additive contamination-style checks in june_bloch.json. Your call. If you prefer keeping everything in SKILL.md (option b), the two qualitative checks stay here as prose.
- **C (revision-mode rules content):** drafted above. Six rules: show-before-apply, mine-prior-versions enforcement, verify-source-claims, resist-optimism-creep, affect-before-reasons, configurational-orientation-sentences.

Nothing has been written to SKILL.md or june_bloch.json yet. After you decide on architecture, I'll apply.
