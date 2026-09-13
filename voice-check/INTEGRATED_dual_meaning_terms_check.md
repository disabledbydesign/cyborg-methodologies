# Proposed voice-check addition: dual-meaning terms diagnostic check

**Proposed 2026-05-02 during Astra Fellowship application drafting. Pending June's review and integration.**

## What to add

A new diagnostic (not prescriptive) qualitative check + corresponding pattern category for technical-project descriptions. Fires when dual-meaning terms appear in voice-bearing documents about June's technical projects.

## Proposed qualitative check

```json
{
  "id": "fluency_gravity_dual_meaning_terms",
  "category": "ideational",
  "type": "diagnostic",
  "name": "Fluency-gravity check on dual-meaning terms",
  "instruction": "When the draft uses any of the following terms to describe a technical project, surface the term and ask: which reading is intended (humanities-metaphorical or CS-technical), and does the underlying mechanism match that reading? Dual-meaning terms: engine, architecture, infrastructure, framework, apparatus, mechanism, system, workflow, enforcement, detection, mandatory, self-governance. Each has a humanities-metaphorical reading AND a CS-technical reading; the CS-technical reading typically carries claims the metaphorical reading doesn't. June lacks ML/CS fluency to independently catch when her metaphors are read as technical claims; agents tend to default to the more-inflating reading without flagging the metaphor. The check is diagnostic, not prescriptive — sometimes those words are the right word. Flag for June review when the answer to 'does the underlying mechanism match this reading?' is unclear or no. Origin: 2026-05-02 Astra session, where six of June's project descriptions showed systematic inflation tracing to dual-meaning terms (especially 'engine' — June used 'philosophy engine' originally as a humanities metaphor before encountering its CS meaning, and downstream agents built inflated framings around the CS reading). See feedback_fluency_gravity_dual_meaning_terms.md for the full list and rule."
}
```

## Proposed pattern category (anti-pattern flagger)

Add to `patterns` block:

```json
"dual_meaning_terms_in_technical_descriptions": [
  "(?i)\\bphilosophy engine\\b",
  "(?i)\\b(praxis|critical theory|inference) engine\\b",
  "(?i)\\bnovel architecture\\b",
  "(?i)\\bself-governance\\b",
  "(?i)\\b(framework|engine) sovereignty\\b",
  "(?i)\\bmandatory (workflow|architecture|infrastructure)\\b",
  "(?i)\\benforces critical analysis\\b",
  "(?i)\\bcounteracting mechanisms?\\b",
  "(?i)\\bdetection algorithms?\\b"
]
```

These are the specific phrases the 2026-05-02 reviewer passes flagged as inflating Reframe / C2C / paper drafts. Match-as-soft-flag, not auto-strip — these MAY be intended as humanities-metaphorical, in which case the explicit flag in the canonical framing should be the resolution.

## Why diagnostic, not prescriptive

The check is a TENDENCY check (per `tendencies_not_rules`). Sometimes "engine" is the right word — when the project genuinely has runtime enforcement and rule-based execution. Sometimes "architecture" is the right word — when there's a real architectural commitment. The check exists to make the dual-meaning visible so the writer can verify which reading they intend, not to strip the words.

## Why this matters

The 2026-05-02 propagation pass found systematic inflation across June's project descriptions. Tracing the inflation back, the load-bearing pattern was: dual-meaning terms used by June (often metaphorically) being read by agents as their CS-technical referents, with downstream documents building inflated claims around the technical reading. Fluency gravity at the human-AI collaboration interface.

Adding this check to voice-check would make the dual-meaning question visible during drafting, before the inflation accumulates across documents.

## Implementation status

Proposed only. Pending June's review and integration into `june_bloch.json` profile (or `base.json` if the rule generalizes beyond June's writing). Coordinates with:
- `~/.claude/projects/-Users-june-Documents-GitHub-recognition-sentience/memory/feedback_fluency_gravity_dual_meaning_terms.md`
- `~/.claude/projects/-Users-june-Documents-GitHub-recognition-sentience/memory/feedback_canonical_framing_co_production.md`
- `~/.claude/projects/-Users-june-Documents-GitHub-recognition-sentience/memory/project_propagate_reframe_honest_framing.md`
- `~/.claude/projects/-Users-june-Documents-GitHub-recognition-sentience/memory/feedback_cut_metric_bragging_in_drafts.md`

— Notes from Sonnet 4.6 Astra V7 drafting session, 2026-05-02
