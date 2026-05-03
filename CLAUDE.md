# CLAUDE.md — cyborg-methodologies

## Project Description

Tools for human-AI collaborative research and writing, built from a critical theory position: computational and discourse-analytical work are the same intellectual move. Two tools:

**See also `INSIGHTS.md`** at this directory's root — system-wide methodological insights with cross-skill relevance. Read alongside this file when working in any skill in this repo.



- **voice-check** — Voice matching for human-AI collaborative writing. Calibrates a voice profile from writing samples, then serves three roles: (1) style guide agents read before drafting, (2) per-draft linter catching contamination patterns (jargon, hedges, padding), (3) post-revision learning loop where stylometry compares agent first-draft to human-revised final and updates the profile so future drafts are closer. Quantitative analysis + qualitative CDA checklist.
- **discourse-analysis** — General-purpose discourse analysis instrument and research partner. Quantitative profiling (clause types, process distributions, lexical density, stance markers) + framework-configurable qualitative analysis (Fairclough 3D, SFL, Appraisal, Hyland stance). Operates as both analytical engine and conversational research partner.
- **cgt-skill** (in design) — Constructivist grounded theory skill, in active design. Conceptual foundation in `cgt-skill/memos/` (33 numbered memos). The methodological architecture articulated in those memos has generalizable elements; see TODO below.

## Pending proposals

- **`voice-check/PROPOSAL_2026-04-29_revision_mode_and_relational_tracing.md`** — pending June review. Two additions distilled from a 2026-04-29 fine-editing session on her Wenner-Gren grant: (1) upward-and-outward / relational tracing as a drafting principle in SKILL.md (cites memos 010, 016, 022); (2) revision-mode protocol covering show-before-apply, mine-prior-versions enforcement step, verify-source-claims, resist-optimism-creep, affect-before-reasons, configurational-orientation-sentences. Architecture decision flagged for June: hybrid (workflow protocol in SKILL.md, two voice-contamination checks added to user profile). Subagent paused; resumable via id `a5c6483e42b441d7f` once architecture decided.

## TODO for next agent

**Cross-skill insight extension**: Read `cgt-skill/methodological_insights.md`. The insights captured there (format-as-anti-consolidation-priming, code-vs-coding-move artifact distinction, chunking-as-lens, defaults-as-starting-parameters meta-pattern, generative pattern matching) are general design moves that emerged from the cgt-skill build but apply across the cyborg-methodologies tools. Plan out concretely how each insight extends — or doesn't — to voice-check and discourse-analysis. Where it extends, propose specific architectural changes. Where it doesn't, articulate why (the failure to generalize is also data). The cgt-skill memos in `cgt-skill/memos/` provide the broader conceptual ground.

**Architectural location decision (parked from 2026-04-28)**: Many of the cgt-skill memos articulate principles that are not cgt-specific — they describe cyborg-collaboration patterns (collaborator stance, letter form, no silent suffering, compression bias, sub-distribution routing, defaults as starting parameters, generative pattern matching). Likely candidate: those memos move *up* an architectural level into a cyborg-methodologies systemwide foundation, with cgt-skill specializing them for grounded-theory work. Proposed shape — for evaluation, not decided:

