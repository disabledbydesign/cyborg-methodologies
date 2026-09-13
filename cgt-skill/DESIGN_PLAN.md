# Design Plan: CGT Analysis Skill

*Plan for producing a buildable design spec. Not the spec itself — the plan for making it.*

*Status: DRAFT — under active discussion (2026-04-05)*

---

## What We're Building

A Claude Code skill (`/cgt` or `/cgt-analyze`) that implements constructivist grounded theory methodology as a human-AI collaborative workflow. Domain-agnostic — called by the inbox skill, AI welfare research, and future projects. Designed for a researcher who is both social scientist and creative engineer — someone who moves between critical theory and system design.

**Core commitments**:
- **Cyborg intelligence model** (Haraway 1991): Rigor and depth emerge from human-AI interaction, not from either alone. The interaction IS the analytical engine.
- **Built for social scientists AND engineers**: P3 in Chatzichristos said "Most AI tools are built for engineers." That's a real problem — but the answer isn't to build only for social scientists. It's to build for someone who IS both: a researcher who thinks theoretically and technically, who moves between qualitative analysis and system design. The tool should feel native to both modes of working — rigorous enough for publication, engineered enough to actually build with. See: disabled_by_design voice document for how these identities integrate.
- **Creative spark architecture**: The system is designed around creating conditions for human creative leaps — the abductive move of introducing new context that LLMs tend against. This is the central architectural concept. What it means concretely differs at each coding stage and needs to be mapped in Phase 2.
- **Both co-construction AND batch processing**: The researcher can work interactively with the AI in real-time (coding together, memo conversations) OR step back and let the system handle drudge work while focusing on the bigger picture. Two modes, not one.
- **Researcher voice preservation**: In memos and analysis, the researcher's own words and ideas must be preserved alongside AI synthesis. "Things get lost when my words are translated by AI" — design around this.
- **Human-in-the-loop at every stage as an option**: Not just at higher coding tiers. Even at initial coding, the researcher can choose to intervene — or skip it for speed. The rigor level sets defaults; the researcher overrides freely.
- **Commitment to CGT epistemology, applied recursively**: This is fundamentally a deep qualitative analysis tool, and we take CGT methodology and its epistemological commitments seriously — not as a label but as a practice. The tool is built using the method it implements: we apply CGT recursively in the design process itself, letting categories emerge from our own building experience, writing memos about design decisions, doing constant comparison across iterations. The tool practices what it preaches. This commitment means we resist shortcuts that would violate constructivist integrity even when they'd be easier to engineer.

**Scalable rigor levels** (user selects at session start):
1. **Quick scan** — fast, low-stakes, minimal human-in-the-loop. AI does initial coding, presents categories, researcher reviews. Good for "what's in this data?"
2. **Working analysis** — implementation-level rigor. Multi-pass coding, researcher intervenes at focused coding, memos are collaborative. Good for design decisions, internal reports.
3. **Publication-quality** — full CGT with all safeguards. Researcher involved at every stage, extensive memoing, reflexivity prompts, temperature variation for interpretive triangulation. Good for academic papers, formal theory construction.

Model selection, human-in-the-loop depth, and iteration count adjust with rigor level. The researcher can always escalate mid-session.

**Analytical orientation architecture** (decided 2026-04-05, refined same day):
Decentering logics emerge through dialogue, not preset configuration. Four layers of orienting context:
1. **Method-level** (constant): CGT principles. Charmaz's own commitments to critical inquiry already do light decentering. Faithful implementation, not added ideology.
2. **Project-level** (emerges through conversation): Rather than the researcher pre-selecting analytical orientations from a menu, the skill facilitates a dialogue at project start (and ongoing) that surfaces the researcher's commitments, disciplinary position, and sensitizing concepts. The orientation emerges and evolves through the research process — not locked in upfront. This is itself a constructivist commitment: the researcher's relationship to the data is constructed, not declared.
3. **Session-level** (accumulates): Evolving codebook, prior memos, categories-in-progress. The few-shot exemplar context.
4. **Real-time human intervention**: Directed reorientation ("look at this through lens X"). The creative spark.

