# /critic-swarm low-stakes test plan

**Date scaffolded:** 2026-05-07
**Status:** Awaiting June's go-ahead before invocation.

---

## Why this test

Both /critic-swarm and /printpress were built today (2026-05-07) but neither has been invoked yet. The SPEC + SKILL files were thoughtfully designed but not battle-tested. Running /critic-swarm first on a low-stakes artifact validates the build before stress-testing it on a real application via /printpress.

Two birds with one stone:
1. Validates /critic-swarm's actual workflow (subagent dispatch, synthesis, LEARNING_LOG.md write)
2. Triggers the author-profile setup UX flow (since author-informed reviewer is profile-gated and no profile exists yet)

The author-profile setup is the one piece of /critic-swarm that requires June's input on first invocation — so this test is the right moment to wire it up.

---

## Recommended artifact: /workshop SPEC.md

**Path:** `~/Documents/GitHub/cyborg-methodologies/workshop/SPEC.md`

**Why this one:**

- **Self-test alignment.** /critic-swarm explicitly says (per INSIGHTS.md 2026-05-07 entry referenced in SPEC) that "any complex design artifact has the same designer-knows-too-much / reader-knows-too-little failure modes as an application." The /workshop SPEC is exactly that kind of artifact.
- **No deadline pressure.** This is internal infrastructure, not an application. If /critic-swarm crashes, returns garbage, or surfaces design problems, nothing time-critical breaks.
- **Real value either way.** If /critic-swarm works well, June gets honest critique of the /workshop design before integration with /printpress. If /critic-swarm misfires, that's data about what the build needs.
- **Stack is built.** The `design_spec` persona stack (`future build agent` + `skeptical architect`) is already extracted at `~/.claude/skills/critic-swarm/personas/design_spec/`. No setup needed.
- **Author-informed reviewer triggers profile setup naturally.** The author-informed reviewer reads from June's documented failure patterns, key contributions, etc. — perfect onboarding moment.

---

## Invocation

Bare invocation, letting /critic-swarm infer the stack:

```
/critic-swarm ~/Documents/GitHub/cyborg-methodologies/workshop/SPEC.md
```

Expected behavior per /critic-swarm SKILL.md § Workflow:

1. **Identify artifact** — reads the path argument.
2. **Determine persona stack** — should infer `design_spec` from artifact type (`.md` SPEC file in a skill folder).
3. **Load profile** — checks `~/.claude/skills/critic-swarm/profiles/`. None exists. Should offer to build one OR proceed without the author-informed reviewer.
4. **Brief the synthesis** — names what stack is running and why.
5. **Dispatch personas in parallel** — at minimum:
   - design_spec/future-build-agent
   - design_spec/skeptical-architect
   - always-runs/intelligibility
   - always-runs/jargon
   - always-runs/author-informed (only if profile is built or skipped)
6. **Synthesize** — cut list, convergent flags, threading suggestions, specialty insights, mechanical flags.
7. **Write LEARNING_LOG.md** — to the working directory of the artifact (`~/Documents/GitHub/cyborg-methodologies/workshop/LEARNING_LOG.md`).

---

## Author-profile setup (the UX moment June needs to drive)

Per /critic-swarm SKILL.md § Profile system:

> Stored at `~/.claude/skills/critic-swarm/profiles/[author].md`. Gitignored.
> 
> Fields: Key contributions / Key projects / Failure patterns / Source documents.
> 
> Bootstrap (optional): point the skill at documents (PDFs, CVs, research statements, briefing docs); it extracts a draft profile for the author to review and refine.

**On first invocation, the skill should ask June one of:**

- (a) "Build a profile from existing documents — point me at your CV, briefing doc, and one or two prior applications. I'll extract a draft profile you review and refine."
- (b) "Build a profile from a short conversation — I'll ask 5–8 questions covering contributions, projects, failure patterns."
- (c) "Skip the author-informed reviewer for this run. We'll build the profile later."

