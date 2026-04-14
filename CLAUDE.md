# CLAUDE.md — cyborg-methodologies

## Project Description

Tools for human-AI collaborative research and writing, built from a critical theory position: computational and discourse-analytical work are the same intellectual move. Two tools:

- **voice-check** — Voice matching for human-AI collaborative writing. Calibrates a voice profile from writing samples, then serves three roles: (1) style guide agents read before drafting, (2) per-draft linter catching contamination patterns (jargon, hedges, padding), (3) post-revision learning loop where stylometry compares agent first-draft to human-revised final and updates the profile so future drafts are closer. Quantitative analysis + qualitative CDA checklist.
- **discourse-analysis** — General-purpose discourse analysis instrument and research partner. Quantitative profiling (clause types, process distributions, lexical density, stance markers) + framework-configurable qualitative analysis (Fairclough 3D, SFL, Appraisal, Hyland stance). Operates as both analytical engine and conversational research partner.

Both tools are built as Claude Code skills but the Python scripts work standalone.

## Current State (as of 2026-04-13)

- voice-check: functional, 277 tests passing. All computational linguistics modules built:
  - `stylometry.py` — function word frequencies, punctuation ratios, vocabulary richness, Burrows' Delta
  - `perplexity.py` — per-sentence perplexity via MLX local models
  - `embeddings.py` — sentence embedding similarity via fastembed
  - Genre system — 8 genres with register-based threshold overrides in profile schema
  - `--learn` mode integrates all three modules for post-revision profile updates
  - SKILL.md rewritten around three-layer agent integration (style guide, contamination linter, learning loop)
- Next priorities: test genre system in real writing sessions, tune genre thresholds from actual use
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
│   ├── profiles/default.json         # Profile schema with genre overrides (8 genres)
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
| `voice-check/profiles/default.json` | Profile JSON schema with 8 genre overrides, stylometry/perplexity/embeddings sections |
| `voice-check/SKILL.md` | Agent integration protocol: style guide, contamination linter, learning loop, genre system |
| `discourse-analysis/SKILL.md` | Full /da pipeline, anti-sycophancy protocols, research note format |
| `contexts/ai-slop.md` | Active discourse analysis project with accumulated findings |

## Agent Instructions

**Before editing writing_check.py**, read it in full — profile loading, calibration, and pattern application are tightly coupled. The profile JSON schema is the contract between Python and LLM layers.

**Skill directory**: All `.py` and `.md` files in `~/.claude/skills/voice-check/` are symlinks to this repo's `voice-check/` directory. The repo is the single source of truth. Profiles are local (not symlinked).

**Privacy constraint**: Before any push, run a grep for personal identifiers (usernames, real names, local paths) from repo root. Must return nothing. Keep the specific grep pattern in your local HANDOFF.md, not in this public file.

**contexts/ is gitignored** — research notes and project contexts contain accumulated findings and may contain corpus excerpts. Do not commit them.

**Voice-check workflow**: The SKILL.md defines a three-layer agent integration protocol — not a linter the user runs manually. Agents load the voice profile before drafting, self-check and self-correct contamination silently, and offer the learning loop at session end. The user sees clean drafts, not reports.

**Genre system**: Profile schema has a `genres` section with register-based threshold overrides. `apply_profile(profile, genre="research_paper")` merges genre overrides on top of base thresholds. Genre selection is usually obvious from context. Eight genres defined: academic_position, tech_position, edtech_position, grant_application, research_paper, blog_essay, social_media, professional_correspondence.

**Computational linguistics modules** (`stylometry.py`, `perplexity.py`, `embeddings.py`): Each has calibrate/compute/compare/update functions. All participate in `--calibrate` and `--learn` with graceful fallback when dependencies are missing. None use the `apply_profile()` globals pattern — they take profile sections as arguments.

**Discourse analysis skill**: Anti-sycophancy and confirmation bias resistance are methodological requirements, not preferences. Do not silently resolve ambiguous codings. The tension between frameworks IS the finding.

**Install**: `pip install textstat nltk` (voice-check core); add `numpy scipy` for stylometry, `mlx mlx-lm` for perplexity, `fastembed` for embeddings, `spacy lexicalrichness` for discourse-analysis. Run `python3 -m spacy download en_core_web_sm`.
