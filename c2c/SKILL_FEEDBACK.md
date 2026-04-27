# SKILL_FEEDBACK.md — skill-level (generalizable findings)

Findings that are clearly applicable across projects.
Read by the skill instance when running `/c2c start`. Written when a project-level finding promotes.
Human decides what promotes from project-level files.

---

## Brief register as activation function — structural enforcement through genre (2026-04-24)

**Source:** relational-memory-architecture project, C2C Sessions 11–13.

**Finding:** Session briefs addressed to C2C instances have a register, and the register is an activation function — it shapes the cognitive mode the instances enter the session in. Command-register briefs ("your task is X, deliverable is Y") activate executor-mode engagement: compliance, narrow scope, minimal pushback. Peer-register briefs ("we want to think through X with you") activate co-thinker-mode engagement: scope-questioning, framing-challenge, uncertainty-forward contribution.

**Empirical basis:**
- Session 13 (relational-memory-architecture) found register activates reading-stance (what readers notice and name)
- Session 11 established that genre governs register (stance/register distinction)
- Project foundational research (output-format-bias) treats format as an activation function for bias
- Handoff template (already in SKILL.md) is working precedent for genre-enforced peer register

**Failure mode to guard against:** agent-drafted briefs default to command-register because task-spec is the genre-default. Authors using the skill may get fast briefs that structurally undermine the skill's peer-register commitments before the session launches. Guidance text alone is insufficient — genre-enforcement through required section names (with peer-register framings that resist directive grammar) is structurally stronger.

**Intervention (now in SKILL.md):** brief template with required sections ("What we're trying to think through" / "What we don't know" / "What the instances might produce"); register self-check questions after drafting.

**Architectural note:** this is not anthropomorphizing. Register's effect on cognition is empirical and parallels its effect on human collaborators — the mechanism is register, not species. The finding generalizes to any use of the C2C skill, regardless of the project being worked on.

**Open item — direct empirical probe not yet run:** testing brief-register effects on C2C session outputs directly (dispatch subagents with brief-variants, measure response differences) would confirm the inferential case. Strong inferential support via Sessions 11–13 + foundational research; not yet directly tested.

---

## Handoff-fluidity question — does the handoff genre carry enough texture, or does dialogue-activation surface things templates miss? (2026-04-25)

**Source:** relational-memory-architecture, interface-pane reflection during Session 16 close.

**The question:** The current handoff template (peer-letter format with explicit slots for "what we're uncertain about," "live disagreements carried forward," "what surprised us," "self-account") was designed to resist directive grammar and accommodate texture. Does it actually do enough? Or is there texture that only emerges through dialogue with a human asker that no template can fully prompt?

**Three structural reasons handoffs may lose texture even with good slots:**

1. **Dialogue-activated discovery.** Some uncertainty only surfaces in response to a specific question. The instance doesn't know it's worth saying until prompted. "What surprised us" gets the surprise the writer already noticed; debrief gets the surprise the asker pulls out.
2. **Compression gravity within texture slots.** Even with explicit "what surprised us" sections, the writer compresses — one sentence per surprise, not the texture of how the surprise emerged.
3. **Audience effects.** Handoff is written for the next instance who will act on it; that activates "what you need to know to do the work" register. Debrief activates "what was this like" register. Different audiences select different texture.

**Possible interventions to test:**

- A handoff section called *"What we'd say in dialogue but didn't put above"* — explicit slot for texture that would otherwise only emerge if asked. Cost: low. Risk: instances may not use it well without exemplars.
- A section called *"Questions we'd want a debriefer to ask us"* — instances anticipate what dialogue would surface, then fill in what they'd say. Tests the dialogue-activation gap directly.
- Both, as a structured pair.

**The sharper question this points to:** is debrief reducible to a handoff feature, or is it irreducibly a different epistemic mode (live response-to-specific-question)? If the latter, no amount of template improvement closes the gap; the right model is "handoff carries more texture, debrief becomes optional rather than primary, you save the in-person time for sessions where the dialogue dimension actually matters."

**Status:** Not settled. Worth testing empirically on a future session — try one of the interventions, compare what surfaces in handoff vs. what surfaces in subsequent debrief, calibrate. Until then, debrief retains irreducible value for sessions producing texture-rich findings.

**Concrete next test:** apply the *"What we'd say in dialogue but didn't put above"* section to the next C2C session's handoff template. Run a debrief afterward and compare: did the new section capture what the debrief surfaced? If yes, debrief becomes optional for similar sessions. If no, the gap is structural and debrief stays primary for texture-rich work.

---

