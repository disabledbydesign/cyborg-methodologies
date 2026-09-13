# /critic-swarm — Persona performance log

Tracks per-persona performance across `/critic-swarm` invocations. Each entry: when, what stack, which persona surfaced load-bearing critique vs. shallow, what spec refinements followed.

---

## 2026-05-08 — Intelligibility persona scope expanded to four levels

**Trigger:** Duquesne Grefenstette postdoc application. Six-persona swarm (program officer, religious ethics specialist, critical AI/STS, methodologist, intelligibility, jargon) reviewed RS v1 and CL v1. June's session-end review (one day later) caught a load-bearing miss the swarm did not surface: the document's central concept ("relational AI welfare," an invented term) was used throughout without ever being introduced. The reader who is not already in June's research conversation cannot enter the document.

**Why no persona caught it:**

- **Program officer** pattern-matches mission fit at speed. They're already in the AI welfare conversation; they don't notice missing field-introduction because they assume the field.
- **Religious ethics specialist, critical AI/STS, methodologist** all read for their respective lenses and are insiders to one of the document's fields. None reads as a non-specialist; none asks "would a non-specialist understand the central concept?"
- **Jargon reviewer** flagged terms-needing-glosses (property-based assessment, crip theory, Place-Thought, Spiritan, theological anthropology). Caught at term level, not at concept-introduction level. "Relational AI welfare" wasn't a jargon issue — it was a missing-paragraph issue.
- **Intelligibility reviewer** is the persona whose job this should have been. The brief's failure was scoping: "every place a reader would stop, re-read, or get confused" was sentence-and-paragraph shaped throughout. The only document-level cue was "can the reader reconstruct the argument from paragraph topic sentences alone?" — which still operates at sentence-level granularity. A real cold reader experiences the document at all four levels (sentence, paragraph, document, cross-document) at once.

**Additional gap surfaced same day:** section-level topic *claims* were also hit-or-miss. The brief asked for paragraph topic sentences, not section-level orientation. A document with strong paragraph topic sentences can still read as a list of paragraphs rather than a structured argument if sections don't have topic claims that say what the section is *arguing toward* (vs. what the section is *about*, which the header already does).

**Spec changes applied 2026-05-08:**

1. `personas/always-runs/intelligibility.md` — restructured the persona's brief into four explicit levels: sentence, paragraph, document, cross-document. Document level includes concept-introduction (especially invented terms, specialized terms from non-dominant traditions, cross-tradition terms with multiple meanings) and stakes-orientation. Cross-document level applies when the swarm receives multiple documents from a single submission (allocation accuracy, standalone-vs-dependent readability, voice consistency). Paragraph level expanded to include section-opening paragraphs' extra work; document level expanded to require section-level topic claims, not just paragraph topic sentences.
2. `SPEC.md` — same structural update at canonical level so the persona file remains traceable to the spec.

**Hypothesis to test on next runs:** the four-level scope expansion will catch concept-introduction gaps and section-architecture gaps that the prior brief missed, without producing noisy false positives at sentence level. Watch for: (a) does the four-level structure produce reports that prioritize correctly (load-bearing concept absences flagged ahead of stylistic flags), and (b) does the cross-document level meaningfully help when multi-doc submissions are reviewed together, or is it overhead.

**Next refinement opportunity:** if a future session catches another load-bearing miss in a swarm review, log here with the persona that should have caught it and the brief-scope gap that prevented it.

---

## 2026-07-03 — ATS persona: render-then-extract verification is the load-bearing move

**Trigger:** Scion Instructional Designer resume (non_academic_application stack, 6 lenses). The artifact was an HTML self-editing template delivered via browser print-to-PDF.

**What happened:** The ATS persona was prompted to assess "the document as the PDF the ATS will ingest" — and it went empirical: rendered the actual PDF via headless Chrome, ran `pdftotext` in raw + layout modes, and found a **blocking failure invisible to any static read**: `letter-spacing` (0.14em/0.2em) on the tagline and section headers pushed inter-character gaps past extractors' word-boundary threshold. The tagline — the document's ONLY occurrence of "Instructional Designer," the job's own title — extracted letter-by-letter (zero search hits), and the EDUCATION header shattered. The persona then *tested* candidate fixes and reported verified values (0.06em/0.05em; 0.08em still failed).

**Why it matters for the stack:** a resume can be keyword-perfect in source and carry zero signal in the artifact the ATS ingests. The four content lenses all read extracted text and were structurally incapable of catching this.

**Refinement applied:** for any HTML→PDF (or docx→PDF) delivery path, the ATS persona's brief should REQUIRE the empirical loop: render the real artifact by the real path → machine-extract → verify keywords and section headers survive → after edits, re-render and re-extract. Static CSS reading is not sufficient. (Extends the project-level rule "visual proofread the rendered PDF" from human-visual to machine-extraction proofing.)

**Also strong this run:** author-informed caught verified factual drift introduced by the author's own browser edits and traced one error (CofC "R1") to its propagating source doc — the systemic-propagation catch its spec names. Cold reader's document-level scope (the 2026-05-08 four-level expansion) delivered: its top structural finding (required platforms are the least-evidenced claims on the page) emerged only at whole-document level — the hypothesis from the 2026-05-08 entry is holding.
