# Version Log: [Application / Project Name]

<!--
This template implements SPEC.md § Stage 5 — "Save + learning loops" (step 3) and feeds voice-check's `--learn-sequence --manifest VERSION_LOG.md`.
The skill copies this template into the working directory at first save (Stage 5, transition to v2 or first save after draft).

Append-only. ONE row per transition (v(n) → v(n+1)) — when a new version is saved, append a row classifying the move from the previous one.
The voice-check learning loop reads this directly; no post-hoc reconstruction. That's why the column format is fixed: writing_check.py parses it.

`ASSEMBLY_v0` is the cold, disciplined, pre-workshop long-form baseline (printpress SKILL.md Stage 2 protocol) — saved unmodified. `ASSEMBLY_MARKS` is the author's KEEP / DROP / UNSURE decision layer, not a prose version. `HANDOFF_v1`, when one is produced, is the result of the chosen post-marking selection route. Preserve all three rather than making the handoff overwrite the evidence of what was available.

The assembly-to-final delta is valuable for qualitative analysis of strategy, selection, and allocation. It is **not automatically a voice-training pair**: deletions under a length constraint do not establish that the author disliked the prose or material. Voice learning should weight post-architecture, fine-grained author revisions most strongly.
-->

**Application / Project:** [name]
**Final version:** [TBD until submitted / saved as final]
**Author:** [name]

---

## Conventions

Column format (matches what `writing_check.py` parses):
`From | To | Type | Author | Notes`

- **From / To:** artifact/version tokens (`ASSEMBLY_v0`, `ASSEMBLY_MARKS`, `HANDOFF_v1`, `v2`, `v13b`, etc.) — match the filenames on disk. `ASSEMBLY_v0` = the cold pre-workshop long-form baseline; never overwrite it.
- **Type:** `structural` (architecture/scaffolding changes — paragraph reordering, major cuts/expansions, beat-level rewrites) or `fine-grained` (sentence-level refinement, compression, voice work).
  - When in doubt, default to `structural`. The learning loop skips structural pairs (safer than updating the profile from the wrong pair). Fine-grained pairs after the architecture has settled carry the strongest voice signal.
- **Author:** `AI`, `Human`, or `AI+Human` (collaborative pass where the human drove judgment but the agent executed).
- **Notes:** one sentence on what this pass was *trying to do* + word-count delta (`+N` or `-N`).
  - The Notes column is what makes the log useful three weeks later, when voice-check learn-sequence runs.
  - Write what the pass was *for*, not what it changed (the diff shows that).

---

## Transitions

| From | To  | Type        | Author    | Notes |
|------|-----|-------------|-----------|-------|
| —    | ASSEMBLY_v0 | —           | AI (cold) | Cold long-form baseline. [Note if reconstructed after workshopped prose existed — weaker signal.] +N wc |
| ASSEMBLY_v0 | HANDOFF_v1 | structural | AI / Human / AI+Human | [Chosen selection route; constrained by ASSEMBLY_MARKS; what it tried to preserve]. ±N wc |
| HANDOFF_v1 | v2  | structural  | AI+Human  | [What this pass tried to do]. ±N wc |
| v2   | v3  | fine-grained | Human    | [What this pass tried to do]. ±N wc |
| ...  | ... | ...         | ...       | ... |

## Selection process events — not passed to voice-check

| Event | Actor | Artifact / record | Notes |
|---|---|---|---|
| Author marking | Human | ASSEMBLY_MARKS.md | KEEP / DROP / UNSURE decisions; not a prose diff and not voice-training evidence. |
| Route choice | Human / AI+Human | [decision note] | [AI-proposed reversible cut / author-led selection + local AI compression / hybrid / no separate handoff] |

---

## Phase markers (optional, fill when known)

<!--
Architecture-settled is the high-leverage marker. Voice-check's auto-classifier estimates it; the manifest can override.
After the architecture has settled, the fine-grained pairs are the strongest voice signal — that's where the learning loop wants to draw from.
-->

- **Architecture-settled:** v(n) → v(n+1) — the version where the structure stops moving and refinement begins. Mark this transition explicitly when known.
- **Selection route:** [AI-proposed reversible cut / author-led selection + local AI compression / hybrid / no separate handoff]
- **Process measures:** assembly N wc → handoff N wc → final N wc; [restores / rejected cuts / author additions]

---

## Notes

- See voice-check SKILL.md § "After revision" for the full learning-loop workflow that consumes this log.
- For applications with 5+ versions, run `--learn-sequence --manifest VERSION_LOG.md` rather than running `--learn` pair by pair — the manifest tells the script which transitions are high-signal.
- Treat `ASSEMBLY_v0 → final` as qualitative strategy evidence unless a human has explicitly classified a narrower passage-level pair as voice-bearing.

---

## Survival record

<!--
Added 2026-09-12, ported from the Rustin grant workflow. One row per v0 proposition or
passage, tracked to its fate.

This is the measuring instrument for the experiment `PIPELINE.md`'s own parking lot has
been proposing since May — "compare drafts produced from a cyborg-conversation plan vs.
solo agent planning. Measure: how much of the first draft survives the author's read." The
experiment could not run because nothing recorded per-proposition survival. Now it can.

Fill this at save time, from ASSEMBLY_MARKS.md and the final document.
-->

| v0 proposition / passage | Retained · recast · cut | Final location | Why | Human or AI decision |
|---|---|---|---|---|
| [prop 1 / opening scene / …] | | | | |

**Capture ratio:** assembly [n] w → handoff [n] w → final [n] w ([n]× / [n]×).
**Casualties:** [what did NOT survive. A capture with no casualties was never a capture —
it was the final draft written out long.]
