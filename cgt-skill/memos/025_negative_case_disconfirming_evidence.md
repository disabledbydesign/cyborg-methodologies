# Negative case and disconfirming evidence as architectural requirement
*Status: current | Date: 2026-04-28*

Constant comparison in CGT is not just "compare data to data to find similarities." It explicitly includes seeking out cases that *don't* fit the emerging theory. Categories get refined through the data they fail to account for, not just the data they account for. This is how the analysis avoids confirmation bias and how categories get sharpened — by being tested against the boundaries of their reach.

The architectural problem: standard RAG defaults to similarity retrieval. Vector search returns the *most similar* extracts to a query. For confirmation, this is what you want. For constant comparison done correctly, this is exactly the wrong default — it surfaces what already fits the category and hides what doesn't. The architecture has to support dissimilar retrieval, deliberately and as a first-class operation.

What we want, instead:

- **Negative-case retrieval as first-class query type.** "What in the corpus does *not* fit this category?" is a structural query the tool supports, not a workaround. Implementation: dissimilar-search (max-distance from category centroid), conditional retrieval (extracts coded under different categories), or anomaly detection (extracts the model can't confidently code under any current category). The tool offers these, not just similarity.
- **Active surfacing at category-stabilization moments.** When a category is consolidating, the tool actively searches for disconfirming material before the category gets locked in. This is built into the workflow, not optional. Categories that survive the negative-case search are stronger; categories that don't are revised.
- **"What doesn't this category cover?"** as a standing prompt at promotion moments (memo 019). Before a category gets elevated from session memo to codebook entry, surface the data it doesn't fit. The researcher decides what to do with that data — refine, split the category, accept the boundary, treat it as outside scope — but the data is in front of them, not hidden behind retrieval defaults.
- **Coherence as drift signal** (memo 020 connection). When the analysis only returns confirming material, suspect that the negative-case search isn't firing — coherence at this stage is a warning, not a quality signal. The tool can flag this: "I haven't surfaced any disconfirming material in the last N coding moves. Want me to actively look?"
- **Differential temperature for divergence.** Higher-temperature passes can surface readings the default doesn't reach, including disconfirming readings. Used in service of negative-case search rather than as "more codes."

## Connection to the broader frame

- This is also drift detection (memo 020): if you can't find disconfirming material, the analysis has likely drifted into pattern-fit rather than data-fit.
- This is also dialogic comparison (memo 016): "where does this record contest what that one assumed?" is itself a form of negative-case work — taking-up sometimes means challenging.
- This is also force-relation analysis (memo 015): the gravity toward coherent, confirming retrieval is itself a force relation in the apparatus, and surfacing it is part of reflexivity.

The structural commitment: a cyborg-CGT system without negative-case retrieval is a confirmation-bias machine wearing constructivist language. The architecture has to make dissimilar retrieval as easy as similar retrieval, and the workflow has to invoke it before category consolidation, not after.
