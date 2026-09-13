# Codebook progressive disclosure
*Status: current | Date: 2026-04-28*

How much of the codebook gets loaded into the AI's context depends on the coding tier. This is methodological, not just performance. Loading the wrong amount of codebook breaks the analytical practice the tool is supposed to support.

## At initial coding: structure only, not content

For initial line-by-line coding, the codebook should *not* be loaded in full. Loading existing codes biases the AI toward them — exactly the move that breaks "letting categories emerge" from the data. Initial coding wants the data to speak first; existing categories should not preempt the reading.

What loads at initial coding:
- Codebook structure (which categories exist, in name only)
- The gerund-form discipline (so new codes match the established form)
- Existing in vivo entries (so the system recognizes participant language already preserved as code, rather than re-coining it)

What does *not* load at initial coding:
- Full code-to-extract mappings
- Category definitions and properties
- Cross-category relations

The cost: initial codes might duplicate what's already in the codebook. The benefit: codes emerge from this data rather than being shaped to fit existing categories. Reconciliation happens after, in focused coding — that's the right phase for it, methodologically.

## At focused coding: more, because we're working at category level

Focused coding selects significant codes from initial coding and raises abstraction toward categories. Here we *want* the codebook present:
- Existing categories with their definitions and properties
- Codes already organized under each category
- Recent category-level memos

What still doesn't load: full extract-level data unless the researcher pulls it. The codebook structure and category-level material is what's working memory.

## At theoretical coding: substantial loading

Theoretical coding constructs relationships across categories. This requires having the categories present in working memory. Here we load:
- The codebook in full
- Recent theoretical memos (memos about category relations)
- Cross-category queries when invoked

But: theoretical coding is dialogic-only (memo 027). The full-codebook context is shared with the researcher in conversation, not given to a solo AI to synthesize.

## Constant comparison: targeted retrieval, not full dump

When constant comparison fires (memo 016, openings and takings-up; memo 025, negative case), retrieval is *targeted*: similar extracts, dissimilar extracts, extracts coded under specific categories. The codebook is queried, not dumped. This is also where similarity-and-dissimilarity retrieval matters architecturally (memo 025): RAG defaults to similar-only; we need both.

## Architectural implications

- The codebook needs to be loadable in pieces. A `load_codebook(mode='structure'|'categories'|'full')` interface, or equivalent.
- The skill knows which mode to invoke based on the current task — initial coding triggers structure-only, focused triggers categories, theoretical triggers full.
- Researcher can override: "actually, show me the full codebook even though we're doing initial coding here" — useful for reconciliation moments. But the *default* should follow the methodological logic above.
- Codebook entries themselves need to be structured so partial loading is meaningful — entry header (name, gerund form, in vivo flag) loadable separately from entry body (definition, properties, source extracts).

## Connection to the broader frame

This is one of several places where progressive disclosure is methodological commitment, not optimization (see also: project memo loading, design memo loading, bibliography on-demand). The pattern is general: load what the analytical move at this stage *needs*, not what's available. Loading more than needed is not just inefficient — it can corrupt the analytical practice. The tool's context management is itself part of the methodology.
