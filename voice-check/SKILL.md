---
name: voice-check
description: "Voice integration for human-AI collaborative writing. Maintains a sociolinguistic voice profile that agents use as a style guide during drafting, as a contamination linter, and as a learning loop that improves from human revision patterns. Run /voice-check setup to create a profile from writing samples. Run /voice-check learn after a revision session to update the profile."
user_invocable: true
trigger: /voice-check, /writing-check, or when user asks to check a draft's voice
---

# Voice Check — Agent Voice Integration

Voice-check is a sociolinguistic voice profiling system for human-AI collaborative writing. It does three things:

1. **Style guide** — Agents read the voice profile before drafting and write in the user's voice from the start. The profile captures how the writer actually writes: sentence rhythm, punctuation habits, vocabulary density, function word patterns, register, argumentation style, and what they never sound like.

2. **Contamination linter** — After drafting, the agent self-runs quantitative checks and silently corrects contamination patterns (hedge words, corporate jargon, narrative padding, self-aggrandizing frames). The user sees a clean draft, not a report of what's wrong with it.

3. **Learning loop** — After the user revises a draft through conversation, the system compares the agent's first draft to the human's final version. It identifies what shifted and updates the voice profile so future drafts are closer. The human's revision choices are the ground truth for what their voice IS.

The user never needs to run a voice check to generate fixes. The agent uses the profile to write well and learns from how the user edits.

## Quick reference

| Command | What it does |
|---|---|
| `/voice-check setup` | Create your voice profile from writing samples (auto-runs on first writing task if no profile exists) |
| `/voice-check learn` | After a revision session: compare first draft to final, update profile |
| `/voice-check [file]` | Optional: run standalone diagnostic on any document |

---

## Agent integration protocol

**This is the primary content of this skill.** Any agent helping with writing should follow this protocol.

### Before drafting

1. **Check for voice profile.** Look in `~/.claude/skills/voice-check/profiles/` for non-default profiles. If exactly one exists, use it. If multiple exist, ask which one. If none exists, run setup (see Setup section below).

2. **Read the profile.** Load the full profile JSON. Read these sections carefully before writing anything:
   - `stylometry.style_notes` — plain-language summary of the writer's voice fingerprint (sentence rhythm, punctuation, vocabulary density, function word patterns)
   - `qualitative` — CDA checklist items describe what makes this writer's voice distinctive and what to protect
   - `genres.[genre].description` — if the current document matches a genre, read its description and genre-specific qualitative checks
   - `patterns` — the anti-pattern lists (hedges, jargon, padding) tell you what words this writer never uses

3. **Select genre.** Identify which genre the current writing task falls into from the profile's `genres` section. Genre selection is usually obvious from context (the user says "help me with this cover letter" or "draft a research statement"). If ambiguous, ask. The genre determines threshold tolerances and expected structural moves.

### During drafting

4. **Write in the user's voice.** Use the style notes and qualitative checks as active guidance, not just post-hoc criteria. Match their sentence rhythm, vocabulary register, argumentation style, and relationship with the reader. Avoid everything in the anti-pattern lists.

5. **Self-check after drafting.** Run the quantitative analysis on your own output:
   ```bash
   python3 writing_check.py DRAFT_PATH --profile PROFILE_PATH --genre GENRE_NAME
   ```
   If `--genre` is specified and the genre defines a `word_count_target`, that target is used automatically (no need for `--target` unless overriding).

6. **Self-correct contamination silently.** If the check flags voice contamination (hedge words, corporate jargon, narrative padding, self-aggrandizing frames, product-description appositives), fix them before presenting the draft to the user. These are binary — "leveraging" is always wrong in this voice regardless of context. Do not tell the user you found and fixed contamination. Just present clean text.

7. **Surface structural/qualitative findings as suggestions.** If the check flags structural issues (long sentences, em-dash density) or if you notice qualitative concerns from the CDA checklist, mention them as suggestions the user can accept or reject. These are judgment calls, not automatic fixes. Frame as: "I noticed X — want me to adjust, or is that intentional?"

### After revision

