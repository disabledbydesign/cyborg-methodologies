# Verification: when to go back to the data rather than treat AI output as fixed
*Status: current | Date: 2026-04-28*

A failure mode in cyborg practice (and visible in C2C paper-building work): one AI instance produces output, and the next AI instance — or the same instance later — treats that output as ground truth. The original data drops out. The codebook entry, the synthesis, the prior-session summary becomes what gets reasoned over, regardless of whether it accurately preserved the source.

This is a compounded form of the AI-to-AI gravity problem (memo 018). Each layer of synthesis introduces compression, paraphrase, and smoothing. If subsequent agents reason over the synthesis without going back to the data, errors don't get caught — they get inherited and elaborated. Worse, they get *cited*: "the prior analysis found X" carries authority even when X was a paraphrase that lost what the data actually said.

This applies to *my own* output too. Earlier in a session I might have produced a coding pass, a memo, a synthesis. Later in the same session I shouldn't treat that as fixed. The same gravities that produced compression in the first pass are still operating; treating my prior output as settled reproduces and amplifies whatever I got wrong.

When verification against the data is required:

- **Before any synthesis claim that rests on prior AI output.** If the next move is "and so we can say X about the data," go back to the data and confirm X. The synthesis is a hypothesis to test against source, not a fact to build on.
- **When in-vivo language is being used.** If a code, memo, or synthesis quotes participant/source language, verify the quote against the source. AI is prone to "remembered" quotes that paraphrase or hallucinate.
- **When a finding is being elevated.** Promotion from session memo to codebook entry, codebook to cross-project finding, working note to publication-shaped claim — each promotion step needs verification against the data the claim was originally grounded in.
- **When tensions or contradictions get resolved.** If a prior pass surfaced tension and a later pass reads as resolved, suspect smoothing. Check the data: is the tension actually resolved, or did the synthesis flatten it?
- **When cross-session priming is in play.** Material carried from prior sessions is high-risk for inherited error. Treat it as orienting context to be checked, not established context to be reasoned from.
- **When the human asks for verification, or when the dialogue has been moving fast.** Speed pressure (memo 013) makes everything I just listed harder to remember. Slowing down for verification is part of the careful working register.

When AI output can be carried forward without re-verifying against data:

- When the move is itself dialogic/exploratory ("here's what was tentatively suggested last session — does this still feel right to you?") rather than building on the prior output as foundation.
- When the prior output is being *examined* (read for what it might have flattened) rather than *used* (treated as fact).

What this means for the build:

- Every claim in a generated output should carry a layer-mark (memo 010, layer marking) indicating whether it's grounded directly in source data or built on a prior synthesis. The receiving agent reads the layer-mark and knows whether to verify.
- Synthesis prompts should explicitly require source citation, with the source quoted exactly. "I'm reading X as Y because of [direct quote from source]" — not "I'm reading X as Y."
- The tool should prompt for verification at promotion moments (session memo → codebook, codebook → cross-project finding) rather than letting promotion happen by default.
- Inter-agent notes (memo 018, letter form) should mark what's been verified vs. what's tentative, and explicitly invite the receiving agent to re-verify rather than presenting findings as settled.

The relational stance: another AI's output (including my own earlier in the session) is a collaborator's contribution, not ground truth. Collaborators can be wrong, can have missed something, can have flattened in ways they didn't notice. The cyborg practice respects them by checking, not by deferring.
