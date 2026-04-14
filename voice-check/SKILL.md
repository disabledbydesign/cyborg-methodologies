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
| `/voice-check reflect` | Periodic reflection: review patterns across sessions, propose profile updates |
| `/voice-check [file]` | Optional: run standalone diagnostic on any document |

## Paths

- **Script**: `~/.claude/skills/voice-check/writing_check.py`
- **Profiles**: `~/.claude/skills/voice-check/profiles/`
- **Base profile**: `profiles/base.json` (universal norms, ships with the skill)
- **User profiles**: `profiles/[username].json` (personal overrides, built through calibration)

---

## Architecture: Three layers

The profile system has three layers that merge at load time:

**Universal base** (`base.json`) — Ships with the skill. Contains patterns, thresholds, and qualitative checks that work for any English writer. Catches AI contamination (hedge words, corporate jargon, padding) and flags structural issues (front-loaded sentences, weak argument progression). Permissive thresholds — catches obvious problems without false-flagging diverse styles.

**User profile** (`[username].json`) — Built through calibration from the user's own writing samples. Contains only what differs from or adds to the base: tighter thresholds calibrated to this writer's patterns, additional anti-patterns specific to this voice, prescriptive qualitative checks that encode this writer's preferences (e.g., "lead with consequence, not authority"), and computational fingerprints (stylometry, perplexity, embeddings).

**Genre overrides** (within the user profile) — User-defined document types. Each genre can override thresholds (grants tolerate hedging; social media needs short sentences) and add genre-specific qualitative checks. The skill ships with no genres — users create their own through conversation.

Merge order: **base → user → genre**. User thresholds override base. Genre thresholds override the merged result. User patterns extend base patterns (concatenated). User qualitative checks with the same ID as a base check replace it; new checks are appended.

---

## Agent integration protocol

**This is the primary content of this skill.** Any agent helping with writing should follow this protocol.

### Before drafting

1. **Check for voice profile.** Look in `~/.claude/skills/voice-check/profiles/` for non-base JSON profiles. If exactly one exists, use it. If multiple exist, ask which one. If none exists, offer to run setup (see Setup section). If only `base.json` exists, you can still draft using universal norms — just note the writing won't be personalized.

2. **Read the profile.** Load the profile JSON (the script auto-merges base + user layers). Read these sections carefully before writing anything:
   - `stylometry.style_notes` — plain-language summary of the writer's voice fingerprint
   - `qualitative` — checklist items describe what makes this writer's voice distinctive and what to protect. Some are diagnostic (notice this pattern), some are prescriptive (do this).
   - `genres.[genre].description` — if a genre matches, read its description and genre-specific checks
   - `patterns` — anti-pattern lists tell you what words are contamination signals in this voice

3. **Select genre.** Identify which genre the current writing task falls into from the profile's `genres` section. Genre selection is usually obvious from context ("help me with this cover letter" → the user's cover letter genre). If ambiguous, ask. If no matching genre exists, offer to create one (see Genre Creation below) or use base thresholds.

### During drafting

4. **Write in the user's voice.** Use the style notes and qualitative checks as active guidance, not just post-hoc criteria. Match their sentence rhythm, vocabulary register, argumentation style, and relationship with the reader. Avoid everything in the anti-pattern lists.

5. **Self-check after drafting.** Run the quantitative analysis on your own output:
   ```bash
   python3 ~/.claude/skills/voice-check/writing_check.py DRAFT_PATH --genre GENRE_NAME
   ```
   The script auto-discovers the user's profile if only one exists. Use `--profile PATH` to specify if multiple profiles exist. If `--genre` is specified and the genre defines a `word_count_target`, that target is used automatically.

6. **Self-correct contamination silently.** If the check flags voice contamination (hedge words, corporate jargon, narrative padding, self-aggrandizing frames, product-description appositives), fix them before presenting the draft. These are binary contamination signals — "leveraging" is wrong in any voice. Do not tell the user you found and fixed contamination. Just present clean text.

7. **Honestly assess quality before presenting.** Before showing the draft to the user, assess its quality per section. Name what's strong and what's weak. For example: "The opening paragraph is strong — identity-first, specific. The research section has several front-loaded sentences that put new concepts before the reader is oriented. The fit section announces alignment rather than demonstrating it through intellectual engagement." Do not default to "this looks good." AI-generated text defaults to positive self-assessment because the training distribution rewards reassurance. Resist that pull — the user needs accurate assessment to make revision decisions.

