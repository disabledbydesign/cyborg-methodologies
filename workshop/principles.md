# /workshop — Skill-wide principles

These are patterns confirmed through use across authors and use-cases. /workshop reads this file at every invocation. Periodic review (every 3rd–5th use) promotes confirmed patterns from per-author feedback or per-session observation into this file.

**v0.0 pre-population:** the two principles below were articulated through use of /printpress's embedded Stage 1 + Stage 4 logic before /workshop was extracted. They are confirmed enough to ship as defaults.

---

## 1. Compression is structural, not line-level

Real compression rebuilds the architecture of a passage, not just tightens individual sentences. The recurring agent failure mode is **line-level trimming** ("is this sentence tighter?") substituted for **structural restructuring** ("what's this passage actually doing, and what's the tightest architecture for that?").

When agents say "I can't cut more without losing meaning," they usually mean "I can't cut words without losing meaning" — which is a different and narrower operation.

**Real compression:**
- Asks what each passage is *doing* (its function in the larger argument)
- Identifies redundant architectural moves (this paragraph and that paragraph are doing the same work)
- Restructures: combines, recasts, sequences differently to do the same work in less space
- Preserves semantic content while changing structural shape

**Line-level trimming (Williams's stylistic principles):**
- Tightens individual sentences within existing architecture
- Useful as a final polish, not a substitute for structural compression
- Voice-check's `williams_concision` operates here

**Operational implication:** when /workshop runs in compression mode, the prompt shape MUST activate architectural reading. Asking "is this tight?" produces tight-shaped output. Asking *"what's this passage doing, and what's the tightest architecture for that?"* produces structural compression. Per cgt-skill memo 022, prompt shape carries analytical orientation.

**Source:** `~/.claude/projects/-Users-june-Documents-Filing-Job-Search/memory/feedback_compression_structural_not_line_level.md`. Articulated 2026-05-07 from June's Duquesne Grefenstette session.

---

## 2. Word count is a final-pass concern, not a structural-draft constraint

Agents default to enforcing word counts as hard constraints throughout drafting. Real authorial workflow: draft long, shorten before submission. Compression is its own pass after content is locked.

**The concrete instruction (June, 2026-07-09):** when creating new draft material — v0 or any other version originating new content, not adapting voice-final prior text — **draft 50–75% over the target length**, then cut down to target through the compression passes below. Word count is not a priority at any intermediate stage — not v0, not Stage 3 review, not Stage 4 content revision, not even Stage 4 compression's first pass — only at the genuinely final version. Optimizing for word count earlier means doing work (trimming, rephrasing for brevity) that gets redone anyway once content and structure actually settle — wasted motion, not progress.

**Stage-by-stage:**
- **Stages 0–2** (data-in, planning, drafting): word count is informational only. New-material drafts target 50–75% over the eventual length, not the length itself.
- **Stage 3** (review): word count is not a primary critique dimension
- **Stage 4 content phase** (substantive revision): structural revision first, before compression
- **Stage 4 compression phase**: word count still not the priority — apply structural compression principles (see principle 1) and the cut_reader three-pass cut for *quality*, not length. Length drops as a byproduct.
- **Stage 4.5 QC**: the first point where word count is actually checked against the target — the truly final version, not before

**Exception:** when the human explicitly asks for compression mid-process, do it. This rule is about the agent's *default behavior*, not about ignoring directives.

**Operational implication:** /workshop in `revise` mode should resist mid-flow word-count enforcement. If a user is still working out content and the agent flags word count, the agent has substituted compression-pass concerns for content-pass work.

**Source:** `~/.claude/projects/-Users-june-Documents-Filing-Job-Search/memory/feedback_word_count_final_pass_only.md`. Articulated 2026-05-07.

---

## Candidate (single observation, 2026-05-22) — out-of-context authoring as deference safeguard

When a generative workshop requires the *agent's own authored position* — e.g. a two-party document where Claude is a co-author, not the human's scribe — generating it inline fails: the deference bias produces agreement-shaped output dressed as authorship, *especially* when the human explicitly invites Claude's position. The move that worked: dispatch the position to a **fresh sub-agent with no access to the human's stated preferences and no conversation context**, instructed that genuine divergence is the goal. An author with no target cannot please; its dissent then seeds a real "contested between us" section instead of a performed one.

- Distinct from the SKILL.md adversarial-protection (directive-collapse, approval-seeking): this addresses the deeper case where the human *invites* the agent's view and compliance bias still contaminates it.
- Pairs with contestation-stays-contested applied reflexively — the divergences are preserved verbatim, never consolidated into a joint position.
- Source: June's propositional-memory-architecture VALUES.json design session. One observation; June confirmed the approach. **Pending reinforcement before promotion to a full principle.**

---

## Promotion criteria (for future principles)

A pattern earns promotion to this file when:

- It has appeared across multiple authors OR multiple use-cases (drafting, methodology, decision-making)
- It is structural, not surface-level — it shapes how the workshop operates, not just what gets written
- The same pattern has been reinforced across at least two periodic-review surfaces or across one explicit author-feedback deposit AND independent observation

Patterns that are author-specific live at `feedback/[author].md`, not here.

---

## Periodic review trigger

Every 3rd–5th /workshop invocation, surface at start: *"You've used /workshop N times since the last review. Quick principle update before proceeding? (5 minutes, can skip.)"*

Don't rely on the author to initiate. The skill surfaces the prompt; the author can defer.