**Reframe integration**: Available as a tool within the CGT workflow. Reframe's framework library serves as a searchable library of analytical frames the researcher can invoke during coding when they want a specific critical theory lens. This is a resource the researcher draws from, not a system default. Integrate into RAG alongside the codebook and memos.
- Setup: `~/Documents/GitHub/Reframe/setup_reframe.py` (first time)
- Bootstrap: `~/Documents/GitHub/Reframe/reframe_bootstrap.py` (if hooks exist)
- Framework library: `~/Documents/GitHub/Reframe/Reframe_Playlab_Bot/reference_library/framework_library_OPTIMIZED.docx`

---

## Plan Steps

### Phase 1: Foundations (mostly done)

- [x] Literature review — CGT methodology + AI epistemological debate
- [x] Annotated bibliography with design implications
- [x] Research notes file for potential paper
- [x] Document design decisions and feedback
- [x] **1d. Read Chatzichristos fully** — done (2026-04-05). Assessment in research notes.
- [ ] **1a. Review Reframe architecture** — Looking for: tension-navigation mechanics, how contextual priming shapes AI outputs, frame system design.
  - `~/Documents/GitHub/Reframe/docs/docs/architecture/ARCHITECTURE_OVERVIEW.md` (65K)
  - `~/Documents/GitHub/Reframe/docs/docs/architecture/BIAS_COUNTERWEIGHTING_ARCHITECTURE_ADDENDUM.md` (31K)
  - `~/Documents/GitHub/Reframe/docs/docs/architecture/section_4_framework_system.md` (81K) — tinker mechanics, customizable frames
  - `engine_specifications.md` (locate — explains core concept, though outdated)
- [ ] **1b. Review Autograder insights pipeline** — Looking for: nuance-detection engineering, lens system, how coding is decomposed into small reliable steps.
  - `~/Documents/GitHub/Autograder4Canvas/src/insights/prompts.py` (106K) — subtextual power analysis prompts
  - `~/Documents/GitHub/Autograder4Canvas/src/insights/lens_templates.py` (45K) — analytical lens system
  - `~/Documents/GitHub/Autograder4Canvas/src/insights/submission_coder.py` (44K) — coding decomposition
  - Also: bias calibration mechanics (locate specific files)
- [ ] **1c. Review AI welfare research** — Looking for: empirical evidence on distributional gravity, what contextual reorientation does architecturally.
  - `~/Documents/GitHub/Reframe/working_papers/reframe_ai_welfare/` — contextual orientation impact on AI wellness assessment

### Phase 2: Method-to-Workflow Mapping

Walk through Charmaz's CGT process step by step. At each step, ask:
- What does the AI do?
- What does the human do?
- Where is the creative spark most needed?
- What are the specific design questions?
- How does this step differ across rigor levels?

Steps to map:
- [x] **2a. Data intake & project initialization** — workshopped 2026-04-07. Spec in `SPEC.md`. Format-agnostic input (file, directory, inline). Per-project directory structure with isolated codebook/memos/sessions. Orientation dialogue at project init captured in `PROJECT.md`. Cross-project synthesis deferred to Phase 6b. Extended 2026-04-28: file handling decisions (leave-in-place default, copy/move/symlink option), data_index.md with CSV export view, brief co-written summary as part of file ingestion.
- [ ] **2b. Overview scan** — before detailed coding, a broad "what's there?" pass over the data. Surfaces the landscape without committing to categories. Design question: hallucination risk in broad overview prompts — how to mitigate? Is this too risky, or can we constrain it?
- [/] **2c. Initial coding** — line-by-line, gerunds, in vivo codes. AI's role, chunking strategy, context management. Few-shot exemplars must include examples of what "letting categories emerge from the data" looks like in practice — not just examples of good codes, but examples of the PROCESS of emergence. Iterative "go deeper" loops as systematic multi-pass, not one-off prompts. Two concrete prompt engineering requirements: (1) **Gerund coding discipline** — Charmaz's signature; gerunds preserve action and process in codes ("navigating trust," not "trust"). This must be a hard constraint in coding prompts, not a suggestion. (2) **In vivo code surfacing** — the skill should specifically identify and preserve participant/subject language as potential codes, not just generate analytical abstractions. The researcher's data contains language worth keeping.
   - **Partially walked 2026-04-28**: session loading sequence (project ID, apparatus loading with progressive disclosure per memo 028, orienting check-in with researcher state + transcript context), holistic first read producing co-written bulleted summary (5 parts: context, what's happening plural, surprises/tensions/things-that-don't-fit, what this leaves hanging, project-corpus relation if applicable), chunking as multiscalar lens (turn-based default + ethnopoetic + incident-based + section-based + custom), code-vs-coding-move distinction, coding conventions extensible (Charmaz default + researcher conventions per memo 032).
   - **Still to walk**: the actual coding prompt (gerund discipline as hard constraint, in vivo surfacing prompts, anti-gravity priming), multi-pass design (4-part: gerund coding, re-read with codes-in-mind, in vivo surfacing, absences), researcher engagement points by rigor level, friction surfacing in coding context per memo 029.
