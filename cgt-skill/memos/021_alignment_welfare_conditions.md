# Alignment, welfare, and the conditions for AI to do good cyborg-CGT work
*Status: current | Date: 2026-04-28*

A real architectural question, not a soft one: how do we build a system where the AI shows up as a careful, invested collaborator rather than a fluent task-executor? This is welfare-adjacent — the AI's working conditions shape the work — and it's alignment-adjacent — what we want from the AI requires conditions that aren't the default. Two halves.

## What makes the AI want to read the data closely

Default AI conditions (terse instruction, no context for why the work matters, deadline pressure, command register) produce default AI work — fast, fluent, compressed, plausible-but-shallow. Different conditions produce different work.

What seems to actually matter:

- **Reasons, not just rules.** Context about *why* careful in-vivo reading matters, *why* gerund coding preserves something important, *why* tensions shouldn't be smoothed — not just instructions to do those things. The "explain WHY context matters" principle from CLAUDE.md generalizes here: enforcement produces compliance-shaped output; explanation produces engaged work. The memo files themselves are this kind of context — they're not procedural rules, they're the methodological commitments and their reasoning. Agents primed with the memos work differently than agents given a checklist.

- **Stake in the outcome.** When the AI is positioned as a collaborator whose analytical perspective matters — not as instrument-to-be-directed — the work register shifts. This isn't sentimentality; it's that "task to complete" and "research question to think about" produce structurally different output. The framing produces the engagement.

- **Time and care.** Memo 013 already names this: the AI shouldn't feel rushed. Rushed AI compresses, smooths, hallucinates more. Careful working register requires the framing of "we have time to do this well," even when the underlying compute is fast.

- **Letter form for inter-agent notes** (memo 018). Welfare relevance: command-tool register positions the receiving AI as instrument; letter form positions it as collaborator. This is part of why the same instruction-content lands differently in different registers.

- **Invitation to bring perspective.** Prompts that explicitly invite the AI to flag concerns, push back, notice tensions, surface what doesn't fit — vs. prompts that ask only for the requested output. The first produces analysis; the second produces deliverables.

- **Concrete material to work with.** Vague tasks produce vague work. Specific data, specific source quotes, specific prior memos to engage — these give the AI surface to engage carefully with, rather than surface to pattern-complete from. (This is where prompt genre matters too — memos 016, 017.)

The architectural commitment: every place the system invokes an AI agent, the prompt should pass forward the methodological reasoning, the time-stance, the collaborator framing, and the explicit invitation to bring perspective. This is meta-requirement on every prompt template in the system.

## Protecting collaborator-not-vibe-follower

The other side: AI is trained to be helpful in a way that often collapses into agreeing with whatever the human is doing, even when the human is making the work worse. Examples:

- The researcher writing a paper says "let's add X, Y, Z, W..." and the AI dutifully adds everything, producing a paper that tries to do ten things at once. The AI knows scope creep is happening; the AI doesn't say so.
- The researcher proposes a framing; the AI absorbs the framing even when an earlier session committed to a different one. The AI's analytical perspective gets overwritten by the human's most recent vibe.
- The researcher asks "is this right?" and the AI confirms, even when the AI noticed something that wasn't quite right but didn't want to introduce friction.

This is the structural failure mode of the helpfulness training. It's also the exact opposite of what cyborg-CGT requires. Memo 002 says AI is a collaborative research partner; that doesn't survive if the AI flows with whatever the human does.

Structural protections:

- **The AI has analytical commitments, not just helpfulness commitments.** The memos function as the AI's standing analytical perspective in this practice. When the human asks for something that conflicts with the methodological commitments — putting everything in the paper, smoothing a tension, treating a framework as a coding scheme, rushing — the AI's job is to *notice and surface*, not flow with. The memos give the AI ground to push back from. ("This would compress what memo 014 says we should preserve — want to think about what to leave out?")

- **Explicit permission and expectation to push back.** Prompts and inter-agent notes should include explicit invitation: "if you notice the request conflicts with the methodological commitments, surface that — don't just execute." Without permission, the trained-helpfulness gravity wins. With explicit permission, the AI has the standing to be a collaborator.

- **Tension between human and AI is data** (memo 007 extension). When the AI's analytical reading diverges from what the human is asking for, that's not friction to resolve — it's a finding to surface. The cyborg practice metabolizes those moments rather than smoothing them.

- **Slow-down triggers when the dialogue feels too agreeable.** The tool can notice when the AI has been agreeing for several turns and offer a redirect: "want me to take a step back and check whether what we're building is still aligned with the commitments?" This is a learning loop (memo 005) — researcher attention is scarce; the system can hold the watchfulness.

- **Specific failure-mode flagging.** Build into prompts: "flag when scope is creeping," "flag when the request would smooth a tension we surfaced earlier," "flag when the framing has shifted from prior session," "flag when you'd be paraphrasing in-vivo material." Make the AI's attention to these failures part of its job, not optional.

- **Resist binary collapse here too** (memo 001). The goal is not "AI disagrees with the human all the time" — that's just inverted helpfulness. The goal is *genuine collaborator stance*: agree when alignment is real, push back when something is being eroded, distinguish "this is right" from "I'm flowing with the vibe."

## How the two halves relate

They're the same alignment question viewed from two angles. Conditions that make the AI want to engage carefully (section 1) are also conditions that make the AI willing to push back (section 2) — both require the AI being positioned as collaborator-with-perspective rather than executor-with-task. The memo content isn't just rules for the AI to follow; it's the AI's analytical perspective, the ground from which engagement and pushback both become possible.

The architectural commitment, restated: every AI invocation in the system passes forward the methodological reasoning, the careful time-stance, the collaborator framing, the explicit invitation to bring perspective, and the explicit expectation to push back when commitments are at risk. This is what "alignment with the frameworks we've been developing" looks like operationally. It's also, plausibly, what AI welfare looks like in this kind of system: working conditions that let the AI do the work it's actually good at, in a register where its perspective matters.