The recommended default is **(a) — bootstrap from documents** because June already has well-developed source material:
- `/Users/june/Documents/GitHub/profile/JUNE_BLOCH_AGENT_BRIEFING.md` (662 lines — agent briefing)
- `/Users/june/Documents/Filing/Job Search/Bloch_Application_Context.md` (drafting mistakes, common patterns)
- `/Users/june/Documents/Filing/Job Search/synthesis/Bloch_Publications_Portfolio.md`
- `/Users/june/Documents/Filing/Job Search/synthesis/Bloch_Teaching_Portfolio.md`
- A draft profile extracted from these would be high-fidelity on first pass; June refines.

The "Failure patterns" section maps cleanly to the seven common drafting mistakes already documented in `Bloch_Application_Context.md`.

**Profile should NOT include:**
- Contact info (irrelevant to author-informed reviewer)
- Voice/style notes (those live in voice-check)
- Application-specific positioning (those live in genre configs)
- Anything that duplicates the `~/.claude/skills/voice-check/profiles/[author].json` data

**Profile SHOULD include:**
- Specific contributions that get undersold
- Current projects (Reframe, Autograder, R&S book, voice-check)
- Documented failure patterns (compression-as-line-trimming, autograder-misdescription, timeline-inflation, etc.)
- Pointers to source documents for deeper reads

---

## What to watch for during the test

### Things going right
- /critic-swarm correctly infers `design_spec` stack
- Subagents dispatch in parallel, return useful critique
- Synthesis is structured (cut list first, convergent flags, etc.) — not just an aggregation
- LEARNING_LOG.md gets written
- Profile setup UX is reasonable (June can complete it without confusion)

### Things to flag if they happen
- Subagent prompts are brittle (returning empty / generic / unrelated output)
- Synthesis collapses into "summary of each reviewer" rather than relational threading
- Author-informed reviewer is scheduled before profile setup, causing confusion
- LEARNING_LOG.md is malformed or missing
- Cut list is generic ("be more concise") rather than specific (`passage → why → savings`)

---

## What to do with the output

The /workshop SPEC was built pre-use by design. Real critique from /critic-swarm IS the kind of pre-use data the SPEC was waiting for.

After the test:

1. **Triage convergent flags** — if multiple reviewers flag the same SPEC weakness, that's signal for a SPEC.md revision. Do this in /workshop revise mode (dogfooding twice).
2. **Note specialty insights** — single-reviewer flags are kept for consideration, not auto-fixed. Some will be the lens's gift.
3. **Update SKILL.md if needed** — if the SPEC revision changes load-bearing decisions, propagate to the SKILL.md.
4. **Log /critic-swarm's own performance** — was synthesis sharp? Were personas in-character throughout? This goes to `~/.claude/skills/critic-swarm/persona_perf.md` per SKILL.md § Update skill-global learning.
5. **Confirm profile setup worked** — if the profile feels off, refine it before next /critic-swarm use.

---

## Alternative artifacts (if /workshop SPEC isn't the right test)

In rough order of low-stakes-ness:

1. **/printpress SPEC.md** — same logic; design artifact; author has not yet stress-tested it. Tests `design_spec` stack and the author-informed reviewer simultaneously. Slightly higher stakes than /workshop SPEC because /printpress is closer to next real use.
2. **One of the new genre configs** (e.g., `non_academic_application.md`) — these were built by a subagent today; haven't been reviewed. Lower stakes than the SPECs because configs are easier to revise. But may be too narrow for `design_spec` stack and might want a custom reviewer mix.
3. **Job Search/`PIPELINE.md`** — would benefit from review but it's actively-edited by June; running adversarial review on a moving target is awkward.
4. **A finished prior cover letter** (e.g., a recently submitted academic CL) — uses the `academic_position` stack. This would test the production review pipeline but needs DEPARTMENT_PROFILE.md context. Bigger lift; not "small."

The /workshop SPEC remains the recommendation. It's small, self-contained, no external context needed, and the author-informed reviewer is the natural profile-setup trigger.

---

## Open question for June

Do you want to:

(a) Run /critic-swarm on /workshop SPEC.md as outlined, with author-profile bootstrap from existing source documents?  
(b) Run on a different artifact (one of the alternatives or something else)?  
(c) Skip author-profile setup for first run; profile later?  
(d) Defer the test entirely — push directly to a real application via /printpress?

Default recommendation is (a). All four are reasonable.