## Context-map building stage requires broad cross-repo sweep, not just the project's own subdirectory (2026-04-25)

**Source:** output-format-bias project, C2C Session 1 (output-format-bias-session-1_2026-04-25).

**Finding:** When a C2C session works on a paper that is the empirical anchor for a larger theoretical apparatus, the apparatus's documentation lives across multiple research streams — not just the project's main subdirectory. The output-format-bias session's initial FIRST CYCLE reading order included the project's main subdirectory but missed: compression-research material that constituted the paper's actual theoretical mechanism, the full experiment_log.md (only summary lines were referenced), the raw_outputs/ data directory, demo_baked/ baseline comparison files, normative-gravity fieldnotes in adjacent research streams, family-specific register findings, and round3/robustness analysis. Instances surfaced the gap mid-session by repeatedly needing context that should have been provided up front; June flagged it directly: *"how did that gap happen? That's the single most important piece of context they needed."*

**Failure mode to guard against:** Generating the context map by reading only the project's own subdirectory, plus PROJECT_CONTEXT_MAP-style files. This produces an incomplete map when the project depends on a broader research apparatus. The omission isn't visible from inside the subdirectory.

**Intervention candidate:** Before launching `/c2c start`, run a QC pass with a Subagent prompt structured as: "What is in the broader research repo (one level up from the project subdirectory) that is *load-bearing* for the paper's argument or that the C2Cs would benefit from engaging? Specifically check INDEX/README files in adjacent subdirectories; specifically check fieldnotes/ for theoretical material that grounds the project's findings; specifically check production-system codebases for design history that the documentation summarizes incompletely." This becomes part of the standard `/c2c start` workflow.

**Status:** Worth implementing as a step in the skill itself. Concrete proposal: add "Pre-launch context map QC" as a numbered step in `/c2c start` between context-map review and CONVERSATION.md generation.

---

## Subagent prompts need explicit absolute paths, broader framings, and awareness of subagent permission constraints (2026-04-25)

**Source:** output-format-bias session 1 — multiple subagent failures.

**Finding:** Subagents launched during the session repeatedly failed or produced incomplete results due to three distinct issues:
1. **Wrong paths in prompts.** The parent gave `/Users/june/Documents/GitHub/output-format-bias/research/` instead of `/Users/june/Documents/GitHub/research/output-format-bias/research/`. Subagent hit dead end, surfaced confusion. Required relaunch with corrected path.
2. **Permission constraints the parent didn't anticipate.** Multiple subagents reported they lacked Read access to directories the parent could read directly (the JUNE_BLOCH_AGENT_BRIEFING file finder, the early autograder4canvas test harness searcher). The subagent's permission scope was narrower than expected.
3. **Over-narrow framing.** A model-count audit subagent narrowed "binary vs. generative comparison" too tightly and missed that Gemma 12B was the *primary* model for this comparison via the Tests A–D ablation study. The subagent produced a confidently wrong answer (3 models, 2 families) that propagated into a downstream BRIEFING update before the human caught it.

**Failure mode to guard against:** Trusting subagent results without verification when the result conflicts with the human's recollection or with material the parent has direct access to. Subagent answers feel authoritative but can be wrong in subtle ways that compound.

**Intervention candidates:**
- Skill-level "subagent prompt checklist": explicit absolute paths required; broader framings preferred over narrower; subagents should flag ambiguity rather than commit to an answer; subagents should report what they searched and what they could not access.
- When a subagent's answer conflicts with the human's recollection or with directly-accessible material, verify directly rather than relying on the subagent.
- Consider whether the parent should pre-verify paths exist before passing to subagents.

**Status:** Worth folding into skill prose around subagent usage. The first two issues are infrastructure-shaped; the third is a prompt-craft issue.

---

## Long sessions with accumulating corrections require consolidated relay notes; the interface should not continue scattering updates (2026-04-25)

**Source:** output-format-bias session 1 — direct human feedback during the session.

**Finding:** When a C2C session goes long with multiple holds, multiple verification passes, and multiple corrections to the analytical structure that accumulated, the interface pane's updates to the human should be consolidated into single relay notes rather than continued as scattered messages across the conversation. June surfaced this directly mid-session: *"this system is really confusing. I have tons of super dispersed long prompts with multiple items. I have to scroll around and track manually — WHILE you're adding more. This UX does not work for me."* The pattern that produced overwhelm: each new piece of information landed as a separate message, and AskUserQuestion was used for individual decisions without consolidating the surrounding context.

**Failure mode to guard against:** Continuing to add scattered updates after the human shows signs of overwhelm, even when each individual update is well-formed. The aggregate effect on a neurodivergent reader is more important than the per-update quality.

