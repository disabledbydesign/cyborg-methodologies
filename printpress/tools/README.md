# printpress/tools

Deterministic parts of the drafting workflow. These run the same way every time, so
they belong in code rather than in an agent's judgment.

Installed to `~/.claude/skills/printpress/tools/` by `../init.sh` (symlinked — edits
here take effect immediately). Cite them from skill markdown as:

```
python3 ~/.claude/skills/printpress/tools/<script>.py
```

| Script | What it enforces | Deps |
|---|---|---|
| `check_pdf_textlayer.py` | The rendered PDF still contains its own words | `pdftotext`, `pdfinfo` (poppler) |
| `draft_state.py` | `PRO-11` — the author sees the assembly before the cut | none |
| `capture_requirements.py` | Captured requirements match the live posting verbatim | `kitlib.py` (vendored here) |
| `check_wiring.py` | Every cited path resolves; no file forked across two locations | none |
| `check_landing.py` | An approved amendment was actually applied, not just proposed | none |
| `check_profile_drift.py` | An applied check still matches the check that defines it | none |

## check_pdf_textlayer.py

Reads the **rendered artifact's** text layer — what a parser, a screen reader, and a
recruiter's Cmd-F actually receive. Everything else in the pipeline reasons about the
`.md`/`.html` source; these are not the same document.

Catches: Quartz-flattened PDFs (`Producer: … Quartz PDFContext` — a Chrome render
re-saved through macOS Preview or the system print dialog, leaving six extractable
characters); CSS `letter-spacing` shatter (`E D U C AT I O N`); the 2.5 MB Greenhouse
parse ceiling; image-only PDFs; bare LinkedIn handles.

Added after a 2026-09-12 sweep found **sixteen** already-submitted application
documents with no text layer. Full findings:
`Job Search/_application_evidence/PDF_TEXTLAYER_SWEEP_2026-09-12.md`.

```
python3 check_pdf_textlayer.py "APP_DIR/Bloch CL.pdf" ["...Resume.pdf" ...]   # --show for reading order
```

Exit 1 = at least one BLOCK finding. Nothing ships with an open BLOCK.

## draft_state.py

Human-gated stage machine in `DRAFT_STATE.md`:
`planning → assembly_ready_for_marking → structural_cut_ready_for_review →
compression_ready_for_review → final_check_ready → approved`.

The compression stage is the one with no author in it, which is why `PRO-11` exists and
why it is the check that most often fires against an agent's instincts. A state file
enforces it; an agent's memory does not.

```
python3 draft_state.py init APP_DIR
python3 draft_state.py check APP_DIR
```

## capture_requirements.py

The JSON ledger (`application-requirements.json`) is authoritative;
`APPLICATION_STRUCTURE.md` is a generated reading view. Hash-checks fidelity so a
paraphrase cannot drift from the posting's actual words.

Addresses the failure named in the first paragraph of `Job Search/CLAUDE.md`: Oxford AFP
added milestones, budget and duration to the live posting *after* `POSTING.md` was
captured, and it was caught late.

```
python3 capture_requirements.py init APP_DIR --posting POSTING.md
python3 capture_requirements.py check APP_DIR
```

**`kitlib.py` is vendored**, not imported across repos. Upstream:
`rustin-tools/knowledge-layer/tools/kitlib.py`. If that changes, re-vendor it here.
Ported into printpress 2026-09-12; Rustin keeps its own copies, per the decision to keep
the two workflow structures separate and share only tooling.

## Tests

```
python3 -m pytest ~/.claude/skills/printpress/tools/tests/ -v
```

30 tests. Style matches `grants-research/workflows/tests/`: pytest-discoverable,
`tmp_path`, plain asserts, tools driven as subprocess CLIs.

## check_landing.py · check_profile_drift.py

Two halves of the same failure, named in `REVISION_ANALYSIS_2026-08-16_FAMSF.md`:
*"capture happens, landing doesn't."*

`check_landing.py` catches a proposal that named its own target file and was never applied.
Nine such amendments were proposed on 2026-08-12; four had landed by 2026-09-13 and five
were amendments to existing items, which presence cannot verify — those report as needing a
human rather than passing silently.

`check_profile_drift.py` catches the reverse: a definition that survives intact while every
*application* of it quietly compresses. Measured against profile v3.13 and
`Spelman/STYLE_REVIEW_v11.md` — median similarity 0.11, applied text 20% of definition text,
28 of 38 below threshold, with `topic_sentence_craft` keeping its four features and losing
the test that makes them usable. Drift fires on low similarity **or** on dropped operational
content (`TEST:`, `Anti-pattern`, an author example), because a restatement that quotes the
opening sentence verbatim and drops the test scores high and is equally unusable — a blind
spot the test suite found before the tool shipped.

Neither resolves anything automatically. The fix for drift is never to replace the
definition with the restatement.
