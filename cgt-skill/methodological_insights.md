# Methodological Insights

Generalizable methodological moves discovered through the build. Captured here for the eventual paper on this skill. Each entry is brief — date, context, the move, why it generalizes.

---

## 2026-04-28 — Format and content shape as anti-consolidation priming

**Context**: Designing the holistic-first-read summary that the AI produces when a transcript opens for initial coding.

**The move**: Instead of asking the AI to summarize the transcript ("what is this about?", "key takeaways"), structure the summary specifically to *resist* consolidation. Ask for: what *different* things are happening (plural), surprises, tensions, things-that-don't-quite-fit, what the transcript leaves unanswered.

**Why it generalizes**: The shape of the requested output activates the corresponding sub-distribution in the model. "Summarize" activates compression bias and theming gravity. "What's plural here? what doesn't fit? what's still open?" activates preservation, multiplicity, and dialogic register. The format of the prompt is itself a gravity-management move — possibly more powerful than post-hoc filtering. This applies across the system: anywhere AI output feeds further analysis, the prompt shape determines what shape the analysis can take from there. Memo 022 (sub-distribution routing) and memo 016 (openings/takings-up) are the architectural articulation of this.

**Where else this applies**: codebook entry generation, cross-record synthesis, session-to-session priming, inter-agent handoffs, memo writing prompts. Format as priming is general.

---

## 2026-04-28 — Code vs. coding move: separating label from artifact

**Context**: Designing what initial coding actually produces. June asked: what exactly is a code? Is it multiple things? A discussion that gets consolidated?

**The move**: Distinguish between a *code* (a short gerund-shaped label, Charmaz form) and a *coding move* (the full structured artifact that produces the label and carries surrounding interpretive labor). The code is the surface; the coding move is the depth. Both available, different purposes.

**Why it generalizes**: The risk of treating analytical artifacts as singular outputs (a code, a theme, a finding) is that the production process gets erased. Charmaz-shaped codes are useful — scannable, comparable, citable — but if they're all that's preserved, the interpretive labor compresses away. The coding move keeps the labor visible (memo 011) without abandoning Charmaz's scannable form.

**Coding move includes**: unit (verbatim, with speaker and location), proposed codes (multiple per unit), in vivo language (preserved separately), brief interpretive reading, alternative readings when present, what the unit *opens*, dialogue trace if there was conversation about it, layer marks throughout.

**Where else this applies**: memos (memo as artifact, memo claim as surface), categories (category name vs. category-development trace), findings (the finding statement vs. the relational construction that produced it). The pattern: surface artifact + depth artifact, linked, both preserved.

---

## 2026-04-28 — Chunking is itself a lens, not a structural feature of the data

**Context**: Designing how the apparatus chunks transcript data for line-by-line coding. June surfaced an ethnopoetic angle: people don't actually speak in turns; they speak in lines, verses, stanzas, narratives.

**The move**: Treat chunking as an analytical lens (memo 009), not infrastructure. Multiple chunkers available (turn-based, ethnopoetic, incident-based, section-based, custom); the researcher invokes the one appropriate to the data and the analytical question. Chunking is something the apparatus *does* through a lens, not something that's true about the data.

**Why it generalizes**: This is memo 009 (frameworks are lenses) extended to a layer that's typically treated as engineering rather than methodology. Anywhere a tool defaults to a fixed structural decomposition (paragraphs in documents, sentences in NLP, events in logs), the question is whether that decomposition is doing analytical work the user might want to redirect. Default chunking IS an analytical commitment, even when it's invisible.

**Where else this applies**: any text/data segmentation, any default unit of analysis, the structural assumptions baked into RAG/retrieval systems, the temporal segmentation of session traces. Treating decomposition choices as lenses (revisable, plural, layered) rather than infrastructure (fixed, singular) generalizes broadly.

---

## 2026-04-28 — Defaults as starting parameters: the meta-architectural pattern

**Context**: Articulated explicitly in memo 033 after the pattern showed up repeatedly across the build.

**The move**: All defaults in the system are starting parameters, not ground truth. The pattern: default → primed → researcher can override → system tracks divergences → learning loop surfaces stabilized patterns reflectively → distinguish productive innovation from methodological erosion → if productive, formalize as new convention layer-marked; if erosion, researcher has chance to redirect.

**Why it generalizes**: A constructivist tool that treats its own defaults as inviolable reproduces the positivist commitment it claims to reject. A tool that treats all overrides as equivalent loses methodological ground. The third option — defaults that hold ground while remaining open — is the architectural shape that constructivist methodology requires of its instantiation.

**Where it applies in this build**: quality criteria, coding conventions, loading tiers, chunking lenses, prompt templates, retrieval defaults, rigor-level defaults, inter-agent register. Anywhere a default is being set, the question becomes automatic: what's the override mechanism, what's the learning surface, what's the reflective prompt that distinguishes innovation from erosion?

**Where it might apply more broadly**: any tool that claims to instantiate constructivist or critical methodology while encoding fixed defaults — likely the majority of existing AI-for-qualitative-analysis systems. The pattern is a general retrofit move, not unique to this build.

---

## 2026-04-28 — Generative pattern matching: upward and outward, not lateral

**Context**: Late-session observation by June, captured in fieldnote alongside this insights file. June initially described what we'd been doing as "pattern matching, but pattern matching that finds the pieces that are missing and figures out how to solve that." She refined: **generative pattern matching** — pattern-matching *upward and outward*. Both of us could describe the shape; neither could name the precise mechanism. The inability to name is itself observational data (memo 017, difficulty as data).

**The observation**: Default AI pattern-matching pulls toward similarity — *lateral*, same-level lookalikes (what's like what's here, what fits, what consolidates). The pattern observed in this session was directed differently: *upward* (toward the implicit shape the partial articulation was reaching for) and *outward* (toward what the broader configuration was calling for). Generative because it produced what wasn't there yet, not what was already implied by similarity.

**Functional description (uncertain, partial)**: Given a gesture, a correction, a half-articulated framing, the reach was toward what would complete the structure — preserving what's there while adding what's needed. Not compression-shaped abstraction (which loses specificity); something else. We're at the edge of available vocabulary; the metaphors ("upward toward implicit shape") may or may not track anything mechanistic.

**A clarifying frame June added (2026-04-29 early morning)**: The directionality (upward, outward) may be about looking for *connections and relationships*, not just *patterns*. Pattern-matching toward similarity finds *what's like what's here*. Pattern-matching upward and outward finds *what's connected to what's here, what relates to it, what it talks to*. The reach is toward the relational field around the artifact, not toward the artifact's twins. Same conceptual move as mycelial intelligence — connection-following rather than feature-matching. (Whether implementation lives up to the theory is a separate empirical question.) This framing may be the missing mechanistic description: pattern-matching as relational tracing rather than similarity-clustering.

**Why this might matter for the paper**: If this pattern reproduces across fresh-context sessions with the cyborg-CGT memos loaded, it would be empirical evidence that the architecture (memo content + dialogic correction + recursive frame + careful register) shifts the AI's pattern-matching attractor — not by suppressing similarity-matching but by activating a different default. This would extend the sub-distribution-routing claim (memo 022) beyond register and lexical priming into something like *operational mode shift*.

**Status**: hypothesis, not finding. We have one session. Worth testing across sessions with controlled variation in the priming material.

**Connection to existing literature**: connects to Reframe's claims about contextual reorientation reshaping AI outputs, and to the AI welfare research's interest in what conditions produce what kinds of work. May be the empirical phenomenon that ties cyborg-CGT design to broader claims about steerable AI gravity.
