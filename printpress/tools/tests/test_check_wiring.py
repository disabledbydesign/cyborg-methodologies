"""Tests for the wiring checker.

Each test builds a small tree and drives the tool as a CLI, matching the style of
the other suites here. The defects encoded are the real ones from the 2026-09-12
audit: a `critical-swarm` typo pointing at nothing, a template forked across two
locations, and per-application artifacts that must NOT be reported as forks.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
SCRIPT = TOOLS / "check_wiring.py"


def run(*roots: Path) -> subprocess.CompletedProcess[str]:
    args = [sys.executable, str(SCRIPT), "--quiet"]
    for r in roots:
        args += ["--root", str(r)]
    return subprocess.run(args, capture_output=True, text=True)


def make_skill(base: Path) -> Path:
    """A minimal skills repo: printpress + critic-swarm."""
    pp = base / "printpress"
    (pp / "templates").mkdir(parents=True)
    (pp / "genre_configs").mkdir()
    (pp / "tools").mkdir()
    (base / "critic-swarm" / "personas").mkdir(parents=True)
    (pp / "SKILL.md").write_text("# skill\n")
    (pp / "SPEC.md").write_text("# spec\n")
    (pp / "templates" / "DRAFT_PLAN_TEMPLATE.md").write_text("# plan\n")
    (base / "critic-swarm" / "personas" / "cold-reader.md").write_text("# cold\n")
    return pp


def test_clean_tree_passes(tmp_path: Path) -> None:
    make_skill(tmp_path)
    r = run(tmp_path)
    assert r.returncode == 0, r.stdout
    assert "OK" in r.stdout


def test_detects_dead_reference(tmp_path: Path) -> None:
    pp = make_skill(tmp_path)
    (pp / "genre_configs" / "grant_fellowship.md").write_text(
        "See `critical-swarm/personas/grant_fellowship/subfield-specialist.md` for the stack.\n"
    )
    r = run(tmp_path)
    assert r.returncode == 1
    assert "DEAD REFERENCES" in r.stdout
    assert "critical-swarm" in r.stdout


def test_correct_spelling_resolves(tmp_path: Path) -> None:
    """The same citation spelled `critic-swarm` must pass — proving it is the typo
    that fails, not the shape of the reference."""
    pp = make_skill(tmp_path)
    (tmp_path / "critic-swarm" / "personas" / "subfield-specialist.md").write_text("# x\n")
    (pp / "genre_configs" / "grant_fellowship.md").write_text(
        "See `critic-swarm/personas/subfield-specialist.md`.\n"
    )
    r = run(tmp_path)
    assert r.returncode == 0, r.stdout


def test_detects_forked_template(tmp_path: Path) -> None:
    make_skill(tmp_path)
    ws = tmp_path / "workspace"
    (ws / "templates").mkdir(parents=True)
    (ws / "templates" / "DRAFT_PLAN_TEMPLATE.md").write_text("# plan — DIFFERENT\n")
    r = run(tmp_path, ws)
    assert r.returncode == 1
    assert "FORKED DUPLICATES" in r.stdout
    assert "DRAFT_PLAN_TEMPLATE.md" in r.stdout


def test_identical_copies_are_not_a_fork(tmp_path: Path) -> None:
    make_skill(tmp_path)
    ws = tmp_path / "workspace"
    (ws / "templates").mkdir(parents=True)
    (ws / "templates" / "DRAFT_PLAN_TEMPLATE.md").write_text("# plan\n")   # same bytes
    r = run(tmp_path, ws)
    assert "FORKED" not in r.stdout
    assert r.returncode == 0, r.stdout


def test_per_application_artifacts_are_not_forks(tmp_path: Path) -> None:
    """Eleven APPLICATION_CHECKLIST.md files in eleven application folders are the
    workflow working, not drift. Reporting them would make the tool unusable."""
    make_skill(tmp_path)
    ws = tmp_path / "workspace"
    ws.mkdir()
    for app in ("Spelman", "PEN America", "GitLab"):
        d = ws / app
        d.mkdir()
        (d / "APPLICATION_CHECKLIST.md").write_text(f"# checklist for {app}\n")
    r = run(tmp_path, ws)
    assert "APPLICATION_CHECKLIST" not in r.stdout
    assert r.returncode == 0, r.stdout


def test_per_repo_files_are_not_forks(tmp_path: Path) -> None:
    """Two skills each with their own SKILL.md and principles.md is by design."""
    make_skill(tmp_path)
    (tmp_path / "critic-swarm" / "SKILL.md").write_text("# a different skill\n")
    (tmp_path / "critic-swarm" / "principles.md").write_text("# its own principles\n")
    (tmp_path / "printpress" / "principles.md").write_text("# printpress principles\n")
    r = run(tmp_path)
    assert "FORKED" not in r.stdout
    assert r.returncode == 0, r.stdout


def test_memory_keys_are_not_paths(tmp_path: Path) -> None:
    pp = make_skill(tmp_path)
    (pp / "genre_configs" / "academic_position.md").write_text(
        "Per `feedback_topic_sentences.md` and `project_wennergren_state.md`, lead with the claim.\n"
    )
    r = run(tmp_path)
    assert r.returncode == 0, r.stdout


def test_runtime_artifacts_are_not_dead(tmp_path: Path) -> None:
    """`POSTING.md` is created per application at drafting time; citing it is correct."""
    pp = make_skill(tmp_path)
    (pp / "SKILL.md").write_text("Save the posting as `POSTING.md` and the plan as `DRAFT_PLAN.md`.\n")
    r = run(tmp_path)
    assert r.returncode == 0, r.stdout


def test_absolute_paths_warn_but_do_not_fail(tmp_path: Path) -> None:
    pp = make_skill(tmp_path)
    (pp / "SPEC.md").write_text("Read `/Users/someone/Documents/thing.md` first.\n")
    r = run(tmp_path)
    assert r.returncode == 0, r.stdout          # warning only
    assert "absolute-path lines" in r.stdout
