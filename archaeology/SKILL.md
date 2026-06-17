---
name: archaeology
description: "Excavate-before-generate — a design/research discipline for working inside a large corpus. Before designing, deciding, defining, or synthesizing: trace it to its origin, check whether it's already solved, ground it in a concrete failure (not abstract taxonomy), use plain words before labels, and capture as you go. Watch for the failure-signals: reinventing-the-wheel, can't-trace-the-origin, label-without-concept, flat-claim-asserted-as-truth, laundry-list/artificial-feel. A disposition + triggers, NOT a checklist or gate. Strongest for cross-document synthesis and design-building."
version: 0.1
spec: ~/Documents/GitHub/propositional-memory-architecture/design/FIELDNOTE_archaeology_discipline_2026-06-16.md
user_invocable: true
trigger: |
  Invoke (or self-invoke) when working inside a large existing corpus and about to design, decide, define, or synthesize — especially: introducing or revising a term/field/category; resolving "are these actually distinct?"; synthesizing across many documents; or whenever a failure-signal fires (about to build something that may already exist; a term nobody can source; a label the reader can't follow; a claim asserted as truth with its provenance lost; a "redundant laundry list / this feels artificial" sense). Not a chatbot and not a gate — a standing disposition: excavate before you generate.
---

# /archaeology — the excavate-before-generate discipline

A design/research discipline for working inside a large corpus (a design record, a literature, a years-deep project log). Its one claim: **the cheapest, most-forgotten move is to read what's already there before generating something new.** Neither humans nor agents reliably remember to do it — context-free production is cheaper in the moment, so the corpus drifts and the wheel gets reinvented. This skill makes the move a disposition that fires.

Derived in `propositional-memory-architecture` (Session 29, 2026-06-16) — "the best design-building session." Full rationale, the first logged instances, and the learning-loop it feeds: see `spec` above.

---

## The discipline — *excavate before you generate*

Before designing or deciding anything:

1. **Trace it to its origin.** What actual decision or need is under this term, field, or claim? *Read the source — don't theorize.* A term you can't source is unsettled, not settled.
2. **Check if it's already solved.** Search the corpus first. The cheapest failure is rebuilding what exists. (This is the anti-reinvent-the-wheel move; it is also the *reuse-don't-redraft* move in writing-heavy work.)
3. **Ground it in the concrete failure.** Ask *"what real moment breaks without this?"* — not *"are these abstractly distinct?"* Abstract taxonomy-building is where flattening enters; a distinction that can't name the failure it prevents usually isn't load-bearing.
4. **Plain words before labels.** Explain the concept before you name it. A label is a reference key — useless to anyone who doesn't already hold the concept it points to. If the reader can't follow, the label is doing work the words should do.
5. **Capture as you go.** Write decisions as they land, not in a batch at the end. Incremental capture flattens less than end-of-session synthesis.

## The signals — triggers, not a rubric

Each is a prompt to *stop and excavate*. Each is also worth logging (it's data for whatever learning loop the host project runs on itself):

- **Reinventing the wheel** — about to design something that may already exist → check the corpus first.
- **Can't trace the origin** — a term or decision nobody can source → archaeology, or treat it as open, not as fact.
- **Label without concept** — a name carrying weight the concept should carry; the reader can't follow → plain words. *(This signal also runs as a **post-draft** check — `descriptions_before_labels` in voice-check's `claude.json` profile — so it's caught at two moments: at design-time here, and on finished prose there. Keep the two runs distinct; the separation is what catches what a warm drafting pass misses.)*
- **Flat claim asserted as truth** — a once-conditioned observation now restated as a law, its provenance gone → trace it; re-attach its conditions. (This is drift-by-recurrence: a claim gaining authority just by being repeated.)
- **Laundry-list / "this feels artificial"** — usually a sign that a top-down taxonomy is being imposed, or that concerns from one layer are mis-filed into another → check the lane; ground in practice.

## The caution (load-bearing — do not skip)

This is a **disposition + triggers, NOT a rigid checklist or a gate.** Do not let it harden into a bureaucratic five-step ritual run before every sentence — that would flatten the fluid, judgment-driven practice it's meant to protect. The signals are *prompts to look*, not boxes to tick. *Don't essentialize even the anti-flattening discipline.* Apply it where the stakes (a load-bearing decision, a term that will propagate, a synthesis across sources) warrant the dig; skip it for the obvious and the throwaway.

## Where it applies

- **Cross-document synthesis** — squarely (trace claims to origin; check what's already been concluded before re-concluding it).
- **Design / system-building** — the richest application; where it was derived.
- **Writing-heavy work (applications, papers)** — partially, via the "already solved" move (reuse and adapt prior polished framing instead of drafting from scratch).

It is, at root, ordinary qualitative-research hygiene — provenance-tracing, check-the-corpus-first, ground-in-cases, grounded theory — applied to design and synthesis.