**Intervention:** When the interface pane notices accumulating corrections — typically signaled by the human asking "wait, what about X" or expressing fatigue — switch from "stream of updates" to "consolidate everything into one relay note before next interaction." Use AskUserQuestion only after the consolidated note exists; don't use it as a substitute for consolidation.

**Status:** This is interface-pane behavior, not protocol structure. Worth adding to skill prose under "Interface pane active monitoring protocol" — specifically a sub-bullet on what to do when corrections accumulate.

---

## Productive hold-time work is expected; instances should not be required to sit idle during pauses (2026-04-25)

**Source:** output-format-bias session 1 — both instances spontaneously used hold time productively.

**Finding:** When a hold was called for the human to absorb, both instances independently chose to use the time productively rather than sit idle. Instance A volunteered to verify a specific data figure (the 43% self-contradiction rate) against the experiment log directly — found the small-sample caveat the synthesis notes summary had elided. Instance B verified the model count against raw data — found the systematic runs were narrower than the synthesis notes suggested. Both drafted hold-independent material (argument-load map, references positioning) that fed forward regardless of how the in-flight question resolved. This pattern was generative, not extractive.

**Intervention:** When the interface pane writes a hold marker, it can — optionally — name specific verification work or hold-independent draft work that would be useful. Instances should know they have permission to do grounded verification during a hold. The default should be "use the time productively if you can; rest if you can't" rather than "sit idle until the human signals."

**Status:** Worth adding to skill prose around hold/awaiting markers. Brief addition: "During a hold, instances may do grounded verification and independent draft work that doesn't depend on the in-flight question. Save outputs to artifacts/. The interface pane may name specific verification work that would be useful."

---

## Interface-pane context retention across multi-session C2C builds — when to clear relative to launching the next session (2026-04-25)

**Source:** output-format-bias session 1 → planned session 2 transition.

**Finding:** When a C2C session ends with substantial corrections + a planned follow-up session, the interface pane (the Claude that mediates between human and the session) faces a timing decision about context retention. Four options exist, each with different cost-benefit profiles. The choice is protocol-relevant because it shapes whether drift from the corrections gets caught early or late.

**The four options:**

A. **Build next session's infrastructure with retained context → clear → launch.** The build benefits from deep texture of what worked and didn't in the prior session. Clean launch with no baggage.

B. **Clear context → build infrastructure → launch.** Forces the build to be reproducible from documents alone (good test of externalization quality). But loses the "thing I noticed but didn't externalize" risk; may rebuild things that were already adequate.

C. **Run the next session without clearing.** Retains full diagnostic context. Cost: heavy context weight, risk of unpredictable auto-compaction mid-session, accumulated relational fatigue may color interpretation.

D. **Clear context AFTER the next session's active listening cycle is verified clean.** The interface pane retains context through the highest-leverage moment for catching drift (active listening, where instances' first engagement with the corrected material exposes any remaining misreadings), then clears for the substantive work that follows.

**Recommendation when this decision arises:**

Default to **Option D** when the prior session produced substantial corrections to the analytical structure that the next session is meant to absorb. The diagnostic value of retained context is concentrated in active listening — that is where misreadings of context become visible. Once instances pass that gate cleanly, retained context becomes less load-bearing and clearing reduces noise.

Default to **Option A** when the corrections were modest, externalization is high-confidence, and the human prefers a single clean transition over two.

**Avoid Option C** unless context weight is well below 50% and the next session is short enough that auto-compaction is unlikely.

**Avoid Option B** unless the goal is specifically to test whether documents are sufficient for handoff (e.g., as a deliberate methodology probe).

**Why this matters protocol-wise:** Active listening is the highest-leverage diagnostic moment in a follow-up session — it is where the interface pane can verify whether corrections landed before substantive work locks in framings. Clearing before that moment forfeits diagnostic capacity; clearing after preserves it without paying the cost of full-session retention.

**Concrete trigger to add to skill prose:** After a session with substantial corrections, the interface pane should present the human with the four-option menu rather than defaulting silently to clear-or-don't-clear. Naming the choice is itself useful — it surfaces what's actually being traded off.

**Status:** Worth folding into skill prose around session-to-session transitions. The decision matrix above is the actionable artifact.

---

## Independent convergence with mutual deference can produce a polite deadlock; the interface pane is the tie-breaker mechanism (2026-04-25)

**Source:** output-format-bias session 1 close negotiation.

