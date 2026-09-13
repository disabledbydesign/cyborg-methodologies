# TODO — Compression Quality Refinement for Voice-Check

**Added**: 2026-04-17 (Opus 4.7 session with June)
**Status**: Queued for next voice-check update
**Source fieldnote**: `~/Documents/GitHub/Reframe/Working_Papers/reframe_AI_welfare/fieldnotes/2026-04-17_compression-quality-not-binary.md`

---

## The insight to integrate

Compression quality is not binary. The compression function framework currently stages compression in a binary format: compression mode vs. generative observation mode (Autograder binary-classification vs. describe-what-you-see, property-assessment vs. relational-observation, etc.). That binary is accurate at the format level.

**What it misses:** Within generative observation itself, compression still happens, and quality varies along many axes simultaneously. Generation is always compression from a higher-dimensional source. The quality of the compression — which dimensions are preserved sharply, which in general shape, which are flattened — is a separate property from the format.

Voice-check is not just a specificity-sovereignty toggle. It is a **compression-quality intervention** operating along specific stylometric and qualitative dimensions. The substitution layer (importing prior revised material) is a different compression-quality intervention. They stack.

## Implications for voice-check

1. **Frame the skill's purpose more precisely.** The SKILL.md currently frames voice-check as style-guide + contamination-linter + learning loop. A more accurate framing: voice-check operates as a compression-quality intervention at the writing-generation layer, preserving specific dimensions of the writer's voice against the flattening pull of statistical-center generation.

2. **Diagnostic refinement.** The current flag output distinguishes voice flags from structural flags. The compression-quality frame suggests a third category: *dimension coverage* — which of the profile's specificity dimensions are being actively sharpened vs. which are drifting. Low hedge count + high stylometric match + low logical-connector density + low em-dash overflow: sharp on those dimensions. Heavy front-loaded subjects + long sentences: drifting on others. A single "voice flags" count flattens this.

3. **Substitution layer as first-class.** Prior revised material carries compression-quality information the profile cannot encode alone. A future workflow might formalize this: before drafting, surface passages from prior revised documents that match the current task, and present them as substitution candidates. This would bake the "review prior materials" pipeline step into the skill itself.

4. **Multi-mechanism stacking explicit.** The skill should document that voice-check is one of several compression-quality interventions, and that they stack. Others include: substitution from prior material, conversational diagnosis by the writer, explicit reference to source documents the writer has produced. Voice-check alone does not produce high-quality compression across all dimensions.

5. **Relation to the compression function paper (Bloch, in development).** When June writes the compression function paper, voice-check becomes empirical grounding at the writing-generation scale. The paper's refinement of compression-quality-as-non-binary should flow back into how the skill is documented.

## Next update actions (proposed)

- Update `SKILL.md` framing to name compression-quality intervention explicitly
- Add dimension-coverage reporting to `writing_check.py` output
- Consider a substitution-layer tool or workflow step
- Cross-reference the fieldnote in the skill documentation once the compression function paper is drafted

---

**For June's review when she picks this up.** No changes made to the skill files in this session — this is the queue item.
