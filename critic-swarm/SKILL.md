---
name: critic-swarm
description: "Adversarial reviewer swarm. Pass any artifact through multiple critical perspectives in parallel and get back a synthesis oriented toward improvement (cuts and substantive flags), not validation. Used standalone for any document needing critical review — design specs, agent prompts, research protocols, briefing docs, plans, papers, applications, instructions — and invoked by /printpress at Stage 3."
version: 0.1
spec: ~/Documents/GitHub/cyborg-methodologies/critic-swarm/SPEC.md
user_invocable: true
trigger: |
  Invoke when the user runs /critic-swarm, asks for adversarial review, asks to "stress-test" or "panel-review" a draft, or when /printpress hands off Stage 3. Also invoke proactively before finalizing any significant design artifact (skill spec, architecture doc, workflow, research protocol) — see INSIGHTS.md 2026-05-07.
---

# /critic-swarm — Adversarial Reviewer Swarm

The swarm passes an artifact through multiple critical perspectives in parallel and returns a synthesis oriented by **what to cut** and **what's load-bearing-but-at-risk**, not by validation.

These personas are **critics, not friendly readers.** Helpful encouragement is the default LLM mode and the failure mode this skill exists to correct against. Brief each persona to read with skepticism appropriate to their lens (panel reviewer's, hiring manager's, peer reviewer's, build agent's).

For full design rationale, see `~/Documents/GitHub/cyborg-methodologies/critic-swarm/SPEC.md`. This file is the executable workflow.

---

## When to use

Any artifact that benefits from multiple critical perspectives:

- **Design artifacts** — skill specs, architecture docs, workflows, plans (per INSIGHTS.md 2026-05-07: any complex design artifact has the same "designer-knows-too-much / reader-knows-too-little" failure modes as an application)
- **Application materials** — cover letters, research statements, grant proposals (when invoked from `/printpress` Stage 3)
- **Agent prompts** — prompt templates, skill instructions, agent briefs
- **Research artifacts** — papers pre-submission, methodology designs, protocols
- **Author-informed solo passes** — when you want a single deep read against the author's own work and documented failure patterns

---

## Hard requirement

The strength of this skill is in robustly defined personas that provide open-ended reads through a situated lens. This allows critics to surface issues that we missed and did not think to ask. 

Rich prompting should lie in building the *personas themselves* – their actual read should be *open ended* so they can surface issues beyond what we can anticipate in advance.

**FAILURE MODE TO AVOID:** priming subagent critics to look for specific issues enacts two failures at once:
 - *Circular logic fallacy:* It constrains what critics will be able to surface in advance, before they even look at the document. We will no longer be able to identify issues we didn't think to prime for. 
 - *Redundancy:* If there is an impulse to prime a critic to look at a specific set of concerns, then that means we have already identified the concern and do not need to run the critic swarm to find it. Those issues should be fixed *before* running the swarm. 

In practice, this failure mode results in running an expensive swarm and receiving minimal useful information – wasting resources and stripping the skill of it's very purpose.

**KEY PRACTICE TO ADHERE TO:** Rather than foreclosing what the critics look for, priming belongs in designing the personas themselves. For example, "feminism" will return generic critiques aligned with white, liberal, mainstream feminism – designing a critic to read like specific scholars, from specific intellectual traditions, with rich and open-ended intellectual moves provides sharper feedback.

**TESTS FOR SWARM DESIGN:** 
- Are the critics tailored to mimic the perspectives of the people who will actually review the finished document? *If no: revise – not run ready
- Are prompts written to prime readers to to look for specific issues, concerns, etc. in the draft? *If yes, address those issues before running critic swarm. Then revise  – not run ready.*
- Do the prompts foreclose the critic from returning feedback that we didn't initially think to ask for? *If no, revise – not run ready*
- Does the swarm design adhere to the "How to design the lenses" list in step 4b? *If no, revise – not run ready

---
## Invocation modes

| Form | Behavior |
|---|---|
| `/critic-swarm [artifact-path]` | Run the swarm with a default persona stack inferred from artifact type. If type is ambiguous, ask. |
| `/critic-swarm [artifact-path] --personas [stack-name]` | Run with a named stack from `personas/[stack-name]/`. |
| `/critic-swarm [artifact-path] --personas p1,p2,p3` | Explicit persona list (mix-and-match across stacks). |
| `/critic-swarm [artifact-path] --reviewer [single-persona]` | Single reviewer only. **Skips the always-runs** (intelligibility, jargon, author-informed). User explicitly asked for one persona; respect that. To get the always-runs alongside, invoke the full swarm. |

