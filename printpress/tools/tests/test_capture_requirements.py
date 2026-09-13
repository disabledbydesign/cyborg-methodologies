import json
import subprocess
import sys
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1]
SCRIPT = TOOLS / "capture_requirements.py"
KINDS = (
    "prompts",
    "criteria",
    "eligibility",
    "attachments",
    "budget",
    "formatting",
    "submission_mechanics",
    "reporting",
    "decision_timing",
    "ai_use",
    "governance_disclosures",
)


def run_cli(*args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *(str(arg) for arg in args)],
        capture_output=True,
        text=True,
        check=False,
    )


def initialized_app(tmp_path: Path, posting_text: str = "Complete guidance.") -> Path:
    app = tmp_path / "application"
    app.mkdir()
    (app / "POSTING.md").write_text(posting_text, encoding="utf-8")
    result = run_cli("init", app, "--posting", "POSTING.md")
    assert result.returncode == 0, result.stderr
    return app


def resolve_all_categories(app: Path) -> dict:
    ledger_path = app / "application-requirements.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger["application"].update(
        {"name": "Example application", "funder": "Example funder"}
    )
    ledger["application"]["applicant"] = {
        "type": "institute",
        "legal_name": "The Rustin Institute",
    }
    ledger["application"]["payee"] = {
        "type": "institute",
        "legal_name": "The Rustin Institute",
    }
    for requirement in ledger["requirements"]:
        requirement["status"] = "not_published"
    ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    return ledger


def set_captured(ledger: dict, kind: str, excerpt: str, source: str = "posting") -> None:
    requirement = next(item for item in ledger["requirements"] if item["kind"] == kind)
    requirement.update(
        {
            "status": "captured",
            "source": source,
            "verbatim": excerpt,
            "interpretation": "Kept separate from the quotation.",
        }
    )


def write_ledger(app: Path, ledger: dict) -> None:
    (app / "application-requirements.json").write_text(
        json.dumps(ledger, indent=2) + "\n", encoding="utf-8"
    )


def test_matching_folds_typography_whitespace_and_line_wrapping(tmp_path: Path) -> None:
    app = initialized_app(tmp_path, "The funder says “care” — across\nseveral   lines.")
    ledger = resolve_all_categories(app)
    set_captured(ledger, "prompts", 'The funder says "care" - across several lines.')
    write_ledger(app, ledger)

    assert run_cli("build", app).returncode == 0
    result = run_cli("check", app)

    assert result.returncode == 0, result.stderr
    assert "PASS" in result.stdout


def test_matching_rejects_case_changes(tmp_path: Path) -> None:
    app = initialized_app(tmp_path, "Name the Rustin Institute.")
    ledger = resolve_all_categories(app)
    set_captured(ledger, "prompts", "Name the rustin Institute.")
    write_ledger(app, ledger)

    result = run_cli("build", app)

    assert result.returncode != 0
    assert "verbatim excerpt not found" in result.stderr


def test_matching_rejects_paraphrases(tmp_path: Path) -> None:
    app = initialized_app(tmp_path, "Describe the proposed activities.")
    ledger = resolve_all_categories(app)
    set_captured(ledger, "prompts", "Explain the work you propose.")
    write_ledger(app, ledger)

    result = run_cli("build", app)

    assert result.returncode != 0
    assert "verbatim excerpt not found" in result.stderr


def test_check_rejects_missing_source(tmp_path: Path) -> None:
    app = initialized_app(tmp_path)
    ledger = resolve_all_categories(app)
    set_captured(ledger, "prompts", "Complete guidance.", source="missing")
    write_ledger(app, ledger)

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "unknown source" in result.stderr


def test_check_rejects_removed_posting_source(tmp_path: Path) -> None:
    app = initialized_app(tmp_path)
    ledger = resolve_all_categories(app)
    ledger["sources"] = []
    write_ledger(app, ledger)

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "required posting source" in result.stderr


def test_check_rejects_duplicate_requirement_ids(tmp_path: Path) -> None:
    app = initialized_app(tmp_path)
    ledger = resolve_all_categories(app)
    ledger["requirements"][1]["id"] = ledger["requirements"][0]["id"]
    write_ledger(app, ledger)

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "duplicate requirement id" in result.stderr


def test_check_rejects_invalid_status(tmp_path: Path) -> None:
    app = initialized_app(tmp_path)
    ledger = resolve_all_categories(app)
    ledger["requirements"][0]["status"] = "probably"
    write_ledger(app, ledger)

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "invalid status" in result.stderr


def test_check_rejects_unresolved_required_category(tmp_path: Path) -> None:
    app = initialized_app(tmp_path)
    ledger = resolve_all_categories(app)
    ledger["requirements"][0]["status"] = "unresolved"
    write_ledger(app, ledger)

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "required category remains unresolved" in result.stderr


def test_check_rejects_unresolved_applicant_and_payee(tmp_path: Path) -> None:
    app = initialized_app(tmp_path)
    ledger = resolve_all_categories(app)
    ledger["application"]["applicant"] = {"type": "unresolved", "legal_name": ""}
    ledger["application"]["payee"] = {"type": "unresolved", "legal_name": ""}
    write_ledger(app, ledger)
    assert run_cli("build", app).returncode == 0

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "application.applicant.type remains unresolved" in result.stderr
    assert "application.payee.type remains unresolved" in result.stderr


def test_one_resolved_record_cannot_mask_an_unresolved_required_record(tmp_path: Path) -> None:
    app = initialized_app(tmp_path)
    ledger = resolve_all_categories(app)
    ledger["requirements"].append(
        {
            "id": "prompts-002",
            "kind": "prompts",
            "status": "unresolved",
            "required": True,
            "source": None,
            "verbatim": None,
            "interpretation": "",
            "funder_purpose": "",
            "applies_to": "",
            "notes": "",
        }
    )
    write_ledger(app, ledger)
    assert run_cli("build", app).returncode == 0

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "prompts-002" in result.stderr


def test_check_rejects_stale_generated_ledger(tmp_path: Path) -> None:
    app = initialized_app(tmp_path)
    ledger = resolve_all_categories(app)
    write_ledger(app, ledger)
    assert run_cli("build", app).returncode == 0
    ledger["application"]["name"] = "Changed after build"
    write_ledger(app, ledger)

    result = run_cli("check", app)

    assert result.returncode != 0
    assert "APPLICATION_STRUCTURE.md is stale" in result.stderr


def test_end_to_end_altered_quote_fails_after_successful_run(tmp_path: Path) -> None:
    app = initialized_app(tmp_path, "What becomes possible with this funding?")
    ledger = resolve_all_categories(app)
    set_captured(ledger, "prompts", "What becomes possible with this funding?")
    write_ledger(app, ledger)

    assert run_cli("build", app).returncode == 0
    assert run_cli("check", app).returncode == 0

    ledger["requirements"][0]["verbatim"] = "What will this funding accomplish?"
    write_ledger(app, ledger)
    result = run_cli("check", app)

    assert result.returncode != 0
    assert "verbatim excerpt not found" in result.stderr


def test_init_creates_every_required_kind(tmp_path: Path) -> None:
    app = initialized_app(tmp_path)
    ledger = json.loads((app / "application-requirements.json").read_text(encoding="utf-8"))

    assert tuple(item["kind"] for item in ledger["requirements"]) == KINDS
    assert all(item["status"] == "unresolved" for item in ledger["requirements"])
