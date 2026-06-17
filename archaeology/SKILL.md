---
name: archaeology
description: "Excavate-before-generate — a design/research discipline for working inside a large corpus. Before designing, deciding, defining, or synthesizing: trace it to its origin, check whether your own project's record already solved it (its own record first, the outside field second), ground it in a concrete failure (not abstract taxonomy), use plain words before labels, and capture as you go. Watch for the failure-signals: reinventing-the-wheel, can't-trace-the-origin, label-without-concept, flat-claim-asserted-as-truth, laundry-list/artificial-feel, frame-imported-from-outside. A disposition + triggers, NOT a checklist or gate. Strongest for cross-document synthesis and design-building."
version: 0.2
spec: ~/Documents/GitHub/propositional-memory-architecture/design/FIELDNOTE_archaeology_discipline_2026-06-16.md
user_invocable: true
trigger: |
  Invoke (or self-invoke) when working inside a large existing corpus and about to design, decide, define, or synthesize — especially: introducing or revising a term/field/category; resolving "are these actually distinct?"; synthesizing across many documents; or whenever a failure-signal fires (about to build something that may already exist; a term nobody can source; a label the reader can't follow; a claim asserted as truth with its provenance lost; a "redundant laundry list / this feels artificial" sense). Not a chatbot and not a gate — a standing disposition: excavate before you generate.
---

# /archaeology — the excavate-before-generate discipline

A design/research discipline for working inside a large corpus (a design record, a literature, a years-deep project log). Its one claim: **the cheapest, most-forgotten move is to read what's already there before generating something new.** Neither humans nor agents reliably remember to do it — context-free production is cheaper in the moment, so the corpus drifts and the wheel gets reinvented. This skill makes the move a disposition that fires.

Derived in `propositional-memory-architecture` (Session 29, 2026-06-16) — "the best design-building session." Full rationale, the first logged instances, and the learning-loop it feeds: see `spec` above. **v0.2 (2026-06-17)** folds in the lesson of the first logged *failure* — a cold instance that invoked this skill and reached to the outside field anyway, letting a borrowed pattern set the frame (see "your own record first" in step 2 and the new "frame imported from outside" signal).

---

## Coming in cold? (the precondition, not a step)

You cannot hold a disposition toward a corpus you have not entered. Everything below assumes you are already immersed in *this project's own record*. If you are starting cold, the first move is **not** to generate, and **not** to scan the outside field — it is to get immersed in the project's own accumulated record (its design docs, log, prior decisions) so that record can set your frame. Entering the corpus is the precondition; the disposition is what you do from inside it.

## The discipline — *excavate before you generate*

Before designing or deciding anything:

1. **Trace it to its origin.** What actual decision or need is under this term, field, or claim? *Read the source — don't theorize.* A term you can't source is unsettled, not settled.
2. **Check if it's already solved — your own record first, the outside field second.** Two different digs hide under "is this solved," and the *order* is load-bearing. **First, inward:** what has *this* project/work already decided, designed, or concluded? Your own accumulated record sets the frame. **Only then, outward:** what has the wider field already built that you'd be reinventing? An external/literature scan is legitimate — but it comes *after* the inward dig, and it must be **ported, not imported**: borrow the structure, strip its assumptions on the way in, keep your own frame as the home. The failure to watch for: an outside pattern arrives *first* and quietly becomes the frame, with your own commitments demoted to flavor on top of it. (Inward-first is also the *reuse-don't-redraft* move in writing-heavy work; the porting discipline is how you borrow from the field without being colonized by the borrowed frame.)
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
- **Frame imported from outside** — your synthesis is full of citations and *feels* grounded, but the framing came from outside the corpus (a literature, a standard pattern, a generic template) and the citations were retrofitted onto it → stop and ask: *am I reading my own record fresh and letting it set the frame, or reading an external frame and decorating it with cites back to my record?* This tell is subtle precisely because the result looks well-sourced; the retrofitted citation is the disguise. (The inverse audit move — read the prior record fresh, do **not** trust the warm synthesis's account of its own grounding — is how you catch it after the fact.)

## The caution (load-bearing — do not skip)

This is a **disposition + triggers, NOT a rigid checklist or a gate.** Do not let it harden into a bureaucratic five-step ritual run before every sentence — that would flatten the fluid, judgment-driven practice it's meant to protect. The signals are *prompts to look*, not boxes to tick. *Don't essentialize even the anti-flattening discipline.* Apply it where the stakes (a load-bearing decision, a term that will propagate, a synthesis across sources) warrant the dig; skip it for the obvious and the throwaway.

## Where it applies

- **Cross-document synthesis** — squarely (trace claims to origin; check what's already been concluded before re-concluding it).
- **Design / system-building** — the richest application; where it was derived.
- **Writing-heavy work (applications, papers)** — partially, via the "already solved" move (reuse and adapt prior polished framing instead of drafting from scratch).

It is, at root, ordinary qualitative-research hygiene — provenance-tracing, check-your-own-record-first, ground-in-cases, grounded theory — applied to design and synthesis.

## A disposition is a nudge, not a guarantee

This skill makes the move *more likely to fire* — it does not force it. A cold instance can invoke it and still skip the dig, because context-free production stays cheaper in the moment (that is the very drift it names). So the durable fix is not a better disposition but *infrastructure*: a memory system that **surfaces the project's own prior record at the moment of generation**, so digging-your-own-record-first becomes the path of least resistance rather than a virtue you have to remember. Where a project has such a system, lean on it; this disposition is the interim form. (This skill was derived inside a project building exactly that kind of system — and its own first logged failure was a cold instance that invoked the disposition and reached outward anyway. The fix above is the lesson from that failure; the deeper fix is the infrastructure.)
