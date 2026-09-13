"""Tests for skills_compare.py — the comparison that decides what gets copied.

Every test here is a bug that actually happened on 2026-09-13, when the
comparison was `find | sort | comm` in shell.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills_compare.py"


def compare(repo: Path, installed: Path, env: dict | None = None) -> dict:
    e = dict(os.environ)
    if env:
        e.update(env)
    r = subprocess.run([sys.executable, str(SCRIPT), str(repo), str(installed), "--json"],
                       capture_output=True, text=True, env=e)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def pair(tmp_path: Path) -> tuple[Path, Path]:
    repo, inst = tmp_path / "repo", tmp_path / "installed"
    repo.mkdir()
    inst.mkdir()
    return repo, inst


def test_identical_trees_have_nothing_to_do(tmp_path: Path) -> None:
    repo, inst = pair(tmp_path)
    for d in (repo, inst):
        (d / "SKILL.md").write_text("# skill\n")
    r = compare(repo, inst)
    assert r["missing"] == [] and r["differing"] == []


def test_locale_does_not_change_the_answer(tmp_path: Path) -> None:
    """THE BUG. `sort` ran under LC_ALL=C while `comm` compared under the user's
    locale. The two disagree about where uppercase stops and lowercase starts, so
    comm saw disordered input at the first lowercase filename and reported every
    shared file after it as missing. Eight files the repo already had were
    'restored' from the installed copy, overwriting one of them.

    The names below straddle that boundary on purpose.
    """
    repo, inst = pair(tmp_path)
    shared = ["SKILL.md", "README.md", "citation_log.json", "diff_analysis.py",
              "embeddings.py", "stylometry.py"]
    for name in shared:
        (repo / name).write_text("same\n")
        (inst / name).write_text("same\n")
    (inst / "AGENT_FEEDBACK_2026-05-02.md").write_text("only installed\n")

    answers = []
    for loc in ("C", "en_US.UTF-8", "C.UTF-8"):
        r = compare(repo, inst, {"LC_ALL": loc, "LANG": loc})
        answers.append((r["missing"], r["differing"]))
    assert all(a == answers[0] for a in answers), answers
    assert answers[0][0] == ["AGENT_FEEDBACK_2026-05-02.md"]
    assert answers[0][1] == []


def test_a_symlink_counts_as_a_present_file(tmp_path: Path) -> None:
    """voice-check/profiles/june_bloch.json in the repo is a symlink to the private
    copy in the Job Search workspace. Counted as absent, it reads as missing, and
    the 'restore' writes the older installed copy straight through the link onto
    the newer private file — silently, with no error."""
    repo, inst = pair(tmp_path)
    private = tmp_path / "private.json"
    private.write_text('{"version": "3.14"}\n')
    (repo / "profiles").mkdir()
    (repo / "profiles" / "june_bloch.json").symlink_to(private)
    (inst / "profiles").mkdir()
    (inst / "profiles" / "june_bloch.json").write_text('{"version": "3.13"}\n')

    r = compare(repo, inst)
    assert "profiles/june_bloch.json" not in r["missing"]
    assert "profiles/june_bloch.json" in r["differing"]
    assert private.read_text() == '{"version": "3.14"}\n'


def test_two_names_for_one_file_are_not_a_difference(tmp_path: Path) -> None:
    """macOS `cp` exits non-zero on 'are identical', which under `set -e` killed
    the rescue halfway through its copies."""
    repo, inst = pair(tmp_path)
    (repo / "diff_analysis.py").write_text("code\n")
    (inst / "diff_analysis.py").symlink_to(repo / "diff_analysis.py")
    r = compare(repo, inst)
    assert r["missing"] == [] and r["differing"] == []
    assert "diff_analysis.py" in r["identical"]


def test_regenerable_noise_is_ignored_but_counted(tmp_path: Path) -> None:
    """discourse-analysis reported thousands of blocking files, essentially all of
    them pip output under .venv/. The one file that genuinely differed was buried."""
    repo, inst = pair(tmp_path)
    (repo / "SKILL.md").write_text("a\n")
    (inst / "SKILL.md").write_text("b\n")
    venv = inst / ".venv" / "lib" / "site-packages" / "numpy"
    venv.mkdir(parents=True)
    for i in range(50):
        (venv / f"f{i}.py").write_text("x\n")
    (inst / "junk.pyc").write_bytes(b"\x00")
    (inst / "profile.json.bak.20260801").write_text("old\n")

    r = compare(repo, inst)
    assert r["missing"] == []
    assert r["differing"] == ["SKILL.md"]
    assert r["counted"] == 1
    assert r["ignored"] == 52


def test_nested_paths_are_reported_relative(tmp_path: Path) -> None:
    repo, inst = pair(tmp_path)
    (inst / "moves").mkdir()
    (inst / "moves" / "point_first.md").write_text("# point first\n")
    r = compare(repo, inst)
    assert r["missing"] == ["moves/point_first.md"]


def test_a_broken_symlink_does_not_crash_the_comparison(tmp_path: Path) -> None:
    repo, inst = pair(tmp_path)
    (repo / "gone.json").symlink_to(tmp_path / "nowhere.json")
    (inst / "gone.json").write_text("real\n")
    r = compare(repo, inst)
    assert "gone.json" in r["differing"]
