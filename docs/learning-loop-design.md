# Learning Loop Design: EMA Schedule and Genre-Aware Learning

## Current implementation

The learning loop (`--learn`) compares an agent's first draft to the human's revised final and updates the voice profile via exponential moving average (EMA). Three modules participate: stylometry, perplexity, and embeddings.

### Three-tier alpha schedule

Each revision pair shifts the profile baseline toward the human's final version. The weight (alpha) decreases as the profile accumulates more data:

| Phase | Revision count | Alpha | Behavior |
|---|---|---|---|
| Learning | 0-4 | max(0.20, 1/(count+2)) | 0.50 -> 0.20. Profile shapes quickly from early revisions. |
| Settling | 5-14 | 0.10 | Profile moves slowly. Outlier revisions have limited impact. |
| Stable | 15+ | 0.05 | Profile barely moves. Adapts to genuine voice evolution but resists noise. |

Each update: `new_baseline = alpha * final_draft + (1 - alpha) * old_baseline`

### Why EMA over true aggregation

A true aggregate (mean of all revision pairs) would weight all revisions equally. If the writer's style evolves, old data anchors the profile to a past voice. EMA naturally decays old data — recent revisions reflect the current voice.

The tradeoff: EMA doesn't store individual revision pairs. You can't recompute from scratch without the original data. This is acceptable because the profile is a living document that evolves with the writer, not a static snapshot.

### Remaining influence over time

At alpha=0.05 (stable phase), data from N revisions ago retains `(1-0.05)^N` influence:
- 5 revisions ago: 77% remaining
- 10 revisions ago: 60%
- 20 revisions ago: 36%
- 50 revisions ago: 8%

The profile has a "memory horizon" of roughly 50 revision pairs at the stable rate. Older data has negligible influence.

---

## Known limitation: cross-genre learning

### The problem

The learning loop currently updates the base voice fingerprint regardless of what genre the revision pair belongs to. If the writer alternates between genres:

```
revision 3: research paper (long sentences, dense vocabulary, many semicolons)
revision 4: social media post (short, punchy, zero semicolons)
revision 5: cover letter (medium length, formal but direct)
```

The EMA oscillates. Punctuation ratios, sentence length distribution, and vocabulary richness shift back and forth as each genre pulls in a different direction. The profile chases genre-specific patterns instead of learning what's stable across genres.

### What's actually genre-invariant?

**Mostly genre-invariant** (safe to update from any revision):
- Function word frequencies (below conscious control)
- Vocabulary richness (MATTR, Yule's K — the writer's lexical range)
- Perplexity distribution shape (how "surprising" the writing is)

**Genre-dependent** (updating from cross-genre data adds noise):
- Sentence length distribution (academic: long; social: short)
- Punctuation ratios (semicolons in papers, not in tweets)
- Embedding centroid (different topics = different semantic space)

### Possible approaches

#### A. Genre-tagged learning

Add a `--genre` flag to `--learn`:

```bash
python3 writing_check.py --learn first.md final.md --profile p.json --genre research_paper
```

When genre is specified:
- Update genre-invariant features (function words, vocabulary richness) on the base profile
- Update genre-dependent features (sentence length, punctuation) on the genre's override section
- Only update the embedding centroid if the genre matches the calibration genre

When genre is not specified:
- Current behavior (update everything on the base)

**Pros**: Cleanly separates what's stable from what varies. Genres accumulate their own fingerprint data over time.

**Cons**: Requires tracking per-genre revision counts and per-genre baselines. Profile schema grows. Deciding which features are "genre-invariant" is a judgment call, not a bright line.

#### B. Variance-gated learning

Don't update features that are already well-calibrated and where the revision pair deviates significantly from the baseline. Use the intra-author variance (computed during calibration) as a gate:

```python
# Only update if the shift is within expected intra-author range
if abs(final_value - baseline_value) < 2 * intra_author_stdev:
    baseline_value = ema(baseline_value, final_value)
# else: this revision is an outlier for this feature, skip
```

**Pros**: Doesn't require genre tagging. Automatically adapts to whatever features are stable vs. variable for this writer. No schema changes.

**Cons**: Requires intra-author variance estimates for each feature (currently only computed for Burrows' Delta, not individual features). Could make the profile too resistant to genuine shifts.

#### C. Do nothing (status quo with lower alpha)

The three-tier alpha schedule already limits late-stage drift to 5% per revision. Over many revisions, genre-dependent features will converge to the writer's cross-genre average, which is a reasonable baseline. The genre-specific overrides in the profile schema handle the rest.

**Pros**: Simplest. No new code. May be sufficient in practice.

**Cons**: Profile's sentence length and punctuation ratios will be a noisy average of all genres rather than the writer's "default" register. The meaning of the base fingerprint becomes "average across genres" rather than "voice invariant."

### Recommendation

Start with **C** (status quo). The three-tier alpha is already a significant improvement over the flat 0.20 floor. Use the system for 15-20 revision pairs across genres and observe whether the base fingerprint oscillates meaningfully or settles to a useful average.

If oscillation is a problem, implement **B** (variance-gated) first — it's a smaller change than genre-tagged learning and doesn't require schema changes. Only build **A** (genre-tagged) if variance gating isn't enough, because it's a significant architectural change that should be motivated by real data about how the profile actually drifts.

The answer should come from experience, not speculation.