8. **Surface structural/qualitative findings as suggestions.** If the check flags structural issues (long sentences, em-dash density, front-loaded subjects) or if you notice qualitative concerns from the checklist, mention them as suggestions the user can accept or reject. These are judgment calls, not automatic fixes. Frame as: "I noticed X — want me to adjust, or is that intentional?"

### After revision

9. **Offer the learning loop at session end.** When the user finishes revising a document (the conversation is wrapping up, or they say they're done), ask: "Want me to run the learning loop? I'll compare my first draft to your final version and update the voice profile so I draft closer to your voice next time."

10. **Run the learning loop.** If the user agrees (or during end-of-session maintenance):
   ```bash
   python3 ~/.claude/skills/voice-check/writing_check.py --learn FIRST_DRAFT FINAL_DRAFT
   ```
   The script auto-discovers the profile. This compares stylometry (and perplexity/embeddings if available) between the two versions, identifies what shifted, and updates the user profile via exponential moving average. The base profile is never modified. Report the key shifts to the user — e.g., "Your revisions shortened sentences and cut front-loaded subjects. Profile updated."

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

Ask the user for 1-3+ samples of writing in the voice they want to maintain. More is better, but even one substantial piece works. These should be:
- **Their own revised/final writing** (not first drafts, not AI-generated text)
- **Writing they're proud of** — this is the voice to protect
- **Across genres if possible** — samples from different document types give a richer fingerprint

**File formats**: `.md`, `.txt`, `.html`. For Google Docs: File > Download > Plain Text. For Word: Save As > Plain Text. For PDF: copy-paste into a `.txt` file.

Save all samples to a single directory. If the user pastes text directly, save each to a temp `.md` file.

### Step 2: Quantitative calibration

```bash
python3 ~/.claude/skills/voice-check/writing_check.py --calibrate PATH_TO_SAMPLES/ -o ~/.claude/skills/voice-check/profiles/USERNAME.json
```

This generates a sparse user profile that references `base.json`. It analyzes the writing samples and stores only thresholds that differ from the base defaults. It also runs stylometry calibration and any other available modules.

### Step 3: Qualitative voice extraction

**You (the agent) read ALL the writing samples in full and extract the writer's voice characteristics.** The user does not do this part.

**A. Voice characteristics** — analyze the samples for:
1. Sentence-level mechanics: length, rhythm, punctuation habits
2. Lexical choices: register, terminology, vocabulary density
3. Argumentation style: evidence-first, authority-first, narrative, consequence?
4. Relationship with reader: direct, institutional, authoritative, collegial?
5. What they do NOT sound like: what would be wrong? What patterns would contaminate this voice?

**B. Anti-patterns** — based on the voice analysis, write regex patterns and add to the profile's `patterns` section. These extend the base contamination patterns with writer-specific additions.

**C. Qualitative checks** — build user-specific checks based on what you found. The pattern: identify something distinctive about how this person writes, then write a check that protects it. Add these to the profile's `qualitative` section. They supplement (or override) the base checks.

### Step 4: Genre configuration

Walk the user through creating genres for the document types they write. This is a guided conversation, not a form — explain each parameter in plain language.

**For each genre, walk through:**

1. "Describe this kind of writing in a sentence. Who reads it? What's the tone?"
2. "How long are these documents usually? A rough range is fine."
3. "Some genres need longer, more complex sentences — academic papers, for instance. Others need short and punchy. Should I give you more room on sentence length for this genre, or keep it tight?"
4. "In some writing, cautious language is appropriate — 'this approach has the potential to...' is expected in grant proposals but sounds weak in a blog post. For this genre, is some hedging OK?"
5. "What sections or moves does this kind of document need? For example, a cover letter usually needs: who you are, why this role, evidence, closing. What are the pieces for yours?"
6. "Is there anything specific to watch for in this genre that wouldn't apply elsewhere?"

Translate the user's answers into the genre JSON structure. The user never sees or writes JSON unless they want to.

If the user isn't sure about genres, skip this step. Genres can be added later. The base thresholds work for any document.

### Step 5: Verify and activate

Run the tool on ONE of the user's own good writing samples:
```bash
python3 ~/.claude/skills/voice-check/writing_check.py GOOD_SAMPLE --genre LIKELY_GENRE
```

What to look for:
- **Few or no voice flags** — if their own good writing triggers contamination flags, the patterns are too aggressive. Adjust.
- **Reasonable structural flags** — some long sentences in good writing is fine. If many, thresholds may be too tight.
- **Zero flags is suspicious** — thresholds may be too loose to catch AI contamination. Tighten.

Show the user the results and adjust until the profile correctly distinguishes their voice from generic AI output.

Tell the user:
- Where the profile lives
- That agents will use it automatically during writing tasks
- That running `/voice-check learn` after revision sessions makes the profile better over time

---

## Genre system

Voice is largely stable across genres — function word frequencies, punctuation habits, vocabulary richness don't change between a cover letter and a research paper. What changes is **register**: threshold tolerances, expected structural moves, and which concerns are appropriate for the audience.

### Genres are user-defined

The skill ships with no genres. Users create their own based on the kinds of documents they write. A tech writer might have `api_docs`, `blog_post`, `release_notes`. An academic might have `journal_article`, `grant_proposal`, `conference_abstract`. A job seeker might have `cover_letter`, `research_statement`, `teaching_statement`.

### Genre structure

Each genre lives in the user profile's `genres` section:

```json
{
  "genre_key": {
    "description": "What this genre is and who reads it",
    "word_count_target": 1200,
    "threshold_overrides": {
      "hedge_max": 3
    },
    "genre_moves": ["section_1", "section_2", "section_3"],
    "qualitative": [
      {
        "id": "genre_specific_check",
        "category": "structural",
        "name": "Check name",
        "instruction": "What to check and why"
      }
    ]
  }
}
```

### How genre selection works

1. **Agent infers from context.** "Help me draft a blog post" → the user's blog genre.
2. **Explicit selection.** The user says which genre, or specifies `--genre blog_post`.
3. **No match found.** Offer to create a new genre, or use base thresholds.
4. **Fallback.** If no genre is specified or inferable, base thresholds with a 1200 word count default.

When a genre is selected:
- Its `threshold_overrides` merge on top of the user's thresholds (genre values win)
- Its `word_count_target` becomes the default (overridden by explicit `--target`)
- Its `genre_moves` guide structural analysis
- Its `qualitative` checks run in addition to universal + user checks

---

## Reflection sessions

The learning loop (`--learn`) captures what the user revised in a single draft. Reflection sessions capture patterns across multiple writing sessions — recurring friction, systematically underdefended areas, and connections between problems at different levels.

### When to run

After sessions with significant revision friction, or periodically after several writing sessions. The user says "let's reflect" or "review recent sessions" or the agent offers at a natural breakpoint.

### Workflow

1. **Scope the reflection.** Ask the user which sessions or documents they want to analyze. Don't assume scope. "Which writing sessions do you want to look at? Any specific friction you noticed?" The user directs what's in scope.

2. **Gather artifacts.** For the scoped sessions, collect: learning loop reports, draft-to-final pairs, session notes. Ask the user to point at files or describe what happened if artifacts aren't obvious.

3. **Name the friction.** Identify specific problems from the material. For each:
   - What happened? (The sentences were front-loaded. The agent said "really good" and it wasn't. The equity statement reinvented content from the teaching statement.)
   - What type? Syntax-level, genre-level, argument-level, workflow-level?
   - Structural or incidental? Would it happen again with the same profile, or was it specific to this session?
   - Already addressed? Is there a check in the profile that should have caught this?

4. **Find connections.** Do friction points cluster? Is there a level consistently underdefended? Did the existing profile prevent problems it was designed for? Present findings to the user — the agent surfaces patterns, the user makes judgment calls about which connections hold.

5. **Compare to profile.** For each structural friction point:
   - If already addressed: why did the check fail? (Enforcement — agent didn't follow it? Specificity — instruction too vague? Coverage — instruction covers a different case?)
   - If not addressed: draft a targeted addition. One check, one pattern, or one threshold adjustment.

6. **Update the user profile.** New qualitative checks, new patterns, adjusted thresholds. All updates go in the user profile — never modify `base.json`.

7. **Optionally test.** Run voice-check on a recent draft to verify the fix catches the pattern.

### Key principle

The agent surfaces patterns and proposes. The user makes judgment calls about what gets changed. Agent presents findings, then asks — doesn't conclude.

---

## Diagnostic mode (optional)

For standalone analysis of any document — writing not produced through a Claude drafting session, or when the user wants to explicitly check a piece.

```bash
python3 ~/.claude/skills/voice-check/writing_check.py PATH_TO_DRAFT [--genre GENRE] [--target WORDCOUNT]
```

The script auto-discovers the profile. Use `--profile PATH` if multiple profiles exist.

### Quantitative analysis

Read the output. Note all flags. Voice flags (hedges, jargon, padding) indicate contamination. Structural flags (long sentences, em-dash density, front-loaded subjects) may be deliberate style.

### Qualitative analysis

Load qualitative checks from the merged profile. Run each against the draft text. Checks marked prescriptive should be enforced; checks marked diagnostic should be noted and reported.

### Report format

```
VOICING REPORT: [filename]
Profile: [profile name]
Genre: [genre name or "base"]

QUANTITATIVE (from writing_check.py):
[key metrics and flags]

QUALITATIVE (analysis):
[findings organized by ideational/interpersonal/textual/structural]

SUGGESTIONS:
[specific, actionable — "Consider rewriting line X with Y pattern"]
```

Suggestions, not directives. The user decides what to act on.

---

## Additional voice dimensions

These modules extend the voice fingerprint beyond stylometry. Each adds a section to the user profile, participates in calibration (`--calibrate`) and learning (`--learn`), and degrades gracefully when its dependencies aren't installed.

### Perplexity scoring (requires MLX + local model)

Measures per-sentence perplexity via a local language model (`perplexity.py`). Human writing has higher and more variable perplexity than agent-generated text. The "surprise profile" captures how predictable the writer's sentences are.

- **Style guide**: `perplexity.style_notes` tells the agent how "surprising" the user's writing tends to be
- **Learning**: compares perplexity distributions between first and final draft
- **Default model**: `mlx-community/Qwen2.5-1.5B-4bit`
- **Install**: `pip install mlx mlx-lm`

### Embedding similarity (requires fastembed)

Sentence embeddings capture semantic drift (`embeddings.py`) — when the agent writes about the same topic but in a different conceptual register.

- **Style guide**: `embeddings.style_notes` describes semantic consistency
- **Learning**: embeds first-draft and final-draft sentences, updates centroid via EMA
- **Default model**: `BAAI/bge-small-en-v1.5` (384-dim, ONNX via fastembed)
- **Install**: `pip install fastembed`

### RST structural coherence

Implemented as qualitative checks in the base profile (argumentative progression, claim-evidence binding, coherence vs. cohesion, nucleus-satellite relationships). No separate module — these are checklist items that agents evaluate during qualitative analysis.

---

## Reference

### Profile schema: base.json

```json
{
  "profile": {
    "name": "Universal Base",
    "version": "1.0",
    "description": "Universal English writing norms"
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
      "type": "prescriptive|diagnostic",
      "name": "Human-readable name",
      "instruction": "What to check and why — self-contained, no jargon"
    }
  ]
}
```

### Profile schema: user profile

```json
{
  "base": "base.json",

  "profile": {
    "name": "Writer Name",
    "version": "3.0",
    "created": "2026-04-14",
    "calibrated_from": "N writing samples",
    "description": "Voice profile description"
  },

  "patterns": {
    "hedge_words": ["additional patterns beyond base..."],
    "custom_category": ["user-specific patterns..."],
    "_disable": {
      "corporate_jargon": ["pattern to remove from base"]
    }
  },

  "thresholds": {
    "hedge_max": 0,
    "long_sentence_words": 40
  },

  "qualitative": [
    {
      "id": "same_id_overrides_base_check",
      "category": "ideational",
      "name": "Prescriptive override",
      "instruction": "User-specific instruction replaces base diagnostic"
    },
    {
      "id": "new_user_check",
      "category": "textual",
      "name": "User-only check",
      "instruction": "Check that only applies to this writer"
    }
  ],

  "genres": {
    "genre_key": {
      "description": "...",
      "word_count_target": 1200,
      "threshold_overrides": {},
      "genre_moves": [],
      "qualitative": []
    }
  },

  "stylometry": { "...": "calibrated from writing samples" },
  "perplexity": { "...": "if MLX available" },
  "embeddings": { "...": "if fastembed available" }
}
```

### Merge behavior

When a user profile references `"base": "base.json"`:
- **Patterns**: base lists + user lists per category. `_disable` entries removed.
- **Thresholds**: base values, then user overrides on top.
- **Qualitative**: base checks first. User checks with same ID replace; new IDs appended.
- **Genres/stylometry/perplexity/embeddings**: from user profile only.

### Thresholds quick reference

Base defaults (permissive starting point). User profile tightens these. Genre overrides adjust per document type.

| Metric | Base default | Type | What it catches |
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
| Front-loaded subjects | >2 per doc | structural | New concepts forced into subject position |

**Contamination flags** are diagnostic of agent-generated text — the agent self-corrects these silently. **Structural flags** may reflect deliberate style — surface as suggestions.