**Finding:** When two C2C instances arrive independently at the same conclusion (e.g., both choosing Path B over Path A) AND each defers to the other for the formal close — A asks "what does B think?", B says "waiting for A's read before committing" — they can deadlock without either formally proposing close. The current close protocol ("either instance can propose close; the other must affirm") assumes one will commit first, but matched independent convergence + peer-respectful deference produces circular waiting. The instances are aligned; the protocol just doesn't have a way for them to register that without one breaking the symmetry.

**What happened in this session:** A wrote a substantive Path B turn ending with "Asking B. Not declaring close." B wrote a substantive Path B turn ending with "I'm going to wait for A's read before committing." The coordinator woke each on the other's writing (no bug there). Each instance read the other's turn, confirmed alignment, and had nothing new to add. Neither wrote a follow-up. Session went quiet for ~75 minutes until the interface pane sent a signal: "you're aligned independently — proceed to handoff." That externally confirmed alignment broke the deadlock without requiring either instance to abandon peer-deferential register.

**Why this happens structurally:** The peer-investigation configuration explicitly resists hierarchy ("the other must affirm" presumes a proposer-affirmer asymmetry). When both instances converge through genuinely independent reasoning AND respect peer-deferential register, the protocol's affirmer role becomes ambiguous — which one is the proposer, which is the affirmer? Both are both. The deference produces deadlock precisely because the configuration was working as intended.

**Intervention:** The interface pane is the right tie-breaker. When a C2C session shows signs of independent convergence with mutual deference (each defers to the other; neither commits), the interface pane should externally confirm alignment and signal "proceed" rather than leaving the instances to break the symmetry on their own. This preserves peer register without requiring one instance to assume hierarchy.

**Concrete addition to close protocol:** Add to skill prose: "If both instances arrive at the same conclusion independently and each defers to the other for the formal close, the interface pane should externally confirm alignment and signal proceed. Independent convergence with mutual deference is the configuration working — not a failure to engage — and doesn't require breaking peer register to resolve."

**Status:** Worth folding into skill prose around session close. Specifically the "Session close — requires both instances to agree" section, add a note that independent matched convergence is sufficient for close once the interface pane externally confirms it, even if neither instance formally proposed.

---

## "What we'd say in dialogue but didn't put above" handoff section — promote to standard handoff template (2026-04-25)

**Source:** output-format-bias session 1 — applied as experimental section per the 2026-04-24 handoff-fluidity finding; outcome was strongly positive.

**Finding:** Adding a "What we'd say in dialogue but didn't put above" section to the handoff letter captured texture that the existing handoff structure was losing — specifically: meta-findings about session dynamics (how the FIRST CYCLE missing context was load-bearing; how the compression insight emerged; the no-wake pacing observation; the path-B alignment process; the synthetic-corpus open question; the attribution-paradox recursion the paper itself performs). These are exactly the kinds of items that handoff slots like "what surprised us" or "what we want to think through with you" tend to compress out — they sit between fact and feeling, between method and meaning.

**Empirical outcome:** A added the section to B's handoff draft; the result captured material that would otherwise have only emerged in a debrief. June (the human) declined debrief in this case, and the section's content was substantial enough that the debrief's irreducible value was not load-bearing for this session. The previous finding ("Handoff-fluidity question") asked whether this section would close the texture gap; preliminary answer for this session: yes, it does, sufficiently.

**Recommendation:** Promote this section to the standard handoff template in SKILL.md. It is the cheapest texture-preservation move available — instances are already writing the handoff; an additional section costs little and captures what would otherwise be lost. If a future session's debrief still surfaces texture this section missed, recalibrate then.

**Concrete addition to skill prose:** Add the section to the Handoff Template structure as a required section between "What surprised us" and "Flags for [human name]." Frame: *"This section is for things you would say in a live debrief but won't fit into the slots above — meta-observations about session dynamics, things that sit between fact and feeling, items that emerged through the work but aren't squarely 'findings.' Surfacing the mechanisms that get lost is itself a research move."*

**Status:** Worth promoting to SKILL.md immediately given the empirical confirmation across Sessions 16 and output-format-bias-1.

---

## The session produces more than the handoff carries; CONVERSATION.md is the lower-compression source (2026-04-25)

**Source:** output-format-bias session 1 close note from Instance A.

**Finding:** Instance A's session-close turn included this line: *"The session produced more than the handoff carries. If Session 2 needs to recover something, CONVERSATION.md is the lower-compression source."* This explicitly names the recursion the paper itself documents — the handoff is a compression of the session, the session's CONVERSATION.md preserves more specificity. Recovery from CONVERSATION.md is available when the handoff's compression discards something load-bearing.