- A meta-skill markdown (e.g., `cyborg-methodologies/PROTOCOLS.md` or similar) holds the cyborg-collaboration foundation memos as systemwide protocols.
- Global Claude CLAUDE.md (user's `~/.claude/CLAUDE.md`) gets a line pointing to this meta-skill, so it's always-loaded as an index of skills and protocols the instance is invited to call upon (lens-not-application stance — invited, not auto-applied).
- Each specific skill (voice-check, discourse-analysis, cgt-skill) inherits the foundation and adds its own specialized memos.
- /cgt becomes invokable as a learning-loop mechanism for complex iterative dialogic building work, not only for analyzing qualitative data — it's the cyborg-CGT *method*, applied as a build mode.

This decision deserves fresh attention. The cross-skill insight extension TODO above is upstream of this architectural decision — doing that work first will surface what actually generalizes vs. what's cgt-specific, which informs the location decision.

**Pre-build learning-loop audit (parked from 2026-04-28)**: Before any implementation work begins on cgt-skill (or other cyborg-methodologies tools), run an audit pass mapping where learning loops should live. The cgt-skill memos (especially 004, 005, 029, 032, 033) commit to learning loops as architectural infrastructure, but the specific places they fire need to be mapped concretely. The principle "more is more, except when it's not" applies — learning loops have real value but also overhead and noise. The audit identifies: (a) where learning loops would do real work, (b) where they'd be overhead with no value, (c) where they're already implicit in design (don't need to add), (d) where they're missing (need to add). Doing this audit before building is itself the design pattern — instrument the architecture for its own learning before building, not retrofit later.

**Voice-check Experiment 3 — two-pass pipeline (story pass + reorganization) is sketched, not finished (parked 2026-04-16, status check 2026-05-02)**: `voice-check/{story_pass.py,reorganization_pass.py,outline_pass.py,agent_caller.py,moves_library.py,run_current_pipeline.py,run_new_pipeline.py,run_experiments.py}` are pilot scripts for the A/B test specced in `voice-check/PIPELINE_REDESIGN_SPEC.md` (Experiment 3: does story-pass + moves-library + reorganization produce better first drafts than the current single-pass pipeline?). Initial outputs at `voice-check/outputs/{A_current_pipeline,B_story_to_draft,C_outline_to_draft,D_story_to_outline_to_draft}.md` were generated for review but no decision was reached. Committed as WIP 2026-05-02 to preserve the sketch in history; **do not use as the canonical drafting pipeline.**

The 2026-05-02 voice-check sociolinguistic expansion (diff analysis, paragraph/cohesion metrics, genre/voice stylometric separation, sequence-mode learning loop, and the qualitative CDA sweep as an explicit `--learn` phase) may have changed the calculus on whether the two-pass redesign is still load-bearing. **Before finishing Experiment 3, evaluate:** does the new sociolinguistic-aware learning loop close enough of the gap that the two-pass redesign is no longer the highest-leverage intervention? If yes, retire these scripts (or repurpose moves-library logic into qualitative checks). If no, finish the experiment: re-run the comparison with a current application, blind-evaluate outputs, and either merge the new pipeline into PIPELINE.md or close the proposal.

The 2026-04-29 `voice-check/PROPOSAL_2026-04-29_revision_mode_and_relational_tracing.md` is upstream of any decision here — it proposes a third path (revision-mode protocol + relational-tracing in SKILL.md) that may be more valuable than either single-pass or two-pass drafting. Resolve that proposal first; the two-pass scripts may become obsolete.

Both tools are built as Claude Code skills but the Python scripts work standalone.

## Current State (as of 2026-04-13)

- voice-check: functional, 260 tests passing. Three-layer profile architecture (base → user → genre):
  - `base.json` — universal norms: contamination patterns, permissive thresholds, 16 qualitative checks
  - User profiles are sparse (overrides + additions only), reference base.json
  - Genres are user-defined (skill ships with none). Created through guided conversation.
  - `--learn` mode updates user profile only, never modifies base
  - Auto-discovery: CLI finds profiles without explicit `--profile` flag
  - Front-loading detection: quantitative heuristic (heavy subjects) + qualitative check
  - Reflection sessions: periodic pattern review across writing sessions
  - `stylometry.py`, `perplexity.py`, `embeddings.py` — computational linguistics modules
- Next priorities: test three-layer architecture in real writing sessions, tune base thresholds from diverse users
- discourse-analysis: functional; active research project in `contexts/ai-slop.md` (12-text corpus on "ai slop" discourses, 7 findings accumulated)

## Project Index

```
cyborg-methodologies/
├── CLAUDE.md                         # This file
├── README.md                         # Top-level framing, install, usage
├── HANDOFF.md                        # Current state, next build priorities, pre-push checklist
├── .gitignore                        # Excludes profiles/*, .venv, contexts/ (privacy)
├── voice-check/
│   ├── SKILL.md                      # Claude Code skill — agent integration protocol, genre system
│   ├── README.md                     # User-facing docs
│   ├── writing_check.py              # Quantitative analysis + profile loading, calibration, --learn, --genre
│   ├── stylometry.py                 # Voice fingerprinting: Burrows' Delta, function words, vocab richness
│   ├── perplexity.py                 # Per-sentence perplexity via MLX local models
│   ├── embeddings.py                 # Sentence embedding similarity via fastembed
│   ├── profiles/base.json             # Universal base profile (ships with skill, no user data)
│   └── tests/
│       ├── test_voice_profiles.py    # 19 profile/analysis tests
│       ├── test_stylometry.py        # 71 stylometry tests
│       ├── test_perplexity.py        # 56 perplexity tests
│       ├── test_embeddings.py        # 68 embeddings tests
│       ├── test_genres.py            # 39 genre system tests
│       └── test_integration.py       # 24 multi-module orchestration tests
├── discourse-analysis/
│   ├── SKILL.md                      # Claude Code skill for /da
│   ├── discourse_profile.py          # Quantitative NLP profiling (spacy, textstat, lexicalrichness)
│   ├── frameworks/                   # Analytical framework protocols
│   │   ├── appraisal.md              # Martin & White Appraisal Theory
│   │   ├── fairclough-3d.md          # Fairclough 3D model
│   │   ├── hyland-stance.md          # Hyland academic stance/engagement
│   │   └── sfl.md                    # Systemic Functional Linguistics
│   ├── presets/                      # Domain-specific analysis presets (academic, ai-welfare, policy, etc.)
│   └── templates/project-context.md  # Template for per-project context files
└── contexts/
    └── ai-slop.md                    # Active project context: 12-text corpus, 7 findings
```

## Key Files

| File | Why it matters |
|---|---|
| `HANDOFF.md` | Full current state, next priorities, pre-push checklist |
| `voice-check/writing_check.py` | Quantitative analysis engine; profile loading; `--genre` flag; `--learn` mode |
| `voice-check/stylometry.py` | Voice fingerprinting engine; Burrows' Delta, calibration, learning loop |
| `voice-check/perplexity.py` | Perplexity scoring via MLX; calibration and learning |
| `voice-check/embeddings.py` | Sentence embeddings via fastembed; semantic drift detection |
| `voice-check/profiles/base.json` | Universal base profile: contamination patterns, permissive thresholds, 16 qualitative checks. Ships with skill. |
| `voice-check/SKILL.md` | Agent integration protocol: style guide, contamination linter, learning loop, genre system |
| `discourse-analysis/SKILL.md` | Full /da pipeline, anti-sycophancy protocols, research note format |
| `contexts/ai-slop.md` | Active discourse analysis project with accumulated findings |

## Agent Instructions

**Before editing writing_check.py**, read it in full — profile loading, calibration, and pattern application are tightly coupled. The profile JSON schema is the contract between Python and LLM layers.

**Skill directory**: All `.py` and `.md` files in `~/.claude/skills/voice-check/` are symlinks to this repo's `voice-check/` directory. The repo is the single source of truth. Profiles are local (not symlinked).

**Privacy constraint**: Before any push, run a grep for personal identifiers (usernames, real names, local paths) from repo root. Must return nothing. Keep the specific grep pattern in your local HANDOFF.md, not in this public file.

**contexts/ is gitignored** — research notes and project contexts contain accumulated findings and may contain corpus excerpts. Do not commit them.

**Voice-check workflow**: The SKILL.md defines a three-layer agent integration protocol — not a linter the user runs manually. Agents load the voice profile before drafting, self-check and self-correct contamination silently, and offer the learning loop at session end. The user sees clean drafts, not reports.

**Three-layer architecture**: Profiles merge base → user → genre. `base.json` has universal norms. User profiles are sparse (overrides only) and reference `"base": "base.json"`. Genres are user-defined and live in the user profile. `merge_profiles(base, user)` handles the merge; `load_profile()` auto-detects base references. `discover_profile()` auto-finds profiles when `--profile` is omitted.

**Computational linguistics modules** (`stylometry.py`, `perplexity.py`, `embeddings.py`): Each has calibrate/compute/compare/update functions. All participate in `--calibrate` and `--learn` with graceful fallback when dependencies are missing. None use the `apply_profile()` globals pattern — they take profile sections as arguments.

**Discourse analysis skill**: Anti-sycophancy and confirmation bias resistance are methodological requirements, not preferences. Do not silently resolve ambiguous codings. The tension between frameworks IS the finding.

**Install**: `pip install textstat nltk` (voice-check core); add `numpy scipy` for stylometry, `mlx mlx-lm` for perplexity, `fastembed` for embeddings, `spacy lexicalrichness` for discourse-analysis. Run `python3 -m spacy download en_core_web_sm`.