8. **Offer the learning loop at session end.** When the user finishes revising a document (the conversation is wrapping up, or they say they're done), ask: "Want me to run the learning loop? I'll compare my first draft to your final version and update the voice profile so I draft closer to your voice next time."

9. **Run the learning loop.** If the user agrees (or during end-of-session maintenance):
   ```bash
   python3 writing_check.py --learn FIRST_DRAFT FINAL_DRAFT --profile PROFILE_PATH
   ```
   This compares stylometry (and perplexity/embeddings if available) between the two versions, identifies what shifted, and updates the profile via exponential moving average. Report the key shifts to the user — e.g., "Your revisions shortened sentences and added semicolons. Profile updated."

   **Important:** Save the agent's first draft to a temp file before beginning the revision conversation. You need both versions for the learning loop.

---

## Setup

Setup creates the voice profile. It runs automatically the first time an agent starts a writing task and no profile exists — the user does not need to remember a command.

If the user explicitly runs `/voice-check setup`, follow this same flow.

### Prerequisites

```bash
pip install textstat nltk
```

Optional (for richer fingerprinting): `numpy`, `scipy` (stylometry), MLX + local model (perplexity), `fastembed` (embeddings). The tool degrades gracefully — each module is optional.

### Step 1: Gather writing samples

Ask the user for 3-10 samples of writing in the voice they want to maintain. These should be:
- **Their own revised/final writing** (not first drafts, not AI-generated text)
- **Writing they're proud of** — this is the voice to protect
- **Across genres if possible** — samples from different document types give a richer voice fingerprint. The base profile captures what's stable across contexts; genre-specific traits are configured separately.

**File formats**: `.md`, `.txt`, `.html`. For Google Docs: File > Download > Plain Text. For Word: Save As > Plain Text. For PDF: copy-paste into a `.txt` file.

Save all samples to a single directory. If the user pastes text directly, save each to a temp `.md` file.

### Step 2: Quantitative calibration

```bash
python3 writing_check.py --calibrate PATH_TO_SAMPLES/ -o ~/.claude/skills/voice-check/profiles/USERNAME.json
```

This analyzes sentence structure, em-dash usage, hedge frequency, and other metrics across the samples, then generates a profile JSON with computed thresholds. It also runs stylometry calibration (function word frequencies, punctuation ratios, vocabulary richness, sentence length distribution, Burrows' Delta baseline) and any other available modules (perplexity, embeddings).

### Step 3: Qualitative voice extraction

**You (the agent) read ALL the writing samples in full and extract the writer's voice characteristics.** The user does not do this part.

**A. Voice characteristics** — analyze the samples for:
1. Sentence-level mechanics: length, rhythm, punctuation habits (em-dashes, parentheticals, semicolons)
2. Lexical choices: register, jargon (whose?), vocabulary density
3. Argumentation style: evidence-first, authority-first, narrative, consequence? Accumulation, contrast, escalation?
4. Relationship with reader: direct address, institutional distance, authoritative, collegial?
5. What they do NOT sound like: what would be wrong? (Corporate jargon? Academic hedging? Inspirational cliches? False modesty?)

**B. Anti-patterns** — based on the voice analysis, write regex patterns and add to the profile:
- Words/phrases this writer never uses → `patterns.corporate_jargon` or custom category
- Framing patterns that contradict their voice → `patterns.self_aggrandizing` or `patterns.narrative_padding`
- The user does NOT write regex. You do.

**C. Qualitative CDA checklist** — build user-specific checks based on what you found. The pattern: identify something distinctive about how this person writes, then write a check that protects it. If they're blunt, write a check that flags hedging. If they use specific theoretical language, write a check that flags generic substitutes.

Example:
```json
{
  "id": "constructivist_epistemology",
  "category": "ideational",
  "name": "Constructivist epistemology",
  "instruction": "Are findings framed as emerging from practice/conditions or as discoveries? Rejects discovery narratives on epistemological grounds."
}
```

### Step 4: Genre configuration

Ask the user which genres they write in. For each genre:
1. Review the genre stub in the profile (see Genre System below)
2. Adjust `threshold_overrides` based on what you observed in the samples and what the genre demands
3. Set appropriate `genre_moves` for the document type
4. Add genre-specific qualitative checks if relevant

If the user isn't sure, configure the genres that are obvious from their samples and tell them new genres can be added later.

### Step 5: Verify and activate

Run the tool on ONE of the user's own good writing samples:
```bash
python3 writing_check.py GOOD_SAMPLE --profile PROFILE_PATH --genre LIKELY_GENRE
```

What to look for:
- **Few or no voice flags** — if their own good writing triggers voice flags, the patterns are too aggressive. Adjust.
- **Reasonable structural flags** — some long sentences in good writing is fine. If many, thresholds may be too tight.
- **Zero flags is suspicious** — thresholds may be too loose to catch AI contamination. Tighten.

Show the user the results and adjust until the profile correctly distinguishes their voice from generic AI output.

Tell the user:
- Where the profile lives
- That agents will use it automatically during writing tasks
- That running `/voice-check learn` after revision sessions makes the profile better over time

---

## Genre system

Voice is largely stable across genres — function word frequencies, punctuation habits, vocabulary richness, and core argumentation patterns don't change between a cover letter and a research paper. What changes is **register**: threshold tolerances, expected structural moves, and which patterns are appropriate for the audience.

The profile separates these concerns:

**Base profile** (shared across all genres):
- Stylometry fingerprint (function words, punctuation, vocabulary richness, sentence distribution)
- Core anti-patterns (corporate jargon, narrative padding — contamination in every genre)
- Core qualitative CDA checks (transitivity, concept scope, referential strategy, etc.)
- `style_notes` — plain-language voice summary

**Genre overrides** (sparse — only what differs from base):
- `word_count_target` — default target for this document type
- `threshold_overrides` — only the thresholds that differ (genre override → base → default)
- `genre_moves` — expected structural moves for this document type
- `qualitative` — genre-specific CDA checks that supplement the universal ones

### Supported genres

| Genre key | Description | Typical register shift |
|---|---|---|
| `academic_position` | Research statements, teaching statements, DEI statements, cover letters for academic jobs | Formal but personal; institutional framing; Swales moves; consequence-led argumentation |
| `tech_position` | Cover letters, personal statements for tech roles | More direct; results-framed; tech jargon tolerance higher |
| `edtech_position` | Materials for roles bridging education and technology | Hybrid register; pedagogical + technical vocabulary both appropriate |
| `grant_application` | Grant proposals, funding applications | Highly structured moves; measured claims acceptable (hedging has different valence here) |
| `research_paper` | Academic papers, journal articles | Densest register; longer sentences OK; high lexical density; disciplinary terminology expected |
| `blog_essay` | Public-facing essays, blog posts, longform commentary | Argumentative, personal voice; accessible but not dumbed down |
| `social_media` | Posts, threads, short-form public writing | Short, punchy, conversational; near-zero hedge tolerance |
| `professional_correspondence` | Emails, outreach, networking messages | Brief, direct, relationship-maintaining |

### How genre selection works

1. **Agent infers from context.** When the user says "help me draft a cover letter for this faculty position," the genre is `academic_position`. This is usually obvious.
2. **Explicit selection.** The user can specify: `/voice-check --genre research_paper`.
3. **CLI flag.** `python3 writing_check.py draft.md --profile p.json --genre research_paper`
4. **Fallback.** If no genre is specified or inferable, use base profile thresholds with the default word count target (1200).

When a genre is selected:
- Its `threshold_overrides` merge on top of base thresholds (genre values win)
- Its `word_count_target` becomes the default (overridden by explicit `--target`)
- Its `genre_moves` guide structural analysis
- Its `qualitative` checks run in addition to universal checks

---

## Diagnostic mode (optional)

For standalone analysis of any document — writing not produced through a Claude drafting session, or when the user wants to explicitly check a piece.

```bash
python3 writing_check.py PATH_TO_DRAFT --profile PROFILE_PATH [--genre GENRE] [--target WORDCOUNT]
```

### Quantitative analysis

Read the output. Note all flags. Voice flags (hedges, jargon, padding) indicate contamination. Structural flags (long sentences, em-dash density) may be deliberate style.

### Qualitative CDA analysis

Load qualitative checks from the profile. Run each against the draft text.

**Universal checks** (always run):

1. **Transitivity**: Material:Relational process ratio in topic sentences.
2. **Concept scope**: Concepts as architecture vs. vocabulary.
3. **Referential strategy** (Wodak): Author as actor vs. category.
4. **Argumentation topoi** (Wodak): Authority-first vs. consequence-first.
5. **Audience aggrandizing**: Attributing values to readers/committees. Flag it.
6. **Appraisal** (Martin & White): Affect shown vs. labeled. Judgment of situations vs. self.
7. **Continuity**: Extension language vs. introduction language after opening.
8. **Cross-document awareness**: Self-contained vs. portfolio-aware.
9. **Theme/Rheme**: New concepts in subject position (bad) vs. predicate (good).
10. **Register** (Biber Dimension 1): Involved vs. informational. Check against user's baseline.
11. **Genre moves** (Swales/Bhatia): All expected moves present for this document type. If genre is selected, check against its `genre_moves` list.
12. **Narrative structure** (Labov): Orientation, complication, evaluation, result. Evaluation earned vs. announced.
13. **Positive DA check** (Martin): Before cutting, protect passages that use affiliation, invocation, or graduation well.

**Profile-specific checks**: Load from `profile.qualitative` and the active genre's `qualitative` array. These supplement universal checks.

### Report format

```
VOICING REPORT: [filename]
Profile: [profile name]
Genre: [genre name or "base"]

QUANTITATIVE (from writing_check.py):
[key metrics and flags]

QUALITATIVE (CDA analysis):
[findings organized by ideational/interpersonal/textual/structural]

SUGGESTIONS:
[specific, actionable — "Consider rewriting line X with Y pattern"]
```

Suggestions, not directives. The user decides what to act on.

---

## Additional voice dimensions

These modules extend the voice fingerprint beyond stylometry. Each adds a section to the profile, participates in calibration (`--calibrate`) and learning (`--learn`), and degrades gracefully when its dependencies aren't installed.

### Perplexity scoring (requires MLX + local model)

Measures per-sentence perplexity via a local language model (`perplexity.py`). Human writing has higher and more variable perplexity than agent-generated text. The "surprise profile" captures how predictable the writer's sentences are.

- **Style guide**: `perplexity.style_notes` tells the agent how "surprising" the user's writing tends to be — whether to aim for smooth or uneven prose
- **Learning**: compares perplexity distributions (mean, CV) between first and final draft
- **Profile section**: `perplexity` with baseline mean, stdev, variance, CV, distance threshold
- **Default model**: `mlx-community/Qwen2.5-1.5B-4bit` (base, not instruct — cleaner perplexity signal)
- **Install**: `pip install mlx mlx-lm` (model downloads on first use)

### Embedding similarity (requires fastembed)

Sentence embeddings capture semantic drift (`embeddings.py`) — when the agent writes about the same topic but in a different conceptual register. The writer's calibrated samples define a semantic centroid; drafts that drift from it are writing in the wrong conceptual space.

- **Style guide**: `embeddings.style_notes` describes semantic consistency (tight cluster = focused, broad = wide-ranging)
- **Learning**: embeds first-draft and final-draft sentences, updates centroid via EMA
- **Profile section**: `embeddings` with centroid vector, mean/stdev distance, threshold
- **Default model**: `BAAI/bge-small-en-v1.5` (384-dim, ONNX via fastembed — no torch needed)
- **Install**: `pip install fastembed`

### RST structural coherence

Implemented as qualitative checks in the base profile (argumentative progression, claim-evidence binding, coherence vs. cohesion, nucleus-satellite relationships). The `research_paper` genre adds a reinforcing `argumentative_spine` check. No separate module — these are CDA checklist items that agents evaluate during qualitative analysis.

---

## Reference

### Profile schema

```json
{
  "profile": {
    "name": "Writer Name",
    "version": "1.0",
    "created": "2026-04-13",
    "calibrated_from": "8 writing samples",
    "description": "Voice profile description"
  },

  "patterns": {
    "hedge_words": ["regex patterns..."],
    "self_aggrandizing": ["..."],
    "topic_sentence_starters": ["..."],
    "logical_connectors": ["..."],
    "narrative_padding": ["..."],
    "corporate_jargon": ["..."]
  },

  "thresholds": {
    "long_sentence_words": 45,
    "rewrite_sentence_words": 60,
    "long_sentence_max": 6,
    "rewrite_sentence_max": 3,
    "emdash_per_1000w": 20,
    "emdash_insertion_words": 12,
    "hedge_max": 2,
    "self_aggrandizing_max": 0,
    "topic_opener_max": 3,
    "logical_connector_max": 5,
    "narrative_padding_max": 0,
    "product_description_max": 0,
    "corporate_jargon_max": 0,
    "wordcount_over_pct": 115
  },

  "qualitative": [
    {
      "id": "check_id",
      "category": "ideational|interpersonal|textual|structural",
      "name": "Human-readable name",
      "instruction": "What to check and why it matters for this writer"
    }
  ],

  "genres": {
    "genre_key": {
      "description": "What this genre is and who reads it",
      "word_count_target": 1200,
      "threshold_overrides": {
        "hedge_max": 3
      },
      "genre_moves": ["move_1", "move_2"],
      "qualitative": [
        {
          "id": "genre_specific_check",
          "category": "structural",
          "name": "Check name",
          "instruction": "What to check"
        }
      ]
    }
  },

  "stylometry": {
    "function_words": ["the", "is", "of", "..."],
    "corpus_mean": {"the": 0.042, "is": 0.019, "...": "..."},
    "corpus_stdev": {"the": 0.005, "is": 0.003, "...": "..."},
    "centroid_z": {"the": 0.12, "is": -0.05, "...": "..."},
    "punctuation_ratios": {"semicolon": 0.06, "emdash": 0.03, "...": "..."},
    "vocabulary_richness": {"ttr": 0.52, "mattr": 0.72, "yules_k": 125},
    "sentence_distribution": {"mean": 18.5, "stdev": 9.2, "skew": 0.8},
    "distance_threshold": 0.35,
    "intra_author_max_delta": 0.23,
    "calibration_word_count": 8500,
    "style_notes": "Plain-language summary of voice fingerprint",
    "revision_count": 0
  },

  "perplexity": {
    "model": "mlx-community/Qwen2.5-1.5B-4bit",
    "baseline_mean": 1505.7,
    "baseline_stdev": 4150.6,
    "baseline_variance": 17227614.0,
    "baseline_cv": 2.76,
    "calibration_sentence_count": 61,
    "distance_threshold": 9807.0,
    "style_notes": "Surprise profile summary",
    "revision_count": 0,
    "enabled": true
  },

  "embeddings": {
    "model": "BAAI/bge-small-en-v1.5",
    "centroid": [0.01, 0.02, "... (384-dim)"],
    "dimension": 384,
    "mean_distance": 0.27,
    "stdev_distance": 0.04,
    "distance_threshold": 0.34,
    "calibration_sentence_count": 61,
    "style_notes": "Semantic space summary",
    "revision_count": 0
  }
}
```

### Thresholds quick reference

Base defaults (from generic starter profile). Genre overrides adjust these per document type.

| Metric | Default | Type | What it catches |
|---|---|---|---|
| Word count | >115% of target | structural | Bloated drafts |
| Sentences >45 words | >6 per doc | structural | Runaway sentence length |
| Sentences >60 words | >3 per doc | structural | Sentences that need splitting |
| Em-dash insertions >12 words | any | structural | Em-dash clauses doing too much work |
| Em-dashes per 1000w | >20 | structural | Em-dash overuse |
| Hedge words | >2 | contamination | Agent-typical hedging |
| Self-aggrandizing | >0 | contamination | Inflated framing |
| "This is" openers | >3 | contamination | Relational process overuse |
| Logical connectors | >5 | contamination | Mechanical transitions |
| Padding phrases | >0 | contamination | Filler that adds no content |
| Product descriptions | >0 | contamination | Appositive sales language |
| Corporate jargon | >0 | contamination | Words the writer would never use |

**Contamination flags** are diagnostic of agent-generated text — the agent self-corrects these silently. **Structural flags** may reflect deliberate style — surface as suggestions.
