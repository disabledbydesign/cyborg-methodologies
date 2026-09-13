# Persona library extraction notes

**Date:** 2026-05-07
**Source:** `/Users/june/Documents/Filing/Job Search/templates/adversarial_reviewer_personas.md` + `~/Documents/GitHub/cyborg-methodologies/critic-swarm/SPEC.md`

## What was created

**always-runs/** (3 files, content from SPEC):
intelligibility, jargon, author-informed.

**shared/** (3 files, extracted from template + named-but-undescribed entries):
skeptical-generalist, cross-subfield-generalist, methodologist.

**academic-application/** (1 file):
README.md — process for instantiating personas from `DEPARTMENT_PROFILE.md` per-application. Stack has no static personas; this directory documents the instantiation process.

**grant-fellowship/** (3 files, all extracted from template):
program-officer, subfield-specialist, critical-theorist.

**non_academic_application/** (3 files, generated from spec):
hiring-manager, culture-fit-reader, ats-compatibility.

**peer-review/** (3 files, generated from spec):
editor-agent (runs FIRST, proposes panel), source-validator, README.md (instantiation process for subject-area reviewers).

**design-spec/** (2 files, generated from spec):
future-build-agent, skeptical-architect.

**agent-prompt/** (2 files, generated from spec):
fresh-build-agent, skeptical-user.

**research-protocol/** (2 files, generated from spec):
methodologist (specialized for forward-projection vs. shared methodologist's backward-evaluating lens), skeptical-reviewer (forward-looking analog of skeptical-generalist).

## What surprised me

The source template is more focused than I expected — it's specifically a grant-application stress-test tool with five core personas and a few "add when needed" entries. The SPEC's nine-stack structure is much wider. So roughly half the persona files (non_academic_application, peer-review, design-spec, agent-prompt, research-protocol) are *generated from spec* rather than extracted from template. Each file's "Source" section names which it is.

The other thing that surprised me: the editor-agent persona for peer-review is structurally unlike everything else — it runs FIRST, proposes a panel, requires author confirmation, and is not itself a reviewer. That asymmetry is preserved and called out in both the editor-agent.md and the peer-review README.md.

## Decisions on ambiguous cases

- **Methodologist** placed in `shared/` (because it composes across grant-fellowship, peer-review, research-protocol, design-spec) AND a specialized `research-protocol/methodologist.md` (because the forward-projection lens differs enough from the backward-evaluating shared lens to warrant a separate file). The research-protocol file inherits and specializes; documented in both Sources.
- **Skeptical-generalist / skeptical-reviewer / skeptical-architect / skeptical-user** — four sibling personas, each a specialization of the same root lens for different artifacts. Kept distinct because each has artifact-specific teeth (claims-to-evidence vs. design-to-execution vs. architecture-to-maintenance vs. prompt-to-production). Cross-referenced in Source sections.
- **ATS reviewer's checklist form** is the one explicit exception to the source template's "orient by lens, not by checklist" principle. Preserved with rationale: ATS failure modes are mechanical, not interpretive.
- **Academic-application stack as README-only** — the SPEC's instruction to anchor personas to actual faculty per `DEPARTMENT_PROFILE.md` means the personas cannot be pre-defined. Documented as a process rather than as static files.