Default stacks (from SPEC.md):
- `design_spec` — future build agent + skeptical architect
- `academic_position` — search committee anchored to actual faculty (requires `DEPARTMENT_PROFILE.md`)
- `grant_fellowship` — program officer + panel composition (requires funder profile)
- `non_academic_application` — hiring manager + culture-fit reader + ATS reviewer
- `peer_review` — editor agent (selects panel) + 2–3 subject reviewers + source validator
- `agent_prompt` — fresh build agent + skeptical user (red-team)
- `research_protocol` — methodologist + skeptical reviewer

When `/printpress` invokes the skill, it passes the stack and the relevant context (posting, funder profile, department profile) directly — the swarm doesn't need to know about drafting.

---

## Required reading at invocation

Read these BEFORE dispatching any persona. They shape how the swarm reasons, especially in synthesis.

1. **`~/Documents/GitHub/cyborg-methodologies/INSIGHTS.md`** — entry **2026-04-29** (relational tracing vs. similarity clustering) and entry **2026-05-07** (swarm as design review method). Synthesis is *relational threading*, not feature-aggregation. Reading these is what the difference depends on — without them, synthesis collapses to "list of issues each reviewer found," which loses the load-bearing signal.
2. **`~/Documents/GitHub/cyborg-methodologies/cgt-skill/memos/006_conversation_is_the_analysis.md`** and **`016_openings_and_takings_up.md`** — the dialogic principles behind the synthesis prompt shape. Why "what does the swarm open up about this artifact?" produces analysis that "summarize the document" cannot.
3. **The persona files for the selected stack** — `~/.claude/skills/critic-swarm/personas/[stack]/` (note: persona library is being extracted from `/Users/june/Documents/Filing/Job Search/templates/adversarial_reviewer_personas.md`; if the stack folder isn't present yet, fall back to that file).
4. **The author profile, if author-informed reviewer is in the stack** — `~/.claude/skills/critic-swarm/profiles/[author].md` (gitignored; local only). If no profile exists, ask the author to point at one or build one; skip the reviewer if declined.
5. **The working directory's `CLAUDE.md`** — for finding source materials, archives, and project paths the swarm may need (especially for `peer_review` source validator). Project organization varies; don't assume.

---

## Always-runs reviewers

These run on **every invocation regardless of stack**. They sit alongside the stack-specific personas.

- **Intelligibility reviewer** — cold reader; flags every place they'd stop, re-read, or get confused. Designed to detect, not enumerate. The general case is "reader can't follow"; common shapes (post-compression logical breaks, broken reference tracking, transition incoherence, front-loaded sentences, "off" passages, through-line invisibility) seed the reading without exhausting the failure space. Reports: passage → the confusion → what the reader would need.
- **Jargon reviewer** — venue-aware. For interdisciplinary work, reads from BOTH (or all) field perspectives — terms obvious in one camp can be opaque in the other, in both directions. Identify the camps from the artifact and venue, then check against each. Reports: term → which camp it fails for → what they hit → suggested replacement or in-text gloss.
- **Author-informed reviewer** — runs *only if a profile exists* (or the user supplies one). Reads from the inside; default move is **CUT**, not ADD. Finds redundancy, overlap, the author's documented failure patterns, underselling, **overclaiming** (and the systemic pattern when source materials propagate it), and factual inaccuracies. Output: cut candidates + (rare) threading suggestions where payoff justifies cost.

---

## Workflow

### 1. Identify the artifact

Path argument or current context. If neither is clear, ask.

### 2. Determine the persona stack

In order of preference:
- Explicit `--personas` / `--reviewer` argument.
- Inference from artifact type and surrounding context (e.g., a `SPEC.md` in a skill folder → `design_spec`; a draft in a `Job Search/[App]/` folder → `academic_position` or `grant_fellowship` based on POSTING.md).
- If ambiguous, ask the user with `AskUserQuestion`. Don't guess on stack — wrong stack produces wrong critique.
- Reviewer personas should be based on the people who will actually review or read the document. For example, for scholarship, what kinds of scholars might be peer reviewers? For grants, are there named reviewers – and if so, build personas around them – if not, what kinds of scholars or practitioners would reviewers be?

### 3. Load profile (if applicable)

If the stack includes `author-informed` or the user passed `--reviewer author-informed`: check `~/.claude/skills/critic-swarm/profiles/`. If exactly one profile exists, use it. If multiple, ask. If none, offer to build one or proceed without the author-informed reviewer.

### 4. Brief the synthesis up front

Note in the working context:
- What stack is running and why.
- Which always-runs are included.
- What context the personas will receive (posting, profile, department/funder profile, source materials).

This gives synthesis its bearings before the personas return — synthesis is the main agent's job, not a subagent's.

### 4b. Propose the critic design and confirm with the author — gate before dispatch (ALL stacks)

**Do not dispatch any persona until the author has signed off on the critic design.** This gate previously ran only for `peer_review` (the editor agent proposing a panel); it now runs for **every invocation**.

*Why this gate exists:* the recurring failure mode is an instance designing and framing the critic lenses on its own default — foreclosing the review before anyone has looked at the artifact — so the swarm returns information that isn't the information the author needs, and the whole run has to be redone. The author confirming the design *before* dispatch is where instance-default foreclosure gets caught. It is cheaper than a re-run and it is where the author's values enter the review.

Propose the design in a short, scannable form (`AskUserQuestion`, or inline if quick):
- **Which lenses** will run — stack personas + always-runs.
- **What each is oriented toward** — one line each, an *orientation*, not a checklist (see "Adversarial orientation" below).
- **What reading/context each receives** — the artifact, the project's values/guards, posting/profile, source registry.
- **Confirm at least one fully-open lens is present** — "what's wrong here that we didn't think to ask about?" (INSIGHTS.md 2026-06-14). Pre-named-flaw lenses find the named flaws and miss the structural one.

The author can add, cut, reframe, or redirect any lens, or hand you the framing directly. Dispatch only after sign-off. (For `peer_review`, the editor-proposes-panel step *is* this gate — keep it as-is.)

**Hard gate: Run the Hard Requirement tests BEFORE presenting the design to the author.*

**How to design the lenses — disciplines, read before proposing:**
- **Lead with WHY.** Each lens carries the purpose it serves, so the critic fits the underlying reason rather than executing a literal instruction.
- **Orientation, not checklist.** "You are X, reading as Y" surfaces what the prompter didn't anticipate; "evaluate these 7 things" returns exactly seven.
- **No verification framing — mirror real readers (THE persistent, expensive failure mode).** Orientations that ask a critic to *verify / check / confirm* something ("does it cover the six criteria?", "is the register right?", "is the claim held as a hypothesis?") — or that pre-define the output shape — produce binary confirmations that are *easier to fold back into the doc than they are useful*, and force a second swarm to get the actual reading. A critic is not a checker; binary framing gets you nothing. Orient each lens to **read the source material and the artifact the way the actual reader would, react as themselves, and say how *they* would approach this work and what they'd do differently** — answering in their own categories, not ours. *Anti-pattern:* "Verify the plan covers all six criteria / holds mechanism claims as hypotheses." *The form that pays:* "You are an SSRC screener — read these source materials and this plan and react as you would to a real submission, including how you'd build this application if it were yours." The author's named worries (overclaim, register) are context a critic *may* surface on its own — never the question you hand it. This is the swarm's whole reason for existing; an instance that narrows it has defeated the tool.
  - **The one exception — named, required components, AND published evaluation criteria.** When the artifact must contain *specific named things* — a grant's required materials, word/page limits, mandated sections, an application's checklist — **exactly one scoped lens SHOULD literally check those are present** (fold it into the program-officer / screener lens, or run a dedicated compliance reviewer). A missing required component is a hard fail no amount of generative reading catches. This compliance check is bounded to the *named, externally-required* list; it does NOT license verification-framing on the analytical lenses, and it is never the whole of any lens's job. Mirror-the-reader is the rule; the named-requirements check is the carve-out.

    **Extended 2026-08-09 to cover PUBLISHED EVALUATION CRITERIA — a distinct thing, and the gap this rule had.** Required components answer "did you include a CV." Published criteria answer "does this address the axes they score on." Many funders publish theirs, and where they do they **outrank every general heuristic in the drafting system** — they are the actual rubric, stated by the people deciding. ACLS, for example, publishes four: clarity, intellectual/social significance, quality, and feasibility (specified as training, past experience, plan of work) — and notably does *not* list originality. A proposal optimized for originality is optimized for a criterion that funder does not use.

    So: **where a funder publishes evaluation criteria, the scoped compliance lens maps the artifact against them, criterion by criterion, and reports which are addressed, which are gestured at, and which are absent.** This is legitimate under the carve-out for the same reason the required-materials check is — the criteria are named, external, and verifiable, not the swarm's own invention. It is still one bounded lens; the analytical personas stay open and must not be handed the criteria list.

    ⚠ Two guards. **Do not let criteria-mapping become the whole review** — a proposal can address every published criterion and still be weak, and Lamont's panel ethnography found panelists routinely evaluate on grounds beyond the formal criteria (diversity considerations, "elegance," and the applicant's fit with the batch they landed in). **And do not invent criteria** — if the funder publishes none, this lens does not run, and the swarm does not substitute a generic rubric. Absence of published criteria is itself information about how idiosyncratic the review will be.