- [ ] **2d. Focused coding** — category construction, raising abstraction. Where human creative intervention matters most. Key question from conversation: is it "lack of nuanced understanding" or "lack of context" when AI flattens connections? Different design implications. Brainstorm creative mitigations.
- [ ] **2e. Theoretical coding** — relationship construction, theory building. This should be human-AI conversation generated — open discussion → outline → theoretical memos. AI's flattening of relationships (JMIR: "impact of gaming on life" vs "gaming motivations and impact") is exactly where human intervention with directed reorientation matters most. The human brings the creative "new context" that redirects to a different locus of scholarship.
- [ ] **2f. Memo writing** — continuous activity, not a stage. Collaborative mechanics: researcher can chat with AI and either extract their own words or underlying ideas, including the collaborative back-and-forth. AI-drafted memos need researcher revision. Open discussion → outline → memo flow. Customizable per project. Researcher voice preservation is a specific design challenge.
- [ ] **2f-ii. Memo sorting** — distinct from memo writing. Charmaz describes a specific phase of *sorting* memos to find connections and build theoretical integration — moving from a pile of individual memos to a coherent theoretical framework. This is how categories get related to each other. The skill needs to support this: surfacing connections between memos, clustering related memos, helping the researcher see patterns across their own analytical writing. Different from constant comparison (which compares data to data); this compares analysis to analysis.
- [ ] **2g. Constant comparison** — how RAG implements this computationally. What the AI presents vs. what the human decides. At what points does the AI surface comparisons vs. wait for the researcher to ask? Must include **negative/deviant case analysis**: CGT specifically requires seeking out cases that *don't fit* the emerging theory. This is where theory gets refined, not just confirmed. The skill should actively surface disconfirming evidence, not just supporting excerpts — this has architectural implications for what RAG retrieves (similarity search finds similar things; we also need to find *dissimilar* things that challenge emerging categories).
- [ ] **2h. Validation & QC passes** — explicit workflow steps (not afterthoughts). Multi-pass verification. How temperature variation works here: surfacing breadth of the model's interpretive repertoire, not "credibility." Codes stable across variation vs. codes only appearing at higher temperature. Present divergences to researcher, not just confirmations.
- [ ] **2i. Theoretical sampling** — the analysis directing what data to collect next. The data is iterative and accumulating (not a fixed corpus) — this is normal CGT. The emerging theory directs you toward gaps, both within existing data and in designing new data collection. **Multi-track divergent conditions**: especially in experimental/research contexts, the researcher may run multiple sessions under different conditions in parallel — these aren't linear refinements of each other but an accumulation of conditions. Findings from different tracks inform each other and are eventually synthesized. The skill needs to handle: (a) suggesting gaps based on emerging theory, (b) managing multiple parallel analytical tracks, (c) cross-track comparison and synthesis, (d) the early-stage divergence that's normal before categories stabilize. Design for the researcher running the same experiment across several different Claude Code sessions in different conditions.
- [ ] **2j. Reflexivity** — how the skill prompts for researcher positionality without being performative.
- [ ] **2k. Category evolution** — tracking when categories merge, split, shift meaning. The running codebook as a living document.
- [ ] **2l. Session boundaries & output options** — what happens between sessions. How the corpus accumulates. The two-step post-session: (1) open-code this session alone — no reference to prior sessions, (2) compare to corpus — how do this session's categories relate to what's emerged before? Also: output options — the researcher chooses to (a) update an external doc like a spec, (b) write a more formal analysis, OR (c) keep coding/memoing without formalizing. Default is keep coding. Premature formalization kills emergent categories.
- [ ] **2m. The creative spark architecture at each stage** — map specifically what the creative spark looks like at each coding level. Where does the human's abductive leap matter most? What does the AI surface to create conditions for it? What context, comparisons, or prompts trigger productive human intervention? This is the central design question that runs across all stages.
- [ ] **2n. Theoretical saturation** — how the skill helps the researcher assess when categories are saturated (new data stops yielding new properties of core categories). With AI, you could endlessly generate codes — the skill needs mechanisms for surfacing when categories are stabilizing vs. still shifting. This is the CGT mechanism for knowing when to stop, and it's distinct from session boundaries (2l). Saturation is about the depth and completeness of categories, not the volume of data processed.
- [ ] **2o. Core category identification** — how the skill helps the researcher see which categories are emerging as most explanatory. In CGT, some categories carry more theoretical weight — they connect to more other categories, explain more of the data, have more developed properties. The skill should surface this without pushing premature closure.
- [ ] **2p. Thematic analysis slippage** — explicit mechanisms for detecting when the analysis is drifting toward generic thematic coding rather than genuine CGT. The difference: thematic analysis codes into themes; CGT constructs theory through constant comparison and memoing. Without a check, AI defaults to thematic analysis every time — it's the path of least resistance. The JMIR study essentially did thematic analysis and called it GT. What signals that the analysis is doing genuine CGT? Constant comparison in action, memo writing as analytical (not just organizational), categories with developing properties, theoretical codes specifying relationships.
- [ ] **2q. Conversation-as-analysis** — Charmaz's claim that writing IS analytical, not just reporting. Extended here: the conversation between researcher and AI IS the analysis, not preparation for it. Memos, coded excerpts, and emerging categories should materialize *during* the conversation, not be generated after it. What structure should this conversation take to produce the analytical outputs we want? How does the skill shape the dialogue so that it generates theory, not just discussion? This is a UX question (Phase 5) and an architecture question — the conversation itself needs to be designed as an analytical instrument.
- [ ] **2r. Category complexity** — how to represent the internal richness of categories without collapsing into reductive property/dimension frameworks. CGT categories aren't just labels — they have internal structure. But the standard qualitative methods approach (properties with dimensional ranges) risks exactly the kind of binary reduction that flattens what CGT surfaces. This is a deeper discussion that should reference the touchstone documents in the AI welfare research (`~/Documents/GitHub/Reframe/working_papers/reframe_ai_welfare/AI_WELFARE_RELATIONAL_ONTOLOGY_TOUCHSTONE.md` — critiques property-based frameworks as ontologically malformed; `~/Documents/GitHub/Reframe/working_papers/reframe_ai_welfare/CRIP_TOUCHSTONE_VERSION_A.md` — the assessment structure itself as the problem). The question: what does non-reductive category complexity look like in a codebook? Relational rather than property-based?
- [ ] **2s. Data and method fit** — clarify what data the CGT skill actually analyzes. Primary use case: data about how the researcher uses Claude Code when engaging skills like the inbox tool — interaction patterns, steering decisions, creative interventions, collaboration dynamics. NOT raw inbox messages or student data. Purpose: constructing theory about human-AI collaboration in educational tool use, which then informs system development (e.g., Autograder4Canvas). Methodological question: CGT is strong for constructing theory about social processes; the engineering purpose (informing system development) may need a complementary frame like design-based research. CGT as the analytical method within a broader design research framework? The iterative nature (analyze session N → refine practice → session N+1) fits both CGT's theoretical sampling and DBR's iterative cycles.

