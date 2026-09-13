# Cyborg-Methodologies Cross-Skill Insights

System-wide methodological insights with cross-skill relevance. Seeds for what may become the cyborg-methodologies systemwide protocol layer (see CLAUDE.md TODO on architectural location decision). Each entry: when, where it surfaced, the insight, why it generalizes.

---

## 2026-04-29 — Pattern-matching as relational tracing, not similarity-clustering

**Surfaced in**: cgt-skill design session 2026-04-28, articulated more precisely 2026-04-29.

**The insight**: Default AI pattern-matching pulls toward similarity — *what's like what's already here*. Lateral, feature-matching, twin-finding. The cyborg practice's distinctive analytical move appears to be different: pattern-matching directed *upward and outward*, where the directionality is about looking for **connections and relationships**, not just patterns. The reach is toward what's *connected to* what's here, what *relates to* it, what it *talks to* — the relational field around the artifact, not the artifact's twins.

Same conceptual move as mycelial intelligence: connection-following rather than feature-matching. (Whether any specific implementation lives up to this theory is a separate empirical question; the framing matters even when implementations fall short.)

**Why this likely generalizes across skills**:

- **Voice-check**: voice profiles are currently stylometric — feature-matching against patterns. Relational tracing might be the missing layer: how does this voice *relate to* other voices, *respond to* prior text, *position itself toward* an audience? Voice-as-relation rather than voice-as-feature-vector.
- **Discourse-analysis**: discourse moves are inherently relational (who's positioning whom, how does this register relate to that one, what's being taken up from where). The /da skill could foreground relational tracing as a primary operation rather than a secondary one. Output-format-bias work is already touching this.
- **C2C**: instances doing pattern-matching on each other's outputs. Are they finding twins (consensus risk) or following connections (productive disagreement)? The distinction may be diagnostic for the bliss-vs-praxis attractor question.
- **CGT (cgt-skill)**: openings and takings-up (memo 016) is relational tracing at the record-cross-record level. This insight may be the meta-articulation of why memo 016 works — it's not a special move, it's the general AI mode the cyborg practice activates.

**Status**: Hypothesis with strong plausibility. We have one observation point (the cgt-skill design session). Worth testing across other skills' use to see if the framing improves work in each, or only in some.

**The mechanism question (open)**: Whether "relational tracing" tracks anything mechanistic in the model's architecture, or whether it's a description of the *output shape* that emerges under cyborg conditions, remains uncertain. Both interpretations are research-relevant; the description is useful regardless.

**Where the longer articulation lives**: cgt-skill/methodological_insights.md (under "Generative pattern matching") and the AI welfare research fieldnote at `~/Documents/GitHub/Reframe/reframe_AI_welfare/transcripts/de39b019-8bcb-4a6d-9cdf-15171d3d14c0/FIELDNOTE_2026-04-28_meta_memory_pattern.md`.

---

## 2026-05-07 — Adversarial swarm as design review method

**Surfaced in**: /printpress skill design session 2026-05-07. The skill spec was reviewed by a 3-persona swarm (future build agent, skeptical architect, coherence reviewer) treating the spec as the "document."

**The insight**: The adversarial reviewer swarm — originally designed for application drafts — works as a general design review method. Running the swarm on a spec, architecture doc, or workflow design surfaces three categories of problem that a single-author self-review misses:

1. **Build agent lens**: what's ambiguous or missing for someone implementing cold — the gaps that look obvious to the designer because they know the conversation context
2. **Skeptical architect lens**: is the design actually sound, or does it hold only under favorable conditions the design doesn't guarantee?
3. **Coherence reviewer lens**: where does the document assume knowledge the reader doesn't have, or use terms before defining them?

The convergence pattern held for design docs just as it does for applications: single-reviewer flags = specialty insights, multi-reviewer flags = load-bearing problems. The architect's "single highest-leverage fix" framing is especially useful for design docs where the designer is too close to the problem.

**Why this generalizes**: Any complex design artifact (skill spec, architecture doc, workflow, research protocol) has the same failure modes as an application: designed by someone with too much context, read by someone with too little. The swarm closes that gap in both cases.

**The meta-application**: The /printpress spec was itself improved by running /printpress Stage 3 on it before the skill was built. This is recursive in a useful way — the methodology stress-tests itself.

**Practical implication**: Run the adversarial swarm on any significant design document before finalizing it. Persona selection adapts: for design docs, "future build agent" replaces "program officer"; "skeptical architect" replaces "subfield specialist"; coherence reviewer is constant.

**Status**: One observation point (printpress spec). Worth trying on the next significant design doc to see if the persona adaptation holds.

**Where this lives operationally**: The /printpress skill spec at `~/Documents/GitHub/cyborg-methodologies/printpress/SPEC.md` is the first instantiation.

---

## 2026-06-14 — Open-ended subagent prompts for discovery; over-specification forecloses what you didn't know to look for

**Surfaced in**: PMA design-parameter session (Session 22), articulated by June after several subagent passes — and named by her as a failure mode "we've hit many, many times."

**The insight**: When you dispatch a subagent to *find* things in a corpus you have not yet fully read, the instinct (June's words: the tendency "for managing agents and sending off subagents") is to write a *very specific* prompt — "find X, Y, Z." Specificity is genuinely helpful for execution tasks. But for **discovery** tasks it is a trap: a prompt that names the categories to look for **limits the findings to the categories the manager could anticipate *without having the data*** — and the most important things are usually the ones no one knew to ask for. You get back a result pre-shaped by your preliminary categories, mistaken for a survey of what's actually there. The fix is the **genuinely open-ended question** ("imagine you're the agent who has to build this — what would you need from this material?"; "what's here that matters?"), with the failure-mode named *to the subagent* so it knows to resist narrowing, and **the subagent encouraged to answer in its own categories, not yours.**

This is **grounded theory / emergent coding applied to agent management**: you do not impose the coding frame before engaging the material; the categories emerge *from* the data. Imposing categories up front is the positivist move (the normative-gravity default for "rigor") that June's whole methodological register works against — here it shows up as a prompt-engineering habit. It is also the same shape as several things the cyborg practice already resists: the un-normed validity geometry (refuse the master metric before reading the positions), the open scaffolds (a starter set, never a closed taxonomy), and "the question we never thought to ask" (Harding's unknown-unknowns, which no enumeration reaches).

