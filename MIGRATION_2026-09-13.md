# The skills migration of 2026-09-13

**For an agent that finds something missing from a skill.** This records where the
pre-migration copies are and what moved, so a gap can be closed by looking rather
than by reconstructing.

`bash link_skills.sh` prints the current backup list every run, read off the
filesystem. Trust that over this file — this one cannot know when a backup has
been deleted.

## What changed

Skills live in this repository. `~/.claude/skills/<name>` is a **symlink** to
`<name>/` here — the whole directory, not file by file. One copy, one history, and
an edit in either place is the same edit.

Before this, four skills were symlinked and three were real directories holding
work that existed in no repository at all.

## The backups

`link_skills.sh --migrate` never deletes. It moves the previous directory aside:

    ~/.claude/skills/c2c.pre-link-20260913-171134
    ~/.claude/skills/discourse-analysis.pre-link-20260913-174137   (~17,000 files, nearly all .venv)
    ~/.claude/skills/voice-check.pre-link-20260913-174138

These are the only way back from this migration. Everything in them is now in this
repository or in the private `Job Search` repository — but "should be" is not
"is", which is why they are still there.

**Keep them until the skills have run for real several times.** Deleting them is
the one step of this migration that cannot be undone.

## Where things went, if something seems missing

| Looking for | It is in |
|---|---|
| `moves/*.md` — point_first, old_to_new, throat_clearing, williams_diagnostic_restructure, and five more | `voice-check/moves/` here. They were only in `~/.claude` before. |
| `june_bloch.json`, `claude.json` | `Job Search/voice_profiles/`, symlinked into `voice-check/profiles/`. **Not here** — this repository is public. |
| `PROFILE_CHANGE_LOG.md` | Same: private repo, symlinked back, because `writing_check.py` names that path. |
| `AUDIT_REPORT_2026-05-06.md`, `AGENT_FEEDBACK_2026-05-02.md`, `TEST_B_PREDRAFT_EXTRACT.json` | `Job Search/voice_profiles/`. Not symlinked — nothing reads them by path. |
| `PIPELINE_REDESIGN_SPEC.md`, `INTEGRATED_dual_meaning_terms_check.md`, `TODO_compression_quality_refinement.md` | `voice-check/` here. Method, so public. |
| `PIPELINE.md`, `DRAFTING_STANDARD.md` | `printpress/`, moved out of the Job Search workspace. Stubs point at them from the old paths. |

## Two merges, not choices

`discourse-analysis/SKILL.md` and `voice-check/citation_log.json` each existed in
two versions. Both here are **merges**, not one version picked over the other:

- **SKILL.md** — took the newer installed copy's project-context step, corpus mode,
  framework-confirmation gate and divergence pass; converted its nine path
  references, which pointed at the nonexistent `cyborg-methodolog*y*` (singular),
  to skill-relative; restored one sentence it had dropped about continuing with
  LLM-only analysis when the quantitative script fails.
- **citation_log.json** — the repo held 22 runs from July, the installed copy 17
  from May, June and August, with zero overlap. One append-only log that had been
  split. The union is 38 runs.

`.skills-resolved.json` records both, by the sha256 of the superseded content, so
an edit to either installed file blocks again rather than inheriting this decision.

## Why the split is public/private

`cyborg-methodologies` is a **public** GitHub repository. Method is shareable. A
model of how one person writes, built from her unpublished drafts, is not. See
`Job Search/voice_profiles/README.md`, and `check_public_safe.py`, which enforces
it from a pre-push hook.