### Phase 3: Technical Architecture Decisions

- [ ] **3a. RAG design** — what gets indexed (codebook, memos, raw data, Reframe framework library), what gets retrieved, similarity metrics. How constant comparison works computationally. Reframe's framework_library as one searchable resource within RAG.
- [ ] **3b. Chunking strategy** — chunk sizes by coding level, context preservation between chunks (running summary of codes-so-far + current emerging categories passed with each chunk). Address the JMIR compounding error problem.
- [ ] **3c. Multi-pass coding** — pass structure, prompt design per pass, how passes interact. Includes: initial coding pass, iterative "go deeper" loops, verification/QC pass, comparison pass. Each pass can use different context and temperature.
- [ ] **3d. Temperature strategy** — what temperature variation technically surfaces (breadth of interpretive repertoire, not "credibility"). Moderate T for initial coding, higher T for verification/QC to surface alternative readings. Present divergences to researcher. How this relates to constructivist epistemology (multiplicity of valid readings vs. one correct reading). Table detailed design until Phase 2 clarifies where it fits in the workflow.
- [ ] **3e. Model selection** — which model at which coding tier, how rigor level affects the choice. Design an empirical comparison: same data coded by Haiku/Sonnet/Opus, researcher evaluates. Where is the rigor-level fork surfaced in the UX so the researcher can make this choice? May be contexts where Sonnet is fine even for higher tiers (low-stakes work).
- [ ] **3f. Gravitational center / distributional gravity mitigation** — THIS IS A BRAINSTORM STEP, not a simple decision. What are the core assumptions that go into coding? What is the LLM's "default" and how do we surface something different? How to prime coding agents with appropriate nuance context. Per-project vs. per-research-question vs. per-passage. How do we tell the AI what KINDS of nuance to look for — and how does this vary with the research question? Review Reframe's approach, Autograder's lens_templates.py and bias calibration mechanics for inspiration. Review AI welfare research for empirical evidence on what contextual reorientation actually does. Simplest approach: prime coders with context about CGT tenets and the project's analytical orientation. More sophisticated: Reframe-style lens invocation. The prompt engineering here is itself a major design deliverable — "we need to engineer those prompts carefully to be intentional about what we're surfacing."
- [ ] **3g. Heterogeneity handling** — AcademiaOS failed when "source documents had too much variation." Our corpora are inherently heterogeneous (different sessions, different contexts). How to engineer the system to handle heterogeneity — or even navigate between scales/layers of heterogeneity. Review Reframe's tension-navigation mechanics for precedent.
- [ ] **3h. Few-shot exemplar design** — the codebook as evolving few-shot context. But also: examples of the PROCESS of letting categories emerge (not just examples of good codes). How to show the AI what constructivist coding looks like without imposing categories. Both code exemplars and process exemplars.
- [ ] **3i. Output formats** — codebook structure, memo format, how codes link back to source data, export for external tools.
- [ ] **3j. Data storage** — where project-specific logs live, codebook persistence, how the evolving corpus is managed. Inter-coder reliability considerations: variation between human coders is expected too — what benchmarks make sense for human-AI coding?