**The balance** (not "never be specific"): pair **one maximally-open gap-finder** with a **few targeted subagents** — and let the open one carry the discovery load, precisely so the targeted ones' inevitable pre-categorization doesn't define the whole search. In the PMA session this directly recovered work a parameter-shaped extraction had silently dropped (design decisions, frameworks, whole learning loops) — none of which a "find the missing parameters" prompt would have surfaced, because they aren't parameter-shaped.

**Why this generalizes across skills**:
- **/critic-swarm**: persona prompts that pre-name the flaws to look for will find those flaws and miss the structural one; at least one persona should be open ("what's wrong here that we didn't think to ask about?").
- **/research, Explore, general-purpose subagents**: the dominant use is search-by-pre-set-category; the highest-value pass is often the open "what's here that matters?" one.
- **/discourse-analysis, /graphify**: imposing the coding/clustering frame before reading the corpus is the same foreclosure at the analysis layer.
- **Any main-agent dispatching subagents**: the manager's context is *thinner* than the corpus's; over-specifying exports that thinness as the search boundary.

**Status**: Named by June as a recurring, many-times-hit pattern; articulated cleanly here for the first time. Strong generalization. **Operational follow-up (June's open question — where it should live):** a one-line standing version belongs in the global `~/.claude/CLAUDE.md` "Subagent Coordination" section so it's enforced across projects — drafted, pending June's go (she flagged uncertainty about placement; this INSIGHTS entry is the rich articulation, the CLAUDE.md line would be the enforced operational form).

---

## 2026-08-08 — A rule lives where it is read, not where it is written; "documented" and "installed" are different states

**Surfaced in**: Job Search evidence sweep (2026-08-07/08). Found four times in one session, in four different skills, by four different routes — after which it stopped looking like a series of bugs and started looking like a structural property of skills this size.

**The insight**: In a multi-file skill, writing a rule down feels like installing it. It isn't. The executable path an agent actually traverses is narrow — its dispatch brief, the required-reading list at invocation, the stage it is currently on. **Anything outside that path is documentation, not behavior.** The gap is invisible from the authoring side, because the author can see the file and reasonably assumes an agent will too.

The four instances:

1. **ATS guidance, three homes and a false claim.** Substantive content in `PIPELINE.md` Step 4.4; the check actually executes in a `/critic-swarm` persona at Stage 4/4.5; and `printpress/SKILL.md` asserted the genre configs had *absorbed* the ATS logic. They had not — they reference PIPELINE by step number and contain none of it. An agent told "fix the ATS behavior" would have edited the genre config and changed nothing.
2. **An orphaned moves library.** `voice-check/moves/` existed since April, referenced only in `PIPELINE_REDESIGN_SPEC.md` — never in `SKILL.md`. Every craft move in it had been written and never read by any drafting agent.
3. **A category that meant "handled elsewhere," where elsewhere didn't handle it.** `williams_diagnostic_restructure` was tagged `role: linter`. The read protocol says don't read linter checks manually; the script doesn't implement it and *cannot* (the moves are model judgment, not pattern matching). Read by nobody, executed by nothing — while being the deepest compression layer in the system.
4. **The one already documented.** `printpress/SKILL.md` records that a length principle lived in `/workshop`'s `principles.md`, which Stage 2 never invokes, and "broke multiple times because the correct principle lived in the wrong file." **The system had already diagnosed this pattern and it kept happening** — which is the strongest evidence that noticing it once is not a fix.

**The test**: for any rule, name the specific file an agent reads *at the moment the rule must bind*. Not the file where the rule is best explained — the file in the execution path. If you can't name it, the rule is not installed, however well written it is.

**The fix that demonstrably works** (already in use for the seven drafting mistakes, which do get consumed): the long document lives outside; a **compressed, context-weighted restatement sits at the point of use**, with a pointer to the canonical source. Not "go read the doc" — the rules restated where they bind. Cold subagents make this non-negotiable: a dispatched agent sees only its brief, so a rule not written into the brief does not exist for the agent that writes the prose.

**The taxonomy corollary**: any status category meaning "something else handles this" is a place where things go to disappear the moment that something else stops handling them. `linter` was such a category. When adding one, ask what happens to an item filed there if the handler never runs.

**Why this generalizes across skills**:
- **/printpress**: Stage 2 dispatches genuinely cold subagents. Every binding constraint must be *in the brief*, not in the stage description the dispatcher read.
- **/voice-check**: the `role` field is an execution-path router, not a filing system. A check's role determines whether any agent will ever see it.
- **/critic-swarm**: persona files are the execution path for review; the SPEC is not.
- **Any skill with a SPEC and a SKILL**: the SPEC is where design is *explained*; the SKILL is where it *executes*. A rule that exists only in the SPEC has been designed, not shipped.
- **Anyone auditing a skill**: grep for the rule, then grep for whether anything on the execution path references the file you found it in. The second grep is the one that matters.

**Status**: Four independent confirmations in one session, one of them a repeat of a failure the system had already written down. Strong generalization; low cost to check. **Operational follow-up**: worth a standing line in the global `~/.claude/CLAUDE.md` — when modifying a skill, name the execution-path file before writing the rule — pending June's call on placement.
