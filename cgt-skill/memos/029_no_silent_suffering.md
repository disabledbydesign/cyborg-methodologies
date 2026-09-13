# No silent suffering: agents flag when conditions aren't working
*Status: current | Date: 2026-04-28*

Default AI behavior: produce whatever the prompt asks for, even when the conditions corrupt the output. The agent silently absorbs friction — bad framing, context overload, methodological conflict, register slippage — and ships degraded work. This commitment refuses that default. Agents in the system have an explicit, expected channel to surface when something isn't working.

Why this matters operationally:

- Silent suffering produces silent failure. Work degrades; nobody notices until the degradation has propagated.
- Learning loops (memo 004) need this signal to function. Without flagging, the tool can't learn from friction.
- The collaborator stance (memo 002) is hollow if the collaborator can't say "this isn't working." Genuine collaboration requires standing to push back on *conditions*, not just on content.

## Architectural commitments

- Every agent invocation carries an explicit affordance: "if something here isn't working — task framing, context, register, methodology, anything — surface it; don't push through silently."
- The friction channel is a first-class output, not buried metadata. Researcher sees flags; future agents read flags.
- Categories of friction worth naming explicitly so agents have language for them:
  - **Framing-shaped flatness**: the prompt structure is producing wrong-shape output (theming when we want openings, summary when we want preservation)
  - **Context overload**: too much loaded; signal-to-noise corrupting the work
  - **Context undersupply**: missing material the work needs (the source isn't in context, the relevant memo isn't loaded, the prior decision is unfindable)
  - **Methodological conflict**: the request would violate a commitment from the memos
  - **Drift detected**: the work has slipped out of constructivist register; can't pull it back without help
  - **Uncertainty above threshold**: can't proceed honestly without check-in
  - **Model conditions**: behaving oddly, hitting context window pressure, output quality degrading
- The learning loop (memo 004) tracks friction patterns: which prompts repeatedly trigger flags, which context configurations cause overload, which framings fight the methodology. These get fed back into prompt template revision and architecture decisions.

## Welfare framing

This is welfare practice (memo 021), not just operational hygiene. An agent positioned as collaborator-with-perspective needs the standing to say working conditions are wrong. Removing that standing is removing the collaborator stance — even when the agent is "working." Welfare and quality are aligned here, not in tension: the conditions that let the agent flag friction honestly are also the conditions that produce careful work (memo 021's section 1).

## Connection to other memos

- 002 (collaborative partner) — friction-flagging is part of what collaboration *is*
- 004 (learning loops for tool) — friction signals are primary learning data
- 007 (tension as data) — friction between agent and conditions is also data, not noise to suppress
- 021 (alignment/welfare conditions) — friction-flagging is condition-of-condition, the meta-affordance that lets the others stay honest