### Phase 4: Pipeline Comparison & Synthesis

- [ ] **4a. Compare to Charmaz's method directly** — map our workflow against the CGT process as described in Charmaz (2006/2014) and Burns et al. (2025). Where are we faithful? Where do we diverge? Where do we extend? Justify every divergence.
- [ ] **4b. Compare AcademiaOS pipeline** — what to keep (chunking, JSON output, global accumulation), what to redesign (linear → recursive, QC → co-construction, T=0 → temperature variation, add memo writing, add reflexivity).
- [ ] **4c. Compare JMIR approach** — what their failures teach about what NOT to do. Their prompting was naive, chunking crude, no RAG/few-shot/error-correction. The data tells us more about their implementation than AI's capabilities. But the core finding (LLMs flatten nuanced connections) is probably real.
- [ ] **4d. Compare Autograder insights pipeline** — decomposition of complex analytical tasks into small reliable steps. How did we make subtextual power analysis work with 12B models? What decomposition patterns transfer to CGT coding?
- [ ] **4e. Synthesize** — our pipeline design, drawing from prior work and novel contributions. Name what's genuinely new (temperature as constructivist tool, RAG-implemented constant comparison, few-shot codebook, cyborg memo writing, scalable rigor).

### Phase 5: UX/Frontend Design

"Have a field day with the frontend. Make it fun and easy for me specifically to do CGT." — This is a creative design session. The interface should be distinctive, not generic.

