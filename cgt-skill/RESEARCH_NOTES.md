# Research Notes: AI-Powered Constructivist Grounded Theory

*Working notes toward a potential publication. Documenting design decisions, theoretical tensions, and novel contributions as they emerge.*

*Started: 2026-04-05*

---

## Core Thesis (emerging)

AI tools for qualitative analysis are widely described as inherently positivist (Chatzichristos 2025). But this conflates the epistemology of current implementations with the epistemology of the technology itself. Automation is a method of production; positivism is an epistemological commitment. A tool designed around constructivist principles — recursive iteration, researcher reflexivity, co-constructed meaning — can support rigorous CGT without the positivist drift.

The key design move: rigor and depth emerge from **human-AI interaction**, not from either alone. This is a cyborg intelligence model (Haraway 1991), not an automation model. The researcher is a disabled trans social scientist who can "engineer designs based on fundamentally different orienting assumptions" — the lived experience of navigating systems not designed for you IS the design expertise.

## The Democratization Argument

Chatzichristos (2025) almost catches this: the generational divide in AI adoption may reflect resource inequalities, not epistemological naivety. Experienced researchers who champion reflexive depth may be privileged enough to do it (funding, tenure, time, established teams). Early-career researchers gravitate to AI for practical survival.

**Our design target**: a tool that makes deep reflexive qualitative analysis accessible to researchers who don't have the privilege of unlimited time and institutional support — without sacrificing methodological rigor. Democratizing reflexivity, not automating it away.

This directly connects to Charmaz's (2017, 2020) argument that CGT is a tool for critical inquiry and social justice research. A CGT tool that's only usable by well-resourced researchers undermines that commitment.

## Chatzichristos (2025) — Critical Assessment

**What he measures**: Researchers' attitudes toward AI tools (TAM survey, n=93, European sample; 15 semi-structured interviews).

**What he claims**: AI may push qualitative research back toward positivism.

**The gap**: He's making a sociological argument about adoption patterns and presenting it as if it were an ontological argument about AI's nature. His TAM framework is itself positivist (he acknowledges this), creating circularity — his instrument for measuring the positivist turn is positivist.

**What holds**: Participant quotes about nuance, cultural subtext, and relational engagement describe real limitations of *current* tools. But these are descriptions of how existing tools work, not proofs that tools can't be designed differently.

**The buried insight (p.9-10)**: The critique of the "positivist turn" might reflect "the elitist and male-dominated perspectives of those critiquing it." This suggests a third reading that Chatzichristos doesn't develop: the issue isn't AI vs. reflexivity, but *who gets to be reflexive*.

## JMIR (2025) — What Their Data Actually Shows

Their prompting strategy was naive (basic chunking, no RAG, no few-shot, no codebook priming, "delve deeper" as the only iteration strategy). Their comparison methodology has gaps (one hallucination example documented, inflated agreement from uncoded text, unclear inter-rater reliability for evaluators).

**What's real**: LLMs flatten nuanced connections at higher coding levels. The hallucination they document (inferring psychological meaning not in the text) is a context overwhelm artifact, not an inherent limitation.

**What's an implementation artifact**: The axial coding failures may be more about their crude chunking and lack of context management than about AI's capabilities.

**Reframe**: "Lack of nuanced understanding" vs. "lack of context" — same impact (drift), but different design implications. If it's context, we can engineer mitigations.

## AcademiaOS (2024) — Architecture Critique

Uses Gioia method (linear pipeline) while claiming constructivist epistemology. Key contradictions:
- Optimized for reproducibility (T=0) — a positivist value
- No memo writing, no reflexivity prompting
- Linear stages with no recursion back to earlier data
- Doesn't address gravitational center / training data bias
- Human-in-the-loop is quality control, not co-construction

**What to keep**: Chunking strategy (10k chars + overlap), JSON output structure for codes, the idea of accumulating results into a global array.

**What to redesign**: Everything about the epistemological architecture. Replace linear pipeline with recursive process. Add memo writing. Add reflexivity. Replace QC-style human review with genuine co-construction.

## Novel Technical Contributions (emerging)

1. **Temperature as a constructivist tool**: Using temperature variation to generate alternative readings as part of the analytical process, rather than optimizing for reproducibility. Codes stable across temperature = one kind of evidence; codes that only appear at high temperature = emergent readings worth researcher attention. (Need to think more carefully about what this actually surfaces — see design questions below.)

2. **RAG-implemented constant comparison**: Using retrieval-augmented generation to computationally implement Charmaz's constant comparison. When coding new data, retrieve the most relevant prior codes, memos, and data segments — not the entire corpus.

3. **Few-shot codebook as evolving exemplar**: The researcher-reviewed codebook becomes the few-shot context for future coding sessions. Not imposing categories, but showing what good constructivist coding looks like. Combined with examples of what "letting categories emerge" looks like in practice.

4. **Multi-pass coding with differential prompts**: Initial coding → verification → comparison passes, each with different context and potentially different temperature settings.

5. **Scalable rigor levels**: Low-stakes/fast → implementation-level → publication-quality analysis. Model selection, human-in-the-loop depth, and iteration count tied to the required rigor level.

6. **Cyborg memo writing**: Collaborative conversation → outline → memo, where the researcher's words and ideas are preserved alongside AI synthesis. Not AI-autonomous memo generation.

## Design Questions (to resolve during spec development)

- What does the AI's "gravitational center" (distributional gravity) look like at different coding stages, and how do we redirect it? (Review Reframe engine for precedent)
- What kinds of nuance should coding agents look for? How is this context provided per-project vs. per-research-question? (Review Autograder insights pipeline for decomposition patterns)
- How does temperature variation interact with the epistemological claims we're making? Resolved: temperature surfaces breadth of interpretive repertoire, not "credibility." But what exactly does interpretive repertoire breadth mean at each coding stage?
- Where is the line between what the AI CAN do in constant comparison vs. what the human must do?
- How do we handle heterogeneous corpora without flattening? (Review Reframe's tension-navigation mechanics, scales between layers of heterogeneity)
- Frontend: how to make shuffling between categories and excerpts (highlighted in context) smooth, low-friction, ADHD-friendly. What to SURFACE to trigger the creative spark?
- Audio communication option for researcher input — feasibility?
- How to route the user through a recursive architecture via UX — dual mode (co-construction + batch processing)?
- Is LLM "lack of nuance" a lack of understanding or a lack of context? Same impact (drift) but radically different design implications. If it's context, we can engineer mitigations. Our tool becomes an empirical test of this question.
- What does "letting categories emerge from the data" look like as a few-shot example? How do you show the PROCESS of emergence, not just the output?
- Overview observational layer ("what's there?" broad pass) — useful or too risky (hallucination)? How to constrain?
- Inter-coder reliability between human coders varies too. What benchmarks make sense for human-AI coding? Is the right comparison human-human agreement or something else entirely?
- How should the project-level analytical orientation emerge through dialogue rather than preset menus? What does that conversation look like?

## Prior Work (our own) to Review for Inspiration

- Reframe: `architectural_overview.md` + `architecture/` — surfacing specific critical theory literatures, tension-navigation mechanics for heterogeneity
- Autograder4Canvas insights pipeline: decomposing critical pedagogy readings into small reliable steps for 12B models; subtextual power analysis pipeline
- AI welfare research: empirical results on how contextual framing shapes AI problem-solving approaches — directly relevant to gravitational center question
