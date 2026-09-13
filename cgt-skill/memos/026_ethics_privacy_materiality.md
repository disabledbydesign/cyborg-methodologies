# Ethics, privacy, and the materiality of qualitative data
*Status: current (foundation; deeper work parked) | Date: 2026-04-28*

Qualitative data is not abstract text strings. It is interview transcripts with real people who shared something specific to a researcher they trusted; fieldnotes about communities where being identifiable can carry consequences; therapy session material; classroom interactions involving minors; oral histories from people whose stories have been extracted before; communications with power asymmetries baked into the relation (instructor-student, clinician-patient, employer-employee). The tool handles material that has weight, history, and stakes for the people whose words it processes.

A constructivist tool has different ethical commitments than a positivist one. Positivist data ethics treats data as object: anonymize, control access, prevent leakage. Constructivist data ethics also treats data as relational: the researcher has obligations to the people whose words they're working with, including obligations the participants couldn't have anticipated when they consented. The tool's commitments need to honor both.

## Foundational commitments

- **Data stays where the researcher puts it.** No automatic upload, no cloud-by-default, no cross-project bleed. The tool reads source data from paths the researcher specifies; it doesn't move that data without explicit action. Storage is local unless the researcher chooses otherwise.
- **Cross-project isolation by default** (already in SPEC.md). A code or category emerging in project A does not auto-apply to project B, even when the projects look related. Cross-project material flows as lens/sensitizing context, never as imposed coding scheme (memo 009). The master library queries are explicit, not implicit.
- **Layer-marking respects source identity.** Every extract tagged with its source (memo 010). When AI synthesizes across sources, the layer-marking remains; the synthesis can't silently strip provenance. This matters for both methodological auditability AND for not erasing whose words are doing the analytical work.
- **In-vivo discipline is also ethical practice.** Preserving participants' actual language (memo 010) is not just methodological — it's also refusing to paraphrase a person's words into the AI's voice, which is a form of representational harm even when "anonymized."
- **The researcher controls what gets surfaced where.** When the tool generates outputs (codebook entries, memos, syntheses), the researcher reviews before any external surfacing. The tool does not auto-export, auto-publish, or auto-share research outputs.
- **Recognize the asymmetric stakes.** The researcher and AI carry different stakes than the people in the data. The tool should not treat the data subject as just-another-text. Particularly important when the researcher is studying populations they have power over (instructor-student in inbox use case), or marginalized populations whose stories have been extracted historically.
- **Sensitivity to who built what for whom.** This tool is built by an under-resourced researcher (memo 013, democratization through depth) for use by similarly-positioned researchers. The ethical infrastructure has to fit the conditions of actual use — including limited institutional support, lack of IRB consultation services, and the reality that the researcher is often working alone with sensitive material.

## Connection to other memos

Visibility of interpretive labor (011) is also visibility of representational labor — the trace shows how participants' words got transformed; verification (019) prevents drift in how those words get represented; force-relation analysis (015) extends to the force relations between researcher, participants, and the institutions that funded or contained the original research.

## Parked for deeper work

These are flagged in PARKED.md for substantive memo work later:

- Consent extension across analytical iterations: participants consented to a specific research project under specific framings. What does it mean when the analysis travels into cross-project synthesis or master-library aggregation that the participants couldn't have anticipated?
- Synthesis-harm: when the AI generates analytical text that pulls from multiple sources, it can produce composite "voices" that no real person spoke. Methodologically risky and ethically risky. What guardrails does the tool need?
- Particularly sensitive populations: minors, clinical patients, marginalized communities with histories of extractive research. Are there populations where additional safeguards are required, or where the tool should refuse certain operations?
- The researcher's own data — autoethnography, journals, fieldnotes about themselves — is its own ethics question. The tool's commitments to that material need explicit articulation.
- Researcher-as-participant in AI welfare research: when the AI is also analytically present in the data (e.g., research on human-AI collaboration where the AI participated), what are the AI's own stakes in how that data gets handled?