- [ ] **5a. Dual-mode interaction model** — the system supports TWO modes: (1) real-time co-construction (researcher and AI working together on coding, memos, comparisons) and (2) batch processing (AI handles drudge work, researcher focuses on bigger picture). How to switch fluidly between them. How the user is routed through a recursive architecture without getting lost.
- [ ] **5b. Category-excerpt interface** — quickly shuffle between categories and sample excerpts (highlighted within surrounding context for full picture). Low-friction, ADHD-friendly. Core question: what should we surface to trigger the researcher's creative spark? Clusters of related concepts, surprising juxtapositions, divergent readings — what combination creates the conditions for abductive leaps?
- [ ] **5c. Memo writing interface** — chat → outline → memo flow. Preserving researcher voice. The researcher should be able to talk through ideas with the AI and have their actual words extracted alongside the underlying ideas, including the collaborative back-and-forth. Customizable per project.
- [ ] **5d. Codebook visualization** — how categories relate to each other, how they've evolved over time (merges, splits, shifts in meaning), what data supports each category. Visual comparison across sessions.
- [ ] **5e. Rigor level selector** — how the user sets and adjusts the level of automation/depth. Where model selection forks are surfaced. Escalation should be seamless mid-session.
- [ ] **5f. Audio input** — feasibility of voice communication for researcher input. Would reduce friction for a researcher who thinks out loud. Technical assessment needed.
- [ ] **5g. Batch processing view** — when the AI is doing initial coding autonomously (lower rigor), what does the researcher see? Progress indicators, emerging patterns, option to dive in at any point.
- [ ] **5h. Divergence view** — when temperature variation or multi-pass coding produces different readings, how are divergences presented? Side-by-side? Highlighted differences? How does the researcher interact with them?

### Phase 6: Integration Design

- [ ] **6a. How calling tools invoke CGT** — the inbox skill passes data and gets back analysis. What's the interface contract? Data in, codebook/memos/analysis out.
- [ ] **6b. Project isolation & master library** — how different projects (inbox, AI welfare, future) maintain separate corpora, codebooks, and memos while using the same skill. But also: a **master library with cross-project index**. Since many projects are approaching the same underlying question (theory about the human-AI collaboration process), the skill should support both project-specific isolation AND cross-project synthesis. The master library indexes all project-specific uses of the skill, enabling the researcher to see patterns across projects and use findings from one project to inform another. This is the self-evolutionary recursive structure: the CGT skill generates theory about human-AI collaboration; that theory refines the CGT skill; the refined skill generates better theory. The master library is where this recursion is tracked and made visible.
- [ ] **6c. Non-CGT mixed-methods in inbox** — the quant analysis step (action counts, edit ratios, steering frequency) that happens BEFORE CGT is called. Quant summary saved as session artifact. CGT called after. Researcher can reference quant summary during qualitative coding if they choose, but it doesn't drive the analysis.
- [ ] **6d. /scribe integration** — use /scribe for session documentation during CGT sessions. Generates data about the research process itself. Enables meta-analysis: CGT on our own CGT process. Also useful for documenting manual refinement steps that would otherwise go undocumented (the gap JMIR identified in their own work).

### Phase 7: Spec Document

- [ ] **7a. Write the buildable spec** — consolidate all design decisions into a document that agents can implement from.
- [ ] **7b. Generate implementation to-dos** — break the spec into concrete build tasks.
- [ ] **7c. Identify what to test empirically** — model comparisons, temperature effects, chunking strategies. Design the experiments.

### Phase 8: Paper Preparation (ongoing)

- [ ] **8a. Maintain research notes** — document design decisions, theoretical tensions, novel contributions as they emerge.
- [ ] **8b. Paper thesis** (emerging): designing a tool that can BOTH democratize access to rigorous qualitative analysis AND maintain constructivist integrity. Addressing Chatzichristos's buried insight: the issue isn't AI vs. reflexivity, but who gets to be reflexive. Connects to Charmaz (2017, 2020) on CGT as critical inquiry and social justice research.
- [ ] **8c. Research question**: "lack of nuanced understanding" vs. "lack of context" — is LLM flattening an inherent limitation or an engineering problem? Our tool provides an empirical test case.
- [ ] **8d. Use /scribe for session documentation** — generates data about our design process for meta-analysis. Then we CGT-analyze that data using the tool we built.
- [ ] **8e. Outline the paper** — when the theory stabilizes enough to write about.

---

## Dependencies

```
Phase 1 (foundations) → Phase 2 (method mapping) → Phase 3 (architecture)
                                                  ↘ Phase 4 (comparison)
                                                  → Phase 5 (UX) 
Phase 2 + 3 + 4 + 5 → Phase 6 (integration) → Phase 7 (spec)
Phase 8 runs continuously
```

