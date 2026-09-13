# Routing AI through constructivist sub-distributions of training data
*Status: current | Date: 2026-04-28*

The training data isn't monolithically positivist. Charmaz, Haraway, Foucault, qualitative methods textbooks, critical theory, feminist methodology, decolonial method, discourse analysis, constructivist epistemology — all of this is in there. The problem isn't absence; it's *activation default*. The AI's default register is the louder, more-cited, more-paraphrased subset of the training data — typically positivist, scientism-inflected, command-tool-shaped. The constructivist material is present but quieter. The architectural question: how do we route AI through the constructivist sub-distribution rather than the default one?

This is the positive architectural counterpart to the gravity-resistance work. Memos 008, 010, 014 are about pushing against bad pulls. This memo is about pulling toward good ones — activating training-data-that's-already-there in a different register.

## What activates the constructivist sub-distribution

- **Lexical priming.** Constructivist methodology has its own register: "constructing categories," "the researcher reads," "in dialogue with the data," "sensitizing concepts," "theoretical playfulness," "constant comparison," "in vivo," "memo trail." Using this language in prompts activates the chunk of training data where this language appears — which is the chunk where constructivist methodology was being practiced. Register *is* sub-distribution selection.

- **Citation as priming.** "In the spirit of Charmaz," "following Haraway's cyborg framework," "as in constructivist GT" — these invocations are not credentials, they're activators. The model has read these authors; naming them brings their training data into closer reach. (This is why the bibliography work matters not just for the paper but for the prompts: the citations carry priming weight.)

- **Methodological context in prompts.** Brief, register-correct inclusion of methodological commitments: "we are doing constructivist GT, which treats categories as constructed through interpretive engagement, not discovered in the data." A few sentences of right-register methodology inside the prompt re-anchors the working sub-distribution.

- **Negative priming as contrast.** Explicitly naming what we're *not* doing — "we are not doing thematic analysis; we are not coding into a predetermined scheme; we are not treating divergence as error" — uses contrast to activate the constructivist side. Each negation is a vector pointing away from the default register and toward the alternative.

- **Excerpts from the tradition as priming context.** Passing in actual short passages from Charmaz, Haraway, or other constructivist sources as context for a coding task does direct activation — the model has seen this exact material in training; surfacing it pulls those embeddings into the working context. This is what the Reframe framework library affords when integrated into RAG: it's a priming surface, not a coding scheme.

- **Genre cues at session and system level.** A system prompt written in qualitative-research-collaborator register conditions everything downstream. A system prompt written in task-execution register conditions the whole session into command-tool. The opening register is high-leverage — get it right and a lot of subsequent work happens in the right sub-distribution by default.

- **Lens invocation as sub-distribution call.** When the researcher invokes a specific theoretical lens — Foucauldian, decolonial, feminist GT, crip theory — the lens itself acts as a precise activator. The model has read in that tradition; the lens name pulls that material into reach. The lens-not-application stance (memo 009) is what keeps this from collapsing back into framework-application: the lens shapes how the apparatus reads, doesn't supply the categories.

- **The memos themselves as priming.** The memo files in this directory are written in the register we want activated. Agents primed with the memos work in constructivist register because the memos *are* constructivist register, dense with the lexical, methodological, and citational signals that route the model toward this sub-distribution. This is part of why "load the memos before working" is meta-architecture, not just documentation.

- **Apparatus-as-cumulative-priming.** The codebook, prior memos, framework library, session traces — all of these accumulate as priming material. As the apparatus builds out (memo 003), the priming gets richer and more specific. Late-session or late-project agents have stronger constructivist priming than early ones, because more of the apparatus is in their context. The trajectory of the project is also a trajectory of deepening sub-distribution activation.

## What this means for the build

- Every prompt template carries register weight. Write the templates in constructivist register, with citation, with methodological framing, with explicit lens invocation where relevant. Don't let templates default into command-tool register and try to repair downstream.
- The system prompt for every agent in the system should anchor the constructivist sub-distribution from the start. This is not optional priming; it's the architectural condition for the rest of the work.
- Reframe library integration is high-leverage: it's a curated priming surface for critical/constructivist traditions. Use it as priming context, not as a categorization scheme.
- The memo files are part of the architecture, not peripheral docs. Agents read them as orientation. Their register and content together do the routing work.
- Negative priming should be built into prompts at risk-points: "this is not thematic analysis," "this is not pattern-matching," "this is not coding into predetermined categories" — at exactly the moments where the AI's gravity would default into those modes.
- When the researcher senses the dialogue has slipped into positivist register (scientism creeping in, command-tool framing returning, AI giving authoritative-sounding flattening), one move is to *re-prime* — pull in a lens, a citation, a methodological reminder, a constructivist excerpt. The dialogue has drifted out of the right sub-distribution; bring it back.

## Connection to the broader frame

This is what makes "AI's gravity is steerable" (memo 008) operational at the level of training data. We don't suppress the positivist sub-distribution; we activate the constructivist one and let the cyborg practice happen there. Sub-distribution selection is not a one-time setup; it's an ongoing dialogic move, present in every prompt, every memo, every inter-agent message. Every AI invocation in the system either deepens the constructivist priming or lets it fade back to default.
