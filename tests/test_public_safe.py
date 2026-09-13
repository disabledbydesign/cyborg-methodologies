"""Tests for check_public_safe.py — the pre-push guard on a public repository.

CLAUDE.md carried this rule in prose from the beginning and it was broken anyway,
because it told you to keep the grep pattern in HANDOFF.md, which is gitignored.
These tests exist so the executable version cannot rot the same way.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check_public_safe.py"


def repo(tmp_path: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    return tmp_path


def add(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    subprocess.run(["git", "-C", str(root), "add", "-f", rel], check=True)


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), "--repo", str(root)],
                          capture_output=True, text=True)


def test_a_clean_repo_passes(tmp_path: Path) -> None:
    r = repo(tmp_path)
    add(r, "SKILL.md", "# method\n")
    assert run(r).returncode == 0


def test_a_voice_profile_blocks_the_push(tmp_path: Path) -> None:
    """june_bloch.json is a model of how one person writes, built from her
    unpublished drafts. A push cannot be taken back."""
    r = repo(tmp_path)
    add(r, "voice-check/profiles/june_bloch.json", '{"profile": {}}\n')
    out = run(r)
    assert out.returncode == 1
    assert "june_bloch.json" in out.stdout


def test_the_shareable_base_profile_is_allowed(tmp_path: Path) -> None:
    """The rule is about the person, not the word 'profile'. base.json is method."""
    r = repo(tmp_path)
    add(r, "voice-check/profiles/base.json", '{"profile": {}}\n')
    assert run(r).returncode == 0


def test_extracts_and_audits_of_the_profile_block_too(tmp_path: Path) -> None:
    """TEST_B_PREDRAFT_EXTRACT.json is a third of the profile under another name.
    Blocking only the file called june_bloch.json would miss it."""
    r = repo(tmp_path)
    for rel in ("voice-check/TEST_B_PREDRAFT_EXTRACT.json",
                "voice-check/AUDIT_REPORT_2026-05-06.md",
                "voice-check/AGENT_FEEDBACK_2026-05-02.md",
                "voice-check/PROFILE_CHANGE_LOG.md"):
        add(r, rel, "content\n")
    out = run(r)
    assert out.returncode == 1
    for name in ("TEST_B_PREDRAFT_EXTRACT", "AUDIT_REPORT", "AGENT_FEEDBACK",
                 "PROFILE_CHANGE_LOG"):
        assert name in out.stdout


def test_a_credential_blocks_the_push(tmp_path: Path) -> None:
    r = repo(tmp_path)
    add(r, "cfg.py", 'KEY = "sk-ant-' + "A" * 28 + '"\n')
    out = run(r)
    assert out.returncode == 1
    assert "Anthropic API key" in out.stdout


def test_test_fixtures_are_not_credentials(tmp_path: Path) -> None:
    """rustin-tools has nineteen files with password= in them; every one is a test
    fixture. Flagging those trains you to push with --no-verify."""
    r = repo(tmp_path)
    add(r, "tests/test_send.py", 'send(password="app-password")\nKEY = os.getenv("API_KEY")\n')
    assert run(r).returncode == 0


def test_home_paths_warn_but_do_not_block(tmp_path: Path) -> None:
    """Sixteen tracked files already have them. A guard that fails every time is a
    guard that gets bypassed every time."""
    r = repo(tmp_path)
    add(r, "PIPELINE.md", "Read `/Users/june/Documents/GitHub/profile/BRIEFING.md`.\n")
    out = run(r)
    assert out.returncode == 0
    assert "WARN" in out.stdout
    assert "PIPELINE.md" in out.stdout


def test_the_hook_installs_and_points_at_this_script(tmp_path: Path) -> None:
    r = repo(tmp_path)
    out = subprocess.run([sys.executable, str(SCRIPT), "--repo", str(r), "--install"],
                         capture_output=True, text=True)
    assert out.returncode == 0
    hook = r / ".git" / "hooks" / "pre-push"
    assert hook.exists() and hook.stat().st_mode & 0o111
    assert "check_public_safe.py" in hook.read_text()