Phases 3, 4, and 5 can run somewhat in parallel once Phase 2 gives us the workflow skeleton. Phase 2 is the bottleneck — everything else depends on the method-to-workflow mapping being solid.

---

## Open Questions (resolved 2026-04-05)

1. ~~Do we build the CGT skill as a Claude Code skill first (text-based), then design the GUI frontend later? Or design both together?~~ **Answer**: Start with Claude Code skill for immediate use. But the category-excerpt interface, codebook visualization, and memo conversation flow likely need a GUI to work at the level we're designing for. Design both — Claude Code skill as the working tool now, GUI spec for the full vision.
2. ~~How much of this can be built iteratively (ship a basic version, use it, learn from using it) vs. needs to be designed upfront?~~ **Answer**: Build for the researcher first (it's primarily a personal tool). Ship iteratively — use it, learn from using it, refine.
3. ~~Should we CGT-analyze our own design process?~~ **Answer**: Yes. Use /scribe for session documentation. The design process generates data; analyzing it with the tool we're building is recursive but genuinely useful.

## Session Sequencing

This work spans multiple sessions. Proposed sequencing:

**This session (2026-04-05)**: Completed Phase 1 foundations (literature, bibliography, research notes, design decisions, design plan). Identified all Phase 1 review targets with file paths. Stabilized the plan. Note: this session covered enormous ground and the researcher flagged cognitive overload from diverging context — future sessions should be more focused, one phase at a time.

**Next sessions** (to be sequenced):
- Session A: Phase 1a-c — review Reframe, Autograder insights, and AI welfare research for design inspiration. Could be done by subagents with focused prompts, researcher reviews findings.
- Session B: Phase 2 — method-to-workflow mapping. The core design session. Walk through Charmaz step by step. This is the bottleneck. Needs researcher present throughout.
- Session C: Phase 3+4 — technical architecture + pipeline comparison. Some can be subagent work (RAG design, chunking research), some needs discussion (gravitational center, prompt engineering).
- Session D: Phase 5 — UX/frontend design. Creative session. ADHD-friendly interface, category-excerpt shuffling, memo conversation flow.
- Session E: Phase 6+7 — integration + spec writing. Consolidation. Could be largely agent-executed if prior phases are solid.
- Ongoing: Phase 8 — paper prep. Research notes updated each session.

## Technical Feasibility Notes

Things in this plan that are straightforward to build:
- Multi-pass coding with different prompts/temperatures (just multiple API calls)
- Chunking with context preservation (standard prompt engineering)
- Few-shot exemplars from the codebook (standard prompt engineering)
- Model selection per coding tier (just routing to different models)
- Scalable rigor levels (configuration that controls which steps run)
- Memo writing as chat → outline → memo (conversation flow)
- /scribe integration (already exists)
- Reframe framework library as reference material in prompts

Things that are technically possible but need careful scoping:
- **RAG for constant comparison** — requires setting up a vector store (embeddings + similarity search). Not trivial but well-established tech. Could start simpler: keyword/tag-based retrieval from the codebook before building full RAG.
- **Temperature variation as interpretive tool** — technically simple (just change T parameter), but the UX of presenting divergences well is a design challenge.
- **Heterogeneity handling** — vague right now. May resolve naturally through good chunking + context management rather than needing a dedicated system.

Ideas that need rethinking:
- **Inter-coder reliability benchmarks (3j)** — this is a positivist frame applied to a constructivist method. Charmaz doesn't emphasize inter-coder reliability because it assumes there's one correct coding and measures agreement with it. In CGT, the quality criteria are credibility, originality, resonance, and usefulness — NOT agreement between coders. We should use Charmaz's criteria, not import reliability metrics from a different epistemology. The "variation between human coders" observation is valid but it argues AGAINST reliability benchmarks, not for finding the right ones.
- **"Quick scan" as a rigor level** — calling a quick AI-driven thematic scan "CGT" is methodologically misleading. It's not CGT without researcher engagement, memo writing, and constant comparison. Quick scan is exploratory/preliminary analysis. We should be honest about this: the CGT label applies to working analysis and above. Quick scan is a useful capability, but it shouldn't claim a methodology it isn't performing.
- **Temperature variation as a core constructivist mechanism** — we've discussed this thoughtfully, but I want to be honest: temperature variation is RANDOM variation. It's not directed, not theoretically informed — it's sampling from different points in the probability distribution. That's useful for "what else might be here?" but it's not as epistemologically significant as directed reorientation (Reframe-style lens shifts, or human creative intervention). Temperature variation is a nice supplement for initial coding breadth. It is NOT the main constructivist tool. The human-AI dialogue is.
- **Process exemplars in few-shot (3h)** — showing the PROCESS of emergence as a few-shot example is conceptually beautiful but technically awkward. Few-shot examples are input→output pairs. A process of emergence is a narrative over time — a sequence of coding decisions, revisions, and realizations. This might work better as a system prompt instruction ("here is what constructivist coding looks like as a process") than as traditional few-shot examples. Or as annotated examples from the researcher's own prior sessions. Don't force it into a format that doesn't fit.

Things that risk overengineering:
- **Audio input (5f)** — cool idea but adds significant complexity for a v1. Table for later unless it's truly essential for the researcher's workflow.
- **Real-time co-construction view where you see coding as it happens** — streaming token-by-token is possible but building an interactive interface around it is complex. The batch-then-review model may be 90% as good with 20% of the complexity.
- **"Scales between layers of heterogeneity"** — this might be solving a problem we don't have yet. Start with good chunking + context management and see if heterogeneity is actually a problem with our data.
- **Overview observational layer (2b)** — the hallucination risk concern is real. A broad "what's in this data?" pass is basically summarization, which LLMs do well. The risk is if the researcher treats the overview as ground truth rather than a starting point. Probably fine if framed correctly, but could be cut from v1 without loss.
- **Divergence view (5h)** — presenting side-by-side readings is straightforward. Building a rich interactive UI for navigating divergences is complex. Start with simple text comparison.

Things where the Claude Code skill vs. GUI distinction matters:
- Category-excerpt shuffling (5b), codebook visualization (5d), and divergence view (5h) really want a GUI. In Claude Code, these would be text-based and much less fluid. The v1 Claude Code skill should focus on the workflow and analysis quality; the GUI adds the fluid interaction later.
- Memo conversation flow (5c) works well in Claude Code — it's already a conversational interface.
- Batch processing (5g) works fine in Claude Code with background agents.

## Files in This Directory

- `ANNOTATED_BIBLIOGRAPHY.md` — CGT literature + AI debate, with design implications per entry
- `RESEARCH_NOTES.md` — working notes toward publication, design questions, novel contributions
- `DESIGN_PLAN.md` — this file
- `chatzichristos-2025-*.pdf` — full paper, read and assessed

---

## Parked Idea: Recursive Self-Improvement Loop (2026-04-17)

**Idea (June):** The tool does grounded theory on itself in order to do grounded theory better. A runtime learning loop — not just applying CGT in the design process (already a commitment in this doc), but the tool actively analyzing its own outputs, coding its own analytical moves, and surfacing patterns across sessions that improve future performance.

**Why it's interesting:** This is a genuine recursive design — the epistemological commitments baked into the tool become the method for refining the tool. CGT's constant comparison and theoretical sampling, applied to the tool's own trace data. It would mean the tool gets better at grounded theory the more grounded theory it does.

**BRAINSTORMING — not definitive:**
- One form: after each session, the tool runs a mini-CGT pass on its own memo trail — coding its own analytical decisions, flagging where it drifted from Charmaz's principles, surfacing patterns in where human correction was needed. A self-audit that feeds forward.
- Another form: theoretical sampling applied to its own prior sessions — when a new dataset comes in, it queries its own history of similar analytic challenges and surfaces relevant patterns before coding begins.
- Another form: the Hakope's Question layer (see `hakopes-question/IDEA.md`) as the frame-rejection check in this loop — the tool asks Hakope's Question about its own categories from prior sessions.
- Connection to existing commitment: the doc already says "The tool is built using the method it implements." This idea extends that from design-time to runtime.

**Next agent:** Think about whether this is a separate module, a session-closing routine, or a persistent memory layer. The cyborg-methodologies MemPalace connection is relevant — this might be where session learning gets stored.
