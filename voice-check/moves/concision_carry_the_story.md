# Concision — Cut Words That Carry No Story

**Genres:** ALL — universal craft, not genre-scoped
**Rescoped:** 2026-08-07 (June: "Williams style craft should be for ALL writing." Originally tagged `gra-memory-creation`; the cut-what-carries-no-story rule, and June's refinement that a cuttable word is not thereby a word worth cutting, apply to any prose.)
**Category:** register / pre-draft tilt (deliberately not a mechanical cut)
**Added:** 2026-07-04 (gra-memory-creation genre build, T2; June's refinement)

## The Move

Cut words that carry no story. That is different from cutting words that merely *could* be cut.

June's refinement, verbatim intent: *"just because a word can be cut doesn't mean it isn't helpful
to have."* A mechanical concision pass — enumerate cuttable words, flag anything removable — trains
toward an over-deletion artifact: prose stripped to its minimum syntactic skeleton, which reads as
terse rather than clear, and often loses exactly the situating detail (`old_to_new.md`,
`story_not_spec.md`) this genre is trying to preserve.

## What This Move Does NOT Do

- Does not enumerate cuttable words.
- Does not flag adjectives, hedged-but-story-carrying phrases, or anything on a could-be-removed
  basis.
- Is not implemented as a mechanical linter rule (see `writing_check.py`'s concision guard — it
  explicitly tests that the checker never flags on a could-be-cut basis).

## What It Does Instead

Ask, sentence by sentence: does this word carry the story — situating detail, who/when/how — or is
it padding that could be cut *and* would lose nothing? Only cut in the second case. The judgment is
about whether the word is doing situating work, not about brevity for its own sake.

## Should / Shouldn't

- **Shouldn't (over-deletion, treats "could be cut" as "should be cut"):** "R3 revised. Revision
  owned." (technically shorter; loses who revised, what was revised, why it mattered)
- **Should (cuts padding, keeps story-carrying detail):** "June revised R3's framing after noticing
  it had collapsed into a single settled rule."

## Why It Works

The mechanical linter only surfaces a size-to-content outlier prompt ("is the narrative sized to
the content?") — never a word-level cut. Suspect the over-deletion reflex when reviewing a draft:
it's more often an artifact of an explicit cutting pass than a genuine improvement.
