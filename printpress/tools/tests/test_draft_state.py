import json
import subprocess
import sys
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
SCRIPT = TOOLS / "draft_state.py"


def run_cli(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
        check=False,
    )


def state_data(app: Path) -> dict:
    text = (app / "DRAFT_STATE.md").read_text(encoding="utf-8")
    raw = text.split("<!-- DRAFT_STATE_JSON\n", 1)[1].split("\n-->\n", 1)[0]
    return json.loads(raw)


def test_state_machine_requires_human_authorization(tmp_path: Path) -> None:
    app = tmp_path / "application"
    app.mkdir()
    assert run_cli("init", app).returncode == 0

    result = run_cli(
        "advance",
        app,
        "--to",
        "assembly_ready_for_marking",
        "--version",
        "answer_v0.md",
        "--ratio",
        "1.70",
        "--turn-id",
        "turn-1",
    )

    assert result.returncode != 0
    assert "not authorized" in result.stderr


def test_state_machine_cannot_skip_a_stage(tmp_path: Path) -> None:
    app = tmp_path / "application"
    app.mkdir()
    assert run_cli("init", app).returncode == 0

    result = run_cli(
        "authorize",
        app,
        "--next",
        "structural_cut_ready_for_review",
        "--human-direction",
        "Proceed.",
    )

    assert result.returncode != 0
    assert "must be assembly_ready_for_marking" in result.stderr


def test_state_machine_advances_one_stage_after_authorization(tmp_path: Path) -> None:
    app = tmp_path / "application"
    app.mkdir()
    assert run_cli("init", app).returncode == 0
    assert (
        run_cli(
            "authorize",
            app,
            "--next",
            "assembly_ready_for_marking",
            "--human-direction",
            "The plan is approved with the stated exclusions.",
        ).returncode
        == 0
    )
    (app / "answer_v0.md").write_text("Assembly\n", encoding="utf-8")

    result = run_cli(
        "advance",
        app,
        "--to",
        "assembly_ready_for_marking",
        "--version",
        "answer_v0.md",
        "--ratio",
        "1.70",
        "--awaiting",
        "KEEP/DROP/UNSURE markings",
        "--turn-id",
        "turn-1",
    )

    assert result.returncode == 0, result.stderr
    state = state_data(app)
    assert state["current_stage"] == "assembly_ready_for_marking"
    assert state["authorized_next_stage"] is None
    assert state["human_direction_received"].startswith("The plan is approved")


def test_state_machine_cannot_advance_twice_in_one_turn(tmp_path: Path) -> None:
    app = tmp_path / "application"
    app.mkdir()
    assert run_cli("init", app).returncode == 0
    assert run_cli(
        "authorize",
        app,
        "--next",
        "assembly_ready_for_marking",
        "--human-direction",
        "Proceed to assembly.",
    ).returncode == 0
    (app / "answer_v0.md").write_text("Assembly\n", encoding="utf-8")
    assert run_cli(
        "advance",
        app,
        "--to",
        "assembly_ready_for_marking",
        "--version",
        "answer_v0.md",
        "--ratio",
        "1.60",
        "--turn-id",
        "same-turn",
    ).returncode == 0
    assert run_cli(
        "authorize",
        app,
        "--next",
        "structural_cut_ready_for_review",
        "--human-direction",
        "Use the markings.",
    ).returncode == 0
    (app / "answer_v1_structural.md").write_text("Structural cut\n", encoding="utf-8")

    result = run_cli(
        "advance",
        app,
        "--to",
        "structural_cut_ready_for_review",
        "--version",
        "answer_v1_structural.md",
        "--ratio",
        "1.35",
        "--turn-id",
        "same-turn",
    )

    assert result.returncode != 0
    assert "already advanced a stage" in result.stderr


def test_check_rejects_invalid_manual_edit(tmp_path: Path) -> None:
    app = tmp_path / "application"
    app.mkdir()
    assert run_cli("init", app).returncode == 0
    path = app / "DRAFT_STATE.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace('"current_stage": "planning"', '"current_stage": "invented"')
    path.write_text(text, encoding="utf-8")

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "invalid current_stage" in result.stderr


def test_check_rejects_changed_immutable_artifact(tmp_path: Path) -> None:
    app = tmp_path / "application"
    app.mkdir()
    assert run_cli("init", app).returncode == 0
    assert run_cli(
        "authorize",
        app,
        "--next",
        "assembly_ready_for_marking",
        "--human-direction",
        "Proceed to assembly.",
    ).returncode == 0
    artifact = app / "answer_v0.md"
    artifact.write_text("Original assembly\n", encoding="utf-8")
    assert run_cli(
        "advance",
        app,
        "--to",
        "assembly_ready_for_marking",
        "--version",
        artifact.name,
        "--ratio",
        "1.75",
        "--turn-id",
        "turn-1",
    ).returncode == 0
    artifact.write_text("Changed after advancement\n", encoding="utf-8")

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "immutable artifact changed" in result.stderr


def test_check_rejects_missing_immutable_artifact(tmp_path: Path) -> None:
    app = tmp_path / "application"
    app.mkdir()
    assert run_cli("init", app).returncode == 0
    assert run_cli(
        "authorize",
        app,
        "--next",
        "assembly_ready_for_marking",
        "--human-direction",
        "Proceed to assembly.",
    ).returncode == 0
    artifact = app / "answer_v0.md"
    artifact.write_text("Original assembly\n", encoding="utf-8")
    assert run_cli(
        "advance",
        app,
        "--to",
        "assembly_ready_for_marking",
        "--version",
        artifact.name,
        "--ratio",
        "1.75",
        "--turn-id",
        "turn-1",
    ).returncode == 0
    artifact.unlink()

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "saved artifact is missing" in result.stderr


def test_check_rejects_state_summary_divergence(tmp_path: Path) -> None:
    app = tmp_path / "application"
    app.mkdir()
    assert run_cli("init", app).returncode == 0
    assert run_cli(
        "authorize",
        app,
        "--next",
        "assembly_ready_for_marking",
        "--human-direction",
        "Proceed to assembly.",
    ).returncode == 0
    (app / "answer_v0.md").write_text("Original assembly\n", encoding="utf-8")
    assert run_cli(
        "advance",
        app,
        "--to",
        "assembly_ready_for_marking",
        "--version",
        "answer_v0.md",
        "--ratio",
        "1.75",
        "--turn-id",
        "turn-1",
    ).returncode == 0
    path = app / "DRAFT_STATE.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace('"current_version": "answer_v0.md"', '"current_version": "other.md"')
    path.write_text(text, encoding="utf-8")

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "current_version does not match" in result.stderr