- **Don't foreclose categories.** Don't pre-name the flaws to look for — that limits findings to what could be anticipated *without* the artifact. Let each critic answer in its *own* categories, and name the foreclosure failure-mode *to* the critic so it resists narrowing.
- **Project values drive the frame, not the instance's default.** Derive the lenses from the artifact + the project's stated values/guards (load them) — never from a generic reviewer-persona grid or the statistical norm of tightly-regulated human prompting. The standard is "what is *this* artifact trying to be," not "how does it score on our pre-baked grid."
- **Open lens, not closed container.** Don't impose a fixed severity/score schema (Critical/Important/Minor, 1–5) on the output — that re-flattens the situated findings the open lens just surfaced. Let synthesis thread by load-bearing-ness (step 6), not by a rating grid.

### 5. Dispatch personas in parallel as background subagents

Each subagent gets a self-contained spec:
- Persona prompt (orientation, **not checklist** — per SPEC: "designed to detect, not enumerate")
- Path to the artifact (the actual file; not a paraphrase)
- Path to the actual posting/funder profile/department profile (when relevant — per SPEC, personas read the actual posting, not an imagined ideal one)
- Path to source materials registry if `peer_review` (look in working directory's `CLAUDE.md`; if absent, ask the author)
- Adversarial-orientation framing: "you are X, you read this as Y, with Z's skepticism" — not "evaluate these 7 things"
- Output format: cut candidates + concerns + load-bearing passages worth protecting

For `peer_review`: the **editor agent runs first**, before reviewers — this is `peer_review`'s instance of the 4b gate. Reads article + target journal + bibliography, proposes a 3–4 reviewer panel with rationale, **shows the panel to the author for override**, then reviewers launch.

Run all reviewer subagents in parallel (independent tasks; same artifact, different lenses).

### 5b. Mid-review author input — invoke `/workshop ask` (if needed)

If a reviewer surfaces a need for author input that the artifact alone can't resolve — a fact only the author has, a story-from-experience that would settle a flag, a clarification on what's load-bearing — invoke `/workshop ask` for a small dialogic ask. After the ask resolves, integrate the answer into synthesis.

This is rare but real. Examples:
- Author-informed reviewer flags a likely inflated number; synthesis can't verify without the author. → `/workshop ask` with the specific claim.
- Subject-area reviewer can't tell if a methodological move is a deliberate choice or an oversight. → `/workshop ask` with the specific passage.
- Convergent flag points to a missing piece (a story, a connection) the author probably has but didn't include. → `/workshop ask` with the gap framed openly.

Use sparingly. Most reviewer flags are addressable in synthesis directly. /workshop ask is for the cases where an answer changes the synthesis itself.

### 6. Synthesize when subagents return

Done in the **main agent's context, not a separate subagent.** Synthesis depends on holding all reviewers' outputs and the artifact in one window so relational threading can trace what's load-bearing across them.

Synthesis is **oriented by relational threading** (per INSIGHTS.md 2026-04-29):
- Don't aggregate or average. Three middle-rankings + two upper-middle ≠ "middle." The two upper-middle saw something; the others saw something else. Preserve variance.
- Trace what connects across reviewer outputs — what's *taken up* by multiple reviewers, what's *opened* by one and unaddressed by others. Convergent ≠ duplicate; convergent = the same load-bearing problem visible through different lenses.
- The swarm can but used to identify cuts in addition to things needing to be added – different contexts may require leaning more towards one side or the other. Cuts: cuts allow the strongest material in the draft to shine – even cutting *good* material is beneficial if it leaves only *exellent* material. Additions gate: avoid the impulse to add everything – this can *weaken* the draft by creating sprawl – additions should only ever *enhance* the overall document, not simply answer a specific critique raised by a reviewer. **Carve-out for build / design-spec artifacts (2026-06-19, PMA): On a build spec or design doc, losing carefully-worked design is the expensive failure (re-deriving it later is the drift the work guards against) — cut only genuine redundancy or overclaim, never designed substance. The cut-default is calibrated to application drafts under a length budget; don't import it into design contexts.

**Required test for additions:** Does this change enhance the overall quality of the draft (when read as a whole) for the specific audience it is intended for? All additions must be answerable "yes."

### 7. Output the synthesis (structured)

This order matters — most revision work lives in the cut list, so it leads.

1. **Cut list** — specific, actionable, start here. Format: `passage → why it can go → estimated word savings`.
2. **Convergent flags** — 3+ reviewers flagged this. High priority. Name what's load-bearing-but-at-risk.
3. **Threading suggestions** — from author-informed reviewer (rare; only when payoff justifies the cost).
4. **Specialty insights** — divergent flags (single reviewer). Consider, don't average. These are the lens's gift.
5. **Mechanical flags** — jargon, intelligibility breaks. Address before save.

Praise that converges across reviewers marks **load-bearing passages** — call these out so revision protects them. Advisory, no enforcement.

### 8. Write to LEARNING_LOG.md

In the **working directory** (the directory containing the artifact, or the project root for that artifact). Append an entry with:
- Date, artifact path, stack used, personas dispatched
- Corrections the author made to the swarm design
- Convergent flags surfaced
- Divergent flags surfaced
- What the author addressed vs. held
- Persona performance notes (which surfaced sharp critique, which were shallow)
- **Cross-stack generalization flag** — if a pattern observed here might apply to other stacks, tag it. Periodic review consolidates these into skill-global principles.

### 9. Update skill-global learning (when warranted)

Per SPEC Tier 2:
- `~/.claude/skills/critic-swarm/stacks/[stack].md` — stack refinements
- `~/.claude/skills/critic-swarm/persona_perf.md` — persona performance data
- `~/.claude/skills/critic-swarm/principles.md` — confirmed cross-stack generalizations (only after the same pattern appears across multiple stacks)

**Periodic stack review** — after every 3rd–5th use of a stack, surface at invocation: *"You've used [stack] N times since the last review. Quick stack update before proceeding? (5 minutes, can skip.)"* Don't rely on the author to initiate.

---

## Profile system (for author-informed reviewer)

Stored at `~/.claude/skills/critic-swarm/profiles/[author].md`. Gitignored. Same convention as voice-check profiles.

```markdown
# Author profile — [Name]
# Last updated: [date]

## Key contributions
<!-- What this person has done that tends to get undersold. Specific. -->

## Key projects
<!-- Current and recent work. Source paths if they exist. -->

## Failure patterns
<!-- What goes wrong in their drafts. Compression casualties, dropped connecting context, common drafting mistakes. -->

## Source documents
<!-- Paths to fuller briefing docs (CV, research statement, briefing doc). -->
```

**Bootstrap** (optional): point the skill at documents (PDFs, CVs, research statements, briefing docs); it extracts a draft profile for the author to review and refine.

---

## Adversarial orientation — the constitutive instruction

When briefing each persona, the framing is:

> You are [X]. You are reading this as [Y], with the skepticism appropriate to [your lens — panel reviewer / hiring manager / peer reviewer / cold reader / build agent]. You are NOT a friendly reader. Helpful encouragement is the default mode, and your job is to pull against it. What you attend to as you read is yours to decide.

Resist the urge to give personas specific evaluation questions. Per SPEC: a prompt that says "evaluate the following 7 things" produces seven evaluations; a prompt that says "you are X, you read this as Y" produces analysis the prompter didn't anticipate — including the things that turn out to matter. See "Hard Requirement" section.

Constrain only what would otherwise drift: in-character throughout, no copy-editing, commit to a panel decision (when applicable), word-count cap.

---

## Synthesis prompt shape (generative, not compressive)

When the personas return, the synthesis prompt to yourself is:

> **What does the swarm open up about this artifact?** What does each reviewer's lens reach toward that the others don't? Where does one reviewer's flag *take up* what another reviewer *opened*? What's load-bearing here — what's redundant — what should be cut?

Not: "summarize each reviewer's findings." Summary collapses variance. The dialogic prompt (per memo 016) holds the *relations* between reviewer outputs so threading can surface what no single reviewer flagged alone.

---

## Quick reference

| Step | Reads | Writes |
|---|---|---|
| Invocation | INSIGHTS.md, persona files for stack, working dir CLAUDE.md, profile (if applicable) | — |
| Dispatch | artifact, posting/profile context | (subagent contexts) |
| Synthesis | all subagent outputs + artifact | structured synthesis to user |
| Per-session log | — | `[working dir]/LEARNING_LOG.md` |
| Skill-global (when warranted) | prior session logs | `~/.claude/skills/critic-swarm/stacks/[stack].md`, `persona_perf.md`, `principles.md` |

---

## Relationship to /printpress

`/printpress` invokes `/critic-swarm` at Stage 3 with the stack and context (posting, funder/department profile, source materials registry) prefilled. The swarm executes and returns synthesis; `/printpress` integrates findings into its revision pass. Standalone invocations don't go through `/printpress`.
