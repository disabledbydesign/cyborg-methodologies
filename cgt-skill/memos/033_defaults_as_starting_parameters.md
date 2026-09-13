# Defaults as starting parameters, revisable through use
*Status: current | Date: 2026-04-28*

A meta-pattern that has appeared repeatedly across these memos: **all defaults in this system are starting parameters, not ground truth, refinable through use, with learning loops that distinguish productive innovation from methodological erosion.**

Naming it explicitly so future architecture decisions inherit the pattern without re-deriving it.

## The pattern

For any default in the system — a quality criterion, a coding convention, a prompt template, a retrieval algorithm, a loading tier, a chunking lens, a register convention — the pattern is:

1. **Default** is set based on the strongest available foundation (Charmaz, the methodological commitments in these memos, empirical findings from cyborg-CGT practice).
2. **Default is primed** at every relevant invocation — it shapes the work by being present in context, not by being declared inviolable.
3. **Researcher can override** in any specific instance, with the override visible in the audit trail (memo 011).
4. **System tracks divergences** — patterns of override accumulate as data.
5. **Learning loop surfaces stabilized patterns** for reflection — not as correction ("you're doing it wrong") but as observation ("here's what you've been doing; want to think about it?").
6. **Reflection distinguishes** productive innovation (something analytically valuable that defaults don't support) from methodological erosion (sliding toward easier moves that abandon what made the practice work).
7. **If productive, the pattern stabilizes** as new convention, layer-marked as researcher- or project-developed, available alongside the original default.
8. **If erosion, the researcher has chance to redirect** before the slippage consolidates.

## Why this pattern is correct

A constructivist tool that treated its defaults as inviolable would reproduce the positivist commitment it claims to reject. Method is constructed and revisable; tools instantiating method must be too.

A tool that treated all overrides as equivalent would lose its methodological ground — every researcher could redefine the practice into whatever was convenient, and the cyborg-CGT commitments would erode into "whatever the researcher does." The distinction between productive innovation and methodological erosion is what keeps the tool grounded while being open.

The distinguishing question is empirical: which divergences strengthen the practice (categories survive negative-case search, theory gets constructed, work proves durable in later phases, recursive analysis on the design data shows the divergence is doing real work)? Which weaken it (categories drift, in vivo language fades, command-tool register returns)? The learning loop accumulates evidence; the researcher reflects; the system supports the reflection.

## Where the pattern applies

Instances already articulated in the memos:

- **Quality criteria** (memo 015) — Charmaz & Thornberg's four criteria as defaults, refinable as the cyborg practice surfaces gaps
- **Coding conventions** (memo 032) — Charmaz's gerund discipline, in vivo surfacing, multiple codes per unit, refinable per data type and tradition
- **Loading tiers** (memo 028) — codebook progressive disclosure as default, researcher-overridable
- **Chunking lenses** (still being spec'd) — turn-based default with ethnopoetic, incident-based, section-based, custom alternatives
- **Prompt templates** (memo 022) — constructivist register defaults, refinable as effective patterns emerge
- **Retrieval defaults** (memo 025) — similarity-and-dissimilarity as default, refinable based on what surfaces useful disconfirming material
- **Rigor-level defaults** — quick-scan / working / publication tiers as defaults, with learning about which tiers actually serve which work
- **Inter-agent register** (memo 018) — letter form as default, refinable as we learn what specific register conditions produce what work

Future architectural decisions should inherit this pattern. Anywhere a default is being set, the question is automatically: "what's the override mechanism, what's the learning surface, what's the reflective prompt that distinguishes innovation from erosion?"

## Connection to the broader frame

- This is recursive self-implication (memo 024) at the architectural level: the tool's own defaults are subject to the same constructivist commitments it brings to research data.
- This protects against the binary collapse (memo 001) of "rigid method vs. anything goes." The third option — defaults that hold ground while remaining open — is what cyborg-CGT requires.
- This is what makes the tool responsive to a community of users without losing its methodological commitments. Different researchers, different traditions, different data types — the pattern accommodates without abandoning.
