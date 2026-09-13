# FACT_INVENTORY — [Application Name]

<!--
⚠ `DRAFTING_STANDARD.md` `ACC-3` IS A HARD GATE: no fact inventory with a NOT-AVAILABLE
section, no drafting. Its teeth came from a run where no FACT_INVENTORY.md was produced —
and until 2026-09-12 there was no template for it in either templates directory. A rule with
no template is the failure mode the standard already documents.

Structure ported from the Rustin DRAFT_INPUTS template: prompt-indexed, with the two columns
that do the real work — what is NOT available, and what must NOT be claimed.

Source facts BEFORE writing; do not verify after. Verification catches hallucinations once
they are already on the page; sourcing prevents them. If you have no source for a number,
write `[DATA NEEDED]` — never generate a plausible one.
-->

## Per prompt / section

| Prompt or section | Exact prompt text | What it asks for | Facts available (with source path) | Approved prior language to reuse |
|---|---|---|---|---|
| | | | | |

## ⚠ NOT AVAILABLE — do not write these

<!--
The hard gate. List everything an agent might reach for here and cannot support.
Fabrication is likeliest exactly where a posting duty has no matching evidence — that is
where generating a claim is the locally optimal move.
-->

| What an agent would reach for | Why it isn't available | What to do instead |
|---|---|---|
| | | |

## ⚠ PROHIBITED OVERCLAIMS

<!--
Things that ARE true but must not be stated at this strength, and retired framings. Check
memory and `_application_evidence/` before filling: retirements that reach the linter but
not the plan produce a workflow that instructs the error and then blocks it (`PRO-10`).
-->

| Claim | Permitted form | Source of the limit |
|---|---|---|
| | | |

## Standing constraints

- **Deadname rule.** Always L. June Bloch narratively; published citations use the published name.
- **Fieldwork duration.** Pvlvcekolv fieldwork reads "over a decade," never a specific year count.
- **Cross-reference rule.** If you cannot point to a source document for a claim, you may be
  hallucinating it.

**`ACC-3` gate:** [this inventory is complete, including the NOT-AVAILABLE section — date]
