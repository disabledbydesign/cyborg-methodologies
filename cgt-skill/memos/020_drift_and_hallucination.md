# Drift and hallucination
*Status: current | Date: 2026-04-28*

Two related failure modes, distinct enough to name separately. Both produce output that diverges from the source data; the mechanisms differ.

**Hallucination** is fabrication: the AI generates content that has no basis in the source — quotes that weren't said, details that weren't in the data, claims that don't trace back to anything the researcher provided. It can be subtle (a paraphrase that adds a meaning the source didn't carry) or gross (an invented quote attributed to a participant). The mechanism is plausibility: the AI generates what *would plausibly be there* given training-data patterns, regardless of whether it *is* there.

**Drift** is gradual departure from source over time: each step is small, but accumulated steps move the analysis away from what the data actually says. Mechanism is compounding compression/paraphrase across rounds — every iteration loses a bit of specificity, and after enough iterations the result is something the source wouldn't recognize. Drift is what happens when verification (memo 019) doesn't fire often enough.

Both are gravity-driven. Both compound in AI-to-AI text (memo 018). Both are most dangerous when invisible — when the output reads coherent and authoritative, the researcher has no obvious signal to check.

**Why these are categorically different from "errors" in command-tool framing:**

In a command-tool/positivist frame, hallucination is a model defect to be eliminated and drift is an accuracy problem to be reduced. In cyborg-CGT, both are also methodologically corrosive in a specific way: they pretend to be grounded readings while actually being pattern-completion. They mimic the analytical move while skipping the construction. Treating them as accuracy bugs misses what they are — they are the AI's gravity producing analysis-shaped output without going through the apparatus.

**What we want, instead:**

- **Source-traceability by design.** Every claim in the system's outputs should be traceable back to specific data — not just "this finding came from the corpus" but "this finding rests on these specific extracts." When traceability isn't possible, the claim is flagged as un-grounded, not silently floated.
- **Mandatory in-vivo quoting at boundaries.** Codes, memos, and synthesis must include direct quotes from the source data, exactly. Paraphrased "quotes" are a hallucination vector; in-vivo discipline (memo 010) is also hallucination prevention.
- **Drift-detection through periodic re-grounding.** The tool periodically returns to the source data and re-checks emergent categories against it: do the codes still trace? do the categories still resonate with the data, or have they drifted into AI-shaped abstractions? This is part of the analytical learning loop (memo 005). Re-grounding is required at promotion moments and at session boundaries.
- **Layer marking exposes drift surface area.** Every extract is tagged with how many layers of synthesis stand between it and the source (memos 010, 019). Findings two or three synthesis-layers deep need verification before they can move forward. The layer marks make drift visible *before* it consolidates.
- **Negative cases as drift detection.** If the analysis only retrieves confirming material, drift is likely — the AI's gravity favors coherence. Active negative-case search (data the emerging theory doesn't fit) is structural drift-detection: if you can't find disconfirming material, suspect that the categories have drifted into pattern-fit rather than data-fit.
- **Treat coherence as suspicious, not reassuring.** Smooth, well-organized AI output that perfectly accounts for everything is a drift/hallucination warning sign, not a quality signal. Real cyborg-CGT analysis carries unresolved tensions, awkward residues, things-that-don't-quite-fit (memo 007). When the output reads too clean, check the data.

**For my own practice in the dialogue:** when I find myself producing a tidy summary, a confident claim, or a paraphrase of source material, that's the moment to slow down and check. The very fluency that makes the output read well is what should make the researcher (and me) suspicious. Fluency is a hallucination/drift signal in this register.

**Hallucination has one further property worth naming**: it can happen even with the source in front of the AI. The researcher provides data; the AI still generates content not in it. So "I have access to the data" is not protection — explicit verification is required (memo 019). Hallucination is not just a context-window problem; it's a gravity problem.
