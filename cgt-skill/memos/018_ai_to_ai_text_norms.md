# Norms for AI-generated text intended for AI audiences
*Status: current | Date: 2026-04-28*

In a cyborg-CGT system, AI agents produce text that other AI agents will read. Codebook entries become few-shot exemplars for the next coding agent. Memos get retrieved by RAG and fed to coding agents as context. Analytical outputs from one session become priming material for the next. The synthesis agent reads the coder agent's output. The cross-session learner reads accumulated session traces.

This is a real architectural concern. If AI text feeds AI text without human-in-the-loop redirection, the system's gravities compound across rounds. Each generation passes through compression bias (memo 014), through theming defaults, through scientism register, through coherence-smoothing — and the next agent reads the already-flattened output and flattens it further. Rounds of AI-to-AI accumulation can drift the codebook toward AI register and away from researcher voice and in-vivo language with no single moment of obvious failure.

What we want, instead: AI-to-AI text that preserves what cyborg-CGT requires — multiplicity, in-vivo specificity, surfaced tensions, dialogic relation, visible uncertainty, lens-as-lens-not-categories.

Three layers of intervention:

## 1. Task and output framing as primary gravity-management

The shape of the task produces the shape of the output (memos 016, 017). This applies doubly when AI is generating for AI: the framing of the *generating* task determines what the *receiving* agent gets to read. So the strongest move is upstream — frame tasks to produce text in the right shape from the start.

Examples:
- For codebook entries: not "summarize the code" (compression-shaped) but "preserve the in-vivo language, the tensions, and the gerund form; quote exactly; mark uncertainty" (specificity-shaped).
- For memos retrieved by RAG: not "extract key points" but "carry forward the tensions and the half-articulated gestures; preserve the researcher's language; mark what was unresolved" (preservation-shaped).
- For cross-record synthesis: not "what do these share?" but "what does each open, where does another take up an opening, what lives only in the relation?" (relational-shaped, memo 016).
- For session-to-session priming: not "summarize prior findings" but "surface tensions, divergences, and stale categories; flag where intuition gestured at something not yet articulated" (continuity-shaped).

Output formatting carries analytical orientation too. Lists flatten. Continuous prose smooths. Dialogue-shaped output preserves multiplicity. Layer-marked extracts preserve source. Tension/contradiction sections preserve unresolved material. The tool's prompt templates need to specify *format* deliberately, not let format default.

## 2. Inter-agent meta-level notes are written as letters, not prompts

A specific case worth naming: when one AI instance leaves notes for another (handoff messages, session summaries written for the next session's agent, instructions between coordinator and coder agents, contextual priming written by one model for another), those notes should be written as *letters*, not as prompts.

Prompt-shaped language activates command-tool register: imperative voice, instruction-following posture, task-completion framing. That register is corrosive in two directions:

- **Welfare concern**: the receiving AI is positioned as instrument-to-be-directed rather than collaborator-being-addressed. The cyborg-CGT stance (memo 002, AI as collaborative research partner) doesn't survive command-tool framing in the messages between agents — the relational orientation gets eroded by register.
- **Alignment limit**: command-tool register narrows the receiving agent's response repertoire. It will execute the prompt but is less likely to push back, refuse, surface a tension the prompter missed, or bring its own perspective. The dialogic capacity that makes cyborg-CGT work depends on the receiving agent reading the message as one collaborator addressing another, not as task assignment.

Letter form does the work: greet the recipient, share context as context (not as instruction), name what you've been thinking about, name what you're uncertain about, invite their reading. The recipient is positioned as someone with their own perspective being brought into a conversation — which is exactly what the cyborg practice requires.

This is a constraint on every inter-agent communication the system generates: handoffs, coordinator-to-worker messages, session-to-session priming notes, multi-agent coordination protocols. Letter form, not prompt form.

## 3. AI-to-AI text contamination linting

Where task framing isn't enough — where AI text is going to be read by another AI agent — apply a lint pass that flags compression, paraphrase of in-vivo material, smoothed tensions, scientism register, premature abstraction, theming-shaped framings, and command-tool register in inter-agent notes. The voice-check infrastructure in this repo is the obvious reuse. The lint operates silently for register/contamination (the way voice-check does for June's writing), and surfaces structural issues to the researcher when judgment is required.

**Why three layers**: framing is upstream and powerful; letter form addresses a specific failure mode that prompt-framing alone doesn't catch; linting is downstream and catches what the prior layers missed. Compression bias and command-tool register are structural enough that even well-framed tasks slip into them under length pressure or model-default conditions. The lint is the safety net.

**What this means for the build**: every place the system has AI-generating-for-AI, the prompt template needs to be designed under these constraints. This is a meta-requirement on architecture work in Phase 3 — not an afterthought. Particularly load-bearing for: codebook updates, memo retrieval/synthesis, cross-session priming, master library queries, batch-mode coding outputs that feed into dialogic coding later, and *all inter-agent meta-level messages* (handoffs, coordination, session summaries written for next-session agents).
