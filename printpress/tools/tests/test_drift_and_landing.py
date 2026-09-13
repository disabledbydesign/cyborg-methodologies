"""Tests for the profile drift detector and the landing check.

The drift detector's job is to prove a restatement has diverged from its definition — the
2026-09-13 measurement found a style review's applied wording was 20% of the profile's
text, median similarity 0.11, with every operational test dropped. Its central test is
that it FAILS on that shape and PASSES when the review quotes the definition.

The landing check's central test is the false-alarm case: on its first run it resolved a
redirect stub instead of the canonical file and reported seven landed proposals as missing.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
DRIFT = TOOLS / "check_profile_drift.py"
LANDING = TOOLS / "check_landing.py"

DEFINITION = (
    "Every paragraph opener must make the paragraph's first real content move rather than "
    "announce that a move is coming. TEST: if the sentence could be replaced with 'The "
    "following paragraph discusses X,' it is meta — rewrite it as the X. Anti-pattern: "
    "'These commitments shaped my work.' June: 'At Cabrillo, I developed Ethnic Studies is "
    "a Strike.'"
)
COMPRESSED = ("Every paragraph opener must make the paragraph's first real content move "
              "rather than announce that a move is coming.")


def profile(tmp: Path, instruction: str, cid: str = "topic_sentence_craft") -> Path:
    p = tmp / "profile.json"
    p.write_text(json.dumps({"profile": {"version": "t"}, "qualitative": [
        {"id": cid, "role": "pre_draft", "instruction": instruction}]}))
    return p


def review(tmp: Path, instruction: str, cid: str = "topic_sentence_craft") -> Path:
    p = tmp / "review.md"
    p.write_text(f"# Style review\n\n## 1. `{cid}`\n\n**What it asks for.** {instruction}\n\n"
                 "**Findings:** paragraph 1 VIOLATION.\n")
    return p


def run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True)


# ── check_profile_drift ─────────────────────────────────────────────────────

def test_flags_a_compressed_restatement(tmp_path: Path) -> None:
    r = run(DRIFT, "--profile", str(profile(tmp_path, DEFINITION)),
            "--review", str(review(tmp_path, COMPRESSED)))
    assert r.returncode == 1, r.stdout
    assert "DRIFT" in r.stdout


def test_names_the_operational_content_that_was_dropped(tmp_path: Path) -> None:
    """Losing the TEST is what makes a check unusable, so the tool must say so."""
    r = run(DRIFT, "--profile", str(profile(tmp_path, DEFINITION)),
            "--review", str(review(tmp_path, COMPRESSED)))
    assert "TEST:" in r.stdout and "Anti-pattern" in r.stdout and "June:" in r.stdout


def test_passes_when_the_review_quotes_the_definition(tmp_path: Path) -> None:
    r = run(DRIFT, "--profile", str(profile(tmp_path, DEFINITION)),
            "--review", str(review(tmp_path, DEFINITION)))
    assert r.returncode == 0, r.stdout
    assert "OK" in r.stdout


def test_flags_a_check_invented_during_application(tmp_path: Path) -> None:
    """The same failure running the other way: a review names a check the profile never defined."""
    r = run(DRIFT, "--profile", str(profile(tmp_path, DEFINITION)),
            "--review", str(review(tmp_path, DEFINITION, cid="invented_check")))
    assert r.returncode == 1
    assert "NOT DEFINED" in r.stdout and "invented_check" in r.stdout


def test_reports_the_compression_ratio(tmp_path: Path) -> None:
    r = run(DRIFT, "--profile", str(profile(tmp_path, DEFINITION)),
            "--review", str(review(tmp_path, COMPRESSED)))
    assert "of the definition text" in r.stdout


def test_role_filter_selects_the_right_checks(tmp_path: Path) -> None:
    p = tmp_path / "profile.json"
    p.write_text(json.dumps({"profile": {}, "qualitative": [
        {"id": "topic_sentence_craft", "role": "linter", "instruction": DEFINITION}]}))
    r = run(DRIFT, "--profile", str(p), "--review", str(review(tmp_path, COMPRESSED)),
            "--role", "pre_draft")
    assert "NOT DEFINED" in r.stdout      # filtered out of the comparison set


# ── check_landing ───────────────────────────────────────────────────────────

PROPOSAL_DOC = """# Revision analysis

**1 · `ARG-9` (new) · `INST` · `_application_evidence/DRAFTING_STANDARD.md`**

Some rationale.

**2 · `ARG-99` (new) · `INST` · `_application_evidence/DRAFTING_STANDARD.md`**

More rationale.
"""


def make_landing_ws(tmp: Path, standard_body: str, stub: bool = False) -> tuple[Path, Path]:
    ws = tmp / "ws"
    (ws / "_application_evidence").mkdir(parents=True)
    (ws / "_application_evidence" / "REVISION_ANALYSIS_2026-08-12.md").write_text(PROPOSAL_DOC)
    skill = tmp / "skill"
    skill.mkdir()
    (skill / "DRAFTING_STANDARD.md").write_text(standard_body)
    if stub:
        (ws / "_application_evidence" / "DRAFTING_STANDARD.md").write_text(
            "# DRAFTING_STANDARD.md has moved\n\nCanonical copy: the skill.\n")
    return ws, skill


def test_flags_a_proposal_that_never_landed(tmp_path: Path) -> None:
    ws, skill = make_landing_ws(tmp_path, "**ARG-9** landed here.\n")
    r = run(LANDING, "--workspace", str(ws), "--skill", str(skill))
    assert r.returncode == 1
    assert "NOT LANDED" in r.stdout
    assert "ARG-99" in r.stdout


def test_passes_when_everything_landed(tmp_path: Path) -> None:
    ws, skill = make_landing_ws(tmp_path, "**ARG-9** and **ARG-99** both landed.\n")
    r = run(LANDING, "--workspace", str(ws), "--skill", str(skill))
    assert r.returncode == 0, r.stdout
    assert "OK" in r.stdout


def test_redirect_stub_does_not_cause_false_alarms(tmp_path: Path) -> None:
    """The first-run bug: resolving to the 'has moved' pointer reported every landed
    proposal as missing. Seven false alarms on 2026-09-12."""
    ws, skill = make_landing_ws(tmp_path, "**ARG-9** and **ARG-99** both landed.\n", stub=True)
    r = run(LANDING, "--workspace", str(ws), "--skill", str(skill))
    assert r.returncode == 0, r.stdout
    assert "NOT LANDED" not in r.stdout


def test_amendment_to_existing_item_needs_a_human(tmp_path: Path) -> None:
    """Presence proves a NEW check landed. It cannot prove an amendment was applied."""
    ws = tmp_path / "ws"
    (ws / "_application_evidence").mkdir(parents=True)
    (ws / "_application_evidence" / "REVISION_ANALYSIS_2026-08-12.md").write_text(
        "**4 · `demonstration_over_peroration` (#43) · `pre_draft` · `june_bloch.json` — narrow it.**\n")
    skill = tmp_path / "skill"
    (skill / "..").resolve()
    (tmp_path / "voice-check").mkdir()
    (tmp_path / "voice-check" / "june_bloch.json").write_text('{"x": "demonstration_over_peroration"}')
    skill.mkdir()
    r = run(LANDING, "--workspace", str(ws), "--skill", str(skill))
    assert "NEEDS HUMAN CONFIRMATION" in r.stdout
    assert r.returncode == 0
