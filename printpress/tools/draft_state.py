#!/usr/bin/env python3
"""Maintain the human-gated grant drafting state in DRAFT_STATE.md."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATE_FILE = "DRAFT_STATE.md"
OPEN_MARKER = "<!-- DRAFT_STATE_JSON\n"
CLOSE_MARKER = "\n-->\n"
STAGES = (
    "planning",
    "assembly_ready_for_marking",
    "structural_cut_ready_for_review",
    "compression_ready_for_review",
    "final_check_ready",
    "approved",
)


class StateError(ValueError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def next_stage(stage: str) -> str | None:
    try:
        index = STAGES.index(stage)
    except ValueError:
        return None
    return STAGES[index + 1] if index + 1 < len(STAGES) else None


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_path(app_dir: Path, declared: Any) -> Path:
    if not isinstance(declared, str) or not declared.strip():
        raise StateError("version must name an artifact inside the application folder")
    resolved = (app_dir / declared).resolve()
    try:
        resolved.relative_to(app_dir.resolve())
    except ValueError as exc:
        raise StateError("version must be an artifact inside the application folder") from exc
    return resolved


def read_state(app_dir: Path) -> dict[str, Any]:
    path = app_dir / STATE_FILE
    if not path.is_file():
        raise StateError(f"missing {STATE_FILE}; run init first")
    raw = path.read_text(encoding="utf-8")
    if OPEN_MARKER not in raw or CLOSE_MARKER not in raw:
        raise StateError(f"{STATE_FILE} is missing its machine-readable state block")
    payload = raw.split(OPEN_MARKER, 1)[1].split(CLOSE_MARKER, 1)[0]
    try:
        state = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise StateError(f"invalid JSON state block: {exc}") from exc
    if not isinstance(state, dict):
        raise StateError("state block must contain one JSON object")
    return state


def validate(
    state: dict[str, Any],
    *,
    app_dir: Path | None = None,
    check_artifacts: bool = False,
) -> list[str]:
    errors: list[str] = []
    if state.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    stage = state.get("current_stage")
    if stage not in STAGES:
        errors.append(f"invalid current_stage: {stage!r}")
    authorized = state.get("authorized_next_stage")
    expected = next_stage(stage) if stage in STAGES else None
    if authorized is not None and authorized != expected:
        errors.append(
            f"authorized_next_stage must be {expected!r} from {stage!r}, not {authorized!r}"
        )
    if authorized is not None and not str(state.get("human_direction_received", "")).strip():
        errors.append("authorized_next_stage requires recorded human direction")
    history = state.get("history")
    if not isinstance(history, list):
        errors.append("history must be a list")
        return errors
    previous = "planning"
    turn_ids: set[str] = set()
    for index, event in enumerate(history):
        where = f"history[{index}]"
        if not isinstance(event, dict):
            errors.append(f"{where} must be an object")
            continue
        if event.get("from") != previous:
            errors.append(f"{where}.from must be {previous!r}")
        expected_to = next_stage(previous)
        if event.get("to") != expected_to:
            errors.append(f"{where}.to must be {expected_to!r}")
        previous = event.get("to")
        turn_id = event.get("turn_id")
        if not isinstance(turn_id, str) or not turn_id.strip():
            errors.append(f"{where}.turn_id must be non-empty")
        elif turn_id in turn_ids:
            errors.append(f"{where} reuses turn_id {turn_id!r}")
        else:
            turn_ids.add(turn_id)
        version = event.get("version")
        try:
            path = artifact_path(app_dir, version) if app_dir is not None else None
        except StateError as exc:
            errors.append(f"{where}: {exc}")
            path = None
        ratio = event.get("ratio")
        if not isinstance(ratio, (int, float)) or isinstance(ratio, bool) or ratio <= 0:
            errors.append(f"{where}.ratio must be a positive number")
        digest = event.get("artifact_sha256")
        if not isinstance(digest, str) or len(digest) != 64:
            errors.append(f"{where}.artifact_sha256 must be a SHA-256 digest")
        if check_artifacts and path is not None:
            if not path.is_file():
                errors.append(f"{where} saved artifact is missing: {version}")
            elif isinstance(digest, str) and digest != file_digest(path):
                errors.append(f"{where} immutable artifact changed after advancement: {version}")
    if stage in STAGES and previous != stage:
        errors.append(f"history ends at {previous!r}, not current_stage {stage!r}")
    if history:
        final = history[-1]
        if state.get("current_version") != final.get("version"):
            errors.append("current_version does not match the final history event")
        if state.get("actual_ratio") != final.get("ratio"):
            errors.append("actual_ratio does not match the final history event")
        if state.get("last_advanced_turn_id") != final.get("turn_id"):
            errors.append("last_advanced_turn_id does not match the final history event")
    else:
        if state.get("current_version") is not None:
            errors.append("current_version must be null before the first advancement")
        if state.get("actual_ratio") is not None:
            errors.append("actual_ratio must be null before the first advancement")
        if state.get("last_advanced_turn_id") is not None:
            errors.append("last_advanced_turn_id must be null before the first advancement")
    return errors


def render(state: dict[str, Any]) -> str:
    payload = json.dumps(state, indent=2, ensure_ascii=False)
    history = state.get("history", [])
    lines = [
        OPEN_MARKER.rstrip("\n"),
        payload,
        "-->",
        "# Draft state",
        "",
        "> Machine-maintained by `workflows/tools/draft_state.py`. Use the CLI instead of",
        "> editing the state block by hand. Human markings remain in the draft artifacts.",
        "",
        f"- Current stage: `{state['current_stage']}`",
        f"- Current immutable version: `{state.get('current_version') or 'none'}`",
        f"- Actual word/character ratio: `{state.get('actual_ratio') if state.get('actual_ratio') is not None else 'not measured'}`",
        f"- Human direction received: {state.get('human_direction_received') or 'none recorded'}",
        f"- Items awaiting human judgment: {state.get('awaiting_human_judgment') or 'none recorded'}",
        f"- Authorized next stage: `{state.get('authorized_next_stage') or 'none'}`",
        "",
        "## Stage history",
        "",
        "| From | To | Version | Ratio | Turn | Human direction |",
        "|---|---|---|---:|---|---|",
    ]
    for event in history:
        direction = str(event.get("human_direction", "")).replace("|", "\\|")
        lines.append(
            f"| {event['from']} | {event['to']} | {event['version']} | "
            f"{event['ratio']:.3f} | {event['turn_id']} | {direction} |"
        )
    if not history:
        lines.append("| — | planning | — | — | — | initialized |")
    return "\n".join(lines) + "\n"


def write_state(app_dir: Path, state: dict[str, Any]) -> None:
    (app_dir / STATE_FILE).write_text(render(state), encoding="utf-8")


def init_command(args: argparse.Namespace) -> int:
    app_dir = Path(args.app_dir).resolve()
    app_dir.mkdir(parents=True, exist_ok=True)
    path = app_dir / STATE_FILE
    if path.exists():
        raise StateError(f"refusing to overwrite existing {path}")
    state = {
        "schema_version": 1,
        "current_stage": "planning",
        "current_version": None,
        "actual_ratio": None,
        "human_direction_received": "",
        "awaiting_human_judgment": "Approve or revise DRAFT_PLAN.md before prose begins.",
        "authorized_next_stage": None,
        "last_advanced_turn_id": None,
        "updated_at": now(),
        "history": [],
    }
    write_state(app_dir, state)
    print(f"Created {path}")
    return 0


def authorize_command(args: argparse.Namespace) -> int:
    app_dir = Path(args.app_dir).resolve()
    state = read_state(app_dir)
    errors = validate(state, app_dir=app_dir, check_artifacts=True)
    if errors:
        raise StateError("\n".join(errors))
    expected = next_stage(state["current_stage"])
    if args.next_stage != expected:
        raise StateError(
            f"from {state['current_stage']}, authorized next stage must be {expected}"
        )
    if not args.human_direction.strip():
        raise StateError("human direction must be recorded before authorization")
    state["human_direction_received"] = args.human_direction.strip()
    state["authorized_next_stage"] = args.next_stage
    state["updated_at"] = now()
    write_state(app_dir, state)
    print(f"Authorized {args.next_stage}; no stage has advanced yet")
    return 0


def advance_command(args: argparse.Namespace) -> int:
    app_dir = Path(args.app_dir).resolve()
    state = read_state(app_dir)
    errors = validate(state, app_dir=app_dir, check_artifacts=True)
    if errors:
        raise StateError("\n".join(errors))
    expected = next_stage(state["current_stage"])
    if args.to_stage != expected:
        raise StateError(f"cannot skip: next stage must be {expected}")
    if state.get("authorized_next_stage") != args.to_stage:
        raise StateError(f"stage {args.to_stage} is not authorized by recorded human direction")
    turn_id = args.turn_id.strip()
    if not turn_id:
        raise StateError("turn ID must be non-empty")
    if state.get("last_advanced_turn_id") == turn_id:
        raise StateError(f"turn {turn_id!r} already advanced a stage")
    try:
        ratio = float(args.ratio)
    except ValueError as exc:
        raise StateError("ratio must be a positive number") from exc
    if ratio <= 0:
        raise StateError("ratio must be a positive number")
    version_path = artifact_path(app_dir, args.version)
    if not version_path.is_file():
        raise StateError(f"saved artifact does not exist: {args.version}")
    version = version_path.relative_to(app_dir).as_posix()

    from_stage = state["current_stage"]
    event = {
        "from": from_stage,
        "to": args.to_stage,
        "version": version,
        "artifact_sha256": file_digest(version_path),
        "ratio": ratio,
        "turn_id": turn_id,
        "human_direction": state["human_direction_received"],
        "advanced_at": now(),
    }
    state["history"].append(event)
    state["current_stage"] = args.to_stage
    state["current_version"] = version
    state["actual_ratio"] = ratio
    state["awaiting_human_judgment"] = args.awaiting.strip()
    state["authorized_next_stage"] = None
    state["last_advanced_turn_id"] = turn_id
    state["updated_at"] = now()
    write_state(app_dir, state)
    print(f"Advanced one stage: {from_stage} -> {args.to_stage}")
    return 0


def check_command(args: argparse.Namespace) -> int:
    app_dir = Path(args.app_dir).resolve()
    state = read_state(app_dir)
    errors = validate(state, app_dir=app_dir, check_artifacts=True)
    if errors:
        raise StateError("\n".join(errors))
    print(f"PASS — {state['current_stage']} with {len(state['history'])} completed transition(s)")
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("app_dir")
    init.set_defaults(function=init_command)
    authorize = commands.add_parser("authorize")
    authorize.add_argument("app_dir")
    authorize.add_argument("--next", dest="next_stage", required=True, choices=STAGES[1:])
    authorize.add_argument("--human-direction", required=True)
    authorize.set_defaults(function=authorize_command)
    advance = commands.add_parser("advance")
    advance.add_argument("app_dir")
    advance.add_argument("--to", dest="to_stage", required=True, choices=STAGES[1:])
    advance.add_argument("--version", required=True)
    advance.add_argument("--ratio", required=True)
    advance.add_argument("--awaiting", default="Review the saved artifact before authorizing the next stage.")
    advance.add_argument("--turn-id", required=True)
    advance.set_defaults(function=advance_command)
    check = commands.add_parser("check")
    check.add_argument("app_dir")
    check.set_defaults(function=check_command)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.function(args)
    except StateError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