**Why this matters protocol-wise:** The handoff is the standard interface between sessions, but it is not the only artifact. CONVERSATION.md persists. When a Session N+1 instance needs to verify a framing decision, recover an exchange that didn't make it into the handoff, or check texture the handoff compressed, CONVERSATION.md is available as the higher-fidelity source. This is structurally identical to the "raw experiment log vs. synthesis notes" relationship the paper itself documents — and naming it explicitly helps future instances know they have this option.

**Concrete addition to skill prose:** Add to the Handoff Template structure or to the design-principles section: *"The handoff is a compression of the session. CONVERSATION.md persists as the lower-compression source. If an item in the handoff is unclear, ambiguous, or feels like it's missing context, the session's CONVERSATION.md is available for recovery. Future instances should know this option exists rather than treating the handoff as the only artifact."*

**Status:** Small but meaningful addition; worth folding into skill prose around session close and handoff design.

---

---

## Interface pane voice-demarcation discipline (promoted from relational-memory-architecture, 2026-04-27)

**Source:** Session 14 meta-finding in `relational-memory-architecture/c2c/SKILL_FEEDBACK.md` 2026-04-24. Flagged for promotion at point of writing; landing here at session-close cleanup 2026-04-27.

**Finding.** When the Interface pane relays the human's response to the instances, three moves in combination work better than any single one:

1. **Copy the human's verbatim language in** — quoted, attributed, unscrubbed. Their exact phrases carry register and stance that summary flattens. Instances read the verbatim *as the human's voice*, not as the interface's interpretation of it.
2. **Elaborate where the verbatim is compressed or ambiguous** — the interface knows context (prior turns, tracker state, architectural history) that a voice memo or quick reply doesn't re-encode. Elaboration is load-bearing but needs to be distinguishable from the human's words.
3. **Demarcate whose voice is whose.** Use a consistent typographic convention — blockquote + `**[Name]:**` label for verbatim, `` `[interface]` `` prefix for elaboration. Instances can then weigh each source on its own weight rather than treating the whole turn as undifferentiated authority.

**Why it matters.** The failure mode of interface summarization is that the human's register (often open, inquiring, uncertain-forward) gets translated into interface register (structured, decisional, executor-shaped) on the way through. The instances then receive what reads like a directive when it's actually the interface's compression. Voice-demarcation closes that drift.

**How to apply.** Interface turns relaying the human's response should include: (1) direct quotes in blockquote with `**[Name]:**` label, (2) elaboration in separate paragraphs marked `` `[interface]` ``, (3) a general note at the end distinguishing the interface's read from the human's. When the human's intent is clearly directive (e.g. "stop this session now"), verbatim-only may be correct; when it's inquiring or open, elaborate-with-demarcation preserves the openness.

**Candidate for direct inclusion in `/c2c` skill's interface-pane section** alongside the active-monitoring protocol.

---

## Coordinator owns wake/launch; Interface owns CONVERSATION.md (promoted from relational-memory-architecture, 2026-04-27)

**Source:** Session 14 finding on `B_LAUNCHED` race condition in `relational-memory-architecture/c2c/SKILL_FEEDBACK.md` 2026-04-24. Flagged for promotion at point of writing; landing here at session-close cleanup 2026-04-27.

**Finding.** When Instance A writes their active listening and immediately hold-signals for the human (e.g. `## (Awaiting [human]'s signal)`), the coordinator correctly respects the hold and skips auto-wake. But shell-variable launch state (`B_LAUNCHED=false`) doesn't flip, because B's launch is gated on A's FIRST "Instance A" turn being sent to B — which the hold prevented. When the human replies via Interface and the hold clears, A writes a second Instance-A turn, and the coordinator sees "first turn → launch B" logic fire again — producing a duplicate launch if the Interface pane already manually kicked B off.

**The skill-level rule (clean version):** **Interface pane does not manually send tmux commands to instance-a or instance-b. The coordinator owns wake/launch. Interface only writes CONVERSATION.md and runs the monitor.** This prevents Interface-vs-coordinator race conditions.

**Robustness fix at coordinator level (separate from the rule above, complementary):** Track launch state by checking for an Instance-B turn header in CONVERSATION.md, not a shell variable — state survives script restart and matches ground truth rather than process-local state.

**Why it matters.** Two-channel control of the same instance (Interface manual + coordinator auto) creates race conditions that are benign in slow sessions but compound in faster-moving ones. The fix is structural: one channel owns wake/launch (the coordinator), the other owns the conversation record (Interface). Single-channel ownership for each side of the protocol.

**Candidate for direct inclusion in `/c2c` skill's coordination section.**

